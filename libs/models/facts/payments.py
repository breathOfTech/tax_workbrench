"""Payment fact models — estimated tax payments, withholding summaries."""

from enum import StrEnum

from pydantic import Field

from libs.models.facts.base import BaseTaxFact


class PaymentType(StrEnum):
    FEDERAL_ESTIMATED = "federal_estimated"
    STATE_ESTIMATED = "state_estimated"
    EXTENSION_PAYMENT = "extension_payment"


class EstimatedPayment(BaseTaxFact):
    """Estimated tax payment — Form 1040-ES or state equivalent."""

    payment_type: PaymentType
    quarter: int = Field(ge=1, le=4)               # Q1=Apr, Q2=Jun, Q3=Sep, Q4=Jan next year
    amount: float
    date_paid: str
    confirmation_number: str | None = None
    state: str | None = None                     # For state estimated payments


class WithholdingSummary(BaseTaxFact):
    """Aggregated withholding totals — derived from W-2s, 1099s, etc."""

    federal_income_tax_withheld: float = 0.0
    social_security_tax_withheld: float = 0.0
    medicare_tax_withheld: float = 0.0
    state_income_tax_withheld: float = 0.0
    state: str | None = None                     # Which state
    local_tax_withheld: float | None = None
