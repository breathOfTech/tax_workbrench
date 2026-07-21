"""Model factory — creates LLM instances with consistent configuration."""

import logging
from enum import Enum
from typing import Optional

from langchain_aws import ChatBedrockConverse
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel

from tax_workbench.config import get_setting

logger = logging.getLogger(__name__)


class ChatModel(Enum):
    ANTHROPIC_CLAUDE_HAIKU_4_5_V1_0 = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
    ANTHROPIC_CLAUDE_SONNET_4_V1_0 = "us.anthropic.claude-sonnet-4-20250514-v1:0"
    ANTHROPIC_CLAUDE_SONNET_4_5_V1_0 = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    ANTHROPIC_CLAUDE_OPUS_4_6_V1_0 = "us.anthropic.claude-opus-4-6-v1"


class ModelSettings(BaseModel):
    model: ChatModel = ChatModel.ANTHROPIC_CLAUDE_SONNET_4_5_V1_0
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class ModelFactory:
    """Creates LLM instances via AWS Bedrock.

    Singleton — instantiated once via DI, used across all agents and nodes.
    AWS credentials are picked up from the environment automatically.
    """

    def __init__(self) -> None:
        self.region: str = "us-east-1"
        self.default_model: ChatModel = ChatModel.ANTHROPIC_CLAUDE_SONNET_4_5_V1_0

    def initialize(self) -> None:
        """Load config from settings."""
        self.region = get_setting("llm.region", "us-east-1")
        model_id = get_setting("llm.default_model", None)
        if model_id:
            self.default_model = ChatModel(model_id)

    def create(self, model_settings: ModelSettings = ModelSettings()) -> BaseChatModel:
        """Create a ChatBedrockConverse instance."""
        model = model_settings.model or self.default_model

        logger.debug(f"[ModelFactory] Creating LLM model: {model.value}")
        logger.debug(f"[ModelFactory] Region: {self.region}")

        return ChatBedrockConverse(
            model=model.value,
            region_name=self.region,
            temperature=model_settings.temperature,
            max_tokens=model_settings.max_tokens,
        )
