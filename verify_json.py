import json

with open("top100_metas.json", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total shows: {len(data)}")
for d in data:
    print(f"{d['rank']:3d}. {d['name']} ({d['releaseInfo']}) | {d['id']}")
