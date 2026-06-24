import requests


def fetch_study_info(accession):

    # Study metadata
    study_url = (
        "https://www.ebi.ac.uk/ena/portal/api/search?"
        f"result=study&query=study_accession={accession}"
        "&fields=study_accession,scientific_name"
        "&format=json"
    )

    study_response = requests.get(study_url)

    if study_response.status_code != 200:
        return None

    study_data = study_response.json()

    if len(study_data) == 0:
        return None

    # Run metadata
    run_url = (
        "https://www.ebi.ac.uk/ena/portal/api/search?"
        f"result=read_run&query=study_accession={accession}"
        "&fields=run_accession,instrument_platform,library_layout"
        "&format=json"
    )

    run_response = requests.get(run_url)

    if run_response.status_code != 200:
        return None

    run_data = run_response.json()

    sample_count = len(run_data)

    platform = "Unknown"
    layout = "Unknown"

    if sample_count > 0:
        platform = run_data[0].get(
            "instrument_platform",
            "Unknown"
        )

        layout = run_data[0].get(
            "library_layout",
            "Unknown"
        )

    return {
        "study_accession": study_data[0]["study_accession"],
        "scientific_name": study_data[0]["scientific_name"],
        "sample_count": sample_count,
        "platform": platform,
        "layout": layout
    }
