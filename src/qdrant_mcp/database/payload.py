"""Payload management tools for Qdrant Database API."""

from typing import Any

from mcp.server import Server

from .client import QdrantDatabaseClient


async def set_payload(
    client: QdrantDatabaseClient,
    collection_name: str,
    payload: dict[str, Any],
    points: list[Any],
) -> dict[str, Any]:
    """Set payload for specified points (merges with existing payload).

    Args:
        collection_name: Name of the collection
        payload: Payload data to set
        points: List of point IDs to update

    Returns:
        Operation result
    """
    return await client.post(
        f"/collections/{collection_name}/points/payload",
        json={"payload": payload, "points": points},
    )


async def overwrite_payload(
    client: QdrantDatabaseClient,
    collection_name: str,
    payload: dict[str, Any],
    points: list[Any],
) -> dict[str, Any]:
    """Overwrite payload for specified points (replaces existing payload).

    Args:
        collection_name: Name of the collection
        payload: Payload data to set
        points: List of point IDs to update

    Returns:
        Operation result
    """
    return await client.put(
        f"/collections/{collection_name}/points/payload",
        json={"payload": payload, "points": points},
    )


async def delete_payload(
    client: QdrantDatabaseClient,
    collection_name: str,
    keys: list[str],
    points: list[Any],
) -> dict[str, Any]:
    """Delete specific payload fields from points.

    Args:
        collection_name: Name of the collection
        keys: List of payload keys to delete
        points: List of point IDs to update

    Returns:
        Operation result
    """
    return await client.post(
        f"/collections/{collection_name}/points/payload/delete",
        json={"keys": keys, "points": points},
    )


async def clear_payload(
    client: QdrantDatabaseClient, collection_name: str, points: list[Any]
) -> dict[str, Any]:
    """Clear all payload data from specified points.

    Args:
        collection_name: Name of the collection
        points: List of point IDs to clear

    Returns:
        Operation result
    """
    return await client.post(
        f"/collections/{collection_name}/points/payload/clear", json={"points": points}
    )


def register_payload_tools(server: Server, client: QdrantDatabaseClient, tools_list: list) -> None:
    """Register payload management tools with MCP server.

    Args:
        server: MCP server instance
        client: Qdrant database client
        tools_list: List to append tool definitions to
    """
    from mcp.types import Tool

    # Define tools
    tools_list.extend([
        Tool(
            name="qdrant_db_payload_set",
            description="Set payload for specified points (merges with existing)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "payload": {"type": "object"},
                    "points": {"type": "array"},
                },
                "required": ["collection_name", "payload", "points"],
            },
        ),
        Tool(
            name="qdrant_db_payload_overwrite",
            description="Overwrite payload for specified points (replaces existing)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "payload": {"type": "object"},
                    "points": {"type": "array"},
                },
                "required": ["collection_name", "payload", "points"],
            },
        ),
        Tool(
            name="qdrant_db_payload_delete",
            description="Delete specific payload fields from points",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "keys": {"type": "array", "items": {"type": "string"}},
                    "points": {"type": "array"},
                },
                "required": ["collection_name", "keys", "points"],
            },
        ),
        Tool(
            name="qdrant_db_payload_clear",
            description="Clear all payload from specified points",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "points": {"type": "array"},
                },
                "required": ["collection_name", "points"],
            },
        ),
    ])

    @server.call_tool()
    async def qdrant_db_payload_set(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Set payload for specified points (merges with existing payload).

        Args:
            collection_name: Name of the collection
            payload: Payload data to set
            points: List of point IDs to update
        """
        result = await set_payload(
            client,
            arguments["collection_name"],
            arguments["payload"],
            arguments["points"],
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_payload_overwrite(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Overwrite payload for specified points (replaces existing payload).

        Args:
            collection_name: Name of the collection
            payload: Payload data to set
            points: List of point IDs to update
        """
        result = await overwrite_payload(
            client,
            arguments["collection_name"],
            arguments["payload"],
            arguments["points"],
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_payload_delete(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Delete specific payload fields from points.

        Args:
            collection_name: Name of the collection
            keys: List of payload keys to delete
            points: List of point IDs to update
        """
        result = await delete_payload(
            client,
            arguments["collection_name"],
            arguments["keys"],
            arguments["points"],
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_payload_clear(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Clear all payload data from specified points.

        Args:
            collection_name: Name of the collection
            points: List of point IDs to clear
        """
        result = await clear_payload(
            client, arguments["collection_name"], arguments["points"]
        )
        return [{"type": "text", "text": str(result)}]
