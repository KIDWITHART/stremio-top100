import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor

indian_movies = [
    (1, "Ankhon Dekhi", "2013", ["Ankhon Dekhi"], None),
    (2, "Peepli Live", "2010", ["Peepli Live"], None),
    (3, "Udaan", "2010", ["Udaan"], None),
    (4, "Chameli", "2003", ["Chameli"], None),
    (5, "Dhobi Ghat", "2010", ["Dhobi Ghat", "Mumbai Diaries"], "tt1433810"),
    (6, "Newton", "2017", ["Newton"], None),
    (7, "Titli", "2014", ["Titli"], "tt3505704"),
    (8, "Masaan", "2015", ["Masaan"], None),
    (9, "Miss Lovely", "2012", ["Miss Lovely"], None),
    (10, "Gulaal", "2009", ["Gulaal"], None),
    (11, "No One Killed Jessica", "2011", ["No One Killed Jessica"], None),
    (12, "Shahid", "2012", ["Shahid"], None),
    (13, "Aiyyaa", "2012", ["Aiyyaa"], None),
    (14, "Lakshya", "2004", ["Lakshya"], None),
    (15, "Rockford", "1999", ["Rockford"], "tt0210960"),
    (16, "Ek Din Achanak", "1989", ["Ek Din Achanak"], "tt0097261"),
    (17, "Iqbal", "2005", ["Iqbal"], None),
    (18, "Antardwand", "2010", ["Antardwand"], "tt1695759"),
    (19, "Manorama Six Feet Under", "2007", ["Manorama Six Feet Under"], "tt1043940"),
    (20, "A Death in the Gunj", "2016", ["A Death in the Gunj"], None),
    (21, "Kumbalangi Nights", "2019", ["Kumbalangi Nights"], None),
    (22, "Thondimuthalum Driksakshiyum", "2017", ["Thondimuthalum Driksakshiyum", "Thondimuthalum"], None),
    (23, "Maheshinte Prathikaram", "2016", ["Maheshinte Prathikaram", "Maheshinte"], None),
    (24, "Ee.Ma.Yau", "2018", ["Ee Ma Yau", "Ee.Ma.Yau"], None),
    (25, "Kammatipaadam", "2016", ["Kammatipaadam", "Kammatti Paadam"], None),
    (26, "Chola", "2019", ["Chola", "Shadow of Water"], None),
    (27, "Perumazhakkalam", "2004", ["Perumazhakkalam"], "tt0438318"),
    (28, "Ozhivudivasathe Kali", "2015", ["Ozhivudivasathe Kali", "An Off-Day Game"], None),
    (29, "Angamaly Diaries", "2017", ["Angamaly Diaries"], None),
    (30, "Aaranya Kaandam", "2011", ["Aaranya Kaandam"], "tt1728285"),
    (31, "Kaakka Muttai", "2014", ["Kaakka Muttai", "The Crow's Egg"], None),
    (32, "Visaranai", "2015", ["Visaranai", "Interrogation"], None),
    (33, "Kaadhal", "2004", ["Kaadhal"], None),
    (34, "Pariyerum Perumal", "2018", ["Pariyerum Perumal"], "tt8097030"),
    (35, "Peranbu", "2019", ["Peranbu", "Resurrection"], None),
    (36, "Meghe Dhaka Tara", "1960", ["Meghe Dhaka Tara", "The Cloud-Capped Star"], None),
    (37, "Egaro", "2011", ["Egaro"], None),
    (38, "Asha Jaoar Majhe", "2014", ["Asha Jaoar Majhe", "Labor of Love"], None),
    (39, "Court", "2015", ["Court"], "tt3799658"),
    (40, "Fandry", "2013", ["Fandry"], None),
    (41, "Killa", "2014", ["Killa", "The Fort"], None),
    (42, "Deool", "2011", ["Deool"], "tt2071477"),
    (43, "Shwaas", "2004", ["Shwaas"], "tt0425455"),
    (44, "Aamis", "2019", ["Aamis", "Ravening"], None),
    (45, "Village Rockstars", "2017", ["Village Rockstars"], None),
    (46, "Ottal", "2015", ["Ottal", "The Trap"], None),
    (47, "Jaane Bhi Do Yaaro", "1983", ["Jaane Bhi Do Yaaro"], None),
    (48, "Om-Dar-B-Dar", "1988", ["Om Dar B Dar", "Om-Dar-B-Dar"], None),
    (49, "Salaam Bombay!", "1988", ["Salaam Bombay!"], None),
    (50, "Garam Hawa", "1973", ["Garam Hawa", "Scorching Winds"], None)
]

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch_movie(item):
    num, canonical_title, year, queries, direct_imdb = item
    
    # Try direct IMDb endpoint if available
    if direct_imdb:
        url = f"https://v3-cinemeta.strem.io/meta/movie/{direct_imdb}.json"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                meta = data.get('meta', {})
                if meta:
                    return {
                        "rank": num,
                        "id": meta['id'],
                        "type": "movie",
                        "name": canonical_title,
                        "cinemeta_name": meta.get('name'),
                        "poster": meta.get('poster'),
                        "background": meta.get('background'),
                        "releaseInfo": meta.get('releaseInfo', year),
                        "description": meta.get('description', '')
                    }
        except Exception:
            pass

    for q in queries:
        encoded_title = urllib.parse.quote(q)
        url = f"https://v3-cinemeta.strem.io/catalog/movie/top/search={encoded_title}.json"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                metas = data.get('metas', [])
                if metas:
                    best = None
                    for m in metas:
                        rel = str(m.get('releaseInfo', ''))
                        if year in rel or rel.startswith(year):
                            best = m
                            break
                    if not best:
                        best = metas[0]
                    return {
                        "rank": num,
                        "id": best['id'],
                        "type": "movie",
                        "name": canonical_title,
                        "cinemeta_name": best.get('name'),
                        "poster": best.get('poster'),
                        "background": best.get('background'),
                        "releaseInfo": best.get('releaseInfo'),
                        "description": best.get('description', '')
                    }
        except Exception:
            pass
    return None

print("Resolving Underrated Indian Movies with IMDb fallback...")
with ThreadPoolExecutor(max_workers=10) as executor:
    results = [r for r in list(executor.map(fetch_movie, indian_movies)) if r]
results.sort(key=lambda x: x['rank'])

with open("indian_movies_metas.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Resolved: {len(results)}/50 Underrated Indian Movies.")
