"""Main MCP server for Qdrant APIs."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

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

# Global list to track registered tools
REGISTERED_TOOLS: list[Tool] = []


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

    # Register database tools if configured
    if config.validate_database_config():
        logger.info("Initializing Qdrant Database API tools")
        db_client = QdrantDatabaseClient(
            base_url=config.url,  # type: ignore
            api_key=config.api_key,  # type: ignore
        )

        register_collection_tools(server, db_client, REGISTERED_TOOLS)
        register_point_tools(server, db_client, REGISTERED_TOOLS)
        register_search_tools(server, db_client, REGISTERED_TOOLS)
        register_payload_tools(server, db_client, REGISTERED_TOOLS)
        register_health_tools(server, db_client, REGISTERED_TOOLS)
        register_vector_tools(server, db_client, REGISTERED_TOOLS)
        register_index_tools(server, db_client, REGISTERED_TOOLS)
        logger.info("Registered 30 database tools (Phase 1 complete)")
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
