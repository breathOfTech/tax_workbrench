"""Test fact accumulation across multiple turns."""

import asyncio
import logging

from langchain_core.messages import HumanMessage

from agents.intake.graph import build_intake_graph
from libs.graph_runtime import ModelFactory

logging.basicConfig(level=logging.INFO)


async def main():
    mf = ModelFactory()
    mf.initialize()
    g = build_intake_graph(mf)

    # Turn 1
    r1 = await g.ainvoke({
        "messages": [HumanMessage(content="I work at Google making $185,000 a year")],
        "extracted_facts": [],
    })
    print(f"\nTurn 1 facts: {len(r1['extracted_facts'])}")
    for f in r1["extracted_facts"]:
        print(f"  - {f['fact_type']}")

    # Turn 2 — pass accumulated facts from turn 1
    r2 = await g.ainvoke({
        "messages": [HumanMessage(content="My mortgage interest was $28,000 with Wells Fargo")],
        "extracted_facts": r1["extracted_facts"],
    })
    print(f"\nTurn 2 facts (accumulated): {len(r2['extracted_facts'])}")
    for f in r2["extracted_facts"]:
        print(f"  - {f['fact_type']}")


if __name__ == "__main__":
    asyncio.run(main())
