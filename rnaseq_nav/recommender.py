def recommend_pipeline(study_type):

    recommendation = {}

    if study_type == "Bulk RNA-seq":

        recommendation["aligner"] = "STAR"
        recommendation["quantification"] = "featureCounts"
        recommendation["analysis"] = "DESeq2"

    elif study_type == "Small RNA-seq":

        recommendation["aligner"] = "Bowtie"
        recommendation["quantification"] = "miRDeep2"
        recommendation["analysis"] = "DESeq2"

    elif study_type == "Metagenomics":

        recommendation["aligner"] = "Kraken2"
        recommendation["quantification"] = "Bracken"
        recommendation["analysis"] = "MetaPhlAn"

    else:

        recommendation["aligner"] = "Unknown"
        recommendation["quantification"] = "Unknown"
        recommendation["analysis"] = "Unknown"

    return recommendation
