"""
RNASeq Navigator

BioProject Validation Tool

Version 1.0

Validates a BioProject before adding it to the benchmark.
"""

import typer

from rnaseq_nav.analysis_engine import analyze_accession


app = typer.Typer()


@app.command()
def validate(accession: str):
    """
    Validate a BioProject for benchmark inclusion.
    """

    print("\nRNASeq Navigator BioProject Validator")
    print("=" * 60)

    result = analyze_accession(accession)

    if result is None:

        print("Unable to retrieve BioProject metadata.")
        print("Validation Status : REJECTED")

        return

    summary = result["summary"]
    classification = result["classification"]
    recommendation = result["recommendation"]

    print(f"Accession      : {summary['accession']}")
    print(f"Organism       : {summary['organism']}")
    print(f"Study Type     : {classification['study_type']}")
    print(f"Confidence     : {classification['confidence']}%")
    print(f"Platform       : {summary['platform']}")
    print(f"Layout         : {summary['layout']}")
    print(f"Runs           : {summary['runs']}")

    print("\nValidation Checklist")
    print("-" * 60)

    metadata_ok = summary["runs"] > 0
    platform_ok = summary["platform"] != "Unknown"
    layout_ok = summary["layout"] != "Unknown"
    classification_ok = classification["study_type"] != "Unknown"
    pipeline_ok = recommendation["aligner"] != "Unknown"

    checks = [
        ("Metadata retrieved", metadata_ok),
        ("Platform detected", platform_ok),
        ("Layout detected", layout_ok),
        ("Study classified", classification_ok),
        ("Pipeline recommended", pipeline_ok),
    ]

    for label, passed in checks:

        status = "PASS" if passed else "FAIL"

        print(f"{label:<25} : {status}")

    print("-" * 60)

    if all(flag for _, flag in checks):

        print("Validation Status : READY FOR BENCHMARK")

    else:

        print("Validation Status : REVIEW REQUIRED")


if __name__ == "__main__":
    app()
