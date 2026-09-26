import http.server
import socketserver
import json
import urllib.parse
import urllib.request
import time
import sys

DEFAULT_PORT = 7070

# Load metas
with open("top100_metas.json", "r", encoding="utf-8") as f:
    RAW_METAS = json.load(f)

STREMIO_METAS = []
for item in RAW_METAS:
    STREMIO_METAS.append({
        "id": item["id"],
        "type": "series",
        "name": f"#{item['rank']} - {item['name']}",
        "poster": item.get("poster"),
        "background": item.get("background"),
        "releaseInfo": str(item.get("releaseInfo", "")),
        "description": item.get("description", "")
    })

MANIFEST = {
    "id": "org.antigravity.top100tvshows",
    "version": "1.0.0",
    "name": "Top 100 TV Shows (21st Century)",
    "description": "Custom Stremio Playlist of the Top 100 TV Shows of the 21st Century (NYT List)",
    "types": ["series"],
    "catalogs": [
        {
            "type": "series",
            "id": "top100_series",
            "name": "Top 100 TV Shows"
        }
    ],
    "resources": ["catalog"],
    "idPrefixes": ["tt"]
}

class AddonHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            super().end_headers()
            host = self.headers.get('Host', f'127.0.0.1:{self.server.server_address[1]}')
            manifest_url = f"http://{host}/manifest.json"
            stremio_link = f"stremio://{host}/manifest.json"
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Top 100 TV Shows - Stremio Addon</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f0f13; color: #fff; text-align: center; padding: 50px 20px; }}
        .card {{ background: #1c1c24; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #2d2d3d; }}
        h1 {{ color: #7b5bf2; margin-bottom: 10px; }}
        p {{ color: #a0a0b0; font-size: 16px; line-height: 1.5; }}
        .btn {{ display: inline-block; background: #7b5bf2; color: #fff; text-decoration: none; padding: 14px 28px; border-radius: 10px; font-weight: bold; font-size: 18px; margin-top: 20px; transition: transform 0.2s; }}
        .btn:hover {{ transform: scale(1.05); background: #6945e0; }}
        code {{ background: #121218; padding: 10px 15px; border-radius: 8px; display: block; margin: 20px 0; word-break: break-all; color: #00e5ff; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🍿 Top 100 TV Shows Playlist</h1>
        <p>Stremio Addon active! Click below to automatically install this playlist into your Stremio client.</p>
        <a class="btn" href="{stremio_link}">➕ Install in Stremio</a>
        <p style="margin-top: 30px;">Or copy and paste this manifest URL into Stremio's search bar:</p>
        <code>{manifest_url}</code>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
            return

        if path == "/manifest.json":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(MANIFEST).encode('utf-8'))
            return

        if path.startswith("/catalog/series/top100_series"):
            skip = 0
            if "skip=" in path:
                try:
                    parts = path.split("skip=")
                    skip = int(parts[1].split(".json")[0])
                except:
                    skip = 0
            
            slice_metas = STREMIO_METAS[skip:skip+100]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"metas": slice_metas}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Not Found"}).encode('utf-8'))

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def check_already_running(port):
    try:
        url = f"http://127.0.0.1:{port}/manifest.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode())
            if data.get("id") == MANIFEST["id"]:
                return True
    except Exception:
        pass
    return False

def run_server():
    port = DEFAULT_PORT
    
    # First check if server is already running on DEFAULT_PORT
    if check_already_running(port):
        print(f"=====================================================")
        print(f" SUCCESS: Stremio Addon Server is ALREADY running!")
        print(f" Manifest URL: http://localhost:{port}/manifest.json")
        print(f" Stremio Link: stremio://localhost:{port}/manifest.json")
        print(f"=====================================================\n")
        print("You can close this window or leave it open.")
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            sys.exit(0)
        return

    # Try binding to DEFAULT_PORT or fallback ports
    server = None
    for try_port in [DEFAULT_PORT, 7071, 7072, 7073]:
        try:
            server = ReusableTCPServer(("0.0.0.0", try_port), AddonHandler)
            port = try_port
            break
        except OSError:
            if check_already_running(try_port):
                print(f"=====================================================")
                print(f" SUCCESS: Stremio Addon Server is ALREADY running!")
                print(f" Manifest URL: http://localhost:{try_port}/manifest.json")
                print(f" Stremio Link: stremio://localhost:{try_port}/manifest.json")
                print(f"=====================================================\n")
                try:
                    while True:
                        time.sleep(3600)
                except KeyboardInterrupt:
                    sys.exit(0)
                return

    if not server:
        print("Error: Could not bind to any available port.")
        sys.exit(1)

    print(f"=====================================================")
    print(f" Stremio Addon Server active on http://127.0.0.1:{port}")
    print(f" Manifest URL: http://localhost:{port}/manifest.json")
    print(f" Stremio Link: stremio://localhost:{port}/manifest.json")
    print(f"=====================================================\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    run_server()
