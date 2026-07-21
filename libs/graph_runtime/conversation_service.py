"""Conversation service — orchestrates repository and graph runner.

This is the service layer between routes and the graph execution.
Routes stay thin, all business logic lives here.
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator

from libs.db.repositories.conversations import BaseConversationsRepository
from libs.graph_runtime.conversation_runner import BaseConversationRunner
from libs.models.conversation import (
    Conversation,
    ConversationMessage,
    ConversationState,
    MessageRole,
)


class BaseConversationService(ABC):
    """Abstract service interface."""

    @abstractmethod
    async def create_conversation(self, content: str) -> Conversation:
        ...

    @abstractmethod
    async def send_message(self, conversation_id: str, content: str) -> Conversation:
        ...

    @abstractmethod
    async def stream_response(
        self, conversation_id: str, content: str
    ) -> AsyncGenerator[str, None]:
        """Stream the assistant response token by token."""
        ...

    @abstractmethod
    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        ...

    @abstractmethod
    async def list_conversations(self) -> list[Conversation]:
        ...

    @abstractmethod
    async def delete_conversation(self, conversation_id: str) -> bool:
        ...


class ConversationService(BaseConversationService):
    """Orchestrates conversation persistence and graph execution.

    Flow (non-streaming):
    1. Persist user message
    2. Mark conversation as agent_executing
    3. Run graph
    4. Persist assistant response
    5. Mark conversation as open

    Flow (streaming):
    1. Persist user message
    2. Mark conversation as agent_executing
    3. Stream graph (yield tokens)
    4. Persist full response after stream completes
    5. Mark conversation as open
    """

    def __init__(
        self,
        repository: BaseConversationsRepository,
        runner: BaseConversationRunner,
    ) -> None:
        self._repository = repository
        self._runner = runner

    async def create_conversation(self, content: str) -> Conversation:
        """Create a new conversation, run the graph, return with response."""
        user_message = ConversationMessage(role=MessageRole.USER, content=content)
        conversation = Conversation(
            messages=[user_message],
            state=ConversationState.AGENT_EXECUTING,
        )
        conversation = await self._repository.create(conversation)

        try:
            response = await self._runner.run(conversation.id, conversation.messages)
            await self._repository.append_message(conversation.id, response)
        finally:
            conversation = await self._repository.update_state(
                conversation.id, ConversationState.OPEN
            )
        return conversation

    async def send_message(self, conversation_id: str, content: str) -> Conversation:
        """Append a message and run the graph (non-streaming)."""
        conversation = await self._repository.find_by_id(conversation_id)
        if conversation is None:
            raise ValueError(f"Conversation {conversation_id} not found")

        user_message = ConversationMessage(role=MessageRole.USER, content=content)
        conversation = await self._repository.append_message(conversation_id, user_message)
        await self._repository.update_state(conversation_id, ConversationState.AGENT_EXECUTING)

        try:
            response = await self._runner.run(conversation_id, conversation.messages)
            await self._repository.append_message(conversation_id, response)
        finally:
            conversation = await self._repository.update_state(
                conversation_id, ConversationState.OPEN
            )
        return conversation

    async def stream_response(
        self, conversation_id: str, content: str
    ) -> AsyncGenerator[str, None]:
        """Stream the assistant response. Persists full message after completion."""
        conversation = await self._repository.find_by_id(conversation_id)
        if conversation is None:
            raise ValueError(f"Conversation {conversation_id} not found")

        user_message = ConversationMessage(role=MessageRole.USER, content=content)
        conversation = await self._repository.append_message(conversation_id, user_message)
        await self._repository.update_state(conversation_id, ConversationState.AGENT_EXECUTING)

        full_response = ""
        try:
            async for chunk in self._runner.stream(conversation_id, conversation.messages):
                full_response += chunk
                yield chunk
        finally:
            if full_response:
                response_message = ConversationMessage(
                    role=MessageRole.ASSISTANT, content=full_response
                )
                await self._repository.append_message(conversation_id, response_message)
            await self._repository.update_state(conversation_id, ConversationState.OPEN)

    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        return await self._repository.find_by_id(conversation_id)

    async def list_conversations(self) -> list[Conversation]:
        return await self._repository.find_all()

    async def delete_conversation(self, conversation_id: str) -> bool:
        return await self._repository.delete(conversation_id)
