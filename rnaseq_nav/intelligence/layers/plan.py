"""
Layer 4 — Plan

Generates a conservative downstream RNA-seq analysis plan
based on the interpreted dataset.

Recommendations are linked to dataset characteristics
rather than being presented as universal requirements.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class PipelineStep:
    step: str
    tool: str
    reason: str


@dataclass
class AnalysisPlan:
    analysis_goal: str
    pipeline: List[PipelineStep] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


def build_analysis_plan(
    interpretation: Any,
    assessment: Any,
    metadata: Any,
) -> AnalysisPlan:

    experiment_type = str(
        getattr(
            interpretation,
            "experiment_type",
            "Unknown",
        )
    )

    pipeline = []
    notes = []

    # ------------------------------------------------------
    # Small RNA
    # ------------------------------------------------------

    if experiment_type == "Small RNA-seq":

        pipeline.extend(
            [
                PipelineStep(
                    "Quality control",
                    "FastQC",
                    "Inspect read quality and sequencing characteristics.",
                ),
                PipelineStep(
                    "Adapter processing",
                    "Cutadapt",
                    "Small RNA libraries commonly require careful adapter removal.",
                ),
                PipelineStep(
                    "Small RNA quantification",
                    "miRDeep2",
                    "Suitable for small RNA/miRNA-oriented analysis when appropriate.",
                ),
                PipelineStep(
                    "Differential analysis",
                    "DESeq2",
                    "Useful for count-based differential analysis when replicate structure permits.",
                ),
            ]
        )

        notes.append(
            "The plan is oriented toward small RNA sequencing."
        )

    # ------------------------------------------------------
    # Conventional RNA-seq
    # ------------------------------------------------------

    elif experiment_type == "RNA-seq":

        pipeline.extend(
            [
                PipelineStep(
                    "Quality control",
                    "FastQC",
                    "Assess raw sequencing quality before downstream processing.",
                ),
                PipelineStep(
                    "Read preprocessing",
                    "Trim Galore",
                    "Remove adapters and low-quality sequence when required.",
                ),
                PipelineStep(
                    "Read alignment",
                    "HISAT2",
                    "Splice-aware alignment is appropriate for conventional RNA-seq.",
                ),
                PipelineStep(
                    "BAM processing",
                    "SAMtools",
                    "Process and inspect alignment files.",
                ),
                PipelineStep(
                    "Gene quantification",
                    "featureCounts",
                    "Generate gene-level count data for count-based analysis.",
                ),
                PipelineStep(
                    "Differential expression",
                    "DESeq2",
                    "Analyze gene-level counts when the experimental design supports it.",
                ),
            ]
        )

        notes.append(
            "The recommended workflow assumes a conventional bulk RNA-seq experiment."
        )

    # ------------------------------------------------------
    # Unknown
    # ------------------------------------------------------

    else:

        pipeline.append(
            PipelineStep(
                "Metadata review",
                "RNASeq Navigator",
                "The experiment type is not sufficiently established for a specific pipeline.",
            )
        )

        notes.append(
            "A specific analysis pipeline should not be recommended "
            "until the experiment type is clarified."
        )

    # ------------------------------------------------------
    # Metadata limitations
    # ------------------------------------------------------

    score = getattr(
        assessment,
        "score",
        0,
    )

    if score < 80:

        notes.append(
            "Review metadata completeness and experimental design "
            "before beginning downstream analysis."
        )

    return AnalysisPlan(
        analysis_goal=(
            "Gene-expression analysis"
            if experiment_type == "RNA-seq"
            else "Small RNA analysis"
            if experiment_type == "Small RNA-seq"
            else "Experiment-specific analysis"
        ),
        pipeline=pipeline,
        notes=notes,
    )


def plan_to_dict(
    plan: AnalysisPlan,
) -> Dict[str, Any]:

    return {
        "analysis_goal": plan.analysis_goal,
        "pipeline": [
            {
                "step": step.step,
                "tool": step.tool,
                "reason": step.reason,
            }
            for step in plan.pipeline
        ],
        "notes": plan.notes,
    }
