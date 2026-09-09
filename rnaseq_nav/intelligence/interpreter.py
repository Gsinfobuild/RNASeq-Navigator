"""
RNASeq Navigator

Dataset Intelligence Engine

Version 1.0

Purpose
-------
Translate metadata into a human-readable description
of the dataset.
"""

from dataclasses import dataclass, field


# ==========================================================
# Dataset Description
# ==========================================================

@dataclass
class DatasetDescription:
    """
    Human-readable interpretation of one dataset.
    """

    title: str = ""

    summary: str = ""

    organism: str = ""

    sequencing: str = ""

    experiment: str = ""

    strengths: list[str] = field(default_factory=list)

    limitations: list[str] = field(default_factory=list)


# ==========================================================
# Dataset Interpreter
# ==========================================================

class DatasetInterpreter:
    """
    Converts normalized metadata into an
    easy-to-understand explanation.
    """

    # -----------------------------------------------------

    def describe(self, metadata):

        description = DatasetDescription()

        # -------------------------------------------------
        # Organism
        # -------------------------------------------------

        description.organism = metadata.sample.organism

        # -------------------------------------------------
        # Experiment type
        # -------------------------------------------------

        strategy = metadata.experiment.library_strategy

        strategy_map = {

            "RNA_SEQ":
                "Bulk RNA sequencing",

            "MRNA_SEQ":
                "Messenger RNA sequencing",

            "NCRNA_SEQ":
                "Non-coding RNA sequencing",

            "MIRNA_SEQ":
                "MicroRNA sequencing",

            "SMRNA_SEQ":
                "Small RNA sequencing",

            "ATAC_SEQ":
                "Chromatin accessibility sequencing",

            "CHIP_SEQ":
                "Protein-DNA interaction sequencing",

            "RAD_SEQ":
                "Restriction-site associated DNA sequencing",

            "WGS":
                "Whole genome sequencing",

            "WXS":
                "Whole exome sequencing",

        }

        description.experiment = strategy_map.get(

            strategy,

            strategy,

        )

        # -------------------------------------------------
        # Layout explanation
        # -------------------------------------------------

        if metadata.experiment.layout == "PAIRED":

            layout_text = (
                "paired-end sequencing, where both "
                "ends of each fragment were sequenced."
            )

            description.strengths.append(

                "Improved alignment accuracy"

            )

            description.strengths.append(

                "Better transcript quantification"

            )

        else:

            layout_text = (
                "single-end sequencing, where one "
                "end of each fragment was sequenced."
            )

            description.limitations.append(

                "Lower alignment information than paired-end data"

            )

        # -------------------------------------------------
        # Platform
        # -------------------------------------------------

        platform_map = {

            "ILLUMINA":
                "Illumina",

            "ION_TORRENT":
                "Ion Torrent",

            "PACBIO_SMRT":
                "PacBio SMRT",

            "OXFORD_NANOPORE":
                "Oxford Nanopore",

            "BGISEQ":
                "BGI sequencing platform",

        }

        platform = platform_map.get(

            metadata.experiment.platform,

            metadata.experiment.platform,

        )

        description.sequencing = (

            f"The dataset was generated using "

            f"{layout_text} "

            f"The sequencing platform was {platform}."

        )

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        description.title = (

            f"{description.experiment} dataset"

        )

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        description.summary = (

            f"This dataset contains "

            f"{description.experiment.lower()} "

            f"data generated from "

            f"{description.organism}. "

            f"The sequencing experiment used "

            f"{metadata.experiment.layout.lower()} "

            f"libraries on the "

            f"{platform} platform."

        )

        # -------------------------------------------------
        # Generic strengths
        # -------------------------------------------------

        if metadata.run.total_spots > 10000000:

            description.strengths.append(

                "High sequencing depth"

            )

        if metadata.run.public:

            description.strengths.append(

                "Publicly available dataset"

            )

        return description
