"""
RNASeq Navigator

Core Result Objects

Version: 1.0

Defines the standard result objects returned by the
public RNASeqNavigator API.
"""

from dataclasses import dataclass
from typing import Optional

from rnaseq_nav.models import Metadata
from rnaseq_nav.intelligence.report import DatasetReport
from rnaseq_nav.normalization.normalizer import (
    NormalizationResult,
)
from rnaseq_nav.validation.validator import (
    ValidationResult,
)


@dataclass
class InspectionResult:
    """
    Complete result returned by
    RNASeqNavigator.inspect().
    """

    success: bool = True

    accession: str = ""

    metadata: Optional[Metadata] = None

    report: Optional[DatasetReport] = None

    normalization: Optional[
        NormalizationResult
    ] = None

    validation: Optional[
        ValidationResult
    ] = None

    error: Optional[str] = None

    @property
    def has_error(self):

        return self.error is not None
