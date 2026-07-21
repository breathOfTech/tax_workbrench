"""Extraction log formatting — readable structured output for fact extraction."""

import logging

from libs.extraction.schema import ExtractionResult

logger = logging.getLogger(__name__)

FACT_DISPLAY_FIELDS: dict[str, list[str]] = {
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
        logger.info("[Extraction] No facts extracted. Reason: %s", result.reasoning)
        return

    lines = [
        "[Extraction] Result:",
        f"  reasoning: \"{result.reasoning}\"",
        "  facts:",
    ]
    for i, fact_action in enumerate(result.facts, 1):
        fact_data = fact_action.fact.model_dump()
        fact_type = fact_data["fact_type"]
        confidence = fact_data["confidence"]
        action = fact_action.action
        display_fields = FACT_DISPLAY_FIELDS.get(fact_type, [])
        parts = [f"{k}={fact_data[k]}" for k in display_fields if fact_data.get(k) is not None]

        action_str = f"[{action}]"
        if fact_action.matched_fact_id:
            action_str += f" -> {fact_action.matched_fact_id[:8]}"

        lines.append(
            f"    {i}. {action_str} {fact_type} | confidence={confidence} | {' | '.join(parts)}"
        )
        if fact_action.reason:
            lines.append(f"       reason: {fact_action.reason}")

    logger.info("\n".join(lines))


def format_extraction_result(result: ExtractionResult) -> str:
    """Format extraction result as a human-readable string for tool output."""
    if not result.facts:
        return "No tax facts found in this message."

    lines = [f"Extracted {len(result.facts)} facts:"]
    for i, fact_action in enumerate(result.facts, 1):
        data = fact_action.fact.model_dump()
        action = fact_action.action
        fact_type = data["fact_type"]
        confidence = data["confidence"]

        skip = {"fact_type", "confidence", "source_quote"}
        fields = {k: v for k, v in data.items() if k not in skip and v is not None and v is not False}
        field_str = ", ".join(f"{k}={v}" for k, v in list(fields.items())[:6])

        lines.append(f"  {i}. [{action}] {fact_type} (confidence={confidence}): {field_str}")
        if fact_action.reason:
            lines.append(f"     reason: {fact_action.reason}")

    return "\n".join(lines)
