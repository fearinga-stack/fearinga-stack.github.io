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
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent
PROJECTS = SITE / "projects"
TEXT_BUDGET = 620          # characters that fit on one text page

IMG_RE = re.compile(r'<img[^>]+src="\.\./assets/img/photo/([^"]+)"[^>]*?(?:width="(\d+)")?[^>]*?(?:height="(\d+)")?[^>]*>')


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
                src = re.search(r'src="\.\./assets/img/photo/([^"]+)"', t)
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
    title, units = parse(PROJECTS / f"{slug}.html")
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
    tmpl = (HERE / "template.html").read_text(encoding="utf-8")
    out = (tmpl.replace("{{TITLE}}", html.escape(title))
               .replace("{{TITLE_UPPER}}", html.escape(cfg.get("cover_title", title).upper()))
               .replace("{{TAGLINE}}", html.escape(cfg.get("tagline", "")))
               .replace("{{COVER}}", cover)
               .replace("{{COVER_POS}}", cfg.get("cover_position", "center 30%"))
               .replace("{{TITLE_PAD}}", cfg.get("title_padding", "6% 6% 0"))
               .replace("{{TITLE_ALIGN}}", cfg.get("title_align", "flex-start"))
               .replace("{{TITLE_COLOR}}", cfg.get("title_color", "#200F3A"))
               .replace("{{PAGES}}", "\n".join(pages)))
    (HERE / f"{slug}.html").write_text(out, encoding="utf-8")
    return title, n, len(pages)


def main():
    cfg = json.loads((HERE / "albums.json").read_text(encoding="utf-8"))
    rows = []
    for slug in cfg["order"]:
        title, photos, pages = build(slug, cfg.get("albums", {}).get(slug, {}))
        rows.append((slug, title, photos, pages))
        print(f"{slug:42s} {photos:2d} photos  {pages:2d} pages  {title}")
    shelf = (HERE / "shelf_template.html").read_text(encoding="utf-8")
    items = "\n".join(f'  <li><a href="{s}.html">{html.escape(t)}</a> <span>{p} photographs</span></li>' for s, t, p, _ in rows)
    (HERE / "index.html").write_text(shelf.replace("{{ITEMS}}", items), encoding="utf-8")


if __name__ == "__main__":
    main()
