"""
RNASeq Scout

Study Experimental Landscape Intelligence

Summarizes the observed assay families and experimental
context labels across a study.

This layer is deliberately descriptive. It does not infer
controls, treatments, biological replicates, time points,
or statistical contrasts.
"""

from collections import Counter
from typing import Iterable

from rnaseq_nav.models import (
    StudyExperiment,
    StudyExperimentalLandscape,
)


def _classify_assay_family(title: str) -> str:
    """
    Classify an experiment title into an observed assay family.

    Classification is based only on the explicit title prefix.
    """

    title = title.strip()

    if title.startswith("sRNA-seq"):
        return "sRNA-seq"

    if title.startswith("TEX+ RNA-seq"):
        return "TEX+ RNA-seq"

    if title.startswith("RNA-seq"):
        return "RNA-seq"

    return "Unclassified"


def _extract_context(title: str) -> str:
    """
    Extract the observed context label from an experiment title.

    The context is the text following the final colon.
    No normalization or semantic merging is performed.
    """

    title = title.strip()

    if ":" not in title:
        return "Unspecified"

    context = title.rsplit(":", 1)[1].strip()

    return context or "Unspecified"


def generate_study_experimental_landscape(
    records: Iterable[StudyExperiment],
) -> StudyExperimentalLandscape:
    """
    Generate a descriptive study-level experimental landscape.

    Parameters
    ----------
    records : Iterable[StudyExperiment]
        Study-level experiment records retrieved from SRA.

    Returns
    -------
    StudyExperimentalLandscape
        Counts and observed labels describing the study.

    Notes
    -----
    This function intentionally does not infer:

    - controls
    - treatments
    - biological replicates
    - time points
    - statistical contrasts
    """

    records = list(records)

    assay_family_counts = Counter()
    context_counts = Counter()
    assay_context_counts = {}

    warnings = []

    for record in records:

        title = (
            record.experiment_title
            if record.experiment_title
            else ""
        )

        assay_family = _classify_assay_family(title)
        context = _extract_context(title)

        assay_family_counts[assay_family] += 1
        context_counts[context] += 1

        if assay_family not in assay_context_counts:
            assay_context_counts[assay_family] = {}

        assay_context_counts[assay_family][context] = (
            assay_context_counts[assay_family].get(
                context,
                0,
            )
            + 1
        )

    if not records:
        warnings.append(
            "No study experiment records were available."
        )

    if "Unclassified" in assay_family_counts:
        warnings.append(
            "One or more experiment titles could not be "
            "assigned to a recognized assay family."
        )

    landscape = StudyExperimentalLandscape(
        total_experiments=len(records),
        assay_family_counts=dict(
            assay_family_counts
        ),
        context_counts=dict(
            context_counts
        ),
        assay_context_counts=assay_context_counts,
        observed_assay_families=sorted(
            assay_family_counts.keys()
        ),
        observed_contexts=sorted(
            context_counts.keys()
        ),
        warnings=warnings,
    )

    return landscape
