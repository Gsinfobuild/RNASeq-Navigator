"""
RNASeq Navigator

Bulk RNA-seq Classification Rule

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
    Classify a Bulk RNA-seq study.
    """

    tokens = metadata.get("tokens", set())

    rules = [

        (
            "rna" in tokens
            and "seq" in tokens
        ),

        "transcriptome" in tokens

    ]

    matched = sum(rules)

    if matched == 0:
        return None

    return {

        "study_type": "Bulk RNA-seq",

        "confidence": calculate_confidence(
            matched,
            len(rules)
        ),

        "evidence": [
            "Bulk RNA-seq evidence detected"
        ]

    }
