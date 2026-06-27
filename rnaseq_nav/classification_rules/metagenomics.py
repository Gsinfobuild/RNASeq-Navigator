"""
RNASeq Navigator

Metagenomics Classification Rule

Version 2.0
"""

from typing import Dict, Optional


KEYWORDS = [
    "metagenome",
    "metagenomic",
    "microbiome",
    "shotgun metagenome",
]


def classify(metadata: Dict) -> Optional[dict]:
    """
    Classify a metagenomic sequencing study.

    Parameters
    ----------
    metadata : dict

    Returns
    -------
    dict | None
        Classification result if matched,
        otherwise None.
    """

    text = " ".join([
        metadata.get("scientific_name", ""),
        metadata.get("library_strategy", ""),
        metadata.get("library_source", ""),
        metadata.get("experiment_title", ""),
        metadata.get("sample_alias", ""),
    ]).lower()

    for keyword in KEYWORDS:

        if keyword in text:

            return {
                "study_type": "Metagenomics",
                "confidence": 100,
                "evidence": [
                    "Metagenomic evidence detected"
                ],
            }

    return None
