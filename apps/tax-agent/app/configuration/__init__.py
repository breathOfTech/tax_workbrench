"""Dependency injection configuration for the tax-agent app."""

from injector import Injector, Module, provider, singleton

from tax_workbench.db.connection import MongoManager
from tax_workbench.db.repositories.conversations import (
    BaseConversationsRepository,
    ConversationsRepository,
)


class AppModule(Module):
    """DI module — binds interfaces to implementations."""

    @singleton
    @provider
    def provide_mongo_manager(self) -> MongoManager:
        return MongoManager()

    @singleton
    @provider
    def provide_conversations_repository(
        self, mongo_manager: MongoManager
    ) -> BaseConversationsRepository:
        return ConversationsRepository(mongo_manager)


def create_container() -> Injector:
    """Create and configure the DI container."""
    return Injector([AppModule])
