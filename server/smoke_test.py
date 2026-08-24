"""Smoke-test: talk to the Blender addon over TCP without MCP.

Requires Blender open with Studio Pro -> Start Server.

Usage:
    python server/smoke_test.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from blender_client import (  # noqa: E402
    DEFAULT_HOST,
    DEFAULT_PORT,
    BlenderConnectionError,
    ping,
    send_command,
)


def main() -> int:
    print(f"Connecting to Blender at {DEFAULT_HOST}:{DEFAULT_PORT} ...")
    try:
        info = ping()
        print("ping_blender:", json.dumps(info, indent=2))
        scene = send_command("get_scene_info", {})
        name = scene.get("name") if isinstance(scene, dict) else None
        n_objects = len(scene.get("objects", [])) if isinstance(scene, dict) else "?"
        print(f"get_scene_info: scene={name!r} objects={n_objects}")
        print("OK - addon is reachable.")
        return 0
    except BlenderConnectionError as exc:
        print("FAIL - cannot reach Blender addon.")
        print(str(exc))
        print(
            "\nFix:\n"
            "  1. Open Blender\n"
            "  2. Enable addon blender_studio_pro_mcp\n"
            "  3. N panel -> Studio Pro -> Start Server\n"
            "  4. Re-run this script"
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
