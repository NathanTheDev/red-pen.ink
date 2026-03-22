import logging
import os
from contextlib import asynccontextmanager

import faiss
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
    get_all_cors_headers,
    init,
)
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe import emailpassword, session

from feedback.core.ml.index import (
    build_index_from_json,
    load_tags,
    save_tags,
    unpack_tag_id,
)
from feedback.core.ml.llm import embed
from feedback.core.ml.nlp import to_sentences
from feedback.core.tag.tag import generate_bulk_feedback
from feedback.models.response import Annotation
from feedback.sandbox import GOOD_PATH, MASKED_PATH
from feedback.util import extract_docx_comments, read_docx
from feedback.utils.extract import tag_good, tag_marked, tag_quality

load_dotenv()

init(
    app_info=InputAppInfo(
        app_name="red.ink",
        api_domain="http://localhost:8080",
        website_domain="http://localhost:3001",
        api_base_path="/auth",
        website_base_path="/login",
    ),
    supertokens_config=SupertokensConfig(
        connection_uri=os.environ["SUPERTOKENS_CONNECTION_URI"],
        api_key=os.environ["SUPERTOKENS_API_KEY"],
    ),
    framework="fastapi",
    recipe_list=[
        emailpassword.init(),
        session.init(),
    ],
    mode="asgi",
)

LOGGER = logging.getLogger("uvicorn")

good_index: faiss.IndexIDMap | None = None
mark_index: faiss.IndexIDMap | None = None


def reload_indexes() -> None:
    global good_index, mark_index
    good_index, mark_index = (
        build_index_from_json(GOOD_PATH),
        build_index_from_json(MASKED_PATH),
    )


def get_indexes() -> tuple[faiss.IndexIDMap, faiss.IndexIDMap]:
    if good_index is None or mark_index is None:
        raise RuntimeError("Indexes not loaded — call /ingest first")
    return good_index, mark_index


def _validate_docx(file: UploadFile) -> None:
    if not file.filename or not file.filename.endswith(".docx"):
        raise HTTPException(
            status_code=400, detail=f"{file.filename} is not a .docx file"
        )
    LOGGER.info(f"Received: {file.filename}")


@asynccontextmanager
async def _lifespan(_: FastAPI):
    LOGGER.info("Feedback service started. Loading model.")
    reload_indexes()
    yield
    LOGGER.info("Feedback quality service shutting down.")


app = FastAPI(
    title="Feedback Service",
    lifespan=_lifespan,
)

app.add_middleware(get_middleware())
# app.add_middleware(TrustedHostMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)


@app.get("/", include_in_schema=False)
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
async def ingest(
    good: list[UploadFile] = File(...),  # noqa: B008
    marked: list[UploadFile] = File(...),  # noqa: B008
    module_context: str = Form(...),  # noqa: B008
) -> Response:
    for file in good:
        _validate_docx(file)
    for file in marked:
        _validate_docx(file)

    good_records = []
    for file in good:
        raw_text = await read_docx(file)
        good_records.append(tag_good(file.filename or "", raw_text, module_context))

    marked_records = []
    for file in marked:
        feedback_pairs = await extract_docx_comments(file)
        marked_records.append(tag_marked(file.filename or "", feedback_pairs, module_context))

    save_tags(GOOD_PATH, good_records)
    save_tags(MASKED_PATH, marked_records)

    reload_indexes()

    return Response(status_code=200)


class CheckResponse(BaseModel):
    content: str
    annotations: list[Annotation]


SIM_THRESHOLD = 0.70


@app.post("/check", response_model=CheckResponse)
async def check(
    file: UploadFile = File(...),  # noqa: B008
) -> CheckResponse:
    _validate_docx(file)

    raw_text = await read_docx(file)
    record = tag_quality("", raw_text, context="")
    tags = [t.tag for t in record.tags]
    embs = embed(tags)

    scores, ids = mark_index.search(embs, k=1)  # type: ignore
    mark_records = load_tags(MASKED_PATH)
    sentences = to_sentences(raw_text)

    results = []
    for quality_tag, (score_row, id_row) in zip(
        record.tags, zip(scores, ids, strict=False), strict=False
    ):
        if float(score_row[0]) < SIM_THRESHOLD:
            continue
        doc_id, tag_idx = unpack_tag_id(int(id_row[0]))
        matched_tag = mark_records[doc_id].tags[tag_idx].tag
        results.append((sentences[quality_tag.sentence_idx], matched_tag))

    feedback_list = generate_bulk_feedback(results, raw_text)
    if feedback_list is None:
        return CheckResponse(content=raw_text, annotations=[])

    return CheckResponse(
        content=raw_text,
        annotations=[
            Annotation(span=sentence, comment=comment)
            for (sentence, _), comment in zip(results, feedback_list, strict=False)
        ],
    )
