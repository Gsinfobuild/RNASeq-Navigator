"""
RNASeq Navigator

Core Package

Version: 1.0

Purpose
-------
The core package defines the public data models and
contracts shared across the RNASeq Navigator framework.

Modules
-------
results
    Standard result objects returned by the public API.

Public Objects
--------------
InspectionResult
"""

from .results import InspectionResult

__version__ = "1.0.0"

__all__ = [
    "InspectionResult",
]
