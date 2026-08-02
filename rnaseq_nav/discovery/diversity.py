"""
RNASeq Navigator

Dataset Diversity Selector

Version 1.0

Purpose
-------
Remove redundant datasets and retain only
representative studies.
"""


class DatasetDiversity:
    """
    Select representative datasets from
    a collection of Metadata objects.
    """

    @staticmethod
    def unique_projects(metadata_list):
        """
        Keep one representative dataset
        per BioProject.
        """

        selected = []

        seen = set()

        for metadata in metadata_list:

            project = metadata.project.accession

            if not project:
                continue

            if project not in seen:

                selected.append(metadata)

                seen.add(project)

        return selected

    @staticmethod
    def unique_studies(metadata_list):
        """
        Keep one representative dataset
        per Study.
        """

        selected = []

        seen = set()

        for metadata in metadata_list:

            study = metadata.study.accession

            if not study:
                continue

            if study not in seen:

                selected.append(metadata)

                seen.add(study)

        return selected

    @staticmethod
    def unique_runs(metadata_list):
        """
        Remove duplicate Run accessions.
        """

        selected = []

        seen = set()

        for metadata in metadata_list:

            run = metadata.run.accession

            if not run:
                continue

            if run not in seen:

                selected.append(metadata)

                seen.add(run)

        return selected
