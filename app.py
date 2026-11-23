#!/usr/bin/env python3
"""
ArbiGraph Interactive Quant Dashboard Server (Zero External Dependencies).

Binds to 0.0.0.0:8000 by default using Python's built-in `ThreadingHTTPServer`,
so anyone cloning the repository from GitHub can run `python3 app.py` immediately
on any laptop or PC without installing web frameworks.
"""

from __future__ import annotations
import argparse
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from arbigraph.algorithms.benchmark import run_scaling_benchmark
from arbigraph.services.engine import run_full_market_analysis
from arbigraph.services.market_data import DATASET_CATALOG

WEB_DIR = Path(__file__).resolve().parent / "arbigraph" / "web"


class ArbiGraphRequestHandler(BaseHTTPRequestHandler):
    """Serves static UI assets and JSON algorithm endpoints."""

    def log_message(self, fmt: str, *args: Any) -> None:
        # Clean concise server logs
        print(f"[ArbiGraph HTTP] {self.address_string()} - {fmt % args}")

    def _send_json(self, payload: Any, status: int = HTTPStatus.OK) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _serve_static(self, rel_path: str) -> None:
        target = (WEB_DIR / rel_path).resolve()
        if not str(target).startswith(str(WEB_DIR.resolve())) or not target.is_file():
            self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)
            return

        content = target.read_bytes()
        mime, _ = mimetypes.guess_type(str(target))
        if target.suffix == ".js":
            mime = "application/javascript; charset=utf-8"
        elif target.suffix == ".css":
            mime = "text/css; charset=utf-8"
        elif target.suffix == ".html":
            mime = "text/html; charset=utf-8"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime or "application/octet-stream")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path

        if route == "/api/health":
            self._send_json({"status": "ok", "engine": "ArbiGraph"})
            return

        if route == "/api/datasets":
            self._send_json({"datasets": DATASET_CATALOG})
            return

        if route == "/api/benchmark":
            points = [asdict(p) for p in run_scaling_benchmark()]
            self._send_json({"points": points})
            return

        if route in ("/", "/index.html"):
            self._serve_static("index.html")
            return

        clean_rel = route.lstrip("/")
        self._serve_static(clean_rel)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/analyze":
            self._send_json({"error": "Unknown endpoint"}, status=HTTPStatus.NOT_FOUND)
            return

        try:
            content_len = int(self.headers.get("Content-Length", "0"))
            body_bytes = self.rfile.read(content_len) if content_len > 0 else b"{}"
            params = json.loads(body_bytes.decode("utf-8"))

            report = run_full_market_analysis(
                dataset_id=str(params.get("dataset_id", "fx_arbitrage_desk")),
                fee_pct=float(params.get("fee_pct", 0.0)),
                starting_capital=float(params.get("starting_capital", 1000.0)),
                trader_budget_usd=float(params.get("trader_budget_usd", 10000.0)),
                route_source=params.get("route_source"),
                route_target=params.get("route_target"),
                rate_overrides=params.get("rate_overrides") or [],
            )
            self._send_json(report)
        except Exception as exc:
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the ArbiGraph Web Dashboard Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="TCP port (default: 8000)")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), ArbiGraphRequestHandler)
    print(f"ArbiGraph Quant Dashboard listening on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down ArbiGraph server.")
        server.server_close()


if __name__ == "__main__":
    main()
