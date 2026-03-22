from collections.abc import Callable

from refactor.feedback.core.ml.index import gen_doc_id, gen_tag_id
from refactor.feedback.core.ml.nlp import to_sentences
from refactor.feedback.core.query.queries import (
    extract_analysis_tags,
    extract_feedback_tags,
    extract_neutral_tags,
)
from refactor.feedback.schemas.records import DocumentRecord, TagRecord


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


def tag_neutral(filename: str, raw_text: str, context: str) -> DocumentRecord:
    return _tag_texts(
        filename,
        to_sentences(raw_text),
        lambda s: extract_neutral_tags(s, context),
    )


def tag_feedback(
    filename: str,
    pairs: list[tuple[str, str]],
    context: str,
) -> DocumentRecord:
    return _tag_texts(
        filename,
        pairs,
        lambda pair: extract_feedback_tags(pair[0], pair[1], context),
    )


def tag_analysis(filename: str, raw_text: str, context: str) -> DocumentRecord:
    return _tag_texts(
        filename,
        to_sentences(raw_text),
        lambda s: extract_analysis_tags(s, context),
    )
