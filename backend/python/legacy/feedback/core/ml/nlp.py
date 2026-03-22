import re

import spacy

NLP = spacy.load("en_core_web_lg")

_PUNCT = re.compile(r"[^\w\s]")


def _remove_punctuation(tag: str) -> str:
    return _PUNCT.sub("", tag).strip()


def _remove_proper_nouns(tags: list[str]) -> list[str]:
    return [tag for tag in tags if not any(tok.pos_ == "PROPN" for tok in NLP(tag))]


def _truncate(tag: str, max_words: int | None = None) -> str:
    words = tag.split()
    return " ".join(words[:max_words]) if max_words else tag


def clean_tags(tags: list[str], max_words: int | None = None) -> list[str]:
    cleaned = [
        _truncate(_remove_punctuation(tag), max_words) for tag in tags if tag.strip()
    ]
    return _remove_proper_nouns(cleaned)


def to_sentences(text: str) -> list[str]:
    return [sent.text.strip() for sent in NLP(text).sents if sent.text.strip()]
