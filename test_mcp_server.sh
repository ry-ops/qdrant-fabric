#!/bin/bash
echo "🧪 Testing Qdrant MCP Server Startup"
echo "======================================"
echo ""

# Activate venv
source venv/bin/activate

# Set environment
export QDRANT_API_KEY="not-needed-for-local"
export QDRANT_URL="http://localhost:6333"

echo "✓ Virtual environment activated"
echo "✓ Environment variables set"
echo "  - QDRANT_URL=$QDRANT_URL"
echo ""

# Try to start the server (it will wait for stdin from MCP protocol)
echo "🚀 Starting MCP server..."
echo "   (Server will start and wait for MCP protocol messages)"
echo ""

# Start server in background and send it a simple test
timeout 5s python -m qdrant_mcp 2>&1 | head -20 &
SERVER_PID=$!

sleep 2

if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo "✅ Server started successfully!"
    echo "   PID: $SERVER_PID"
    kill $SERVER_PID 2>/dev/null
else
    echo "❌ Server failed to start"
    exit 1
fi

echo ""
echo "✅ MCP Server Test: PASSED"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Desktop to load the new MCP server"
echo "  2. Look for 'qdrant' in the tools menu"
echo "  3. Try: 'List collections in Qdrant'"
