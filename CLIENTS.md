# MCP client configs — Blender Studio Pro MCP

Same stdio server works with **any** MCP host. After:

```bash
pip install -e .
```

use command `blender-studio-pro-mcp` (alias: `blender-mcp`).

Blender must be open: **N → Studio Pro → Start Server**.

---

## Cursor

Settings → MCP, or project `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "blender-studio-pro-mcp": {
      "command": "blender-studio-pro-mcp",
      "args": []
    }
  }
}
```

## Claude Code / Claude Desktop

`~/.claude.json` or `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "blender-studio-pro-mcp": {
      "command": "blender-studio-pro-mcp",
      "args": []
    }
  }
}
```

## OpenAI Codex

Add to Codex MCP / tools config (stdio):

```json
{
  "mcpServers": {
    "blender-studio-pro-mcp": {
      "command": "blender-studio-pro-mcp",
      "args": []
    }
  }
}
```

## OpenCode

```json
{
  "mcp": {
    "blender-studio-pro-mcp": {
      "command": "blender-studio-pro-mcp",
      "args": []
    }
  }
}
```

(Adjust key name to match OpenCode’s schema if it uses `mcpServers`.)

## DeepSeek (and other MCP hosts)

Any client that supports MCP stdio:

```json
{
  "mcpServers": {
    "blender-studio-pro-mcp": {
      "command": "blender-studio-pro-mcp",
      "args": []
    }
  }
}
```

## Without global install

```json
{
  "mcpServers": {
    "blender-studio-pro-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/blender-mcp/server/server.py"]
    }
  }
}
```

## Windsurf / VS Code Copilot Chat

Same JSON as Cursor. If tools don’t refresh after lazy load, all tools are registered eagerly at startup (no license / no lazy gate).

---

Author: Cristofer Arango — https://corporacionarango.com  
License: Apache-2.0
