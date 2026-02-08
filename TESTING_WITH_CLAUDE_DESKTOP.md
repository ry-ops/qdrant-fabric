# Testing Qdrant MCP Server with Claude Desktop

## ✅ Configuration Complete

Your Qdrant MCP server is now configured and ready to use!

### Files Updated
- ✅ `~/.claude/.mcp.json` - Added qdrant server
- ✅ `~/.claude/settings.local.json` - Enabled qdrant server

## 🚀 Next Steps

### 1. Restart Claude Desktop

**IMPORTANT:** You must restart Claude Desktop for it to load the new MCP server.

```bash
# Force quit Claude Desktop
osascript -e 'quit app "Claude"'

# Wait a moment, then reopen
open -a Claude
```

### 2. Verify Server is Loaded

After restarting, you should see the Qdrant tools available. Look for the tools icon in Claude Desktop.

### 3. Test the Tools

Try these test queries in Claude Desktop:

#### Basic Tests

**Test 1: List Collections**
```
List all collections in my Qdrant database
```
Expected: Should call `qdrant_db_collections_list` and show existing collections

**Test 2: Create a Collection**
```
Create a new Qdrant collection called "test_embeddings" with vector size 384 and cosine distance
```
Expected: Should call `qdrant_db_collections_create`

**Test 3: Add Points**
```
Add some test points to the test_embeddings collection
```
Expected: Should call `qdrant_db_points_upsert`

**Test 4: Search**
```
Search for similar vectors in test_embeddings
```
Expected: Should call `qdrant_db_points_search`

**Test 5: Health Check**
```
Check the health of my Qdrant database
```
Expected: Should call `qdrant_db_health_check`

#### Advanced Tests

**Test 6: Batch Operations**
```
Use batch operations to add multiple points at once to test_embeddings
```
Expected: Should call `qdrant_db_points_batch`

**Test 7: Recommendations**
```
Get recommendations based on point ID 1 in test_embeddings
```
Expected: Should call `qdrant_db_points_recommend`

**Test 8: Index Management**
```
Create an index on the 'category' field in test_embeddings
```
Expected: Should call `qdrant_db_index_create`

## 🔍 Troubleshooting

### Server Not Appearing

1. **Check logs** in Claude Desktop Console (Help > Show Logs)
2. **Verify configuration**:
   ```bash
   cat ~/.claude/.mcp.json
   cat ~/.claude/settings.local.json
   ```

3. **Test server manually**:
   ```bash
   cd ~/Projects/qdrant-mcp
   source venv/bin/activate
   python -m qdrant_mcp
   ```
   Should output: "Registered 30 database tools (Phase 1 complete)"

### Tools Not Working

1. **Check Qdrant is running**:
   ```bash
   curl http://localhost:6333/
   ```
   Should return version info

2. **Check environment variables** in `.mcp.json`:
   - QDRANT_URL: http://localhost:6333
   - QDRANT_API_KEY: not-needed-for-local

3. **View detailed logs**:
   ```bash
   # Add logging to see what's happening
   export QDRANT_LOG_LEVEL=DEBUG
   ```

## 📊 Available Tools (30 Total)

### Collections (6)
- `qdrant_db_collections_list`
- `qdrant_db_collections_get`
- `qdrant_db_collections_create`
- `qdrant_db_collections_delete`
- `qdrant_db_collections_update`
- `qdrant_db_collections_exists`

### Points (7)
- `qdrant_db_points_upsert`
- `qdrant_db_points_get`
- `qdrant_db_points_get_single`
- `qdrant_db_points_delete`
- `qdrant_db_points_count`
- `qdrant_db_points_scroll`
- `qdrant_db_points_batch`

### Search (4)
- `qdrant_db_points_search`
- `qdrant_db_points_search_batch`
- `qdrant_db_points_recommend`
- `qdrant_db_points_recommend_batch`

### Payload (4)
- `qdrant_db_payload_set`
- `qdrant_db_payload_overwrite`
- `qdrant_db_payload_delete`
- `qdrant_db_payload_clear`

### Vectors (2)
- `qdrant_db_vectors_update`
- `qdrant_db_vectors_delete`

### Index (2)
- `qdrant_db_index_create`
- `qdrant_db_index_delete`

### Health (5)
- `qdrant_db_health_root`
- `qdrant_db_health_check`
- `qdrant_db_health_liveness`
- `qdrant_db_health_readiness`
- `qdrant_db_health_metrics`

## 🎯 Example Workflows

### Workflow 1: Setup and Test
```
1. "List my Qdrant collections"
2. "Create a collection called 'documents' with 1536-dimensional vectors using cosine similarity"
3. "Add 5 sample points to the documents collection"
4. "Search for similar documents"
5. "Delete the test collection"
```

### Workflow 2: Working with AIANA
```
1. "What collections exist in my Qdrant database?"
2. "Show me some points from the semantic_memory collection"
3. "Search AIANA's semantic memory for discussions about MCP servers"
```

### Workflow 3: Advanced Operations
```
1. "Create a collection with custom configuration"
2. "Use batch operations to add 100 points"
3. "Create indexes on frequently queried fields"
4. "Get recommendations based on user preferences"
```

## 🎉 Success Indicators

When everything is working, you should see:

1. ✅ Qdrant tools appear in Claude Desktop tool picker
2. ✅ Server logs show "Registered 30 database tools"
3. ✅ Collection operations work (list, create, etc.)
4. ✅ Search and recommendations return results
5. ✅ No connection errors in responses

## 📝 Notes

- **Local Qdrant**: Using existing AIANA Qdrant on port 6333
- **No Authentication**: Local instance doesn't require API key
- **AIANA Integration**: Can query AIANA's semantic_memory collection
- **Performance**: Operations typically complete in <50ms

---

**Status**: ✅ Configured and ready for testing
**Next**: Restart Claude Desktop and try the test queries above!
