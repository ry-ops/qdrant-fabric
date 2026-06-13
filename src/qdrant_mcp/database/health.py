"""Health check tools for Qdrant Database API."""

from typing import Any

from mcp.types import Tool

from .client import QdrantDatabaseClient


async def get_root(client: QdrantDatabaseClient) -> dict[str, Any]:
    """Get root endpoint information.

    Returns:
        Version and build information
    """
    return await client.get("/")


async def healthz(client: QdrantDatabaseClient) -> str:
    """Health check endpoint.

    Returns:
        Health status (plain text)
    """
    response = await client.client.get("/healthz")
    response.raise_for_status()
    return response.text


async def livez(client: QdrantDatabaseClient) -> str:
    """Liveness probe - checks if service is running.

    Returns:
        Liveness status (plain text)
    """
    response = await client.client.get("/livez")
    response.raise_for_status()
    return response.text


async def readyz(client: QdrantDatabaseClient) -> str:
    """Readiness probe - checks if service is ready to serve requests.

    Returns:
        Readiness status (plain text)
    """
    response = await client.client.get("/readyz")
    response.raise_for_status()
    return response.text


async def metrics(client: QdrantDatabaseClient) -> str:
    """Get Prometheus metrics.

    Returns:
        Prometheus-formatted metrics
    """
    response = await client.client.get("/metrics")
    response.raise_for_status()
    return response.text


def register_health_tools(client: QdrantDatabaseClient, tools_list: list, handlers: dict) -> None:
    """Register health check tools.

    Args:
        client: Qdrant database client
        tools_list: List to append tool definitions to
        handlers: Mapping of tool name -> async handler to populate
    """
    # Define tools
    tools_list.extend([
        Tool(
            name="qdrant_db_health_root",
            description="Get Qdrant version and build information",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="qdrant_db_health_check",
            description="Perform health check on Qdrant database",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="qdrant_db_health_liveness",
            description="Check if Qdrant is alive",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="qdrant_db_health_readiness",
            description="Check if Qdrant is ready to serve requests",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="qdrant_db_health_metrics",
            description="Get Prometheus metrics from Qdrant",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ])

    async def qdrant_db_health_root(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Get Qdrant version and build information."""
        result = await get_root(client)
        return [{"type": "text", "text": str(result)}]

    async def qdrant_db_health_check(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Perform health check on Qdrant database."""
        result = await healthz(client)
        return [{"type": "text", "text": str(result)}]

    async def qdrant_db_health_liveness(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Check if Qdrant service is running."""
        result = await livez(client)
        return [{"type": "text", "text": str(result)}]

    async def qdrant_db_health_readiness(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Check if Qdrant service is ready to serve requests."""
        result = await readyz(client)
        return [{"type": "text", "text": str(result)}]

    async def qdrant_db_health_metrics(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Get Prometheus metrics from Qdrant."""
        result = await metrics(client)
        return [{"type": "text", "text": result}]

    handlers.update(
        {
            "qdrant_db_health_root": qdrant_db_health_root,
            "qdrant_db_health_check": qdrant_db_health_check,
            "qdrant_db_health_liveness": qdrant_db_health_liveness,
            "qdrant_db_health_readiness": qdrant_db_health_readiness,
            "qdrant_db_health_metrics": qdrant_db_health_metrics,
        }
    )
