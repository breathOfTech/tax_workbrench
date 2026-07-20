"""Conversations repository — data access layer for conversation documents."""

from abc import ABC, abstractmethod

from tax_workbench.db.connection import MongoManager
from tax_workbench.db.database_service import DatabaseService
from tax_workbench.models.conversation import (
    Conversation,
    ConversationMessage,
    ConversationState,
)


class BaseConversationsRepository(ABC):
    """Abstract repository interface for conversations.

    Allows swapping storage backend without changing service layer.
    """

    @abstractmethod
    async def create(self, conversation: Conversation) -> Conversation:
        ...

    @abstractmethod
    async def find_by_id(self, conversation_id: str) -> Conversation | None:
        ...

    @abstractmethod
    async def find_all(self) -> list[Conversation]:
        ...

    @abstractmethod
    async def append_message(
        self, conversation_id: str, message: ConversationMessage
    ) -> Conversation | None:
        ...

    @abstractmethod
    async def update_state(
        self, conversation_id: str, state: ConversationState
    ) -> Conversation | None:
        ...

    @abstractmethod
    async def delete(self, conversation_id: str) -> bool:
        ...


class ConversationsRepository(BaseConversationsRepository):
    """MongoDB implementation of conversations repository."""

    def __init__(self, mongo_manager: MongoManager) -> None:
        self._db_service = DatabaseService(
            mongo_manager=mongo_manager,
            collection_name="conversations",
        )

    async def create(self, conversation: Conversation) -> Conversation:
        data = await self._db_service.create(conversation)
        return Conversation.from_mongo(data)

    async def find_by_id(self, conversation_id: str) -> Conversation | None:
        data = await self._db_service.find_by_id(conversation_id)
        if data is None:
            return None
        return Conversation.from_mongo(data)

    async def find_all(self) -> list[Conversation]:
        docs = await self._db_service.find({})
        return [Conversation.from_mongo(doc) for doc in docs]

    async def append_message(
        self, conversation_id: str, message: ConversationMessage
    ) -> Conversation | None:
        data = await self._db_service.push(
            conversation_id, "messages", message.model_dump()
        )
        if data is None:
            return None
        return Conversation.from_mongo(data)

    async def update_state(
        self, conversation_id: str, state: ConversationState
    ) -> Conversation | None:
        data = await self._db_service.update(
            conversation_id, {"$set": {"state": state.value}}
        )
        if data is None:
            return None
        return Conversation.from_mongo(data)

    async def delete(self, conversation_id: str) -> bool:
        return await self._db_service.delete(conversation_id)
