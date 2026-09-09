"""
RNASeq Navigator

Dataset Report Model

Version: 1.0

Purpose
-------
Defines the canonical DatasetReport object used by
RNASeq Navigator.

DatasetReport is a structured representation of all
information associated with a sequencing accession.

It is intentionally independent of any output format.

Console, JSON, Markdown, HTML and future GUI components
should all consume this object.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# Report Section
# ==========================================================

@dataclass
class ReportSection:
    """
    Generic report section.

    Each section contains a title and a dictionary of
    key-value pairs.
    """

    title: str

    fields: dict[str, Any] = field(
        default_factory=dict
    )

    def add(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add a field to the section.
        """

        self.fields[key] = value

    @property
    def empty(self) -> bool:
        """
        True if the section contains no fields.
        """

        return len(self.fields) == 0


# ==========================================================
# Dataset Report
# ==========================================================

@dataclass
class DatasetReport:
    """
    Canonical report object.

    This object is produced by DatasetReportBuilder
    and later rendered by different output formatters.
    """

    accession: str = ""

    generated_by: str = "RNASeq Navigator"

    version: str = "1.0"

    identity: ReportSection = field(
        default_factory=lambda: ReportSection(
            "Dataset Identity"
        )
    )

    biology: ReportSection = field(
        default_factory=lambda: ReportSection(
            "Biological Information"
        )
    )

    sequencing: ReportSection = field(
        default_factory=lambda: ReportSection(
            "Sequencing Information"
        )
    )

    study: ReportSection = field(
        default_factory=lambda: ReportSection(
            "Study Information"
        )
    )

    project: ReportSection = field(
        default_factory=lambda: ReportSection(
            "BioProject"
        )
    )

    sample: ReportSection = field(
        default_factory=lambda: ReportSection(
            "BioSample"
        )
    )

    publications: ReportSection = field(
        default_factory=lambda: ReportSection(
            "Publications"
        )
    )

    external_links: ReportSection = field(
        default_factory=lambda: ReportSection(
            "External Links"
        )
    )

    validation: ReportSection = field(
        default_factory=lambda: ReportSection(
            "Validation"
        )
    )

    normalization: ReportSection = field(
        default_factory=lambda: ReportSection(
            "Normalization"
        )
    )

    provenance: ReportSection = field(
        default_factory=lambda: ReportSection(
            "Metadata Provenance"
        )
    )

    metadata_completeness: ReportSection = field(
        default_factory=lambda: ReportSection(
            "Metadata Completeness"
        )
    )

    # ------------------------------------------------------

    def sections(self) -> list[ReportSection]:
        """
        Return report sections in display order.
        """

        return [

            self.identity,

            self.biology,

            self.sequencing,

            self.study,

            self.project,

            self.sample,

            self.publications,

            self.external_links,

            self.validation,

            self.normalization,

            self.provenance,

            self.metadata_completeness,

        ]

    # ------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Convert report into a JSON-serializable dictionary.
        """

        data = {

            "accession": self.accession,

            "generated_by": self.generated_by,

            "version": self.version,

        }

        for section in self.sections():

            data[section.title] = section.fields

        return data
