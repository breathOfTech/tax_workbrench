"""Chainlit chat UI — streams responses from the deep agent graph."""

import logging

import chainlit as cl
from langchain_core.messages import AIMessage, HumanMessage

from agents.deep_agent import DeepAgentProvider
from libs.config import load_settings
from libs.graph_runtime import ModelFactory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
    force=True,
)

# Load settings and initialize
load_settings("app/settings.yaml")

model_factory = ModelFactory()
model_factory.initialize()

graph_provider = DeepAgentProvider(model_factory)


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming user message — stream the agent response."""
    graph = await graph_provider.get_graph()

    # Build message history from Chainlit session
    history = cl.user_session.get("history", [])
    history.append(HumanMessage(content=message.content))

    # Stream response
    response = cl.Message(content="")
    await response.send()

    full_content = ""
    async for event in graph.astream_events(
        {"messages": history}, version="v2"
    ):
        if event.get("event") == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk and hasattr(chunk, "content") and chunk.content:
                content = chunk.content
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            await response.stream_token(block["text"])
                            full_content += block["text"]
                        elif isinstance(block, str):
                            await response.stream_token(block)
                            full_content += block
                else:
                    await response.stream_token(content)
                    full_content += content

    await response.update()

    # Store history for multi-turn conversation
    history.append(AIMessage(content=full_content))
    cl.user_session.set("history", history)
