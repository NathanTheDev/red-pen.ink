# ruff: noqa: B008

from fastapi import APIRouter, File, HTTPException, UploadFile
from refactor.feedback.config import get_feedback_index, get_feedback_tag
from refactor.feedback.core.ml.llm import llm
from refactor.feedback.core.ml.nlp import to_sentences
from refactor.feedback.core.query.queries import generate_response_feedback
from refactor.feedback.schemas.response import Annotation, CheckResponse
from refactor.feedback.utils.parse import read_docx
from refactor.feedback.utils.tag import tag_analysis

SIM_THRESHOLD = 0.8

router = APIRouter()


# Parameter names from legacy
@router.post("/check")
async def check(
    file: UploadFile = File(...),
) -> CheckResponse:
    if not file.filename or not file.filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=400, detail=f"{file.filename} is not a .docx file"
        )

    content = await read_docx(file)
    analysis_records = tag_analysis(file.filename, content, context="")

    tags = [t.tag for t in analysis_records.tags]
    embs = llm.embed(tags)

    scores, ids = get_feedback_index().search(embs, k=1)  # type: ignore

    sentences = to_sentences(content)
    results: list[tuple[str, str]] = []
    seen: set[str] = set()

    for score_row, id_row, quality_tag in zip(
        scores, ids, analysis_records.tags, strict=False
    ):
        if float(score_row[0]) < SIM_THRESHOLD:
            continue
        sentence = sentences[quality_tag.sentence_idx]
        if sentence in seen:
            continue
        seen.add(sentence)
        tag = get_feedback_tag(int(id_row[0]))
        if tag is None:
            continue
        results.append((sentence, tag))

    feedback_list = generate_response_feedback(results, content)
    if feedback_list is None:
        return CheckResponse(content=content, annotations=[])

    return CheckResponse(
        content=content,
        annotations=[
            Annotation(span=sentence, comment=comment)
            for (sentence, _), comment in zip(results, feedback_list, strict=False)
        ],
    )
