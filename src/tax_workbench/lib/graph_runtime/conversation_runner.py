"""Conversation runner — executes LangGraph against a conversation thread."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.state import CompiledStateGraph

from tax_workbench.lib.graph_runtime.provider import BaseGraphProvider
from tax_workbench.models.conversation import ConversationMessage, MessageRole


class BaseConversationRunner(ABC):
    """Abstract runner interface."""

    @abstractmethod
    async def run(
        self, conversation_id: str, messages: list[ConversationMessage]
    ) -> ConversationMessage:
        """Execute the graph and return the full assistant response."""
        ...

    @abstractmethod
    async def stream(
        self, conversation_id: str, messages: list[ConversationMessage]
    ) -> AsyncGenerator[str, None]:
        """Execute the graph and yield response token chunks as they arrive."""
        ...


class ConversationRunner(BaseConversationRunner):
    """Runs the supervisor graph for a conversation turn.

    Supports both full invocation and streaming.
    """

    def __init__(self, graph_provider: BaseGraphProvider) -> None:
        self._graph_provider = graph_provider

    def _to_langchain_messages(self, messages: list[ConversationMessage]) -> list:
        """Convert conversation messages to LangChain format."""
        lc_messages = []
        for msg in messages:
            if msg.role == MessageRole.USER:
                lc_messages.append(HumanMessage(content=msg.content))
            elif msg.role == MessageRole.ASSISTANT:
                lc_messages.append(AIMessage(content=msg.content))
        return lc_messages

    async def run(
        self, conversation_id: str, messages: list[ConversationMessage]
    ) -> ConversationMessage:
        """Execute one turn of the graph (non-streaming)."""
        graph = await self._graph_provider.get_graph()
        lc_messages = self._to_langchain_messages(messages)
        config = {"configurable": {"thread_id": conversation_id}}

        result = await graph.ainvoke({"messages": lc_messages}, config=config)

        # Extract the last AI message
        response_messages = result.get("messages", [])
        last_ai_message = ""
        for msg in reversed(response_messages):
            if isinstance(msg, AIMessage):
                last_ai_message = msg.content
                break

        return ConversationMessage(
            role=MessageRole.ASSISTANT,
            content=last_ai_message or "I couldn't generate a response.",
        )

    async def stream(
        self, conversation_id: str, messages: list[ConversationMessage]
    ) -> AsyncGenerator[str, None]:
        """Execute one turn and yield token chunks via astream_events."""
        graph = await self._graph_provider.get_graph()
        lc_messages = self._to_langchain_messages(messages)
        config = {"configurable": {"thread_id": conversation_id}}

        async for event in graph.astream_events(
            {"messages": lc_messages}, config=config, version="v2"
        ):
            kind = event.get("event")
            if kind == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    content = chunk.content
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                yield block["text"]
                            elif isinstance(block, str):
                                yield block
                    else:
                        yield content
