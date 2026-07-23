"""
RNASeq Navigator

Benchmark Runner

Version 2.2

Executes the benchmark suite,
computes statistics,
and generates publication-ready reports.
"""

import csv

from rnaseq_nav.analysis_engine import analyze_accession

from benchmarks.benchmark_statistics import calculate_statistics

from benchmarks.benchmark_summary import (
    write_markdown_report,
    write_json_report,
    write_csv_report,
)

SOFTWARE_VERSION = "0.9.0"


def main():
    """
    Execute benchmark validation.
    """

    benchmark_file = "benchmarks/benchmark_projects.csv"

    results = []

    print("\nRNASeq Navigator Benchmark")
    print("=" * 50)

    with open(
        benchmark_file,
        newline="",
        encoding="utf-8",
    ) as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            accession = row["accession"]
            expected = row["expected_type"]

            print(f"\nTesting {accession}")

            analysis = analyze_accession(accession)

            if analysis is None:
                print("Failed to retrieve metadata.")
                continue

            predicted = analysis["classification"]["study_type"]

            print(f"Expected : {expected}")
            print(f"Predicted: {predicted}")

            passed = predicted == expected

            print("PASS" if passed else "FAIL")

            results.append(
                {
                    "accession": accession,
                    "expected": expected,
                    "predicted": predicted,
                    "correct": passed,
                }
            )

    stats = calculate_statistics(results)

    summary = {
        "tested": stats["total"],
        "correct": stats["correct"],
        "incorrect": stats["incorrect"],
        "accuracy": stats["accuracy"],
    }

    class_stats = {}

    for study_type, values in stats["per_class"].items():

        class_stats[study_type] = {
            "projects": values["total"],
            "correct": values["correct"],
            "incorrect": values["incorrect"],
            "accuracy": values["accuracy"],
        }

    print("\n" + "=" * 50)

    print(f"Projects Tested : {summary['tested']}")
    print(f"Correct         : {summary['correct']}")
    print(f"Incorrect       : {summary['incorrect']}")
    print(f"Accuracy        : {summary['accuracy']:.2f}%")

    print("=" * 50)

    print("\nPer-Class Statistics")
    print("=" * 50)

    for study_type in sorted(class_stats):

        values = class_stats[study_type]

        print(f"\n{study_type}")

        print(f"  Projects  : {values['projects']}")
        print(f"  Correct   : {values['correct']}")
        print(f"  Incorrect : {values['incorrect']}")
        print(f"  Accuracy  : {values['accuracy']:.2f}%")

        print("-" * 50)

    print("\nGenerating benchmark reports...")

    write_markdown_report(
        summary=summary,
        class_stats=class_stats,
        benchmark_name=benchmark_file,
        software_version=SOFTWARE_VERSION,
        results=results,
    )

    write_json_report(
        summary=summary,
        class_stats=class_stats,
        benchmark_name=benchmark_file,
        software_version=SOFTWARE_VERSION,
        results=results,
    )

    write_csv_report(results)

    print("\nBenchmark completed successfully.")


if __name__ == "__main__":
    main()
