"""California-specific adjustment models — Schedule CA (540)."""

from enum import StrEnum

from libs.models.facts.base import BaseTaxFact


class CAAdjustmentType(StrEnum):
    """Types of California adjustments to federal AGI."""

    # Income additions (CA taxes what federal doesn't)
    HSA_CONTRIBUTION = "hsa_contribution"                # CA doesn't recognize HSA deduction
    MUNICIPAL_BOND_INTEREST = "municipal_bond_interest"  # Out-of-state muni bonds taxable in CA

    # Income subtractions (CA doesn't tax what federal does)
    SOCIAL_SECURITY = "social_security"                  # CA fully excludes SS income
    MILITARY_PAY = "military_pay"                        # Active duty stationed outside CA

    # Depreciation differences
    SECTION_179_DIFFERENCE = "section_179_difference"    # CA limits differ from federal
    BONUS_DEPRECIATION = "bonus_depreciation"            # CA doesn't allow bonus depreciation

    # Capital gains
    QUALIFIED_OPPORTUNITY_ZONE = "qualified_opportunity_zone"  # CA doesn't conform

    # Other
    ROTH_CONVERSION = "roth_conversion"                  # Timing differences
    NOL_DIFFERENCE = "nol_difference"                    # CA NOL rules differ
    OTHER = "other"


class CaliforniaAdjustment(BaseTaxFact):
    """California adjustment to federal income — Schedule CA Line items.

    Represents differences between federal and California tax treatment.
    Additions increase CA taxable income; subtractions decrease it.
    """

    adjustment_type: CAAdjustmentType
    federal_amount: float                        # Amount reported on federal return
    california_amount: float                     # Amount for CA purposes
    adjustment_amount: float | None = None       # Difference (computed if not provided)
    is_addition: bool                            # True = adds to CA income, False = subtracts
    schedule_ca_line: str | None = None          # e.g., "7" for wages, "13" for capital gains
    description: str | None = None               # Free-text explanation
