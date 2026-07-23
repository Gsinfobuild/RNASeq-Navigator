"""
RNASeq Navigator

Validation Engine

Version 1.0

Performs reusable BioProject validation for
benchmark curation.
"""

from rnaseq_nav.analysis_engine import analyze_accession


def validate_bioproject(accession):
    """
    Validate a BioProject for benchmark inclusion.

    Parameters
    ----------
    accession : str
        BioProject accession.

    Returns
    -------
    dict
        Validation result.
    """

    analysis = analyze_accession(accession)

    if analysis is None:

        return {

            "status": "REJECTED",

            "score": 0,

            "max_score": 5,

            "checks": {},

            "analysis": None,

        }

    summary = analysis["summary"]

    classification = analysis["classification"]

    recommendation = analysis["recommendation"]

    checks = {

        "metadata": summary["runs"] > 0,

        "platform": summary["platform"] != "Unknown",

        "layout": summary["layout"] != "Unknown",

        "classification":
            classification["study_type"] != "Unknown",

        "pipeline":
            recommendation["aligner"] != "Unknown",

    }

    score = sum(checks.values())

    if score == 5:

        status = "READY FOR BENCHMARK"

    elif score >= 3:

        status = "REVIEW REQUIRED"

    else:

        status = "REJECTED"

    return {

        "status": status,

        "score": score,

        "max_score": 5,

        "checks": checks,

        "analysis": analysis,

    }
