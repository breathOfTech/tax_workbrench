"""Tax fact models — structured entities extracted from conversations."""

from libs.models.facts.base import BaseTaxFact, FactStatus
from libs.models.facts.california import CaliforniaAdjustment, CAAdjustmentType
from libs.models.facts.deductions import (
    MortgageInterest,
    PropertyTax,
    RentalExpense,
    RentalExpenseType,
)
from libs.models.facts.income import (
    DividendIncome,
    HoldingPeriod,
    RentalIncome,
    RSUVest,
    StockSale,
    W2Income,
)
from libs.models.facts.payments import EstimatedPayment, PaymentType, WithholdingSummary
from libs.models.facts.property import (
    DepreciationAsset,
    DepreciationMethod,
    PrimaryResidence,
    PropertyType,
    RentalProperty,
)
from libs.models.facts.registry import FACT_TYPE_REGISTRY, resolve_fact_class
from libs.models.facts.taxpayer import (
    Dependent,
    FilingStatus,
    FilingStatusType,
    Taxpayer,
)

__all__ = [
    # Base
    "BaseTaxFact",
    "FactStatus",
    # Taxpayer
    "Taxpayer",
    "Dependent",
    "FilingStatus",
    "FilingStatusType",
    # Income
    "W2Income",
    "RSUVest",
    "StockSale",
    "DividendIncome",
    "RentalIncome",
    "HoldingPeriod",
    # Deductions
    "MortgageInterest",
    "PropertyTax",
    "RentalExpense",
    "RentalExpenseType",
    # Property
    "PrimaryResidence",
    "RentalProperty",
    "DepreciationAsset",
    "PropertyType",
    "DepreciationMethod",
    # Payments
    "EstimatedPayment",
    "WithholdingSummary",
    "PaymentType",
    # California
    "CaliforniaAdjustment",
    "CAAdjustmentType",
    # Registry
    "FACT_TYPE_REGISTRY",
    "resolve_fact_class",
]
