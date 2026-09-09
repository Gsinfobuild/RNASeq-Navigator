"""
RNASeq Navigator

Public API definitions.

Any change to these signatures
requires a major version bump.
"""

DATASET_DISCOVERY_API = {

    "fetch": [

        "accession",

    ],

    "search": [

        "organism",

        "strategy",

        "layout",

        "platform",

        "source",

        "selection",

        "max_results",

        "diversity",

    ],

}
