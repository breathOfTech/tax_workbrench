"""MongoDB connection manager.

Singleton — one client shared across all services via DI container.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel

from tax_workbench.config import get_setting


class DBSettings(BaseModel):
    """MongoDB connection settings, loaded from config."""

    uri: str = "mongodb://localhost:27017"
    db_name: str = "tax_workbench"


class MongoManager:
    """Manages MongoDB connection lifecycle.

    Singleton pattern — instantiated once via DI container,
    injected into all repositories and services that need DB access.
    """

    def __init__(self) -> None:
        self._client: AsyncIOMotorClient | None = None
        self._db: AsyncIOMotorDatabase | None = None
        self._settings: DBSettings | None = None

    async def connect(self) -> None:
        """Initialize connection from application settings."""
        self._settings = DBSettings(
            uri=get_setting("mongodb.uri", "mongodb://localhost:27017"),
            db_name=get_setting("mongodb.db_name", "tax_workbench"),
        )
        self._client = AsyncIOMotorClient(self._settings.uri)
        self._db = self._client[self._settings.db_name]

    async def disconnect(self) -> None:
        """Close connection and release resources."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    def get_database(self) -> AsyncIOMotorDatabase:
        """Get the database instance. Raises if not connected."""
        if self._db is None:
            raise RuntimeError("MongoManager not connected. Call connect() first.")
        return self._db

    def get_collection(self, name: str):
        """Get a collection by name."""
        return self.get_database()[name]
