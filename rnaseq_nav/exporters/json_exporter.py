"""
RNASeq Navigator

JSON Exporter

Version 1.0
"""

import json


def export_json(result, indent=4):
    """
    Convert analysis result into formatted JSON.

    Parameters
    ----------
    result : dict
        Analysis result returned by analysis_engine.

    indent : int
        JSON indentation.

    Returns
    -------
    str
        JSON formatted string.
    """

    return json.dumps(
        result,
        indent=indent,
        ensure_ascii=False
    )
