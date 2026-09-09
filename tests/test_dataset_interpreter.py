"""
RNASeq Navigator

Dataset Interpreter Test
"""

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery
from rnaseq_nav.normalization.normalizer import MetadataNormalizer
from rnaseq_nav.intelligence.interpreter import DatasetInterpreter


def main():

    discovery = DatasetDiscovery(

        email="gshankar.bbaul@gmail.com"

    )

    datasets = discovery.search(

        organism="Mycobacterium tuberculosis",

        strategy="RNA-Seq",

        diversity="run",

        max_results=1,

    )

    metadata = datasets[0]

    normalizer = MetadataNormalizer()

    normalized = normalizer.normalize(metadata).metadata

    interpreter = DatasetInterpreter()

    report = interpreter.describe(normalized)

    print("=" * 70)
    print("DATASET INTERPRETATION")
    print("=" * 70)

    print(f"Title      : {report.title}")

    print()

    print("Summary")

    print("-" * 70)

    print(report.summary)

    print()

    print("Sequencing")

    print("-" * 70)

    print(report.sequencing)

    print()

    print("Strengths")

    print("-" * 70)

    if report.strengths:

        for item in report.strengths:

            print(f"✔ {item}")

    else:

        print("None")

    print()

    print("Limitations")

    print("-" * 70)

    if report.limitations:

        for item in report.limitations:

            print(f"• {item}")

    else:

        print("None")


if __name__ == "__main__":

    main()
