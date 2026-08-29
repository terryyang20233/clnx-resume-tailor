#!/usr/bin/env python3
"""Local HTTP endpoint for the CLNx Chrome extension. Binds to 127.0.0.1 only."""

from __future__ import annotations

import json
import os
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from tailor import tailor

HOST = "127.0.0.1"
PORT = 18765
ROOT = Path(__file__).resolve().parent

# pdflatex is often outside GUI/app PATH
texbin = "/Library/TeX/texbin"
if Path(texbin).exists():
    os.environ["PATH"] = texbin + os.pathsep + os.environ.get("PATH", "")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        print("[clnx-resume]", self.address_string(), fmt % args)

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path.rstrip("/") == "/health":
            self._json(200, {"ok": True, "root": str(ROOT)})
            return
        self._json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path.rstrip("/") != "/tailor":
            self._json(404, {"ok": False, "error": "not found"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length > 2_000_000:
            self._json(413, {"ok": False, "error": "payload too large"})
            return
        raw = self.rfile.read(length)
        try:
            job = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._json(400, {"ok": False, "error": "invalid JSON"})
            return
        if not isinstance(job, dict) or not (job.get("fields") or job.get("heading")):
            self._json(400, {"ok": False, "error": "expected a job object with fields"})
            return
        try:
            result = tailor(job)
        except Exception as exc:  # noqa: BLE001
            traceback.print_exc()
            self._json(500, {"ok": False, "error": str(exc)})
            return
        self._json(200, result)


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"CLNx resume server on http://{HOST}:{PORT}")
    print(f"Workspace: {ROOT}")
    print("Keep this terminal open, then use the Chrome extension on CLNx.")
    server.serve_forever()


if __name__ == "__main__":
    main()
