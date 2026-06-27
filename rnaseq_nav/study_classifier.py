"""
RNASeq Navigator

Study Classification Engine

Version 5.0

This module serves as a lightweight wrapper around the
modular rule-based classification engine.
"""

from rnaseq_nav.classification_rules.registry import (
    classify_using_rules,
)


def classify_study(study: dict) -> dict:
    """
    Classify a sequencing study.

    Parameters
    ----------
    study : dict
        Study metadata returned by the metadata engine.

    Returns
    -------
    dict
        Classification result.
    """

    return classify_using_rules(study)
