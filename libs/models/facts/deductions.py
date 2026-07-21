"""Deduction fact models — mortgage interest, property tax, rental expenses."""

from enum import StrEnum

from libs.models.facts.base import BaseTaxFact


class MortgageInterest(BaseTaxFact):
    """Mortgage interest from Form 1098."""

    lender_name: str
    property_id: str                               # Links to PrimaryResidence or RentalProperty
    mortgage_interest_paid: float                   # Box 1
    outstanding_principal: float | None = None      # Box 2
    origination_date: str | None = None            # Box 3
    refund_of_overpaid_interest: float | None = None  # Box 4
    mortgage_insurance_premiums: float | None = None   # Box 5
    points_paid: float | None = None               # Box 6
    property_tax_from_escrow: float | None = None  # Box 10 (informational)

    # Limitation fields
    original_loan_amount: float | None = None
    acquisition_debt_limit_applies: bool = False   # $750K post-2017, $1M pre-2017


class PropertyTax(BaseTaxFact):
    """Property tax paid — Schedule A or Schedule E."""

    property_id: str                               # Links to PrimaryResidence or RentalProperty
    annual_amount: float
    is_rental_property: bool = False               # If True, goes to Sch E (no SALT cap)
    state: str | None = None
    county: str | None = None


class RentalExpenseType(StrEnum):
    ADVERTISING = "advertising"
    AUTO_TRAVEL = "auto_travel"
    CLEANING_MAINTENANCE = "cleaning_maintenance"
    COMMISSIONS = "commissions"
    INSURANCE = "insurance"
    LEGAL_PROFESSIONAL = "legal_professional"
    MANAGEMENT_FEES = "management_fees"
    MORTGAGE_INTEREST = "mortgage_interest"
    OTHER_INTEREST = "other_interest"
    REPAIRS = "repairs"
    SUPPLIES = "supplies"
    UTILITIES = "utilities"
    OTHER = "other"


class RentalExpense(BaseTaxFact):
    """Individual rental expense — Schedule E Lines 5-19."""

    property_id: str                               # Links to RentalProperty.id
    expense_type: RentalExpenseType
    amount: float
    description: str | None = None                 # For "other" type
