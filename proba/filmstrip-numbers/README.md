# Film strips: frame numbers running into each other on phones

Close-ups of the first strip on `films.html` and `commercial.html`, before and after the fix,
at 375×812 and 390×844 (phone, 3× density) and 1440×900 (desktop).

- `*-loading-*` — the still pictures have not arrived yet (a phone on a slow connection, or lazy pictures
  the browser has not fetched yet). This is what the owner saw.
- `*-loaded-*` — every picture is in.

## Cause
The stills have `loading="lazy"` and no `width`/`height`. A frame is as wide as its picture
(`.frame img{height:100%;width:auto}`), so until the picture arrives the frame is **0 px wide**.
Every frame number (`.fn`, pinned to the frame's right edge) then sits 8 px from the next one, and the
numbers of a whole strip pile up into one smear — `00 01A 01B 01C…` → "0020100201E"
(see `films-375-loading-before.png`). On a desktop the pictures usually arrive before anyone looks,
so it looked right there.

## Fix
`redesign/films/build_films.py` writes each frame picture's real `width`/`height` (read from the JPEG)
into the `<img>`. The browser takes the aspect ratio from them, so each frame has its real width from the
first paint, whether the picture is in yet or not; each number stays in its own frame. The CSS
(`height:100%;width:auto`) is unchanged, so the loaded strip is the same size as before. Plus
`white-space:nowrap` on `.fn` so a number never wraps.

Desktop at 1440: full-page screenshots of all 9 pages that carry strips (films, commercial, home, the six
film pages), before vs after, are pixel-identical (video/iframe players masked: their posters differ between
two runs of the same page anyway).

`shots.js` reproduces the close-ups: serve the site on :8765, then `node shots.js <outdir> <tag>`.
