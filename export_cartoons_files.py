import json
import csv

with open("cartoons_metas.json", "r", encoding="utf-8") as f:
    cartoons = json.load(f)

# 1. Export CSV
with open("cartoons_trakt_import.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "Title", "Type", "Year", "IMDb_ID", "Stremio_Link"])
    for item in cartoons:
        stremio_link = f"stremio://detail/{item['type']}/{item['id']}"
        writer.writerow([item["rank"], item["name"], item["type"], item["releaseInfo"], item["id"], stremio_link])

# 2. Export MDBList TXT
with open("cartoons_mdblist.txt", "w", encoding="utf-8") as f:
    for item in cartoons:
        f.write(f"{item['id']}\n")

# 3. Export Markdown catalog
with open("cartoons_catalog.md", "w", encoding="utf-8") as f:
    f.write("# 🎨 100 Curated Cartoons & Animated Movies\n\n")
    f.write("| Rank | Title | Type | Year | IMDb ID | Quick Watch in Stremio |\n")
    f.write("| :---: | :--- | :---: | :---: | :---: | :--- |\n")
    for item in cartoons:
        stremio_app = f"stremio://detail/{item['type']}/{item['id']}"
        stremio_web = f"https://web.stremio.com/#/detail/{item['type']}/{item['id']}"
        f.write(f"| {item['rank']} | **{item['name']}** | {item['type'].capitalize()} | {item['releaseInfo']} | `{item['id']}` | [Open App]({stremio_app}) • [Web Client]({stremio_web}) |\n")

print("Export files for cartoons created successfully!")
