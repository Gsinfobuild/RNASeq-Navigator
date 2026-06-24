def classify_study(study):
    """
    Classify study type from ENA metadata.
    """

    organism = study["scientific_name"].lower()

    titles = []

    for run in study["run_metadata"]:
        titles.append(
            run.get(
                "experiment_title",
                ""
            ).lower()
        )

    combined_text = " ".join(titles)

    if "metagenomic" in combined_text:
        return "Metagenomics"

    if "srna-seq" in combined_text:
        return "Small RNA-seq"

    if "rna-seq" in combined_text:
        return "Bulk RNA-seq"

    return "Unknown"
