"""Intake agent subgraph — extracts tax facts from user messages."""

from typing import Annotated

from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

from agents.intake.prompt import INTAKE_PROMPT
from libs.graph_runtime import ModelFactory, ModelSettings


class IntakeState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_intake_graph(model_factory: ModelFactory) -> CompiledStateGraph:
    """Build the intake agent subgraph."""
    llm = model_factory.create(ModelSettings(temperature=0.3))

    async def extract(state: IntakeState) -> dict:
        messages = [SystemMessage(content=INTAKE_PROMPT)] + state["messages"]
        response = await llm.ainvoke(messages)
        return {"messages": [response]}

    graph = StateGraph(IntakeState)
    graph.add_node("extract", extract)
    graph.set_entry_point("extract")
    graph.add_edge("extract", END)

    return graph.compile()
