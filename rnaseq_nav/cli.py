"""
RNASeq Navigator

Command Line Interface

Version 0.9
"""

import typer

from rnaseq_nav.analysis_engine import analyze_accession

app = typer.Typer()


def render_console_report(result):
    """
    Render a console report from the analysis engine output.
    """

    summary = result["summary"]
    classification = result["classification"]
    conditions = result["conditions"]
    design = result["design"]
    recommendation = result["recommendation"]

    print("\nRNASeq Navigator Report")
    print("=" * 45)

    print(f"Accession        : {summary['accession']}")
    print(f"Organism         : {summary['organism'] or 'Unknown'}")
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


@app.command()
def analyze(accession: str):
    """
    Analyze a BioProject accession.
    """

    result = analyze_accession(accession)

    if result is None:
        print("Accession not found.")
        return

    render_console_report(result)


@app.command()
def version():
    """
    Show software version.
    """

    print("RNASeq Navigator v0.9-dev")


if __name__ == "__main__":
    app()
