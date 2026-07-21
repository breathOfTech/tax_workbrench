"""Test fact extraction from the intake agent."""

import asyncio
import logging

from langchain_core.messages import HumanMessage

from agents.intake.graph import build_intake_graph
from libs.graph_runtime import ModelFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_extraction():
    """Run extraction against sample messages and print results."""
    model_factory = ModelFactory()
    model_factory.initialize()

    intake_graph = build_intake_graph(model_factory)

    test_messages = [
        "Hi, I'm John Smith. I live in California and work as a software engineer at Google.",
        "My W-2 from Google shows $185,000 in gross wages. They withheld $42,000 in federal taxes and $15,000 in state taxes. I also contributed $23,500 to my 401k.",
        "I'm married filing jointly. My wife Sarah works at Apple and made about $120,000.",
        "We sold 200 shares of Google stock in March 2025 for $175 per share. I originally got them as RSUs that vested at $140 per share in 2023.",
        "Our mortgage with Wells Fargo — we paid $28,000 in interest this year. Property taxes were $12,500.",
        "How's the weather today?",
    ]

    for msg in test_messages:
        print(f"\n{'='*70}")
        print(f"USER: {msg}")
        print(f"{'='*70}")

        result = await intake_graph.ainvoke({
            "messages": [HumanMessage(content=msg)],
            "extracted_facts": [],
        })

        # Print agent response
        ai_msg = result["messages"][-1]
        content = ai_msg.content
        if isinstance(content, list):
            content = "".join(
                block["text"] if isinstance(block, dict) else str(block)
                for block in content
            )
        print(f"\nAGENT: {content[:200]}...")

        # Print extracted facts
        facts = result.get("extracted_facts", [])
        if facts:
            print(f"\nEXTRACTED FACTS ({len(facts)}):")
            for i, fact in enumerate(facts, 1):
                print(f"  {i}. [{fact['fact_type']}] confidence={fact['confidence']}")
                print(f"     quote: \"{fact['source_quote'][:80]}\"")
                # Print key fields
                skip_keys = {"fact_type", "confidence", "source_quote"}
                for k, v in fact.items():
                    if k not in skip_keys and v is not None and v is not False:
                        print(f"     {k}: {v}")
        else:
            print("\n  No facts extracted.")


if __name__ == "__main__":
    asyncio.run(test_extraction())
