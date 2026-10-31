"""About, Contact and Commercial in the new style, built from the live pages so no word is lost.

about.html       -> redesign/pages/about.html       (her photograph as a print, the letter, the two hands, how I work, facts)
contact.html     -> redesign/pages/contact.html     (what for, the address, elsewhere)
commercial.html  -> redesign/pages/commercial.html  (Scent of imagination as a strip of film, the reel text)

Every text node inside <main> of the source must turn up in the output, or the build stops.
Run after build_films.py:  python build_pages.py
"""
import html
import json
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
    # the old page described its Squarespace showreel; the reel is gone, the monitor took its place (her call,
    # 31.10), so that section is left out on purpose and out of the text check
    m = re.sub(r'<section class="prose reel">.*?</section>', "", m, flags=re.S)
    film = re.search(r'<header class="film-hero">(.*?)</header>',
                     (SITE / "scent-of-imagination.html").read_text(encoding="utf-8"), re.S).group(1)
    meta = re.search(r'<p class="meta">(.*?)</p>', film).group(1).strip()
    f = dict(slug="scent-of-imagination", title=title, meta=meta,
             frames=["scent-of-imagination-hero.jpg"] + sorted(p.name for p in bf.IMG.glob("scent-of-imagination-still-*.jpg")))
    extra = json.loads((RD / "films" / "films.json").read_text(encoding="utf-8")).get(f["slug"], {})
    strip = bf.reel(6, f, extra)         # sixth after the five films; same frames as its own page
    strip = re.sub(r'src="(frames|laurels)/', r'src="../films/\1/', strip)
    page = "../films/scent-of-imagination.html"
    # every piece on this page works the same way: the strip leads down to a player right under it
    yt = re.search(r'<iframe[^>]*src="([^"]+)"[^>]*title="([^"]*)"',
                   (SITE / "scent-of-imagination.html").read_text(encoding="utf-8"))
    scent_watch = (f'<div class="screen" id="watch-scent-of-imagination"><iframe src="{yt.group(1)}" title="{yt.group(2)}" '
                   f'loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; '
                   f'web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>')
    more_pieces = []
    for n, (slug, p) in enumerate((k, v) for k, v in json.loads(
            (HERE / "commercial.json").read_text(encoding="utf-8")).items() if not k.startswith("_")):
        g = dict(slug=slug, title=p["title"], meta=p["meta"], frames=[])
        reel = re.sub(r'src="(frames|laurels)/', r'src="../films/\1/', bf.reel(7 + n, g, p))
        watch = ""
        if p.get("video"):           # short enough to live on the site itself
            watch = (f'<div class="screen" id="watch-{slug}"><video controls playsinline preload="none" '
                     f'poster="{p["poster"]}" src="{p["video"]}"></video></div>')
        strip_tag = (f'<a class="strip" href="#watch-{slug}"' if watch else '<div class="strip"')
        strip_end = "</a>" if watch else "</div>"
        more_pieces.append(f'''<article class="film">
  {strip_tag} aria-label="{html.escape(p["title"])}">{reel}{strip_end}
  <div class="caption"><h2>{html.escape(p["title"])}</h2><p class="logline">{html.escape(p["logline"])}</p><p class="meta">{p["meta"]}</p>
    {watch}</div>
</article>''')
    spots = monitor(json.loads((HERE / "commercial.json").read_text(encoding="utf-8"))["_spots"])
    out = f'''<header class="page-head">
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
</header>
<article class="film">
  <a class="strip" href="#watch-scent-of-imagination" aria-label="{html.escape(title)}">{strip}</a>
  <div class="caption"><h2>{title}</h2><p class="logline">{logline}</p><p class="meta">{meta}</p>
    {scent_watch}
    <p class="more"><a href="{page}">{more}</a></p></div>
</article>
{chr(10).join(more_pieces)}
{spots}
{SOUND}'''
    return m, out


ADS = "../../assets/video/ads/"

# one sound switch for every player on the page: on each screen, in step with each other, remembered
SOUND = '''<script>
(() => {
  const players = [...document.querySelectorAll('main video[controls]')];
  let off = false;
  try { off = localStorage.getItem('sound') === 'off'; } catch (e) {}
  const buttons = players.map(v => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'sound';
    b.addEventListener('click', () => set(!off));
    v.parentElement.appendChild(b);
    v.addEventListener('volumechange', () => { if (v.muted !== off) set(v.muted); });
    return b;
  });
  function set(o) {
    off = o;
    try { localStorage.setItem('sound', off ? 'off' : 'on'); } catch (e) {}
    players.forEach(v => v.muted = off);
    buttons.forEach(b => { b.textContent = off ? 'SOUND OFF' : 'SOUND ON'; b.setAttribute('aria-pressed', String(off)); });
  }
  set(off);
})();
</script>'''


