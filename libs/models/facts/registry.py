"""Fact type registry — maps fact_type strings to their Pydantic model classes."""

from libs.models.facts.base import BaseTaxFact
from libs.models.facts.california import CaliforniaAdjustment
from libs.models.facts.deductions import MortgageInterest, PropertyTax, RentalExpense
from libs.models.facts.income import (
    DividendIncome,
    RentalIncome,
    RSUVest,
    StockSale,
    W2Income,
)
from libs.models.facts.payments import EstimatedPayment, WithholdingSummary
from libs.models.facts.property import DepreciationAsset, PrimaryResidence, RentalProperty
from libs.models.facts.taxpayer import Dependent, FilingStatus, Taxpayer

FACT_TYPE_REGISTRY: dict[str, type[BaseTaxFact]] = {
    "w2_income": W2Income,
    "rsu_vest": RSUVest,
    "stock_sale": StockSale,
    "dividend_income": DividendIncome,
    "rental_income": RentalIncome,
    "mortgage_interest": MortgageInterest,
    "property_tax": PropertyTax,
    "rental_expense": RentalExpense,
    "taxpayer": Taxpayer,
    "dependent": Dependent,
    "filing_status": FilingStatus,
    "estimated_payment": EstimatedPayment,
    "withholding_summary": WithholdingSummary,
    "primary_residence": PrimaryResidence,
    "rental_property": RentalProperty,
    "depreciation_asset": DepreciationAsset,
    "california_adjustment": CaliforniaAdjustment,
}


def resolve_fact_class(fact_type: str) -> type[BaseTaxFact]:
    """Resolve a fact_type string to its model class. Falls back to BaseTaxFact."""
    return FACT_TYPE_REGISTRY.get(fact_type, BaseTaxFact)
