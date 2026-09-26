from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load TV shows
tv_path = os.path.join(base_dir, "top100_metas.json")
if not os.path.exists(tv_path):
    tv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "top100_metas.json")

TV_METAS = []
if os.path.exists(tv_path):
    with open(tv_path, "r", encoding="utf-8") as f:
        raw_tv = json.load(f)
        for item in raw_tv:
            TV_METAS.append({
                "id": item["id"],
                "type": "series",
                "name": f"#{item['rank']} - {item['name']}",
                "poster": item.get("poster"),
                "background": item.get("background"),
                "releaseInfo": str(item.get("releaseInfo", "")),
                "description": item.get("description", "")
            })

# Load Movies
movie_path = os.path.join(base_dir, "movies_metas.json")
if not os.path.exists(movie_path):
    movie_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movies_metas.json")

A24_METAS = []
UNDERRATED_METAS = []

if os.path.exists(movie_path):
    with open(movie_path, "r", encoding="utf-8") as f:
        raw_movies = json.load(f)
        for item in raw_movies.get("a24_movies", []):
            A24_METAS.append({
                "id": item["id"],
                "type": "movie",
                "name": f"#{item['rank']} - {item['name']}",
                "poster": item.get("poster"),
                "background": item.get("background"),
                "releaseInfo": str(item.get("releaseInfo", "")),
                "description": item.get("description", "")
            })
        for item in raw_movies.get("underrated_movies", []):
            UNDERRATED_METAS.append({
                "id": item["id"],
                "type": "movie",
                "name": f"#{item['rank']} - {item['name']}",
                "poster": item.get("poster"),
                "background": item.get("background"),
                "releaseInfo": str(item.get("releaseInfo", "")),
                "description": item.get("description", "")
            })

MANIFEST = {
    "id": "org.antigravity.curatedplaylists",
    "version": "1.1.0",
    "name": "Curated Playlists (A24, Underrated Movies & Top 100 TV)",
    "description": "Custom Stremio Playlists featuring 50 Notable A24 Films, 50 Underrated Films (2010-2026), and Top 100 TV Shows.",
    "types": ["movie", "series"],
    "catalogs": [
        {
            "type": "movie",
            "id": "a24_movies",
            "name": "50 Notable A24 Films"
        },
        {
            "type": "movie",
            "id": "underrated_movies",
            "name": "50 Underrated Gems (2010-2026)"
        },
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
    <title>Curated Playlists - Stremio Addon</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f0f13; color: #fff; text-align: center; padding: 50px 20px; }}
        .card {{ background: #1c1c24; max-width: 650px; margin: 0 auto; padding: 35px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #2d2d3d; }}
        h1 {{ color: #7b5bf2; margin-bottom: 10px; }}
        p {{ color: #a0a0b0; font-size: 16px; line-height: 1.5; }}
        .btn {{ display: inline-block; background: #7b5bf2; color: #fff; text-decoration: none; padding: 14px 28px; border-radius: 10px; font-weight: bold; font-size: 18px; margin-top: 20px; transition: transform 0.2s; }}
        .btn:hover {{ transform: scale(1.05); background: #6945e0; }}
        code {{ background: #121218; padding: 10px 15px; border-radius: 8px; display: block; margin: 20px 0; word-break: break-all; color: #00e5ff; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🎬 Curated Stremio Playlists Addon</h1>
        <p>Active on Vercel Cloud! Includes <b>50 Notable A24 Films</b>, <b>50 Underrated Gems (2010–2026)</b>, and <b>Top 100 TV Shows</b>.</p>
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

    metas = []
    if id_ == "a24_movies":
        metas = A24_METAS
    elif id_ == "underrated_movies":
        metas = UNDERRATED_METAS
    elif id_ == "top100_series":
        metas = TV_METAS

    slice_metas = metas[skip:skip+100]
    return jsonify({"metas": slice_metas})

if __name__ == '__main__':
    app.run(port=7070)
