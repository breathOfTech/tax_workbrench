"""Dependency injection configuration for the tax-agent app."""

from injector import Injector, Module, provider, singleton

from app.graph import TaxAgentGraphProvider
from tax_workbench.db.connection import MongoManager
from tax_workbench.db.repositories.conversations import (
    BaseConversationsRepository,
    ConversationsRepository,
)
from tax_workbench.lib.graph_runtime import (
    BaseConversationRunner,
    BaseConversationService,
    BaseGraphProvider,
    ConversationRunner,
    ConversationService,
    ModelFactory,
)


class AppModule(Module):
    """DI module — binds interfaces to implementations."""

    @singleton
    @provider
    def provide_mongo_manager(self) -> MongoManager:
        return MongoManager()

    @singleton
    @provider
    def provide_model_factory(self) -> ModelFactory:
        factory = ModelFactory()
        factory.initialize()
        return factory

    @singleton
    @provider
    def provide_conversations_repository(
        self, mongo_manager: MongoManager
    ) -> BaseConversationsRepository:
        return ConversationsRepository(mongo_manager)

    @singleton
    @provider
    def provide_graph_provider(self, model_factory: ModelFactory) -> BaseGraphProvider:
        return TaxAgentGraphProvider(model_factory)

    @singleton
    @provider
    def provide_conversation_runner(
        self, graph_provider: BaseGraphProvider
    ) -> BaseConversationRunner:
        return ConversationRunner(graph_provider)

    @singleton
    @provider
    def provide_conversation_service(
        self,
        repository: BaseConversationsRepository,
        runner: BaseConversationRunner,
    ) -> BaseConversationService:
        return ConversationService(repository, runner)


def create_container() -> Injector:
    """Create and configure the DI container."""
    return Injector([AppModule])
