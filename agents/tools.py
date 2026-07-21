"""Agent tools — fact extraction and persistence tools for the deep agent."""

import logging
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import tool

from libs.extraction import (
    extract_from_message,
    format_extraction_result,
    log_extraction_result,
)

logger = logging.getLogger(__name__)


def create_extract_facts_tool(llm: BaseChatModel):
    """Create an extract_facts tool bound to a specific LLM instance."""

    @tool
    async def extract_facts(
        user_message: str,
        existing_facts_summary: str = "No existing facts collected yet.",
    ) -> str:
        """Extract structured tax facts from a user message.

        Use this tool when the user shares personal or financial information
        (income, deductions, life events, filing status, etc.).

        Do NOT use this tool when the user is asking questions or seeking explanations.

        Args:
            user_message: The user's message to extract facts from.
            existing_facts_summary: Summary of previously collected facts for context.

        Returns:
            Formatted extraction result describing what was found.
        """
        result = await extract_from_message(llm, user_message, existing_facts_summary)
        log_extraction_result(result)
        return format_extraction_result(result)

    return extract_facts


@tool
def save_extracted_facts(facts: list[dict[str, Any]]) -> str:
    """Save extracted tax facts to the fact ledger.

    Call this after extracting facts to persist them.

    Args:
        facts: List of extracted fact dictionaries with action metadata.

    Returns:
        Confirmation message with count of saved facts.
    """
    # Placeholder for DB persistence — will be wired to FactsRepository
    if not facts:
        return "No facts to save."

    creates = sum(1 for f in facts if f.get("action") == "create")
    updates = sum(1 for f in facts if f.get("action") == "update")
    replaces = sum(1 for f in facts if f.get("action") == "replace")

    return f"Saved {len(facts)} facts: {creates} new, {updates} updated, {replaces} replaced."


@tool
def get_collected_facts() -> str:
    """Retrieve all previously collected tax facts for this conversation.

    Use this to understand what information has already been gathered
    before asking follow-up questions or when the user references
    previously shared information.

    Returns:
        Summary of all collected facts.
    """
    # Placeholder — will be wired to FactsRepository
    return "No facts collected yet."
