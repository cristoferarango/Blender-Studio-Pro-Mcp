"""
Blender Studio Pro MCP — free local server (stdio).

Author: Cristofer Arango
Website: https://corporacionarango.com
License: Apache-2.0

100% Blender coverage for Cursor, Claude, Codex, OpenCode, DeepSeek, and any MCP client.
Talks to the Blender addon over TCP localhost:9877. No license keys.
"""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path
from typing import Any, Optional

# Ensure server/ is on path when launched as a script
_SERVER_DIR = Path(__file__).resolve().parent
if str(_SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(_SERVER_DIR))

from mcp.server.fastmcp import FastMCP

try:
    from .blender_client import (
        DEFAULT_HOST,
        DEFAULT_PORT,
        BlenderConnectionError,
        ping,
        send_command,
    )
except ImportError:
    from blender_client import (
        DEFAULT_HOST,
        DEFAULT_PORT,
        BlenderConnectionError,
        ping,
        send_command,
    )

_CATALOG_PATH = _SERVER_DIR / "commands_catalog.json"

mcp = FastMCP(
    "blender-studio-pro-mcp",
    instructions=(
        "Blender Studio Pro MCP by Cristofer Arango (https://corporacionarango.com). "
        "Start Blender addon: N panel -> Studio Pro -> Start Server. "
        "100% Blender: get_coverage_report, list_operator_categories, search_operators, "
        "get_operator_info, poll_operator, call_operator, call_operators_batch cover every "
        "bpy.ops category (typically 70+ categories / 1500–2500+ operators). "
        "Prefer dedicated tools when available; use execute_python for arbitrary bpy. "
        "Works with Cursor, Claude, Codex, OpenCode, DeepSeek, Windsurf, and any MCP host. "
        "No license or API key required."
    ),
)


def _load_catalog() -> list[dict[str, Any]]:
    if not _CATALOG_PATH.exists():
        return []
    return json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))


def _result_text(value: Any) -> str:
    return json.dumps(value, indent=2, default=str)


def _call(command: str, params: dict[str, Any]) -> str:
    try:
        cleaned = {k: v for k, v in params.items() if v is not None}
        result = send_command(command, cleaned)
        return _result_text(result)
    except BlenderConnectionError as exc:
        return _result_text({"error": str(exc)})


@mcp.tool()
def ping_blender() -> str:
    """Check connectivity to Blender Studio Pro MCP addon on localhost."""
    try:
        return _result_text(ping())
    except BlenderConnectionError as exc:
        return _result_text(
            {
                "ok": False,
                "host": DEFAULT_HOST,
                "port": DEFAULT_PORT,
                "error": str(exc),
            }
        )


@mcp.tool()
def list_blender_commands() -> str:
    """List dedicated Blender Studio Pro MCP commands grouped by module."""
    catalog = _load_catalog()
    by_module: dict[str, list[str]] = {}
    for entry in catalog:
        by_module.setdefault(entry["module"], []).append(entry["command"])
    return _result_text(
        {
            "app": "Blender Studio Pro MCP",
            "host": DEFAULT_HOST,
            "port": DEFAULT_PORT,
            "total": len(catalog),
            "modules": {m: sorted(cmds) for m, cmds in sorted(by_module.items())},
            "full_blender": "Also use call_operator for 100% of bpy.ops",
        }
    )


def _make_tool_fn(entry: dict[str, Any]):
    command = entry["command"]
    doc = entry.get("doc") or f"Blender Studio Pro MCP: {command}"
    param_specs = entry.get("params") or []

    parameters: list[inspect.Parameter] = []
    annotations: dict[str, Any] = {"return": str}
    has_kwargs = False

    for spec in param_specs:
        if spec.get("kwargs"):
            has_kwargs = True
            continue
        name = spec["name"]
        if spec.get("required"):
            parameters.append(
                inspect.Parameter(
                    name,
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Any,
                )
            )
            annotations[name] = Any
        else:
            default = spec.get("default", None)
            parameters.append(
                inspect.Parameter(
                    name,
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    default=default,
                    annotation=Any,
                )
            )
            annotations[name] = Any

    if has_kwargs:
        parameters.append(
            inspect.Parameter(
                "extra_params",
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=None,
                annotation=Optional[dict],
            )
        )
        annotations["extra_params"] = Optional[dict]

    def impl(*args, **kwargs):
        bound_params: dict[str, Any] = {}
        names = [p.name for p in parameters if p.name != "extra_params"]
        for i, val in enumerate(args):
            if i < len(names):
                bound_params[names[i]] = val
        bound_params.update(kwargs)
        extra = bound_params.pop("extra_params", None) or {}
        if isinstance(extra, dict):
            bound_params.update(extra)
        return _call(command, bound_params)

    impl.__name__ = command
    impl.__doc__ = doc
    impl.__signature__ = inspect.Signature(parameters, return_annotation=str)
    impl.__annotations__ = annotations
    return impl


def _register_catalog_tools() -> int:
    catalog = _load_catalog()
    skip = {"ping_blender", "list_blender_commands"}
    count = 0
    for entry in catalog:
        name = entry["command"]
        if name in skip:
            continue
        fn = _make_tool_fn(entry)
        mcp.tool(name=name, description=entry.get("doc") or f"Blender Studio Pro MCP: {name}")(fn)
        count += 1
    return count


_REGISTERED = _register_catalog_tools()


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
