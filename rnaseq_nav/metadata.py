import requests

def fetch_study_info(accession):

    url = (
        "https://www.ebi.ac.uk/ena/portal/api/search?"
        f"result=study&query=study_accession={accession}"
        "&fields=study_accession,scientific_name,center_name"
        "&format=json"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if len(data) == 0:
        return None

    return data[0]
