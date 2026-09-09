"""
RNASeq Navigator

Metadata Normalization Test
"""

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery
from rnaseq_nav.normalization.normalizer import MetadataNormalizer


def main():

    discovery = DatasetDiscovery(

        email="gshankar.bbaul@gmail.com"

    )

    datasets = discovery.search(

        organism="Mycobacterium tuberculosis",

        strategy="RNA-Seq",

        max_results=1,

        diversity="run",

    )

    metadata = datasets[0]

    normalizer = MetadataNormalizer()

    result = normalizer.normalize(metadata)

    normalized = result.metadata

    print("=" * 70)
    print("RAW METADATA")
    print("=" * 70)

    print("Strategy :", metadata.experiment.library_strategy)
    print("Layout   :", metadata.experiment.layout)
    print("Platform :", metadata.experiment.platform)

    print()

    print("=" * 70)
    print("NORMALIZED METADATA")
    print("=" * 70)

    print("Strategy :", normalized.experiment.library_strategy)
    print("Layout   :", normalized.experiment.layout)
    print("Platform :", normalized.experiment.platform)

    print()

    print("=" * 70)
    print("NORMALIZATION SUMMARY")
    print("=" * 70)

    summary = result.summary

    print(f"Total Changes      : {summary['total_changes']}")
    print(f"Sections Modified  : {summary['sections_modified']}")
    print(f"Fields Modified    : {summary['fields_modified']}")

    print()

    print("Changes by Section")

    print("-" * 30)

    for section, count in summary["changes_by_section"].items():

        print(f"{section:<20} {count}")

    print()

    print("Changes by Field")

    print("-" * 30)

    for field, count in summary["changes_by_field"].items():

        print(f"{field:<20} {count}")

    print()

    print("=" * 70)
    print("DETAILED REPORT")
    print("=" * 70)

    for i, change in enumerate(result.report, start=1):

        print()

        print(f"{i}.")

        print(f"Section    : {change.section}")

        print(f"Field      : {change.field}")

        print(f"Original   : {change.original}")

        print(f"Normalized : {change.normalized}")

    print()

    print(f"Normalization Objects : {len(result.report)}")


if __name__ == "__main__":

    main()
