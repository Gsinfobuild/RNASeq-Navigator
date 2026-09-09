"""
RNASeq Navigator

Dataset Report Builder Test
"""

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery
from rnaseq_nav.normalization.normalizer import MetadataNormalizer
from rnaseq_nav.validation.validator import MetadataValidator
from rnaseq_nav.intelligence.interpreter import DatasetInterpreter
from rnaseq_nav.intelligence.report_builder import DatasetReportBuilder


def main():

    discovery = DatasetDiscovery(
        email="gshankar.bbaul@gmail.com"
    )

    metadata = discovery.search(

        organism="Mycobacterium tuberculosis",

        strategy="RNA-Seq",

        max_results=1,

        diversity="run",

    )[0]

    normalization = MetadataNormalizer().normalize(metadata)

    normalized = normalization.metadata

    validation = MetadataValidator().validate(normalized)

    description = DatasetInterpreter().describe(normalized)

    report = DatasetReportBuilder().build(

        normalized,

        normalization,

        validation,

        description,

    )

    print("=" * 70)
    print("RNASeq Navigator Report")
    print("=" * 70)

    print()

    print("Identity")
    print("-" * 70)

    print("Run        :", report.run)
    print("Project    :", report.project)
    print("Study      :", report.study)
    print("Experiment :", report.experiment)
    print("Organism   :", report.organism)

    print()

    print("Experiment")
    print("-" * 70)

    print("Strategy   :", report.strategy)
    print("Layout     :", report.layout)
    print("Platform   :", report.platform)
    print("Instrument :", report.instrument)

    print()

    print("Sequencing")
    print("-" * 70)

    print("Reads       :", f"{report.total_spots:,}")
    print("Bases       :", f"{report.total_bases:,}")

    print()

    print("Metadata Quality")
    print("-" * 70)

    print("Validation Score     :", report.validation_score)
    print("Normalization Changes:", report.normalization_changes)

    print()

    print("Interpretation")
    print("-" * 70)

    print(report.summary)

    print()

    print("Strengths")

    for item in report.strengths:

        print("✔", item)

    if report.limitations:

        print()

        print("Limitations")

        for item in report.limitations:

            print("•", item)


if __name__ == "__main__":

    main()
