"""
RNASeq Navigator

CLI Parser Test
"""

from rnaseq_nav.cli.parser import parse_args


def show(arguments):

    parsed = parse_args(arguments)

    print("=" * 60)
    print(arguments)
    print("=" * 60)

    print(parsed)
    print()


def main():

    show(
        [
            "inspect",
            "SRR17730393",
        ]
    )

    show(
        [
            "inspect",
            "ERR315346",
            "--json",
        ]
    )

    show(
        [
            "inspect",
            "DRR138920",
            "--validation",
        ]
    )


if __name__ == "__main__":
    main()
