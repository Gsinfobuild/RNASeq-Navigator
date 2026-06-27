"""
RNASeq Navigator

Small RNA-seq Classification Rule

Version 1.0
"""

from typing import Dict, Optional


def calculate_confidence(matched_rules: int, total_rules: int) -> int:
    """
    Calculate classification confidence.
    """

    if total_rules == 0:
        return 0

    confidence = int((matched_rules / total_rules) * 100)

    return max(50, min(confidence, 100))


def classify(metadata: Dict) -> Optional[dict]:
    """
    Classify a Small RNA-seq study.
    """

    tokens = metadata.get("tokens", set())

    rules = [

        "srna" in tokens,

        "mirna" in tokens,

        "pirna" in tokens,

        (
            "small" in tokens
            and "rna" in tokens
        )

    ]

    matched = sum(rules)

    if matched == 0:
        return None

    return {

        "study_type": "Small RNA-seq",

        "confidence": calculate_confidence(
            matched,
            len(rules)
        ),

        "evidence": [
            "Small RNA evidence detected"
        ]

    }
