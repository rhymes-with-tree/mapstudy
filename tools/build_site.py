# Builds the web version of World Map Recall into docs/, for GitHub Pages.
# index.html has no page of its own around it (doctype, charset, viewport and a few base styles); this adds one, and
# copies the map data next to it. Progress stays in each person's browser.
# Run from the repo root after changing index.html, world.json or disputed.json: python3 tools/build_site.py
import os, shutil
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;padding:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
os.makedirs("docs", exist_ok=True)
page = open("index.html", encoding="utf-8").read()
open("docs/index.html", "w", encoding="utf-8").write(HEAD + page + "\n</body>\n</html>\n")
for f in ("world.json", "disputed.json"): shutil.copy(f, os.path.join("docs", f))
open("docs/.nojekyll", "w").close()   # serve the files as they are, without GitHub's Jekyll step
print("docs/ built")
