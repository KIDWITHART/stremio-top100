import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor

a24_movies = [
    (1, "Hereditary", "2018"),
    (2, "Midsommar", "2019"),
    (3, "The Witch", "2015"),
    (4, "The Lighthouse", "2019"),
    (5, "It Comes at Night", "2017"),
    (6, "Talk to Me", "2023"),
    (7, "Men", "2022"),
    (8, "X", "2022"),
    (9, "Pearl", "2022"),
    (10, "MaXXXine", "2024"),
    (11, "Saint Maud", "2019"),
    (12, "The Green Knight", "2021"),
    (13, "Enemy", "2013"),
    (14, "Under the Skin", "2013"),
    (15, "Beau Is Afraid", "2023"),
    (16, "Moonlight", "2016"),
    (17, "Room", "2015"),
    (18, "Lady Bird", "2017"),
    (19, "The Farewell", "2019"),
    (20, "Minari", "2020"),
    (21, "Waves", "2019"),
    (22, "First Reformed", "2017"),
    (23, "20th Century Women", "2016"),
    (24, "A Ghost Story", "2017"),
    (25, "The Disaster Artist", "2017"),
    (26, "Amy", "2015"),
    (27, "Zola", "2020"),
    (28, "The Whale", "2022"),
    (29, "Past Lives", "2023"),
    (30, "Aftersun", "2022"),
    (31, "The Souvenir", "2019"),
    (32, "The Souvenir: Part II", "2021"),
    (33, "C'mon C'mon", "2021"),
    (34, "Eighth Grade", "2018"),
    (35, "American Honey", "2016"),
    (36, "Everything Everywhere All at Once", "2022"),
    (37, "Uncut Gems", "2019"),
    (38, "Good Time", "2017"),
    (39, "Spring Breakers", "2012"),
    (40, "Swiss Army Man", "2016"),
    (41, "The Bling Ring", "2013"),
    (42, "Y2K", "2024"),
    (43, "Bodies Bodies Bodies", "2022"),
    (44, "Death Grip", "2023"),
    (45, "On the Rocks", "2020"),
    (46, "Ex Machina", "2014"),
    (47, "Civil War", "2024"),
    (48, "Marcel the Shell with Shoes On", "2021"),
    (49, "After Yang", "2021"),
    (50, "High Life", "2018")
]

underrated_movies = [
    (1, "Sound of My Voice", "2011"),
    (2, "Take Shelter", "2011"),
    (3, "The Hunt", "2012"),
    (4, "Blue Ruin", "2013"),
    (5, "The Spectacular Now", "2013"),
    (6, "Snowpiercer", "2013"),
    (7, "Cheap Thrills", "2013"),
    (8, "Prisoners", "2013"),
    (9, "Short Term 12", "2013"),
    (10, "The Kings of Summer", "2013"),
    (11, "The One I Love", "2014"),
    (12, "Cold in July", "2014"),
    (13, "The Guest", "2014"),
    (14, "Coherence", "2014"),
    (15, "Krisha", "2015"),
    (16, "The Invitation", "2015"),
    (17, "Green Room", "2015"),
    (18, "Anomalisa", "2015"),
    (19, "The Nice Guys", "2016"),
    (20, "Hell or High Water", "2016"),
    (21, "Swiss Army Man", "2016"),
    (22, "The Handmaiden", "2016"),
    (23, "Colossal", "2017"),
    (24, "Good Time", "2017"),
    (25, "Thoroughbreds", "2017"),
    (26, "Support the Girls", "2018"),
    (27, "Sorry to Bother You", "2018"),
    (28, "Destroyer", "2018"),
    (29, "The Endless", "2017"),
    (30, "High Life", "2018"),
    (31, "The Peanut Butter Falcon", "2019"),
    (32, "Booksmart", "2019"),
    (33, "The Nightingale", "2018"),
    (34, "Palm Springs", "2020"),
    (35, "The Vast of Night", "2019"),
    (36, "Sound of Metal", "2019"),
    (37, "Materna", "2020"),
    (38, "Pig", "2021"),
    (39, "The Green Knight", "2021"),
    (40, "Cha Cha Real Smooth", "2022"),
    (41, "The Novice", "2021"),
    (42, "Emily the Criminal", "2022"),
    (43, "The Greatest Beer Run Ever", "2022"),
    (44, "Fair Play", "2023"),
    (45, "Dream Scenario", "2023"),
    (46, "All of Us Strangers", "2023"),
    (47, "Sing Sing", "2023"),
    (48, "Furiosa: A Mad Max Saga", "2024"),
    (49, "I Saw the TV Glow", "2024"),
    (50, "Highest 2 Lowest", "2025"),
    (51, "Eleanor the Great", "2025"),
    (52, "Black Bag", "2025"),
    (53, "The Ballad of Wallis Island", "2025")
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

print("Resolving A24 Movies...")
with ThreadPoolExecutor(max_workers=10) as executor:
    a24_results = [r for r in list(executor.map(fetch_movie, a24_movies)) if r]
a24_results.sort(key=lambda x: x['rank'])

print("Resolving Underrated Movies...")
with ThreadPoolExecutor(max_workers=10) as executor:
    underrated_results = [r for r in list(executor.map(fetch_movie, underrated_movies)) if r]
underrated_results.sort(key=lambda x: x['rank'])

all_data = {
    "a24_movies": a24_results,
    "underrated_movies": underrated_results
}

with open("movies_metas.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2)

print(f"Resolved: {len(a24_results)} A24 movies, {len(underrated_results)} Underrated movies.")
