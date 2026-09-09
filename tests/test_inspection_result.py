from rnaseq_nav.core import InspectionResult


def main():

    result = InspectionResult(

        success=True,

        accession="SRR17730393",

    )

    print("=" * 60)

    print("Inspection Result Test")

    print("=" * 60)

    print(result)

    print()

    print(result.success)

    print(result.accession)


if __name__ == "__main__":
    main()
