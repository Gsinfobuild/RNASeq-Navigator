import typer
from metadata import fetch_study_info
from recommender import recommend_pipeline

app = typer.Typer()

@app.command()
def analyze(accession: str):
    """Analyze an RNA-seq accession."""

    study = fetch_study_info(accession)

    if study is None:
        print("Accession not found.")
        return

    print("\nRNASeq Navigator Report")
    print("=" * 30)

    print(f"Accession: {study['study_accession']}")
    print(f"Organism: {study['scientific_name']}")
    print(f"Samples: {study['sample_count']}")
    print(f"Platform: {study['platform']}")
    print(f"Layout: {study['layout']}")

    recommendation = recommend_pipeline(
        study["scientific_name"],
        study["layout"]
    )

    print("\nRecommended Pipeline")
    print("-" * 25)

    print(f"Aligner: {recommendation['aligner']}")
    print(f"Quantification: {recommendation['quantification']}")
    print(f"Differential Expression: {recommendation['de']}")

@app.command()
def version():
    """Show version."""
    print("RNASeq Navigator v0.1")

if __name__ == "__main__":
    app()
