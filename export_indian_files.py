import json
import csv

with open("indian_movies_metas.json", "r", encoding="utf-8") as f:
    indian = json.load(f)

# 1. Export CSV
with open("indian_movies_trakt_import.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "Title", "Year", "IMDb_ID", "Stremio_Link"])
    for item in indian:
        stremio_link = f"stremio://detail/movie/{item['id']}"
        writer.writerow([item["rank"], item["name"], item["releaseInfo"], item["id"], stremio_link])

# 2. Export MDBList TXT
with open("indian_movies_mdblist.txt", "w", encoding="utf-8") as f:
    for item in indian:
        f.write(f"{item['id']}\n")

# 3. Export Markdown catalog
with open("indian_movies_catalog.md", "w", encoding="utf-8") as f:
    f.write("# 🇮🇳 50 Underrated Indian Films Across Languages\n\n")
    f.write("| Rank | Film Title | Year | IMDb ID | Quick Watch in Stremio |\n")
    f.write("| :---: | :--- | :---: | :---: | :--- |\n")
    for item in indian:
        stremio_app = f"stremio://detail/movie/{item['id']}"
        stremio_web = f"https://web.stremio.com/#/detail/movie/{item['id']}"
        f.write(f"| {item['rank']} | **{item['name']}** | {item['releaseInfo']} | `{item['id']}` | [Open App]({stremio_app}) • [Web Client]({stremio_web}) |\n")

print("Export files for Indian movies created successfully!")
