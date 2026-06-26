import typer

from metadata import fetch_study_info
from study_classifier import classify_study
from recommender import recommend_pipeline
from replicate_detector import detect_replicates
from design_assessor import assess_design

app = typer.Typer()


@app.command()
def analyze(accession: str):
    """
    Analyze a BioProject accession using the RNASeq Navigator pipeline.
    """

    # ---------------------------------------------------------
    # Step 1 : Retrieve metadata
    # ---------------------------------------------------------

    study = fetch_study_info(accession)

    if study is None:
        print("Accession not found.")
        return

    # ---------------------------------------------------------
    # Step 2 : Classify study
    # ---------------------------------------------------------

    classification = classify_study(study)

    study_type = classification["study_type"]
    confidence = classification["confidence"]
    evidence = classification["evidence"]

    # ---------------------------------------------------------
    # Step 3 : Recommend workflow
    # ---------------------------------------------------------

    recommendation = recommend_pipeline(study_type)

    # ---------------------------------------------------------
    # Step 4 : Detect study conditions
    # ---------------------------------------------------------

    conditions = detect_replicates(
        study["run_metadata"]
    )

    # ---------------------------------------------------------
    # Step 5 : Assess experimental design
    # ---------------------------------------------------------

    design = assess_design(
        study["run_metadata"]
    )

    # ---------------------------------------------------------
    # Step 6 : Generate report
    # ---------------------------------------------------------

    print("\nRNASeq Navigator Report")
    print("=" * 45)

    print(f"Accession        : {study['study_accession']}")
    print(f"Organism         : {study['scientific_name'] or 'Unknown'}")
    print(f"Study Type       : {study_type}")
    print(f"Confidence       : {confidence}%")
    print(f"Runs             : {study['sample_count']}")
    print(f"Platform         : {study['platform']}")
    print(f"Layout           : {study['layout']}")

    # ---------------------------------------------------------
    # Classification Evidence
    # ---------------------------------------------------------

    print("\nClassification Evidence")
    print("-" * 45)

    if evidence:
        for item in evidence:
            print(f"• {item}")
    else:
        print("No supporting evidence detected.")

    # ---------------------------------------------------------
    # Study Conditions
    # ---------------------------------------------------------

    print("\nStudy Conditions")
    print("-" * 45)

    if conditions:

        for condition, count in sorted(conditions.items()):
            print(f"{condition:<35}{count} run(s)")

    else:

        print("No experimental conditions detected.")

    # ---------------------------------------------------------
    # Experimental Design
    # ---------------------------------------------------------

    print("\nExperimental Design Assessment")
    print("-" * 45)

    if design:

        print(f"Conditions Detected : {len(design['conditions'])}")
        print(f"Largest Group       : {design['largest']} run(s)")
        print(f"Smallest Group      : {design['smallest']} run(s)")
        print(f"Design Quality      : {design['quality']}")

    else:

        print("No sequencing runs available.")

    # ---------------------------------------------------------
    # Workflow Recommendation
    # ---------------------------------------------------------

    print("\nRecommended Pipeline")
    print("-" * 45)

    print(f"Primary Tool   : {recommendation['aligner']}")
    print(f"Quantification : {recommendation['quantification']}")
    print(f"Analysis       : {recommendation['analysis']}")


@app.command()
def version():
    """
    Show software version.
    """

    print("RNASeq Navigator v0.8-dev")


if __name__ == "__main__":
    app()
