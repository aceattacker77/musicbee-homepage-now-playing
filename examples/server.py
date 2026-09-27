#!/usr/bin/env python3
"""Minimal HTTP server for the Homepage `customapi` widget. Standard library only.

    python server.py                 # serves http://0.0.0.0:8788/now-playing
    python server.py --port 9000 --host 127.0.0.1

Reads the nowplaying.json the MusicBee plugin writes and returns the card
fields built by now_playing.py (next to this file).
"""

import argparse
import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from now_playing import build_now_playing

DEFAULT_FILE = os.path.join(os.environ.get("APPDATA", ""), "MusicBee",
                            "HomepageNowPlaying", "nowplaying.json")


def make_handler(path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.split("?")[0] != "/now-playing":
                self.send_error(404)
                return
            body = json.dumps(build_now_playing(path, datetime.now(timezone.utc))).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_args):
            pass

    return Handler


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8788)
    ap.add_argument("--file", default=os.environ.get("MUSICBEE_NOW_PLAYING", DEFAULT_FILE))
    args = ap.parse_args()
    print(f"Serving {args.file} at http://{args.host}:{args.port}/now-playing")
    ThreadingHTTPServer((args.host, args.port), make_handler(args.file)).serve_forever()


if __name__ == "__main__":
    main()
