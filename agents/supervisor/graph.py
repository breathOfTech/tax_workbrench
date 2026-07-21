"""Supervisor graph — routes user messages to the appropriate subagent."""

import operator
from typing import Annotated, Literal

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

from agents.general.graph import build_general_graph
from agents.intake.graph import build_intake_graph
from agents.supervisor.prompt import SUPERVISOR_PROMPT
from libs.graph_runtime import CachingGraphProvider, ModelFactory, ModelSettings


def _normalize_content(content: str | list) -> str:
    """Normalize message content that may be a list (Bedrock) to a string."""
    if isinstance(content, list):
        return "".join(
            block["text"] if isinstance(block, dict) else str(block)
            for block in content
        )
    return content


class SupervisorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    extracted_facts: Annotated[list[dict], operator.add]


class SupervisorGraphProvider(CachingGraphProvider):
    """Builds the supervisor graph with intake and general subagents."""

    def __init__(self, model_factory: ModelFactory) -> None:
        super().__init__()
        self._model_factory = model_factory

    async def build_graph(self) -> CompiledStateGraph:
        router_llm = self._model_factory.create(
            ModelSettings(temperature=0.0, max_tokens=10)
        )
        intake_graph = build_intake_graph(self._model_factory)
        general_graph = build_general_graph(self._model_factory)

        async def route(state: SupervisorState) -> dict:
            """Classify the last user message and decide which agent handles it."""
            last_message = state["messages"][-1]
            content = _normalize_content(last_message.content)
            response = await router_llm.ainvoke([
                SystemMessage(content=SUPERVISOR_PROMPT),
                HumanMessage(content=content),
            ])
            response_content = _normalize_content(response.content)
            decision = response_content.strip().lower()
            return {"route": decision}

        async def intake_node(state: SupervisorState) -> dict:
            result = await intake_graph.ainvoke({
                "messages": state["messages"],
                "extracted_facts": [],
            })
            return {
                "messages": result["messages"][-1:],
                "extracted_facts": result.get("extracted_facts", []),
            }

        async def general_node(state: SupervisorState) -> dict:
            result = await general_graph.ainvoke({"messages": state["messages"]})
            return {"messages": result["messages"][-1:]}

        def pick_agent(state: SupervisorState) -> Literal["intake", "general"]:
            decision = state.get("route", "general")
            if "intake" in decision:
                return "intake"
            return "general"

        class RoutingState(TypedDict):
            messages: Annotated[list[BaseMessage], add_messages]
            route: str
            extracted_facts: Annotated[list[dict], operator.add]

        graph = StateGraph(RoutingState)
        graph.add_node("router", route)
        graph.add_node("intake", intake_node)
        graph.add_node("general", general_node)

        graph.set_entry_point("router")
        graph.add_conditional_edges("router", pick_agent, {"intake": "intake", "general": "general"})
        graph.add_edge("intake", END)
        graph.add_edge("general", END)

        return graph.compile()
