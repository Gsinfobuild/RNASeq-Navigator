"""
RNASeq Navigator
================

Public Navigator API

Version: 1.2

Purpose
-------
Provides the single public interface to the RNASeq Navigator
framework.

All user interfaces (CLI, GUI, Web, Python API) should interact
with this class.

Pipeline
--------
    Fetch
      ↓
    Normalize
      ↓
    Validate
      ↓
    Interpret
      ↓
    Build Report
      ↓
    InspectionResult

Author
------
RNASeq Navigator Project
"""

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery
from rnaseq_nav.normalization.normalizer import MetadataNormalizer
from rnaseq_nav.validation.validator import MetadataValidator
from rnaseq_nav.intelligence.interpreter import DatasetInterpreter
from rnaseq_nav.intelligence.report_builder import DatasetReportBuilder
from rnaseq_nav.core import InspectionResult


class RNASeqNavigator:
    """
    Public API for RNASeq Navigator.

    This class coordinates the complete metadata inspection
    pipeline.

    Public methods
    --------------
    fetch()
        Fetch metadata.

    normalize()
        Fetch and normalize metadata.

    validate()
        Fetch, normalize, and validate metadata.

    inspect()
        Execute the complete pipeline and return an
        InspectionResult.
    """

    # ======================================================
    # Initialization
    # ======================================================

    def __init__(
        self,
        email: str,
    ):
        """
        Initialize RNASeq Navigator.

        Parameters
        ----------
        email : str
            Email address used for NCBI Entrez requests.
        """

        self.discovery = DatasetDiscovery(
            email=email
        )

        self.normalizer = MetadataNormalizer()

        self.validator = MetadataValidator()

        self.interpreter = DatasetInterpreter()

        self.report_builder = DatasetReportBuilder()

    # ======================================================
    # Fetch
    # ======================================================

    def fetch(
        self,
        accession: str,
    ):
        """
        Fetch metadata for an accession.

        Parameters
        ----------
        accession : str
            SRA accession such as SRR17730393.

        Returns
        -------
        Metadata
            Metadata returned by the discovery layer.
        """

        return self.discovery.fetch(
            accession
        )

    # ======================================================
    # Normalize
    # ======================================================

    def normalize(
        self,
        accession: str,
    ):
        """
        Fetch and normalize metadata.

        Parameters
        ----------
        accession : str
            SRA accession.

        Returns
        -------
        NormalizationResult
            Structured normalization result.
        """

        metadata = self.fetch(
            accession
        )

        normalization = (
            self.normalizer.normalize(
                metadata
            )
        )

        return normalization

    # ======================================================
    # Validate
    # ======================================================

    def validate(
        self,
        accession: str,
    ):
        """
        Fetch, normalize, and validate metadata.

        Parameters
        ----------
        accession : str
            SRA accession.

        Returns
        -------
        Validation result
        """

        metadata = self.fetch(
            accession
        )

        normalization = (
            self.normalizer.normalize(
                metadata
            )
        )

        normalized_metadata = (
            normalization.metadata
        )

        validation = (
            self.validator.validate(
                normalized_metadata
            )
        )

        return validation

    # ======================================================
    # Inspect
    # ======================================================

    def inspect(
        self,
        accession: str,
    ):
        """
        Execute the complete metadata inspection pipeline.

        Pipeline
        --------

        1. Fetch metadata
        2. Normalize metadata
        3. Validate normalized metadata
        4. Interpret normalized metadata
        5. Build dataset report
        6. Return InspectionResult

        Parameters
        ----------
        accession : str
            SRA accession such as SRR17730393.

        Returns
        -------
        InspectionResult
            Structured inspection result containing:

            - success
            - accession
            - metadata
            - normalization
            - validation
            - report
            - error
        """

        try:

            # ------------------------------------------------
            # Step 1
            # Fetch metadata
            # ------------------------------------------------

            metadata = self.fetch(
                accession
            )

            # ------------------------------------------------
            # Step 2
            # Normalize metadata
            # ------------------------------------------------

            normalization = (
                self.normalizer.normalize(
                    metadata
                )
            )

            normalized_metadata = (
                normalization.metadata
            )

            # ------------------------------------------------
            # Step 3
            # Validate metadata
            # ------------------------------------------------

            validation = (
                self.validator.validate(
                    normalized_metadata
                )
            )

            # ------------------------------------------------
            # Step 4
            # Interpret metadata
            # ------------------------------------------------
            #
            # DatasetInterpreter.describe() returns:
            #
            #     DatasetDescription
            #
            # DatasetReportBuilder.build() expects this
            # object as its fourth argument.

            description = (
                self.interpreter.describe(
                    normalized_metadata
                )
            )

            # ------------------------------------------------
            # Step 5
            # Build report
            # ------------------------------------------------

            report = (
                self.report_builder.build(
                    normalized_metadata,
                    normalization,
                    validation,
                    description,
                )
            )

            # ------------------------------------------------
            # Step 6
            # Return successful result
            # ------------------------------------------------

            return InspectionResult(

                success=True,

                accession=accession,

                metadata=normalized_metadata,

                report=report,

                normalization=normalization,

                validation=validation,

                error=None,

            )

        except Exception as exc:

            # ------------------------------------------------
            # Controlled failure
            # ------------------------------------------------
            #
            # The UI/CLI receives a structured failure instead
            # of an unhandled exception.

            return InspectionResult(

                success=False,

                accession=accession,

                metadata=None,

                report=None,

                normalization=None,

                validation=None,

                error=str(exc),

            )
