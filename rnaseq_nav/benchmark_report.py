"""
RNASeq Navigator

Benchmark Report Generator

Version 0.9
"""


def generate_benchmark_report(result):
    """
    Generate a structured benchmark report dictionary
    from the analysis engine output.
    """

    if result is None:
        return None

    summary = result["summary"]
    classification = result["classification"]
    recommendation = result["recommendation"]
    design = result["design"]

    report = {
        "accession": summary["accession"],
        "organism": summary["organism"],
        "study_type": classification["study_type"],
        "confidence": classification["confidence"],
        "pipeline": recommendation["aligner"],
        "platform": summary["platform"],
        "layout": summary["layout"],
        "runs": summary["runs"],
        "design_quality": (
            design["quality"]
            if design
            else "Unavailable"
        ),
        "benchmark_status": "Candidate"
    }

    return report
