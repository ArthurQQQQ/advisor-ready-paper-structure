#!/usr/bin/env python3
"""Serve a research workspace and its live state on this computer."""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from secrets import token_urlsafe


HOST = "127.0.0.1"


def workspace_handler(html, state, prefix):
    routes = {
        prefix: (html, "text/html; charset=utf-8"),
        prefix + "research-state.json": (state, "application/json; charset=utf-8"),
    }

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            host, port = self.server.server_address
            route = routes.get(self.path)
            if self.headers.get("Host") != f"{host}:{port}" or route is None:
                self.send_error(404)
                return

            path, content_type = route
            try:
                body = path.read_bytes()
            except OSError:
                self.send_error(503, "Workspace file is temporarily unavailable")
                return

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Cross-Origin-Resource-Policy", "same-origin")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Rendered workspace HTML file")
    parser.add_argument("state", type=Path, help="Research state JSON file")
    parser.add_argument("--port", type=int, default=0, help="Loopback port (default: choose a free port)")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535")

    try:
        html = args.html.resolve()
        state = args.state.resolve()
        if not html.is_file() or not state.is_file():
            parser.error("the workspace HTML and state JSON must both exist as files")

        prefix = f"/{token_urlsafe(18)}/"
        with ThreadingHTTPServer((HOST, args.port), workspace_handler(html, state, prefix)) as server:
            host, port = server.server_address
            print(f"http://{host}:{port}{prefix}", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        return
    except OSError as error:
        parser.exit(1, f"Preview unavailable: {error}\n")


if __name__ == "__main__":
    main()
