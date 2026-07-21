"""Extraction log formatting — readable structured output for fact extraction."""

import logging

from agents.intake.extraction import ExtractionResult

logger = logging.getLogger(__name__)

_FACT_DISPLAY_FIELDS: dict[str, list[str]] = {
    "w2_income": ["employer_name", "gross_wages", "federal_tax_withheld"],
    "rsu_vest": ["company", "vest_date", "shares_vested", "fmv_per_share"],
    "stock_sale": ["company", "shares_sold", "proceeds", "holding_period"],
    "dividend_income": ["payer_name", "ordinary_dividends", "qualified_dividends"],
    "rental_income": ["property_address", "gross_rent_received", "months_rented"],
    "mortgage_interest": ["lender_name", "mortgage_interest_paid"],
    "property_tax": ["annual_amount", "is_rental_property"],
    "rental_expense": ["expense_type", "amount"],
    "filing_status": ["status_type", "spouse_name"],
    "taxpayer": ["first_name", "last_name", "state_of_residency"],
    "dependent": ["first_name", "relationship"],
    "estimated_payment": ["payment_type", "quarter", "amount", "state"],
    "california_adjustment": ["adjustment_type", "federal_amount", "california_amount", "is_addition"],
}


def log_extraction_result(result: ExtractionResult) -> None:
    """Log extraction result in a readable format."""
    if not result.facts:
        logger.info(f"[Intake] No facts extracted. Reason: {result.reasoning}")
        return

    lines = [
        "[Intake] Extraction result:",
        f"  reasoning: \"{result.reasoning}\"",
        "  facts:",
    ]
    for i, fact in enumerate(result.facts, 1):
        data = fact.model_dump()
        fact_type = data["fact_type"]
        confidence = data["confidence"]
        display_fields = _FACT_DISPLAY_FIELDS.get(fact_type, [])
        parts = [f"{k}={data[k]}" for k in display_fields if data.get(k) is not None]
        lines.append(f"    {i}. {fact_type} | confidence={confidence} | {' | '.join(parts)}")

    logger.info("\n".join(lines))
