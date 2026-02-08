#!/usr/bin/env python3
"""Quick test to verify Qdrant Cloud API connectivity."""

import asyncio
import httpx
from qdrant_mcp.config import QdrantConfig


async def test_cloud_api():
    """Test basic Cloud API connectivity."""
    config = QdrantConfig()

    if not config.validate_cloud_config():
        print("❌ Cloud API not configured")
        return

    print("✅ Configuration loaded")
    print(f"   Cloud URL: {config.cloud_url}")
    print(f"   API Key: {config.cloud_api_key[:20]}...")

    async with httpx.AsyncClient(
        base_url=config.cloud_url,
        headers={"Authorization": f"Bearer {config.cloud_api_key}"},
        timeout=10.0
    ) as client:
        try:
            # Test 1: Get authenticated user (simpler endpoint)
            print("\n🔍 Testing: GET /api/iam/v1/users/me")
            response = await client.get("/api/iam/v1/users/me")
            response.raise_for_status()
            data = response.json()

            print(f"✅ Success! Authenticated as:")
            print(f"   Status: {response.status_code}")
            if "result" in data and "user" in data["result"]:
                user = data["result"]["user"]
                print(f"   Email: {user.get('email', 'N/A')}")
                print(f"   ID: {user.get('id', 'N/A')}")
            else:
                print(f"   Data: {data}")

            # Test 2: List accounts
            print("\n🔍 Testing: GET /api/account/v1/accounts")
            response = await client.get("/api/account/v1/accounts")
            response.raise_for_status()
            data = response.json()

            print(f"✅ Success! Accounts:")
            if "result" in data and "items" in data["result"]:
                accounts = data["result"]["items"]
                print(f"   Found {len(accounts)} account(s)")
                for acc in accounts:
                    print(f"     - {acc.get('name', 'Unnamed')} ({acc.get('id', 'no-id')})")
            else:
                print(f"   Data: {data}")

        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP Error: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_cloud_api())
