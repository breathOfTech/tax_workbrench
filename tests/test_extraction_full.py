"""Full extraction test — covers all fact types."""

import asyncio
import logging

from langchain_core.messages import HumanMessage

from agents.intake.graph import build_intake_graph
from libs.graph_runtime import ModelFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


TEST_MESSAGES = [
    # RSU vest
    "I had 500 shares of Google RSUs vest on June 15, 2025. The FMV was $178 per share. They withheld 200 shares for taxes, so I got 300 shares delivered.",

    # Dividend income
    "I received dividends from Vanguard Total Stock Market fund — $3,200 in ordinary dividends and $2,800 of that was qualified. They also withheld $320 in federal taxes.",

    # Rental income
    "My rental property at 456 Oak Ave brought in $3,500 per month in rent. It was rented for 11 months — we had it empty in January while doing repairs.",

    # Rental expenses
    "For the rental property I spent $4,500 on repairs, $2,200 on insurance, $1,800 on property management fees, and $3,600 on utilities.",

    # Dependent
    "We have two kids — Emma, born March 2018, she's our daughter. And Jake, born November 2020, he's our son. Both live with us full time.",

    # Estimated payments
    "I made quarterly estimated tax payments to the IRS — $5,000 each quarter in April, June, September, and January. I also paid $2,000 per quarter to California FTB.",

    # California adjustment — HSA
    "I contributed $4,150 to my HSA through my employer. I know California doesn't allow the HSA deduction so that's an addition on my CA return.",

    # California adjustment — bonus depreciation
    "I took $15,000 in bonus depreciation on the rental appliances for federal, but California doesn't allow that so it's zero for CA purposes.",
]


async def test_all_extractions():
    """Run extraction against all fact type scenarios."""
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

        # Print extracted facts
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
        else:
            print("\n  *** NO FACTS EXTRACTED — POTENTIAL ISSUE ***")

    print(f"\n{'='*70}")
    print("DONE — all scenarios tested.")


if __name__ == "__main__":
    asyncio.run(test_all_extractions())