def monitor(spots):
    """The rest of the commercial work on one screen: a stage, a strip of live previews, tabs that filter it.
    The page does not grow with the catalogue; a new piece is one more item in commercial.json."""
    first = spots["items"][0]
    esc = html.escape
    tabs = "".join(f'<button type="button" data-tag="{t}"{" aria-pressed=\"true\"" if k == 0 else ""}>{esc(n)}</button>'
                   for k, (t, n) in enumerate(spots["tabs"]))
    thumbs = "".join(
        f'<button type="button" class="frame {it["shape"]}" data-id="{it["id"]}" data-tags="{" ".join(it["tags"])}" '
        f'data-title="{esc(it["title"])}" data-line="{esc(it["line"])}" data-meta="{esc(it["meta"])}" '
        f'aria-label="{esc(it["title"])}"{" aria-current=\"true\"" if k == 0 else ""}>'
        f'<video muted loop playsinline preload="none" poster="{ADS}{it["id"]}-poster.jpg" src="{ADS}{it["id"]}-preview.mp4"></video>'
        f'<span class="fn">{k + 1:02d}</span></button>'
        for k, it in enumerate(spots["items"]))
    return f'''<section class="spots" aria-label="More commercial work">
  <nav class="tabs" aria-label="Filter">{tabs}</nav>
  <div class="stage {first["shape"]}"><video controls playsinline preload="none" poster="{ADS}{first["id"]}-poster.jpg" src="{ADS}{first["id"]}.mp4"></video></div>
  <div class="now"><h2>{esc(first["title"])}</h2><p class="logline">{esc(first["line"])}</p><p class="meta">{esc(first["meta"])}</p></div>
  <div class="deck"><div class="set"><div class="perf"></div><div class="frames">{thumbs}</div><div class="perf"></div></div></div>
  <p class="hint">← → to step through</p>
</section>
<script>
(() => {{
  const box = document.querySelector('.spots'), stage = box.querySelector('.stage'), v = stage.querySelector('video');
  const now = box.querySelector('.now'), thumbs = [...box.querySelectorAll('.deck .frame')];
  const ADS = "{ADS}";
  const visible = () => thumbs.filter(t => !t.hidden);
  function pick(t, play) {{
    thumbs.forEach(x => x.removeAttribute('aria-current')); t.setAttribute('aria-current', 'true');
    stage.className = 'stage ' + (t.classList.contains('tall') ? 'tall' : 'wide');
    v.poster = ADS + t.dataset.id + '-poster.jpg'; v.src = ADS + t.dataset.id + '.mp4';
    now.querySelector('h2').textContent = t.dataset.title;
    now.querySelector('.logline').textContent = t.dataset.line;
    now.querySelector('.meta').textContent = t.dataset.meta;
    t.scrollIntoView({{block: 'nearest', inline: 'nearest', behavior: 'smooth'}});
    if (play) v.play().catch(() => {{}});
  }}
  thumbs.forEach(t => {{
    const pv = t.querySelector('video');
    t.addEventListener('mouseenter', () => pv.play().catch(() => {{}}));
    t.addEventListener('mouseleave', () => {{ pv.pause(); pv.currentTime = 0; }});
    t.addEventListener('click', () => pick(t, true));
  }});
  box.querySelectorAll('.tabs button').forEach(b => b.addEventListener('click', () => {{
    box.querySelectorAll('.tabs button').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    const tag = b.dataset.tag;
    thumbs.forEach(t => t.hidden = tag !== 'all' && !t.dataset.tags.split(' ').includes(tag));
    const cur = thumbs.find(t => t.hasAttribute('aria-current'));
    if (cur.hidden) pick(visible()[0], false);
  }}));
  // arrows step through what the tab shows, while the monitor is on screen
  let seen = false;
  new IntersectionObserver(e => seen = e[0].isIntersecting, {{threshold: .25}}).observe(box);
  document.addEventListener('keydown', e => {{
    if (!seen || !['ArrowLeft', 'ArrowRight'].includes(e.key) || (e.target.closest && e.target.closest('input,textarea'))) return;
    const list = visible(), i = list.findIndex(t => t.hasAttribute('aria-current'));
    const n = list[(i + (e.key === 'ArrowRight' ? 1 : -1) + list.length) % list.length];
    e.preventDefault(); pick(n, !v.paused);
  }});
  // on touch screens there is no hover: previews in view play on their own
  if (matchMedia('(hover: none)').matches) {{
    const io = new IntersectionObserver(es => es.forEach(x => {{
      const pv = x.target.querySelector('video'); x.isIntersecting ? pv.play().catch(() => {{}}) : pv.pause();
    }}), {{threshold: .6}});
    thumbs.forEach(t => io.observe(t));
  }}
}})();
</script>'''


PAGES = {"about":("About", "About", about), "contact": ("Contact", "Contact", contact),
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
