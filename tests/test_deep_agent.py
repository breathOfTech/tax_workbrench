"""Test the Deep Agent — end-to-end conversation flow."""

import asyncio
import logging

from agents.deep_agent import DeepAgentProvider
from libs.graph_runtime import ModelFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_deep_agent():
    mf = ModelFactory()
    mf.initialize()
    provider = DeepAgentProvider(mf)
    graph = await provider.build_graph()

    test_messages = [
        # Intake — should delegate to intake subagent
        "Hi, I'm John Smith. I work at Google making $185,000 a year and live in California.",
        # General — should delegate to general subagent
        "What's the standard deduction for married filing jointly in 2025?",
        # Intake — correction
        "Actually my salary is $192,000, I just checked my W-2.",
    ]

    for msg in test_messages:
        print(f"\n{'='*70}")
        print(f"USER: {msg}")
        print(f"{'='*70}")

        result = await graph.ainvoke({
            "messages": [{"role": "user", "content": msg}],
        })

        # Get the last AI message
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
            if isinstance(content, list):
                content = "".join(
                    block["text"] if isinstance(block, dict) else str(block)
                    for block in content
                )
            print(f"\nAGENT: {content[:300]}")
        else:
            print("\n  No response")


if __name__ == "__main__":
    asyncio.run(test_deep_agent())
