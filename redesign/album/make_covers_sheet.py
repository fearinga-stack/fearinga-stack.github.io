"""All album covers on one page (covers.html), for choosing cover frames and title placement."""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
cfg = json.loads((HERE / "albums.json").read_text(encoding="utf-8"))
css = re.search(r"<style>(.*?)</style>", (HERE / "template.html").read_text(encoding="utf-8"), re.S).group(1)
rules, cells = [], []
for slug in cfg["order"]:
    s = (HERE / f"{slug}.html").read_text(encoding="utf-8")
    st = re.search(r"<style>(.*?)</style>", s, re.S).group(1)
    k = "c-" + slug.replace("_", "-")
    rules.append(re.search(r"\.cover\{.*?\}\n", st, re.S).group(0).replace(".cover{", f".{k} .cover{{"))
    rules.append(re.search(r"\.cover h2\{.*?\}\n", st, re.S).group(0).replace(".cover h2{", f".{k} .cover h2{{"))
    front = re.search(r'<div class="cover"><h2>.*?</div>', s).group(0)
    cells.append(f'<div><div class="cell {k}">{front}</div><small>{slug}</small></div>')
html = ('<!doctype html><html><head><meta charset="utf-8"><title>Album covers</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+SC:wght@400;500&display=swap"><style>'
        + css + "\n".join(rules)
        + 'body{display:block;overflow:auto;padding:20px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:18px}'
          '.cell{aspect-ratio:600/430}.cell small{display:block}small{color:#bbb;font:12px sans-serif}</style></head><body><div class="grid">'
        + "".join(cells) + "</div></body></html>")
(HERE / "covers.html").write_text(html, encoding="utf-8")
print("covers.html")
