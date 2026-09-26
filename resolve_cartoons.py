import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor

cartoons_list = [
    (1, "Tom and Jerry", "series", "1940"),
    (2, "Looney Tunes", "series", "1930"),
    (3, "The Flintstones", "series", "1960"),
    (4, "Scooby-Doo, Where Are You!", "series", "1969"),
    (5, "The Jetsons", "series", "1962"),
    (6, "DuckTales", "series", "1987"),
    (7, "Tiny Toon Adventures", "series", "1990"),
    (8, "Animaniacs", "series", "1993"),
    (9, "Garfield and Friends", "series", "1988"),
    (10, "He-Man and the Masters of the Universe", "series", "1983"),
    (11, "The Simpsons", "series", "1989"),
    (12, "Batman: The Animated Series", "series", "1992"),
    (13, "Dragon Ball Z", "series", "1989"),
    (14, "Pokémon", "series", "1997"),
    (15, "SpongeBob SquarePants", "series", "1999"),
    (16, "Avatar: The Last Airbender", "series", "2005"),
    (17, "Samurai Jack", "series", "2001"),
    (18, "Courage the Cowardly Dog", "series", "1999"),
    (19, "Ed, Edd n Eddy", "series", "1999"),
    (20, "Dexter's Laboratory", "series", "1996"),
    (21, "The Powerpuff Girls", "series", "1998"),
    (22, "Codename: Kids Next Door", "series", "2002"),
    (23, "Johnny Bravo", "series", "1997"),
    (24, "Rugrats", "series", "1991"),
    (25, "Hey Arnold!", "series", "1996"),
    (26, "Recess", "series", "1997"),
    (27, "Kim Possible", "series", "2002"),
    (28, "Teen Titans", "series", "2003"),
    (29, "Justice League", "series", "2001"),
    (30, "X-Men: The Animated Series", "series", "1992"),
    (31, "Beavis and Butt-Head", "series", "1993"),
    (32, "King of the Hill", "series", "1997"),
    (33, "Family Guy", "series", "1999"),
    (34, "Futurama", "series", "1999"),
    (35, "South Park", "series", "1997"),
    (36, "Adventure Time", "series", "2010"),
    (37, "Gravity Falls", "series", "2012"),
    (38, "Steven Universe", "series", "2013"),
    (39, "Regular Show", "series", "2010"),
    (40, "Rick and Morty", "series", "2013"),
    (41, "BoJack Horseman", "series", "2014"),
    (42, "Bob's Burgers", "series", "2011"),
    (43, "Archer", "series", "2009"),
    (44, "The Legend of Korra", "series", "2012"),
    (45, "Star vs. the Forces of Evil", "series", "2015"),
    (46, "Amphibia", "series", "2019"),
    (47, "The Owl House", "series", "2020"),
    (48, "Infinity Train", "series", "2019"),
    (49, "Over the Garden Wall", "series", "2014"),
    (50, "Big Mouth", "series", "2017"),
    (51, "Harley Quinn", "series", "2019"),
    (52, "Invincible", "series", "2021"),
    (53, "Arcane", "series", "2021"),
    (54, "Castlevania", "series", "2017"),
    (55, "Primal", "series", "2019"),
    (56, "Blue Eye Samurai", "series", "2023"),
    (57, "Hilda", "series", "2018"),
    (58, "Bluey", "series", "2018"),
    (59, "Craig of the Creek", "series", "2018"),
    (60, "We Bare Bears", "series", "2015"),
    (61, "Naruto", "series", "2002"),
    (62, "One Piece", "series", "1999"),
    (63, "Attack on Titan", "series", "2013"),
    (64, "Fullmetal Alchemist: Brotherhood", "series", "2009"),
    (65, "Death Note", "series", "2006"),
    (66, "My Hero Academia", "series", "2016"),
    (67, "Demon Slayer: Kimetsu no Yaiba", "series", "2019"),
    (68, "Jujutsu Kaisen", "series", "2020"),
    (69, "Cowboy Bebop", "series", "1998"),
    (70, "Neon Genesis Evangelion", "series", "1995"),
    (71, "Hunter x Hunter", "series", "2011"),
    (72, "Sailor Moon", "series", "1992"),
    (73, "Bleach", "series", "2004"),
    (74, "Spy x Family", "series", "2022"),
    (75, "Mob Psycho 100", "series", "2016"),
    (76, "Vinland Saga", "series", "2019"),
    (77, "Snow White and the Seven Dwarfs", "movie", "1937"),
    (78, "Pinocchio", "movie", "1940"),
    (79, "The Lion King", "movie", "1994"),
    (80, "Beauty and the Beast", "movie", "1991"),
    (81, "Aladdin", "movie", "1992"),
    (82, "Toy Story", "movie", "1995"),
    (83, "Finding Nemo", "movie", "2003"),
    (84, "Up", "movie", "2009"),
    (85, "WALL·E", "movie", "2008"),
    (86, "Inside Out", "movie", "2015"),
    (87, "Coco", "movie", "2017"),
    (88, "Frozen", "movie", "2013"),
    (89, "Zootopia", "movie", "2016"),
    (90, "Encanto", "movie", "2021"),
    (91, "The Incredibles", "movie", "2004"),
    (92, "Ratatouille", "movie", "2007"),
    (93, "Moana", "movie", "2016"),
    (94, "Shrek", "movie", "2001"),
    (95, "How to Train Your Dragon", "movie", "2010"),
    (96, "Kung Fu Panda", "movie", "2008"),
    (97, "The Prince of Egypt", "movie", "1998"),
    (98, "Spider-Man: Into the Spider-Verse", "movie", "2018"),
    (99, "Spirited Away", "movie", "2001"),
    (100, "Your Name.", "movie", "2016")
]

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch_cartoon(item):
    num, title, item_type, year = item
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

print("Resolving Curated Cartoons & Animated Movies...")
with ThreadPoolExecutor(max_workers=10) as executor:
    results = [r for r in list(executor.map(fetch_cartoon, cartoons_list)) if r]
results.sort(key=lambda x: x['rank'])

with open("cartoons_metas.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Resolved: {len(results)}/100 Cartoons & Animated Movies.")
