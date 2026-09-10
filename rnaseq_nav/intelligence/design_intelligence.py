"""
RNASeq Navigator

Experimental Design Intelligence Layer
======================================

Layer 2 interprets available dataset metadata to identify
possible experimental design information.

Important scientific principle
------------------------------

This module distinguishes between:

1. Observed metadata
   Information explicitly present in the dataset metadata.

2. Inferred design information
   Information suggested by metadata but not explicitly established.

The module must never claim biological replication, control groups,
treatment groups, or statistical design formulas unless the available
metadata provides sufficient evidence.

Version: 1.0
"""

from dataclasses import dataclass, field
from typing import List


# ==========================================================
# Experimental Design Insight
# ==========================================================

@dataclass
class ExperimentalDesignInsight:
    """
    Structured interpretation of experimental design metadata.
    """

    condition: str = ""

    control: str = ""

    treatment: str = ""

    time_point: str = ""

    replicate_information: str = ""

    design_description: str = ""

    design_confidence: str = "Insufficient information"

    observed_features: List[str] = field(
        default_factory=list
    )

    inferred_features: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    missing_information: List[str] = field(
        default_factory=list
    )


# ==========================================================
# Utility Functions
# ==========================================================

def _clean(value):
    """
    Convert a metadata value into a clean string.
    """

    if value is None:
        return ""

    return str(value).strip()


def _get_experiment(metadata):
    """
    Safely retrieve experiment metadata.
    """

    return getattr(
        metadata,
        "experiment",
        None,
    )


def _get_sample(metadata):
    """
    Safely retrieve sample metadata.
    """

    return getattr(
        metadata,
        "sample",
        None,
    )


# ==========================================================
# Metadata Collection
# ==========================================================

def _collect_observed_metadata(metadata):
    """
    Collect fields that may contain experimental design
    information.

    These values are treated strictly as observations.
    """

    experiment = _get_experiment(metadata)
    sample = _get_sample(metadata)

    observed = {}

    if experiment is not None:

        observed["title"] = _clean(
            getattr(
                experiment,
                "title",
                "",
            )
        )

        observed["library_strategy"] = _clean(
            getattr(
                experiment,
                "library_strategy",
                "",
            )
        )

        observed["library_source"] = _clean(
            getattr(
                experiment,
                "library_source",
                "",
            )
        )

        observed["layout"] = _clean(
            getattr(
                experiment,
                "layout",
                "",
            )
        )

        observed["platform"] = _clean(
            getattr(
                experiment,
                "platform",
                "",
            )
        )

    if sample is not None:

        observed["organism"] = _clean(
            getattr(
                sample,
                "organism",
                "",
            )
        )

        observed["biosample"] = _clean(
            getattr(
                sample,
                "biosample",
                "",
            )
        )

    return observed


# ==========================================================
# Condition Detection
# ==========================================================

def _detect_condition(title):
    """
    Identify a possible experimental condition from the title.

    This is deliberately conservative.

    The returned value represents a possible condition,
    not a confirmed experimental group.
    """

    if not title:
        return ""

    title_lower = title.lower()

    keywords = [
        "stress",
        "starvation",
        "treatment",
        "treated",
        "control",
        "infection",
        "infected",
        "drug",
        "antibiotic",
        "iron",
        "hypoxia",
        "nutrient",
        "detergent",
        "isoniazid",
        "kanamycin",
    ]

    for keyword in keywords:

        if keyword in title_lower:
            return title

    return ""


# ==========================================================
# Control Detection
# ==========================================================

def _detect_control(title):
    """
    Detect explicit control terminology.

    This does not infer a control merely because another
    condition exists.
    """

    if not title:
        return ""

    title_lower = title.lower()

    control_terms = [
        "control",
        "untreated",
        "vehicle control",
        "mock control",
        "mock-treated",
    ]

    for term in control_terms:

        if term in title_lower:
            return title

    return ""


# ==========================================================
# Treatment Detection
# ==========================================================

def _detect_treatment(title):
    """
    Detect explicit treatment-related terminology.
    """

    if not title:
        return ""

    title_lower = title.lower()

    treatment_terms = [
        "treated",
        "treatment",
        "drug",
        "antibiotic",
        "isoniazid",
        "kanamycin",
        "detergent",
    ]

    for term in treatment_terms:

        if term in title_lower:
            return title

    return ""


# ==========================================================
# Time Point Detection
# ==========================================================

def _detect_time_point(title):
    """
    Detect simple explicit time-point terminology.

    Examples potentially recognized:

        6h
        12h
        24h
        6 hours
        24 hours
        time point

    The function does not invent a time point.
    """

    if not title:
        return ""

    title_lower = title.lower()

    tokens = title_lower.replace(
        "_",
        " ",
    ).split()

    for token in tokens:

        if token.endswith("h"):

            numeric_part = token[:-1]

            if numeric_part.isdigit():
                return token

    if "time point" in title_lower:
        return "Time point mentioned"

    if "hours" in title_lower:
        return "Time duration mentioned"

    return ""


