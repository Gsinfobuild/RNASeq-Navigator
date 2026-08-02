"""
Retrieve BioProject summary from NCBI.

This test performs:

BioProject Accession
        ↓
ESearch
        ↓
UID
        ↓
ESummary
        ↓
Print available metadata
"""

from pprint import pprint
from Bio import Entrez

# Replace with your email
Entrez.email = "gshankar.bbau@gmail.com"

ACCESSION = "PRJNA799829"

print("=" * 70)
print("Retrieving BioProject Summary")
print("=" * 70)

# ----------------------------------------------------------
# Step 1: Find UID
# ----------------------------------------------------------

search = Entrez.esearch(
    db="bioproject",
    term=ACCESSION
)

search_result = Entrez.read(search)
search.close()

uid = search_result["IdList"][0]

print(f"\nBioProject UID: {uid}")

# ----------------------------------------------------------
# Step 2: Retrieve Summary
# ----------------------------------------------------------

summary = Entrez.esummary(
    db="bioproject",
    id=uid
)

summary_result = Entrez.read(summary)
summary.close()

print("\nReturned object type:")
print(type(summary_result))

print("\nFull summary:\n")

pprint(summary_result)
