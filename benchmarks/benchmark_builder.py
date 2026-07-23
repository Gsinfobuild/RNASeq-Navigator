"""
RNASeq Navigator

Benchmark Builder

Version 1.0

Combines all benchmark category files into one
master benchmark CSV.
"""

from pathlib import Path
import csv


CATEGORY_DIR = Path("benchmarks/categories")

OUTPUT_FILE = Path("benchmarks/benchmark_projects.csv")


def build_benchmark():

    rows = []

    for csv_file in sorted(CATEGORY_DIR.glob("*.csv")):

        with open(csv_file, newline="", encoding="utf-8") as handle:

            reader = csv.DictReader(handle)

            for row in reader:
                rows.append(row)

    if not rows:
        print("No benchmark entries found.")
        return

    fieldnames = rows[0].keys()

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(rows)

    print(f"Benchmark written to {OUTPUT_FILE}")

    print(f"Total projects: {len(rows)}")


if __name__ == "__main__":

    build_benchmark()
