import typer

from metadata import fetch_study_info
from recommender import recommend_pipeline
from design_detector import detect_conditions
from study_classifier import classify_study

app = typer.Typer()


@app.command()
def analyze(accession: str):
    """Analyze a sequencing study accession."""

    study = fetch_study_info(accession)

    if study is None:
        print("Accession not found.")
        return

    study_type = classify_study(study)

    print("\nRNASeq Navigator Report")
    print("=" * 30)

    print(f"Accession: {study['study_accession']}")
    print(f"Organism: {study['scientific_name']}")
    print(f"Study Type: {study_type}")
    print(f"Samples: {study['sample_count']}")
    print(f"Platform: {study['platform']}")
    print(f"Layout: {study['layout']}")

    # Detect experimental conditions
    conditions = detect_conditions(
        study["run_metadata"]
    )

    print("\nStudy Conditions")
    print("-" * 25)

    for condition in conditions:
        print(condition)

    # Study-type-specific recommendations
    recommendation = recommend_pipeline(
        study_type
    )

    print("\nRecommended Pipeline")
    print("-" * 25)

    print(f"Primary Tool: {recommendation['aligner']}")
    print(f"Quantification: {recommendation['quantification']}")
    print(f"Analysis: {recommendation['analysis']}")

@app.command()
def version():
    """Show version."""
    print("RNASeq Navigator v0.6")


if __name__ == "__main__":
    app()
