"""Base tax fact model — common fields for all fact entities."""

from enum import StrEnum

from pydantic import Field, model_validator

from libs.db.base_document import BaseDocument


class FactStatus(StrEnum):
    EXTRACTED = "extracted"
    CONFIRMED = "confirmed"
    NEEDS_CLARIFICATION = "needs_clarification"
    SUPERSEDED = "superseded"


class BaseTaxFact(BaseDocument):
    """Base class for all tax fact entities.

    Every fact is linked to a conversation, has a confidence score,
    and tracks its extraction status.
    """

    fact_type: str = ""
    conversation_id: str
    tax_year: int
    confidence: float = Field(ge=0.0, le=1.0)
    status: FactStatus = FactStatus.EXTRACTED
    source_quote: str
    superseded_by_id: str | None = None

    @model_validator(mode="before")
    @classmethod
    def set_fact_type(cls, data: dict) -> dict:
        """Auto-set fact_type from the class name if not provided."""
        if isinstance(data, dict) and not data.get("fact_type"):
            data["fact_type"] = cls._class_name_to_fact_type()
        return data

    @classmethod
    def _class_name_to_fact_type(cls) -> str:
        """Convert CamelCase class name to snake_case fact_type.

        Examples: W2Income -> w2_income, RSUVest -> rsu_vest,
        CaliforniaAdjustment -> california_adjustment
        """
        name = cls.__name__
        chars = []
        for i, c in enumerate(name):
            if c.isupper() and i > 0:
                prev_upper = name[i - 1].isupper()
                next_lower = (i + 1 < len(name)) and name[i + 1].islower()
                if not prev_upper or next_lower:
                    chars.append("_")
            chars.append(c.lower())
        return "".join(chars)
