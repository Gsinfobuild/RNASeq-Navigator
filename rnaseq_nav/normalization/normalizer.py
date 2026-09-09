"""
RNASeq Navigator

Metadata Normalization Engine

Version 4.0

Features
--------
- Preserves original metadata
- Returns normalized metadata
- Generates normalization report
- Produces summary statistics
- Uses strongly typed normalization objects
"""

from copy import deepcopy
from dataclasses import dataclass, field
from collections import Counter

from rnaseq_nav.normalization.dictionaries import (
    canonical_key,
    LIBRARY_LAYOUT,
    LIBRARY_SELECTION,
    LIBRARY_SOURCE,
    LIBRARY_STRATEGY,
    PLATFORM,
)


# ==========================================================
# Normalization Change
# ==========================================================

@dataclass
class NormalizationChange:
    """
    Represents one normalization event.
    """

    section: str

    field: str

    original: str

    normalized: str


# ==========================================================
# Normalization Result
# ==========================================================

@dataclass
class NormalizationResult:
    """
    Result returned by MetadataNormalizer.
    """

    metadata: object

    report: list[NormalizationChange] = field(default_factory=list)

    changes: int = 0

    summary: dict = field(default_factory=dict)


# ==========================================================
# Metadata Normalizer
# ==========================================================

class MetadataNormalizer:
    """
    Normalize metadata into canonical
    RNASeq Navigator representations.
    """

    def __init__(self):

        self.strategy = LIBRARY_STRATEGY

        self.layout = LIBRARY_LAYOUT

        self.source = LIBRARY_SOURCE

        self.selection = LIBRARY_SELECTION

        self.platform = PLATFORM

    # -----------------------------------------------------

    def _normalize_field(
        self,
        report,
        section,
        field_name,
        old_value,
        dictionary,
    ):

        key = canonical_key(old_value)

        new_value = dictionary.get(
            key,
            key
        )

        if old_value != new_value:

            report.append(

                NormalizationChange(

                    section=section,

                    field=field_name,

                    original=old_value,

                    normalized=new_value,

                )

            )

        return new_value

    # -----------------------------------------------------

    def _build_summary(self, report):

        section_counter = Counter()

        field_counter = Counter()

        for change in report:

            section_counter[change.section] += 1

            field_counter[change.field] += 1

        return {

            "total_changes": len(report),

            "sections_modified": len(section_counter),

            "fields_modified": len(field_counter),

            "changes_by_section": dict(section_counter),

            "changes_by_field": dict(field_counter),

        }

    # -----------------------------------------------------

    def normalize(self, metadata):

        metadata = deepcopy(metadata)

        report = []

        # --------------------------------------------------
        # Library Strategy
        # --------------------------------------------------

        metadata.experiment.library_strategy = self._normalize_field(

            report,

            "Experiment",

            "library_strategy",

            metadata.experiment.library_strategy,

            self.strategy,

        )

        # --------------------------------------------------
        # Layout
        # --------------------------------------------------

        metadata.experiment.layout = self._normalize_field(

            report,

            "Experiment",

            "layout",

            metadata.experiment.layout,

            self.layout,

        )

        # --------------------------------------------------
        # Library Source
        # --------------------------------------------------

        metadata.experiment.library_source = self._normalize_field(

            report,

            "Experiment",

            "library_source",

            metadata.experiment.library_source,

            self.source,

        )

        # --------------------------------------------------
        # Library Selection
        # --------------------------------------------------

        metadata.experiment.library_selection = self._normalize_field(

            report,

            "Experiment",

            "library_selection",

            metadata.experiment.library_selection,

            self.selection,

        )

        # --------------------------------------------------
        # Platform
        # --------------------------------------------------

        metadata.experiment.platform = self._normalize_field(

            report,

            "Experiment",

            "platform",

            metadata.experiment.platform,

            self.platform,

        )

        summary = self._build_summary(report)

        return NormalizationResult(

            metadata=metadata,

            report=report,

            changes=len(report),

            summary=summary,

        )
