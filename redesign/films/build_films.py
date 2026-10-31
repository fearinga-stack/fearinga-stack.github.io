"""Build the films page as strips of film: one strip per film, its stills in sequence.

Reads films.html (title, logline, meta line, link) and assets/img/films/<slug>-hero/-still-N.
Writes redesign/films/index.html.  Run:  python build_films.py
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent
IMG = SITE / "assets" / "img" / "films"


def films():
    s = (SITE / "films.html").read_text(encoding="utf-8")
    main = re.search(r"<main.*?</main>", s, re.S).group(0)
    lead = re.search(r'<p class="lead">(.*?)</p>', main, re.S)
    out = []
    for card in re.findall(r'<article class="card">(.*?)</article>', main, re.S):
        link = re.search(r'<a href="([^"]+)"', card).group(1)
        slug = link.rsplit(".", 1)[0]
        title = re.sub("<[^>]+>", "", re.search(r"<h2>(.*?)</h2>", card, re.S).group(1)).strip()
        ps = re.findall(r"<p( class=\"meta\")?>(.*?)</p>", card, re.S)
        logline = next((p for c, p in ps if not c), "").strip()
        meta = next((p for c, p in ps if c), "").strip()
        frames = [f"{slug}-hero.jpg"] + sorted(p.name for p in IMG.glob(f"{slug}-still-*.jpg"))
        out.append(dict(slug=slug, link=link, title=title, logline=logline, meta=meta, frames=frames))
    return (lead.group(1).strip() if lead else ""), out


def strip(i, f):
    edge = f'{f["title"].upper()} · {f["meta"].upper()}'
    frames = "".join(
        f'<figure class="frame"><img src="../../assets/img/films/{name}" alt="Still {k + 1} from {html.escape(f["title"])}" '
        f'loading="lazy"><span class="fn">{i:02d}{"ABCDEFGH"[k]}</span></figure>'
        for k, name in enumerate(f["frames"]))
    return f'''  <article class="film">
    <a class="strip" href="../../{f["link"]}" aria-label="{html.escape(f["title"])}">
      <div class="perf"></div>
      <div class="edge top"><span>{html.escape(edge)}</span><span>AMATA LYNNER · RENDERED AT HOME</span><span>{html.escape(edge)}</span></div>
      <div class="frames">{frames}</div>
      <div class="edge bottom"><span>▸ {i:02d}</span><span>▸ {i:02d}A</span><span>▸ {i:02d}B</span><span>▸ {i:02d}C</span><span>▸ {i:02d}D</span></div>
      <div class="perf"></div>
    </a>
    <div class="caption"><h2><a href="../../{f["link"]}">{html.escape(f["title"])}</a></h2>
      <p class="logline">{f["logline"]}</p><p class="meta">{f["meta"]}</p></div>
  </article>'''


def main():
    lead, fs = films()
    body = "\n".join(strip(i + 1, f) for i, f in enumerate(fs))
    out = (HERE / "template.html").read_text(encoding="utf-8").replace("{{LEAD}}", lead).replace("{{FILMS}}", body)
    (HERE / "index.html").write_text(out, encoding="utf-8")
    for f in fs:
        print(f'{f["slug"]:22s} {len(f["frames"])} frames  {f["title"]}')


if __name__ == "__main__":
    main()
