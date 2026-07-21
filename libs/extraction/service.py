"""Extraction service — performs structured fact extraction via LLM."""

import logging

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from libs.extraction.schema import ExtractionResult

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """You are a tax fact extraction engine. Your job is to identify and extract structured tax facts from a user's message, and determine how each fact relates to previously collected facts.

## Extraction Rules

- Only extract facts that are EXPLICITLY stated in the message
- Do NOT infer, assume, or fill in information the user didn't say
- Set confidence between 0.0 and 1.0 based on how clear and specific the information is:
  - 1.0: exact numbers with clear context ("my W-2 shows $150,000 gross wages from Google")
  - 0.7-0.9: clear intent but some ambiguity ("I made about 150k at Google")
  - 0.5-0.7: vague or partial ("I work at Google and make good money")
  - Below 0.5: don't extract, it's too uncertain
- source_quote must be the exact text from the user's message that supports the fact
- If the message contains NO extractable tax facts (greetings, questions, off-topic), return an empty facts list
- A single message can contain multiple facts (e.g., "I made 150k at Google and my wife made 80k at Apple" = 2 W2 facts)

## Action Classification

For each extracted fact, determine the appropriate action by comparing against EXISTING FACTS (provided below):

- **create**: This is a brand new fact not previously collected. Use when:
  - No existing fact matches this entity (e.g., first time mentioning an employer)
  - User is providing information about a different entity (e.g., second W-2 from a different employer)

- **update**: The user is adding more detail to an existing fact. Use when:
  - Same entity (same employer, same property, same dependent) but providing additional fields
  - e.g., previously had employer name only, now providing salary details
  - Set matched_fact_id to the existing fact's ID

- **replace**: The user is correcting or contradicting an existing fact. Use when:
  - Same entity but a previously stated value is being changed
  - e.g., "Actually my salary was $190k, not $185k"
  - e.g., "Wait, we're filing single not jointly"
  - Set matched_fact_id to the existing fact's ID

**How to match entities:**
- W-2s match on employer_name
- RSU vests match on company + vest_date
- Stock sales match on company + date_sold + shares_sold
- Mortgage interest matches on lender_name
- Property tax matches on state/county or property context
- Dependents match on first_name
- Filing status: only one exists per return — any new one replaces
- Taxpayer: only one per person — updates accumulate

If no existing facts are provided, all extracted facts should use action "create".

## Fact Types

- w2_income: W-2 wage/salary information
- rsu_vest: RSU vesting events
- stock_sale: Stock or RSU sales
- dividend_income: Dividend income (1099-DIV)
- rental_income: Rental property income
- mortgage_interest: Mortgage interest (1098)
- property_tax: Property tax payments
- rental_expense: Rental property expenses
- filing_status: Filing status (single, MFJ, etc.)
- taxpayer: Taxpayer personal info (name, state, occupation)
- dependent: Dependent information
- estimated_payment: Estimated tax payments made
- california_adjustment: California-specific differences from federal (HSA contributions not deductible in CA, no bonus depreciation, etc.)"""


async def extract_from_message(
    llm: BaseChatModel,
    user_message: str,
    existing_facts_context: str = "No existing facts collected yet.",
) -> ExtractionResult:
    """Extract structured tax facts from a user message.

    Args:
        llm: The LLM to use for structured extraction.
        user_message: The user's raw message text.
        existing_facts_context: Formatted summary of previously collected facts.

    Returns:
        ExtractionResult with facts and their reconciliation actions.
    """
    structured_llm = llm.with_structured_output(ExtractionResult)

    result: ExtractionResult = await structured_llm.ainvoke([
        SystemMessage(content=EXTRACTION_PROMPT),
        HumanMessage(
            content=f"EXISTING FACTS:\n{existing_facts_context}\n\nUSER MESSAGE:\n{user_message}"
        ),
    ])

    return result
