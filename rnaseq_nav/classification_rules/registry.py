"""
RNASeq Navigator

Classification Rule Registry

Version 4.0
"""

from rnaseq_nav.classification_rules.tokenizer import collect_tokens

from rnaseq_nav.classification_rules.metagenomics import (
    classify as metagenomics_rule,
)

from rnaseq_nav.classification_rules.small_rna import (
    classify as small_rna_rule,
)

from rnaseq_nav.classification_rules.bulk_rna import (
    classify as bulk_rna_rule,
)


# ==========================================================
# Registered Classification Rules
# ==========================================================

RULES = [
    metagenomics_rule,
    small_rna_rule,
    bulk_rna_rule,
]


# ==========================================================
# Rule Engine
# ==========================================================

def classify_using_rules(metadata: dict) -> dict:
    """
    Classify a sequencing study using the registered rules.

    Parameters
    ----------
    metadata : dict
        Study metadata returned by the metadata engine.

    Returns
    -------
    dict
        Classification result.
    """

    # ------------------------------------------------------
    # Build the shared token set once
    # ------------------------------------------------------

    metadata["tokens"] = collect_tokens(metadata)

    # ------------------------------------------------------
    # Evaluate rules in priority order
    # ------------------------------------------------------

    for rule in RULES:

        result = rule(metadata)

        if result is not None:
            return result

    # ------------------------------------------------------
    # Default classification
    # ------------------------------------------------------

    return {
        "study_type": "Unknown",
        "confidence": 0,
        "evidence": [],
    }
