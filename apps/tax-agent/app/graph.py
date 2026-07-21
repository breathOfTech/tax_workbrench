"""Placeholder graph provider — minimal echo graph for testing the runtime.

Will be replaced with the full supervisor graph in the next commit.
"""

from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

from tax_workbench.lib.graph_runtime import CachingGraphProvider, ModelFactory, ModelSettings


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


class TaxAgentGraphProvider(CachingGraphProvider):
    """Placeholder — simple LLM call graph to prove the runtime works."""

    def __init__(self, model_factory: ModelFactory) -> None:
        super().__init__()
        self._model_factory = model_factory

    async def build_graph(self) -> CompiledStateGraph:
        llm = self._model_factory.create(ModelSettings(temperature=0.0))

        async def respond(state: State) -> dict:
            response = await llm.ainvoke(state["messages"])
            return {"messages": [response]}

        graph = StateGraph(State)
        graph.add_node("respond", respond)
        graph.set_entry_point("respond")
        graph.add_edge("respond", END)

        return graph.compile()
