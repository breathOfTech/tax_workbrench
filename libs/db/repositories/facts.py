"""Facts repository — data access layer for tax fact documents."""

from abc import ABC, abstractmethod

from libs.db.connection import MongoManager
from libs.db.database_service import DatabaseService
from libs.models.facts.base import BaseTaxFact
from libs.models.facts.registry import resolve_fact_class


class BaseFactsRepository(ABC):
    """Abstract repository interface for tax facts."""

    @abstractmethod
    async def save(self, fact: BaseTaxFact) -> BaseTaxFact:
        ...

    @abstractmethod
    async def save_many(self, facts: list[BaseTaxFact]) -> list[BaseTaxFact]:
        ...

    @abstractmethod
    async def find_by_conversation(self, conversation_id: str) -> list[BaseTaxFact]:
        ...

    @abstractmethod
    async def find_by_tax_year(self, tax_year: int) -> list[BaseTaxFact]:
        ...


class FactsRepository(BaseFactsRepository):
    """MongoDB implementation of facts repository."""

    def __init__(self, mongo_manager: MongoManager) -> None:
        self._db_service = DatabaseService(
            mongo_manager=mongo_manager,
            collection_name="facts",
        )

    async def save(self, fact: BaseTaxFact) -> BaseTaxFact:
        data = await self._db_service.create(fact)
        return fact.__class__.from_mongo(data)

    async def save_many(self, facts: list[BaseTaxFact]) -> list[BaseTaxFact]:
        if not facts:
            return []
        docs = await self._db_service.create_many(facts)
        return [
            fact.__class__.from_mongo(doc)
            for fact, doc in zip(facts, docs)
        ]

    async def find_by_conversation(self, conversation_id: str) -> list[BaseTaxFact]:
        docs = await self._db_service.find({"conversation_id": conversation_id})
        return [_deserialize_fact(doc) for doc in docs]

    async def find_by_tax_year(self, tax_year: int) -> list[BaseTaxFact]:
        docs = await self._db_service.find({"tax_year": tax_year})
        return [_deserialize_fact(doc) for doc in docs]


def _deserialize_fact(data: dict) -> BaseTaxFact:
    """Deserialize a fact dict into the correct typed model using fact_type."""
    fact_type = data.get("fact_type", "")
    cls = resolve_fact_class(fact_type)
    return cls.from_mongo(data)
