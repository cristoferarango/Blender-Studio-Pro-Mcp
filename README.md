# Blender Studio Pro MCP

**100% Blender control** from Cursor, Claude, Codex, OpenCode, DeepSeek, Windsurf, and any MCP client.

- **Author:** Cristofer Arango  
- **Website:** [corporacionarango.com](https://corporacionarango.com)  
- **License:** [Apache License 2.0](LICENSE)  
- **No license keys. Local only. Clone on any device.**

## Capabilities

| | |
|--|--|
| Dedicated tools | **221** |
| Modules | **33** |
| `bpy.ops` categories | **70+** |
| Operators (via universal bridge) | **1,500–2,500+** |

**221 dedicated tools · 33 modules · 70+ bpy.ops categories · 1,500–2,500+ operators**

## Installation

```bash
git clone https://github.com/cristoferarango/Blender-Studio-Pro-Mcp.git
cd Blender-Studio-Pro-Mcp
pip install -e .
```

Then run the MCP server:

```bash
blender-studio-pro-mcp
```

### Install the ZIP in Blender

Download: **[blender_studio_pro_mcp.zip](https://github.com/cristoferarango/Blender-Studio-Pro-Mcp/raw/main/blender_studio_pro_mcp.zip)**

1. Open Blender → **Edit → Preferences → Add-ons → Install…**
2. Select `blender_studio_pro_mcp.zip`
3. Enable **Blender Studio Pro MCP**
4. In the 3D Viewport press **N** → **Studio Pro** → **Start Server** (port `9877`)

Or copy the folder `blender_studio_pro_mcp/` into Blender’s `scripts/addons/`.

### Connect any MCP client

See **[CLIENTS.md](CLIENTS.md)** for Cursor, Claude, Codex, OpenCode, DeepSeek, Windsurf.

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

## What “100%” means

Blender ships **~70+ `bpy.ops` categories** and typically **1500–2500+ operators**.  
Blender Studio Pro MCP covers them completely:

| Layer | Capability |
|-------|------------|
| **Universal bridge** | `get_coverage_report` · `list_operator_categories` · `search_operators` · `get_operator_info` · `poll_operator` · `call_operator` · `call_operators_batch` |
| **Dedicated tools** | 221 high-level tools (materials, physics, sculpt, VSE, GP, compositor, mesh edit, …) |
| **Python** | `execute_python` for any `bpy` / `bmesh` |

So agents can do **everything** in Blender: model, animate, rig, simulate, paint, composite, sequence, render, and file I/O.

## Agent workflow (full Blender)

```
get_coverage_report()
list_operator_categories()
search_operators("subdivide")
get_operator_info("mesh.subdivide")
poll_operator("mesh.subdivide")
call_operator("mesh.subdivide", {"number_cuts": 2})
```

Or use dedicated tools (`create_object`, `set_principled_bsdf`, …) when available.

## Architecture

```
Cursor / Claude / Codex / OpenCode / DeepSeek / …
        │  MCP stdio
        ▼
blender-studio-pro-mcp
        │  TCP 127.0.0.1:9877
        ▼
Blender Studio Pro MCP addon → bpy (100%)
```

## Verify

```bash
python server/self_check.py
python server/test_protocol.py
python server/smoke_test.py   # Blender + Start Server
```

## Requirements

- Blender 3.6+ (4.x / 5.x recommended)
- Python 3.10+
- Any MCP-compatible client

## License

Copyright 2026 Cristofer Arango — Apache-2.0  
https://corporacionarango.com
