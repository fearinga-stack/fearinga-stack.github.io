"""About, Contact and Commercial in the new style, built from the live pages so no word is lost.

about.html       -> redesign/pages/about.html       (her photograph as a print, the letter, the two hands, how I work, facts)
contact.html     -> redesign/pages/contact.html     (what for, the address, elsewhere)
commercial.html  -> redesign/pages/commercial.html  (Scent of imagination as a strip of film, the reel text)

Every text node inside <main> of the source must turn up in the output, or the build stops.
Run after build_films.py:  python build_pages.py
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RD = HERE.parent
SITE = RD.parent
sys.path.insert(0, str(RD))
sys.path.insert(0, str(RD / "films"))
import chrome          # noqa: E402
import build_films as bf  # noqa: E402


def main_of(name):
    s = (SITE / name).read_text(encoding="utf-8")
    return re.search(r'<main id="main">(.*?)</main>', s, re.S).group(1)


def ps(chunk):
    return [re.sub(r"\s+", " ", p).strip() for p in re.findall(r"<p[^>]*>(.*?)</p>", chunk, re.S)]


def lis(chunk):
    return [re.sub(r"\s+", " ", x).strip() for x in re.findall(r"<li[^>]*>(.*?)</li>", chunk, re.S)]


def text_nodes(fragment):
    fragment = re.sub(r"<!--.*?-->", " ", fragment, flags=re.S)
    return [t for t in (re.sub(r"\s+", " ", html.unescape(x)).strip() for x in re.split(r"<[^>]+>", fragment)) if t]


def flat(fragment):
    return " ".join(text_nodes(fragment))


# ---------------------------------------------------------------- about
def about():
    m = main_of("about.html")
    head = re.search(r'<header class="page-head[^"]*">(.*?)</header>', m, re.S).group(1)
    img = re.search(r"<img [^>]*>", head).group(0)
    alt = re.search(r'alt="([^"]*)"', img).group(1)
    h1 = re.search(r"<h1>(.*?)</h1>", head, re.S).group(1).strip()
    lead = re.search(r'<p class="lead">(.*?)</p>', head, re.S).group(1).strip()
    letter = ps(re.search(r"<blockquote>(.*?)</blockquote>", m, re.S).group(1))
    cols = re.findall(r'<div>\s*<h2 class="label">(.*?)</h2>\s*<p>(.*?)</p>\s*</div>', m, re.S)
    note = re.search(r'<p class="note">(.*?)</p>', m, re.S).group(1).strip()
    how = re.search(r'<h2 class="label">(HOW I WORK)</h2>', m).group(1)
    steps = re.findall(r'<li><span class="num">(\d+)</span>\s*(.*?)</li>', m, re.S)
    facts = re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", m, re.S)

    *body, last = letter
    hands = "\n".join(
        (f'<div class="seam" aria-hidden="true"></div>\n' if k else "")
        + f'<div class="hand"><h2>{t.strip()}</h2><p>{p.strip()}</p></div>' for k, (t, p) in enumerate(cols))
    out = f'''<header class="page-head">
  <figure class="print"><img src="../../assets/img/site/about-hero.jpg" alt="{alt}" width="1600" height="893" decoding="async"></figure>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
</header>
<section class="letter">
{chr(10).join(f"  <p>{p}</p>" for p in body)}
</section>
<section class="black"><p>{last}</p></section>
<section class="hands">
{hands}
</section>
<p class="note">{note}</p>
<section class="how">
  <h2 class="label">{how}</h2>
  <ol>{"".join(f'<li><span class="num">{n}</span>{w.strip()}</li>' for n, w in steps)}</ol>
</section>
<section class="card">
{chr(10).join(f'  <div class="row"><h2 class="label">{dt.strip()}</h2><p>{dd.strip()}</p></div>' for dt, dd in facts)}
</section>'''
    return m, out


# ---------------------------------------------------------------- contact
def contact():
    m = main_of("contact.html")
    h1 = re.search(r"<h1>(.*?)</h1>", m).group(1)
    lead = re.search(r'<p class="lead">(.*?)</p>', m, re.S).group(1).strip()
    band = re.search(r'<section class="band">(.*?)</section>', m, re.S).group(1)
    avail = re.search(r'<h2 class="label">(.*?)</h2>', band).group(1)
    lists = [lis(u) for u in re.findall(r'<ul class="plain">(.*?)</ul>', band, re.S)]
    cols = re.search(r'<section class="columns">(.*?)</section>\s*$', m, re.S).group(1)
    labels = re.findall(r'<h2 class="label">(.*?)</h2>', cols)
    email = re.search(r'<p class="email"><a href="mailto:([^"]+)">', cols).group(1)
    reply = [p for p in ps(cols) if "reply" in p][0]
    links = re.findall(r'<li><a href="([^"]+)">(.*?)</a></li>', cols)
    based = [p for p in ps(cols) if p.startswith("Based")][0]
    out = f'''<header class="page-head">
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
</header>
<section class="address">
  <h2 class="label">{labels[0]}</h2>
  <p class="email"><a href="mailto:{email}">{email}</a></p>
  <p class="small">{reply}</p>
</section>
<section class="card">
  <div class="row"><h2 class="label">{avail}</h2><div class="cell">{"".join(f'<ul>{"".join(f"<li>{x}</li>" for x in l)}</ul>' for l in lists)}</div></div>
  <div class="row"><h2 class="label">{labels[1]}</h2><div class="cell"><ul class="links">{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)}</ul><p class="small">{based}</p></div></div>
</section>'''
    return m, out


# ---------------------------------------------------------------- commercial
def commercial():
    m = main_of("commercial.html")
    h1 = re.search(r"<h1>(.*?)</h1>", m).group(1)
    lead = re.search(r'<p class="lead">(.*?)</p>', m, re.S).group(1).strip()
    card = re.search(r'<article class="card">(.*?)</article>', m, re.S).group(1)
    title = re.search(r"<h2>(.*?)</h2>", card).group(1)
    logline = [p for p in ps(card) if "more" not in p and "VIEW" not in p][0]
    more = re.search(r'<p class="more"><a href="[^"]+">(.*?)</a></p>', card).group(1)
    reel_sec = re.search(r'<section class="prose reel">(.*?)</section>', m, re.S).group(1)
    reel_h = re.search(r"<h2>(.*?)</h2>", reel_sec).group(1)
    comment = re.search(r"<!--.*?-->", reel_sec, re.S).group(0)
    reel_ps = ps(reel_sec)
    film = re.search(r'<header class="film-hero">(.*?)</header>',
                     (SITE / "scent-of-imagination.html").read_text(encoding="utf-8"), re.S).group(1)
    meta = re.search(r'<p class="meta">(.*?)</p>', film).group(1).strip()
    f = dict(slug="scent-of-imagination", title=title, meta=meta,
             frames=["scent-of-imagination-hero.jpg"] + sorted(p.name for p in bf.IMG.glob("scent-of-imagination-still-*.jpg")))
    strip = bf.reel(6, f, {})            # sixth after the five films; frame paths already point at ../../assets
    page = "../films/scent-of-imagination.html"
    out = f'''<header class="page-head">
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
</header>
<article class="film">
  <a class="strip" href="{page}" aria-label="{html.escape(title)}">{strip}</a>
  <div class="caption"><h2><a href="{page}">{title}</a></h2><p class="logline">{logline}</p><p class="meta">{meta}</p>
    <p class="more"><a href="{page}">{more}</a></p></div>
</article>
<section class="reel-text">
  <h2>{reel_h}</h2>
  {comment}
{chr(10).join(f"  <p>{p}</p>" for p in reel_ps)}
</section>'''
    return m, out


PAGES = {"about": ("About", "About", about), "contact": ("Contact", "Contact", contact),
         "commercial": ("Commercial", "Commercial", commercial)}


def check(name, src, out):
    have = flat(out)
    lost = [t for t in text_nodes(src) if t not in have]
    if lost:
        raise SystemExit(f"{name}: lost text {lost}")
    n_src, n_out = len(re.findall(r"<img ", src)), len(re.findall(r"<img ", out))
    return len(text_nodes(src)), n_src, n_out


def main():
    tmpl = (HERE / "template.html").read_text(encoding="utf-8")
    for slug, (title, current, fn) in PAGES.items():
        src, body = fn()
        nodes, i_src, i_out = check(slug, src, body)
        page = (tmpl.replace("{{TITLE}}", title).replace("{{SLUG}}", slug)
                    .replace("{{CHROME_CSS}}", chrome.CSS).replace("{{TOPBAR}}", chrome.topbar(current))
                    .replace("{{BODY}}", body).replace("{{FOOTER}}", chrome.FOOTER))
        (HERE / f"{slug}.html").write_text(page, encoding="utf-8")
        print(f"{slug:11s} text nodes {nodes} all present · images source {i_src} -> page {i_out}")


if __name__ == "__main__":
    main()
