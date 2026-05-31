from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from plotly_web_app.content import STATIC_APP_DIR, STATIC_CONTENT_FILE, export_static_content


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the fully static Plotly app locally.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind to.")
    parser.add_argument("--port", type=int, default=8000, help="Port to expose the static app on.")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild the exported JSON content before starting the server.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.rebuild or not STATIC_CONTENT_FILE.exists():
        export_static_content()

    handler = partial(SimpleHTTPRequestHandler, directory=str(STATIC_APP_DIR))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving static Plotly app from {STATIC_APP_DIR} at http://{args.host}:{args.port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping static server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

