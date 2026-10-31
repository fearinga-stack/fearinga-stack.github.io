"""Home page: the roses diptych, the two sides of the seam, and a way into each.

Camera side  -> three album covers from the photography shelf (album/index.html)
Machine side -> one endless strip of every film's opening frame (films/*.html)
Texts are hers, from about.html.  Run after the album and film builders:  python build_home.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RD = HERE.parent
SITE = RD.parent
sys.path.insert(0, str(RD))
import chrome  # noqa: E402
ALBUMS_ON_HOME = ["normandie", "ukraine-one", "kherson-2023"]


def about_text(start):
    s = (SITE / "about.html").read_text(encoding="utf-8")
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", s, re.S):
        t = re.sub(r"\s+", " ", m.group(1)).strip()
        if re.sub("<[^>]+>", "", t).startswith(start):
            return t
    raise SystemExit(f"about.html has no paragraph starting with {start!r}")


def album_covers():
    shelf = (RD / "album" / "index.html").read_text(encoding="utf-8")
    style = re.search(r"<style>(.*?)</style>", shelf, re.S).group(1)
    rules, tiles = [], []
    for slug in ALBUMS_ON_HOME:
        k = "c-" + slug.replace("_", "-")
        rules += re.findall(rf"\.{k} \.cover(?: h2)?\{{.*?\}}\n", style, re.S)
        tile = re.search(rf'<a class="tile {k}" href="{slug}\.html"[^>]*>.*?</a>', shelf, re.S).group(0)
        tiles.append(tile.replace(f'href="{slug}.html"', f'href="../album/{slug}.html"')
                         .replace('src="../../', 'src="../../'))
    return "".join(rules), "\n".join(tiles)


def film_openers():
    """Each film's first frame on its page strip, linked to the film."""
    out = []
    films = (RD / "films" / "index.html").read_text(encoding="utf-8")
    for slug in re.findall(r'<a class="strip" href="([^"]+)\.html"', films):
        page = (RD / "films" / f"{slug}.html").read_text(encoding="utf-8")
        first = re.search(r'<div class="frames">(<figure.*?</figure>)', page, re.S).group(1)
        first = re.sub(r'src="(?!\.\./|https?:)', 'src="../films/', first)       # frames/, laurels/
        first = first.replace('src="../../', 'src="../../')
        out.append(f'<a class="opener" href="../films/{slug}.html">{first}</a>')
    return "".join(out)


def main():
    cover_css, tiles = album_covers()
    openers = film_openers()
    one = (f'<div class="set"><div class="perf"></div><div class="frames">{openers}</div><div class="perf"></div></div>')
    hidden = one.replace('<div class="set">', '<div class="set" aria-hidden="true">')
    out = ((HERE / "template.html").read_text(encoding="utf-8")
           .replace("{{CHROME_CSS}}", chrome.CSS)
           .replace("{{TOPBAR}}", chrome.topbar())
           .replace("{{FOOTER}}", chrome.FOOTER)
           .replace("{{COVER_CSS}}", cover_css)
           .replace("{{TILES}}", tiles)
           .replace("{{REEL}}", f'<div class="reel">{one}{hidden}{hidden}</div>')
           .replace("{{CAMERA}}", about_text("Documentary and fine art photography"))
           .replace("{{MACHINE}}", about_text("AI-directed short films"))
           .replace("{{NOTE}}", about_text("The two are not separate careers")))
    (HERE / "index.html").write_text(out, encoding="utf-8")
    print("home: covers", len(ALBUMS_ON_HOME), "· film openers", openers.count('class="opener"'))


if __name__ == "__main__":
    main()
