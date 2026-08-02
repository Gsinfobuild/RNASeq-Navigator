"""
RNASeq Navigator

Regression Dataset Verifier

Purpose
-------
Verify that every accession in the regression
benchmark matches its intended category.
"""

from Bio import Entrez

from rnaseq_nav.parsers.sra_parser import SRAParser
from tests.regression.regression_datasets import REGRESSION_DATASETS


EMAIL = "gshankar.bbaul@gmail.com"


def retrieve_record(accession):
    """Retrieve an SRA ESummary record."""

    search = Entrez.esearch(
        db="sra",
        term=accession
    )

    search_record = Entrez.read(search)
    search.close()

    ids = search_record["IdList"]

    if not ids:
        return None

    uid = ids[0]

    summary = Entrez.esummary(
        db="sra",
        id=uid,
        retmode="xml"
    )

    record = Entrez.read(summary)[0]
    summary.close()

    return record


def expected_category(metadata):
    """
    Infer the dataset category from metadata.
    """

    organism = metadata.sample.organism.lower()
    strategy = metadata.experiment.library_strategy.upper()
    layout = metadata.experiment.layout.upper()

    # Organism

    if "tuberculosis" in organism or "escherichia" in organism \
       or "bacillus" in organism:
        organism_group = "Bacterial"

    elif "homo sapiens" in organism:
        organism_group = "Human"

    elif "mus musculus" in organism:
        organism_group = "Mouse"

    elif "arabidopsis" in organism \
         or "oryza" in organism \
         or "zea" in organism:
        organism_group = "Plant"

    else:
        organism_group = "Other"

    return organism_group, strategy, layout


def main():

    Entrez.email = EMAIL

    parser = SRAParser()

    print("=" * 90)
    print("RNASeq Navigator Dataset Catalog Verification")
    print("=" * 90)

    mismatches = 0

    total = 0

    for category, accessions in REGRESSION_DATASETS.items():

        print()
        print("=" * 90)
        print(category)
        print("=" * 90)

        for accession in accessions:

            total += 1

            print()

            print(f"Checking {accession}")

            try:

                record = retrieve_record(accession)

                if record is None:

                    print("❌ Not found")

                    mismatches += 1

                    continue

                metadata = parser.parse(
                    record["ExpXml"],
                    record["Runs"]
                )

                organism_group, strategy, layout = expected_category(metadata)

                print(f"Organism : {metadata.sample.organism}")
                print(f"Strategy : {strategy}")
                print(f"Layout   : {layout}")

                warning = False

                # -----------------------------
                # Organism check
                # -----------------------------

                if "Human" in category and organism_group != "Human":
                    warning = True

                if "Mouse" in category and organism_group != "Mouse":
                    warning = True

                if "Plant" in category and organism_group != "Plant":
                    warning = True

                if "Bacterial" in category and organism_group != "Bacterial":
                    warning = True

                # -----------------------------
                # Layout check
                # -----------------------------

                if "Single-End" in category and layout != "SINGLE":
                    warning = True

                if "Paired-End" in category and layout != "PAIRED":
                    warning = True

                # -----------------------------
                # Strategy check
                # -----------------------------

                if "Small RNA" in category:

                    if "RNA" not in strategy:
                        warning = True

                if warning:

                    print("⚠ CATEGORY MISMATCH")

                    mismatches += 1

                else:

                    print("✅ VERIFIED")

            except Exception as e:

                print("❌ ERROR")

                print(e)

                mismatches += 1

    print()
    print("=" * 90)
    print("Verification Summary")
    print("=" * 90)

    print(f"Datasets checked : {total}")

    print(f"Mismatches       : {mismatches}")

    print(f"Verified         : {total - mismatches}")

    accuracy = ((total - mismatches) / total) * 100

    print(f"Catalog Accuracy : {accuracy:.1f}%")

    if mismatches == 0:

        print()

        print("🎉 Dataset catalog verified successfully.")


if __name__ == "__main__":
    main()
