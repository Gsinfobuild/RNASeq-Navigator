"""
RNASeq Navigator

Public API Regression Test
"""

import inspect

from rnaseq_nav.discovery.dataset_discovery import DatasetDiscovery

EXPECTED = [

    "self",

    "organism",

    "strategy",

    "layout",

    "platform",

    "source",

    "selection",

    "max_results",

    "diversity",

]


def main():

    print("=" * 70)
    print("RNASeq Navigator Public API Test")
    print("=" * 70)

    params = list(

        inspect.signature(

            DatasetDiscovery.search

        ).parameters

    )

    print()

    print("Current API")

    print(params)

    print()

    if params == EXPECTED:

        print("✓ API STABLE")

    else:

        print("✗ API CHANGED")

        print()

        print("Expected")

        print(EXPECTED)


if __name__ == "__main__":

    main()
