import requests


def fetch_study_info(accession):
    """
    Retrieve study and run metadata from ENA.
    """

    # Study-level metadata
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

    # Run-level metadata
    run_url = (
        "https://www.ebi.ac.uk/ena/portal/api/search?"
        f"result=read_run&query=study_accession={accession}"
        "&fields=run_accession,sample_accession,sample_alias,experiment_title,instrument_platform,library_layout"
        "&format=json"
    )

    run_response = requests.get(run_url)

    if run_response.status_code != 200:
        return None

    run_data = run_response.json()

    # Debug output
    print("\nDEBUG OUTPUT")
    print("=" * 60)

    for row in run_data[:5]:
        print(row)

    print("=" * 60)

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
        "layout": layout,
        "run_metadata": run_data
    }
