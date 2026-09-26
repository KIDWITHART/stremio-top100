import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor

anime_list = [
    (1, "Serial Experiments Lain", "series", "1998", None),
    (2, "Boogiepop Phantom", "series", "2000", None),
    (3, "Paranoia Agent", "series", "2004", None),
    (4, "Texhnolyze", "series", "2003", None),
    (5, "Kaiba", "series", "2008", None),
    (6, "Mind Game", "movie", "2004", None),
    (7, "Shiki", "series", "2010", None),
    (8, "The Perfect Insider", "series", "2015", None),
    (9, "Zetsuen no Tempest", "series", "2012", None),
    (10, "Kuuchuu Buranko", "series", "2009", None),
    (11, "Planetes", "series", "2003", None),
    (12, "Time of Eve", "series", "2008", None),
    (13, "Ergo Proxy", "series", "2006", None),
    (14, "Casshern Sins", "series", "2008", None),
    (15, "Coppelion", "series", "2013", None),
    (16, "Space Brothers", "series", "2012", None),
    (17, "Kemonozume", "series", "2006", None),
    (18, "Eureka Seven", "series", "2005", None),
    (19, "Gunbuster", "series", "1988", None),
    (20, "Knights of Sidonia", "series", "2014", "tt3429340"),
    (21, "Aoi Bungaku Series", "series", "2009", None),
    (22, "Sonny Boy", "series", "2021", None),
    (23, "The Eccentric Family", "series", "2013", None),
    (24, "Wandering Son", "series", "2011", None),
    (25, "Natsume's Book of Friends", "series", "2008", None),
    (26, "Bunny Drop", "series", "2011", None),
    (27, "March Comes in Like a Lion", "series", "2016", None),
    (28, "A Place Further Than the Universe", "series", "2018", None),
    (29, "Barakamon", "series", "2014", None),
    (30, "Sangatsu no Lion OVA Specials", "series", "2016", None),
    (31, "Silver Spoon", "series", "2013", None),
    (32, "Honey and Clover", "series", "2005", None),
    (33, "Mushishi", "series", "2005", None),
    (34, "The Twelve Kingdoms", "series", "2002", None),
    (35, "Now and Then, Here and There", "series", "1999", None),
    (36, "Kino's Journey", "series", "2003", None),
    (37, "Haibane Renmei", "series", "2002", None),
    (38, "Vinland Saga", "series", "2019", None),
    (39, "Dorohedoro", "series", "2020", None),
    (40, "Made in Abyss", "series", "2017", None),
    (41, "The Vision of Escaflowne", "series", "1996", None),
    (42, "Fushigi Yuugi", "series", "1995", None),
    (43, "Nichijou", "series", "2011", None),
    (44, "Cromartie High School", "series", "2003", "tt0411835"),
    (45, "Space Dandy", "series", "2014", None),
    (46, "Gintama", "series", "2006", None),
    (47, "Grand Blue", "series", "2018", None),
    (48, "Great Teacher Onizuka", "series", "1999", None),
    (49, "Haven't You Heard? I'm Sakamoto", "series", "2016", None),
    (50, "Daily Lives of High School Boys", "series", "2012", None),
    (51, "Another", "series", "2012", None),
    (52, "Ghost Hound", "series", "2007", None),
    (53, "Requiem from the Darkness", "series", "2003", None),
    (54, "Shigurui: Death Frenzy", "series", "2007", "tt1069279"),
    (55, "Perfect Blue", "movie", "1997", None),
    (56, "Ping Pong the Animation", "series", "2014", None),
    (57, "Haikyuu!!", "series", "2014", None),
    (58, "Welcome to the Ballroom", "series", "2017", None),
    (59, "Chihayafuru", "series", "2011", None),
    (60, "Giant Killing", "series", "2010", None),
    (61, "RahXephon", "series", "2002", None),
    (62, "Gasaraki", "series", "1998", None),
    (63, "Aldnoah.Zero", "series", "2014", None),
    (64, "Broken Blade", "movie", "2010", None),
    (65, "Patlabor", "series", "1989", None),
    (66, "Shirobako", "series", "2014", None),
    (67, "Land of the Lustrous", "series", "2017", None),
    (68, "Girls' Last Tour", "series", "2017", None),
    (69, "Hyouka", "series", "2012", None),
    (70, "The Great Passage", "series", "2016", None),
    (71, "Perfect Blue", "movie", "1997", None),
    (72, "Millennium Actress", "movie", "2001", "tt0320480"),
    (73, "Paprika", "movie", "2006", None),
    (74, "In This Corner of the World", "movie", "2016", None),
    (75, "A Silent Voice", "movie", "2016", None),
    (76, "Wolf Children", "movie", "2012", None),
    (77, "The Girl Who Leapt Through Time", "movie", "2006", None),
    (78, "Mirai", "movie", "2018", None),
    (79, "5 Centimeters per Second", "movie", "2007", "tt0983213"),
    (80, "The Garden of Words", "movie", "2013", None),
    (81, "Patema Inverted", "movie", "2013", None),
    (82, "Belladonna of Sadness", "movie", "1973", None),
    (83, "Angel's Egg", "movie", "1985", None),
    (84, "Redline", "movie", "2009", None),
    (85, "Metropolis", "movie", "2001", None),
    (86, "Memories", "movie", "1995", None),
    (87, "Tokyo Godfathers", "movie", "2003", None),
    (88, "Grave of the Fireflies", "movie", "1988", None),
    (89, "Only Yesterday", "movie", "1991", None),
    (90, "Ocean Waves", "movie", "1993", None),
    (91, "Whisper of the Heart", "movie", "1995", None),
    (92, "The Wind Rises", "movie", "2013", None),
    (93, "Maquia: When the Promised Flower Blooms", "movie", "2018", None),
    (94, "A Letter to Momo", "movie", "2011", None),
    (95, "Colorful", "movie", "2010", None),
    (96, "The Anthem of the Heart", "movie", "2015", None),
    (97, "Josee, the Tiger and the Fish", "movie", "2020", None),
    (98, "Ride Your Wave", "movie", "2019", None),
    (99, "Lu Over the Wall", "movie", "2017", None),
    (100, "On-Gaku: Our Sound", "movie", "2019", None)
]

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch_anime(item):
    num, title, item_type, year, direct_imdb = item
    
    if direct_imdb:
        url = f"https://v3-cinemeta.strem.io/meta/{item_type}/{direct_imdb}.json"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                meta = data.get('meta', {})
                if meta:
                    return {
                        "rank": num,
                        "id": meta['id'],
                        "type": item_type,
                        "name": title,
                        "cinemeta_name": meta.get('name'),
                        "poster": meta.get('poster'),
                        "background": meta.get('background'),
                        "releaseInfo": meta.get('releaseInfo', year),
                        "description": meta.get('description', '')
                    }
        except Exception:
            pass

    encoded_title = urllib.parse.quote(title)
    types = [item_type, "movie" if item_type == "series" else "series"]
    for t in types:
        url = f"https://v3-cinemeta.strem.io/catalog/{t}/top/search={encoded_title}.json"
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
                        "type": best.get('type', t),
                        "name": title,
                        "cinemeta_name": best.get('name'),
                        "poster": best.get('poster'),
                        "background": best.get('background'),
                        "releaseInfo": best.get('releaseInfo'),
                        "description": best.get('description', '')
                    }
        except Exception:
            pass
    return None

print("Resolving Underrated Anime with IMDb fallbacks...")
with ThreadPoolExecutor(max_workers=10) as executor:
    results = [r for r in list(executor.map(fetch_anime, anime_list)) if r]
results.sort(key=lambda x: x['rank'])

with open("anime_metas.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Resolved: {len(results)}/100 Underrated Anime.")
