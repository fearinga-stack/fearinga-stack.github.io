"""Rebuild each film page in the new style, keeping every block of the old page in order.

Old page (root/<slug>.html)  ->  redesign/films/<slug>.html
  header.film-hero   -> the film's endless strip + the observation card (title, tag, meta, laurels)
  section.band       -> lead, large italic
  section.watch      -> label, optional paragraph, the video
  section.prose      -> label(s), paragraphs, notes
  section.columns    -> card rows: label on the left, text on the right
  section.stills     -> dropped: the strip at the top shows the film
  nav.pager          -> links between films, rewritten to the new pages

Run after build_films.py:  python build_film_pages.py
"""
import html
import json
import re
from pathlib import Path

import build_films as bf

HERE = bf.HERE
SITE = bf.SITE
PAGES = ["step-sequence", "plus", "nominal", "wearenotalone", "06percents", "scent-of-imagination"]


def img_src(src):
    return "../../" + src.lstrip("./").replace("../", "")


def inner(tag_html):
    return tag_html[tag_html.index(">") + 1:tag_html.rindex("<")]


def blocks(chunk):
    """h2.label / p / p.note / iframe / figure, in order."""
    out = []
    for m in re.finditer(r'<h2[^>]*class="label"[^>]*>.*?</h2>|<p[^>]*>.*?</p>|<iframe.*?</iframe>|<figure.*?</figure>', chunk, re.S):
        t = m.group(0)
        if t.startswith("<h2"):
            out.append(("label", inner(t).strip()))
        elif t.startswith("<iframe"):
            src = re.search(r'src="([^"]+)"', t).group(1)
            title = re.search(r'title="([^"]*)"', t)
            out.append(("video", src, title.group(1) if title else ""))
        elif t.startswith("<figure"):
            s = re.search(r'src="([^"]+)"', t)
            if s:
                out.append(("img", img_src(s.group(1))))
        else:
            cls = re.search(r'class="([^"]+)"', t[:t.index(">")])
            out.append(("note" if cls and "note" in cls.group(1) else "p", inner(t).strip()))
    return out


def render_flow(items):
    parts = []
    for it in items:
        if it[0] == "label":
            parts.append(f'<h2 class="label">{it[1]}</h2>')
        elif it[0] == "p":
            parts.append(f"<p>{it[1]}</p>")
        elif it[0] == "note":
            parts.append(f'<aside class="note"><p>{it[1]}</p></aside>')
        elif it[0] == "video":
            parts.append(f'<div class="screen"><iframe src="{it[1]}" title="{it[2]}" loading="lazy" '
                         f'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
                         f'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>')
    return "\n".join(parts)


def page_link(href):
    slug = href.rsplit(".", 1)[0]
    if slug == "films":
        return "index.html"
    return f"{slug}.html" if slug in PAGES else "../../" + href


def build(slug, i, extra_all, film_meta):
    s = (SITE / f"{slug}.html").read_text(encoding="utf-8")
    art = re.search(r'<article class="film">(.*?)</article>', s, re.S).group(1)
    hero = re.search(r'<header class="film-hero">(.*?)</header>', art, re.S).group(1)
    title = re.sub("<[^>]+>", "", re.search(r"<h1>(.*?)</h1>", hero, re.S).group(1)).strip()
    meta = re.search(r'<p class="meta">(.*?)</p>', hero, re.S).group(1).strip()
    tag = re.search(r'<p class="tag">(.*?)</p>', hero, re.S)
    hero_img = re.search(r'src="([^"]+)"', hero).group(1).split("/")[-1]
    extra = extra_all.get(slug, {})
    f = film_meta.get(slug) or dict(slug=slug, title=title, meta=meta,
                                    frames=[hero_img] + sorted(p.name for p in bf.IMG.glob(f"{slug}-still-*.jpg")))
    body = []
    stills = []
    for m in re.finditer(r'<section class="([^"]+)">(.*?)</section>|<nav class="pager"[^>]*>(.*?)</nav>', art, re.S):
        cls, chunk, pager = m.group(1), m.group(2), m.group(3)
        if pager is not None:
            links = re.findall(r'<a href="([^"]+)">(.*?)</a>', pager, re.S)
            body.append('<nav class="pager">' + "".join(
                f'<a href="{page_link(h)}">{t.strip()}</a>' for h, t in links) + "</nav>")
        elif cls == "band":
            body.append('<section class="lead-block">' + "".join(
                f'<p class="lead">{x[1]}</p>' for x in blocks(chunk)) + "</section>")
        elif cls == "columns":
            rows = []
            for col in re.findall(r"<div>(.*?)</div>", chunk, re.S):
                items = blocks(col)
                label = next((x[1] for x in items if x[0] == "label"), "")
                rest = [x for x in items if x[0] != "label"]
                rows.append(f'<div class="row"><h2 class="label">{label}</h2><div class="cell">{render_flow(rest)}</div></div>')
            body.append('<section class="card">' + "".join(rows) + "</section>")
        elif cls == "stills":
            continue                     # the strip at the top shows the film
        else:   # watch, prose
            body.append(f'<section class="flow {cls}">{render_flow(blocks(chunk))}</section>')
    laurels = "".join(f'<img src="laurels/{n}" alt="">' for n in extra.get("laurels", []))
    head = (f'<header class="obs"><h1>{html.escape(title)}</h1>'
            + (f'<p class="tag">{tag.group(1).strip()}</p>' if tag else "")
            + f'<p class="meta">{meta}</p>'
            + (f'<div class="obs-laurels">{laurels}</div>' if laurels else "")
            + (f'<p class="awards">{html.escape(extra["awards"])}</p>' if extra.get("awards") else "")
            + "</header>")
    tmpl = (HERE / "page_template.html").read_text(encoding="utf-8")
    out = (tmpl.replace("{{TITLE}}", html.escape(title))
               .replace("{{REEL}}", bf.reel(i, f, extra))
               .replace("{{HEAD}}", head)
               .replace("{{BODY}}", "\n".join(body)))
    (HERE / f"{slug}.html").write_text(out, encoding="utf-8")
    return title


def main():
    _, fs = bf.films()
    meta = {f["slug"]: f for f in fs}
    order = {f["slug"]: n + 1 for n, f in enumerate(fs)}
    extra = json.loads((HERE / "films.json").read_text(encoding="utf-8"))
    for slug in PAGES:
        print(slug, "->", build(slug, order.get(slug, len(order) + 1), extra, meta))


if __name__ == "__main__":
    main()
