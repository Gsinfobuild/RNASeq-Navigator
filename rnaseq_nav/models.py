"""
RNASeq Navigator

Data Models

Version 0.9
"""

from dataclasses import dataclass


@dataclass
class Summary:

    accession: str
    organism: str
    platform: str
    layout: str
    runs: int


@dataclass
class Classification:

    study_type: str
    confidence: int
    evidence: list


@dataclass
class Design:

    conditions: dict
    largest: int
    smallest: int
    quality: str


@dataclass
class Recommendation:

    aligner: str
    quantification: str
    analysis: str


@dataclass
class AnalysisResult:

    summary: Summary
    classification: Classification
    conditions: dict
    design: Design | None
    recommendation: Recommendation
