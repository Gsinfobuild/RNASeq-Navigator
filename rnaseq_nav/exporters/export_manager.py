"""
RNASeq Navigator

Export Manager

Version 1.0
"""

from rnaseq_nav.exporters.json_exporter import export_json


SUPPORTED_EXPORTS = {
    "json": export_json,
}


def export_result(result, output_format):
    """
    Export an analysis result using the requested exporter.

    Parameters
    ----------
    result : dict
        Analysis result.

    output_format : str
        Requested output format.

    Returns
    -------
    str
        Exported report.
    """

    output_format = output_format.lower()

    if output_format not in SUPPORTED_EXPORTS:

        raise ValueError(
            f"Unsupported output format: {output_format}"
        )

    exporter = SUPPORTED_EXPORTS[output_format]

    return exporter(result)
