# amatalynner.com — design passport

## Palette (hers, collected deliberately — survives any redesign EXACTLY, not approximately)
Captured from the live Squarespace site, 15.10.2026.

- `#200F3A` — night: deep violet indigo, the ground of everything
- `#F3E5F5` — light: pale lavender, text and headings
- `#150830` — depth: darker indigo, links/accents
- Warm light lives in the IMAGES (forge neon, sunset bridge, yellow gloves) — the UI itself never competes with them: frames are the only warm thing in the night.

## Type
- Headings: **Cormorant SC** (small-caps serif, Google Fonts) — quiet elegance, pairs with the AL monogram
- Body: **Cormorant Garamond** (since the redesign, 31.10.2026); mono only for meta lines (edge print, FIG/SHEET-style labels)

## Signature
- AL monogram (вензель) — keeps its place as the closing signature.

## Direction (agreed 15.10.2026, evening) — SUPERSEDED by «D · Two Ways» below; kept as history
- The site is ONE continuous scene; scroll = time (same deterministic draw(t) engines as the films, t ← scroll).
- MERGED ARC (her call, 15.10): the path OPENS as the strict field of «Число два» — indigo at the edge of black, rare points of light at the threshold of visibility (закон видимости: barely-there made of MEANING, the eye leans in to check whether the light is real). As scroll carries on, the law releases: points approach, gain warmth, become frames-WINDOWS, windows become DOORS into normal section pages (films / projects / photography / about). From strict field to warm house in one continuous motion. Existing sections remain as destinations.
- Dramaturgy note: doubt-then-real-light is the site's own arc; it needs no caption.
- The order of lights along the path = her montage.
- Optional gesture: two lights visible at once faintly answer each other (перекличка, from «Число два»).
- Criterion (hers): the visitor must leave carrying ONE thing they remember. Catalogs fail this by construction.
- Liked references (hers): kalohane.com, davidlangarica.dev — both «scroll carries the eye»; neither palette nor mood is borrowed.

## Бриф-картка напрямку (16.10.2026 — ІСТОРІЯ, частково живе в D: плівка зі стіллами, альбом відбитків — обрано ПО НАМАЛЬОВАНОМУ: 4 листи Астри в D:\Lynner\сайт\*.png)
**Теза одним реченням: ніч, у якій світло проявляє носії — плівку і відбитки, — і все, що написано на носіях, правда.**
Гібрид: тіло «Проявки» (A) · кістяк «Журналу спостережень» (B) · техніка проявки відбитків із «Темної кімнати» (C). Незабутня річ: світло проявляє кадри з ночі.

Рішення, зафіксовані по листах:
1. **Hero глави 1 — плівкова лента на всю ширину зі СТІЛЛАМИ РІЗНИХ ФІЛЬМІВ** (її правка: не один кадр — фільмографія на одному носії). Крайова печать ЗВЕРХУ ленти: «AMATA LYNNER · RENDERED AT HOME · ▸ 2026». Нижче — самотня тепла точка, обіцянка наступного кадру.
2. **Глава 2 (фото-альбом) — стопка відбитків у стадіях проявки:** чиста бумага → напівпроявлений → готовий; листання = наступний відбиток доходить. Карандашні підписи на полях («№ 012 · Dnipro» — номер і місце, справжні). Вензель AL у куті.
3. **Детальні сторінки фільмів — картки спостережень** (лист B як шаблон): serif-заголовок + mono-метадані (instrument / exposure / date / seed / plate — УСІ справжні, з реальних рендерів), hairline-лінійки, ледь видна зоряна карта фоном.
4. **Температури:** ніч лишається НАША (#200F3A, глибока), тепло ленти беремо АСТРИНЕ (стара бронза, тепліша за #1A1114) — контраст холоду й тепла жорсткішає.
5. Ванночка (лист C) — не UI; з неї береться тільки матеріал: мокрий янтарний блік на папері, якщо знадобиться у главі 2.
6. Структурне з аудиту deslop (16.10): біти різнити вагою/зсувом/парою/довгим — вирішується МОНТАЖЕМ глави 1, разом із шоурілом.

Порядок збірки: шоуріл (монтаж, «очень красиво») → глава 1 навколо нього → глава 2 альбом → картки-сторінки. Перша версія не віддається (Iron Law deslop).

## LIVE since 31.10.2026 — «D · Two Ways» (her choice of four variants)
- Home: her Speos photograph (roses on a page of the Versailles directory, 1893) beside Astra's diffusion of it; one seam, DRAG. «I make images two ways».
- Films: endless film strips with the real title cards; each film has its own page. Photography: albums that turn like issuu (12 projects + People below a rule). About / Contact / Commercial in the same night.
- Commercial: Scent of Imagination and Blood Orange Soda as strips with a player under each; then ONE monitor — tabs (filters), stage, caption, a strip of live previews, ← →. A new piece is one item in `redesign/pages/commercial.json` → `_spots`. SOUND ON/OFF on every self-hosted player, in step, remembered.

## How the site is made now
1. Generators in `redesign/` (films/, album/, home/, pages/) build pages into their own folders; text comes from `content-src/interim/` — the interim site frozen on the day the redesign went live (every text node is checked: a build that loses a word stops).
2. `python redesign/publish.py` copies each built page onto its OLD address (index, about, contact, commercial, films.html, the film pages, projects.html, projects/*.html, people.html), rewrites relative paths, copies support files to `assets/site/`, and checks every local reference. Old links never break.
3. Video for Commercial lives in `assets/video/` (720p, CRF 24; previews 3 s muted).
Order: build_films → build_film_pages → build_albums → build_home → build_pages → publish.
