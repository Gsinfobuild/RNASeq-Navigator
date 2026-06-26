"""
RNASeq Navigator

Experimental Design Assessment

Version 0.9
"""

from collections import Counter


def assess_design(run_metadata):
    """
    Assess experimental design using run metadata.

    Parameters
    ----------
    run_metadata : list
        List of sequencing run dictionaries returned by metadata.py

    Returns
    -------
    dict
        Experimental design summary.
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
        "conditions": dict(counts),
        "largest": largest,
        "smallest": smallest,
        "quality": quality
    }
