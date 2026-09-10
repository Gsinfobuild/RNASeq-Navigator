"""
RNASeq Scout
================

A metadata intelligence and exploration platform for
public sequencing datasets.

RNASeq Navigator provides a unified interface for
retrieving, validating, normalizing, enriching, and
reporting metadata associated with public sequencing
accessions (SRA, ENA, DDBJ, BioProject, BioSample, etc.).

Public API
----------
Example
-------

from rnaseq_nav import RNASeqNavigator

navigator = RNASeqNavigator(
    email="your_email@example.com"
)

report = navigator.inspect("SRR17730393")

Version
-------
0.1.0
"""

from .navigator import RNASeqNavigator

__version__ = "0.1.0"

__author__ = "RNASeq Scout Project"

__all__ = [
    "RNASeqNavigator",
]
