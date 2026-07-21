"""Extraction schema — structured output model for fact extraction."""

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Discriminator, Field, Tag


class ExtractedW2Income(BaseModel):
    """W-2 wage income extracted from conversation."""

    fact_type: Literal["w2_income"] = "w2_income"
    employer_name: str
    employer_ein: str | None = None
    state: str | None = None
    gross_wages: float | None = None
    federal_tax_withheld: float | None = None
    social_security_wages: float | None = None
    social_security_tax_withheld: float | None = None
    medicare_wages: float | None = None
    medicare_tax_withheld: float | None = None
    retirement_401k_contributions: float | None = None
    roth_401k_contributions: float | None = None
    hsa_employer_contributions: float | None = None
    rsu_income_included: float | None = None
    statutory_employee: bool = False
    retirement_plan_participant: bool = False
    state_wages: float | None = None
    state_tax_withheld: float | None = None
    ca_sdi_withheld: float | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedRSUVest(BaseModel):
    """RSU vest event extracted from conversation."""

    fact_type: Literal["rsu_vest"] = "rsu_vest"
    company: str
    ticker: str | None = None
    vest_date: str
    shares_vested: int
    fmv_per_share: float
    total_fmv_at_vest: float | None = None
    shares_withheld_for_taxes: int | None = None
    net_shares_delivered: int | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedStockSale(BaseModel):
    """Stock or RSU sale extracted from conversation."""

    fact_type: Literal["stock_sale"] = "stock_sale"
    company: str | None = None
    ticker: str | None = None
    date_acquired: str | None = None
    date_sold: str
    shares_sold: float
    proceeds: float
    cost_basis: float | None = None
    holding_period: Literal["short_term", "long_term"] | None = None
    is_rsu_sale: bool = False
    wash_sale_loss_disallowed: float | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedDividendIncome(BaseModel):
    """Dividend income extracted from conversation."""

    fact_type: Literal["dividend_income"] = "dividend_income"
    payer_name: str
    ordinary_dividends: float | None = None
    qualified_dividends: float | None = None
    capital_gain_distributions: float | None = None
    federal_tax_withheld: float | None = None
    foreign_tax_paid: float | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedRentalIncome(BaseModel):
    """Rental income extracted from conversation."""

    fact_type: Literal["rental_income"] = "rental_income"
    property_address: str | None = None
    gross_rent_received: float
    months_rented: int = 12
    days_personal_use: int = 0
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedMortgageInterest(BaseModel):
    """Mortgage interest extracted from conversation."""

    fact_type: Literal["mortgage_interest"] = "mortgage_interest"
    lender_name: str
    mortgage_interest_paid: float
    outstanding_principal: float | None = None
    mortgage_insurance_premiums: float | None = None
    points_paid: float | None = None
    original_loan_amount: float | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedPropertyTax(BaseModel):
    """Property tax extracted from conversation."""

    fact_type: Literal["property_tax"] = "property_tax"
    annual_amount: float
    is_rental_property: bool = False
    state: str | None = None
    county: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedRentalExpense(BaseModel):
    """Rental expense extracted from conversation."""

    fact_type: Literal["rental_expense"] = "rental_expense"
    expense_type: str
    amount: float
    description: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedFilingStatus(BaseModel):
    """Filing status extracted from conversation."""

    fact_type: Literal["filing_status"] = "filing_status"
    status_type: Literal[
        "single",
        "married_filing_jointly",
        "married_filing_separately",
        "head_of_household",
        "qualifying_surviving_spouse",
    ]
    spouse_name: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedTaxpayer(BaseModel):
    """Taxpayer info extracted from conversation."""

    fact_type: Literal["taxpayer"] = "taxpayer"
    first_name: str
    last_name: str
    date_of_birth: str | None = None
    occupation: str | None = None
    state_of_residency: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedDependent(BaseModel):
    """Dependent extracted from conversation."""

    fact_type: Literal["dependent"] = "dependent"
    first_name: str
    last_name: str
    relationship: str
    date_of_birth: str | None = None
    qualifies_for_child_tax_credit: bool = False
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedEstimatedPayment(BaseModel):
    """Estimated tax payment extracted from conversation."""

    fact_type: Literal["estimated_payment"] = "estimated_payment"
    payment_type: Literal["federal_estimated", "state_estimated", "extension_payment"]
    quarter: int
    amount: float
    date_paid: str
    state: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


class ExtractedCaliforniaAdjustment(BaseModel):
    """California-specific tax adjustment extracted from conversation."""

    fact_type: Literal["california_adjustment"] = "california_adjustment"
    adjustment_type: Literal[
        "hsa_contribution",
        "municipal_bond_interest",
        "social_security",
        "military_pay",
        "section_179_difference",
        "bonus_depreciation",
        "qualified_opportunity_zone",
        "roth_conversion",
        "nol_difference",
        "other",
    ]
    federal_amount: float
    california_amount: float
    is_addition: bool
    description: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_quote: str


ExtractedFact = Annotated[
    Union[
        Annotated[ExtractedW2Income, Tag("w2_income")],
        Annotated[ExtractedRSUVest, Tag("rsu_vest")],
        Annotated[ExtractedStockSale, Tag("stock_sale")],
        Annotated[ExtractedDividendIncome, Tag("dividend_income")],
        Annotated[ExtractedRentalIncome, Tag("rental_income")],
        Annotated[ExtractedMortgageInterest, Tag("mortgage_interest")],
        Annotated[ExtractedPropertyTax, Tag("property_tax")],
        Annotated[ExtractedRentalExpense, Tag("rental_expense")],
        Annotated[ExtractedFilingStatus, Tag("filing_status")],
        Annotated[ExtractedTaxpayer, Tag("taxpayer")],
        Annotated[ExtractedDependent, Tag("dependent")],
        Annotated[ExtractedEstimatedPayment, Tag("estimated_payment")],
        Annotated[ExtractedCaliforniaAdjustment, Tag("california_adjustment")],
    ],
    Discriminator("fact_type"),
]


class FactAction(BaseModel):
    """An extracted fact paired with its reconciliation action."""

    fact: ExtractedFact
    action: Literal["create", "update", "replace"] = Field(
        description=(
            "create: brand new fact not seen before. "
            "update: refines/adds fields to an existing fact (same entity). "
            "replace: contradicts an existing fact — old one should be marked replaced."
        ),
    )
    matched_fact_id: str | None = Field(
        default=None,
        description="ID of the existing fact being updated or replaced. Required for update/replace actions.",
    )
    reason: str = Field(
        default="",
        description="Why this action was chosen (e.g., 'User corrected salary from $185k to $190k').",
    )


class ExtractionResult(BaseModel):
    """Result of fact extraction from a conversation turn.

    The LLM returns this as structured output. If no facts are found,
    the list is empty.
    """

    facts: list[FactAction] = Field(
        default_factory=list,
        description="Tax facts extracted from the user's message with reconciliation actions. Empty if no facts found.",
    )
    reasoning: str = Field(
        default="",
        description="Brief explanation of what facts were found and why, or why none were found.",
    )
