"""
RNASeq Navigator

Metadata Regression Test Suite

Version 2.0

Purpose
-------
Regression testing of the metadata parser across
multiple RNA-seq experiment categories.
"""

from Bio import Entrez

from rnaseq_nav.parsers.sra_parser import SRAParser
from tests.regression.regression_datasets import REGRESSION_DATASETS


EMAIL = "gshankar.bbaul@gmail.com"


# ==========================================================
# Retrieve ESummary record
# ==========================================================

def retrieve_record(accession):

    search = Entrez.esearch(
        db="sra",
        term=accession
    )

    search_record = Entrez.read(search)

    search.close()

    ids = search_record["IdList"]

    if len(ids) == 0:
        return None

    uid = ids[0]

    summary = Entrez.esummary(
        db="sra",
        id=uid,
        retmode="xml"
    )

    record = Entrez.read(summary)[0]

    summary.close()

    return record


# ==========================================================
# Metadata validator
# ==========================================================

def validate(metadata):

    required = {

        "Project":
            metadata.project.accession,

        "Study":
            metadata.study.accession,

        "Experiment":
            metadata.experiment.accession,

        "Run":
            metadata.run.accession,

        "Organism":
            metadata.sample.organism,

        "Library Strategy":
            metadata.experiment.library_strategy,

        "Layout":
            metadata.experiment.layout,

        "Platform":
            metadata.experiment.platform,

        "Instrument":
            metadata.experiment.instrument,

        "BioSample":
            metadata.sample.biosample,

    }

    missing = []

    for field, value in required.items():

        if value is None:

            missing.append(field)

        elif isinstance(value, str):

            if value.strip() == "":

                missing.append(field)

    return missing


# ==========================================================
# Main regression test
# ==========================================================

def main():

    Entrez.email = EMAIL

    parser = SRAParser()

    total_tests = 0

    total_passed = 0

    total_failed = 0

    category_summary = {}

    print("=" * 80)
    print("RNASeq Navigator Regression Benchmark")
    print("=" * 80)

    for category, accessions in REGRESSION_DATASETS.items():

        print()
        print("=" * 80)
        print(category)
        print("=" * 80)

        passed = 0

        failed = 0

        for accession in accessions:

            total_tests += 1

            print()
            print("-" * 60)
            print(f"Testing : {accession}")

            try:

                record = retrieve_record(accession)

                if record is None:

                    print("❌ Accession not found")

                    failed += 1

                    total_failed += 1

                    continue

                metadata = parser.parse(

                    record["ExpXml"],

                    record["Runs"]

                )

                missing = validate(metadata)

                if len(missing) == 0:

                    print("✅ PASSED")

                    print(f"Organism : {metadata.sample.organism}")

                    print(f"Strategy : {metadata.experiment.library_strategy}")

                    print(f"Layout   : {metadata.experiment.layout}")

                    print(f"Run      : {metadata.run.accession}")

                    passed += 1

                    total_passed += 1

                else:

                    print("❌ FAILED")

                    print("Missing metadata:")

                    for field in missing:

                        print(f"   - {field}")

                    failed += 1

                    total_failed += 1

            except Exception as e:

                print("❌ ERROR")

                print(e)

                failed += 1

                total_failed += 1

        category_summary[category] = {

            "passed": passed,

            "failed": failed,

            "total": len(accessions)

        }

    # ======================================================
    # Summary
    # ======================================================

    print()
    print("=" * 80)
    print("Regression Summary")
    print("=" * 80)

    print()

    print(f"{'Category':35} {'Passed':>8} {'Failed':>8}")

    print("-" * 60)

    for category, result in category_summary.items():

        print(

            f"{category:35}"

            f"{result['passed']:>8}"

            f"{result['failed']:>8}"

        )

    print("-" * 60)

    print(f"{'TOTAL':35}{total_passed:>8}{total_failed:>8}")

    print()

    accuracy = 0

    if total_tests > 0:

        accuracy = (total_passed / total_tests) * 100

    print(f"Datasets Tested : {total_tests}")

    print(f"Passed          : {total_passed}")

    print(f"Failed          : {total_failed}")

    print(f"Parser Accuracy : {accuracy:.1f}%")

    if total_failed == 0:

        print()

        print("🎉 ALL REGRESSION TESTS PASSED")


if __name__ == "__main__":

    main()
