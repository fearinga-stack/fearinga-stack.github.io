"""Build the films page as strips of film: one strip per film, its stills in sequence.

Reads films.html (title, logline, meta line, link) and assets/img/films/<slug>-hero/-still-N.
Writes redesign/films/index.html.  Run:  python build_films.py
"""
import html
import json
import re
import struct
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


def jpeg_size(path):
    data = path.read_bytes()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return 16, 9


def title_card(f, extra):
    laurels = "".join(f'<img src="laurels/{n}" alt="">' for n in extra.get("laurels", []))
    lau = f'<div class="laurels">{laurels}</div>' if laurels else ""
    if extra.get("title_image"):
        # a real title frame from the film; laurels sit under the title
        return (f'<figure class="frame titlecard real"><img src="{extra["title_image"]}" alt="Title of {html.escape(f["title"])}">'
                f'{lau}<span class="fn">00</span></figure>')
    w, h = jpeg_size(IMG / f["frames"][0])
    return (f'<figure class="frame titlecard" style="aspect-ratio:{w}/{h}">'
            f'<div class="tc"><span class="tc-title">{html.escape(f["title"])}</span>{lau}</div>'
            f'<span class="fn">00</span></figure>')


def strip(i, f, extra):
    edge = f'{f["title"].upper()} · {f["meta"].upper()}'
    srcs = extra.get("frames") or [f"../../assets/img/films/{name}" for name in f["frames"]]
    frames = "".join(
        f'<figure class="frame"><img src="{src}" alt="Still {k + 1} from {html.escape(f["title"])}" '
        f'loading="lazy"><span class="fn">{i:02d}{"ABCDEFGH"[k]}</span></figure>'
        for k, src in enumerate(srcs))
    if not extra.get("no_title_card"):        # some films open on their own title already
        frames = title_card(f, extra) + frames
    awards = f'<p class="awards">{html.escape(extra["awards"])}</p>' if extra.get("awards") else ""
    one = f'''<div class="set">
        <div class="perf"></div>
        <div class="edge top"><span>{html.escape(edge)}</span><span>AMATA LYNNER · RENDERED AT HOME</span><span>{html.escape(edge)}</span></div>
        <div class="frames">{frames}</div>
        <div class="edge bottom"><span>▸ {i:02d}</span><span>▸ {i:02d}A</span><span>▸ {i:02d}B</span><span>▸ {i:02d}C</span><span>▸ {i:02d}D</span></div>
        <div class="perf"></div>
      </div>'''
    # three identical lengths of film: the page keeps the view on the middle one, so the strip has no end
    return f'''  <article class="film">
    <a class="strip" href="../../{f["link"]}" aria-label="{html.escape(f["title"])}">
      <div class="reel">{one}{one.replace('<div class="set">', '<div class="set" aria-hidden="true">')}{one.replace('<div class="set">', '<div class="set" aria-hidden="true">')}</div>
    </a>
    <div class="caption"><h2><a href="../../{f["link"]}">{html.escape(f["title"])}</a></h2>
      <p class="logline">{f["logline"]}</p><p class="meta">{f["meta"]}</p>{awards}</div>
  </article>'''


def main():
    lead, fs = films()
    extra = json.loads((HERE / "films.json").read_text(encoding="utf-8"))
    body = "\n".join(strip(i + 1, f, extra.get(f["slug"], {})) for i, f in enumerate(fs))
    out = (HERE / "template.html").read_text(encoding="utf-8").replace("{{LEAD}}", lead).replace("{{FILMS}}", body)
    (HERE / "index.html").write_text(out, encoding="utf-8")
    for f in fs:
        print(f'{f["slug"]:22s} {len(f["frames"])} frames  {f["title"]}')


if __name__ == "__main__":
    main()
