"""Health check tools for Qdrant Database API."""

from typing import Any

from mcp.server import Server

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


def register_health_tools(server: Server, client: QdrantDatabaseClient) -> None:
    """Register health check tools with MCP server.

    Args:
        server: MCP server instance
        client: Qdrant database client
    """

    @server.call_tool()
    async def qdrant_db_health_root(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Get Qdrant version and build information.

        Returns version, title, and build information.
        """
        result = await get_root(client)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_health_check(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Perform health check on Qdrant database.

        Returns health status of the database.
        """
        result = await healthz(client)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_health_liveness(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Check if Qdrant service is running.

        Liveness probe for Kubernetes-style health checks.
        """
        result = await livez(client)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_health_readiness(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Check if Qdrant service is ready to serve requests.

        Readiness probe for Kubernetes-style health checks.
        """
        result = await readyz(client)
        return [{"type": "text", "text": str(result)}]

    @server.call_tool()
    async def qdrant_db_health_metrics(arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Get Prometheus metrics from Qdrant.

        Returns metrics in Prometheus text format.
        """
        result = await metrics(client)
        return [{"type": "text", "text": result}]
