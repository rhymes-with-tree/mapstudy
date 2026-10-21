# World Map Recall

Click-the-country world map quiz with Anki-style spaced repetition. Built for Stellyn.

Published as a claude.ai artifact: https://claude.ai/artifact/Po6m9MbbpMrpjwaSNNpKoQ
Keep publishing to that same URL. Review progress is stored in that artifact's per-user database (`data/users/<id>/srs`, capabilities `db` + `user`), so a new artifact would start from zero.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole app: one page, inline CSS and JS. Loads d3 7.9.0 from cdnjs. |
| `world.json` | Country outlines, published alongside the page and fetched as `world.json`. Compact array: `[ADM0_A3, NAME, SUBREGION, REGION_UN, TYPE, MultiPolygon coords]`. |
| `tools/prep_world.py` | Builds `world.json` from Natural Earth `ne_50m_admin_0_countries.geojson` (github.com/nvkelso/natural-earth-vector). Run: `python3 tools/prep_world.py <geojson> world.json` |

### world.json build rules

- Uniform 3-decimal rounding and no line simplification. Simplifying each country separately makes neighboring borders stop matching, and then the thick coastline stroke shows through as slivers along inland borders.
- Exterior rings are clockwise and holes counterclockwise, as d3 expects. Holes are kept, so Italy has holes for San Marino and Vatican City, and South Africa has one for Lesotho.

## Countries

- 200 quizzable: 193 UN members plus Vatican City, Palestine, Taiwan, Kosovo, Western Sahara, Cook Islands, and Niue. Display names are in `NAMES`.
- `MINE` holds the 63 "small nations" codes, which is Stellyn's original list.
- `NON_UN` is the 7 non-UN entries.
- `ALIAS` maps map pieces to the quiz country they count as: N. Cyprus → Cyprus, Somaliland → Somalia, Åland → Finland.
- Region and subregion overrides:
  - Cyprus is in Europe / Southern Europe.
  - Mexico is in North America.
  - "Northern America" is renamed "North America".
- Dependencies (Greenland, Puerto Rico, Guam, and so on) appear on the map and are clickable, but are never quizzed.

## Scheduling (Anki-like)

- New cards: learning steps of 1 and 10 minutes, then graduate to 1 day. Easy graduates to 4 days.
- Review cards: Again sends the card to relearning (10 min) and halves the interval. Hard multiplies the interval by 1.2, Good by ease, Easy by ease × 1.3.
- Ease starts at 2.5, with a minimum of 1.3. Intervals get ±5% fuzz.
- The day starts at 4am.
- The new-card limit per day is shared across all filters.
- Tries per card (default 2): a wrong click shows "Try again" and shades the wrong pick. A right answer on a later try defaults to Hard. Running out of tries, or pressing "I don't know", counts as Again.
- Neighbor nudge: a country clicked by mistake has its review pulled to within a day. This applies to regular reviews only.

### Exposure rule

Any country whose name you saw becomes "exposed" and sits out of reviews for 10 minutes. Names are seen by tapping countries after an answer, in Browse, as a named wrong pick, or by drilling it.

- If an exposed country has to be shown anyway and you get it right, it doesn't count: "Correct, but not counted," and it comes back when the 10 minutes are up.
- A miss's own reveal does not expose that country, because it is in normal relearning.
- Exposure is kept in memory only and resets on reload.

## Features

- **Filters:** "Small nations only" and "UN members only" toggles, plus continent and subregion chips. A country is included if it matches any picked region.
- **Fading:** with regions picked, land outside them fades.
  - Fading goes by where each piece of land sits, not who owns it. A piece more than 40 map units from its country's main body takes the region of the nearest other country. French Guiana is South America, Martinique is Caribbean, the Canaries are Northern Africa.
  - This is so fading never reveals a piece's owner.
- **Drill this view:** quizzes only the countries whose main-body centroid is on screen.
  - It ignores due dates and doesn't change the schedule.
  - A country clears when found on the first try. Misses come back 2–3 cards later.
  - When a drill ends, all drilled countries are exposed.
- **Mix-ups:** wrong picks are counted as pairs in `state.confusions`. Progress lists them with a Drill button per pair and a "Drill all of these" button.
- **Browse:** tap countries to see names, with no quiz. Exposure applies.
- **Sessions:** stop after 15 or 30 cards, or 10 or 20 minutes. The summary shows answered, right first time, mix-ups, and how many are due in the next 24 hours.
- **Undo last answer:** a button, or U / Ctrl+Z. Restores the card and any nudged neighbors.
- **Direction of miss:** after a final wrong answer, shows distance in miles and km and a compass direction, with a dashed arrow from the click to the answer. Not shown during retries.
- **Zoom column:** zoom in/out, drill, browse, ATL/IND/PAC centering, pin, and globe.
  - The pin returns to the study area (the drill's starting view, otherwise the picked regions).
  - The globe always shows the whole world.
  - Labels show on hover, on long-press, and once on first visit.
- **After each card, zoom out to:** study area / whole world / stay.
- **Find card:** draggable (double-click resets its position). The answer panel can be folded to one line.
- **Read pause (optional):** clicks are ignored for 1 second after a new name appears, so the whole name gets read first.

## Map rendering decisions

- Natural Earth 1 projection, fitted to 1000 units wide. Each country is pre-built as a Path2D.
- The map wraps horizontally, so the Pacific is continuous. Maximum zoom is 4000× home.
- No dots or markers. Countries are clicked by their outlines (Stellyn's request).
- Coastlines: every outline is stroked thick first, then all land is filled, then thin borders are drawn. Only the water side of the thick stroke survives, so every coast and island gets a heavy edge.
- Microstates (largest piece no bigger than about 1°, roughly Luxembourg-sized) get a heavy outline all the way around, including land borders.
- Close calls: tapping near a microstate that is under 30px on screen, when more than one country is in range, zooms in instead of guessing. The next tap is exact. Countries are never offered as a list of names, because that would give the answer away.
- Clicks are tested smallest country first, so enclaves win. A water click within 6px of an outline counts as that outline.
- Answered countries are never recolored afterward. This is the reason the app exists: Seterra whitens answered countries, which makes the later ones easier.

## Design

- Palette from Stellyn's preferences: Rosy Copper #BD5538, Burnt Peach #E16A4A, Pacific Blue #73A7AE, Amber Honey #ECA818, Sage Green #6AA673, Fuchsia Plum #B94588.
- Light and dark themes are defined through CSS tokens.
- Fonts:
  - Atkinson Hyperlegible for the country name to find. It has wide letter spacing so the whole name gets read, not just the first letters.
  - Bricolage Grotesque for display text.

## Preferences for working on this

- Be literal; build exactly what's asked.
- Prefer tables in explanations.
- When asking a question, say why it's being asked.
- Never name files "final"; use versions or descriptive names.
