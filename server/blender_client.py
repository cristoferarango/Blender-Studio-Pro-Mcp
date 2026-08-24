"""TCP client for Blender Studio Pro MCP addon (localhost only).

Author: Cristofer Arango — https://corporacionarango.com
License: Apache-2.0
"""

from __future__ import annotations

import json
import os
import socket
import struct
from typing import Any

HEADER_SIZE = 4
DEFAULT_HOST = os.environ.get("BLENDER_MCP_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("BLENDER_MCP_PORT", "9877"))
DEFAULT_TIMEOUT = float(os.environ.get("BLENDER_MCP_TIMEOUT", "120"))


class BlenderConnectionError(Exception):
    """Raised when Blender addon is unreachable or the protocol fails."""


def send_command(
    command: str,
    params: dict[str, Any] | None = None,
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    """Send a command to the Blender addon and return the result payload.

    Protocol: 4-byte big-endian length header + UTF-8 JSON body.
    Request:  {"command": str, "params": dict}
    Response: {"status": "ok"|"error", "result"| "message": ...}
    """
    payload = json.dumps(
        {"command": command, "params": params or {}},
        default=str,
    ).encode("utf-8")
    header = struct.pack(">I", len(payload))

    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            sock.sendall(header + payload)

            # Read header
            hdr = _recv_exact(sock, HEADER_SIZE)
            msg_len = struct.unpack(">I", hdr)[0]
            body = _recv_exact(sock, msg_len)
    except (ConnectionRefusedError, TimeoutError, OSError) as exc:
        raise BlenderConnectionError(
            f"Cannot reach Blender Studio Pro MCP at {host}:{port}. "
            "Open Blender, enable the addon, N panel -> Studio Pro -> Start Server. "
            f"Detail: {exc}"
        ) from exc

    try:
        response = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise BlenderConnectionError(f"Invalid JSON from Blender: {exc}") from exc

    if not isinstance(response, dict):
        raise BlenderConnectionError(f"Unexpected response type: {type(response)}")

    status = response.get("status")
    if status == "ok":
        return response.get("result")
    if status == "error":
        parts = [response.get("message") or "Unknown Blender error"]
        if response.get("hint"):
            parts.append(f"Hint: {response['hint']}")
        raise BlenderConnectionError("\n".join(parts))

    # Some handlers return raw dicts without status wrapping (defensive)
    return response


def ping(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> dict[str, Any]:
    """Lightweight connectivity check via get_scene_info."""
    result = send_command("get_scene_info", {}, host=host, port=port, timeout=10.0)
    name = result.get("name") if isinstance(result, dict) else None
    return {"ok": True, "host": host, "port": port, "scene": name}


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    data = b""
    while len(data) < n:
        chunk = sock.recv(min(65536, n - len(data)))
        if not chunk:
            raise BlenderConnectionError("Connection closed while reading response")
        data += chunk
    return data
