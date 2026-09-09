"""
RNASeq Navigator

Navigator Integration Test

Verifies the complete inspection pipeline.
"""

from rnaseq_nav import RNASeqNavigator


def main():

    navigator = RNASeqNavigator(

        email="gshankar.bbaul@gmail.com"

    )

    result = navigator.inspect(

        "SRR17730393"

    )

    print("=" * 70)
    print("RNASeq Navigator")
    print("=" * 70)
    print()

    print("Success        :", result.success)

    print("Accession      :", result.accession)

    print("Metadata       :", result.metadata is not None)

    print("Normalization  :", result.normalization is not None)

    print("Validation     :", result.validation is not None)

    print("Report         :", result.report is not None)

    print("Error          :", result.error)

    if result.report is not None:

        print()

        print("Report Type    :", type(result.report).__name__)


if __name__ == "__main__":

    main()
