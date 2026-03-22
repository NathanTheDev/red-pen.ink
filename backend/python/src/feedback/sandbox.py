# ruff: noqa: E501


from feedback.config import DATA_DIR
from feedback.core.ml.index import (
    build_index_from_json,
    load_tags,
    save_tags,
)
from feedback.utils.extract import (
    tag_good,
    tag_marked,
)

GOOD_EXAMPLE = (
    "Shakespeare constructs Prospero as a figure whose authority is fundamentally inseparable from his capacity for violence. "
    "Through the opening tempest, the playwright frames power not as benevolent governance but as an act of deliberate destabilisation. "
    "The storm is not merely atmospheric but structural — it unsettles the audience's assumptions about who holds legitimate control over the island. "
    "By positioning Prospero as the architect of this chaos, Shakespeare implicates him in the very disorder he claims to resolve."
)
MARKED_EXAMPLE = "Shakespeare employs the metaphor of the tempest to interrogate the moral legitimacy of Prospero's authority."
MARKED_COMMENT = "You've identified the metaphor but not explained what it constructs — why does Shakespeare use the tempest specifically to frame questions of authority?"

MODULE_CONTEXT = "HSC English Advanced. Prescribed text: The Tempest. Rubric criteria: thesis, evidence, analysis, conceptual depth, contextual knowledge"

WEAK_EXAMPLE = "Prospero uses magic to control the island and its inhabitants."
QUAITY_THRESHOLD = 0.7

GOOD_PATH = DATA_DIR / "good.json"
MASKED_PATH = DATA_DIR / "marked.json"


if __name__ == "__main__":
    good_record = tag_good("good.docx", GOOD_EXAMPLE, MODULE_CONTEXT)
    marked_record = tag_marked(
        "marked1.docx", [(MARKED_EXAMPLE, MARKED_COMMENT)], MODULE_CONTEXT
    )

    # Will be linked to the final save after route call
    save_tags(GOOD_PATH, [good_record])
    save_tags(MASKED_PATH, [marked_record])

    # Add a way to append if memory index is active

    good_index = build_index_from_json(GOOD_PATH)
    mark_index = build_index_from_json(MASKED_PATH)

    good_records = load_tags(GOOD_PATH)
    marked_records = load_tags(MASKED_PATH)

    # weak_tags = extract_quality_tags(WEAK_EXAMPLE, MODULE_CONTEXT)
    # weak_embs = embed(weak_tags)

    # scores, ids = good_index.search(weak_embs, k=5)  # type: ignore

    # matched = {unpack_tag_id(int(tid)) for row in ids for tid in row}
    # matched_doc_id = Counter(doc_id for doc_id, _ in matched).most_common(1)[0][0]
    # similar_doc = good_records[matched_doc_id]

    # matched_idxs = {tag_idx for doc_id, tag_idx in matched if doc_id == matched_doc_id}
    # gap_idxs = set()
    # for idx in range(len(similar_doc.tags)):
    #     tag = similar_doc.tags[idx].tag
    #     tag_emb = embed([tag])
    #     sim = float((tag_emb @ weak_embs.T).max())
    #     if sim < QUAITY_THRESHOLD:
    #         gap_idxs.add(idx)

    # print("Matched:")
    # for idx in sorted(matched_idxs):
    #     print(f"  {similar_doc.tags[idx].tag}")

    # print("\nGaps:")
    # for idx in sorted(gap_idxs):
    #     print(f"  {similar_doc.tags[idx].tag}")

    # scores, ids = mark_index.search(weak_embs, k=5)  # type: ignore
    # matched = {unpack_tag_id(int(tid)) for row in ids for tid in row}
    # matched_doc_id = Counter(doc_id for doc_id, _ in matched).most_common(1)[0][0]
    # matched_idxs = {tag_idx for doc_id, tag_idx in matched if doc_id == matched_doc_id}

    # print("Feedback:")
    # for idx in sorted(matched_idxs):
    #     print(f"  {marked_records[matched_doc_id].tags[idx].tag}")
