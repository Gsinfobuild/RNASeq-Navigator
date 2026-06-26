"""
RNASeq Navigator

Experimental Condition Detector

Version 0.9
"""

from collections import Counter


def detect_conditions(run_metadata):
    """
    Detect experimental conditions and count the number of runs
    belonging to each condition.

    Parameters
    ----------
    run_metadata : list
        List of sequencing run dictionaries.

    Returns
    -------
    dict
        Dictionary mapping condition -> run count.
    """

    conditions = []

    for run in run_metadata:

        title = run.get("experiment_title", "").lower()

        if ":" in title:

            condition = title.split(":")[-1].strip()

            conditions.append(condition)

    counts = Counter(conditions)

    return dict(sorted(counts.items()))
