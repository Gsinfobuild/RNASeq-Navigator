"""
RNASeq Navigator

BioProject Evaluation Script

Tests one or more BioProject accessions using the
RNASeq Navigator analysis engine.
"""

from rnaseq_nav.analysis_engine import analyze_accession

BIOPROJECTS = [
    "PRJDB18474",
    "PRJNA1493258",
    "PRJNA1492197",
    "PRJDB42722",
    "PRJNA1495506",
    "PRJNA1491685",
    "PRJNA1489785",
    "PRJNA1489741",
    "PRJNA1480001",
]


def main():

    print("\nRNASeq Navigator - BioProject Evaluation")
    print("=" * 80)

    successful = 0
    failed = 0

    for accession in BIOPROJECTS:

        print("\n" + "-" * 80)
        print(f"Analyzing: {accession}")

        try:

            result = analyze_accession(accession)

            if result is None:
                print("❌ Metadata retrieval failed.")
                failed += 1
                continue

            metadata = result.get("metadata", {})
            classification = result.get("classification", {})

            print(f"Study Type : {classification.get('study_type', 'Unknown')}")
            print(f"Organism   : {metadata.get('organism', 'Unknown')}")
            print(f"Platform   : {metadata.get('platform', 'Unknown')}")
            print(f"Layout     : {metadata.get('layout', 'Unknown')}")
            print(f"Runs       : {metadata.get('runs', 'Unknown')}")

            if "pipeline" in result:
                print(f"Pipeline   : {result['pipeline']}")

            if "design" in result:
                print(f"Design     : {result['design']}")

            successful += 1

        except Exception as e:

            print(f"❌ ERROR: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print("Evaluation Summary")
    print("=" * 80)
    print(f"Projects Tested : {len(BIOPROJECTS)}")
    print(f"Successful      : {successful}")
    print(f"Failed          : {failed}")
    print("=" * 80)


if __name__ == "__main__":
    main()
