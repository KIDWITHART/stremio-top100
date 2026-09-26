import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor

shows = [
    (1, "Breaking Bad", "2008"),
    (2, "The Wire", "2002"),
    (3, "Mad Men", "2007"),
    (4, "Succession", "2018"),
    (5, "Fleabag", "2016"),
    (6, "Game of Thrones", "2011"),
    (7, "Veep", "2012"),
    (8, "30 Rock", "2006"),
    (9, "Curb Your Enthusiasm", "2000"),
    (10, "Atlanta", "2016"),
    (11, "The Office", "2005"),
    (12, "Arrested Development", "2003"),
    (13, "Girls", "2012"),
    (14, "Friday Night Lights", "2006"),
    (15, "Six Feet Under", "2001"),
    (16, "The Office", "2001"),
    (17, "The Americans", "2013"),
    (18, "I May Destroy You", "2020"),
    (19, "Chernobyl", "2019"),
    (20, "The Crown", "2016"),
    (21, "The White Lotus", "2021"),
    (22, "Lost", "2004"),
    (23, "The Comeback", "2005"),
    (24, "Deadwood", "2004"),
    (25, "The Leftovers", "2014"),
    (26, "Black Mirror", "2011"),
    (27, "Better Call Saul", "2015"),
    (28, "Band of Brothers", "2001"),
    (29, "Key & Peele", "2012"),
    (30, "Severance", "2022"),
    (31, "Survivor", "2000"),
    (32, "Andor", "2022"),
    (33, "Enlightened", "2011"),
    (34, "Schitt's Creek", "2015"),
    (35, "True Detective", "2014"),
    (36, "The Pitt", "2025"),
    (37, "Battlestar Galactica", "2005"),
    (38, "Homeland", "2011"),
    (39, "Watchmen", "2019"),
    (40, "Adolescence", "2025"),
    (41, "Louie", "2010"),
    (42, "Hacks", "2021"),
    (43, "Peaky Blinders", "2013"),
    (44, "BoJack Horseman", "2014"),
    (45, "Happy Valley", "2014"),
    (46, "Broad City", "2014"),
    (47, "Twin Peaks", "2017"),
    (48, "House of Cards", "2013"),
    (49, "Normal People", "2020"),
    (50, "Parks and Recreation", "2009"),
    (51, "The Good Place", "2016"),
    (52, "Downton Abbey", "2010"),
    (53, "Stranger Things", "2016"),
    (54, "The Bureau", "2015"),
    (55, "Insecure", "2018"),
    (56, "Nathan for You", "2013"),
    (57, "I Think You Should Leave with Tim Robinson", "2019"),
    (58, "Chappelle's Show", "2003"),
    (59, "PEN15", "2019"),
    (60, "Peep Show", "2003"),
    (61, "RuPaul's Drag Race", "2009"),
    (62, "Slow Horses", "2022"),
    (63, "The Thick of It", "2005"),
    (64, "Anthony Bourdain: Parts Unknown", "2013"),
    (65, "Mare of Easttown", "2021"),
    (66, "The Rehearsal", "2022"),
    (67, "The Handmaid's Tale", "2017"),
    (68, "Ozark", "2017"),
    (69, "Anthony Bourdain: No Reservations", "2005"),
    (70, "The Shield", "2002"),
    (71, "Beef", "2023"),
    (72, "Squid Game", "2021"),
    (73, "Barry", "2018"),
    (74, "The Bear", "2022"),
    (75, "Ted Lasso", "2020"),
    (76, "Somebody Somewhere", "2022"),
    (77, "Modern Family", "2009"),
    (78, "It's Always Sunny in Philadelphia", "2005"),
    (79, "The Good Wife", "2009"),
    (80, "How To with John Wilson", "2020"),
    (81, "The Queen's Gambit", "2020"),
    (82, "Better Things", "2016"),
    (83, "Justified", "2010"),
    (84, "Planet Earth", "2006"),
    (85, "The Great British Bake Off", "2010"),
    (86, "Shogun", "2024"),
    (87, "Reservation Dogs", "2021"),
    (88, "Dexter", "2006"),
    (89, "Baby Reindeer", "2024"),
    (90, "Eastbound & Down", "2009"),
    (91, "Catastrophe", "2015"),
    (92, "The Night Of", "2016"),
    (93, "Station Eleven", "2021"),
    (94, "The Diplomat", "2023"),
    (95, "House", "2004"),
    (96, "Halt and Catch Fire", "2014"),
    (97, "Community", "2009"),
    (98, "The OA", "2016"),
    (99, "Gilmore Girls", "2000"),
    (100, "Scandal", "2012")
]

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch_show(item):
    num, title, year = item
    encoded_title = urllib.parse.quote(title)
    url = f"https://v3-cinemeta.strem.io/catalog/series/top/search={encoded_title}.json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
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
                    "type": best.get('type', 'series'),
                    "name": best.get('name'),
                    "poster": best.get('poster'),
                    "background": best.get('background'),
                    "releaseInfo": best.get('releaseInfo'),
                    "description": best.get('description', '')
                }
    except Exception as e:
        pass
    return None

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_show, shows))

valid_results = [r for r in results if r is not None]
valid_results.sort(key=lambda x: x['rank'])

with open("top100_metas.json", "w", encoding="utf-8") as f:
    json.dump(valid_results, f, indent=2)

print(f"DONE: {len(valid_results)}/100 resolved.")
