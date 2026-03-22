from collections.abc import Callable

from feedback.core.ml.index import gen_doc_id, gen_tag_id
from feedback.core.ml.nlp import to_sentences
from feedback.core.tag.tag import (
    extract_feedback_tags,
    extract_quality_tags,
    extract_technique_tags,
)
from feedback.models.records import DocumentRecord, TagRecord


def _tag_texts[T](
    filename: str,
    items: list[T],
    tag_fn: Callable[[T], list[str]],
) -> DocumentRecord:
    doc_id = gen_doc_id()
    tag_records: list[TagRecord] = []

    tag_idx = 0
    for idx, item in enumerate(items):
        for tag in tag_fn(item):
            tag_records.append(
                TagRecord(tag_id=gen_tag_id(doc_id, tag_idx), tag=tag, sentence_idx=idx)
            )
            tag_idx += 1

    return DocumentRecord(doc_id=doc_id, filename=filename, tags=tag_records)


def tag_good(filename: str, raw_text: str, context: str) -> DocumentRecord:
    return _tag_texts(
        filename,
        to_sentences(raw_text),
        lambda s: extract_technique_tags(s, context),
    )


def tag_marked(
    filename: str,
    pairs: list[tuple[str, str]],
    context: str,
) -> DocumentRecord:
    return _tag_texts(
        filename,
        pairs,
        lambda pair: extract_feedback_tags(pair[0], pair[1], context),
    )


def tag_quality(filename: str, raw_text: str, context: str) -> DocumentRecord:
    return _tag_texts(
        filename,
        to_sentences(raw_text),
        lambda s: extract_quality_tags(s, context),
    )
