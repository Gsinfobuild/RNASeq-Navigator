"""
Test new RNASeq Navigator accessions.

This script analyzes a list of RNA-seq accessions and prints
their classification results.
"""

from rnaseq_nav.analysis_engine import analyze_accession

ACCESSIONS = [
    "ERX16608090",
    "ERX16608085",
    "SRX34444857",
    "SRX34444842",
]

print("\nRNASeq Navigator - New Dataset Evaluation")
print("=" * 70)

for accession in ACCESSIONS:

    print(f"\nAnalyzing: {accession}")

    result = analyze_accession(accession)

    if result is None:
        print("❌ Metadata retrieval failed.")
        continue

    metadata = result["metadata"]
    classification = result["classification"]

    print(f"Study Type : {classification['study_type']}")
    print(f"Organism   : {metadata.get('organism', 'Unknown')}")
    print(f"Platform   : {metadata.get('platform', 'Unknown')}")
    print(f"Layout     : {metadata.get('layout', 'Unknown')}")
    print(f"Runs       : {metadata.get('runs', 'Unknown')}")

    if "pipeline" in result:
        print(f"Pipeline   : {result['pipeline']}")

print("\n" + "=" * 70)
print("Evaluation completed.")
