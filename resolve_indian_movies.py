import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor

indian_movies = [
    (1, "Ankhon Dekhi", "2013"),
    (2, "Peepli Live", "2010"),
    (3, "Udaan", "2010"),
    (4, "Chameli", "2003"),
    (5, "Dhobi Ghat", "2010"),
    (6, "Newton", "2017"),
    (7, "Titli", "2014"),
    (8, "Masaan", "2015"),
    (9, "Miss Lovely", "2012"),
    (10, "Gulaal", "2009"),
    (11, "No One Killed Jessica", "2011"),
    (12, "Shahid", "2012"),
    (13, "Aiyyaa", "2012"),
    (14, "Lakshya", "2004"),
    (15, "Rockford", "1999"),
    (16, "Ek Din Achanak", "1989"),
    (17, "Iqbal", "2005"),
    (18, "Antardwand", "2010"),
    (19, "Manorama Six Feet Under", "2007"),
    (20, "A Death in the Gunj", "2016"),
    (21, "Kumbalangi Nights", "2019"),
    (22, "Thondimuthalum Driksakshiyum", "2017"),
    (23, "Maheshinte Prathikaram", "2016"),
    (24, "Ee.Ma.Yau", "2018"),
    (25, "Kammatipaadam", "2016"),
    (26, "Chola", "2019"),
    (27, "Perumazhakkalam", "2004"),
    (28, "Ozhivudivasathe Kali", "2015"),
    (29, "Angamaly Diaries", "2017"),
    (30, "Aaranya Kaandam", "2011"),
    (31, "Kaakka Muttai", "2014"),
    (32, "Visaranai", "2015"),
    (33, "Kaadhal", "2004"),
    (34, "Pariyerum Perumal", "2018"),
    (35, "Peranbu", "2019"),
    (36, "Meghe Dhaka Tara", "1960"),
    (37, "Egaro", "2011"),
    (38, "Asha Jaoar Majhe", "2014"),
    (39, "Court", "2015"),
    (40, "Fandry", "2013"),
    (41, "Killa", "2014"),
    (42, "Deool", "2011"),
    (43, "Shwaas", "2004"),
    (44, "Aamis", "2019"),
    (45, "Village Rockstars", "2017"),
    (46, "Ottal", "2015"),
    (47, "Jaane Bhi Do Yaaro", "1983"),
    (48, "Om-Dar-B-Dar", "1988"),
    (49, "Salaam Bombay!", "1988"),
    (50, "Garam Hawa", "1973")
]

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch_movie(item):
    num, title, year = item
    encoded_title = urllib.parse.quote(title)
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
                    "name": best.get('name'),
                    "poster": best.get('poster'),
                    "background": best.get('background'),
                    "releaseInfo": best.get('releaseInfo'),
                    "description": best.get('description', '')
                }
    except Exception as e:
        pass
    return None

print("Resolving Underrated Indian Movies...")
with ThreadPoolExecutor(max_workers=10) as executor:
    results = [r for r in list(executor.map(fetch_movie, indian_movies)) if r]
results.sort(key=lambda x: x['rank'])

with open("indian_movies_metas.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Resolved: {len(results)}/50 Underrated Indian Movies.")
