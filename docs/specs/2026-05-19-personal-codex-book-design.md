# Personal Codex — HTML Study Book — Design Spec

**Date:** 2026-05-19
**Status:** Approved (design), pending user spec review
**Artifact:** `/home/lakshay/practice/codex.html`
**Source material:** Claude Code session transcripts in
`/home/lakshay/.claude/projects/-home-lakshay-practice-login/` (the grill sessions)

---

## 1. Purpose

A single, self-contained, growing HTML book that serves as a **personalized
refresher**. For every concept it (a) explains the topic clearly and (b)
resurfaces the exact points the user got wrong, was imprecise about, or skipped
during grilling sessions — including points that got buried when those sessions
were compacted/continued across multiple chats ("rolling sessions").

It is a personal artifact, not project documentation. It lives at the
`practice/` root because it may eventually span multiple projects, not just
`login/`.

### Success criteria

- Opens by double-click in a browser, no server, no build step, no external
  network/font/JS dependencies (fully portable single file).
- A returning reader can, in one pass, both relearn a topic and see precisely
  where their past understanding was weak.
- New concepts can be added later without restructuring or breaking navigation.
- A polished, readable **dark** reading experience (its own standalone
  document; borrows only the typography convention from
  `practice/login/EXPLAINER.html`, not its light palette).

### Non-goals (YAGNI)

- No full-text search in v1 (TOC + anchor links are sufficient; can be added
  later).
- No backend, no automated transcript ingestion pipeline, no build tooling.
- Not project/API documentation; not a replacement for `EXPLAINER.html`.

---

## 2. Format & location

- **File:** `/home/lakshay/practice/codex.html` (single file; HTML + inline CSS
  + minimal inline vanilla JS for collapse/scrollspy).
- **Name:** `codex.html` (user-confirmed; rename trivially if desired).
- **No dependencies:** all CSS inline, no web fonts (system font stack), JS
  inline and minimal. Must work offline from `file://`.

---

## 3. Content model

Each **Chapter** corresponds to one concept and is composed of up to three
clearly-distinguished layers:

1. **Explanation** — refresher-style teaching of the topic, in the user's
   project context (concrete, uses real code/flow from `login/`).
2. **⚠️ Where you slipped** — one callout per fumble, sourced from the grill
   transcripts. Each callout follows a fixed micro-structure:
   - *What you said* (the user's answer/assumption, paraphrased)
   - *What's actually true* (the correction)
   - *Why it matters* (the consequence/stakes)
3. **🔄 Rolling-session caveat** — included only where a key point was buried
   because a session was compacted or continued across chats. Short note so the
   point is not lost again.

Layers 2 and 3 are visually distinct from layer 1 and from each other (color +
icon + label). A chapter always has layer 1; layers 2 and 3 appear only when
there is real material for them.

### Intro chapter

A first chapter, **"Read me first: rolling sessions"**, explains why this book
exists: what rolling/compacted sessions are, how sharp correction moments get
buried across continued chats (concrete example: the auth grill spanning
`1f808049` → `5ecebe87`), and how to read the ⚠️ and 🔄 callouts.

---

## 4. UI & navigation

- **No sidebar.** Navigation is page-based instead.
- **Home / landing index** at the top of the document: the book's front page —
  title, the "Read me first" framing, and a grid/list of **chapter links**
  (each with a one-line description) that jump to the chapter. This is the
  primary index.
- **In-page navigation links:** every chapter has a "↑ Back to home/index"
  link, and chapters cross-reference each other with real in-page links.
  Optional simple prev/next links between chapters.
- **Collapsible sections:** every chapter and major sub-section can
  expand/collapse. Global **Expand all / Collapse all** control.
- **Anchor links:** every chapter/sub-section has a stable `id`; the home index
  and all cross-references are real in-page anchor links.
- **Visual language:**
  - **Polished dark theme** (not the Solarized-light of `EXPLAINER.html`):
    deep ink page, soft off-white body text, brighter headings, comfortable
    for long reading. Keep the magenta/teal/amber accent family but tuned for
    contrast on dark. Reuse only the *typography* convention from
    `EXPLAINER.html` (serif headings, sans body, mono code), not its colors.
  - Explanation = default body styling.
  - ⚠️ "Where you slipped" = warning-accent callout box (amber/orange accent
    on a subtle dark-tinted background), labeled, with the three-line
    micro-structure.
  - 🔄 "Rolling-session caveat" = secondary-accent callout box (teal accent on
    a subtle dark-tinted background), labeled.
  - Code wells: dark, slightly lighter than the page, mono font, readable
    contrast.
- **Readability first:** generous line-height, constrained content column
  width, clear hierarchy. "Creative but readable" — styling serves legibility,
  not decoration for its own sake.

---

## 5. Growth model

- A bottom section **"How to add a chapter"** containing a documented,
  copy-paste **HTML chapter template** (skeleton with the home-index link
  entry, the chapter wrapper, and empty layer-1/layer-2/layer-3 blocks with
  comments).
- The chapter HTML structure is regular and predictable so:
  - the user can hand-add a chapter by copying the template, and
  - a future Claude session can re-read new transcripts and append chapters
    consistently.
- Adding a chapter must not require touching existing chapters (only adding one
  home-index link + one chapter block).

---

## 6. First build scope (v1 content)

Ship the complete shell **plus real chapters extracted from the auth grill
transcripts** (`5ecebe87`, `1f808049`), so the book is immediately useful:

1. **Read me first: rolling sessions** (intro/meta chapter, per §3).
2. **The auth flow end to end** — frontend ↔ backend request/response walk
   (grounded in `login/` and consistent with `EXPLAINER.html`).
3. **Password hashing & the bcrypt cost factor** — incl. the cost `n` =
   `2ⁿ` iterations point and the "slow hash vs. billions of guesses/sec"
   reasoning the user fumbled.
4. **JWT: access vs refresh, secrets, and the leakage attack** — incl. the
   skipped "if `JWT_ACCESS_SECRET` leaks, attacker runs
   `jwt.sign({ id: <anyone> }, leakedSecret)`" point.
5. **The `useEffect` async auth-load bug** — the inner-async-function fix and
   the cancelled-flag pattern.

Each chapter carries its ⚠️ "Where you slipped" callouts taken from the actual
grill correction moments, and 🔄 caveats where the point was buried by a rolled
session.

> Content accuracy note: chapter explanations and callouts are derived from the
> transcripts and the actual `login/` code. During implementation, the relevant
> transcript passages and source files will be read to keep technical claims
> correct (no invented details).

---

## 7. Risks / open considerations

- **Transcript size:** the source `.jsonl` files are large (up to ~3 MB).
  Extraction during implementation must target the grill correction moments
  rather than reading entire files indiscriminately.
- **Not a git repository:** `practice/` is not under version control, so the
  brainstorming "commit the spec" step is skipped; the spec is saved to
  `practice/docs/superpowers/specs/`.
- **Single-file growth:** acceptable for the foreseeable future; if the file
  becomes unwieldy the regular chapter structure allows a later split into a
  multi-page wiki without redesign.
