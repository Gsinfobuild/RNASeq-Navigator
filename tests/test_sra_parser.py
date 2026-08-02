"""
RNASeq Navigator

Metadata Object Test
"""

from Bio import Entrez

from rnaseq_nav.parsers.sra_parser import SRAParser


EMAIL = "gshankar.bbaul@gmail.com"
ACCESSION = "SRR17730393"


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

    metadata = SRAParser().parse(
        record["ExpXml"],
        record["Runs"]
    )

    print("=" * 70)
    print("RNASeq Navigator Metadata Object")
    print("=" * 70)

    print(f"Project     : {metadata.project.accession}")
    print(f"Study       : {metadata.study.accession}")

    print(f"Experiment  : {metadata.experiment.accession}")
    print(f"Strategy    : {metadata.experiment.library_strategy}")
    print(f"Layout      : {metadata.experiment.layout}")
    print(f"Platform    : {metadata.experiment.platform}")
    print(f"Instrument  : {metadata.experiment.instrument}")

    print(f"Run         : {metadata.run.accession}")
    print(f"Spots       : {metadata.run.total_spots}")
    print(f"Bases       : {metadata.run.total_bases}")

    print(f"Sample      : {metadata.sample.accession}")
    print(f"BioSample   : {metadata.sample.biosample}")
    print(f"Organism    : {metadata.sample.organism}")


if __name__ == "__main__":
    main()
