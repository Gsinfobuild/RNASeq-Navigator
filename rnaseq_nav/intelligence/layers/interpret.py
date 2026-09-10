"""
Layer 2 — Interpret

Transforms dataset metadata into an interpretable description
of the sequencing experiment.

Interpretation is rule-based and evidence-driven.
It does not invent biological conclusions that are not
supported by the available metadata.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class InterpretationResult:
    experiment_type: str = "Unknown"
    confidence: str = "Low"
    evidence: List[str] = field(default_factory=list)
    biological_context: str = "Insufficient metadata"
    detected_factors: List[str] = field(default_factory=list)
    detected_groups: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _collect_metadata(metadata: Any) -> str:
    if isinstance(metadata, dict):
        values = []

        for key, value in metadata.items():
            values.append(str(key))
            values.append(str(value))

        return " ".join(values).lower()

    return str(metadata).lower()


def interpret_dataset(
    metadata: Any,
    study_type: str = "",
    library_strategy: str = "",
) -> InterpretationResult:

    evidence = []
    warnings = []

    combined = _collect_metadata(metadata)

    combined += " " + _text(study_type)
    combined += " " + _text(library_strategy)

    # ------------------------------------------------------
    # Study classification
    # ------------------------------------------------------

    if "small rna" in combined or "small-rna" in combined:
        experiment_type = "Small RNA-seq"
        confidence = "High"

        evidence.append(
            "Metadata contains evidence for a small RNA-seq study."
        )

    elif (
        "rna-seq" in combined
        or "rna seq" in combined
        or "transcriptom" in combined
    ):
        experiment_type = "RNA-seq"
        confidence = "High"

        evidence.append(
            "Metadata contains evidence for transcriptomic RNA sequencing."
        )

    elif "scrna" in combined or "single cell" in combined:
        experiment_type = "Single-cell RNA-seq"
        confidence = "High"

        evidence.append(
            "Metadata contains evidence for single-cell sequencing."
        )

    else:
        experiment_type = "Unknown"
        confidence = "Low"

        warnings.append(
            "The available metadata do not provide enough evidence "
            "to classify the experiment confidently."
        )

    # ------------------------------------------------------
    # Experimental factors
    # ------------------------------------------------------

    factor_keywords = {
        "treatment": [
            "treatment",
            "treated",
            "drug",
            "compound",
        ],
        "stress": [
            "stress",
            "starvation",
            "heat shock",
            "oxidative",
        ],
        "infection": [
            "infection",
            "infected",
            "pathogen",
        ],
        "genotype": [
            "mutant",
            "knockout",
            "knockdown",
            "wild type",
            "wild-type",
        ],
        "time": [
            "timepoint",
            "time point",
            "hour",
            "hours",
            "day",
        ],
    }

    detected_factors = []

    for factor, keywords in factor_keywords.items():

        if any(keyword in combined for keyword in keywords):
            detected_factors.append(factor)

    # ------------------------------------------------------
    # Common groups
    # ------------------------------------------------------

    group_keywords = [
        "control",
        "treated",
        "treatment",
        "mutant",
        "wild type",
        "wild-type",
        "knockout",
        "knockdown",
    ]

    detected_groups = [
        keyword
        for keyword in group_keywords
        if keyword in combined
    ]

    # ------------------------------------------------------
    # Biological context
    # ------------------------------------------------------

    if detected_factors:
        biological_context = (
            "Metadata suggests an experiment involving "
            + ", ".join(detected_factors)
            + "."
        )
    else:
        biological_context = (
            "No clear experimental factor could be inferred "
            "from the available metadata."
        )

    return InterpretationResult(
        experiment_type=experiment_type,
        confidence=confidence,
        evidence=evidence,
        biological_context=biological_context,
        detected_factors=detected_factors,
        detected_groups=detected_groups,
        warnings=warnings,
    )


def interpretation_to_dict(
    interpretation: InterpretationResult,
) -> Dict[str, Any]:

    return {
        "experiment_type": interpretation.experiment_type,
        "confidence": interpretation.confidence,
        "evidence": interpretation.evidence,
        "biological_context": interpretation.biological_context,
        "detected_factors": interpretation.detected_factors,
        "detected_groups": interpretation.detected_groups,
        "warnings": interpretation.warnings,
    }
