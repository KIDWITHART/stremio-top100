import json
import csv

with open("anime_metas.json", "r", encoding="utf-8") as f:
    anime = json.load(f)

# 1. Export CSV
with open("anime_trakt_import.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "Title", "Type", "Year", "IMDb_ID", "Stremio_Link"])
    for item in anime:
        stremio_link = f"stremio://detail/{item['type']}/{item['id']}"
        writer.writerow([item["rank"], item["name"], item["type"], item["releaseInfo"], item["id"], stremio_link])

# 2. Export MDBList TXT
with open("anime_mdblist.txt", "w", encoding="utf-8") as f:
    for item in anime:
        f.write(f"{item['id']}\n")

# 3. Export Markdown catalog
with open("anime_catalog.md", "w", encoding="utf-8") as f:
    f.write("# ⛩️ 100 Underrated Anime & Movies Playlist\n\n")
    f.write("| Rank | Anime Title | Type | Year | IMDb ID | Quick Watch in Stremio |\n")
    f.write("| :---: | :--- | :---: | :---: | :---: | :--- |\n")
    for item in anime:
        stremio_app = f"stremio://detail/{item['type']}/{item['id']}"
        stremio_web = f"https://web.stremio.com/#/detail/{item['type']}/{item['id']}"
        f.write(f"| {item['rank']} | **{item['name']}** | {item['type'].capitalize()} | {item['releaseInfo']} | `{item['id']}` | [Open App]({stremio_app}) • [Web Client]({stremio_web}) |\n")

print("Export files for anime created successfully!")
