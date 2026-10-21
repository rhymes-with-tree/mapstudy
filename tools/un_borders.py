# Redraw disputed land the way the UN sees it, and split out territories drawn inside their country.
# tools/prep_world.py's world.json (Natural Earth 1:50m) draws some land as the side that controls it. Using Natural
# Earth's 1:50m breakaway and disputed areas, this moves:
#   Crimea from Russia to Ukraine, the Golan Heights from Israel to Syria, and the Moroccan-held part of
#   Western Sahara from Morocco to Western Sahara.
# The Chagos Islands stay a shape of their own (they're quizzed as "Chagos Islands (Mauritius)"); the game names
# Mauritius as their country, as the UN General Assembly voted in 2019.
# It also splits off overseas places that have their own ISO country code but are drawn inside their country's
# shape (French Guiana, Réunion, Svalbard…), so they can be quizzed on their own and don't light up with it.
# Places without a code of their own (Alaska, Hawaii, the Canaries, the Azores, Madeira) stay with their country.
# Run after tools/prep_world.py, once: python3 tools/un_borders.py world.json <ne_50m_admin_0_breakaway_disputed_areas.geojson> world.json
# Needs shapely (pip install shapely). Running it twice fails, as the territories are already split out.
import json, sys
from shapely.geometry import shape, mapping, MultiPolygon, Polygon
from shapely.geometry.polygon import orient
from shapely import set_precision
src, disputed, out = sys.argv[1:4]
MOVES = {"Crimea": ("RUS", "UKR"), "Golan Heights": ("ISR", "SYR"), "W. Sahara": ("MAR", "SAH")}
world = json.load(open(src, encoding="utf-8"))
areas = {f["properties"]["BRK_NAME"]: f for f in json.load(open(disputed, encoding="utf-8"))["features"]}
snap = lambda g: set_precision(g.buffer(0), 0.001)
geom = {row[0]: snap(MultiPolygon([Polygon(p[0], p[1:]) for p in row[5]])) for row in world}
for name, (frm, to) in MOVES.items():
    piece = snap(shape(areas[name]["geometry"]))
    geom[frm] = snap(geom[frm].difference(piece))
    geom[to] = snap(geom[to].union(piece))
def coords(g):
    polys = [g] if isinstance(g, Polygon) else [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)]
    res = []
    for p in polys:
        if p.area < 1e-6: continue          # drop slivers left where the two outlines don't quite meet
        p = orient(p, sign=-1.0)            # outer rings clockwise, holes counterclockwise, as in world.json
        res.append([[[round(x, 3), round(y, 3)] for x, y in r.coords] for r in [p.exterior, *p.interiors]])
    return res
changed = {c for pair in MOVES.values() for c in pair}
rows = [row[:5] + [coords(geom[row[0]])] if row[0] in changed else row for row in world]
# (code, name, subregion, region, country it's cut from, lon range, lat range)
SPLIT = [("GUF", "French Guiana", "South America", "Americas", "FRA", (-55, -51), (2, 6.5)),
  ("GLP", "Guadeloupe", "Caribbean", "Americas", "FRA", (-62, -60.9), (15.8, 16.6)),
  ("MTQ", "Martinique", "Caribbean", "Americas", "FRA", (-61.3, -60.7), (14.3, 14.95)),
  ("REU", "Réunion", "Eastern Africa", "Africa", "FRA", (55, 56), (-21.5, -20.8)),
  ("MYT", "Mayotte", "Eastern Africa", "Africa", "FRA", (44.9, 45.4), (-13.1, -12.5)),
  ("SJM", "Svalbard", "Northern Europe", "Europe", "NOR", (9, 35), (76, 81)),
  ("BES", "Bonaire, Sint Eustatius and Saba", "Caribbean", "Americas", "NLD", (-68.5, -62.9), (11.9, 17.7)),
  ("TKL", "Tokelau", "Polynesia", "Oceania", "NZL", (-173, -171), (-10, -8))]
byc = {r[0]: r for r in rows}
for code, name, sub, region, parent, (x0, x1), (y0, y1) in SPLIT:
    inbox = lambda p: all(x0 <= x <= x1 and y0 <= y <= y1 for x, y in p[0])
    take = [p for p in byc[parent][5] if inbox(p)]
    assert take, code
    byc[parent][5] = [p for p in byc[parent][5] if not inbox(p)]
    rows.append([code, name, sub, region, "Dependency", take])
# Natural Earth puts these in "Seven seas (open ocean)"; give them a region by what they're nearest to.
OCEAN = {"SGS": ("South America", "Americas"), "IOA": ("South-eastern Asia", "Asia"), "IOT": ("Eastern Africa", "Africa"),
  "ATF": ("Southern Ocean", "Southern Ocean"), "HMD": ("Southern Ocean", "Southern Ocean")}
for r in rows:
    if r[0] in OCEAN: r[2], r[3] = OCEAN[r[0]]
json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
for c in sorted(changed): print(c, len(geom[c].geoms) if hasattr(geom[c], "geoms") else 1, "pieces")
