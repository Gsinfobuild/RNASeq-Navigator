"""
RNASeq Navigator

Benchmark Statistics Engine

Version 2.0

Computes overall and per-class benchmark statistics.
"""


def calculate_statistics(results):
    """
    Calculate benchmark statistics.

    Parameters
    ----------
    results : list of dict

        Each dictionary must contain:

        {
            "expected": "...",
            "predicted": "...",
            "correct": True or False
        }

    Returns
    -------
    dict

        {
            "total": int,
            "correct": int,
            "incorrect": int,
            "accuracy": float,
            "per_class": {
                ...
            }
        }
    """

    # -----------------------------------------------------
    # Overall statistics
    # -----------------------------------------------------

    total = len(results)

    correct = sum(
        1
        for item in results
        if item["correct"]
    )

    incorrect = total - correct

    accuracy = 0.0

    if total > 0:
        accuracy = round(
            (correct / total) * 100,
            2,
        )

    # -----------------------------------------------------
    # Per-class statistics
    # -----------------------------------------------------

    per_class = {}

    for item in results:

        study_type = item["expected"]

        if study_type not in per_class:

            per_class[study_type] = {
                "total": 0,
                "correct": 0,
                "incorrect": 0,
                "accuracy": 0.0,
            }

        per_class[study_type]["total"] += 1

        if item["correct"]:
            per_class[study_type]["correct"] += 1
        else:
            per_class[study_type]["incorrect"] += 1

    # -----------------------------------------------------
    # Calculate per-class accuracy
    # -----------------------------------------------------

    for study_type in per_class:

        class_total = per_class[study_type]["total"]

        class_correct = per_class[study_type]["correct"]

        if class_total > 0:

            per_class[study_type]["accuracy"] = round(
                (class_correct / class_total) * 100,
                2,
            )

    # -----------------------------------------------------
    # Return statistics
    # -----------------------------------------------------

    return {

        "total": total,

        "correct": correct,

        "incorrect": incorrect,

        "accuracy": accuracy,

        "per_class": per_class,

    }
