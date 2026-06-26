"""
RNASeq Navigator
Metadata Retrieval Engine v2.0

Retrieves study and run metadata from ENA
and performs metadata normalization.
"""

import re
import requests


# --------------------------------------------------------
# NORMALIZER
# --------------------------------------------------------

def normalize_text(text):
    """
    Normalize free-text metadata.
    """

    if not text:
        return ""

    text = text.lower().strip()

    replacements = {
        "rna-sep": "rna-seq",
        "rna seq": "rna-seq",
        "rnaseq": "rna-seq",
        "srna seq": "srna-seq",
        "srnaseq": "srna-seq",
        "small rna sequencing": "small rna",
        "miglog": "midlog",
        "_": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text)

    return text


# --------------------------------------------------------
# METADATA RETRIEVAL
# --------------------------------------------------------

def fetch_study_info(accession):
    """
    Download metadata from ENA Portal API.
    """

    # -------------------------
    # Study metadata
    # -------------------------

    study_url = (
        "https://www.ebi.ac.uk/ena/portal/api/search?"
        f"result=study&query=study_accession={accession}"
        "&fields=study_accession,scientific_name"
        "&format=json"
    )

    response = requests.get(study_url)

    if response.status_code != 200:
        return None

    study_data = response.json()

    if len(study_data) == 0:
        return None

    # -------------------------
    # Run metadata
    # -------------------------

    run_url = (
        "https://www.ebi.ac.uk/ena/portal/api/search?"
        f"result=read_run&query=study_accession={accession}"
        "&fields="
        "run_accession,"
        "sample_accession,"
        "sample_alias,"
        "experiment_title,"
        "instrument_platform,"
        "instrument_model,"
        "library_layout,"
        "library_strategy,"
        "library_source,"
        "library_selection"
        "&format=json"
    )

    response = requests.get(run_url)

    if response.status_code != 200:
        return None

    run_data = response.json()

    # -------------------------
    # Normalize metadata
    # -------------------------

    for row in run_data:

        row["experiment_title"] = normalize_text(
            row.get("experiment_title", "")
        )

        row["sample_alias"] = normalize_text(
            row.get("sample_alias", "")
        )

        row["library_strategy"] = normalize_text(
            row.get("library_strategy", "Unknown")
        )

        row["library_source"] = normalize_text(
            row.get("library_source", "Unknown")
        )

        row["library_selection"] = normalize_text(
            row.get("library_selection", "Unknown")
        )

        row["instrument_model"] = row.get(
            "instrument_model",
            "Unknown"
        )

    # -------------------------
    # Summary
    # -------------------------

    sample_count = len(run_data)

    if sample_count > 0:

        platform = run_data[0].get(
            "instrument_platform",
            "Unknown"
        )

        layout = run_data[0].get(
            "library_layout",
            "Unknown"
        )

    else:

        platform = "Unknown"
        layout = "Unknown"

    return {

        "study_accession": study_data[0]["study_accession"],

        "scientific_name": normalize_text(
            study_data[0].get(
                "scientific_name",
                ""
            )
        ),

        "sample_count": sample_count,

        "platform": platform,

        "layout": layout,

        "run_metadata": run_data

    }
    print("\nFIRST RUN METADATA")
    print("=" * 70)

    if run_data:
       first = run_data[0]

    fields = [
        "run_accession",
        "experiment_title",
        "sample_alias",
        "library_strategy",
        "library_source",
        "library_selection",
        "library_layout",
        "instrument_platform",
        "instrument_model"
    ]

    for field in fields:
        print(f"{field:20}: {first.get(field, 'Missing')}")

    print("=" * 70)
