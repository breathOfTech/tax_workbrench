"""Database service — CRUD abstraction over a MongoDB collection.

Each repository gets its own DatabaseService instance bound to a specific collection.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection

from libs.db.base_document import BaseDocument
from libs.db.connection import MongoManager


class BaseDatabaseService(ABC):
    """Abstract database service interface.

    Allows swapping MongoDB for another backend without changing repositories.
    """

    @abstractmethod
    async def create(self, document: BaseDocument) -> dict[str, Any]:
        ...

    @abstractmethod
    async def create_many(self, documents: list[BaseDocument]) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    async def find_by_id(self, doc_id: str) -> dict[str, Any] | None:
        ...

    @abstractmethod
    async def find(
        self, query: dict[str, Any], limit: int = 100, sort_field: str = "created_at"
    ) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    async def update(self, doc_id: str, update: dict[str, Any]) -> dict[str, Any] | None:
        ...

    @abstractmethod
    async def delete(self, doc_id: str) -> bool:
        ...

    @abstractmethod
    async def push(self, doc_id: str, field: str, value: Any) -> dict[str, Any] | None:
        ...


class DatabaseService(BaseDatabaseService):
    """MongoDB implementation of BaseDatabaseService.

    Provides CRUD operations for a single collection with
    automatic timestamp management.
    """

    def __init__(self, mongo_manager: MongoManager, collection_name: str) -> None:
        self._mongo_manager = mongo_manager
        self._collection_name = collection_name

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._mongo_manager.get_collection(self._collection_name)

    async def create(self, document: BaseDocument) -> dict[str, Any]:
        """Insert a document. Returns the inserted document dict."""
        data = document.to_mongo()
        await self.collection.insert_one(data)
        return data

    async def create_many(self, documents: list[BaseDocument]) -> list[dict[str, Any]]:
        """Insert multiple documents. Returns the inserted document dicts."""
        if not documents:
            return []
        docs = [doc.to_mongo() for doc in documents]
        await self.collection.insert_many(docs)
        return docs

    async def find_by_id(self, doc_id: str) -> dict[str, Any] | None:
        """Find a document by its ID."""
        return await self.collection.find_one({"_id": doc_id})

    async def find(
        self, query: dict[str, Any], limit: int = 100, sort_field: str = "created_at"
    ) -> list[dict[str, Any]]:
        """Find documents matching a query, sorted by creation date descending."""
        cursor = self.collection.find(query).sort(sort_field, -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def update(self, doc_id: str, update: dict[str, Any]) -> dict[str, Any] | None:
        """Update a document. Automatically sets updated_at."""
        update = {**update}
        set_fields = {**update.get("$set", {}), "updated_at": datetime.now(timezone.utc)}
        update["$set"] = set_fields
        result = await self.collection.find_one_and_update(
            {"_id": doc_id},
            update,
            return_document=True,
        )
        return result

    async def delete(self, doc_id: str) -> bool:
        """Delete a document by ID. Returns True if deleted."""
        result = await self.collection.delete_one({"_id": doc_id})
        return result.deleted_count > 0

    async def push(self, doc_id: str, field: str, value: Any) -> dict[str, Any] | None:
        """Push a value onto an array field. Used for appending messages."""
        return await self.update(doc_id, {"$push": {field: value}})
