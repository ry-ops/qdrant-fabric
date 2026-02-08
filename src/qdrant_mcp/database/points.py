"""Point management tools for Qdrant Database API."""

from typing import Any

from mcp.server import Server

from .client import QdrantDatabaseClient


async def upsert_points(
    client: QdrantDatabaseClient, collection_name: str, points: list[dict[str, Any]]
) -> dict[str, Any]:
    """Upsert (insert or update) points in a collection.

    Args:
        collection_name: Name of the collection
        points: List of points to upsert

    Returns:
        Upsert operation result
    """
    return await client.put(f"/collections/{collection_name}/points", json={"points": points})


async def get_points(
    client: QdrantDatabaseClient, collection_name: str, ids: list[Any]
) -> dict[str, Any]:
    """Retrieve points by their IDs.

    Args:
        collection_name: Name of the collection
        ids: List of point IDs to retrieve

    Returns:
        Retrieved points
    """
    return await client.post(f"/collections/{collection_name}/points", json={"ids": ids})


async def get_point(
    client: QdrantDatabaseClient, collection_name: str, point_id: Any
) -> dict[str, Any]:
    """Retrieve a single point by ID.

    Args:
        collection_name: Name of the collection
        point_id: ID of the point to retrieve

    Returns:
        Retrieved point
    """
    return await client.get(f"/collections/{collection_name}/points/{point_id}")


async def delete_points(
    client: QdrantDatabaseClient, collection_name: str, points: list[Any]
) -> dict[str, Any]:
    """Delete points from a collection.

    Args:
        collection_name: Name of the collection
        points: List of point IDs to delete

    Returns:
        Deletion result
    """
    return await client.post(
        f"/collections/{collection_name}/points/delete", json={"points": points}
    )


async def count_points(
    client: QdrantDatabaseClient, collection_name: str, filter_: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Count points in a collection, optionally with a filter.

    Args:
        collection_name: Name of the collection
        filter_: Optional filter to apply

    Returns:
        Point count
    """
    body = {"exact": True}
    if filter_:
        body["filter"] = filter_
    return await client.post(f"/collections/{collection_name}/points/count", json=body)


async def scroll_points(
    client: QdrantDatabaseClient,
    collection_name: str,
    limit: int = 10,
    offset: Any | None = None,
    filter_: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Scroll through points in a collection.

    Args:
        collection_name: Name of the collection
        limit: Maximum number of points to return
        offset: Scroll offset (point ID or numeric offset)
        filter_: Optional filter to apply

    Returns:
        Scrolled points and next offset
    """
    body: dict[str, Any] = {"limit": limit, "with_payload": True, "with_vector": False}
    if offset is not None:
        body["offset"] = offset
    if filter_:
        body["filter"] = filter_
    return await client.post(f"/collections/{collection_name}/points/scroll", json=body)


async def batch_update(
    client: QdrantDatabaseClient, collection_name: str, operations: list[dict[str, Any]]
) -> dict[str, Any]:
    """Perform multiple update operations in a single request.

    Args:
        collection_name: Name of the collection
        operations: List of operations to perform (upsert, delete, set_payload, etc.)

    Returns:
        Batch operation result
    """
    return await client.post(
        f"/collections/{collection_name}/points/batch", json={"operations": operations}
    )


def register_point_tools(server: Server, client: QdrantDatabaseClient, tools_list: list) -> None:
    """Register point management tools with MCP server.

    Args:
        server: MCP server instance
        client: Qdrant database client
        tools_list: List to append tool definitions to
    """
    from mcp.types import Tool

    # Define tools
    tools_list.extend([
        Tool(
            name="qdrant_db_points_upsert",
            description="Upsert (insert or update) points in a collection",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "points": {"type": "array", "items": {"type": "object"}},
                },
                "required": ["collection_name", "points"],
            },
        ),
        Tool(
            name="qdrant_db_points_get",
            description="Retrieve multiple points by their IDs",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "ids": {"type": "array"},
                },
                "required": ["collection_name", "ids"],
            },
        ),
        Tool(
            name="qdrant_db_points_get_single",
            description="Retrieve a single point by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "point_id": {"type": ["string", "integer"]},
                },
                "required": ["collection_name", "point_id"],
            },
        ),
        Tool(
            name="qdrant_db_points_delete",
            description="Delete points from a collection",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "points": {"type": "array"},
                },
                "required": ["collection_name", "points"],
            },
        ),
        Tool(
            name="qdrant_db_points_count",
            description="Count points in a collection with optional filter",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "filter": {"type": "object"},
                },
                "required": ["collection_name"],
            },
        ),
        Tool(
            name="qdrant_db_points_scroll",
            description="Scroll through points in a collection",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                    "offset": {"type": ["string", "integer", "null"]},
                    "filter": {"type": "object"},
                },
                "required": ["collection_name"],
            },
        ),
        Tool(
            name="qdrant_db_points_batch",
            description="Perform multiple point operations in a single request",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "operations": {"type": "array", "items": {"type": "object"}},
                },
                "required": ["collection_name", "operations"],
            },
        ),
    ])

    @server.call_tool()
    async def qdrant_db_points_upsert(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Upsert (insert or update) points in a collection.

        Args:
            collection_name: Name of the collection
            points: List of points with id, vector, and optional payload
        """
        result = await upsert_points(
            client, arguments["collection_name"], arguments["points"]
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_points_get(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Retrieve multiple points by their IDs.

        Args:
            collection_name: Name of the collection
            ids: List of point IDs to retrieve
        """
        result = await get_points(client, arguments["collection_name"], arguments["ids"])
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_points_get_single(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Retrieve a single point by ID.

        Args:
            collection_name: Name of the collection
            point_id: ID of the point to retrieve
        """
        result = await get_point(client, arguments["collection_name"], arguments["point_id"])
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_points_delete(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Delete points from a collection.

        Args:
            collection_name: Name of the collection
            points: List of point IDs to delete
        """
        result = await delete_points(client, arguments["collection_name"], arguments["points"])
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_points_count(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Count points in a collection with optional filter.

        Args:
            collection_name: Name of the collection
            filter: Optional filter conditions
        """
        filter_ = arguments.get("filter")
        result = await count_points(client, arguments["collection_name"], filter_)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_points_scroll(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Scroll through points in a collection.

        Args:
            collection_name: Name of the collection
            limit: Maximum number of points to return (default: 10)
            offset: Scroll offset (optional)
            filter: Optional filter conditions
        """
        result = await scroll_points(
            client,
            arguments["collection_name"],
            arguments.get("limit", 10),
            arguments.get("offset"),
            arguments.get("filter"),
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_points_batch(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Perform multiple update operations in a single batch request.

        Allows you to combine multiple operations (upsert, delete, set_payload, etc.)
        into a single atomic request for better performance.

        Args:
            collection_name: Name of the collection
            operations: List of operations to perform
        """
        result = await batch_update(
            client, arguments["collection_name"], arguments["operations"]
        )
        return [{"type": "text", "text": str(result)}]