# ==========================================================
# Replicate Assessment
# ==========================================================

def _assess_replicates(metadata):
    """
    Assess whether replicate information is explicitly available.

    A single sequencing run must NOT be interpreted as a biological
    replicate.

    Therefore, absence of explicit replicate metadata results in
    an 'unclear' assessment.
    """

    run = getattr(
        metadata,
        "run",
        None,
    )

    if run is None:

        return (
            "Replicate structure could not be established "
            "from the available metadata."
        )

    accession = _clean(
        getattr(
            run,
            "accession",
            "",
        )
    )

    if accession:

        return (
            "One sequencing run is represented by the inspected "
            "accession; biological replicate status is not "
            "established by this information alone."
        )

    return (
        "Replicate structure could not be established "
        "from the available metadata."
    )


# ==========================================================
# Main Layer 2 Function
# ==========================================================

def generate_design_insight(metadata):
    """
    Generate an experimental design interpretation.

    Scientific policy
    -----------------

    The function distinguishes explicit observations from
    cautious inference.

    It does not claim:

    - biological replicates
    - experimental controls
    - treatment groups
    - statistical design formulas

    unless sufficient metadata supports those claims.
    """

    insight = ExperimentalDesignInsight()

    observed = _collect_observed_metadata(
        metadata
    )

    title = observed.get(
        "title",
        "",
    )

    # ------------------------------------------------------
    # Record observed metadata
    # ------------------------------------------------------

    if title:

        insight.observed_features.append(
            f"Experiment title: {title}"
        )

    if observed.get("library_strategy"):

        insight.observed_features.append(
            "Library strategy: "
            + observed["library_strategy"]
        )

    if observed.get("layout"):

        insight.observed_features.append(
            "Sequencing layout: "
            + observed["layout"]
        )

    if observed.get("platform"):

        insight.observed_features.append(
            "Sequencing platform: "
            + observed["platform"]
        )

    if observed.get("organism"):

        insight.observed_features.append(
            "Organism: "
            + observed["organism"]
        )

    # ------------------------------------------------------
    # Condition
    # ------------------------------------------------------

    condition = _detect_condition(
        title
    )

    if condition:

        insight.condition = condition

        insight.inferred_features.append(
            "The experiment title suggests a "
            "condition or experimental context."
        )

    # ------------------------------------------------------
    # Control
    # ------------------------------------------------------

    control = _detect_control(
        title
    )

    if control:

        insight.control = control

        insight.inferred_features.append(
            "Control terminology is explicitly present "
            "in the experiment title."
        )

    else:

        insight.warnings.append(
            "No explicit control group was identified "
            "from the available metadata."
        )

        insight.missing_information.append(
            "Control-group annotation"
        )

    # ------------------------------------------------------
    # Treatment
    # ------------------------------------------------------

    treatment = _detect_treatment(
        title
    )

    if treatment:

        insight.treatment = treatment

        insight.inferred_features.append(
            "Treatment-related terminology is present "
            "in the experiment metadata."
        )

    else:

        insight.missing_information.append(
            "Treatment-group annotation, if applicable"
        )

    # ------------------------------------------------------
    # Time point
    # ------------------------------------------------------

    time_point = _detect_time_point(
        title
    )

    if time_point:

        insight.time_point = time_point

        insight.inferred_features.append(
            "Time-related information is suggested "
            "by the experiment metadata."
        )

    else:

        insight.missing_information.append(
            "Time-point information, if applicable"
        )

    # ------------------------------------------------------
    # Replicates
    # ------------------------------------------------------

    insight.replicate_information = (
        _assess_replicates(
            metadata
        )
    )

    insight.warnings.append(
        insight.replicate_information
    )

    insight.missing_information.append(
        "Biological replicate annotation"
    )

    # ------------------------------------------------------
    # Design description
    # ------------------------------------------------------

    if condition:

        insight.design_description = (
            "The metadata suggests an experimental "
            "condition, but the complete experimental "
            "group structure cannot be established "
            "from the inspected accession alone."
        )

    else:

        insight.design_description = (
            "The available metadata does not provide "
            "enough information to establish the "
            "experimental design."
        )

    # ------------------------------------------------------
    # Confidence
    # ------------------------------------------------------

    if (
        condition
        and control
        and treatment
        and time_point
    ):

        insight.design_confidence = (
            "Partially characterized"
        )

    elif condition:

        insight.design_confidence = (
            "Condition suggested; design incomplete"
        )

    else:

        insight.design_confidence = (
            "Insufficient information"
        )

    # ------------------------------------------------------
    # Final warning
    # ------------------------------------------------------

    insight.warnings.append(
        "Experimental relationships are interpreted "
        "conservatively and should be confirmed using "
        "sample-level metadata before downstream "
        "statistical analysis."
    )

    return insight
