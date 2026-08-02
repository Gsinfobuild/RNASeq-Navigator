#!/usr/bin/env python3
"""
RNASeq Navigator
Diagnostic script for SRA RunInfo retrieval

This script:
1. Searches a BioProject
2. Finds linked SRA record
3. Downloads RunInfo CSV
4. Saves the raw response
5. Displays CSV structure
"""

from Bio import Entrez
import requests
import csv
import io
from pprint import pprint

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

Entrez.email = "YOUR_EMAIL@example.com"   # <-- Replace with your email
BIOPROJECT = "PRJNA799829"

print("=" * 80)
print("RNASeq Navigator - SRA RunInfo Diagnostic")
print("=" * 80)

# -----------------------------------------------------
# Step 1 - BioProject search
# -----------------------------------------------------

print("\n[1] Searching BioProject...")

handle = Entrez.esearch(
    db="bioproject",
    term=BIOPROJECT
)

result = Entrez.read(handle)
handle.close()

if not result["IdList"]:
    raise RuntimeError("BioProject not found.")

bioproject_uid = result["IdList"][0]

print(f"BioProject UID : {bioproject_uid}")

# -----------------------------------------------------
# Step 2 - Link to SRA
# -----------------------------------------------------

print("\n[2] Finding linked SRA record...")

handle = Entrez.elink(
    dbfrom="bioproject",
    db="sra",
    id=bioproject_uid
)

links = Entrez.read(handle)
handle.close()

linksets = links[0]["LinkSetDb"]

if not linksets:
    raise RuntimeError("No SRA links found.")

sra_uid = linksets[0]["Link"][0]["Id"]

print(f"SRA UID : {sra_uid}")

# -----------------------------------------------------
# Step 3 - Download RunInfo
# -----------------------------------------------------

print("\n[3] Downloading RunInfo...")

url = (
    "https://trace.ncbi.nlm.nih.gov/Traces/sra/"
    f"?runinfo={sra_uid}"
)

print("URL:")
print(url)

response = requests.get(url, timeout=60)

print("\nHTTP Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))

# -----------------------------------------------------
# Save raw response
# -----------------------------------------------------

outfile = "runinfo_raw_response.txt"

with open(outfile, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"\nRaw response saved to: {outfile}")

print("\nFirst 500 characters:\n")
print("-" * 80)
print(response.text[:500])
print("-" * 80)

# -----------------------------------------------------
# Parse CSV
# -----------------------------------------------------

print("\n[4] Parsing CSV...")

reader = csv.DictReader(io.StringIO(response.text))

rows = list(reader)

print(f"Rows parsed: {len(rows)}")

if not rows:
    print("\nNo rows parsed.")
    raise SystemExit

print("\nCSV Columns\n")
print("=" * 80)

for col in rows[0].keys():
    print(col)

print("\nFirst Row\n")
print("=" * 80)

pprint(rows[0])

print("\nDiagnostic complete.")
