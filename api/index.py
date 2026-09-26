from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Load TV shows
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

# 2. Load A24 & Underrated Hollywood Movies
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

# 3. Load Indian Movies
indian_path = os.path.join(base_dir, "indian_movies_metas.json")
if not os.path.exists(indian_path):
    indian_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "indian_movies_metas.json")

INDIAN_METAS = []
if os.path.exists(indian_path):
    with open(indian_path, "r", encoding="utf-8") as f:
        raw_indian = json.load(f)
        for item in raw_indian:
            INDIAN_METAS.append({
                "id": item["id"],
                "type": "movie",
                "name": f"#{item['rank']} - {item['name']}",
                "poster": item.get("poster"),
                "background": item.get("background"),
                "releaseInfo": str(item.get("releaseInfo", "")),
                "description": item.get("description", "")
            })

# Manifest 1: Underrated Indian Films Addon
MANIFEST_INDIAN = {
    "id": "org.antigravity.underratedindianfilmsaddon",
    "version": "1.0.0",
    "name": "50 Underrated Indian Films",
    "description": "Custom Stremio Addon featuring 50 Underrated Indian Films across languages (Hindi, Malayalam, Tamil, Bengali, Marathi, Assamese).",
    "types": ["movie"],
    "catalogs": [
        {
            "type": "movie",
            "id": "underrated_indian_movies",
            "name": "50 Underrated Indian Films"
        }
    ],
    "resources": ["catalog"],
    "idPrefixes": ["tt"]
}

# Manifest 2: A24 & Underrated Hollywood Movies Addon
MANIFEST_MOVIES = {
    "id": "org.antigravity.curatedmoviesaddon",
    "version": "1.0.0",
    "name": "A24 & Underrated Movies Playlist",
    "description": "Custom Stremio Addon featuring 50 Notable A24 Films & 50 Underrated Gems (2010-2026).",
    "types": ["movie"],
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
        }
    ],
    "resources": ["catalog"],
    "idPrefixes": ["tt"]
}

# Manifest 3: TV Shows Addon
MANIFEST_TV = {
    "id": "org.antigravity.top100tvshowsaddon",
    "version": "1.0.0",
    "name": "Top 100 TV Shows (21st Century)",
    "description": "Custom Stremio Addon featuring the Top 100 TV Shows of the 21st Century (NYT List).",
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
    
    indian_manifest_url = f"{scheme}://{host}/indian/manifest.json"
    indian_stremio_link = f"stremio://{host}/indian/manifest.json"
    
    movies_manifest_url = f"{scheme}://{host}/movies/manifest.json"
    movies_stremio_link = f"stremio://{host}/movies/manifest.json"
    
    tv_manifest_url = f"{scheme}://{host}/tv/manifest.json"
    tv_stremio_link = f"stremio://{host}/tv/manifest.json"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Stremio Custom Addons Directory</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f0f13; color: #fff; text-align: center; padding: 40px 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .card {{ background: #1c1c24; padding: 25px 30px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #2d2d3d; margin-bottom: 25px; text-align: left; }}
        h1 {{ color: #7b5bf2; font-size: 28px; margin-bottom: 10px; }}
        h2 {{ color: #fff; margin-top: 0; font-size: 20px; }}
        p {{ color: #a0a0b0; font-size: 15px; line-height: 1.5; }}
        .btn {{ display: inline-block; background: #7b5bf2; color: #fff; text-decoration: none; padding: 12px 24px; border-radius: 10px; font-weight: bold; font-size: 15px; margin-top: 15px; transition: transform 0.2s; }}
        .btn:hover {{ transform: scale(1.03); background: #6945e0; }}
        code {{ background: #121218; padding: 10px 15px; border-radius: 8px; display: block; margin-top: 15px; word-break: break-all; color: #00e5ff; font-family: monospace; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 Custom Stremio Addons Directory</h1>
        <p style="margin-bottom: 30px;">Choose and install each addon independently into your Stremio client.</p>
        
        <div class="card">
            <h2>🇮🇳 Addon 1: 50 Underrated Indian Films</h2>
            <p>50 Underrated Indian Films across Hindi, Malayalam, Tamil, Bengali, Marathi, Assamese, and classic cinema.</p>
            <a class="btn" href="{indian_stremio_link}">➕ Install Indian Movies Addon</a>
            <code>{indian_manifest_url}</code>
        </div>

        <div class="card">
            <h2>🎬 Addon 2: A24 & Underrated Movies</h2>
            <p>Includes <b>50 Notable A24 Films</b> and <b>50 Underrated Gems (2010–2026)</b>.</p>
            <a class="btn" href="{movies_stremio_link}">➕ Install Hollywood Movies Addon</a>
            <code>{movies_manifest_url}</code>
        </div>

        <div class="card">
            <h2>🍿 Addon 3: Top 100 TV Shows</h2>
            <p>Includes the <b>Top 100 TV Shows of the 21st Century</b> (NYT List).</p>
            <a class="btn" href="{tv_stremio_link}">➕ Install TV Shows Addon</a>
            <code>{tv_manifest_url}</code>
        </div>
    </div>
</body>
</html>"""
    return html

# Routes for Indian Movies Addon
@app.route('/indian/manifest.json')
@app.route('/indian/manifest')
@app.route('/indian-movies/manifest.json')
def indian_manifest():
    return jsonify(MANIFEST_INDIAN)

# Routes for Hollywood Movies Addon
@app.route('/movies/manifest.json')
@app.route('/movies/manifest')
def movies_manifest():
    return jsonify(MANIFEST_MOVIES)

# Routes for TV Shows Addon
@app.route('/manifest.json')
@app.route('/tv/manifest.json')
def tv_manifest():
    return jsonify(MANIFEST_TV)

# Catalog endpoints (supporting root and prefixed paths)
@app.route('/catalog/<type_>/<id_>.json')
@app.route('/catalog/<type_>/<id_>/<skip_str>.json')
@app.route('/<prefix>/catalog/<type_>/<id_>.json')
@app.route('/<prefix>/catalog/<type_>/<id_>/<skip_str>.json')
def catalog(type_, id_, prefix=None, skip_str=None):
    skip = 0
    if skip_str and "skip=" in skip_str:
        try:
            skip = int(skip_str.replace("skip=", ""))
        except:
            skip = 0

    metas = []
    if id_ == "underrated_indian_movies":
        metas = INDIAN_METAS
    elif id_ == "a24_movies":
        metas = A24_METAS
    elif id_ == "underrated_movies":
        metas = UNDERRATED_METAS
    elif id_ == "top100_series":
        metas = TV_METAS

    slice_metas = metas[skip:skip+100]
    return jsonify({"metas": slice_metas})

if __name__ == '__main__':
    app.run(port=7070)
