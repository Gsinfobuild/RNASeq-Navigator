"""
RNASeq Navigator

Benchmark Dataset Manager

Version 1.0

Safely adds validated BioProjects to the
benchmark dataset.
"""

import csv
from pathlib import Path

import typer

from benchmarks.validation.curator import (
    generate_csv_entry,
)

from benchmarks.benchmark_builder import (
    build_benchmark,
)

app = typer.Typer()

CATEGORY_DIR = Path("benchmarks/categories")


@app.command()
def add(accession: str):
    """
    Add a validated BioProject to the benchmark dataset.
    """

    result = generate_csv_entry(accession)

    if result is None:

        print("BioProject is not ready for benchmark inclusion.")
        return

    category_file = CATEGORY_DIR / result["category"]

    row = result["row"]

    # -----------------------------------------
    # Duplicate check
    # -----------------------------------------

    with open(
        category_file,
        newline="",
        encoding="utf-8",
    ) as handle:

        reader = csv.DictReader(handle)

        for existing in reader:

            if existing["accession"] == row["accession"]:

                print("\nDuplicate accession detected.")
                print("Dataset was not modified.")
                return

    # -----------------------------------------
    # Append entry
    # -----------------------------------------

    with open(
        category_file,
        "a",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=row.keys(),
        )

        writer.writerow(row)

    print("\nEntry successfully added.")

    print(f"Category : {category_file.name}")

    # -----------------------------------------
    # Rebuild benchmark
    # -----------------------------------------

    print("\nRebuilding master benchmark...")

    build_benchmark()

    print("\nDataset updated successfully.")


if __name__ == "__main__":
    app()
