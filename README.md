# RNASeq Scout

**RNASeq Scout** is an open-source RNA-seq experiment intelligence engine for inspecting and interpreting public sequencing datasets from the NCBI Sequence Read Archive (SRA) and related NCBI resources.

## Overview

RNASeq Scout is designed to move beyond simple sequencing-metadata retrieval. It examines a public sequencing accession and converts available metadata into a structured interpretation of the experiment, its sequencing modality, experimental design, dataset suitability, and a provisional analysis plan.

The project is intended for researchers who want to assess a public sequencing dataset before investing time in downloading and processing the underlying reads.

### What RNASeq Scout provides

- Metadata retrieval and normalization
- Metadata quality assessment
- Biological and experimental context interpretation
- Sequencing modality and workflow classification
- Experimental design interpretation
- Dataset suitability assessment for RNA-seq analysis
- Context-aware analysis planning
- Structured inspection results for GUI, PDF, and JSON presentation

RNASeq Scout does not replace domain expertise or downstream RNA-seq analysis pipelines. Its purpose is to provide an evidence-based starting point for understanding a dataset.


## Architecture

RNASeq Scout follows a layered inspection pipeline:

```text
SRA Accession
     |
     v
Metadata Retrieval
     |
     v
Normalization
     |
     v
Validation
     |
     v
Metadata Intelligence
     |
     v
Modality / Workflow Intelligence
     |
     v
Experimental Design Intelligence
     |
     v
Dataset Suitability
     |
     v
Analysis Planning
     |
     v
InspectionResult
     |
     +---------> Streamlit GUI
     |
     +---------> PDF Report
     |
     +---------> Structured Output
```

## Scientific Design Principles

RNASeq Scout is built around several principles intended to keep automated interpretation scientifically conservative and transparent.

### Evidence before inference

The system distinguishes information directly supported by metadata from information inferred from metadata patterns. Inferences are not presented as experimentally confirmed facts.

### Modality before workflow

RNA-seq-specific analysis recommendations are generated only after the sequencing modality has been assessed. Explicit evidence for incompatible sequencing workflows takes precedence over generic metadata completeness.

### No unsupported biological replicates

The presence of multiple sequencing runs does not by itself establish biological replication. Replicate interpretation requires supporting experimental metadata.

### Conservative interpretation of incomplete metadata

When essential information is unavailable, RNASeq Scout reports uncertainty or missing information rather than inventing experimental details.

### Context-aware analysis planning

Analysis recommendations are linked to the interpreted sequencing modality and experimental context rather than being applied as a universal pipeline.

## Supported Scope

RNASeq Scout v0.1.0 is primarily designed for inspection of public sequencing experiments represented through NCBI SRA metadata.

The current implementation is particularly focused on:

- Public NCBI SRA accessions
- RNA-seq experiment interpretation
- Sequencing modality classification
- Experimental design interpretation from available metadata
- Dataset suitability assessment for RNA-seq analysis
- Provisional planning of downstream RNA-seq workflows

The system can also recognize several non-RNA sequencing modalities so that they are not incorrectly passed to an RNA-seq workflow.

## What RNASeq Scout Does Not Do

RNASeq Scout does not:

- Download and process sequencing reads as part of the inspection workflow
- Replace FastQC, trimming, alignment, quantification, or differential-expression software
- Establish biological replication when replication is not supported by metadata
- Infer experimental details as established facts when they are not documented
- Guarantee that a dataset will be suitable for a particular biological question
- Perform statistical differential-expression analysis itself

Analysis recommendations should therefore be treated as a starting point for researcher review rather than as an automatically validated experimental protocol.

## Web Application

RNASeq Scout includes a Streamlit-based web interface for interactive dataset inspection.

Launch the application from the project directory with:

```bash
venv/bin/python -m streamlit run rnaseq_nav/ui/app.py
```

The web application presents the inspection results as a structured workflow, including metadata intelligence, modality and workflow classification, experimental design, dataset suitability, analysis planning, metadata quality, and dataset reporting.

## Python API

The canonical programmatic interface is the `RNASeqNavigator` class.

A basic inspection can be performed with:

```python
from rnaseq_nav.navigator import RNASeqNavigator

navigator = RNASeqNavigator(email="your_email@example.com")
result = navigator.inspect("SRR17730393")

print(result)
```

The `inspect()` method is the canonical end-to-end inspection workflow. It retrieves, normalizes, validates, interprets, and analyzes the available metadata before returning an `InspectionResult`.

## Validation

RNASeq Scout includes deterministic tests for the intelligence layers and end-to-end regression cases through the canonical `RNASeqNavigator.inspect()` API.

Run the test suite with:

```bash
venv/bin/python -m pytest -q
```

The v0.1.0 regression suite verifies, among other behaviors:

- Explicit RNA-seq experiments are classified as RNA-seq compatible
- Amplicon sequencing is not passed to an RNA-seq workflow
- Unknown sequencing strategies remain compatibility-uncertain
- Specialized RNA sequencing is not automatically treated as conventional bulk RNA-seq
- Biological replicates are not assumed from sequencing runs alone
- Missing controls are not invented
- Modality classification propagates into dataset suitability and analysis planning

### Example regression cases

A known RNA-seq dataset (`SRR17730393`) passes through the complete inspection pipeline and receives an RNA-seq analysis plan.

An amplicon sequencing dataset (`SRX35157977`) is classified as incompatible with RNA-seq analysis. The suitability layer reports `Not suitable for RNA-seq analysis`, and the analysis planner does not recommend RNA-seq-specific tools.

These regression cases are intended to protect the architectural boundary between general sequencing metadata interpretation and RNA-seq-specific analysis planning.

## Data Sources and Attribution

RNASeq Scout retrieves public sequencing metadata from resources provided by the National Center for Biotechnology Information (NCBI), including the Sequence Read Archive (SRA).

RNASeq Scout is an independent open-source software project and is not affiliated with, endorsed by, or maintained by NCBI.

The underlying sequencing datasets remain subject to their respective data-access conditions, metadata records, and attribution requirements. RNASeq Scout does not claim ownership of the underlying NCBI datasets.

## Citation

If you use RNASeq Scout in research, please cite the software using the information provided in `CITATION.cff`.

The current software release is version `0.1.0`.

## License

RNASeq Scout is released under the MIT License. See [`LICENSE`](LICENSE) for the complete license text.

## Ownership and Attribution

The RNASeq Scout software code is solely owned by Dr. Gauri Shankar.

Development and project attribution are documented within the repository. The graphical interface credits Dr. Gauri Shankar and Dr. Ranjana Soni as developers.

## Project Status

RNASeq Scout v0.1.0 represents the initial public release of the experiment intelligence architecture.

The v0.1.0 release establishes the core inspection pipeline and its separation into metadata intelligence, modality and workflow intelligence, experimental design intelligence, dataset suitability, and analysis planning.

Future development may extend modality coverage, improve metadata interpretation, expand experimental-design inference, and integrate additional analysis-planning capabilities while preserving the conservative evidence-based design principles of the current architecture.

**RNASeq Scout**

*From SRA accession to experiment-aware analysis plan.*
