"""The shared top bar and footer, one source for every page of the redesign.

Pages live one folder deep (redesign/<section>/<page>.html), so every path here is written from there.
"""

NAV = [("Films", "../films/index.html"),
       ("Photography", "../album/index.html"),
       ("Commercial", "../pages/commercial.html"),
       ("About", "../pages/about.html"),
       ("Contact", "../pages/contact.html")]

CSS = """
:root{color-scheme:dark}   /* the site is dark already: phone browsers must not "darken" it (their forced dark mode ate the gold, 31.10) */
.topbar{position:absolute;top:0;left:0;right:0;z-index:6;display:flex;justify-content:space-between;align-items:center;
  padding:1rem 16px 1.6rem;padding-top:max(1rem,env(safe-area-inset-top,0px))}
/* gold from her roses (#DBA048, petal median): dust at the top that thins into the night, sparks over the page,
   a few that wink (31.10, her call); the home keeps its photograph and a plain dark scrim instead */
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.7;
  background:url(../../assets/img/site/pollen-gold.png) center top/100% auto no-repeat,
  linear-gradient(to bottom,rgba(219,160,72,.10),rgba(219,160,72,.03) 28%,rgba(219,160,72,0) 45%),
  url(../../assets/img/site/sparks-gold.png) 0 0/1000px 1000px repeat}
/* the Witcher's note (31.10): the dust stays put with the sparks; Lin's: a few of them wink */
.winks{position:fixed;inset:0;z-index:0;pointer-events:none}
.winks i{position:absolute;border-radius:50%;opacity:0;
  background:radial-gradient(circle,rgba(255,226,160,1) 0,rgba(219,160,72,.85) 22%,rgba(219,160,72,0) 70%);
  animation:wink var(--d) ease-in-out var(--w) infinite}
@keyframes wink{0%,100%{opacity:0;transform:scale(.4)}6%{opacity:.95;transform:scale(1.25)}14%{opacity:0;transform:scale(.6)}}
@media (prefers-reduced-motion:reduce){.winks{display:none}}
main,section,article,.films-head,.site-foot{position:relative;z-index:1}
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


WINKS = '<div class="winks" aria-hidden="true"><i style="top:7.8%;left:12.7%;width:10px;height:10px;margin:-5.0px 0 0 -5.0px;--d:9.8s;--w:-0.9s"></i><i style="top:1.6%;left:54.6%;width:8px;height:8px;margin:-4.0px 0 0 -4.0px;--d:9.0s;--w:-2.0s"></i><i style="top:16.6%;left:29.0%;width:8px;height:8px;margin:-4.0px 0 0 -4.0px;--d:8.2s;--w:-2.1s"></i><i style="top:28.3%;left:5.4%;width:12px;height:12px;margin:-6.0px 0 0 -6.0px;--d:11.5s;--w:-9.2s"></i><i style="top:6.6%;left:32.1%;width:12px;height:12px;margin:-6.0px 0 0 -6.0px;--d:11.4s;--w:-1.0s"></i><i style="top:18.6%;left:66.1%;width:10px;height:10px;margin:-5.0px 0 0 -5.0px;--d:10.5s;--w:-2.6s"></i><i style="top:9.1%;left:91.8%;width:18px;height:18px;margin:-9.0px 0 0 -9.0px;--d:12.7s;--w:-10.7s"></i><i style="top:1.2%;left:30.4%;width:12px;height:12px;margin:-6.0px 0 0 -6.0px;--d:11.9s;--w:-10.1s"></i><i style="top:15.7%;left:41.9%;width:14px;height:14px;margin:-7.0px 0 0 -7.0px;--d:11.2s;--w:-5.1s"></i><i style="top:7.8%;left:27.4%;width:8px;height:8px;margin:-4.0px 0 0 -4.0px;--d:12.6s;--w:-0.6s"></i><i style="top:72.6%;left:29.4%;width:14px;height:14px;margin:-7.0px 0 0 -7.0px;--d:10.7s;--w:-7.5s"></i><i style="top:43.7%;left:66.3%;width:10px;height:10px;margin:-5.0px 0 0 -5.0px;--d:7.5s;--w:-4.7s"></i><i style="top:61.5%;left:20.3%;width:18px;height:18px;margin:-9.0px 0 0 -9.0px;--d:10.1s;--w:-3.2s"></i><i style="top:68.5%;left:88.0%;width:8px;height:8px;margin:-4.0px 0 0 -4.0px;--d:7.7s;--w:-5.5s"></i><i style="top:15.4%;left:37.8%;width:3px;height:3px;margin:-1.5px 0 0 -1.5px;--d:5.1s;--w:-1.7s"></i><i style="top:15.4%;left:60.1%;width:6px;height:6px;margin:-3.0px 0 0 -3.0px;--d:6.0s;--w:-4.2s"></i><i style="top:23.6%;left:18.3%;width:5px;height:5px;margin:-2.5px 0 0 -2.5px;--d:8.8s;--w:-1.4s"></i><i style="top:8.4%;left:12.7%;width:6px;height:6px;margin:-3.0px 0 0 -3.0px;--d:6.8s;--w:-0.4s"></i><i style="top:22.3%;left:77.8%;width:4px;height:4px;margin:-2.0px 0 0 -2.0px;--d:8.5s;--w:-1.7s"></i><i style="top:8.0%;left:78.1%;width:4px;height:4px;margin:-2.0px 0 0 -2.0px;--d:8.5s;--w:-7.7s"></i><i style="top:13.3%;left:34.8%;width:3px;height:3px;margin:-1.5px 0 0 -1.5px;--d:4.7s;--w:-4.1s"></i><i style="top:2.7%;left:38.4%;width:3px;height:3px;margin:-1.5px 0 0 -1.5px;--d:6.7s;--w:-1.6s"></i><i style="top:23.8%;left:83.7%;width:3px;height:3px;margin:-1.5px 0 0 -1.5px;--d:8.8s;--w:-1.1s"></i><i style="top:18.9%;left:87.9%;width:3px;height:3px;margin:-1.5px 0 0 -1.5px;--d:5.4s;--w:-4.8s"></i><i style="top:5.1%;left:90.1%;width:6px;height:6px;margin:-3.0px 0 0 -3.0px;--d:6.8s;--w:-3.4s"></i><i style="top:90.3%;left:42.3%;width:3px;height:3px;margin:-1.5px 0 0 -1.5px;--d:6.3s;--w:-4.4s"></i><i style="top:43.7%;left:92.2%;width:3px;height:3px;margin:-1.5px 0 0 -1.5px;--d:7.7s;--w:-0.4s"></i><i style="top:68.3%;left:60.2%;width:4px;height:4px;margin:-2.0px 0 0 -2.0px;--d:5.2s;--w:-3.8s"></i><i style="top:69.5%;left:5.3%;width:5px;height:5px;margin:-2.5px 0 0 -2.5px;--d:8.4s;--w:-8.0s"></i><i style="top:49.2%;left:60.7%;width:4px;height:4px;margin:-2.0px 0 0 -2.0px;--d:4.7s;--w:-4.0s"></i></div>'


def topbar(current=""):
    links = "\n    ".join(
        f'<a href="{href}"{" aria-current=\"page\"" if name == current else ""}>{name}</a>' for name, href in NAV)
    return f'''<header class="topbar">
  <a class="mark" href="../home/index.html" aria-label="Amata Lynner, home"><img src="../../assets/img/brand/monogram-lavender.png" alt="AL"></a>
  <nav aria-label="Main">
    {links}
  </nav>
</header>
'''+WINKS


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
