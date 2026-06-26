from collections import Counter


def assess_design(run_metadata):
    """
    Assess experimental design based on sequencing run metadata.
    """

    conditions = []

    for run in run_metadata:

        title = run.get("experiment_title", "").lower()

        if ":" in title:
            condition = title.split(":")[-1].strip()
            conditions.append(condition)

    counts = Counter(conditions)

    if len(counts) == 0:
        return None

    largest = max(counts.values())
    smallest = min(counts.values())

    if largest == smallest:
        quality = "Balanced"

    elif largest - smallest <= 1:
        quality = "Moderately balanced"

    else:
        quality = "Unbalanced"

    return {
        "conditions": counts,
        "largest": largest,
        "smallest": smallest,
        "quality": quality
    }
