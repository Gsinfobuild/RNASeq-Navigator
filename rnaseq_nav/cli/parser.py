"""
RNASeq Scout

CLI Argument Parser

Version: 0.1.0

Purpose
-------
Defines the command-line interface for RNASeq Navigator.

This module is responsible only for parsing command-line
arguments. It does NOT execute commands.

Current Commands
----------------
inspect <ACCESSION>

Global Options
--------------
--version
--help
"""

from __future__ import annotations

import argparse


# ==========================================================
# Parser Factory
# ==========================================================

def create_parser() -> argparse.ArgumentParser:
    """
    Create and return the CLI argument parser.

    Returns
    -------
    argparse.ArgumentParser
    """

    parser = argparse.ArgumentParser(
        prog="rnaseq-nav",
        description=(
            "RNASeq Scout - Explore metadata associated "
            "with public sequencing datasets."
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version="RNASeq Scout 0.1.0",
    )

    # ------------------------------------------------------
    # Subcommands
    # ------------------------------------------------------

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="command",
        metavar="<command>",
    )

    # ======================================================
    # inspect
    # ======================================================

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Inspect a sequencing accession",
        description=(
            "Retrieve metadata and generate a report "
            "for a sequencing accession."
        ),
    )

    inspect_parser.add_argument(
        "accession",
        metavar="ACCESSION",
        help=(
            "Sequencing accession "
            "(e.g. SRR17730393, ERR315346, "
            "DRR138920, PRJNA799829)"
        ),
    )

    inspect_parser.add_argument(
        "--email",
        required=False,
        default=None,
        help=(
            "NCBI email address. "
            "If omitted, the configured default is used."
        ),
    )

    inspect_parser.add_argument(
        "--json",
        action="store_true",
        help="Output report as JSON.",
    )

    inspect_parser.add_argument(
        "--raw",
        action="store_true",
        help="Display raw metadata before normalization.",
    )

    inspect_parser.add_argument(
        "--validation",
        action="store_true",
        help="Display validation report.",
    )

    return parser


# ==========================================================
# Parse Arguments
# ==========================================================

def parse_args(args=None):
    """
    Parse command-line arguments.

    Parameters
    ----------
    args : list[str], optional

    Returns
    -------
    argparse.Namespace
    """

    parser = create_parser()

    return parser.parse_args(args)
