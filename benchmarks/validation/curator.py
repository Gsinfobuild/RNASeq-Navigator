"""
RNASeq Navigator

Benchmark Curator

Version 2.0

Generates standardized benchmark entries.
"""

import typer

from benchmarks.validation.validation_engine import (
    validate_bioproject,
)

app = typer.Typer()


CATEGORY_FILES = {
    "Bulk RNA-seq": "bulk_rnaseq.csv",
    "Small RNA-seq": "small_rnaseq.csv",
    "Metagenomics": "metagenomics.csv",
    "Unknown": "unknown.csv",
}


def generate_csv_entry(accession):
    """
    Generate a benchmark-ready CSV entry.

    Returns
    -------
    dict
    """

    validation = validate_bioproject(accession)

    if validation["analysis"] is None:
        return None

    if validation["status"] != "READY FOR BENCHMARK":
        return None

    analysis = validation["analysis"]

    summary = analysis["summary"]
    classification = analysis["classification"]

    study_type = classification["study_type"]

    return {

        "category": CATEGORY_FILES.get(
            study_type,
            "unknown.csv",
        ),

        "row": {

            "accession": summary["accession"],

            "organism": summary["organism"],

            "platform": summary["platform"],

            "layout": summary["layout"],

            "expected_type": study_type,

            "status": "Validated",

            "source": "Manual validation",

            "notes": "Validated using RNASeq Navigator",

        }

    }


@app.command()
def curate(accession: str):
    """
    Display the generated benchmark entry.
    """

    result = generate_csv_entry(accession)

    if result is None:

        print("BioProject is not ready for benchmark inclusion.")

        return

    print("\nSuggested Category")
    print("=" * 60)

    print(result["category"])

    print("\nCSV Entry")
    print("=" * 60)

    for key, value in result["row"].items():
        print(f"{key:15}: {value}")


if __name__ == "__main__":
    app()
