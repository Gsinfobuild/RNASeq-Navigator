"""
RNASeq Navigator

Metadata Contract

Version 1.0

Defines the minimum metadata requirements that every
Metadata object must satisfy before entering the
RNASeq Navigator pipeline.
"""

from dataclasses import dataclass, field

from rnaseq_nav.models import Metadata


# ==========================================================
# Contract Violation
# ==========================================================

@dataclass
class ContractViolation:

    section: str
    field: str
    message: str


# ==========================================================
# Contract Result
# ==========================================================

@dataclass
class ContractResult:

    passed: bool = True

    violations: list[ContractViolation] = field(
        default_factory=list
    )

    @property
    def total_violations(self):

        return len(self.violations)


# ==========================================================
# Metadata Contract
# ==========================================================

class MetadataContract:
    """
    Validates the structural integrity of a Metadata object.

    This checks only whether required fields exist and are
    populated. It does NOT assess biological correctness or
    metadata quality.
    """

    REQUIRED_FIELDS = [

        ("project", "accession"),

        ("study", "accession"),

        ("experiment", "accession"),

        ("experiment", "library_strategy"),

        ("experiment", "layout"),

        ("run", "accession"),

        ("sample", "organism"),

    ]

    # ------------------------------------------------------

    @classmethod
    def validate(
        cls,
        metadata: Metadata,
    ) -> ContractResult:

        result = ContractResult()

        for section_name, field_name in cls.REQUIRED_FIELDS:

            section = getattr(metadata, section_name)

            value = getattr(section, field_name)

            missing = False

            if value is None:

                missing = True

            elif isinstance(value, str):

                missing = value.strip() == ""

            if missing:

                result.passed = False

                result.violations.append(

                    ContractViolation(

                        section=section_name,

                        field=field_name,

                        message=(
                            f"{section_name}.{field_name} "
                            "is required."
                        ),

                    )

                )

        return result
