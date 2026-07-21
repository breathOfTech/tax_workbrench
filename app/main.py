"""Tax Agent — FastAPI application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from libs.config import load_settings
from libs.db.connection import MongoManager
from app.container import create_container
from app.routes.conversations import router as conversations_router


SETTINGS_PATH = Path(__file__).parent / "settings.yaml"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown."""
    # Startup
    load_settings(SETTINGS_PATH)
    container = create_container()
    app.state.container = container

    # Connect MongoDB
    mongo_manager = container.get(MongoManager)
    await mongo_manager.connect()

    yield

    # Shutdown
    await mongo_manager.disconnect()


app = FastAPI(
    title="Tax Workbench",
    description="Agentic tax planning workspace for U.S. individual tax scenarios",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(conversations_router, prefix="/v1")
