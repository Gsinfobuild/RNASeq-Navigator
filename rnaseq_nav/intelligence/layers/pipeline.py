"""
RNASeq Navigator intelligence pipeline.

Connects Layers 1–4:

Explore → Interpret → Assess → Plan
"""

from typing import Any, Dict

from .explore import (
    explore_dataset,
    exploration_to_dict,
)

from .interpret import (
    interpret_dataset,
    interpretation_to_dict,
)

from .assess import (
    assess_dataset,
    assessment_to_dict,
)

from .plan import (
    build_analysis_plan,
    plan_to_dict,
)


def run_intelligence_pipeline(
    result: Any,
    accession: str,
) -> Dict[str, Any]:
    """
    Execute the complete RNASeq Navigator interpretation pipeline.
    """

    # ------------------------------------------------------
    # Layer 1 — Explore
    # ------------------------------------------------------

    exploration = explore_dataset(
        result,
        accession,
    )

    # ------------------------------------------------------
    # Layer 2 — Interpret
    # ------------------------------------------------------

    interpretation = interpret_dataset(
        exploration.metadata,
        study_type=exploration.study_type,
        library_strategy=exploration.library_strategy,
    )

    # ------------------------------------------------------
    # Layer 3 — Assess
    # ------------------------------------------------------

    assessment = assess_dataset(
        exploration.metadata,
        interpretation,
    )

    # ------------------------------------------------------
    # Layer 4 — Plan
    # ------------------------------------------------------

    plan = build_analysis_plan(
        interpretation,
        assessment,
        exploration.metadata,
    )

    return {
        "explore": exploration_to_dict(
            exploration
        ),
        "interpret": interpretation_to_dict(
            interpretation
        ),
        "assess": assessment_to_dict(
            assessment
        ),
        "plan": plan_to_dict(
            plan
        ),
    }
