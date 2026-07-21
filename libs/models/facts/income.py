"""Income fact models — W-2, RSU, stock sales, dividends, rental income."""

from enum import StrEnum

from pydantic import Field

from libs.models.facts.base import BaseTaxFact


class W2Income(BaseTaxFact):
    """W-2 wage income from an employer."""

    employer_name: str
    employer_ein: str | None = None
    state: str | None = None

    # Box 1-6: Core compensation
    gross_wages: float | None = None               # Box 1
    federal_tax_withheld: float | None = None      # Box 2
    social_security_wages: float | None = None     # Box 3
    social_security_tax_withheld: float | None = None  # Box 4
    medicare_wages: float | None = None            # Box 5
    medicare_tax_withheld: float | None = None     # Box 6

    # Box 12: Coded items
    retirement_401k_contributions: float | None = None   # Code D
    roth_401k_contributions: float | None = None         # Code AA
    hsa_employer_contributions: float | None = None      # Code W
    rsu_income_included: float | None = None             # Code V (RSU vest value in wages)

    # Box 13: Checkboxes
    statutory_employee: bool = False
    retirement_plan_participant: bool = False

    # Box 15-17: State
    state_wages: float | None = None               # Box 16
    state_tax_withheld: float | None = None        # Box 17

    # Box 14: Other (CA SDI, etc.)
    ca_sdi_withheld: float | None = None


class HoldingPeriod(StrEnum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"


class RSUVest(BaseTaxFact):
    """RSU vest event — creates cost basis for future sales."""

    company: str
    ticker: str | None = None
    vest_date: str
    shares_vested: int
    fmv_per_share: float                           # FMV at vest = cost basis for sale
    total_fmv_at_vest: float | None = None         # shares × FMV
    shares_withheld_for_taxes: int | None = None   # sell-to-cover
    net_shares_delivered: int | None = None
    grant_date: str | None = None
    grant_id: str | None = None

    # Multi-state sourcing (CA)
    days_worked_in_ca: int | None = None
    total_days_in_vesting_period: int | None = None


class StockSale(BaseTaxFact):
    """Stock or RSU sale — reported on 1099-B / Form 8949."""

    company: str | None = None
    ticker: str | None = None
    date_acquired: str | None = None
    date_sold: str
    shares_sold: float
    proceeds: float                                # Sale price × shares
    cost_basis: float | None = None                # FMV at vest for RSUs, purchase price for stocks
    gain_or_loss: float | None = None
    holding_period: HoldingPeriod | None = None

    # 1099-B specifics
    basis_reported_to_irs: bool = True
    wash_sale_loss_disallowed: float | None = None
    adjustment_code: str | None = None             # B = basis needs correction (common for RSUs)
    adjustment_amount: float | None = None

    # Link to RSU vest (if RSU sale)
    is_rsu_sale: bool = False
    related_vest_id: str | None = None             # Links to RSUVest.id


class DividendIncome(BaseTaxFact):
    """Dividend income from 1099-DIV."""

    payer_name: str
    ordinary_dividends: float | None = None        # Box 1a
    qualified_dividends: float | None = None       # Box 1b
    capital_gain_distributions: float | None = None  # Box 2a
    nondividend_distributions: float | None = None   # Box 3 (return of capital)
    federal_tax_withheld: float | None = None      # Box 4
    section_199a_dividends: float | None = None    # Box 5 (REIT QBI)
    foreign_tax_paid: float | None = None          # Box 7
    foreign_country: str | None = None             # Box 8
    exempt_interest_dividends: float | None = None  # Box 12
    state_tax_withheld: float | None = None        # Box 16


class RentalIncome(BaseTaxFact):
    """Rental income for a property — Schedule E Line 3."""

    property_id: str                               # Links to RentalProperty.id
    gross_rent_received: float
    months_rented: int = Field(default=12, ge=0, le=12)
    days_personal_use: int = 0
    active_participation: bool = True              # For $25K passive loss allowance
