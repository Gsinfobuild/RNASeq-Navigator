"""
RNASeq Scout

Command-Line Interface (CLI)

Version: 0.1.0

Purpose
-------
Provides the public entry point for the RNASeq Scout
command-line interface.

The CLI is responsible only for:

    • Parsing command-line arguments
    • Dispatching commands
    • Calling the RNASeqNavigator public API
    • Formatting output

All metadata retrieval, normalization, validation,
and reporting are handled by the backend library.

Examples
--------
Run from the source tree:

    python -m rnaseq_nav inspect SRR17730393

After installation:

    rnaseq-nav inspect SRR17730393
"""

from .main import main

__version__ = "0.1.0"

__all__ = [
    "main",
]
