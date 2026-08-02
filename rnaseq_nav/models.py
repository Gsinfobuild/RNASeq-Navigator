"""
RNASeq Navigator

Metadata Models

Version 1.1

Defines the core metadata objects used throughout
RNASeq Navigator.
"""

from dataclasses import dataclass, field
from typing import Optional


# ==========================================================
# Project Metadata
# ==========================================================

@dataclass
class ProjectMetadata:
    """
    BioProject-level metadata.
    """

    accession: str = ""


# ==========================================================
# Study Metadata
# ==========================================================

@dataclass
class StudyMetadata:
    """
    Study (SRP) metadata.
    """

    accession: str = ""


# ==========================================================
# Experiment Metadata
# ==========================================================

@dataclass
class ExperimentMetadata:
    """
    Experiment (SRX) metadata.
    """

    accession: str = ""

    # Experiment title
    title: str = ""

    # Sequencing information
    library_strategy: str = ""
    library_source: str = ""
    library_selection: str = ""

    # Layout
    layout: str = ""

    # Sequencing platform
    platform: str = ""

    # Instrument model
    instrument: str = ""


# ==========================================================
# Run Metadata
# ==========================================================

@dataclass
class RunMetadata:
    """
    Run (SRR) metadata.
    """

    accession: str = ""

    total_spots: Optional[int] = None

    total_bases: Optional[int] = None

    public: bool = False

    cluster: str = ""

    static_data: bool = False


# ==========================================================
# Sample Metadata
# ==========================================================

@dataclass
class SampleMetadata:
    """
    Sample (SRS/SAMN) metadata.
    """

    accession: str = ""

    biosample: str = ""

    organism: str = ""


# ==========================================================
# Master Metadata Object
# ==========================================================

@dataclass
class Metadata:
    """
    Master metadata object used throughout RNASeq Navigator.
    """

    project: ProjectMetadata = field(
        default_factory=ProjectMetadata
    )

    study: StudyMetadata = field(
        default_factory=StudyMetadata
    )

    experiment: ExperimentMetadata = field(
        default_factory=ExperimentMetadata
    )

    run: RunMetadata = field(
        default_factory=RunMetadata
    )

    sample: SampleMetadata = field(
        default_factory=SampleMetadata
    )
