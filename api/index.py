from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import urllib.request
import urllib.parse
import os
import time
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------------------
# 1. STATIC METAS LOADERS (TV, Hollywood Movies, Indian Movies, Anime, Cartoons)
# -------------------------------------------------------------

# TV Shows
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

# Hollywood Movies
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

# Indian Movies
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

# Anime
anime_path = os.path.join(base_dir, "anime_metas.json")
if not os.path.exists(anime_path):
    anime_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anime_metas.json")

ANIME_SERIES_METAS = []
ANIME_MOVIE_METAS = []

if os.path.exists(anime_path):
    with open(anime_path, "r", encoding="utf-8") as f:
        raw_anime = json.load(f)
        for item in raw_anime:
            formatted = {
                "id": item["id"],
                "type": item.get("type", "series"),
                "name": f"#{item['rank']} - {item['name']}",
                "poster": item.get("poster"),
                "background": item.get("background"),
                "releaseInfo": str(item.get("releaseInfo", "")),
                "description": item.get("description", "")
            }
            if item.get("type") == "movie":
                ANIME_MOVIE_METAS.append(formatted)
            else:
                ANIME_SERIES_METAS.append(formatted)

# Cartoons
cartoons_path = os.path.join(base_dir, "cartoons_metas.json")
if not os.path.exists(cartoons_path):
    cartoons_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cartoons_metas.json")

CARTOON_SERIES_METAS = []
CARTOON_MOVIE_METAS = []

if os.path.exists(cartoons_path):
    with open(cartoons_path, "r", encoding="utf-8") as f:
        raw_cartoons = json.load(f)
        for item in raw_cartoons:
            formatted = {
                "id": item["id"],
                "type": item.get("type", "series"),
                "name": f"#{item['rank']} - {item['name']}",
                "poster": item.get("poster"),
                "background": item.get("background"),
                "releaseInfo": str(item.get("releaseInfo", "")),
                "description": item.get("description", "")
            })
            if item.get("type") == "movie":
                CARTOON_MOVIE_METAS.append(formatted)
            else:
                CARTOON_SERIES_METAS.append(formatted)

# -------------------------------------------------------------
# 2. DYNAMIC TRENDING INDIAN SERIES FETCHER & CACHE (DAILY REFRESH)
# -------------------------------------------------------------

TMDB_KEY = "4ef0d7355d9ffb5151e987764708ce96"
DYNAMIC_CACHE = {}

TOP_INDIAN_OTT_SERIES = [
    "Panchayat", "Mirzapur", "Sacred Games", "The Family Man", "Farzi", 
    "Scam 1992: The Harshad Mehta Story", "Kota Factory", "Asur: Welcome to Your Dark Side", 
    "Criminal Justice", "Delhi Crime", "Special OPS", "Paatal Lok", 
    "Aspirants", "Gullak", "Bandish Bandits", "Yeh Meri Family", "Rocket Boys",
    "TVF Pitchers", "Permanent Roommates", "Made in Heaven", "Breathe",
    "Suzhal - The Vortex", "Dahaad", "Kohrra", "Kaala Paani", "Poacher",
    "Heeramandi: The Diamond Bazaar", "Taaza Khabar", "Grahan", "The Railway Men"
]

def resolve_cinemeta_show(show_tuple):
    rank, name = show_tuple
    encoded = urllib.parse.quote(name)
    url = f"https://v3-cinemeta.strem.io/catalog/series/top/search={encoded}.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            metas = data.get('metas', [])
            if metas:
                best = metas[0]
                return {
                    "id": best['id'],
                    "type": "series",
                    "name": f"#{rank} - {best.get('name', name)}",
                    "poster": best.get('poster'),
                    "background": best.get('background'),
                    "releaseInfo": str(best.get('releaseInfo', '')),
                    "description": best.get('description', '')
                }
    except Exception:
        pass
    return None

def fetch_live_trending_india():
    metas = []
    # 1. Try TMDb Discover API
    try:
        url = f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_KEY}&with_origin_country=IN&sort_by=popularity.desc&page=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get('results', [])
            
            shows_to_resolve = []
            for rank, show in enumerate(results[:20], 1):
                s_name = show.get('name')
                if s_name:
                    shows_to_resolve.append((rank, s_name))
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                metas = [m for m in list(executor.map(resolve_cinemeta_show, shows_to_resolve)) if m]
    except Exception as e:
        print(f"TMDb live fetch warning: {e}")
    
    # 2. Fallback / Augment with top Indian OTT series if needed
    if len(metas) < 15:
        fallback_tuples = [(i+1, name) for i, name in enumerate(TOP_INDIAN_OTT_SERIES)]
        with ThreadPoolExecutor(max_workers=5) as executor:
            f_metas = [m for m in list(executor.map(resolve_cinemeta_show, fallback_tuples)) if m]
        
        # Deduplicate
        existing_ids = set(m['id'] for m in metas)
        for fm in f_metas:
            if fm['id'] not in existing_ids:
                metas.append(fm)
                existing_ids.add(fm['id'])

    return metas

