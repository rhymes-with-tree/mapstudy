# The disputed areas drawn with stripes (World Map Recall and Cat Atlas), from Natural Earth's 1:50m breakaway and disputed areas.
# The rule (the owner's): stripe land where the map, drawn the UN's way, and whoever actually runs it disagree; or a
# region split by a ceasefire line where the UN takes no view on which side is whose. So the Koreas aren't striped
# (the UN has both as member states, each with its own side). Palestine isn't striped either: Israel runs much of the
# West Bank, but this map data can't show which parts, and striping all of it would mark land Palestinians do run.
# Natural Earth's other disputed areas are drawn plainly, as the country that runs them. Every dispute, striped or not,
# belongs in the disputed-territory round.
# Western Sahara is striped whole (Natural Earth's shape is only the Moroccan-held part), so its outline comes from
# the game's map.
# Run: python3 tools/disputed.py <ne_50m_admin_0_breakaway_disputed_areas.geojson> world.json disputed.json
# (world.json after tools/un_borders.py; Western Sahara's outline comes from it)
import json, sys
src, world, out = sys.argv[1:4]
STRIPED = {
  # drawn as one country, run by another (or by itself)
  "Crimea", "Donetsk People's Republic", "Luhansk People's Republic", "Golan Heights", "N. Cyprus", "Somaliland",
  "Abkhazia", "South Ossetia", "Transnistria", "Abyei",
  # held along a ceasefire line or line of control, not an agreed border
  "Jammu and Kashmir", "Gilgit-Baltistan", "Siachen Glacier", "Shaksam Valley", "Aksai Chin", "Arunachal Pradesh",
  "Tirpani Valleys", "Bara Hotii Valleys", "Demchok", "Samdu Valleys"}
# Not striped: Kuril Is. (drawn as Russia, run by Russia), Ilemi Triangle (Kenya), Lawa and Courantyne Headwaters
# (France, Guyana), Junagadh and Manavadar (India), Artsakh (Azerbaijan has run it since 2023), North Borneo.
def signed(r): return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(r, r[1:])) / 2
def wind(ring, outer):
    # d3 (World Map Recall) needs outer rings clockwise and holes counterclockwise; Natural Earth's GeoJSON runs the other way
    return ring[::-1] if (signed(ring) > 0) == outer else ring
rows = []
for f in json.load(open(src, encoding="utf-8"))["features"]:
    p, g = f["properties"], f["geometry"]
    if p["BRK_NAME"] not in STRIPED: continue
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    rows.append([p["BRK_NAME"], p["NOTE_BRK"], [[wind([[round(x, 3), round(y, 3)] for x, y in r], i == 0) for i, r in enumerate(poly)] for poly in polys]])
assert len(rows) == len(STRIPED), sorted(STRIPED - {r[0] for r in rows})
sah = next(r for r in json.load(open(world, encoding="utf-8")) if r[0] == "SAH")
rows.append(["Western Sahara", "Claimed by Morocco", sah[5]])
json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(rows), "striped areas")
