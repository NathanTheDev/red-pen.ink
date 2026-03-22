import spacy

NLP = spacy.load("en_core_web_lg")


def _remove_proper_nouns(tags: list[str]) -> list[str]:
    return [tag for tag in tags if not any(tok.pos_ == "PROPN" for tok in NLP(tag))]


def _clean_dash(tag: str) -> str:
    return tag.split("–", maxsplit=1)[0].split("-")[0].strip()


def clean_tags(tags: list[str]) -> list[str]:
    return _remove_proper_nouns([_clean_dash(tag) for tag in tags])