def get_trending_indian_series_cached():
    now = time.time()
    cache_key = "trending_indian_series"
    if cache_key in DYNAMIC_CACHE:
        cached_data, timestamp = DYNAMIC_CACHE[cache_key]
        if now - timestamp < 43200: # 12 hours TTL (Refreshes automatically every day!)
            return cached_data
    
    fresh_metas = fetch_live_trending_india()
    if fresh_metas:
        DYNAMIC_CACHE[cache_key] = (fresh_metas, now)
        return fresh_metas
    
    if cache_key in DYNAMIC_CACHE:
        return DYNAMIC_CACHE[cache_key][0]
    return []

# -------------------------------------------------------------
# 3. MANIFEST DEFINITIONS (6 SEPARATE ADDONS)
# -------------------------------------------------------------

# Manifest 1: Trending Indian Series Addon (Daily Refresh)
MANIFEST_TRENDING_INDIA = {
    "id": "org.antigravity.trendingindianseriesaddon",
    "version": "1.0.0",
    "name": "Trending Indian Series & OTT (Daily Refresh)",
    "description": "Live Stremio Addon featuring Trending Indian Web Series & TV Shows, refreshed daily automatically.",
    "types": ["series"],
    "catalogs": [
        {
            "type": "series",
            "id": "trending_indian_series",
            "name": "🔥 Trending Indian Web Series (Daily)"
        }
    ],
    "resources": ["catalog"],
    "idPrefixes": ["tt"]
}

# Manifest 2: Cartoons Addon
MANIFEST_CARTOONS = {
    "id": "org.antigravity.curatedcartoonsaddon",
    "version": "1.0.0",
    "name": "100 Curated Cartoons & Animated Movies",
    "description": "Custom Stremio Addon featuring 100 Classic, Modern, and Masterpiece Cartoons & Animated Movies.",
    "types": ["series", "movie"],
    "catalogs": [
        {
            "type": "series",
            "id": "curated_cartoons_series",
            "name": "100 Curated Cartoon Series"
        },
        {
            "type": "movie",
            "id": "curated_cartoons_movies",
            "name": "Animated Movies Masterpieces"
        }
    ],
    "resources": ["catalog"],
    "idPrefixes": ["tt"]
}

# Manifest 3: Anime Addon
MANIFEST_ANIME = {
    "id": "org.antigravity.underratedanimeaddon",
    "version": "1.0.0",
    "name": "100 Underrated Anime & Movies",
    "description": "Custom Stremio Addon featuring 100 Underrated Anime Series, OVAs, and Movies across all genres.",
    "types": ["series", "movie"],
    "catalogs": [
        {
            "type": "series",
            "id": "underrated_anime_series",
            "name": "100 Underrated Anime Series"
        },
        {
            "type": "movie",
            "id": "underrated_anime_movies",
            "name": "Underrated Anime Movies"
        }
    ],
    "resources": ["catalog"],
    "idPrefixes": ["tt"]
}

