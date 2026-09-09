from rnaseq_nav.intelligence.report import DatasetReport


def main():

    report = DatasetReport(
        accession="SRR17730393"
    )

    report.identity.add(
        "Run",
        "SRR17730393",
    )

    report.identity.add(
        "Study",
        "SRP356545",
    )

    report.sequencing.add(
        "Platform",
        "ILLUMINA",
    )

    report.sequencing.add(
        "Layout",
        "PAIRED",
    )

    print("=" * 70)
    print("Dataset Report Model")
    print("=" * 70)

    print()

    print(report.to_dict())


if __name__ == "__main__":

    main()
