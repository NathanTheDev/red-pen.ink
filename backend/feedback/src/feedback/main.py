# ruff: noqa: E501


from feedback.core.ollama import build_index, embed, search
from feedback.tag.tag import (
    extract_feedback_tags,
    extract_quality_tags,
    extract_technique_tags,
)

MODULE_CONTEXT = "HSC English Advanced. Prescribed text: The Tempest. Rubric criteria: thesis, evidence, analysis, conceptual depth, contextual knowledge"

TRAIN_EXAMPLE = "Shakespeare employs the metaphor of the tempest to interrogate the moral legitimacy of Prospero's authority."
TRAIN_COMMENT = "You've identified the metaphor but not explained what it constructs — why does Shakespeare use the tempest specifically to frame questions of authority?"

STRONG_EXAMPLE = "By framing Prospero's authority through the violence of the tempest, Shakespeare constructs power as inherently destructive, destabilising any reading of the protagonist as a benevolent ruler."
WEAK_EXAMPLE = "Prospero uses magic to control the island and its inhabitants."

QUALITY_THRESHOLD = 0.7


def print_tags(tags: list[str]) -> None:
    for i, tag in enumerate(tags):
        prefix = "└──" if i == len(tags) - 1 else "├──"
        print(f" {prefix} {tag}")


if __name__ == "__main__":
    good_tags = extract_technique_tags(STRONG_EXAMPLE, MODULE_CONTEXT)
    print("Technique Tags on good example:")
    print_tags(good_tags)

    feed_tags = extract_feedback_tags(TRAIN_EXAMPLE, TRAIN_COMMENT, MODULE_CONTEXT)
    print("\nFeedback Tags on past examples:")
    print_tags(feed_tags)

    good_index, stored_good_tags = build_index(good_tags)
    feed_index, stored_feed_tags = build_index(feed_tags)
    print(f"\nGood Example Index: {good_index.ntotal} tags")
    print(f"Feedback Index: {feed_index.ntotal} tags")

    quality_tags = extract_quality_tags(WEAK_EXAMPLE, MODULE_CONTEXT)
    print("\nQuality Tags on student example:")
    print_tags(quality_tags)

    missing = []
    if quality_tags:
        q_embs = embed(quality_tags)
        g_embs = embed(stored_good_tags)
        sim_matrix = g_embs @ q_embs.T
        for i, good_tag in enumerate(stored_good_tags):
            if float(sim_matrix[i].max()) < QUALITY_THRESHOLD:
                missing.append(good_tag)

    print("\nMissing (not in student):")
    print_tags(missing)

    if missing:
        record_hits: dict[int, float] = {}
        for tag in missing:
            for score, matched_tag in search(tag, feed_index, stored_feed_tags, k=3):
                idx = stored_feed_tags.index(matched_tag)
                record_hits[idx] = record_hits.get(idx, 0) + score

        ranked = sorted(record_hits.items(), key=lambda x: x[1], reverse=True)
        top_feedback = [stored_feed_tags[i] for i, _ in ranked[:3]]

        print("\nRetrieved feedback tags:")
        print_tags(top_feedback)
