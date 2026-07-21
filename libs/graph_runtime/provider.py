"""Graph provider — abstract base and caching implementation.

BaseGraphProvider defines the contract for building compiled LangGraph graphs.
CachingGraphProvider adds TTL-based caching so the graph isn't recompiled on every request.
"""

import asyncio
import time
from abc import ABC, abstractmethod

from langgraph.graph.state import CompiledStateGraph


class BaseGraphProvider(ABC):
    """Abstract base for providing compiled LangGraph graphs."""

    @abstractmethod
    async def build_graph(self) -> CompiledStateGraph:
        """Build and compile the graph. Called when cache expires or on first use."""
        ...


class CachingGraphProvider(BaseGraphProvider):
    """Caches the compiled graph with a configurable TTL.

    Subclass this and implement `build_graph()`. The compiled graph
    is cached and reused until the TTL expires, then rebuilt.

    Thread-safe via asyncio.Lock.
    """

    cache_ttl_seconds: float = 300.0  # 5 minutes

    def __init__(self) -> None:
        self._graph: CompiledStateGraph | None = None
        self._built_at: float = 0.0
        self._lock = asyncio.Lock()

    async def get_graph(self) -> CompiledStateGraph:
        """Get the compiled graph, rebuilding if cache has expired."""
        now = time.time()
        if self._graph is not None and (now - self._built_at) < self.cache_ttl_seconds:
            return self._graph

        async with self._lock:
            # Double-check after acquiring lock
            now = time.time()
            if self._graph is not None and (now - self._built_at) < self.cache_ttl_seconds:
                return self._graph

            self._graph = await self.build_graph()
            self._built_at = time.time()
            return self._graph
