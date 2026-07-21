"""Conversation routes."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from libs.graph_runtime import BaseConversationService
from libs.models.conversation import Conversation


router = APIRouter(prefix="/conversations", tags=["conversations"])


class CreateConversationRequest(BaseModel):
    content: str


class UpdateConversationRequest(BaseModel):
    content: str


def _get_service(request: Request) -> BaseConversationService:
    """Resolve conversation service from DI container."""
    return request.app.state.container.get(BaseConversationService)


@router.post("/", response_model=Conversation)
async def create_conversation(request: Request, body: CreateConversationRequest):
    """Create a new conversation and run the agent."""
    service = _get_service(request)
    return await service.create_conversation(body.content)


@router.post("/{conversation_id}", response_model=Conversation)
async def update_conversation(
    request: Request, conversation_id: str, body: UpdateConversationRequest
):
    """Send a follow-up message (non-streaming)."""
    service = _get_service(request)
    try:
        return await service.send_message(conversation_id, body.content)
    except ValueError:
        raise HTTPException(status_code=404, detail="Conversation not found")


@router.post("/{conversation_id}/stream")
async def stream_conversation(
    request: Request, conversation_id: str, body: UpdateConversationRequest
):
    """Send a message and stream the response via SSE."""
    service = _get_service(request)

    conversation = await service.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    async def event_stream():
        async for chunk in service.stream_response(conversation_id, body.content):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(request: Request, conversation_id: str):
    """Retrieve a conversation by ID."""
    service = _get_service(request)
    conversation = await service.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.get("/", response_model=list[Conversation])
async def list_conversations(request: Request):
    """List all conversations."""
    service = _get_service(request)
    return await service.list_conversations()


@router.delete("/{conversation_id}")
async def delete_conversation(request: Request, conversation_id: str):
    """Delete a conversation."""
    service = _get_service(request)
    deleted = await service.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted"}
