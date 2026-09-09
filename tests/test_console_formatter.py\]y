from rnaseq_nav.intelligence.report import (
    DatasetReport,
)

from rnaseq_nav.formatters import (
    ConsoleFormatter,
)


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

    formatter = ConsoleFormatter()

    print(

        formatter.render(
            report
        )

    )


if __name__ == "__main__":

    main()
