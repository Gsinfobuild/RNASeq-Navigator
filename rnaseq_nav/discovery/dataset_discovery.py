"""
RNASeq Navigator

Dataset Discovery Engine

Version 2.0
"""

from Bio import Entrez

from rnaseq_nav.parsers.sra_parser import SRAParser
from rnaseq_nav.discovery.diversity import DatasetDiversity


class DatasetDiscovery:

    def __init__(self, email):

        self.email = email

        Entrez.email = email

        self.parser = SRAParser()

    def search(
        self,
        organism=None,
        strategy=None,
        layout=None,
        max_results=20,
        diversity="project",
    ):

        query = []

        if organism:
            query.append(f'"{organism}"[Organism]')

        if strategy:
            query.append(f'"{strategy}"')

        query.append("public[Access]")

        term = " AND ".join(query)

        print("=" * 70)
        print("RNASeq Navigator Dataset Discovery")
        print("=" * 70)

        print(term)
        print()

        search = Entrez.esearch(
            db="sra",
            term=term,
            retmax=max_results,
        )

        record = Entrez.read(search)

        search.close()

        ids = record["IdList"]

        print(f"Candidates: {len(ids)}")

        metadata_list = []

        for uid in ids:

            try:

                summary = Entrez.esummary(
                    db="sra",
                    id=uid,
                    retmode="xml",
                )

                result = Entrez.read(summary)[0]

                summary.close()

                metadata = self.parser.parse(
                    result["ExpXml"],
                    result["Runs"],
                )

                if layout:

                    if metadata.experiment.layout.upper() != layout.upper():
                        continue

                metadata_list.append(metadata)

            except Exception as e:

                print(f"Skipping UID {uid}")

                print(e)

        print()

        print(f"Before diversity filter : {len(metadata_list)}")

        if diversity == "project":

            metadata_list = DatasetDiversity.unique_projects(
                metadata_list
            )

        elif diversity == "study":

            metadata_list = DatasetDiversity.unique_studies(
                metadata_list
            )

        elif diversity == "run":

            metadata_list = DatasetDiversity.unique_runs(
                metadata_list
            )

        print(f"After diversity filter  : {len(metadata_list)}")

        return metadata_list
