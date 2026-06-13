"""Main MCP server for Qdrant APIs."""

import asyncio
import logging
from contextlib import AsyncExitStack
from typing import Any, Awaitable, Callable

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .config import QdrantConfig
from .database import (
    QdrantDatabaseClient,
    register_collection_tools,
    register_health_tools,
    register_index_tools,
    register_payload_tools,
    register_point_tools,
    register_search_tools,
    register_vector_tools,
)

logger = logging.getLogger(__name__)

# Tool definitions advertised via list_tools().
REGISTERED_TOOLS: list[Tool] = []

# Maps a tool name to the async handler that executes it. The MCP SDK supports
# exactly ONE @server.call_tool() handler, so every tool is dispatched through
# the single handler below using this table.
ToolHandler = Callable[[dict[str, Any]], Awaitable[list[dict[str, Any]]]]
TOOL_HANDLERS: dict[str, ToolHandler] = {}


async def main() -> None:
    """Run the Qdrant MCP server."""
    # Load configuration
    config = QdrantConfig()

    # Initialize MCP server
    server = Server("qdrant-mcp")

    # List tools handler - returns all registered tools
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List all available tools."""
        return REGISTERED_TOOLS

    # Single dispatch handler. The SDK invokes this with (name, arguments) for
    # every tool call; we route to the matching handler in TOOL_HANDLERS.
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Dispatch a tool call to its registered handler."""
        handler = TOOL_HANDLERS.get(name)
        if handler is None:
            raise ValueError(f"Unknown tool: {name}")
        results = await handler(arguments or {})
        return [TextContent(type="text", text=item["text"]) for item in results]

    async with AsyncExitStack() as stack:
        # Register database tools if configured
        if config.validate_database_config():
            logger.info("Initializing Qdrant Database API tools")
            db_client = QdrantDatabaseClient(
                base_url=config.url,  # type: ignore[arg-type]
                api_key=config.api_key or "",
            )
            # Open the HTTP client for the lifetime of the server so handlers
            # can issue requests (otherwise client.client raises RuntimeError).
            await stack.enter_async_context(db_client)

            register_collection_tools(db_client, REGISTERED_TOOLS, TOOL_HANDLERS)
            register_point_tools(db_client, REGISTERED_TOOLS, TOOL_HANDLERS)
            register_search_tools(db_client, REGISTERED_TOOLS, TOOL_HANDLERS)
            register_payload_tools(db_client, REGISTERED_TOOLS, TOOL_HANDLERS)
            register_health_tools(db_client, REGISTERED_TOOLS, TOOL_HANDLERS)
            register_vector_tools(db_client, REGISTERED_TOOLS, TOOL_HANDLERS)
            register_index_tools(db_client, REGISTERED_TOOLS, TOOL_HANDLERS)
            logger.info("Registered %d database tools (Phase 1 complete)", len(REGISTERED_TOOLS))
        else:
            logger.warning("Database API not configured. Set QDRANT_URL and QDRANT_API_KEY")
            logger.info("Running with no tools registered")

        # Run server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())


def serve() -> None:
    """Entry point for running the server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    asyncio.run(main())


if __name__ == "__main__":
    serve()
