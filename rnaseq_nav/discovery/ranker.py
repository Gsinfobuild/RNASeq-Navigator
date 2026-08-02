"""
RNASeq Navigator

Dataset Ranking Engine

Version 1.0

Purpose
-------
Assign a quality score to each Metadata object and
select the best representative dataset.
"""

from collections import defaultdict


class DatasetRanker:

    @staticmethod
    def score(metadata):
        """
        Compute a quality score for one dataset.
        Higher score = better representative.
        """

        score = 0

        # --------------------------------------------------
        # Sequencing depth
        # --------------------------------------------------

        if metadata.run.total_spots:
            score += metadata.run.total_spots / 1_000_000

        if metadata.run.total_bases:
            score += metadata.run.total_bases / 100_000_000

        # --------------------------------------------------
        # Metadata completeness
        # --------------------------------------------------

        if metadata.project.accession:
            score += 5

        if metadata.study.accession:
            score += 5

        if metadata.sample.biosample:
            score += 5

        if metadata.sample.organism:
            score += 5

        if metadata.experiment.platform:
            score += 3

        if metadata.experiment.instrument:
            score += 3

        # --------------------------------------------------
        # Public data
        # --------------------------------------------------

        if metadata.run.public:
            score += 2

        # --------------------------------------------------
        # Preferred RNA strategies
        # --------------------------------------------------

        strategy = metadata.experiment.library_strategy.upper()

        if strategy == "RNA-SEQ":
            score += 10

        elif strategy == "NCRNA-SEQ":
            score += 8

        elif strategy == "MRNA-SEQ":
            score += 9

        return score

    # ------------------------------------------------------

    @staticmethod
    def best_per_project(metadata_list):
        """
        Keep the highest-scoring dataset
        for each BioProject.
        """

        grouped = defaultdict(list)

        for metadata in metadata_list:

            project = metadata.project.accession

            if project:

                grouped[project].append(metadata)

        selected = []

        for project, datasets in grouped.items():

            best = max(
                datasets,
                key=DatasetRanker.score
            )

            selected.append(best)

        return selected
