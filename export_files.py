import json
import csv

with open("top100_metas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 1. Export CSV
with open("top100_shows_trakt_import.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "Title", "Year", "IMDb_ID", "Stremio_Link"])
    for item in data:
        stremio_link = f"stremio://detail/series/{item['id']}"
        writer.writerow([item["rank"], item["name"], item["releaseInfo"], item["id"], stremio_link])

# 2. Export MDBList txt (IMDb IDs only)
with open("top100_shows_mdblist.txt", "w", encoding="utf-8") as f:
    for item in data:
        f.write(f"{item['id']}\n")

# 3. Export Markdown list
with open("top100_shows_playlist.md", "w", encoding="utf-8") as f:
    f.write("# 🍿 Top 100 TV Shows of the 21st Century — Stremio Playlist\n\n")
    f.write("| Rank | Show Title | Years | IMDb ID | Quick Watch in Stremio |\n")
    f.write("| :---: | :--- | :---: | :---: | :--- |\n")
    for item in data:
        stremio_app = f"stremio://detail/series/{item['id']}"
        stremio_web = f"https://web.stremio.com/#/detail/series/{item['id']}"
        f.write(f"| {item['rank']} | **{item['name']}** | {item['releaseInfo']} | `{item['id']}` | [Open App]({stremio_app}) • [Web Client]({stremio_web}) |\n")

print("All export files created successfully!")
