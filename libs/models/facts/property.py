"""Property fact models — primary residence, rental properties, depreciation."""

from enum import StrEnum

from pydantic import Field

from libs.models.facts.base import BaseTaxFact


class PropertyType(StrEnum):
    SINGLE_FAMILY = "single_family"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    MULTI_FAMILY = "multi_family"
    COMMERCIAL = "commercial"


class PrimaryResidence(BaseTaxFact):
    """Primary residence — relevant for mortgage interest and property tax."""

    address: str
    city: str
    state: str
    zip_code: str | None = None
    property_type: PropertyType | None = None
    date_acquired: str | None = None
    purchase_price: float | None = None
    current_fmv: float | None = None


class RentalProperty(BaseTaxFact):
    """Rental property — Schedule E reporting."""

    address: str
    city: str
    state: str
    zip_code: str | None = None
    property_type: PropertyType | None = None
    date_acquired: str | None = None
    purchase_price: float | None = None
    land_value: float | None = None              # Non-depreciable portion
    building_value: float | None = None          # Depreciable portion

    # Schedule E classification
    fair_rental_days: int | None = None
    personal_use_days: int = 0
    percentage_ownership: float = Field(default=100.0, ge=0.0, le=100.0)


class DepreciationMethod(StrEnum):
    STRAIGHT_LINE = "straight_line"
    MACRS_GDS = "macrs_gds"
    MACRS_ADS = "macrs_ads"


class DepreciationAsset(BaseTaxFact):
    """Depreciable asset for a rental property — Form 4562."""

    property_id: str                             # Links to RentalProperty.id
    asset_description: str
    date_placed_in_service: str
    cost_or_basis: float
    land_excluded: bool = True                   # Land is never depreciable
    recovery_period_years: float                 # 27.5 residential, 39 commercial
    method: DepreciationMethod = DepreciationMethod.STRAIGHT_LINE
    prior_depreciation: float = 0.0             # Accumulated depreciation
    current_year_depreciation: float | None = None
    section_179_deduction: float | None = None
    bonus_depreciation_percentage: float | None = None
