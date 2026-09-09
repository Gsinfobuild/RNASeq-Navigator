# RNASeq Navigator

RNASeq Navigator is a computational framework for discovering, inspecting, normalizing, validating, classifying, and interpreting sequencing datasets available through the NCBI Sequence Read Archive (SRA) and related NCBI resources.

The project is designed to make public sequencing dataset exploration easier for researchers who want to understand the characteristics and potential usefulness of a dataset before beginning downstream analysis.

---

## What RNASeq Navigator Does

RNASeq Navigator accepts SRA-related accession identifiers and retrieves available metadata from NCBI resources.

The retrieved information is processed through a structured workflow:

```text
SRA / NCBI accession
        │
        ▼
Metadata Discovery
        │
        ▼
Metadata Normalization
        │
        ▼
Metadata Validation
        │
        ▼
Dataset Classification
        │
        ▼
Dataset Interpretation
        │
        ▼
Structured Dataset Report
        │
        ├── JSON export
        │
        └── PDF export
