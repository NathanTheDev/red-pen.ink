# ruff: noqa: E501

import json
import re

from feedback.core.ml.llm import query
from feedback.core.ml.nlp import clean_tags

_MIN_WORDS = 3
_MAX_WORDS = 7

_JSON_FENCE = re.compile(r"```json|```")

_QUALITY_PROMPT = (
    "Analyse this student essay sentence against strong analytical writing.\n\n"
    "Identify what analytical moves are present and what is notably absent or incomplete.\n"
    "Describe the sentence's analytical quality as observable tags. Not suggestions, not instructions.\n\n"
    f"- Must have {_MIN_WORDS}-{_MAX_WORDS} words per tag\n"
    "- Describe what the sentence does AND what it stops short of\n"
    "- Tag completed moves: 'technique identified and named'\n"
    "- Tag incomplete moves: 'technique named without effect explained'\n"
    "- Tag absent moves: 'significance of technique not addressed'\n"
    "- No proper nouns, no character names, no text titles\n"
    "- Tags must be reusable for any student on any text\n"
    '- Example: ["technique identified but not analysed", "claim made without textual support", "effect of device left unexplored", "analytical move initiated but incomplete"]\n\n'
    "Respond with a JSON array of strings and nothing else\n"
)

_TECHNIQUE_PROMPT = (
    "Identify the analytical and writing techniques present in this sentence as a list of tags\n\n"
    "- Describe only what the sentence is doing\n"
    f"- Must have {_MIN_WORDS}-{_MAX_WORDS} words per tag\n"
    "- Describe the move being made, even if incomplete\n"
    "- Do not suggest improvements\n"
    "- No proper nouns, no character names, no text titles\n"
    "- Tags must be reusable for any student on any text\n"
    '- Example: ["juxtaposition reveals character contradiction", "contrast used to interrogate theme", "surface detail undercuts deeper meaning"]\n\n'
    "Respond with a JSON array of strings and nothing else\n"
)

_FEEDBACK_PROMPT = (
    "Extract tags from this teacher comment on a student essay.\n\n"
    "For each comment identify:\n"
    "1. What the teacher wants the student to improve or address\n"
    "2. The intent behind the comment — what writing move is being demanded\n"
    "3. The specific gap — what the student did versus what they should have done\n\n"
    "Every tag must describe a writing behaviour, not a textual event.\n"
    f"- Must have {_MIN_WORDS}-{_MAX_WORDS} words per tag\n"
    "- Tag the gap: what is missing or underdeveloped\n"
    "- Tag the demand: what writing move is being asked for\n"
    "- Tag the writing behaviour: what the student did instead of what was needed\n"
    "- No proper nouns, no character names, no text titles\n"
    "- Tags must be reusable for any student on any text\n"
    '- Example: ["analysis absent from evidence", "surface reading not interrogated", "technique named without effect explained"]\n\n'
    "Respond with a JSON array of strings and nothing else\n"
)

_SIMILAR_FEEDBACK_PROMPT = (
    "A teacher left a comment on a student essay sentence similar to yours.\n\n"
    "Based on that sentence and comment pair, write a short, direct comment for the new sentence.\n"
    "Write as a teacher addressing the student directly.\n"
    "You have the full passage for context — do not repeat feedback already implied by surrounding sentences.\n"
    "Do not reference the original sentence or comment explicitly.\n"
    "2-3 sentences maximum.\n"
)

_BULK_FEEDBACK_PROMPT = (
    "A teacher has left comments on student essay sentences similar to those in the passage below.\n\n"
    "For each (sentence, similar comment) pair, write a short direct comment for that sentence.\n"
    "Write as a teacher addressing the student directly.\n"
    "You have the full passage for context, avoid redundant or repeated feedback.\n"
    "Do not reference the similar sentence or comment explicitly.\n"
    "2-3 sentences per comment maximum.\n"
    "Respond with a JSON array of strings, one comment per pair, in the same order.\n"
    "Respond with a JSON array of strings and nothing else.\n"
)


def _build_prompt(*parts: str) -> str:
    return "\n\n".join(p for p in parts if p)


def _extract(prompt_template: str, parts: list[str]) -> list[str]:
    prompt = _build_prompt(prompt_template, *parts)
    answer = query(prompt)
    if answer is None:
        return []
    clean = _JSON_FENCE.sub("", answer).strip()
    try:
        result = json.loads(clean)
        if result and isinstance(result[0], list):
            result = [item for sublist in result for item in sublist]
        return clean_tags([tag for tag in result if isinstance(tag, str)])
    except json.JSONDecodeError:
        return []


def extract_quality_tags(sentence: str, context: str) -> list[str]:
    return _extract(
        _QUALITY_PROMPT,
        [
            f'Sentence: "{sentence}"',
            f'Context: "{context}"' if context else "",
        ],
    )


def extract_technique_tags(sentence: str, context: str) -> list[str]:
    return _extract(
        _TECHNIQUE_PROMPT,
        [
            f'Sentence: "{sentence}"',
            f'Context: "{context}"' if context else "",
        ],
    )


def extract_feedback_tags(sentence: str, comment: str, context: str) -> list[str]:
    return _extract(
        _FEEDBACK_PROMPT,
        [
            f'Sentence: "{sentence}"',
            f'Comment: "{comment}"',
            f'Context: "{context}"' if context else "",
        ],
    )


def generate_similar_feedback(
    sentence: str, similar_sentence: str, similar_comment: str, full_text: str
) -> str | None:
    prompt = _build_prompt(
        _SIMILAR_FEEDBACK_PROMPT,
        f'Full passage:\n"{full_text}"',
        f'Similar sentence: "{similar_sentence}"',
        f'Teacher comment: "{similar_comment}"',
        f'Student sentence: "{sentence}"',
    )
    return query(prompt)


def generate_bulk_feedback(
    pairs: list[tuple[str, str]], full_text: str
) -> list[str] | None:
    numbered = "\n".join(
        f'{i + 1}. Sentence: "{s}"\n   Similar comment: "{c}"'
        for i, (s, c) in enumerate(pairs)
    )
    prompt = _build_prompt(
        _BULK_FEEDBACK_PROMPT,
        f'Full passage:\n"{full_text}"',
        f"Pairs:\n{numbered}",
    )
    answer = query(prompt)
    if answer is None:
        return None
    clean = _JSON_FENCE.sub("", answer).strip()
    try:
        result = json.loads(clean)
        if len(result) != len(pairs):
            return None
        return [r for r in result if isinstance(r, str)]
    except json.JSONDecodeError:
        return None
