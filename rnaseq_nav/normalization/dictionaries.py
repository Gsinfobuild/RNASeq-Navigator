"""
RNASeq Navigator

Metadata Normalization Dictionaries

Version 1.0

Defines canonical metadata values used throughout
RNASeq Navigator.
"""

# ==========================================================
# Helper
# ==========================================================

def canonical_key(value):
    """
    Convert arbitrary metadata strings into a
    normalized dictionary lookup key.
    """

    if value is None:
        return ""

    value = value.strip()

    value = value.replace("-", "_")

    value = value.replace(" ", "_")

    value = value.upper()

    return value


# ==========================================================
# Library Strategy
# ==========================================================

LIBRARY_STRATEGY = {

    canonical_key("RNA-Seq"): "RNA_SEQ",

    canonical_key("mRNA-Seq"): "MRNA_SEQ",

    canonical_key("ncRNA-Seq"): "NCRNA_SEQ",

    canonical_key("miRNA-Seq"): "MIRNA_SEQ",

    canonical_key("smRNA-Seq"): "SMRNA_SEQ",

    canonical_key("AMPLICON"): "AMPLICON",

    canonical_key("RAD-Seq"): "RAD_SEQ",

    canonical_key("WGS"): "WGS",

    canonical_key("WXS"): "WXS",

    canonical_key("ATAC-Seq"): "ATAC_SEQ",

    canonical_key("ChIP-Seq"): "CHIP_SEQ",

}


# ==========================================================
# Library Layout
# ==========================================================

LIBRARY_LAYOUT = {

    canonical_key("PAIRED"): "PAIRED",

    canonical_key("paired"): "PAIRED",

    canonical_key("SINGLE"): "SINGLE",

    canonical_key("single"): "SINGLE",

}


# ==========================================================
# Library Source
# ==========================================================

LIBRARY_SOURCE = {

    canonical_key("TRANSCRIPTOMIC"): "TRANSCRIPTOMIC",

    canonical_key("GENOMIC"): "GENOMIC",

    canonical_key("METAGENOMIC"): "METAGENOMIC",

    canonical_key("METATRANSCRIPTOMIC"): "METATRANSCRIPTOMIC",

}


# ==========================================================
# Platform
# ==========================================================

PLATFORM = {

    canonical_key("ILLUMINA"): "ILLUMINA",

    canonical_key("ION_TORRENT"): "ION_TORRENT",

    canonical_key("PACBIO_SMRT"): "PACBIO_SMRT",

    canonical_key("OXFORD_NANOPORE"): "OXFORD_NANOPORE",

    canonical_key("BGISEQ"): "BGISEQ",

}


# ==========================================================
# Library Selection
# ==========================================================

LIBRARY_SELECTION = {

    canonical_key("PolyA"): "POLYA",

    canonical_key("polyA"): "POLYA",

    canonical_key("Poly-A"): "POLYA",

    canonical_key("PCR"): "PCR",

    canonical_key("RANDOM"): "RANDOM",

    canonical_key("cDNA"): "CDNA",

    canonical_key("other"): "OTHER",

}
