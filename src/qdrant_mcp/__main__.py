"""Entry point for running qdrant-mcp as a module."""

from .server import serve

if __name__ == "__main__":
    serve()
