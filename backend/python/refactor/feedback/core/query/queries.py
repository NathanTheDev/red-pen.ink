import json
import re

from refactor.feedback.core.ml.llm import llm
from refactor.feedback.core.ml.nlp import clean_tags
from refactor.feedback.core.query.prompts import (
    ANALYSIS_PROMPT,
    FEEDBACK_PROMPT,
    NEUTRAL_PROMPT,
    RESPONSE_PROMPT,
    build_prompt,
)

_JSON_FENCE = re.compile(r"```json|```")


def _parse_json(text: str) -> list:
    stripped = _JSON_FENCE.sub("", text).strip()
    result = json.loads(stripped)
    if result and isinstance(result[0], list):
        result = [item for sublist in result for item in sublist]
    return result


def _extract(prompt_template: str, parts: list[str]) -> list[str]:
    answer = llm.query(build_prompt(prompt_template, *parts))
    if answer is None:
        return []
    try:
        return clean_tags([t for t in _parse_json(answer) if isinstance(t, str)])
    except (json.JSONDecodeError, TypeError, IndexError):
        return []


def _ctx(context: str) -> str:
    return f'Context: "{context}"' if context else ""


def extract_analysis_tags(sentence: str, context: str) -> list[str]:
    return _extract(ANALYSIS_PROMPT, [f'Sentence: "{sentence}"', _ctx(context)])


def extract_neutral_tags(sentence: str, context: str) -> list[str]:
    return _extract(NEUTRAL_PROMPT, [f'Sentence: "{sentence}"', _ctx(context)])


def extract_feedback_tags(sentence: str, comment: str, context: str) -> list[str]:
    return _extract(
        FEEDBACK_PROMPT,
        [f'Sentence: "{sentence}"', f'Comment: "{comment}"', _ctx(context)],
    )


def generate_response_feedback(
    pairs: list[tuple[str, str]], full_text: str
) -> list[str] | None:
    numbered = "\n".join(
        f'{i + 1}. Sentence: "{s}"\n   Similar comment: "{c}"'
        for i, (s, c) in enumerate(pairs)
    )
    answer = llm.query(
        build_prompt(
            RESPONSE_PROMPT,
            f'Full passage:\n"{full_text}"',
            f"Pairs:\n{numbered}",
        )
    )
    if answer is None:
        return None
    try:
        result = _parse_json(answer)
        return (
            [r for r in result if isinstance(r, str)]
            if len(result) == len(pairs)
            else None
        )
    except (json.JSONDecodeError, TypeError, IndexError):
        return None
