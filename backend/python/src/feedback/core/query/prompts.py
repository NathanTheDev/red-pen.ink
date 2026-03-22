# ruff: noqa: E501

_MIN_WORDS = 3
_MAX_WORDS = 7

NEUTRAL_PROMPT = (
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

ANALYSIS_PROMPT = (
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

FEEDBACK_PROMPT = (
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

RESPONSE_PROMPT = (
    "A teacher has left comments on student essay sentences similar to those in the passage below.\n\n"
    "For each (sentence, similar comment) pair, write a short direct comment for that sentence.\n"
    "Write as a teacher addressing the student directly.\n"
    "You have the full passage for context, avoid redundant or repeated feedback.\n"
    "Do not reference the similar sentence or comment explicitly.\n"
    "2-3 sentences per comment maximum.\n"
    "Respond with a JSON array of strings, one comment per pair, in the same order.\n"
    "Respond with a JSON array of strings and nothing else.\n"
)


def build_prompt(*parts: str) -> str:
    return "\n\n".join(p for p in parts if p)
