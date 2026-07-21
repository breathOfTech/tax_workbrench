"""General agent subgraph — answers tax questions and explains concepts."""

from typing import Annotated

from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

from agents.general.prompt import GENERAL_PROMPT
from libs.graph_runtime import ModelFactory, ModelSettings


class GeneralState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_general_graph(model_factory: ModelFactory) -> CompiledStateGraph:
    """Build the general agent subgraph."""
    llm = model_factory.create(ModelSettings(temperature=0.2))

    async def respond(state: GeneralState) -> dict:
        messages = [SystemMessage(content=GENERAL_PROMPT)] + state["messages"]
        response = await llm.ainvoke(messages)
        return {"messages": [response]}

    graph = StateGraph(GeneralState)
    graph.add_node("respond", respond)
    graph.set_entry_point("respond")
    graph.add_edge("respond", END)

    return graph.compile()
