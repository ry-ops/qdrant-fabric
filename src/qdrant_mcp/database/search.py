"""Vector search tools for Qdrant Database API."""

from typing import Any

from mcp.server import Server

from .client import QdrantDatabaseClient


async def search_points(
    client: QdrantDatabaseClient,
    collection_name: str,
    vector: list[float],
    limit: int = 10,
    filter_: dict[str, Any] | None = None,
    with_payload: bool = True,
    with_vector: bool = False,
) -> dict[str, Any]:
    """Search for similar vectors in a collection.

    Args:
        collection_name: Name of the collection
        vector: Query vector
        limit: Maximum number of results
        filter_: Optional filter conditions
        with_payload: Include payload in results
        with_vector: Include vectors in results

    Returns:
        Search results with scores
    """
    body: dict[str, Any] = {
        "vector": vector,
        "limit": limit,
        "with_payload": with_payload,
        "with_vector": with_vector,
    }
    if filter_:
        body["filter"] = filter_
    return await client.post(f"/collections/{collection_name}/points/search", json=body)


async def search_batch_points(
    client: QdrantDatabaseClient, collection_name: str, searches: list[dict[str, Any]]
) -> dict[str, Any]:
    """Perform multiple search queries in a single request.

    Args:
        collection_name: Name of the collection
        searches: List of search queries

    Returns:
        Batch search results
    """
    return await client.post(
        f"/collections/{collection_name}/points/search/batch", json={"searches": searches}
    )


async def recommend_points(
    client: QdrantDatabaseClient,
    collection_name: str,
    positive: list[Any],
    negative: list[Any] | None = None,
    limit: int = 10,
    filter_: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Get recommendations based on positive and negative examples.

    Args:
        collection_name: Name of the collection
        positive: List of positive example point IDs
        negative: List of negative example point IDs
        limit: Maximum number of results
        filter_: Optional filter conditions

    Returns:
        Recommended points
    """
    body: dict[str, Any] = {"positive": positive, "limit": limit}
    if negative:
        body["negative"] = negative
    if filter_:
        body["filter"] = filter_
    return await client.post(f"/collections/{collection_name}/points/recommend", json=body)


async def recommend_batch_points(
    client: QdrantDatabaseClient, collection_name: str, searches: list[dict[str, Any]]
) -> dict[str, Any]:
    """Perform multiple recommendation queries in a single request.

    Args:
        collection_name: Name of the collection
        searches: List of recommendation queries

    Returns:
        Batch recommendation results
    """
    return await client.post(
        f"/collections/{collection_name}/points/recommend/batch", json={"searches": searches}
    )


def register_search_tools(server: Server, client: QdrantDatabaseClient, tools_list: list) -> None:
    """Register vector search tools with MCP server.

    Args:
        server: MCP server instance
        client: Qdrant database client
    """

    @server.call_tool()
    async def qdrant_db_points_search(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Search for similar vectors in a collection.

        Args:
            collection_name: Name of the collection
            vector: Query vector (list of floats)
            limit: Maximum number of results (default: 10)
            filter: Optional filter conditions
            with_payload: Include payload in results (default: true)
            with_vector: Include vectors in results (default: false)
        """
        result = await search_points(
            client,
            arguments["collection_name"],
            arguments["vector"],
            arguments.get("limit", 10),
            arguments.get("filter"),
            arguments.get("with_payload", True),
            arguments.get("with_vector", False),
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_points_search_batch(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Perform multiple search queries in a single request.

        Args:
            collection_name: Name of the collection
            searches: List of search queries
        """
        result = await search_batch_points(
            client, arguments["collection_name"], arguments["searches"]
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_points_recommend(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Get recommendations based on positive and negative examples.

        Args:
            collection_name: Name of the collection
            positive: List of positive example point IDs
            negative: List of negative example point IDs (optional)
            limit: Maximum number of results (default: 10)
            filter: Optional filter conditions
        """
        result = await recommend_points(
            client,
            arguments["collection_name"],
            arguments["positive"],
            arguments.get("negative"),
            arguments.get("limit", 10),
            arguments.get("filter"),
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_points_recommend_batch(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Perform multiple recommendation queries in a single request.

        Args:
            collection_name: Name of the collection
            searches: List of recommendation queries
        """
        result = await recommend_batch_points(
            client, arguments["collection_name"], arguments["searches"]
        )
        return [{"type": "text", "text": str(result)}]
