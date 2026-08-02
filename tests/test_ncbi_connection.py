"""
Test connection to NCBI Entrez
"""

from Bio import Entrez

# Replace with your email
Entrez.email = "gshankar.bbau@gmail.com"

print("=" * 60)
print("Testing connection to NCBI Entrez")
print("=" * 60)

try:

    handle = Entrez.esearch(
        db="bioproject",
        term="PRJNA799829"
    )

    result = Entrez.read(handle)
    handle.close()

    print("\nConnection successful!\n")

    print(result)

except Exception as e:

    print("\nConnection failed!\n")

    print(e)
