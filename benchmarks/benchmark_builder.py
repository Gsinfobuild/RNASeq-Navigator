"""
RNASeq Navigator

Benchmark Builder

Version 0.9
"""

import csv


def load_benchmark(csv_file):
    """
    Load benchmark dataset.
    """

    projects = []

    with open(csv_file, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:
            projects.append(row)

    return projects


def benchmark_summary(projects):

    print("\nRNASeq Navigator Benchmark")
    print("=" * 45)

    print(f"Projects : {len(projects)}")

    study_types = {}

    for project in projects:

        study = project["expected_type"]

        study_types[study] = study_types.get(study, 0) + 1

    print("\nStudy Types")

    print("-" * 45)

    for study, count in sorted(study_types.items()):

        print(f"{study:<20} {count}")

    print("=" * 45)


if __name__ == "__main__":

    projects = load_benchmark(
        "benchmarks/benchmark_projects.csv"
    )

    benchmark_summary(projects)
