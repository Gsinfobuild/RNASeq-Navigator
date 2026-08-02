"""
RNASeq Navigator

Dataset Ranking Test
"""

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery
from rnaseq_nav.discovery.ranker import DatasetRanker


def main():

    discovery = DatasetDiscovery(
        email="gshankar.bbaul@gmail.com"
    )

    datasets = discovery.search(

        organism="Mycobacterium tuberculosis",

        strategy="RNA-Seq",

        layout="PAIRED",

        max_results=20,

        diversity="run",

    )

    print("=" * 80)
    print("Dataset Ranking")
    print("=" * 80)

    for metadata in datasets:

        score = DatasetRanker.score(metadata)

        print()

        print(f"Run      : {metadata.run.accession}")
        print(f"Project  : {metadata.project.accession}")
        print(f"Strategy : {metadata.experiment.library_strategy}")
        print(f"Spots    : {metadata.run.total_spots}")
        print(f"Score    : {score:.2f}")

    print()

    print("=" * 80)
    print("Best Representative Per Project")
    print("=" * 80)

    best = DatasetRanker.best_per_project(datasets)

    for metadata in best:

        print()

        print(f"Project : {metadata.project.accession}")
        print(f"Run     : {metadata.run.accession}")
        print(f"Score   : {DatasetRanker.score(metadata):.2f}")


if __name__ == "__main__":
    main()
