"""Quick self-check that the MCP server module loads and catalogs tools.

Does not require Blender to be running.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> int:
    import server as blender_mcp_server

    catalog = blender_mcp_server._load_catalog()
    print(f"catalog commands: {len(catalog)}")
    print(f"registered tools: {blender_mcp_server._REGISTERED}")
    assert len(catalog) >= 200, f"expected 200+ dedicated handlers, got {len(catalog)}"
    assert blender_mcp_server._REGISTERED == len(catalog)
    # Ensure critical + universal bridge tools exist
    names = {e["command"] for e in catalog}
    for required in (
        "get_scene_info",
        "create_object",
        "execute_python",
        "set_principled_bsdf",
        "add_modifier",
        "list_operator_categories",
        "list_operators",
        "search_operators",
        "call_operator",
        "call_operators_batch",
        "get_operator_info",
        "poll_operator",
        "get_coverage_report",
    ):
        assert required in names, f"missing {required}"
    print("OK — MCP server module and catalog look good.")
    print(json.dumps(sorted(list(names))[:10], indent=2), "...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
