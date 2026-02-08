"""HTTP client for Qdrant Database API."""

from typing import Any, Optional

import httpx


class QdrantDatabaseClient:
    """Async HTTP client for Qdrant Database REST API.

    Handles authentication, retries, and response parsing.
    """

    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0):
        """Initialize database client.

        Args:
            base_url: Qdrant database URL (e.g., https://xyz.qdrant.io:6333)
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "QdrantDatabaseClient":
        """Enter async context."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"api-key": self.api_key, "Content-Type": "application/json"},
            timeout=self.timeout,
        )
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit async context."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the underlying HTTP client.

        Raises:
            RuntimeError: If client is not initialized (use async context manager)
        """
        if self._client is None:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        return self._client

    async def get(self, path: str, **kwargs: Any) -> Any:
        """Make GET request.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            Response JSON data
        """
        response = await self.client.get(path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def post(self, path: str, **kwargs: Any) -> Any:
        """Make POST request.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters (json, data, etc.)

        Returns:
            Response JSON data
        """
        response = await self.client.post(path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def put(self, path: str, **kwargs: Any) -> Any:
        """Make PUT request.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            Response JSON data
        """
        response = await self.client.put(path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def patch(self, path: str, **kwargs: Any) -> Any:
        """Make PATCH request.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            Response JSON data
        """
        response = await self.client.patch(path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def delete(self, path: str, **kwargs: Any) -> Any:
        """Make DELETE request.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            Response JSON data
        """
        response = await self.client.delete(path, **kwargs)
        response.raise_for_status()
        return response.json()
