"""
RNASeq Navigator
================

Public Navigator API

Version: 1.4

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
    Metadata Intelligence
      ↓
    Modality / Workflow Intelligence
      ↓
    Experimental Design Intelligence
      ↓
    Dataset Suitability
      ↓
    Analysis Planning
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

from rnaseq_nav.discovery.dataset_discovery import (
    DatasetDiscovery,
)

from rnaseq_nav.normalization.normalizer import (
    MetadataNormalizer,
)

from rnaseq_nav.validation.validator import (
    MetadataValidator,
)

from rnaseq_nav.intelligence.interpreter import (
    DatasetInterpreter,
)

from rnaseq_nav.intelligence.report_builder import (
    DatasetReportBuilder,
)

from rnaseq_nav.intelligence.metadata_intelligence import (
    generate_metadata_insight,
)

from rnaseq_nav.intelligence.modality_intelligence import (
    generate_modality_insight,
)

from rnaseq_nav.intelligence.design_intelligence import (
    generate_design_insight,
)

from rnaseq_nav.intelligence.suitability import (
    generate_suitability_insight,
)

from rnaseq_nav.intelligence.analysis_planner import (
    generate_analysis_plan,
)

from rnaseq_nav.core import (
    InspectionResult,
)


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
        ValidationResult
            Structured validation result.
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
        4. Generate metadata intelligence
        5. Classify sequencing modality and workflow compatibility
        6. Generate experimental design intelligence
        7. Generate dataset suitability assessment
        8. Generate contextual analysis plan
        9. Interpret normalized metadata
        10. Build dataset report
        11. Return InspectionResult

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
            - metadata_insight
            - modality_insight
            - design_insight
            - suitability_insight
            - analysis_plan
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
            # Metadata Intelligence
            # ------------------------------------------------
            #
            # Layer 1 converts normalized metadata into
            # a concise biological interpretation.
            #
            # This layer intentionally avoids making
            # unsupported experimental claims.

            metadata_insight = (
                generate_metadata_insight(
                    normalized_metadata,
                )
            )

            # ------------------------------------------------
            # Step 5
            # Modality / Workflow Intelligence
            # ------------------------------------------------
            #
            # Layer 1.5 determines what kind of sequencing
            # experiment is represented by the available
            # library metadata.
            #
            # This classification acts as an important
            # workflow-compatibility gate. The navigator must
            # not assume that every sequencing dataset is
            # appropriate for conventional RNA-seq analysis.
            #
            # Explicit library strategy is treated as the
            # primary evidence.

            modality_insight = (
                generate_modality_insight(
                    normalized_metadata,
                )
            )

            # ------------------------------------------------
            # Step 6
            # Experimental Design Intelligence
            # ------------------------------------------------
            #
            # Layer 2 evaluates the available metadata for
            # possible experimental design information.
            #
            # The design intelligence layer distinguishes
            # observed metadata from cautious inference.
            #
            # It must not assume that sequencing runs are
            # biological replicates.

            design_insight = (
                generate_design_insight(
                    normalized_metadata,
                )
            )

            # ------------------------------------------------
            # Step 7
            # Dataset Suitability
            # ------------------------------------------------
            #
            # Layer 3 evaluates whether the available
            # metadata provides enough evidence to consider
            # the dataset potentially suitable for analysis.
            #
            # The suitability function accepts:
            #
            #     metadata
            #     design_insight
            #     modality_insight
            #
            # Modality compatibility is evaluated before
            # generic RNA-seq suitability scoring.

            suitability_insight = (
                generate_suitability_insight(
                    normalized_metadata,
                    design_insight,
                    modality_insight,
                )
            )

            # ------------------------------------------------
            # Step 8
            # Analysis Planning
            # ------------------------------------------------
            #
            # Layer 4 generates a contextual analysis plan
            # using the outputs of Layers 1–3.
            #
            # The planner expects exactly four arguments:
            #
            #     metadata
            #     metadata_insight
            #     design_insight
            #     suitability_insight

            analysis_plan = (
                generate_analysis_plan(
                    normalized_metadata,
                    metadata_insight,
                    design_insight,
                    suitability_insight,
                    modality_insight,
                )
            )

            # ------------------------------------------------
            # Step 9
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
            # Step 10
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
            # Step 11
            # Return successful result
            # ------------------------------------------------

            return InspectionResult(

                success=True,

                accession=accession,

                metadata=normalized_metadata,

                metadata_insight=metadata_insight,

                modality_insight=modality_insight,

                design_insight=design_insight,

                suitability_insight=suitability_insight,

                analysis_plan=analysis_plan,

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

                metadata_insight=None,

                modality_insight=None,

                design_insight=None,

                suitability_insight=None,

                analysis_plan=None,

                report=None,

                normalization=None,

                validation=None,

                error=str(exc),

            )
