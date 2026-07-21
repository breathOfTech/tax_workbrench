"""Taxpayer, dependent, and filing status models."""

from enum import StrEnum

from pydantic import Field

from libs.models.facts.base import BaseTaxFact


class FilingStatusType(StrEnum):
    SINGLE = "single"
    MARRIED_FILING_JOINTLY = "married_filing_jointly"
    MARRIED_FILING_SEPARATELY = "married_filing_separately"
    HEAD_OF_HOUSEHOLD = "head_of_household"
    QUALIFYING_SURVIVING_SPOUSE = "qualifying_surviving_spouse"


class FilingStatus(BaseTaxFact):
    """Filing status for the tax year."""

    status_type: FilingStatusType
    spouse_name: str | None = None


class Taxpayer(BaseTaxFact):
    """Primary taxpayer and spouse information."""

    first_name: str
    last_name: str
    ssn: str | None = None
    date_of_birth: str | None = None
    occupation: str | None = None
    is_blind: bool = False
    state_of_residency: str | None = None
    residency_type: str | None = None  # full_year, part_year


class Dependent(BaseTaxFact):
    """A dependent claimed on the return."""

    first_name: str
    last_name: str
    relationship: str
    date_of_birth: str | None = None
    ssn: str | None = None
    qualifies_for_child_tax_credit: bool = False
    qualifies_for_other_dependent_credit: bool = False
    months_lived_with_taxpayer: int = Field(default=12, ge=0, le=12)
