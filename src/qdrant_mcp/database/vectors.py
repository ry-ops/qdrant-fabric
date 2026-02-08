"""Vector operations tools for Qdrant Database API."""

from typing import Any

from mcp.server import Server

from .client import QdrantDatabaseClient


async def update_vectors(
    client: QdrantDatabaseClient,
    collection_name: str,
    points: list[dict[str, Any]],
) -> dict[str, Any]:
    """Update vectors for existing points.

    Args:
        collection_name: Name of the collection
        points: List of points with id and vector to update

    Returns:
        Update operation result
    """
    return await client.put(
        f"/collections/{collection_name}/points/vectors", json={"points": points}
    )


async def delete_vectors(
    client: QdrantDatabaseClient,
    collection_name: str,
    points: list[Any],
    vector_names: list[str] | None = None,
) -> dict[str, Any]:
    """Delete vectors from points.

    Args:
        collection_name: Name of the collection
        points: List of point IDs to delete vectors from
        vector_names: Optional list of vector names to delete (for named vectors)

    Returns:
        Deletion operation result
    """
    body: dict[str, Any] = {"points": points}
    if vector_names:
        body["vectors"] = vector_names
    return await client.post(f"/collections/{collection_name}/points/vectors/delete", json=body)


def register_vector_tools(server: Server, client: QdrantDatabaseClient) -> None:
    """Register vector operation tools with MCP server.

    Args:
        server: MCP server instance
        client: Qdrant database client
    """

    @server.call_tool()
    async def qdrant_db_vectors_update(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Update vectors for existing points.

        Args:
            collection_name: Name of the collection
            points: List of points with id and vector fields
        """
        result = await update_vectors(
            client, arguments["collection_name"], arguments["points"]
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_vectors_delete(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Delete vectors from points.

        Args:
            collection_name: Name of the collection
            points: List of point IDs to delete vectors from
            vector_names: Optional list of vector names (for named vectors)
        """
        result = await delete_vectors(
            client,
            arguments["collection_name"],
            arguments["points"],
            arguments.get("vector_names"),
        )
        return [{"type": "text", "text": str(result)}]
