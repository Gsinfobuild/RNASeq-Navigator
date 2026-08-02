"""
RNASeq Navigator

XML Structure Inspector

Purpose
-------
Inspect the hierarchy of ExpXml.
"""

from Bio import Entrez
import xml.etree.ElementTree as ET

EMAIL = "gshankar.bbaul@gmail.com"
ACCESSION = "SRR17730393"


def print_tree(node, level=0):
    """Recursively print XML tree."""
    print("  " * level + f"- {node.tag}")

    for child in node:
        print_tree(child, level + 1)


def main():

    Entrez.email = EMAIL

    search = Entrez.esearch(
        db="sra",
        term=ACCESSION
    )

    uid = Entrez.read(search)["IdList"][0]
    search.close()

    summary = Entrez.esummary(
        db="sra",
        id=uid,
        retmode="xml"
    )

    record = Entrez.read(summary)[0]
    summary.close()

    root = ET.fromstring(f"<ROOT>{record['ExpXml']}</ROOT>")

    print("=" * 70)
    print("ROOT CHILDREN")
    print("=" * 70)

    for child in root:
        print(child.tag)

    print("\n")
    print("=" * 70)
    print("FULL XML TREE")
    print("=" * 70)

    print_tree(root)


if __name__ == "__main__":
    main()
