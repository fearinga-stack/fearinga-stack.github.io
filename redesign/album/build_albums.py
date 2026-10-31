"""Build page-flip photo albums from the site's project pages.

Each project page becomes redesign/album/<slug>.html. Text pages go on the left
of a spread, facing the photograph they belong to:
  - an intro (section.prose) faces the first photograph after it;
  - text inside a section.story faces the first photograph of that section.
Blank pages are inserted where needed to keep text on the left.

Cover photo and title placement come from albums.json (per slug); without an
entry the cover uses the first photograph and puts the title top-left.

Run from anywhere:  python build_albums.py
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import chrome  # noqa: E402
SITE = HERE.parent.parent
SRC = SITE / "content-src" / "interim"   # the interim site, frozen as text source when the redesign went live
PROJECTS = SRC / "projects"
TEXT_BUDGET = 620          # characters that fit on one text page



def photo_dims(name, w, h):
    if w and h:
        return int(w), int(h)
    return 3, 2


def parse(path):
    s = path.read_text(encoding="utf-8")
    main = re.search(r"<main.*?</main>", s, re.S).group(0)
    title = re.sub("<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", main, re.S).group(1)).strip()
    seen = set()
    tok_re = re.compile(r"<figure.*?</figure>|<blockquote.*?</blockquote>|<(h2|h3|p)[^>]*>.*?</\1>", re.S)

    def plain(x):
        return re.sub(r"\s+", " ", re.sub("<[^>]+>", "", x)).strip()

    def scan(chunk):
        out = []
        for m in tok_re.finditer(chunk):
            t = m.group(0)
            if t.startswith("<figure"):
                src = re.search(r'src="(?:\.\./)?assets/img/photo/([^"]+)"', t)
                if not src or src.group(1) in seen:
                    continue
                seen.add(src.group(1))
                w = re.search(r'width="(\d+)"', t); h = re.search(r'height="(\d+)"', t)
                cap = re.search(r"<figcaption>(.*?)</figcaption>", t, re.S)
                capt = ""
                if cap:
                    spans = [plain(x) for x in re.findall(r"<span[^>]*>(.*?)</span>", cap.group(1), re.S)]
                    capt = " · ".join(x for x in spans if x) or plain(cap.group(1))
                out.append(("img", src.group(1), int(w.group(1)) if w else 3, int(h.group(1)) if h else 2, capt))
            elif t.startswith("<blockquote"):
                txt = plain(t)
                if txt:
                    out.append(("text", [("q", t[t.index(">") + 1:t.rindex("</blockquote>")], len(txt))]))
            else:
                tag = m.group(1); inner = t[t.index(">") + 1:t.rindex("</")]
                txt = plain(inner)
                if txt and "©" not in txt:
                    out.append(("text", [(tag, inner, len(txt))]))
        return out

    units = []
    pos = 0
    for m in re.finditer(r'<section[^>]*class="[^"]*story[^"]*"[^>]*>(.*?)</section>', main, re.S):
        units += scan(main[pos:m.start()])
        body = scan(m.group(1))
        units += [u for u in body if u[0] == "text"] + [u for u in body if u[0] == "img"]
        pos = m.end()
    units += scan(main[pos:])
    merged = []
    for u in units:                      # consecutive text tokens make one text unit
        if u[0] == "text" and merged and merged[-1][0] == "text":
            merged[-1] = ("text", merged[-1][1] + u[1])
        else:
            merged.append(u)
    return title, merged


def split_text(blocks):
    pages, cur, n = [], [], 0
    for b in blocks:
        if cur and n + b[2] > TEXT_BUDGET and b[0] == "p":
            pages.append(cur)
            cur, n = [], 0
        cur.append(b)
        n += b[2]
    if cur:
        pages.append(cur)
    return pages


def text_page(blocks):
    parts = []
    for tag, inner, _ in blocks:
        if tag == "q":
            parts.append(f'<blockquote class="t-q">{inner}</blockquote>')
            continue
        cls = "t-head" if tag in ("h2", "h3") else "t-p"
        parts.append(f'<p class="{cls}">{inner}</p>')
    return f'    <div class="page"><div class="leaf text">{"".join(parts)}</div></div>'


def photo_page(n, name, w, h, caption=""):
    m = re.match(r"mv-(\d{4})(\d\d)(\d\d)", name)
    date = f" · {m.group(3)}.{m.group(2)}.{m.group(1)}" if m else ""
    if caption:
        date = " · " + html.escape(caption)
    orient = "portrait" if h > w else "landscape"
    return (f'    <div class="page"><div class="leaf {orient}"><figure><img src="../../assets/img/photo/{name}" '
            f'alt="Photograph {n}" loading="lazy"></figure><p class="pencil">№ {n:02d}{date}</p></div></div>')


BLANK = '    <div class="page"><div class="leaf blank"></div></div>'


def build(slug, cfg):
    title, units = parse(SRC / cfg.get("source", f"projects/{slug}.html"))
    first_img = next(u for u in units if u[0] == "img")
    cover = cfg.get("cover", first_img[1])
    pages = []                       # index 0 is the cover; odd = left, even = right
    n = 0
    i = 0
    while i < len(units):
        u = units[i]
        if u[0] == "text":
            chunks = split_text(u[1])
            faces_photo = i + 1 < len(units) and units[i + 1][0] == "img"
            # with its photo: the last text page sits on the left, the photo opposite it.
            # without one: the text opens on a right-hand page, like a book's first page.
            want_first_left = (len(chunks) % 2 == 1) if faces_photo else False
            first_is_left = (len(pages) + 1) % 2 == 1
            if first_is_left != want_first_left:
                pages.append(BLANK)
            for chunk in chunks:
                pages.append(text_page(chunk))
            # the photo that follows lands on the right automatically if the last text page was left
            if (len(pages) + 1) % 2 == 0 and i + 1 < len(units) and units[i + 1][0] == "img":
                n += 1
                pages.append(photo_page(n, *units[i + 1][1:]))
                i += 1
        else:
            n += 1
            pages.append(photo_page(n, *u[1:]))
        i += 1
    if len(pages) % 2:
        pages.append(BLANK)
    light = cfg.get("title_style") == "light"
    tmpl = (HERE / "template.html").read_text(encoding="utf-8")
    out = (tmpl.replace("{{TITLE}}", html.escape(title))
               .replace("{{TITLE_UPPER}}", html.escape(cfg.get("cover_title", title).upper()).replace("_", "_<wbr>"))
               .replace("{{TAGLINE}}", html.escape(cfg.get("tagline", "")))
               .replace("{{COVER}}", cover)
               .replace("{{COVER_POS}}", cfg.get("cover_position", "center 30%"))
               .replace("{{TITLE_PAD}}", cfg.get("title_padding", "6% 6% 0"))
               .replace("{{TITLE_ALIGN}}", cfg.get("title_align", "flex-start"))
               .replace("{{TITLE_COLOR}}", "#F3E5F5" if light else cfg.get("title_color", "#200F3A"))
               .replace("{{TITLE_SHADOW}}", "0 1px 3px rgba(0,0,0,.6),0 0 22px rgba(17,6,38,.85)" if light
                        else "0 1px 0 rgba(255,255,255,.45),0 -1px 0 rgba(0,0,0,.25)")
               .replace("{{TITLE_VEIL}}", "linear-gradient(rgba(17,6,38,.62) 0%,rgba(17,6,38,0) 42%)," if light else "")
               .replace("{{VEIL_BLEND}}", "normal," if light else "")
               .replace("{{PAGES}}", "\n".join(pages)))
    (HERE / f"{slug}.html").write_text(out, encoding="utf-8")
    return title, n, len(pages)


def main():
    cfg = json.loads((HERE / "albums.json").read_text(encoding="utf-8"))
    groups = []
    for key in ("order", "order_below"):
        rows = []
        for slug in cfg.get(key, []):
            title, photos, pages = build(slug, cfg.get("albums", {}).get(slug, {}))
            rows.append((slug, title, photos, pages))
            print(f"{slug:42s} {photos:2d} photos  {pages:2d} pages  {title}")
        groups.append(rows)
    # the shelf: every album's own cover, scoped CSS taken from the built album
    base_css = re.search(r"<style>(.*?)</style>", (HERE / "template.html").read_text(encoding="utf-8"), re.S).group(1)
    base_css = re.sub(r"\{\{[A-Z_]+\}\}", "", base_css)
    rules = []

    def tile(r):
        slug, title, photos, _ = r
        s = (HERE / f"{slug}.html").read_text(encoding="utf-8")
        st = re.search(r"<style>(.*?)</style>", s, re.S).group(1)
        k = "c-" + slug.replace("_", "-")
        rules.append(re.search(r"\.cover\{.*?\}\n", st, re.S).group(0).replace(".cover{", f".{k} .cover{{"))
        rules.append(re.search(r"\.cover h2\{.*?\}\n", st, re.S).group(0).replace(".cover h2{", f".{k} .cover h2{{"))
        front = re.search(r'<div class="cover"><h2>.*?</div>', s).group(0)
        return (f'  <a class="tile {k}" href="{slug}.html" aria-label="{html.escape(title)}, {photos} photographs">'
                f'{front}</a>')

    items = "\n".join(tile(r) for r in groups[0])
    if groups[1]:
        items += '\n  <hr class="rule">\n' + "\n".join(tile(r) for r in groups[1])
    shelf = (HERE / "shelf_template.html").read_text(encoding="utf-8")
    out = shelf.replace("{{BASE_CSS}}", base_css).replace("{{CHROME_CSS}}", chrome.CSS).replace("{{TOPBAR}}", chrome.topbar("Photography")).replace("{{FOOTER}}", chrome.FOOTER).replace("{{COVER_CSS}}", "\n".join(rules)).replace("{{ITEMS}}", items)
    (HERE / "index.html").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
