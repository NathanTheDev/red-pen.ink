from pathlib import Path

import faiss
from refactor.feedback.core.ml.index import (
    build_index_from_json,
    load_tags,
    save_tags,
    unpack_tag_id,
)
from refactor.feedback.schemas.records import DocumentRecord

DATA_DIR = Path(__file__).parents[2] / "data"
DATA_DIR.mkdir(parents=False, exist_ok=True)

NEUTRAL_JSON_PATH = DATA_DIR / "neutral.json"
FEEDBACK_JSON_PATH = DATA_DIR / "feedback.json"

_state: dict = {
    "neutral_index": None,
    "neutral_records": None,
    "feedback_index": None,
    "feedback_records": None,
}


def _get_tag_text(records: dict[int, DocumentRecord], tag_id: int) -> str | None:
    doc_id, _ = unpack_tag_id(tag_id)
    record = records.get(doc_id)
    if record is None:
        return None
    return next((t.tag for t in record.tags if t.tag_id == tag_id), None)


def get_neutral_tag(tag_id: int) -> str | None:
    return _get_tag_text(get_neutral_records(), tag_id)


def get_feedback_tag(tag_id: int) -> str | None:
    return _get_tag_text(get_feedback_records(), tag_id)


def get_neutral_records() -> dict[int, DocumentRecord]:
    if _state["neutral_records"] is None:
        _state["neutral_records"] = load_tags(NEUTRAL_JSON_PATH)
    return _state["neutral_records"]


def get_feedback_index() -> faiss.IndexIDMap:
    if _state["feedback_index"] is None:
        _state["feedback_index"] = build_index_from_json(FEEDBACK_JSON_PATH)
    return _state["feedback_index"]


def get_feedback_records() -> dict[int, DocumentRecord]:
    if _state["feedback_records"] is None:
        _state["feedback_records"] = load_tags(FEEDBACK_JSON_PATH)
    return _state["feedback_records"]


def reload_neutral(records: list[DocumentRecord]) -> None:
    save_tags(NEUTRAL_JSON_PATH, records)
    _state["neutral_records"] = {r.doc_id: r for r in records}
    _state["neutral_index"] = build_index_from_json(NEUTRAL_JSON_PATH)


def reload_feedback(records: list[DocumentRecord]) -> None:
    save_tags(FEEDBACK_JSON_PATH, records)
    _state["feedback_re cords"] = {r.doc_id: r for r in records}
    _state["feedback_index"] = build_index_from_json(FEEDBACK_JSON_PATH)
