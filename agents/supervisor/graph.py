"""Supervisor graph — routes user messages to the appropriate subagent."""

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


class SupervisorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


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
            response = await router_llm.ainvoke([
                SystemMessage(content=SUPERVISOR_PROMPT),
                HumanMessage(content=last_message.content),
            ])
            content = response.content
            if isinstance(content, list):
                content = "".join(
                    block["text"] if isinstance(block, dict) else block
                    for block in content
                )
            decision = content.strip().lower()
            return {"messages": [], "route": decision}

        async def intake_node(state: SupervisorState) -> dict:
            result = await intake_graph.ainvoke({"messages": state["messages"]})
            return {"messages": result["messages"][-1:]}

        async def general_node(state: SupervisorState) -> dict:
            result = await general_graph.ainvoke({"messages": state["messages"]})
            return {"messages": result["messages"][-1:]}

        def pick_agent(state: dict) -> Literal["intake", "general"]:
            decision = state.get("route", "general")
            if "intake" in decision:
                return "intake"
            return "general"

        # Build the graph with routing state
        class RoutingState(TypedDict):
            messages: Annotated[list[BaseMessage], add_messages]
            route: str

        graph = StateGraph(RoutingState)
        graph.add_node("router", route)
        graph.add_node("intake", intake_node)
        graph.add_node("general", general_node)

        graph.set_entry_point("router")
        graph.add_conditional_edges("router", pick_agent, {"intake": "intake", "general": "general"})
        graph.add_edge("intake", END)
        graph.add_edge("general", END)

        return graph.compile()
