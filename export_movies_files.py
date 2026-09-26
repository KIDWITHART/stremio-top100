import json
import csv

with open("movies_metas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

a24 = data["a24_movies"]
underrated = data["underrated_movies"]

# 1. Export CSVs
with open("a24_movies_trakt_import.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "Title", "Year", "IMDb_ID", "Stremio_Link"])
    for item in a24:
        stremio_link = f"stremio://detail/movie/{item['id']}"
        writer.writerow([item["rank"], item["name"], item["releaseInfo"], item["id"], stremio_link])

with open("underrated_movies_trakt_import.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "Title", "Year", "IMDb_ID", "Stremio_Link"])
    for item in underrated:
        stremio_link = f"stremio://detail/movie/{item['id']}"
        writer.writerow([item["rank"], item["name"], item["releaseInfo"], item["id"], stremio_link])

# 2. Export MDBList TXTs
with open("a24_movies_mdblist.txt", "w", encoding="utf-8") as f:
    for item in a24:
        f.write(f"{item['id']}\n")

with open("underrated_movies_mdblist.txt", "w", encoding="utf-8") as f:
    for item in underrated:
        f.write(f"{item['id']}\n")

# 3. Export Markdown catalog
with open("movies_playlist_catalog.md", "w", encoding="utf-8") as f:
    f.write("# 🎬 Curated Movie Playlists: A24 & Underrated Gems\n\n")
    
    f.write("## 🎨 50 Notable A24 Films\n\n")
    f.write("| Rank | Film Title | Year | IMDb ID | Quick Watch in Stremio |\n")
    f.write("| :---: | :--- | :---: | :---: | :--- |\n")
    for item in a24:
        stremio_app = f"stremio://detail/movie/{item['id']}"
        stremio_web = f"https://web.stremio.com/#/detail/movie/{item['id']}"
        f.write(f"| {item['rank']} | **{item['name']}** | {item['releaseInfo']} | `{item['id']}` | [Open App]({stremio_app}) • [Web Client]({stremio_web}) |\n")

    f.write("\n---\n\n")
    f.write("## 💎 50 Underrated Films (2010–2026)\n\n")
    f.write("| Rank | Film Title | Year | IMDb ID | Quick Watch in Stremio |\n")
    f.write("| :---: | :--- | :---: | :---: | :--- |\n")
    for item in underrated:
        stremio_app = f"stremio://detail/movie/{item['id']}"
        stremio_web = f"https://web.stremio.com/#/detail/movie/{item['id']}"
        f.write(f"| {item['rank']} | **{item['name']}** | {item['releaseInfo']} | `{item['id']}` | [Open App]({stremio_app}) • [Web Client]({stremio_web}) |\n")

print("Export files for movies created successfully!")
