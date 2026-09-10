"""
Layer 1 — Explore

Converts the existing RNASeq Navigator inspection result into
a compact, researcher-facing dataset exploration summary.

This layer does not retrieve new information from NCBI.
It works on the structured inspection result already produced
by RNASeq Navigator.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ExplorationResult:
    accession: str
    organism: str = "—"
    study_type: str = "—"
    library_strategy: str = "—"
    platform: str = "—"
    instrument: str = "—"
    layout: str = "—"
    sample_count: int | None = None
    run_count: int | None = None
    project_accession: str = "—"
    experiment_accession: str = "—"
    sample_accession: str = "—"
    metadata: Dict[str, Any] = field(default_factory=dict)


def _get(obj: Any, *names: str, default=None):
    """Safely retrieve a field from an object or dictionary."""

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


def explore_dataset(result: Any, accession: str) -> ExplorationResult:
    """
    Build the Layer 1 exploration summary.

    The function intentionally accepts the existing inspection
    result instead of performing another NCBI request.
    """

    metadata = _get(
        result,
        "metadata",
        default=result,
    )

    return ExplorationResult(
        accession=accession,
        organism=_get(
            metadata,
            "organism",
            "scientific_name",
            default="—",
        ),
        study_type=_get(
            metadata,
            "study_type",
            "studyType",
            default="—",
        ),
        library_strategy=_get(
            metadata,
            "library_strategy",
            "libraryStrategy",
            default="—",
        ),
        platform=_get(
            metadata,
            "platform",
            default="—",
        ),
        instrument=_get(
            metadata,
            "instrument",
            default="—",
        ),
        layout=_get(
            metadata,
            "layout",
            default="—",
        ),
        sample_count=_get(
            metadata,
            "sample_count",
            "samples",
        ),
        run_count=_get(
            metadata,
            "run_count",
            "runs",
        ),
        project_accession=_get(
            metadata,
            "bioproject",
            "project_accession",
            "bioproject_accession",
            default="—",
        ),
        experiment_accession=_get(
            metadata,
            "experiment_accession",
            "sra_experiment",
            default="—",
        ),
        sample_accession=_get(
            metadata,
            "biosample",
            "sample_accession",
            default="—",
        ),
        metadata=(
            metadata
            if isinstance(metadata, dict)
            else {}
        ),
    )


def exploration_to_dict(
    exploration: ExplorationResult,
) -> Dict[str, Any]:
    """Convert exploration result to a serializable dictionary."""

    return {
        "accession": exploration.accession,
        "organism": exploration.organism,
        "study_type": exploration.study_type,
        "library_strategy": exploration.library_strategy,
        "platform": exploration.platform,
        "instrument": exploration.instrument,
        "layout": exploration.layout,
        "sample_count": exploration.sample_count,
        "run_count": exploration.run_count,
        "project_accession": exploration.project_accession,
        "experiment_accession": exploration.experiment_accession,
        "sample_accession": exploration.sample_accession,
    }
