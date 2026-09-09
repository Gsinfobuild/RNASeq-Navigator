"""
RNASeq Navigator

Multiple SRR Accession Test

Purpose
-------
Verify that RNASeq Navigator can process
multiple independent SRR accessions using
the same public API.
"""

from rnaseq_nav import RNASeqNavigator


def main():

    navigator = RNASeqNavigator(
        email="gshankar.bbaul@gmail.com"
    )

    accessions = [
        "SRR17730393",
        "SRR17730394",
        "SRR17730395",
    ]

    print("=" * 70)
    print("RNASeq Navigator - Multiple SRR Test")
    print("=" * 70)

    print()

    for accession in accessions:

        print("-" * 70)
        print(f"Testing: {accession}")
        print("-" * 70)

        result = navigator.inspect(
            accession
        )

        print(
            "Success        :",
            result.success
        )

        print(
            "Accession      :",
            result.accession
        )

        print(
            "Metadata       :",
            result.metadata is not None
        )

        print(
            "Normalization  :",
            result.normalization is not None
        )

        print(
            "Validation     :",
            result.validation is not None
        )

        print(
            "Report         :",
            result.report is not None
        )

        print(
            "Error          :",
            result.error
        )

        print()


if __name__ == "__main__":

    main()
