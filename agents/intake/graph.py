"""Intake agent subgraph — extracts tax facts from user messages."""

import logging
import operator
from typing import Annotated

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

from agents.intake.extraction import ExtractionResult
from agents.intake.log_formatter import log_extraction_result
from agents.intake.prompt import INTAKE_PROMPT, EXTRACTION_PROMPT
from libs.graph_runtime import ModelFactory, ModelSettings

logger = logging.getLogger(__name__)


def _normalize_content(content: str | list) -> str:
    """Normalize message content that may be a list (Bedrock) to a string."""
    if isinstance(content, list):
        return "".join(
            block["text"] if isinstance(block, dict) else str(block)
            for block in content
        )
    return content


class IntakeState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    extracted_facts: Annotated[list[dict], operator.add]


def build_intake_graph(model_factory: ModelFactory) -> CompiledStateGraph:
    """Build the intake agent subgraph with conversation + extraction."""
    conversation_llm = model_factory.create(ModelSettings(temperature=0.3))
    extraction_llm = model_factory.create(ModelSettings(temperature=0.0))

    async def converse(state: IntakeState) -> dict:
        """Generate conversational response to user."""
        messages = [SystemMessage(content=INTAKE_PROMPT)] + state["messages"]
        response = await conversation_llm.ainvoke(messages)
        return {"messages": [response]}

    async def extract(state: IntakeState) -> dict:
        """Extract structured facts from the conversation turn."""
        user_messages = [m for m in state["messages"] if m.type == "human"]
        if not user_messages:
            return {"extracted_facts": []}

        last_user_msg = _normalize_content(user_messages[-1].content)

        try:
            structured_llm = extraction_llm.with_structured_output(ExtractionResult)
            result: ExtractionResult = await structured_llm.ainvoke([
                SystemMessage(content=EXTRACTION_PROMPT),
                HumanMessage(content=last_user_msg),
            ])
        except Exception:
            logger.warning("[Intake] Extraction failed, continuing without facts", exc_info=True)
            return {"extracted_facts": []}

        log_extraction_result(result)

        if result.facts:
            return {"extracted_facts": [fact.model_dump() for fact in result.facts]}
        return {"extracted_facts": []}

    graph = StateGraph(IntakeState)
    graph.add_node("converse", converse)
    graph.add_node("extract", extract)

    graph.set_entry_point("converse")
    graph.add_edge("converse", "extract")
    graph.add_edge("extract", END)

    return graph.compile()
