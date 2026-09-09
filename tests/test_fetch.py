"""
RNASeq Navigator

Dataset Fetch Test
"""

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery


ACCESSIONS = [

    "SRR17730393",

    "SRR521457",

    "ERR315346",

    "DRR138920",

]


def main():

    discovery = DatasetDiscovery(

        email="gshankar.bbaul@gmail.com"

    )

    print("=" * 70)
    print("RNASeq Navigator Fetch Benchmark")
    print("=" * 70)

    for accession in ACCESSIONS:

        print()

        print("-" * 60)

        print(accession)

        try:

            metadata = discovery.fetch(accession)

            print("SUCCESS")

            print(

                metadata.sample.organism

            )

            print(

                metadata.experiment.library_strategy

            )

            print(

                metadata.run.accession

            )

        except Exception as error:

            print("FAILED")

            print(error)


if __name__ == "__main__":

    main()
