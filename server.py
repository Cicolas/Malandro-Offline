#!/usr/bin/env python3
"""Local game server; cache public static assets on demand."""
import argparse
import mimetypes
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit, unquote, quote

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".asset-cache"
ORIGIN = "https://malandro.app/"
STATIC_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg", ".svg", ".mp3", ".ogg", ".wav", ".woff", ".woff2", ".ttf", ".otf", ".json", ".webmanifest"}
LOCAL_FILES = {"index.html", "local.js"}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.serve(False)

    def do_HEAD(self):
        self.serve(True)

    def do_POST(self):
        self.send_error(404, "Online services are disabled")
        self.close_connection = True

    def serve(self, head):
        raw = unquote(urlsplit(self.path).path)
        if ".." in PurePosixPath(raw).parts or "\\" in raw or "\x00" in raw:
            return self.send_error(400)
        relative = raw.lstrip("/") or "index.html"
        if relative.startswith(("api/", "pvp/")):
            return self.send_error(404, "Online services are disabled")
        target = ROOT / relative
        local = relative in LOCAL_FILES or (relative.startswith("assets/") and target.suffix in {".js", ".css"})
        if local:
            if not target.is_file():
                return self.send_error(404)
            data = target.read_bytes()
        elif Path(relative).suffix.lower() in STATIC_EXTENSIONS:
            target = CACHE / relative
            if target.is_file():
                data = target.read_bytes()
            else:
                try:
                    result = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--max-time", "20", ORIGIN + quote(relative, safe="/")], capture_output=True, timeout=25)
                    if result.returncode:
                        return self.send_error(502, "Uncached asset unavailable")
                    data = result.stdout
                    if data.lstrip().lower().startswith((b"<!doctype html", b"<html")):
                        return self.send_error(404)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                except (subprocess.TimeoutExpired, OSError):
                    return self.send_error(502, "Asset not cached; internet access is required")
        else:
            return self.send_error(404)
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(relative)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self' data: blob:; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' blob:; connect-src 'self'; font-src 'self' data:; frame-src 'none'; object-src 'none'")
        self.end_headers()
        if not head:
            self.wfile.write(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    print(f"Malandro local: http://127.0.0.1:{args.port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