# Manifest 4: Underrated Indian Films Addon
MANIFEST_INDIAN = {
    "id": "org.antigravity.underratedindianfilmsaddon",
    "version": "1.0.0",
    "name": "50 Underrated Indian Films",
    "description": "Custom Stremio Addon featuring 50 Underrated Indian Films across languages.",
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

# Manifest 5: A24 & Underrated Hollywood Movies Addon
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

# Manifest 6: TV Shows Addon
MANIFEST_TV = {
    "id": "org.antigravity.top100tvshowsaddon",
    "version": "1.0.0",
    "name": "Top 100 TV Shows (21st Century)",
    "description": "Custom Stremio Addon featuring the Top 100 TV Shows of the 21st Century.",
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

# -------------------------------------------------------------
# 4. ROUTE HANDLERS
# -------------------------------------------------------------

@app.route('/')
@app.route('/index.html')
def home():
    host = request.headers.get('Host', 'localhost')
    scheme = request.headers.get('X-Forwarded-Proto', 'https')
    
    t_india_manifest_url = f"{scheme}://{host}/trending-india/manifest.json"
    t_india_stremio_link = f"stremio://{host}/trending-india/manifest.json"

    cartoons_manifest_url = f"{scheme}://{host}/cartoons/manifest.json"
    cartoons_stremio_link = f"stremio://{host}/cartoons/manifest.json"

    anime_manifest_url = f"{scheme}://{host}/anime/manifest.json"
    anime_stremio_link = f"stremio://{host}/anime/manifest.json"

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
        .container {{ max-width: 850px; margin: 0 auto; }}
        .card {{ background: #1c1c24; padding: 25px 30px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #2d2d3d; margin-bottom: 25px; text-align: left; }}
        h1 {{ color: #7b5bf2; font-size: 28px; margin-bottom: 10px; }}
        h2 {{ color: #fff; margin-top: 0; font-size: 20px; }}
        p {{ color: #a0a0b0; font-size: 15px; line-height: 1.5; }}
        .btn {{ display: inline-block; background: #7b5bf2; color: #fff; text-decoration: none; padding: 12px 24px; border-radius: 10px; font-weight: bold; font-size: 15px; margin-top: 15px; transition: transform 0.2s; }}
        .btn:hover {{ transform: scale(1.03); background: #6945e0; }}
        .badge {{ background: #ff9800; color: #000; font-size: 11px; padding: 3px 8px; border-radius: 6px; font-weight: bold; margin-left: 8px; text-transform: uppercase; }}
        code {{ background: #121218; padding: 10px 15px; border-radius: 8px; display: block; margin-top: 15px; word-break: break-all; color: #00e5ff; font-family: monospace; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 Custom Stremio Addons Directory</h1>
        <p style="margin-bottom: 30px;">Choose and install each addon independently into your Stremio client.</p>
        
        <div class="card" style="border-color: #ff9800;">
            <h2>🔥 Addon 1: Trending Indian Series & OTT <span class="badge">Live Daily Refresh</span></h2>
            <p>Refreshes automatically every 24 hours with live daily trending Indian Web Series & TV Shows (Panchayat, Mirzapur, Farzi, etc.).</p>
            <a class="btn" style="background: #ff9800; color: #000;" href="{t_india_stremio_link}">➕ Install Trending India Addon</a>
            <code>{t_india_manifest_url}</code>
        </div>

        <div class="card">
            <h2>🎨 Addon 2: 100 Curated Cartoons & Animated Movies</h2>
            <p>100 Classic & Modern Cartoon Series and Animated Movies (Disney, Pixar, DreamWorks, Cartoon Network).</p>
            <a class="btn" href="{cartoons_stremio_link}">➕ Install Cartoons Addon</a>
            <code>{cartoons_manifest_url}</code>
        </div>

        <div class="card">
            <h2>⛩️ Addon 3: 100 Underrated Anime & Movies</h2>
            <p>100 Underrated Anime Series, OVAs, and Movies across all genres.</p>
            <a class="btn" href="{anime_stremio_link}">➕ Install Anime Addon</a>
            <code>{anime_manifest_url}</code>
        </div>

        <div class="card">
            <h2>🇮🇳 Addon 4: 50 Underrated Indian Films</h2>
            <p>50 Underrated Indian Films across Hindi, Malayalam, Tamil, Bengali, Marathi, Assamese, and classic cinema.</p>
            <a class="btn" href="{indian_stremio_link}">➕ Install Indian Movies Addon</a>
            <code>{indian_manifest_url}</code>
        </div>

        <div class="card">
            <h2>🎬 Addon 5: A24 & Underrated Movies</h2>
            <p>Includes <b>50 Notable A24 Films</b> and <b>50 Underrated Gems (2010–2026)</b>.</p>
            <a class="btn" href="{movies_stremio_link}">➕ Install Hollywood Movies Addon</a>
            <code>{movies_manifest_url}</code>
        </div>

        <div class="card">
            <h2>🍿 Addon 6: Top 100 TV Shows</h2>
            <p>Includes the <b>Top 100 TV Shows of the 21st Century</b> (NYT List).</p>
            <a class="btn" href="{tv_stremio_link}">➕ Install TV Shows Addon</a>
            <code>{tv_manifest_url}</code>
        </div>
    </div>
</body>
</html>"""
    return html

# Routes for Trending Indian Series Addon
@app.route('/trending-india/manifest.json')
@app.route('/trending-india/manifest')
@app.route('/trending-india-series/manifest.json')
def trending_india_manifest():
    return jsonify(MANIFEST_TRENDING_INDIA)

# Routes for Cartoons Addon
@app.route('/cartoons/manifest.json')
@app.route('/cartoons/manifest')
def cartoons_manifest():
    return jsonify(MANIFEST_CARTOONS)

# Routes for Anime Addon
@app.route('/anime/manifest.json')
@app.route('/anime/manifest')
def anime_manifest():
    return jsonify(MANIFEST_ANIME)

# Routes for Indian Movies Addon
@app.route('/indian/manifest.json')
@app.route('/indian/manifest')
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
    if id_ == "trending_indian_series":
        metas = get_trending_indian_series_cached()
    elif id_ == "curated_cartoons_series":
        metas = CARTOON_SERIES_METAS
    elif id_ == "curated_cartoons_movies":
        metas = CARTOON_MOVIE_METAS
    elif id_ == "underrated_anime_series":
        metas = ANIME_SERIES_METAS
    elif id_ == "underrated_anime_movies":
        metas = ANIME_MOVIE_METAS
    elif id_ == "underrated_indian_movies":
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
