# World Map Recall

A click-the-country world map quiz with Anki-style spaced repetition. A country's name appears; click it on the map. Countries you know come back less often, and ones you miss come back sooner.

Play it at https://rhymes-with-tree.github.io/mapstudy/, where it's saved in your browser.

## What's in it

- **245 places:** the 193 UN members plus Vatican City, Palestine, Taiwan, Kosovo, Western Sahara, the Cook Islands and Niue, and 45 territories with country codes of their own, such as Greenland (Denmark) and Puerto Rico (United States).
- **Borders as the UN draws them:** Crimea is part of Ukraine, the Golan Heights part of Syria, and Western Sahara separate from Morocco. Disputed land is striped.
- **Spaced repetition:** new countries are learned in steps of 1 and 10 minutes and then graduate to a day. After that, answers of Again, Hard, Good and Easy set the next review. The day starts at 4am.
- **Tries:** a wrong click says "Try again" and shades the wrong country. A right answer on a later try counts as Hard. Running out of tries, or pressing "I don't know", counts as Again.
- **No recolouring:** countries you've answered keep their colour, so later questions don't get easier by elimination.
- **Filters:** small nations only, UN members only, and any mix of continents and subregions. Land outside the picked regions fades.
- **Drill this view:** quiz only the countries on screen, without changing the schedule.
- **Mix-ups:** pairs of countries you confuse are counted, and each pair can be drilled.
- **Browse:** tap countries to see their names, without a quiz.
- **Sessions:** stop after 15 or 30 cards, or 10 or 20 minutes, with a summary at the end.
- **Direction of miss:** after a final wrong answer, the distance and compass direction to the right country.
- **Undo** the last answer with the button, U or Ctrl+Z.
- Light and dark themes.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole app: one page with inline CSS and JavaScript |
| `world.json` | Country outlines, fetched by the page |
| `disputed.json` | Disputed areas, drawn striped |
| `tools/prep_world.py` | Builds `world.json` from Natural Earth |
| `tools/un_borders.py` | Redraws disputed borders the UN's way and splits out territories |
| `tools/disputed.py` | Builds `disputed.json` |
| `tools/build_site.py` | Builds the web version into `docs/` for GitHub Pages |
| `docs/` | The web version: built, not edited by hand |

## Running it yourself

Serve the folder with any static web server and open `index.html`, for example:

```
python3 -m http.server 8000
```

Opened outside claude.ai, progress is saved in that browser only.

## The web version

GitHub Pages serves `docs/` from the `main` branch (Settings → Pages → Deploy from a branch → `main`, `/docs`). After changing `index.html`, `world.json` or `disputed.json`, rebuild it:

```
python3 tools/build_site.py
```

## Rebuilding the map data

Download `ne_50m_admin_0_countries.geojson` and `ne_50m_admin_0_breakaway_disputed_areas.geojson` from https://github.com/nvkelso/natural-earth-vector, then run:

```
python3 tools/prep_world.py ne_50m_admin_0_countries.geojson world.json
python3 tools/un_borders.py world.json ne_50m_admin_0_breakaway_disputed_areas.geojson world.json
python3 tools/disputed.py ne_50m_admin_0_breakaway_disputed_areas.geojson world.json disputed.json
```

`un_borders.py` needs shapely (`pip install shapely`), and runs once on a fresh `world.json`.

## Credits

| What | From | Terms |
|---|---|---|
| Country outlines and disputed areas | [Natural Earth](https://www.naturalearthdata.com/), 1:50m Admin 0 countries and breakaway and disputed areas | Public domain |
| Map drawing | [d3](https://d3js.org/) 7.9.0, loaded from cdnjs | ISC licence |
| Fonts | [Atkinson Hyperlegible](https://fonts.google.com/specimen/Atkinson+Hyperlegible) and [Bricolage Grotesque](https://fonts.google.com/specimen/Bricolage+Grotesque), loaded from Google Fonts | SIL Open Font License 1.1 |

Borders follow the UN's view, and disputed land is striped rather than given to either side; the rules are in `CLAUDE.md`. They are not a statement on any disputed territory.

## Licence

The code is under the MIT License; see `LICENSE`.
