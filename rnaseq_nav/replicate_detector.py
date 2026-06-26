from collections import Counter


def detect_replicates(run_metadata):
    """
    Count sequencing runs associated with each detected condition.
    """

    conditions = []

    for run in run_metadata:

        title = run.get("experiment_title", "").lower()

        if ":" in title:
            condition = title.split(":")[-1].strip()
            conditions.append(condition)

    return Counter(conditions)
