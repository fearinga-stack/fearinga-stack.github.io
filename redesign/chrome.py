"""The shared top bar and footer, one source for every page of the redesign.

Pages live one folder deep (redesign/<section>/<page>.html), so every path here is written from there.
"""

NAV = [("Films", "../films/index.html"),
       ("Photography", "../album/index.html"),
       ("Commercial", "../pages/commercial.html"),
       ("About", "../pages/about.html"),
       ("Contact", "../pages/contact.html")]

CSS = """
.topbar{position:absolute;top:0;left:0;right:0;z-index:6;display:flex;justify-content:space-between;align-items:center;
  padding:1rem 16px 1.6rem;padding-top:max(1rem,env(safe-area-inset-top,0px));
  background:linear-gradient(to bottom,rgba(12,6,24,.62),rgba(12,6,24,0))}   /* the menu reads over a bright photograph too */
.topbar .mark img{height:46px;width:auto;display:block}
.topbar nav{display:flex;gap:clamp(.8rem,2vw,1.6rem);flex-wrap:wrap;justify-content:flex-end;
  font:500 clamp(1.05rem,1.3vw,1.25rem) "Cormorant SC",serif;letter-spacing:.16em}
.topbar nav a{color:rgba(243,229,245,.84);text-shadow:0 1px 10px rgba(0,0,0,.7);text-decoration:none}
.topbar nav a:hover,.topbar nav a[aria-current]{color:var(--light)}
@media (max-width:600px){.topbar .mark img{height:36px}.topbar nav{gap:.25rem .8rem;font-size:.86rem;letter-spacing:.08em;max-width:15rem}}
.site-foot{border-top:1px solid var(--hair);padding:2rem 16px 3rem;text-align:center;font:500 .92rem "Cormorant SC",serif;letter-spacing:.2em;color:var(--dim)}
.site-foot nav{display:flex;gap:1.2rem;justify-content:center;flex-wrap:wrap;margin-bottom:1rem}
.site-foot a{color:inherit;text-decoration:none}
.site-foot a:hover{color:var(--light)}
.site-foot img{height:30px;width:auto;margin:1.4rem auto 0;display:block;opacity:.8}
"""


def topbar(current=""):
    links = "\n    ".join(
        f'<a href="{href}"{" aria-current=\"page\"" if name == current else ""}>{name}</a>' for name, href in NAV)
    return f'''<header class="topbar">
  <a class="mark" href="../home/index.html" aria-label="Amata Lynner, home"><img src="../../assets/img/brand/monogram-lavender.png" alt="AL"></a>
  <nav aria-label="Main">
    {links}
  </nav>
</header>'''


FOOTER = '''<footer class="site-foot">
  <nav aria-label="Elsewhere">
    <a href="https://www.instagram.com/amata_lynner/">Instagram</a>
    <a href="https://www.linkedin.com/in/amata-lynner/">LinkedIn</a>
    <a href="https://www.youtube.com/@alynner">YouTube</a>
    <a href="https://x.com/amatalynner">X</a>
  </nav>
  <p><a href="mailto:info@amatalynner.com">info@amatalynner.com</a></p>
  <p>© 2026 · Amata Lynner · Dnipro, Ukraine</p>
  <img src="../../assets/img/brand/monogram-lavender.png" alt="">
</footer>'''
