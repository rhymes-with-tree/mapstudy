# World Map Recall

A click-the-country world map quiz with Anki-style spaced repetition. A country's name appears; click it on the map. Countries you know come back less often, and ones you miss come back sooner.

Play it at https://claude.ai/artifact/Po6m9MbbpMrpjwaSNNpKoQ. Your review progress is saved to your account there.

## What's in it

- **200 countries:** the 193 UN members plus Vatican City, Palestine, Taiwan, Kosovo, Western Sahara, the Cook Islands and Niue. Dependencies such as Greenland and Puerto Rico are on the map and can be clicked, but are never asked.
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
| `tools/prep_world.py` | Builds `world.json` from Natural Earth |

## Running it yourself

Serve the folder with any static web server and open `index.html`, for example:

```
python3 -m http.server 8000
```

Opened outside claude.ai, progress is saved in that browser only.

## Rebuilding the map data

Download `ne_50m_admin_0_countries.geojson` from https://github.com/nvkelso/natural-earth-vector, then run:

```
python3 tools/prep_world.py ne_50m_admin_0_countries.geojson world.json
```

## Credits

| What | From | Terms |
|---|---|---|
| Country outlines | [Natural Earth](https://www.naturalearthdata.com/), 1:50m Admin 0 countries | Public domain |
| Map drawing | [d3](https://d3js.org/) 7.9.0, loaded from cdnjs | ISC licence |
| Fonts | [Atkinson Hyperlegible](https://fonts.google.com/specimen/Atkinson+Hyperlegible) and [Bricolage Grotesque](https://fonts.google.com/specimen/Bricolage+Grotesque), loaded from Google Fonts | SIL Open Font License 1.1 |

Country names, borders and which places count as countries follow Natural Earth with a few changes listed in `CLAUDE.md`. They are not a statement on any disputed territory.

## Licence

The code is under the MIT License; see `LICENSE`.
