"""Protocol unit test with a mock Blender TCP server (no Blender required)."""

from __future__ import annotations

import json
import socket
import struct
import threading
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from blender_client import send_command, BlenderConnectionError  # noqa: E402


def _mock_server(port: int, stop: threading.Event):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", port))
    srv.listen(1)
    srv.settimeout(0.5)
    try:
        while not stop.is_set():
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            with conn:
                hdr = conn.recv(4)
                n = struct.unpack(">I", hdr)[0]
                body = b""
                while len(body) < n:
                    body += conn.recv(n - len(body))
                req = json.loads(body.decode("utf-8"))
                assert req["command"] == "get_scene_info"
                resp = json.dumps(
                    {"status": "ok", "result": {"name": "MockScene", "objects": []}}
                ).encode("utf-8")
                conn.sendall(struct.pack(">I", len(resp)) + resp)
    finally:
        srv.close()


def main() -> int:
    port = 19877
    stop = threading.Event()
    t = threading.Thread(target=_mock_server, args=(port, stop), daemon=True)
    t.start()
    time.sleep(0.2)
    try:
        result = send_command("get_scene_info", {}, host="127.0.0.1", port=port, timeout=5.0)
        assert result["name"] == "MockScene"
        print("OK - TCP protocol round-trip works.")
        return 0
    except BlenderConnectionError as exc:
        print("FAIL:", exc)
        return 1
    finally:
        stop.set()
        t.join(timeout=2.0)


if __name__ == "__main__":
    raise SystemExit(main())
