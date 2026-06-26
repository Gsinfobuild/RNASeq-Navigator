"""
RNASeq Navigator

Core Analysis Engine

Version 0.9
"""

from .metadata import fetch_study_info
from .study_classifier import classify_study
from .design_detector import detect_conditions
from .design_assessor import assess_design
from .recommender import recommend_pipeline


def analyze_accession(accession):
    """
    Analyze a BioProject accession and return a structured result.
    """

    # ---------------------------------------------------------
    # Step 1 : Retrieve metadata
    # ---------------------------------------------------------

    study = fetch_study_info(accession)

    if study is None:
        return None

    # ---------------------------------------------------------
    # Step 2 : Classify study
    # ---------------------------------------------------------

    classification = classify_study(study)

    # ---------------------------------------------------------
    # Step 3 : Detect experimental conditions
    # ---------------------------------------------------------

    conditions = detect_conditions(
        study["run_metadata"]
    )

    # ---------------------------------------------------------
    # Step 4 : Assess experimental design
    # ---------------------------------------------------------

    design = assess_design(
        study["run_metadata"]
    )

    # ---------------------------------------------------------
    # Step 5 : Recommend analysis workflow
    # ---------------------------------------------------------

    recommendation = recommend_pipeline(
        classification["study_type"]
    )

    # ---------------------------------------------------------
    # Step 6 : Return structured result
    # ---------------------------------------------------------

    summary = {

        "accession": study["study_accession"],

        "organism": study["scientific_name"],

        "runs": study["sample_count"],

        "platform": study["platform"],

        "layout": study["layout"]

    }

    return {

        "summary": summary,

        "classification": classification,

        "conditions": conditions,

        "design": design,

        "recommendation": recommendation,

    }
