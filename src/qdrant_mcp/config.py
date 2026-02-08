"""Configuration management for Qdrant MCP server."""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class QdrantConfig(BaseSettings):
    """Configuration for Qdrant MCP server.

    Supports both Cloud Management API and Database API configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="QDRANT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Cloud Management API
    cloud_api_key: Optional[str] = None
    cloud_url: str = "https://cloud.qdrant.io"

    # Database API
    api_key: Optional[str] = None
    url: Optional[str] = None

    # Optional: Default account ID for cloud operations
    account_id: Optional[str] = None

    def validate_cloud_config(self) -> bool:
        """Check if Cloud Management API is configured."""
        return self.cloud_api_key is not None

    def validate_database_config(self) -> bool:
        """Check if Database API is configured."""
        return self.api_key is not None and self.url is not None
