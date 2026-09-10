"""
Layer 3 — Assess

Evaluates whether the available metadata are sufficiently
structured for downstream RNA-seq analysis.

This is a metadata-readiness assessment, not a guarantee
of experimental quality.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AssessmentResult:
    overall_status: str = "Needs review"
    score: int = 0
    strengths: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    checks: Dict[str, str] = field(default_factory=dict)


def _get(obj: Any, *names: str, default=None):

    if obj is None:
        return default

    for name in names:

        if isinstance(obj, dict):
            value = obj.get(name)

        else:
            value = getattr(obj, name, None)

        if value not in (None, ""):
            return value

    return default


def assess_dataset(
    metadata: Any,
    interpretation: Any,
) -> AssessmentResult:

    strengths = []
    limitations = []
    checks = {}

    score = 0

    # ------------------------------------------------------
    # Experiment type
    # ------------------------------------------------------

    experiment_type = _get(
        interpretation,
        "experiment_type",
        default="Unknown",
    )

    if experiment_type != "Unknown":

        checks["Experiment type"] = "Pass"
        strengths.append(
            "The sequencing experiment could be classified."
        )
        score += 20

    else:

        checks["Experiment type"] = "Review"
        limitations.append(
            "Experiment type could not be classified confidently."
        )

    # ------------------------------------------------------
    # Organism
    # ------------------------------------------------------

    organism = _get(
        metadata,
        "organism",
        "scientific_name",
    )

    if organism:

        checks["Organism"] = "Pass"
        strengths.append("Organism information is available.")
        score += 20

    else:

        checks["Organism"] = "Missing"
        limitations.append(
            "Organism information is missing."
        )

    # ------------------------------------------------------
    # Library strategy
    # ------------------------------------------------------

    strategy = _get(
        metadata,
        "library_strategy",
        "libraryStrategy",
    )

    if strategy:

        checks["Library strategy"] = "Pass"
        strengths.append(
            "Library strategy is available."
        )
        score += 15

    else:

        checks["Library strategy"] = "Missing"
        limitations.append(
            "Library strategy is unavailable."
        )

    # ------------------------------------------------------
    # Sequencing layout
    # ------------------------------------------------------

    layout = _get(
        metadata,
        "layout",
    )

    if layout:

        checks["Read layout"] = "Pass"
        strengths.append(
            "Read layout is available."
        )
        score += 15

    else:

        checks["Read layout"] = "Missing"
        limitations.append(
            "Read layout is unavailable."
        )

    # ------------------------------------------------------
    # Experimental factors
    # ------------------------------------------------------

    factors = _get(
        interpretation,
        "detected_factors",
        default=[],
    )

    if factors:

        checks["Experimental factors"] = "Pass"
        strengths.append(
            "Potential experimental factors were detected."
        )
        score += 15

    else:

        checks["Experimental factors"] = "Review"
        limitations.append(
            "No clear experimental factors were detected."
        )

    # ------------------------------------------------------
    # Replicate information
    # ------------------------------------------------------

    sample_count = _get(
        metadata,
        "sample_count",
        "samples",
    )

    if sample_count:

        checks["Sample information"] = "Pass"
        strengths.append(
            "Sample-level information is available."
        )
        score += 15

    else:

        checks["Sample information"] = "Review"
        limitations.append(
            "Sample or replicate information could not be established."
        )

    # ------------------------------------------------------
    # Overall status
    # ------------------------------------------------------

    if score >= 80:
        overall_status = "Ready for analysis planning"

    elif score >= 55:
        overall_status = "Suitable with metadata review"

    else:
        overall_status = "Needs metadata review"

    return AssessmentResult(
        overall_status=overall_status,
        score=score,
        strengths=strengths,
        limitations=limitations,
        checks=checks,
    )


def assessment_to_dict(
    assessment: AssessmentResult,
) -> Dict[str, Any]:

    return {
        "overall_status": assessment.overall_status,
        "score": assessment.score,
        "strengths": assessment.strengths,
        "limitations": assessment.limitations,
        "checks": assessment.checks,
    }
