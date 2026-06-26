"""
RNASeq Navigator

Benchmark Validator

Version 0.9
"""

import csv
import re


REQUIRED_FIELDS = [
    "accession",
    "expected_type",
    "expected_pipeline",
    "organism",
    "platform",
    "layout",
    "validated",
    "notes",
]


def load_benchmark(csv_file):

    with open(csv_file, newline="", encoding="utf-8") as f:

        return list(csv.DictReader(f))


def validate(projects):

    print("\nRNASeq Navigator Benchmark Validation")
    print("=" * 55)

    duplicates = set()
    seen = set()

    invalid = 0

    missing = 0

    for project in projects:

        accession = project["accession"]

        if accession in seen:
            duplicates.add(accession)

        seen.add(accession)

        if not re.match(r"^PRJNA\d+$", accession):
            invalid += 1

        for field in REQUIRED_FIELDS:

            if project[field].strip() == "":
                missing += 1

    print(f"Projects          : {len(projects)}")
    print(f"Duplicate IDs     : {len(duplicates)}")
    print(f"Invalid IDs       : {invalid}")
    print(f"Missing Fields    : {missing}")

    if duplicates:

        print("\nDuplicate Accessions")

        for d in duplicates:
            print(" -", d)

    print("=" * 55)


if __name__ == "__main__":

    projects = load_benchmark(
        "benchmarks/benchmark_projects.csv"
    )

    validate(projects)
