"""Index management tools for Qdrant Database API."""

from typing import Any

from mcp.server import Server

from .client import QdrantDatabaseClient


async def create_field_index(
    client: QdrantDatabaseClient,
    collection_name: str,
    field_name: str,
    field_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create an index for a payload field.

    Args:
        collection_name: Name of the collection
        field_name: Name of the field to index
        field_schema: Optional field schema (type, indexing parameters)

    Returns:
        Index creation result
    """
    body: dict[str, Any] = {"field_name": field_name}
    if field_schema:
        body["field_schema"] = field_schema
    return await client.put(f"/collections/{collection_name}/index", json=body)


async def delete_field_index(
    client: QdrantDatabaseClient, collection_name: str, field_name: str
) -> dict[str, Any]:
    """Delete an index for a payload field.

    Args:
        collection_name: Name of the collection
        field_name: Name of the field to remove index from

    Returns:
        Index deletion result
    """
    return await client.delete(f"/collections/{collection_name}/index/{field_name}")


def register_index_tools(server: Server, client: QdrantDatabaseClient, tools_list: list) -> None:
    """Register index management tools with MCP server.

    Args:
        server: MCP server instance
        client: Qdrant database client
        tools_list: List to append tool definitions to
    """
    from mcp.types import Tool

    # Define tools
    tools_list.extend([
        Tool(
            name="qdrant_db_index_create",
            description="Create an index for a payload field to speed up filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "field_name": {"type": "string"},
                    "field_schema": {"type": "object"},
                },
                "required": ["collection_name", "field_name"],
            },
        ),
        Tool(
            name="qdrant_db_index_delete",
            description="Delete an index for a payload field",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string"},
                    "field_name": {"type": "string"},
                },
                "required": ["collection_name", "field_name"],
            },
        ),
    ])

    @server.call_tool()
    async def qdrant_db_index_create(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Create an index for a payload field.

        Creates an index to speed up filtering operations on a specific field.

        Args:
            collection_name: Name of the collection
            field_name: Name of the field to index
            field_schema: Optional field schema configuration
        """
        result = await create_field_index(
            client,
            arguments["collection_name"],
            arguments["field_name"],
            arguments.get("field_schema"),
        )
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_index_delete(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Delete an index for a payload field.

        Removes the index from a field. Filtering on this field will be slower.

        Args:
            collection_name: Name of the collection
            field_name: Name of the field to remove index from
        """
        result = await delete_field_index(
            client, arguments["collection_name"], arguments["field_name"]
        )
        return [{"type": "text", "text": str(result)}]
