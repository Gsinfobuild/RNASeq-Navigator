"""
RNASeq Navigator

Candidate Screening Engine

Version 2.0

Screens candidate BioProjects, ranks them according
to validation readiness, and automatically saves
a screening report.
"""

from pathlib import Path
import csv

import typer

from benchmarks.validation.validation_engine import (
    validate_bioproject,
)

app = typer.Typer(
    help="Screen candidate BioProjects before benchmark curation."
)

REPORT_DIR = Path("benchmarks/screening_reports")


@app.command()
def screen(candidate_file: str):
    """
    Screen a candidate BioProject CSV file.

    Required CSV column:
        accession
    """

    candidate_path = Path(candidate_file)

    if not candidate_path.exists():
        print(f"\nFile not found: {candidate_path}")
        raise typer.Exit()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_file = (
        REPORT_DIR /
        f"{candidate_path.stem}_screening.csv"
    )

    results = []

    with open(
        candidate_path,
        newline="",
        encoding="utf-8",
    ) as handle:

        reader = csv.DictReader(handle)

        if reader.fieldnames is None:
            print("\nCSV file is empty.")
            raise typer.Exit()

        fieldnames = [field.strip().lower() for field in reader.fieldnames]

        if "accession" not in fieldnames:
            print("\nCSV must contain an 'accession' column.")
            raise typer.Exit()

        accession_index = fieldnames.index("accession")
        accession_column = reader.fieldnames[accession_index]

        for row in reader:

            accession = row.get(accession_column, "").strip()

            if not accession:
                continue

            validation = validate_bioproject(accession)

            analysis = validation.get("analysis")

            if analysis is None:

                organism = "Unknown"
                study_type = "Unknown"

            else:

                organism = (
                    analysis["summary"]
                    .get("organism", "")
                    or "Unknown"
                )

                study_type = (
                    analysis["classification"]
                    .get("study_type", "Unknown")
                )

            results.append(
                {
                    "accession": accession,
                    "organism": organism,
                    "study_type": study_type,
                    "score": validation["score"],
                    "status": validation["status"],
                }
            )

    results.sort(
        key=lambda x: (
            -x["score"],
            x["accession"],
        )
    )

    print("\nRNASeq Navigator Candidate Screening")
    print("=" * 90)

    print(
        f"{'Rank':<6}"
        f"{'Accession':<18}"
        f"{'Study Type':<22}"
        f"{'Score':<8}"
        f"{'Status'}"
    )

    print("-" * 90)

    with open(
        report_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.writer(handle)

        writer.writerow(
            [
                "rank",
                "accession",
                "organism",
                "study_type",
                "score",
                "status",
            ]
        )

        for rank, result in enumerate(results, start=1):

            print(
                f"{rank:<6}"
                f"{result['accession']:<18}"
                f"{result['study_type']:<22}"
                f"{result['score']:<8}"
                f"{result['status']}"
            )

            writer.writerow(
                [
                    rank,
                    result["accession"],
                    result["organism"],
                    result["study_type"],
                    result["score"],
                    result["status"],
                ]
            )

    print("-" * 90)
    print(f"\nCandidates screened : {len(results)}")
    print(f"Screening report saved to:\n{report_file}")


if __name__ == "__main__":
    app()
