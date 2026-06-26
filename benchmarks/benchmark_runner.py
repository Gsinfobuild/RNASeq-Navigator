"""
RNASeq Navigator

Benchmark Runner

Version 0.9
"""

import csv

from rnaseq_nav.analysis_engine import analyze_accession


def main():

    benchmark_file = "benchmarks/benchmark_projects.csv"

    total = 0
    correct = 0

    print("\nRNASeq Navigator Benchmark")
    print("=" * 50)

    with open(benchmark_file, newline="") as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            accession = row["accession"]
            expected = row["expected_type"]

            print(f"\nTesting {accession}")

            result = analyze_accession(accession)

            if result is None:
                print("Failed to retrieve metadata.")
                continue

            predicted = result["classification"]["study_type"]

            print(f"Expected : {expected}")
            print(f"Predicted: {predicted}")

            total += 1

            if predicted == expected:
                print("PASS")
                correct += 1
            else:
                print("FAIL")

    print("\n" + "=" * 50)

    print(f"Projects Tested : {total}")
    print(f"Correct         : {correct}")
    print(f"Incorrect       : {total - correct}")

    if total > 0:

        accuracy = (correct / total) * 100

        print(f"Accuracy        : {accuracy:.1f}%")

    print("=" * 50)


if __name__ == "__main__":
    main()
