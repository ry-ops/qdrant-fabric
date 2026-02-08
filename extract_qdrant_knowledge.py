#!/usr/bin/env python3
"""
Extract and index all Qdrant learning resources into collections.

Creates separate collections for:
- Learning portal content
- Quickstart guides
- Technical articles
- Courses
- Tutorials

Each item is embedded and stored with rich metadata.
"""

import asyncio
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
from bs4 import BeautifulSoup


class QdrantKnowledgeExtractor:
    """Extract and index Qdrant learning resources."""

    def __init__(self, qdrant_url: str = "http://localhost:6333"):
        self.qdrant_url = qdrant_url
        self.base_url = "https://qdrant.tech"
        self.session: httpx.AsyncClient | None = None

    async def __aenter__(self):
        """Enter async context."""
        self.session = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(self, *args):
        """Exit async context."""
        if self.session:
            await self.session.aclose()

    async def fetch_page(self, url: str) -> str:
        """Fetch HTML content from URL."""
        print(f"  Fetching: {url}")
        response = await self.session.get(url)
        response.raise_for_status()
        return response.text

    async def create_collection(self, name: str, description: str) -> None:
        """Create a Qdrant collection."""
        print(f"\n📁 Creating collection: {name}")

        # Delete if exists
        try:
            await self.session.delete(f"{self.qdrant_url}/collections/{name}")
            print(f"  Deleted existing collection")
        except:
            pass

        # Create new collection
        # Using 384 dimensions for all-MiniLM-L6-v2 embeddings (common model)
        collection_config = {
            "vectors": {
                "size": 384,
                "distance": "Cosine"
            }
        }

        response = await self.session.put(
            f"{self.qdrant_url}/collections/{name}",
            json=collection_config
        )
        response.raise_for_status()
        print(f"  ✓ Created with 384-dim vectors (Cosine)")

    def generate_id(self, content: str) -> int:
        """Generate deterministic ID from content."""
        # Generate integer ID from hash
        hash_hex = hashlib.sha256(content.encode()).hexdigest()[:16]
        return int(hash_hex, 16) % (2**63 - 1)  # Ensure positive 64-bit int

    async def index_item(
        self,
        collection: str,
        url: str,
        title: str,
        content: str,
        category: str,
        metadata: dict[str, Any]
    ) -> None:
        """Index a single item into collection."""
        # For now, use a simple hash-based embedding (placeholder)
        # In production, you'd use a real embedding model
        embedding = self._simple_embedding(content)

        point = {
            "id": self.generate_id(url),
            "vector": embedding,
            "payload": {
                "url": url,
                "title": title,
                "content": content[:1000],  # Truncate for storage
                "category": category,
                "indexed_at": datetime.now().isoformat(),
                **metadata
            }
        }

        response = await self.session.put(
            f"{self.qdrant_url}/collections/{collection}/points",
            json={"points": [point]}
        )
        response.raise_for_status()

    def _simple_embedding(self, text: str) -> list[float]:
        """Generate simple embedding (placeholder - use real model in production)."""
        # This is a stub - in production use sentence-transformers or similar
        # For demo purposes, generate deterministic random embedding
        import random
        random.seed(hash(text) % (2**32))
        return [random.random() for _ in range(384)]

    async def extract_learn_portal(self) -> list[dict]:
        """Extract content from learning portal."""
        print("\n🎓 Extracting Learning Portal")

        items = []
        learn_url = f"{self.base_url}/learn/"

        # Main sections to extract
        sections = [
            {"name": "articles", "url": "/articles/"},
            {"name": "courses", "url": "/documentation/courses/"},
            {"name": "tutorials", "url": "/documentation/tutorials/"},
        ]

        # For now, create placeholder data structure
        # In production, parse actual HTML
        items.append({
            "url": learn_url,
            "title": "Qdrant Learning Portal",
            "content": "Central hub for Qdrant learning resources",
            "category": "portal",
            "section": "overview"
        })

        return items

    async def extract_articles(self) -> list[dict]:
        """Extract technical articles."""
        print("\n📰 Extracting Articles")

        items = []

        # Known article categories from research
        categories = [
            "Vector Search Manuals",
            "Qdrant Internals",
            "Data Exploration",
            "Machine Learning",
            "RAG & GenAI",
            "Practical Examples",
            "Ecosystem"
        ]

        # Placeholder - would scrape actual articles
        for i, cat in enumerate(categories):
            items.append({
                "url": f"{self.base_url}/articles/{cat.lower().replace(' ', '-')}/",
                "title": cat,
                "content": f"Technical articles about {cat}",
                "category": "article",
                "article_category": cat
            })

        return items

    async def extract_courses(self) -> list[dict]:
        """Extract course information."""
        print("\n🎓 Extracting Courses")

        items = []

        courses = [
            {
                "title": "Qdrant Essentials",
                "level": "beginner",
                "description": "Vector search fundamentals"
            },
            {
                "title": "Retrieval Optimization",
                "level": "intermediate",
                "description": "From tokenization to vector quantization",
                "partner": "Deep Learning AI"
            },
            {
                "title": "Multi-Vector Retrieval",
                "level": "advanced",
                "description": "Advanced multi-vector techniques",
                "partner": "Deep Learning AI"
            }
        ]

        for course in courses:
            items.append({
                "url": f"{self.base_url}/documentation/courses/{course['title'].lower().replace(' ', '-')}/",
                "title": course["title"],
                "content": course["description"],
                "category": "course",
                "level": course["level"],
                "partner": course.get("partner", "Qdrant")
            })

        return items

    async def extract_tutorials(self) -> list[dict]:
        """Extract tutorials."""
        print("\n📚 Extracting Tutorials")

        items = []

        tutorial_types = [
            {"name": "Basics", "desc": "Foundational exercises on embeddings"},
            {"name": "Search Engineering", "desc": "Technical implementation strategies"},
            {"name": "Operations & Scale", "desc": "Production deployment"},
            {"name": "Develop & Implement", "desc": "Building practical projects"}
        ]

        for tut in tutorial_types:
            items.append({
                "url": f"{self.base_url}/documentation/tutorials/{tut['name'].lower().replace(' ', '-')}/",
                "title": f"Tutorial: {tut['name']}",
                "content": tut["desc"],
                "category": "tutorial",
                "tutorial_type": tut["name"]
            })

        return items

    async def extract_quickstarts(self) -> list[dict]:
        """Extract quickstart guides."""
        print("\n⚡ Extracting Quickstarts")

        items = []

        quickstarts = [
            {
                "title": "Beginner Vector Search",
                "desc": "Getting started with vector search basics"
            },
            {
                "title": "Build Project Prototypes",
                "desc": "Ready-to-build projects with integration guides"
            }
        ]

        for qs in quickstarts:
            items.append({
                "url": f"{self.base_url}/documentation/quickstart/",
                "title": f"Quickstart: {qs['title']}",
                "content": qs["desc"],
                "category": "quickstart"
            })

        return items

    async def run(self):
        """Main extraction and indexing pipeline."""
        print("=" * 80)
        print("QDRANT KNOWLEDGE BASE EXTRACTION")
        print("=" * 80)

        # Create collections
        collections = {
            "qdrant_learning": "Learning portal and overview content",
            "qdrant_articles": "Technical articles and deep dives",
            "qdrant_courses": "Structured learning courses",
            "qdrant_tutorials": "Hands-on tutorials and guides",
            "qdrant_quickstarts": "Quick start guides and examples"
        }

        for name, desc in collections.items():
            await self.create_collection(name, desc)

        # Extract all content
        all_items = {
            "qdrant_learning": await self.extract_learn_portal(),
            "qdrant_articles": await self.extract_articles(),
            "qdrant_courses": await self.extract_courses(),
            "qdrant_tutorials": await self.extract_tutorials(),
            "qdrant_quickstarts": await self.extract_quickstarts()
        }

        # Index all items
        print("\n" + "=" * 80)
        print("INDEXING CONTENT")
        print("=" * 80)

        total_indexed = 0
        for collection, items in all_items.items():
            print(f"\n📊 Indexing into: {collection}")
            for item in items:
                await self.index_item(
                    collection=collection,
                    url=item["url"],
                    title=item["title"],
                    content=item["content"],
                    category=item["category"],
                    metadata={k: v for k, v in item.items()
                             if k not in ["url", "title", "content", "category"]}
                )
                print(f"  ✓ {item['title']}")
                total_indexed += 1

        # Summary
        print("\n" + "=" * 80)
        print("EXTRACTION COMPLETE")
        print("=" * 80)
        print(f"\n✅ Created {len(collections)} collections")
        print(f"✅ Indexed {total_indexed} items")
        print("\nCollections:")
        for name, desc in collections.items():
            count = len(all_items[name])
            print(f"  • {name}: {count} items - {desc}")

        print("\n🎯 Next Steps:")
        print("  1. Use qdrant-fabric tools to query collections")
        print("  2. Add real embedding model (sentence-transformers)")
        print("  3. Scrape actual content from pages")
        print("  4. Add more articles/tutorials")
        print("  5. Build search interface")


async def main():
    """Run the extraction."""
    async with QdrantKnowledgeExtractor() as extractor:
        await extractor.run()


if __name__ == "__main__":
    asyncio.run(main())
