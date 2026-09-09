"""
RNASeq Navigator

Dataset Report Reproducibility Benchmark

Version 1.0

Purpose
-------
Verify that the complete RNASeq Navigator pipeline
works consistently across many public datasets.

Pipeline Tested

Discovery
↓

Metadata Parsing
↓

Normalization
↓

Validation
↓

Interpretation
↓

Report Builder
"""

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery
from rnaseq_nav.normalization.normalizer import MetadataNormalizer
from rnaseq_nav.validation.validator import MetadataValidator
from rnaseq_nav.intelligence.interpreter import DatasetInterpreter
from rnaseq_nav.intelligence.report_builder import DatasetReportBuilder


# ==========================================================
# Benchmark Datasets
# ==========================================================

TEST_DATASETS = {

    "Bacterial RNA-seq": [

        "SRR17730393",

        "SRR17730394",

        "SRR17730395",

    ],

    "Human RNA-seq": [

        "SRR521457",

        "SRR521458",

    ],

    "Mouse RNA-seq": [

        "SRR1553606",

        "SRR1553607",

    ],

    "Plant RNA-seq": [

        "SRR1946547",

        "SRR959239",

    ],

    "Yeast RNA-seq": [

        "SRR453566",

    ],

    "Fish RNA-seq": [

        "SRR1030194",

    ],

    "ENA": [

        "ERR315346",

    ],

    "DDBJ": [

        "DRR138920",

    ],

}


# ==========================================================
# Benchmark
# ==========================================================

def main():

    discovery = DatasetDiscovery(
        email="gshankar.bbaul@gmail.com"
    )

    normalizer = MetadataNormalizer()

    validator = MetadataValidator()

    interpreter = DatasetInterpreter()

    builder = DatasetReportBuilder()

    total = 0
    passed = 0
    failed = 0

    print("=" * 80)
    print("RNASeq Navigator Report Reproducibility Benchmark")
    print("=" * 80)

    for category, accessions in TEST_DATASETS.items():

        print()
        print("=" * 80)
        print(category)
        print("=" * 80)

        for accession in accessions:

            total += 1

            print()
            print("-" * 60)
            print("Testing:", accession)

            try:

                metadata = discovery.fetch(accession)

                normalization = normalizer.normalize(metadata)

                normalized = normalization.metadata

                validation = validator.validate(normalized)

                description = interpreter.describe(normalized)

                report = builder.build(

                    normalized,

                    normalization,

                    validation,

                    description,

                )

                print("✓ PASSED")

                print("Organism :", report.organism)

                print("Strategy :", report.strategy)

                print("Layout   :", report.layout)

                print("Platform :", report.platform)

                print("Score    :", report.validation_score)

                print("Reads    :", f"{report.total_spots:,}")

                passed += 1

            except Exception as error:

                failed += 1

                print("✗ FAILED")

                print(type(error).__name__)

                print(error)

    print()
    print("=" * 80)
    print("Benchmark Summary")
    print("=" * 80)

    print(f"Datasets Tested : {total}")

    print(f"Passed          : {passed}")

    print(f"Failed          : {failed}")

    accuracy = 0

    if total:

        accuracy = (passed / total) * 100

    print(f"Success Rate    : {accuracy:.1f}%")

    print("=" * 80)


if __name__ == "__main__":

    main()
