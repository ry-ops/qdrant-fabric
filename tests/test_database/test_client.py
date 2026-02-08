"""Tests for Qdrant Database API client."""

import pytest
from httpx import AsyncClient

from qdrant_mcp.database.client import QdrantDatabaseClient


@pytest.mark.asyncio
async def test_client_context_manager():
    """Test that client can be used as async context manager."""
    client = QdrantDatabaseClient(
        base_url="https://test.qdrant.io:6333",
        api_key="test-key",
    )

    async with client as c:
        assert c._client is not None
        assert isinstance(c._client, AsyncClient)

    assert client._client is None


@pytest.mark.asyncio
async def test_client_raises_without_context():
    """Test that client raises error when used outside context."""
    client = QdrantDatabaseClient(
        base_url="https://test.qdrant.io:6333",
        api_key="test-key",
    )

    with pytest.raises(RuntimeError, match="Client not initialized"):
        _ = client.client
