# RNASeq Navigator Benchmark Plan

**Project Goal**

Develop a scientifically curated benchmark dataset consisting of **100 manually validated BioProjects** to evaluate RNASeq Navigator classification accuracy and pipeline recommendation performance.

---

## Benchmark Progress

| Study Type | Target | Validated | Status |
|------------|-------:|----------:|--------|
| Bulk RNA-seq | 20 | 1 | 🟡 In Progress |
| Small RNA-seq | 10 | 1 | 🟡 In Progress |
| Single-cell RNA-seq | 10 | 0 | ⚪ Not Started |
| Metagenomics | 10 | 1 | 🟡 In Progress |
| ChIP-seq | 10 | 0 | ⚪ Not Started |
| ATAC-seq | 10 | 0 | ⚪ Not Started |
| Long-read RNA-seq | 10 | 0 | ⚪ Not Started |
| Unsupported / Unknown | 10 | 1 | 🟡 In Progress |
| Poor Metadata / Edge Cases | 10 | 0 | ⚪ Not Started |

---

## Overall Progress

**Validated Projects:** **4 / 100**

Current Completion:

```text
████□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□ 4%
```

---

## Benchmark Objectives

- Validate study type classification accuracy.
- Validate workflow recommendations.
- Evaluate metadata normalization.
- Test edge cases and incomplete metadata.
- Prevent regressions after future code updates.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ⚪ | Not Started |
| 🟡 | In Progress |
| 🟢 | Completed |

---

## Notes

This benchmark is manually curated.

Each BioProject is independently verified before inclusion.

Only validated public BioProjects are added to the benchmark.
