"""
RNASeq Navigator
Metadata Retrieval Engine v2.1

Retrieves study and run metadata from the ENA Portal API
and performs metadata normalization.
"""

import re
import requests
from requests.exceptions import RequestException


# ==========================================================
# Text Normalization
# ==========================================================

def normalize_text(text: str) -> str:
    """
    Normalize free-text metadata for downstream analysis.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
        Normalized text.
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


# ==========================================================
# Metadata Retrieval
# ==========================================================

def fetch_study_info(accession: str):
    """
    Retrieve study and run metadata from the ENA Portal API.

    Parameters
    ----------
    accession : str
        BioProject accession.

    Returns
    -------
    dict | None
        Normalized study metadata or None if retrieval fails.
    """

    study_url = (
        "https://www.ebi.ac.uk/ena/portal/api/search?"
        f"result=study&query=study_accession={accession}"
        "&fields=study_accession,scientific_name"
        "&format=json"
    )

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

    try:

        study_response = requests.get(study_url, timeout=30)
        study_response.raise_for_status()

        study_data = study_response.json()

        if not study_data:
            return None

        run_response = requests.get(run_url, timeout=30)
        run_response.raise_for_status()

        run_data = run_response.json()

    except RequestException:

        return None

    # ------------------------------------------------------
    # Normalize run metadata
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Study summary
    # ------------------------------------------------------

    sample_count = len(run_data)

    if sample_count:

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
        "run_metadata": run_data,
    }
