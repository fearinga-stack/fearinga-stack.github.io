# A — The Cut

**The idea in three sentences.** The site behaves like an edit, not a page: every screen is one full-bleed frame that holds until you cut to the next, with scroll-snap making each scroll a hard cut rather than a glide. A frame counter in the corner (03 / 09) makes the grammar explicit — you are moving through a sequence someone built, in the order she chose. There is no grid anywhere; the homepage *is* a montage of her strongest frames, and the Kherson reportage becomes a sequence of full-screen photographs with one prose card cut into the middle, exactly like an intertitle.

**What a visitor remembers after leaving.** The cut itself — "her site doesn't scroll, it cuts." They experienced the work the way she edits: one frame at a time, full screen, in sequence.

**What it costs to build fully.** Low-to-medium: pure CSS scroll-snap plus ~30 lines of JS for the counter and arrow keys, no libraries. Every existing page maps naturally (films → one film per cut, each project → its own sequence); the main work is editorial, not technical — choosing and ordering the frames for each sequence, and exporting heroes large enough for full-bleed (~2000px). Long galleries get long pages of full-size images, so lazy-loading and compressed JPGs matter; text-heavy pages (About) need a "prose card" treatment like the one shown in the Kherson sequence.
