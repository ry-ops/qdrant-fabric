# Project Renamed: qdrant-mcp → qdrant-fabric

## Changes Made

### 1. Directory
- ✅ Renamed: `~/Projects/qdrant-mcp` → `~/Projects/qdrant-fabric`

### 2. MCP Configuration
- ✅ Updated: `~/.claude/.mcp.json`
  - Server name: `qdrant` → `qdrant-fabric`
  - Command path: Updated to new directory

### 3. Settings
- ✅ Updated: `~/.claude/settings.local.json`
  - Enabled servers: `"qdrant"` → `"qdrant-fabric"`

### 4. Documentation
- ✅ Updated: `README.md`
  - Title: "Qdrant MCP Server" → "Qdrant Fabric"
  - Added fabric integration mention
  - Updated all paths and examples

- ✅ Updated: `pyproject.toml`
  - Package name: `qdrant-mcp` → `qdrant-fabric`
  - Added fabric description

## What Stayed the Same

- ✅ Python module name: `qdrant_mcp` (unchanged - no breaking changes)
- ✅ All 30 tools: Same names, same functionality
- ✅ Virtual environment: Still works at new location
- ✅ Configuration: `.env` file unchanged
- ✅ Code: No code changes required

## Testing Required

### ⚠️ Important: Restart Claude Desktop

The MCP server name changed, so you need to restart Claude Desktop:

```bash
osascript -e 'quit app "Claude"'
open -a Claude
```

### Test in New Conversation

In a new Claude Desktop conversation, try:
```
List all collections in my Qdrant database
```

Should see the `qdrant-fabric` MCP server load with all 30 tools.

## Why the Rename?

**qdrant-fabric** better reflects:
- Part of the "Infrastructure as a Fabric" ecosystem
- Integration with AIANA (semantic memory)
- Integration with n8n-fabric (workflow automation)
- Aligns with fabric naming convention (warp, weft, tink, frog)

## Status

✅ Rename complete
✅ Configuration updated
⏳ Needs: Claude Desktop restart + test
