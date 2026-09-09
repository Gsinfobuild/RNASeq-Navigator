"""
RNASeq Navigator

Command-Line Interface (CLI)

Version: 1.0

Purpose
-------
Provides the public entry point for the RNASeq Navigator
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

__version__ = "1.0.0"

__all__ = [
    "main",
]
