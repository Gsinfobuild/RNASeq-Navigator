import typer
from metadata import fetch_study_info

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

@app.command()
def version():
    """Show version."""
    print("RNASeq Navigator v0.1")

if __name__ == "__main__":
    app()
