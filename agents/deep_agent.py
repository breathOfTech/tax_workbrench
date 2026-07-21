"""Deep Agent provider — main orchestrator using deepagents harness."""

from langgraph.graph.state import CompiledStateGraph

from deepagents import create_deep_agent, SubAgent

from agents.general.prompt import GENERAL_PROMPT
from agents.intake.prompt import INTAKE_PROMPT
from agents.prompt import MAIN_AGENT_PROMPT
from agents.tools import create_extract_facts_tool, get_collected_facts, save_extracted_facts
from libs.graph_runtime import CachingGraphProvider, ModelFactory, ModelSettings


class DeepAgentProvider(CachingGraphProvider):
    """Builds a Deep Agent with intake and general subagents."""

    def __init__(self, model_factory: ModelFactory) -> None:
        super().__init__()
        self._model_factory = model_factory

    async def build_graph(self) -> CompiledStateGraph:
        main_model = self._model_factory.create(ModelSettings(temperature=0.3))
        intake_model = self._model_factory.create(ModelSettings(temperature=0.0))
        general_model = self._model_factory.create(ModelSettings(temperature=0.2))

        extraction_llm = self._model_factory.create(ModelSettings(temperature=0.0))
        extract_facts = create_extract_facts_tool(extraction_llm)

        agent = create_deep_agent(
            model=main_model,
            system_prompt=MAIN_AGENT_PROMPT,
            tools=[get_collected_facts],
            subagents=[
                SubAgent(
                    name="intake",
                    description=(
                        "Extract and store structured tax facts from user messages. "
                        "Use when the user shares personal or financial information "
                        "(income, deductions, assets, dependents, filing status, life events). "
                        "The intake agent will extract facts, classify them as create/update/replace, "
                        "and confirm back to the user."
                    ),
                    system_prompt=INTAKE_PROMPT,
                    model=intake_model,
                    tools=[extract_facts, save_extracted_facts, get_collected_facts],
                ),
                SubAgent(
                    name="general",
                    description=(
                        "Answer questions about U.S. tax concepts, rules, and strategies. "
                        "Use when the user is asking questions, seeking explanations, "
                        "or wants clarification about tax topics."
                    ),
                    system_prompt=GENERAL_PROMPT,
                    model=general_model,
                ),
            ],
        )

        return agent
