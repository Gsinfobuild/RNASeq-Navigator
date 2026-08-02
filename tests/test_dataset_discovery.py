"""
RNASeq Navigator

Dataset Discovery Diversity Test
"""

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery


def main():

    discovery = DatasetDiscovery(
        email="gshankar.bbaul@gmail.com"
    )

    datasets = discovery.search(

        organism="Mycobacterium tuberculosis",

        strategy="RNA-Seq",

        layout="PAIRED",

        max_results=20,

        diversity="project",

    )

    print()

    print("=" * 80)
    print("Representative Datasets")
    print("=" * 80)

    for i, metadata in enumerate(datasets, start=1):

        print()

        print(f"Representative {i}")

        print("-" * 40)

        print(f"Project : {metadata.project.accession}")

        print(f"Study   : {metadata.study.accession}")

        print(f"Run     : {metadata.run.accession}")

        print(f"Strategy: {metadata.experiment.library_strategy}")

        print(f"Layout  : {metadata.experiment.layout}")

        print(f"Organism: {metadata.sample.organism}")


if __name__ == "__main__":
    main()
