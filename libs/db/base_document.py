"""Base document model with common fields.

All MongoDB documents inherit from this to get consistent
bookkeeping (id, timestamps) without manual wiring.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return str(uuid4())


class BaseDocument(BaseModel):
    """Base class for all MongoDB documents.

    Provides:
    - Auto-generated UUID id
    - created_at / updated_at timestamps
    - to_mongo / from_mongo conversion
    """

    id: str = Field(default_factory=_new_id)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    model_config = {"populate_by_name": True}

    def to_mongo(self) -> dict[str, Any]:
        """Convert to MongoDB document with _id field."""
        data = self.model_dump()
        data["_id"] = data.pop("id")
        return data

    @classmethod
    def from_mongo(cls, data: dict[str, Any]) -> "BaseDocument":
        """Create instance from MongoDB document."""
        if data is None:
            return None
        if "_id" in data:
            data["id"] = data.pop("_id")
        return cls(**data)
