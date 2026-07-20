"""Conversation document model."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from tax_workbench.db.base_document import BaseDocument, _utcnow


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationMessage(BaseModel):
    """A single message in a conversation thread."""

    role: MessageRole
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: _utcnow().isoformat())


class ConversationState(StrEnum):
    OPEN = "open"
    AGENT_EXECUTING = "agent_executing"
    CLOSED = "closed"


class Conversation(BaseDocument):
    """A conversation thread between user and the tax agent."""

    messages: list[ConversationMessage] = Field(default_factory=list)
    state: ConversationState = ConversationState.OPEN
