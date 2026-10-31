"""Put the redesign on the live addresses.

Built pages stay where the generators write them (redesign/...). This copies each one to the address the
interim site used, so every old link keeps working, and rewrites its relative paths for the new place:
  - a link to another built page -> that page's live address
  - a support file inside redesign/ (strip.css/js, film frames, laurels...) -> copied to assets/site/...
  - anything else (assets/...) -> the same file, path recomputed
Then it checks every local reference on every published page exists on disk.

Run after all the generators:  python publish.py
"""
import posixpath
import re
import shutil
import sys
from pathlib import Path

RD = Path(__file__).resolve().parent
SITE = RD.parent

FILMS = ["06percents", "nominal", "plus", "scent-of-imagination", "step-sequence", "wearenotalone"]
PAGES = {"redesign/home/index.html": "index.html",
         "redesign/pages/about.html": "about.html",
         "redesign/pages/contact.html": "contact.html",
         "redesign/pages/commercial.html": "commercial.html",
         "redesign/films/index.html": "films.html",
         "redesign/album/index.html": "projects.html",
         "redesign/album/people.html": "people.html"}
PAGES.update({f"redesign/films/{s}.html": f"{s}.html" for s in FILMS})
PAGES.update({f"redesign/album/{p.name}": f"projects/{p.name}" for p in (SITE / "content-src/interim/projects").glob("*.html")})

ATTR = re.compile(r'''((?:href|src|poster)=")([^"]+)(")''')
STR = re.compile(r'''(["'(])((?:\.\./)+[^"')\s]+)(["')])''')     # relative paths in inline scripts / styles
BOTH = re.compile(ATTR.pattern + "|" + STR.pattern)


def local(u):
    return not re.match(r"^(?:[a-z]+:|#|//|data:|\?)", u)


def rewrite(src_rel, dst_rel, text, copied):
    sdir, ddir = posixpath.dirname(src_rel), posixpath.dirname(dst_rel)

    def fix(u):
        if not local(u):
            return u
        path, frag = (u.split("#", 1) + [""])[:2]
        if not path:
            return u
        absp = posixpath.normpath(posixpath.join(sdir, path))
        if absp in PAGES:
            target = PAGES[absp]
        elif absp.startswith("redesign/"):
            target = "assets/site/" + absp[len("redesign/"):]
            copied.add((absp, target))
        else:
            target = absp
        rel = posixpath.relpath(target, ddir or ".")
        if path.endswith("/"):               # a folder prefix in a script ("…/ads/" + id): normpath drops the slash
            rel += "/"
        return rel + ("#" + frag if frag else "")

    # one pass over the original: an attribute is taken whole before its quoted value could match as a string
    return BOTH.sub(lambda m: m.group(1) + fix(m.group(2)) + m.group(3) if m.group(1)
                    else m.group(4) + fix(m.group(5)) + m.group(6), text)


def check(dst_rel, text):
    ddir = posixpath.dirname(dst_rel)
    missing = []
    for u in [m.group(2) or m.group(5) for m in BOTH.finditer(text)]:
        if not local(u):
            continue
        path = u.split("#", 1)[0]
        if not path:
            continue
        p = SITE / posixpath.normpath(posixpath.join(ddir, path))
        if path.endswith("/"):
            ok = p.is_dir()
        else:
            ok = p.exists()
        if not ok:
            missing.append(u)
    return missing


def main():
    copied = set()
    out = {}
    for src_rel, dst_rel in PAGES.items():
        text = (SITE / src_rel).read_text(encoding="utf-8")
        out[dst_rel] = rewrite(src_rel, dst_rel, text, copied)
    # support files: whole folders where a file inside one is used (frames come and go with films.json)
    dirs = {posixpath.dirname(s) for s, _ in copied if posixpath.basename(posixpath.dirname(s)) in ("frames", "laurels", "roses")}
    for d in sorted(dirs):
        dst = SITE / ("assets/site/" + d[len("redesign/"):])
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(SITE / d, dst)
    for s, t in sorted(copied):
        if posixpath.dirname(s) not in dirs:
            (SITE / t).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SITE / s, SITE / t)
    bad = 0
    for dst_rel, text in out.items():
        (SITE / dst_rel).write_text(text, encoding="utf-8")
        miss = check(dst_rel, text)
        if miss:
            bad += 1
            print(f"{dst_rel}: MISSING {miss[:6]}")
    print(f"published {len(out)} pages, {len(copied)} support refs, {len(dirs)} folders copied; pages with missing refs: {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
