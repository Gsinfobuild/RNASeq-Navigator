"""
RNASeq Navigator

Metadata Validation Test
"""

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery
from rnaseq_nav.normalization.normalizer import MetadataNormalizer
from rnaseq_nav.validation.validator import MetadataValidator


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

    normalized = normalizer.normalize(metadata).metadata

    validator = MetadataValidator()

    result = validator.validate(normalized)

    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    print(f"Quality Score : {result.quality_score:.1f}")

    print(f"Total Issues  : {result.summary['total_issues']}")

    print()

    print("Issues by Severity")

    print("-" * 30)

    for severity, count in result.summary["by_severity"].items():

        print(f"{severity:<10} {count}")

    print()

    print("Issues by Section")

    print("-" * 30)

    for section, count in result.summary["by_section"].items():

        print(f"{section:<15} {count}")

    print()

    print("=" * 70)
    print("DETAILED ISSUES")
    print("=" * 70)

    if not result.issues:

        print("No validation issues detected.")

    else:

        for i, issue in enumerate(result.issues, start=1):

            print()

            print(f"{i}.")

            print(f"Severity : {issue.severity}")

            print(f"Section  : {issue.section}")

            print(f"Field    : {issue.field}")

            print(f"Message  : {issue.message}")


if __name__ == "__main__":

    main()
