import json
import random
from pathlib import Path

import faiss
import numpy as np

from feedback.core.ml.llm import embed
from feedback.models.records import DocumentRecord

MAX_TAGS_PER_DOCUMENT = 1000


def gen_doc_id() -> int:
    return random.randint(1, 2**31 // MAX_TAGS_PER_DOCUMENT) * MAX_TAGS_PER_DOCUMENT


def gen_tag_id(doc_id: int, tag_idx: int) -> int:
    return doc_id + tag_idx


def unpack_tag_id(tag_id: int) -> tuple[int, int]:
    doc_id = (tag_id // MAX_TAGS_PER_DOCUMENT) * MAX_TAGS_PER_DOCUMENT
    tag_idx = tag_id % MAX_TAGS_PER_DOCUMENT
    return doc_id, tag_idx


def _build_id_index(embs: np.ndarray, ids: list[int]) -> faiss.IndexIDMap:
    dim = embs.shape[1]
    base = faiss.IndexFlatIP(dim)
    index = faiss.IndexIDMap(base)
    index.add_with_ids(embs, np.array(ids, dtype="int64"))  # type: ignore
    return index


def build_index_from_json(path: Path) -> faiss.IndexIDMap:
    records = load_tags(path)
    tags: list[str] = []
    ids: list[int] = []

    for record in records.values():
        for t in record.tags:
            tags.append(t.tag)
            ids.append(t.tag_id)

    if not tags:
        raise ValueError(f"No tags found in {path}")

    embs = embed(tags)
    return _build_id_index(embs, ids)


def load_tags(load_path: Path) -> dict[int, DocumentRecord]:
    if load_path.exists():
        raw = json.loads(load_path.read_text())
        return {int(k): DocumentRecord.model_validate(v) for k, v in raw.items()}
    return {}


def save_tags(save_path: Path, records: list[DocumentRecord]) -> None:
    save_path.write_text(
        json.dumps(
            {str(r.doc_id): r.model_dump(mode="json") for r in records},
            indent=2,
        )
    )
