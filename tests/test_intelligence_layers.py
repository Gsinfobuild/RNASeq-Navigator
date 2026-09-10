from types import SimpleNamespace

from rnaseq_nav.intelligence.modality_intelligence import (
    generate_modality_insight,
)
from rnaseq_nav.intelligence.design_intelligence import (
    generate_design_insight,
)
from rnaseq_nav.intelligence.suitability import (
    generate_suitability_insight,
)
from rnaseq_nav.intelligence.analysis_planner import (
    generate_analysis_plan,
)
from rnaseq_nav.intelligence.metadata_intelligence import (
    generate_metadata_insight,
)


def make_metadata(
    strategy="RNA_SEQ",
    title="Control and treated samples",
    organism="Mycobacterium tuberculosis H37Rv",
    layout="PAIRED",
    platform="ILLUMINA",
    source="TRANSCRIPTOMIC",
    selection="cDNA",
    run_accession="SRR17730393",
):
    return SimpleNamespace(
        project=SimpleNamespace(
            accession="PRJNA_TEST"
        ),
        study=SimpleNamespace(
            accession="SRP_TEST"
        ),
        experiment=SimpleNamespace(
            accession="SRX_TEST",
            title=title,
            library_strategy=strategy,
            library_source=source,
            library_selection=selection,
            layout=layout,
            platform=platform,
            instrument="Illumina instrument",
        ),
        run=SimpleNamespace(
            accession=run_accession,
            total_spots=1000,
            total_bases=100000,
            public=True,
        ),
        sample=SimpleNamespace(
            accession="SRS_TEST",
            biosample="SAMN_TEST",
            organism=organism,
        ),
    )


def test_rna_seq_is_classified_as_compatible():
    metadata = make_metadata(strategy="RNA_SEQ")

    insight = generate_modality_insight(metadata)

    assert insight.modality == "RNA-seq"
    assert insight.workflow_family == "bulk_rna_seq"
    assert insight.rna_seq_compatible is True
    assert insight.compatibility_status == "Compatible"
    assert insight.classification_confidence == "High"


def test_amplicon_is_not_rna_seq_compatible():
    metadata = make_metadata(
        strategy="AMPLICON",
        source="GENOMIC",
        selection="PCR",
    )

    insight = generate_modality_insight(metadata)

    assert insight.modality == "Amplicon sequencing"
    assert insight.workflow_family == "amplicon"
    assert insight.rna_seq_compatible is False
    assert insight.compatibility_status == "Not compatible"
    assert insight.classification_confidence == "High"

    assert any(
        "AMPLICON" in warning
        for warning in insight.warnings
    )


def test_unknown_strategy_remains_uncertain():
    metadata = make_metadata(strategy="")

    insight = generate_modality_insight(metadata)

    assert insight.rna_seq_compatible is None
    assert insight.compatibility_status == "Uncertain"
    assert insight.classification_confidence == "Low"


def test_small_rna_is_not_automatically_conventional_rna_seq():
    metadata = make_metadata(
        strategy="SMALL_RNA",
        source="TRANSCRIPTOMIC",
        selection="size fractionation",
    )

    insight = generate_modality_insight(metadata)

    assert insight.modality == "Small RNA sequencing"
    assert insight.workflow_family == "specialized_rna"
    assert insight.rna_seq_compatible is False
    assert insight.compatibility_status == "Specialized workflow"


def test_design_does_not_assume_biological_replicates_from_one_run():
    metadata = make_metadata(
        strategy="RNA_SEQ",
        title="Iron stress treatment",
    )

    insight = generate_design_insight(metadata)

    assert "biological replicate" in (
        insight.replicate_information.lower()
    )

    assert "One sequencing run" in insight.replicate_information


def test_design_marks_control_as_missing_when_not_explicit():
    metadata = make_metadata(
        strategy="RNA_SEQ",
        title="Iron stress treatment",
    )

    insight = generate_design_insight(metadata)

    assert not insight.control

    assert (
        "Control-group annotation"
        in insight.missing_information
    )


def test_amplicon_is_not_suitable_for_rna_seq():
    metadata = make_metadata(
        strategy="AMPLICON",
        source="GENOMIC",
        selection="PCR",
    )

    modality = generate_modality_insight(metadata)
    design = generate_design_insight(metadata)

    suitability = generate_suitability_insight(
        metadata,
        design_insight=design,
        modality_insight=modality,
    )

    assert (
        suitability.overall
        == "Not suitable for RNA-seq analysis"
    )

    assert suitability.score == 0


def test_unknown_modality_does_not_become_suitable():
    metadata = make_metadata(strategy="")

    modality = generate_modality_insight(metadata)
    design = generate_design_insight(metadata)

    suitability = generate_suitability_insight(
        metadata,
        design_insight=design,
        modality_insight=modality,
    )

    assert (
        suitability.overall
        == "RNA-seq compatibility uncertain"
    )

    assert suitability.score == 0


def test_rna_seq_receives_rna_seq_analysis_plan():
    metadata = make_metadata(
        strategy="RNA_SEQ",
        title="RNA-seq experiment",
    )

    metadata_insight = generate_metadata_insight(metadata)
    modality = generate_modality_insight(metadata)
    design = generate_design_insight(metadata)

    suitability = generate_suitability_insight(
        metadata,
        design_insight=design,
        modality_insight=modality,
    )

    plan = generate_analysis_plan(
        metadata,
        metadata_insight,
        design,
        suitability,
        modality,
    )

    assert plan.workflow == "RNA-seq analysis"
    assert plan.alignment == "STAR"
    assert plan.quantification == "featureCounts"
    assert plan.differential_analysis == "DESeq2"


def test_amplicon_cannot_receive_rna_seq_tools():
    metadata = make_metadata(
        strategy="AMPLICON",
        source="GENOMIC",
        selection="PCR",
        title="16S amplicon sequencing",
    )

    metadata_insight = generate_metadata_insight(metadata)
    modality = generate_modality_insight(metadata)
    design = generate_design_insight(metadata)

    suitability = generate_suitability_insight(
        metadata,
        design_insight=design,
        modality_insight=modality,
    )

    plan = generate_analysis_plan(
        metadata,
        metadata_insight,
        design,
        suitability,
        modality,
    )

    assert (
        plan.workflow
        == "RNA-seq workflow not applicable"
    )

    assert plan.alignment == "Not applicable"
    assert plan.quantification == "Not applicable"
    assert plan.differential_analysis == "Not applicable"
    assert plan.design_formula == "Not applicable"
    assert plan.confidence == "High"


def test_modality_gate_propagates_through_suitability_and_planning():
    metadata = make_metadata(
        strategy="AMPLICON",
        source="GENOMIC",
        selection="PCR",
        title="16S amplicon sequencing",
    )

    modality = generate_modality_insight(metadata)

    assert modality.rna_seq_compatible is False

    design = generate_design_insight(metadata)

    suitability = generate_suitability_insight(
        metadata,
        design_insight=design,
        modality_insight=modality,
    )

    assert suitability.score == 0
    assert (
        suitability.overall
        == "Not suitable for RNA-seq analysis"
    )

    metadata_insight = generate_metadata_insight(metadata)

    plan = generate_analysis_plan(
        metadata,
        metadata_insight,
        design,
        suitability,
        modality,
    )

    assert (
        plan.workflow
        == "RNA-seq workflow not applicable"
    )

    assert plan.alignment == "Not applicable"
    assert plan.quantification == "Not applicable"
    assert plan.differential_analysis == "Not applicable"
    assert plan.design_formula == "Not applicable"
