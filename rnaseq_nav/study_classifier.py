"""
RNASeq Navigator
Study Classification Engine v4.0

Architecture

Metadata
    │
    ▼
Tokenizer
    │
    ▼
Evidence Collector
    │
    ▼
Hierarchical Rule Engine
    │
    ▼
Confidence Calculator
"""

import re


# ------------------------------------------------------------
# TOKENIZER
# ------------------------------------------------------------

def tokenize(text):
    """
    Convert metadata into normalized tokens.
    """

    if not text:
        return []

    text = text.lower()

    text = text.replace("_", " ")
    text = text.replace("-", " ")

    text = re.sub(r"[^\w\s]", " ", text)

    return text.split()


# ------------------------------------------------------------
# EVIDENCE COLLECTOR
# ------------------------------------------------------------

def collect_evidence(study):
    """
    Collect all searchable metadata into one token set.
    """

    tokens = []

    scientific_name = study.get(
        "scientific_name",
        ""
    )

    tokens.extend(
        tokenize(scientific_name)
    )

    for run in study.get(
        "run_metadata",
        []
    ):

        tokens.extend(
            tokenize(
                run.get(
                    "experiment_title",
                    ""
                )
            )
        )

        tokens.extend(
            tokenize(
                run.get(
                    "sample_alias",
                    ""
                )
            )
        )

    return set(tokens)


# ------------------------------------------------------------
# CONFIDENCE CALCULATOR
# ------------------------------------------------------------

def calculate_confidence(
    matched_rules,
    total_rules
):
    """
    Calculate confidence based on
    matched diagnostic rules.
    """

    if total_rules == 0:
        return 0

    confidence = int(
        matched_rules /
        total_rules *
        100
    )

    return max(
        50,
        min(
            confidence,
            100
        )
    )


# ------------------------------------------------------------
# CLASSIFIER
# ------------------------------------------------------------

def classify_study(study):

    tokens = collect_evidence(study)

    evidence = []

    # =========================================================
    # LEVEL 1
    # Metagenomics
    # =========================================================

    metagenomics_rules = [

        "metagenomic" in tokens,

        "metagenome" in tokens,

        "microbiome" in tokens

    ]

    matched = sum(metagenomics_rules)

    if matched > 0:

        evidence.append(
            "Metagenomic evidence detected"
        )

        return {

            "study_type": "Metagenomics",

            "confidence": calculate_confidence(
                matched,
                len(metagenomics_rules)
            ),

            "evidence": evidence

        }

    # =========================================================
    # LEVEL 2
    # Small RNA-seq
    # =========================================================

    small_rules = [

        "srna" in tokens,

        "mirna" in tokens,

        "pirna" in tokens,

        (
            "small" in tokens
            and "rna" in tokens
        )

    ]

    matched = sum(small_rules)

    if matched > 0:

        evidence.append(
            "Small RNA evidence detected"
        )

        return {

            "study_type": "Small RNA-seq",

            "confidence": calculate_confidence(
                matched,
                len(small_rules)
            ),

            "evidence": evidence

        }

    # =========================================================
    # LEVEL 3
    # Single-cell RNA-seq
    # =========================================================

    scrna_rules = [

        "single" in tokens
        and "cell" in tokens,

        "10x" in tokens,

        "smartseq" in tokens,

        "scrna" in tokens

    ]

    matched = sum(scrna_rules)

    if matched > 0:

        evidence.append(
            "Single-cell RNA evidence detected"
        )

        return {

            "study_type": "Single-cell RNA-seq",

            "confidence": calculate_confidence(
                matched,
                len(scrna_rules)
            ),

            "evidence": evidence

        }

    # =========================================================
    # LEVEL 4
    # ChIP-seq
    # =========================================================

    chip_rules = [

        "chip" in tokens,

        "chipseq" in tokens

    ]

    matched = sum(chip_rules)

    if matched > 0:

        evidence.append(
            "ChIP-seq evidence detected"
        )

        return {

            "study_type": "ChIP-seq",

            "confidence": calculate_confidence(
                matched,
                len(chip_rules)
            ),

            "evidence": evidence

        }

    # =========================================================
    # LEVEL 5
    # ATAC-seq
    # =========================================================

    atac_rules = [

        "atac" in tokens,

        "atacseq" in tokens

    ]

    matched = sum(atac_rules)

    if matched > 0:

        evidence.append(
            "ATAC-seq evidence detected"
        )

        return {

            "study_type": "ATAC-seq",

            "confidence": calculate_confidence(
                matched,
                len(atac_rules)
            ),

            "evidence": evidence

        }

    # =========================================================
    # LEVEL 6
    # Bulk RNA-seq
    # =========================================================

    bulk_rules = [

        (
            "rna" in tokens
            and "seq" in tokens
        ),

        "transcriptome" in tokens

    ]

    matched = sum(bulk_rules)

    if matched > 0:

        evidence.append(
            "Bulk RNA-seq evidence detected"
        )

        return {

            "study_type": "Bulk RNA-seq",

            "confidence": calculate_confidence(
                matched,
                len(bulk_rules)
            ),

            "evidence": evidence

        }

    # =========================================================
    # UNKNOWN
    # =========================================================

    return {

        "study_type": "Unknown",

        "confidence": 0,

        "evidence": []

    }
