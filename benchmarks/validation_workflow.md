# RNASeq Navigator Benchmark Validation Workflow

## Objective

Every BioProject included in the benchmark must pass the same validation workflow.

---

## Step 1 — Candidate Selection

Choose a public BioProject.

Record:

- BioProject accession
- Organism
- Study description

---

## Step 2 — Metadata Verification

Verify:

- Sequencing strategy
- Platform
- Library layout
- Organism

---

## Step 3 — RNASeq Navigator Analysis

Run:

python -m rnaseq_nav.cli analyze <BioProject>

Record:

- Predicted study type
- Confidence
- Recommended workflow

---

## Step 4 — Manual Comparison

Compare Navigator output with public metadata.

Record:

- Correct
- Incorrect
- Notes

---

## Step 5 — Benchmark Entry

If validated:

- Add to benchmark_projects.csv

- Update benchmark_plan.md

- Update the appropriate category file

---

## Validation Status

Possible values:

- Candidate
- Under Review
- Validated
- Rejected
