"""
RNASeq Navigator

Core Result Objects

Version: 1.3

Defines the standard result objects returned by the
public RNASeqNavigator API.
"""

from dataclasses import dataclass
from typing import Optional

from rnaseq_nav.models import Metadata

from rnaseq_nav.intelligence.report import (
    DatasetReport,
)

from rnaseq_nav.intelligence.metadata_intelligence import (
    MetadataInsight,
)

from rnaseq_nav.intelligence.modality_intelligence import (
    ModalityInsight,
)

from rnaseq_nav.intelligence.design_intelligence import (
    ExperimentalDesignInsight,
)

from rnaseq_nav.intelligence.suitability import (
    SuitabilityInsight,
)

from rnaseq_nav.intelligence.analysis_planner import (
    AnalysisPlan,
)

from rnaseq_nav.normalization.normalizer import (
    NormalizationResult,
)

from rnaseq_nav.validation.validator import (
    ValidationResult,
)


# ==========================================================
# Inspection Result
# ==========================================================

@dataclass
class InspectionResult:
    """
    Complete result returned by
    RNASeqNavigator.inspect().
    """

    # ------------------------------------------------------
    # Basic inspection status
    # ------------------------------------------------------

    success: bool = True

    accession: str = ""

    # ------------------------------------------------------
    # Core metadata
    # ------------------------------------------------------

    metadata: Optional[Metadata] = None

    # ------------------------------------------------------
    # Layer 1 — Metadata Intelligence
    # ------------------------------------------------------

    metadata_insight: Optional[
        MetadataInsight
    ] = None

    # ------------------------------------------------------
    # Layer 1.5 — Modality / Workflow Intelligence
    # ------------------------------------------------------

    modality_insight: Optional[
        ModalityInsight
    ] = None

    # ------------------------------------------------------
    # Layer 2 — Experimental Design Intelligence
    # ------------------------------------------------------

    design_insight: Optional[
        ExperimentalDesignInsight
    ] = None

    # ------------------------------------------------------
    # Layer 3 — Dataset Suitability
    # ------------------------------------------------------

    suitability_insight: Optional[
        SuitabilityInsight
    ] = None

    # ------------------------------------------------------
    # Layer 4 — Analysis Planning
    # ------------------------------------------------------

    analysis_plan: Optional[
        AnalysisPlan
    ] = None

    # ------------------------------------------------------
    # Existing dataset report
    # ------------------------------------------------------

    report: Optional[
        DatasetReport
    ] = None

    # ------------------------------------------------------
    # Normalization
    # ------------------------------------------------------

    normalization: Optional[
        NormalizationResult
    ] = None

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    validation: Optional[
        ValidationResult
    ] = None

    # ------------------------------------------------------
    # Error information
    # ------------------------------------------------------

    error: Optional[str] = None

    # ======================================================
    # Error helper
    # ======================================================

    @property
    def has_error(self):
        """
        Return True when the inspection contains an error.
        """

        return self.error is not None
