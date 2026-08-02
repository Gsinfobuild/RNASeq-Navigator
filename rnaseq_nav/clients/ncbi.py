"""
NCBI metadata client.

This module communicates with the NCBI Entrez API to retrieve
metadata associated with RNA-seq accessions.

Current milestone (v0.2)
------------------------
✓ Connect to NCBI
✓ Search SRA accession
✓ Retrieve UID
✓ Retrieve ESummary record

Future milestones
-----------------
- Extract ExpXml
- Extract Runs
- Parse XML
- Populate Metadata dataclasses
- Cache metadata
"""

from Bio import Entrez


class NCBIClient:
    """
    Client for retrieving RNA-seq metadata from NCBI.
    """

    def __init__(self, email: str):
        """
        Initialize the NCBI client.

        Parameters
        ----------
        email : str
            Email address required by NCBI Entrez.
        """

        self.email = email
        Entrez.email = email

    def fetch(self, accession: str):
        """
        Retrieve the raw ESummary record for an accession.

        Parameters
        ----------
        accession : str
            SRA accession (SRR, SRX, SRP, PRJNA, etc.)

        Returns
        -------
        dict | None
            Raw NCBI ESummary record, or None if retrieval fails.
        """

        print("=" * 60)
        print("RNASeq Navigator - NCBI Client")
        print("=" * 60)

        print(f"Email      : {self.email}")
        print(f"Accession  : {accession}")
        print()

        try:

            # --------------------------------------------------
            # Step 1: Search accession
            # --------------------------------------------------

            print("Searching NCBI SRA...")

            search_handle = Entrez.esearch(
                db="sra",
                term=accession
            )

            search_record = Entrez.read(search_handle)
            search_handle.close()

            id_list = search_record.get("IdList", [])

            if not id_list:

                print("No matching accession found.")

                return None

            uid = id_list[0]

            print(f"UID        : {uid}")

            # --------------------------------------------------
            # Step 2: Retrieve summary
            # --------------------------------------------------

            print("Retrieving ESummary record...")

            summary_handle = Entrez.esummary(
                db="sra",
                id=uid,
                retmode="xml"
            )

            summary_record = Entrez.read(summary_handle)
            summary_handle.close()

            # ESummary returns a DocumentSummarySet-like structure.
            # We'll inspect it before parsing in the next milestone.

            print("ESummary successfully retrieved.")
            print()

            print("Top-level keys:")

            if isinstance(summary_record, dict):
                for key in summary_record.keys():
                    print(f"  - {key}")
            else:
                print(type(summary_record))

            return summary_record

        except Exception as error:

            print()
            print("Metadata retrieval failed.")
            print(f"Error: {error}")

            return None
