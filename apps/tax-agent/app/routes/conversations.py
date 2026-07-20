"""Conversation routes."""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from tax_workbench.db.repositories.conversations import BaseConversationsRepository
from tax_workbench.models.conversation import (
    Conversation,
    ConversationMessage,
    ConversationState,
    MessageRole,
)


router = APIRouter(prefix="/conversations", tags=["conversations"])


class CreateConversationRequest(BaseModel):
    content: str


class UpdateConversationRequest(BaseModel):
    content: str


def _get_repository(request: Request) -> BaseConversationsRepository:
    """Resolve repository from DI container."""
    return request.app.state.container.get(BaseConversationsRepository)


@router.post("/", response_model=Conversation)
async def create_conversation(request: Request, body: CreateConversationRequest):
    """Create a new conversation and kick off graph execution."""
    repo = _get_repository(request)
    message = ConversationMessage(role=MessageRole.USER, content=body.content)
    conversation = Conversation(messages=[message], state=ConversationState.AGENT_EXECUTING)
    created = await repo.create(conversation)

    # TODO: Trigger supervisor graph execution here
    # For now, mark as open (no agent wired yet)
    return await repo.update_state(created.id, ConversationState.OPEN)


@router.post("/{conversation_id}", response_model=Conversation)
async def update_conversation(
    request: Request, conversation_id: str, body: UpdateConversationRequest
):
    """Send a follow-up message to an existing conversation."""
    repo = _get_repository(request)
    conversation = await repo.find_by_id(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    message = ConversationMessage(role=MessageRole.USER, content=body.content)
    updated = await repo.append_message(conversation_id, message)

    # TODO: Trigger supervisor graph execution here
    return updated


@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(request: Request, conversation_id: str):
    """Retrieve a conversation by ID."""
    repo = _get_repository(request)
    conversation = await repo.find_by_id(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.get("/", response_model=list[Conversation])
async def list_conversations(request: Request):
    """List all conversations."""
    repo = _get_repository(request)
    return await repo.find_all()


@router.delete("/{conversation_id}")
async def delete_conversation(request: Request, conversation_id: str):
    """Delete a conversation."""
    repo = _get_repository(request)
    deleted = await repo.delete(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted"}
