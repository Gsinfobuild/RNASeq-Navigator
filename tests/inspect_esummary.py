"""
RNASeq Navigator

ESummary Inspector

Purpose
-------
Inspect the raw ESummary record returned by NCBI before
implementing the XML parser.

This script is for development and debugging only.
"""

from pprint import pprint

from Bio import Entrez


EMAIL = "gshankar.bbaul@gmail.com"
ACCESSION = "SRR17730393"


def main():
    """
    Inspect the ESummary record.
    """

    Entrez.email = EMAIL

    print("=" * 80)
    print("RNASeq Navigator - ESummary Inspector")
    print("=" * 80)

    # ----------------------------------------------------------
    # Search accession
    # ----------------------------------------------------------

    print("\n[1] Searching accession...")

    search = Entrez.esearch(
        db="sra",
        term=ACCESSION
    )

    search_record = Entrez.read(search)
    search.close()

    ids = search_record["IdList"]

    if not ids:
        print("Accession not found.")
        return

    uid = ids[0]

    print(f"UID : {uid}")

    # ----------------------------------------------------------
    # Retrieve ESummary
    # ----------------------------------------------------------

    print("\n[2] Retrieving ESummary...")

    handle = Entrez.esummary(
        db="sra",
        id=uid,
        retmode="xml"
    )

    summary = Entrez.read(handle)
    handle.close()

    print("\nSummary object type:")
    print(type(summary))

    print("\nNumber of records:")
    print(len(summary))

    if len(summary) == 0:
        print("No records returned.")
        return

    record = summary[0]

    print("\nRecord type:")
    print(type(record))

    print("\nAvailable fields")
    print("-" * 80)

    for key in sorted(record.keys()):
        print(key)

    print("\n" + "=" * 80)
    print("FULL RECORD")
    print("=" * 80)

    pprint(record)

    print("\nInspection complete.")


if __name__ == "__main__":
    main()
