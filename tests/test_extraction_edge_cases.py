"""Edge case extraction tests — multi-fact, ambiguous, and tricky scenarios."""

import asyncio
import logging

from langchain_core.messages import HumanMessage

from agents.intake.graph import build_intake_graph
from libs.graph_runtime import ModelFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


TEST_MESSAGES = [
    # --- Multi W-2: two employers in one message ---
    "I worked at Google until June making $95,000, then switched to Meta where I made $110,000 for the rest of the year. Google withheld $22,000 federal and Meta withheld $26,000 federal.",

    # --- Spouse W-2 with different state ---
    "My wife Sarah earned $145,000 at Apple in Cupertino, CA. She had $35,000 federal withheld, $12,000 CA state tax withheld, and contributed $23,500 to her 401k. She also had $4,200 in RSU income included on her W-2.",

    # --- Multiple RSU vests same company, different dates ---
    "I had three Google RSU vests in 2025: 100 shares on Feb 15 at $165/share, 150 shares on May 15 at $172/share, and 100 shares on Aug 15 at $180/share.",

    # --- Short-term vs long-term stock sales in same message ---
    "I sold two lots of stock. First, 50 shares of Apple I bought in January 2025 and sold in March 2025 for $12,000 — that's short term. Second, 100 shares of Microsoft I held since 2021 that I sold for $45,000 with a cost basis of $28,000.",

    # --- Rental property with both income and expenses together ---
    "The rental at 789 Elm St brought in $42,000 for the year, rented all 12 months. I spent $8,500 on the mortgage interest for that property, $3,200 on repairs, and $4,800 on property taxes.",

    # --- Ambiguous / low-confidence (vague amounts) ---
    "I think I made somewhere around six figures at my job, maybe like 100 or 110k? I'm not sure exactly, I haven't looked at my W-2 yet.",

    # --- Multiple dependents with different credit eligibility ---
    "We have three kids: Tyler age 16, Madison age 19 who's in college, and baby Oliver born December 2024. My mother-in-law Patricia also lives with us — she's 72 and has no income.",

    # --- Two properties: primary residence + rental mortgage ---
    "We pay mortgage interest on two properties. Our primary home with Chase — $32,000 in interest on a $650,000 loan. The rental property mortgage with US Bank — $14,000 in interest on a $320,000 loan.",

    # --- Wash sale scenario ---
    "I sold 100 shares of Tesla at a loss in November — bought at $250, sold at $180. Then I bought back 100 shares of Tesla two weeks later at $185.",

    # --- CA adjustment with multiple items ---
    "For California, I need to add back my $4,150 HSA deduction and also $8,000 in bonus depreciation from the rental. And I can subtract $2,400 in out-of-state municipal bond interest that California doesn't tax.",
]


async def test_edge_cases():
    """Run extraction against edge case scenarios."""
    model_factory = ModelFactory()
    model_factory.initialize()

    intake_graph = build_intake_graph(model_factory)

    for msg in TEST_MESSAGES:
        print(f"\n{'='*70}")
        print(f"USER: {msg}")
        print(f"{'='*70}")

        result = await intake_graph.ainvoke({
            "messages": [HumanMessage(content=msg)],
            "extracted_facts": [],
        })

        facts = result.get("extracted_facts", [])
        if facts:
            print(f"\nEXTRACTED FACTS ({len(facts)}):")
            for i, fact in enumerate(facts, 1):
                print(f"  {i}. [{fact['fact_type']}] confidence={fact['confidence']}")
                print(f"     quote: \"{fact['source_quote'][:80]}\"")
                skip_keys = {"fact_type", "confidence", "source_quote"}
                for k, v in fact.items():
                    if k not in skip_keys and v is not None and v is not False:
                        print(f"     {k}: {v}")
                print()
        else:
            print("\n  *** NO FACTS EXTRACTED ***")

    print(f"\n{'='*70}")
    print("DONE — edge cases tested.")


if __name__ == "__main__":
    asyncio.run(test_edge_cases())
