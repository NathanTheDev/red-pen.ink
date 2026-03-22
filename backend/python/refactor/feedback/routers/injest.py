# ruff: noqa: B008

from fastapi import APIRouter, File, Form, Response, UploadFile
from refactor.feedback.config import reload_feedback, reload_neutral
from refactor.feedback.utils.parse import extract_docx_comments, read_docx
from refactor.feedback.utils.tag import tag_feedback, tag_neutral

router = APIRouter()


# Parameter names from legacy
@router.post("/ingest")
async def ingest(
    good: list[UploadFile] = File(...),
    marked: list[UploadFile] = File(...),
    module_context: str = Form(...),
) -> Response:
    valid_neutral = [
        f for f in good if f.filename and f.filename.lower().endswith(".docx")
    ]
    valid_feedback = [
        f for f in marked if f.filename and f.filename.lower().endswith(".docx")
    ]

    neutral_records = []
    for f in valid_neutral:
        raw_text = await read_docx(f)
        neutral_records.append(tag_neutral(f.filename or "", raw_text, module_context))

    feedback_records = []
    for f in valid_feedback:
        feedback_pairs = await extract_docx_comments(f)
        feedback_records.append(
            tag_feedback(f.filename or "", feedback_pairs, module_context)
        )

    reload_neutral(neutral_records)
    reload_feedback(feedback_records)

    return Response(status_code=200)
