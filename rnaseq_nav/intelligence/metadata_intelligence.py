"""
RNASeq Navigator

Metadata Intelligence Layer

Converts normalized metadata into a concise biological interpretation.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class MetadataInsight:
    organism: str = ""
    study_type: str = ""
    biological_system: str = ""
    experimental_focus: str = ""
    sequencing_summary: str = ""
    observations: List[str] = field(default_factory=list)


def _clean(value):
    if value is None:
        return ""

    return str(value).strip()


def infer_biological_system(metadata):
    organism = _clean(
        getattr(
            getattr(metadata, "sample", None),
            "organism",
            "",
        )
    )

    if organism:
        return organism

    return "Not specified"


def infer_experimental_focus(metadata):
    experiment = getattr(
        metadata,
        "experiment",
        None,
    )

    if experiment is None:
        return "Not specified"

    title = _clean(
        getattr(
            experiment,
            "title",
            "",
        )
    )

    strategy = _clean(
        getattr(
            experiment,
            "library_strategy",
            "",
        )
    )

    if title:
        return title

    if strategy:
        return strategy

    return "Not specified"


def build_sequencing_summary(metadata):

    experiment = getattr(
        metadata,
        "experiment",
        None,
    )

    if experiment is None:
        return "Sequencing information unavailable."

    strategy = _clean(
        getattr(
            experiment,
            "library_strategy",
            "",
        )
    )

    source = _clean(
        getattr(
            experiment,
            "library_source",
            "",
        )
    )

    selection = _clean(
        getattr(
            experiment,
            "library_selection",
            "",
        )
    )

    layout = _clean(
        getattr(
            experiment,
            "layout",
            "",
        )
    )

    platform = _clean(
        getattr(
            experiment,
            "platform",
            "",
        )
    )

    parts = []

    if strategy:
        parts.append(f"strategy={strategy}")

    if source:
        parts.append(f"source={source}")

    if selection:
        parts.append(f"selection={selection}")

    if layout:
        parts.append(f"layout={layout}")

    if platform:
        parts.append(f"platform={platform}")

    if not parts:
        return "Sequencing information unavailable."

    return "; ".join(parts)


def generate_metadata_insight(
    metadata,
    study_type="",
):
    """
    Generate a biological interpretation from normalized metadata.

    This layer intentionally does not claim experimental relationships
    that are not explicitly represented in the available metadata.
    """

    insight = MetadataInsight()

    insight.organism = infer_biological_system(
        metadata
    )

    insight.study_type = _clean(
        study_type
    ) or "Not classified"

    insight.biological_system = insight.organism

    insight.experimental_focus = (
        infer_experimental_focus(metadata)
    )

    insight.sequencing_summary = (
        build_sequencing_summary(metadata)
    )

    if insight.organism != "Not specified":
        insight.observations.append(
            f"Organism identified as {insight.organism}."
        )

    if insight.study_type != "Not classified":
        insight.observations.append(
            f"Dataset classified as {insight.study_type}."
        )

    return insight
