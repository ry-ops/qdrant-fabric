"""Collection management tools for Qdrant Database API."""

from typing import Any

from mcp.server import Server
from mcp.types import Tool

from .client import QdrantDatabaseClient


async def list_collections(client: QdrantDatabaseClient) -> dict[str, Any]:
    """List all collections in the database.

    Returns:
        Dictionary containing collection list and metadata
    """
    return await client.get("/collections")


async def get_collection(client: QdrantDatabaseClient, collection_name: str) -> dict[str, Any]:
    """Get detailed information about a specific collection.

    Args:
        collection_name: Name of the collection

    Returns:
        Collection configuration and statistics
    """
    return await client.get(f"/collections/{collection_name}")


async def create_collection(
    client: QdrantDatabaseClient, collection_name: str, config: dict[str, Any]
) -> dict[str, Any]:
    """Create a new collection with specified configuration.

    Args:
        collection_name: Name for the new collection
        config: Collection configuration (vectors, distance metric, etc.)

    Returns:
        Creation result
    """
    return await client.put(f"/collections/{collection_name}", json=config)


async def delete_collection(client: QdrantDatabaseClient, collection_name: str) -> dict[str, Any]:
    """Delete a collection and all its data.

    Args:
        collection_name: Name of the collection to delete

    Returns:
        Deletion result
    """
    return await client.delete(f"/collections/{collection_name}")


async def update_collection(
    client: QdrantDatabaseClient, collection_name: str, updates: dict[str, Any]
) -> dict[str, Any]:
    """Update collection configuration.

    Args:
        collection_name: Name of the collection
        updates: Configuration updates to apply

    Returns:
        Update result
    """
    return await client.patch(f"/collections/{collection_name}", json=updates)


async def collection_exists(client: QdrantDatabaseClient, collection_name: str) -> dict[str, Any]:
    """Check if a collection exists.

    Args:
        collection_name: Name of the collection

    Returns:
        Existence check result
    """
    return await client.get(f"/collections/{collection_name}/exists")


def register_collection_tools(server: Server, client: QdrantDatabaseClient) -> None:
    """Register collection management tools with MCP server.

    Args:
        server: MCP server instance
        client: Qdrant database client
    """

    @server.call_tool()
    async def qdrant_db_collections_list(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """List all collections in the Qdrant database.

        Returns a list of all collections with their configurations.
        """
        result = await list_collections(client)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_collections_get(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Get detailed information about a specific collection.

        Args:
            collection_name: Name of the collection to retrieve
        """
        collection_name = arguments["collection_name"]
        result = await get_collection(client, collection_name)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_collections_create(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Create a new collection with specified configuration.

        Args:
            collection_name: Name for the new collection
            vectors: Vector configuration (size, distance metric)
            Additional optional parameters for collection configuration
        """
        collection_name = arguments["collection_name"]
        # Remove collection_name from arguments to get config
        config = {k: v for k, v in arguments.items() if k != "collection_name"}
        result = await create_collection(client, collection_name, config)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_collections_delete(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Delete a collection and all its data.

        Args:
            collection_name: Name of the collection to delete
        """
        collection_name = arguments["collection_name"]
        result = await delete_collection(client, collection_name)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_collections_update(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Update collection configuration.

        Args:
            collection_name: Name of the collection
            Updates to apply to the collection configuration
        """
        collection_name = arguments["collection_name"]
        updates = {k: v for k, v in arguments.items() if k != "collection_name"}
        result = await update_collection(client, collection_name, updates)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_collections_exists(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Check if a collection exists.

        Args:
            collection_name: Name of the collection to check
        """
        collection_name = arguments["collection_name"]
        result = await collection_exists(client, collection_name)
        return [{"type": "text", "text": str(result)}]

    # Register tool definitions
    server.list_tools = lambda: [
        Tool(
            name="qdrant_db_collections_list",
            description="List all collections in the Qdrant database",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="qdrant_db_collections_get",
            description="Get detailed information about a specific collection",
            inputSchema={
                "type": "object",
                "properties": {"collection_name": {"type": "string"}},
                "required": ["collection_name"],
            },
        ),
        Tool(
            name="qdrant_db_collections_create",
            description="Create a new collection",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "vectors": {"type": "object"},
                },
                "required": ["collection_name", "vectors"],
            },
        ),
        Tool(
            name="qdrant_db_collections_delete",
            description="Delete a collection",
            inputSchema={
                "type": "object",
                "properties": {"collection_name": {"type": "string"}},
                "required": ["collection_name"],
            },
        ),
        Tool(
            name="qdrant_db_collections_update",
            description="Update collection configuration",
            inputSchema={
                "type": "object",
                "properties": {"collection_name": {"type": "string"}},
                "required": ["collection_name"],
            },
        ),
        Tool(
            name="qdrant_db_collections_exists",
            description="Check if a collection exists",
            inputSchema={
                "type": "object",
                "properties": {"collection_name": {"type": "string"}},
                "required": ["collection_name"],
            },
        ),
    ]
