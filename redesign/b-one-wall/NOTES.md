# B — One Wall

**The idea in three sentences.** The site is a dark viewing room where only one work hangs at a time: the image sits matted inside a hairline frame on the deep-violet wall, with a proper wall label beneath it — title, medium, one sentence — and you *walk* past the works instead of scanning a grid. The grid is banned everywhere; the films page is a gallery index where choosing a title hangs its frame, and the Kherson reportage becomes eleven numbered prints behind one wall statement. It treats her photographs and film frames the way she treats prints — as objects worth standing in front of ("the black still has to be black").

**What a visitor remembers after leaving.** The act of looking at one photograph properly, in the dark, with nothing competing for attention — "her site is a room, and I stood in front of the work."

**What it costs to build fully.** Medium: the walk/hang mechanic is ~40 lines of vanilla JS reused across pages, no libraries, so the engineering is cheap. The real cost is curatorial and content-structural — every work needs a wall label written for it (title, medium line, one sentence), and preloading the neighbouring image matters so a "walk" never shows a blank wall. Deep-linking each print (URL hash per wall) and a no-JS fallback (plain vertical list of framed prints) are the two things the prototype skips that the full build needs.
