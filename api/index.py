from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Resolve path to top100_metas.json
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
metas_path = os.path.join(base_dir, "top100_metas.json")

if not os.path.exists(metas_path):
    metas_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "top100_metas.json")

with open(metas_path, "r", encoding="utf-8") as f:
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

@app.route('/')
@app.route('/index.html')
def home():
    host = request.headers.get('Host', 'localhost')
    scheme = request.headers.get('X-Forwarded-Proto', 'https')
    manifest_url = f"{scheme}://{host}/manifest.json"
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
        <p>Stremio Addon active on Vercel Cloud! Click below to automatically install this playlist into your Stremio client.</p>
        <a class="btn" href="{stremio_link}">➕ Install in Stremio</a>
        <p style="margin-top: 30px;">Or copy and paste this manifest URL into Stremio's search bar:</p>
        <code>{manifest_url}</code>
    </div>
</body>
</html>"""
    return html

@app.route('/manifest.json')
def manifest():
    return jsonify(MANIFEST)

@app.route('/catalog/<type_>/<id_>.json')
@app.route('/catalog/<type_>/<id_>/<skip_str>.json')
def catalog(type_, id_, skip_str=None):
    skip = 0
    if skip_str and "skip=" in skip_str:
        try:
            skip = int(skip_str.replace("skip=", ""))
        except:
            skip = 0
    
    slice_metas = STREMIO_METAS[skip:skip+100]
    return jsonify({"metas": slice_metas})

if __name__ == '__main__':
    app.run(port=7070)
