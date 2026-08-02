"""
RNASeq Navigator

Dataset Discovery Engine

Version 3.0

Purpose
-------
Discover representative RNA-seq datasets directly
from NCBI using biological search criteria.

Features
--------
- NCBI Entrez search
- Automatic metadata retrieval
- Metadata parsing
- Optional layout filtering
- Quality-based ranking
- Diversity selection
"""

from Bio import Entrez

from rnaseq_nav.parsers.sra_parser import SRAParser
from rnaseq_nav.discovery.diversity import DatasetDiversity
from rnaseq_nav.discovery.ranker import DatasetRanker


class DatasetDiscovery:
    """
    Discover representative RNA-seq datasets.
    """

    def __init__(self, email: str):

        self.email = email

        Entrez.email = email

        self.parser = SRAParser()

    # ======================================================
    # Search
    # ======================================================

    def search(
        self,
        organism=None,
        strategy=None,
        layout=None,
        max_results=20,
        diversity="project",
    ):
        """
        Search NCBI SRA using biological criteria.

        Parameters
        ----------
        organism : str
            Scientific organism name.

        strategy : str
            Library strategy (RNA-Seq, ncRNA-Seq, etc.)

        layout : str
            SINGLE or PAIRED.

        max_results : int
            Maximum candidate records retrieved.

        diversity : str
            project | study | run

        Returns
        -------
        list[Metadata]
        """

        query = []

        if organism:
            query.append(f'"{organism}"[Organism]')

        if strategy:
            query.append(f'"{strategy}"')

        query.append("public[Access]")

        search_term = " AND ".join(query)

        print("=" * 70)
        print("RNASeq Navigator Dataset Discovery")
        print("=" * 70)
        print(search_term)
        print()

        # --------------------------------------------------
        # Search SRA
        # --------------------------------------------------

        handle = Entrez.esearch(
            db="sra",
            term=search_term,
            retmax=max_results,
        )

        search_record = Entrez.read(handle)

        handle.close()

        ids = search_record["IdList"]

        print(f"Candidates found : {len(ids)}")

        metadata_list = []

        # --------------------------------------------------
        # Retrieve metadata
        # --------------------------------------------------

        for uid in ids:

            try:

                summary = Entrez.esummary(
                    db="sra",
                    id=uid,
                    retmode="xml",
                )

                record = Entrez.read(summary)[0]

                summary.close()

                metadata = self.parser.parse(
                    record["ExpXml"],
                    record["Runs"],
                )

                # ------------------------------------------
                # Optional layout filter
                # ------------------------------------------

                if layout:

                    if (
                        metadata.experiment.layout.upper()
                        != layout.upper()
                    ):
                        continue

                metadata_list.append(metadata)

            except Exception as e:

                print(f"Skipping UID {uid}")

                print(e)

        print()
        print(f"Datasets retrieved      : {len(metadata_list)}")

        # ==================================================
        # Diversity Selection
        # ==================================================

        if diversity.lower() == "project":

            print("Applying project diversity ranking...")

            metadata_list = DatasetRanker.best_per_project(
                metadata_list
            )

        elif diversity.lower() == "study":

            print("Applying study diversity...")

            metadata_list = DatasetDiversity.unique_studies(
                metadata_list
            )

        elif diversity.lower() == "run":

            print("Keeping all unique runs...")

            metadata_list = DatasetDiversity.unique_runs(
                metadata_list
            )

        else:

            raise ValueError(
                f"Unknown diversity mode: {diversity}"
            )

        print(
            f"Representative datasets : {len(metadata_list)}"
        )

        # ==================================================
        # Sort representatives by quality score
        # ==================================================

        metadata_list.sort(

            key=DatasetRanker.score,

            reverse=True,

        )

        return metadata_list
