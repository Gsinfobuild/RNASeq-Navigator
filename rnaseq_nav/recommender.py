def recommend_pipeline(organism, layout):

    organism = organism.lower()

    recommendation = {}

    # Bacteria
    if "tuberculosis" in organism:
        recommendation["aligner"] = "HISAT2"
        recommendation["quantification"] = "featureCounts"
        recommendation["de"] = "DESeq2"

    # Human
    elif "homo sapiens" in organism:
        recommendation["aligner"] = "STAR"
        recommendation["quantification"] = "featureCounts"
        recommendation["de"] = "DESeq2"

    # Mouse
    elif "mus musculus" in organism:
        recommendation["aligner"] = "STAR"
        recommendation["quantification"] = "featureCounts"
        recommendation["de"] = "DESeq2"

    else:
        recommendation["aligner"] = "HISAT2"
        recommendation["quantification"] = "featureCounts"
        recommendation["de"] = "DESeq2"

    return recommendation
