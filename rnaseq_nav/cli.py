"""
RNASeq Navigator

Command Line Interface

Version 1.0
"""

import typer

from rnaseq_nav.analysis_engine import analyze_accession
from rnaseq_nav.exporters.json_exporter import export_json

app = typer.Typer(
    help="RNASeq Navigator - Intelligent BioProject Analysis"
)


# ==========================================================
# Console Renderer
# ==========================================================

def render_console_report(result):
    """
    Render the standard console report.
    """

    summary = result["summary"]
    classification = result["classification"]
    design = result["design"]
    recommendation = result["recommendation"]
    conditions = design["conditions"] if design else {}

    print("\nRNASeq Navigator Report")
    print("=" * 45)

    print(f"Accession        : {summary['accession']}")
    print(f"Organism         : {summary['organism']}")
    print(f"Study Type       : {classification['study_type']}")
    print(f"Confidence       : {classification['confidence']}%")
    print(f"Runs             : {summary['runs']}")
    print(f"Platform         : {summary['platform']}")
    print(f"Layout           : {summary['layout']}")

    print("\nClassification Evidence")
    print("-" * 45)

    if classification["evidence"]:
        for item in classification["evidence"]:
            print(f"• {item}")
    else:
        print("No supporting evidence detected.")

    print("\nStudy Conditions")
    print("-" * 45)

    if conditions:
        for condition, count in sorted(conditions.items()):
            print(f"{condition:<35}{count} run(s)")
    else:
        print("No experimental conditions detected.")

    print("\nExperimental Design Assessment")
    print("-" * 45)

    if design:
        print(f"Conditions Detected : {len(design['conditions'])}")
        print(f"Largest Group       : {design['largest']} run(s)")
        print(f"Smallest Group      : {design['smallest']} run(s)")
        print(f"Design Quality      : {design['quality']}")
    else:
        print("No sequencing runs available.")

    print("\nRecommended Pipeline")
    print("-" * 45)

    print(f"Primary Tool   : {recommendation['aligner']}")
    print(f"Quantification : {recommendation['quantification']}")
    print(f"Analysis       : {recommendation['analysis']}")


# ==========================================================
# Analyze Command
# ==========================================================

@app.command()
def analyze(
    accession: str,
    output: str = typer.Option(
        "console",
        "--output",
        "-o",
        help="Output format: console or json",
    ),
):
    """
    Analyze a BioProject accession.
    """

    result = analyze_accession(accession)

    if result is None:
        typer.echo("Accession not found.")
        raise typer.Exit()

    output = output.lower()

    if output == "console":
        render_console_report(result)

    elif output == "json":
        print(export_json(result))

    else:
        typer.echo(f"\nUnsupported output format: {output}")
        typer.echo("\nSupported formats:")
        typer.echo("  • console")
        typer.echo("  • json")
        raise typer.Exit(code=1)


# ==========================================================
# Version Command
# ==========================================================

@app.command()
def version():
    """
    Show current software version.
    """

    print("RNASeq Navigator v1.0-dev")


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    app()
