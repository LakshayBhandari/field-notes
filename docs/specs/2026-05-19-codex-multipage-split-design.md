# Codex Multi-Page Split — Design Spec

**Date:** 2026-05-19
**Status:** Approved by user ("yes do build it" — user waived the spec-review gate; proceed to plan)
**Artifact:** new `/home/lakshay/practice/codex/` static site, replacing the single-file `/home/lakshay/practice/codex.html`
**Builds on:** `2026-05-19-personal-codex-book-design.md`, `2026-05-19-codex-theme-switcher-design.md`

---

## 1. Purpose

The book will grow to many chapters and be deployed free (GitHub Pages or
Vercel). Split the single `codex.html` into a multi-page static site: one HTML
page per chapter, a home index page, shared CSS/JS so cross-cutting concerns
(theme, layout, nav) live in exactly one place. **An agent generates each
chapter page from a strict template — there is no build step.**

### Success criteria

- `codex/index.html` is the landing page (title, lede, chapter grid linking to
  each chapter page).
- Each chapter is its own page; deep-linkable by URL (e.g. `…/ch-jwt.html`).
- All links/asset refs are **relative** so the site works both at domain root
  and at a subpath (`user.github.io/repo/`).
- Theme (Dark default + Light) works and persists across page navigations with
  no flash on any page.
- Adding a chapter = copy `ch-TEMPLATE.html`, fill content, add one card to
  `index.html` (no build, no other files touched).
- `codex_check.py` is reworked to validate the whole directory and still
  passes; HTML parses on every page.
- Content of the 5 existing chapters + home + how-to + theme is migrated
  **verbatim** (no rewrite of prose/callouts/values).
- Deploys to GitHub Pages or Vercel with zero config beyond static hosting.

### Non-goals (YAGNI)

- No build/generator/framework, no bundler.
- No client-side search, no 404 page, no service worker.
- Still exactly two themes (Dark, Light); no new content.
- No SPA/client-router; plain multi-page navigation.

---

## 2. Directory layout

```
/home/lakshay/practice/codex/
  index.html          home: title, lede, chapter-grid → links to ch-*.html + how-to-add.html
  ch-rolling.html     chapter pages (one per chapter)
  ch-authflow.html
  ch-bcrypt.html
  ch-jwt.html
  ch-useeffect.html
  how-to-add.html     the "how to add a chapter / add a theme" guide page
  ch-TEMPLATE.html    canonical skeleton an agent copies for a new chapter
  assets/
    codex.css         ALL styling + both :root/[data-theme] palettes (single source)
    codex.js          setTheme(), localStorage persistence, select-sync, prev/next nav helper
  DEPLOY.md            GitHub Pages + Vercel steps
```

- The existing single file is preserved as
  `/home/lakshay/practice/codex.legacy.html` (nothing lost; not part of the
  deployed site).
- All `href`/`src` are relative with **no leading `/`** (`ch-jwt.html`,
  `assets/codex.css`, `index.html`).

---

## 3. Page anatomy

Every page (`index.html`, each `ch-*.html`, `how-to-add.html`,
`ch-TEMPLATE.html`) has the same shell:

- `<head>`:
  - `<meta charset>`, `<meta viewport>`, `<title>`.
  - `<link rel="stylesheet" href="assets/codex.css">`.
  - **Inline no-flash theme script** (the only intentionally duplicated code,
    ~2 lines): reads `localStorage['codex-theme']` in try/catch and sets
    `data-theme` on `<html>` before first paint. Must be inline (an external
    deferred script cannot beat first paint).
- `<body>`:
  - **Top nav bar** (`.topnav`, replaces the old sticky `.controls`):
    - On chapter pages: `← Home` (→ `index.html`), `‹ Prev` / `Next ›`
      (→ adjacent chapter page; omitted/disabled at the ends), and the theme
      `<select id="theme-select">`.
    - On `index.html`: title context + theme `<select>` (no prev/next).
  - Main content column (same typographic styling as today).
  - `<script src="assets/codex.js"></script>` at end of `<body>`.

Chapter pages no longer use `<details>` collapsing — each chapter is its own
always-visible page. The `openHashTarget` behavior is removed (URL = page now;
in-page sub-anchors may still use plain `#id`).

`index.html` keeps the chapter-grid card UI; cards link to `ch-*.html`
(+ a card for `how-to-add.html`).

## 4. Shared assets

- **`assets/codex.css`** — every CSS rule from the current `codex.html`
  `<style>` block, carried over **verbatim**, including:
  - `:root, :root[data-theme="dark"]` (default dark) and
    `:root[data-theme="light"]` palettes with the exact current values
    (incl. WCAG fixes: accent `#b83a0a`, secondary `#0a7a6f`,
    text-dim `#5a6170`), the promoted vars (`--slip-bg`/`--slip-border`/
    `--caveat-bg`/`--caveat-border`/`--controls-bg`/`--code-text`).
  - `.topnav` rules adapted from the existing `.controls`/`.controls select`
    rules (variable-driven, both themes), plus `.topnav a` link styling and a
    disabled/absent end-state for prev/next.
- **`assets/codex.js`** — `function setTheme(name)` (sets `data-theme`,
  `localStorage.setItem` in try/catch, syncs `#theme-select`); a
  `DOMContentLoaded` handler syncing the select to the active theme
  (default `'dark'`). No `toggleAll`/`openHashTarget` (not needed in
  multi-page). Prev/next links are static HTML per page (no JS needed);
  `codex.js` stays minimal.

## 5. Adding a chapter (growth model)

Documented in `how-to-add.html`:
1. Copy `ch-TEMPLATE.html` to `ch-NAME.html`.
2. Fill `<title>`, the `<h1>`/content, ⚠️/🔄 callouts; set the `← Home` and
   `‹ Prev`/`Next ›` hrefs (and update the previous last chapter's `Next ›`).
3. Add one `<a class="chapter-card" href="ch-NAME.html">…</a>` to
   `index.html`'s grid.
4. Run `python3 docs/superpowers/codex_check.py` → must PASS.

`ch-TEMPLATE.html` is a real file in the site dir (excluded from the index grid
and from prev/next chains) so the agent always has the exact contract to copy.

## 6. Validator rework

`/home/lakshay/practice/docs/superpowers/codex_check.py` is rewritten to
validate the directory (it remains the single test harness):

- The expected chapter set exists: `index.html`, `ch-rolling.html`,
  `ch-authflow.html`, `ch-bcrypt.html`, `ch-jwt.html`, `ch-useeffect.html`,
  `how-to-add.html`, `ch-TEMPLATE.html`, `assets/codex.css`, `assets/codex.js`,
  `DEPLOY.md`.
- Every `*.html` page: links `assets/codex.css` and `assets/codex.js`; contains
  the inline no-flash snippet (`localStorage.getItem('codex-theme')`) and the
  `#theme-select` control with Dark/Light options; uses only relative links
  (assert no `href="/`, no `src="/"`, no `http://`/`https://` external refs).
- `index.html`: chapter-grid cards link to files that actually exist.
- Each `ch-*.html` (excluding TEMPLATE): has `← Home` link to `index.html`,
  and prev/next hrefs (if present) point to existing files.
- Content sanity per chapter: the migrated ⚠️/🔄 callout structure
  (`callout slip`/`callout caveat`, `lbl`, `said`) and the chapter's key
  tokens (carried from the existing per-chapter assertions, e.g. `authMiddleware`,
  `2ⁿ`, `JWT_ACCESS_SECRET`, `useEffect(async`) appear on the right page.
- `assets/codex.css`: both `:root[data-theme="dark"]`/`["light"]` blocks
  present; the 23-variable light-coverage check (ported from the current
  validator).
- `assets/codex.js`: `function setTheme(name)`,
  `localStorage.setItem('codex-theme', name)`, select-sync present.
- Every `.html` parses via `html.parser`.
- Exit non-zero on any failure (same contract as today).

## 7. Deployment (DEPLOY.md)

- **GitHub Pages:** push the `codex/` contents to a repo; enable Pages on the
  branch/`/root` (or `/docs`); site served at `…/`. Add an empty `.nojekyll`
  file in `codex/` so Pages serves all files untouched. Relative paths make it
  work at the project subpath.
- **Vercel:** import the repo, framework preset "Other", output directory =
  `codex/` (or set root to `codex/`); no build command. Static deploy.
- Both: no env, no build step, no server.

## 8. Risks / decisions

- **No-flash duplication:** the ~2-line inline head script is repeated per page
  by necessity (must run before paint, can't be deferred-external). Accepted;
  the validator asserts its presence on every page so it can't be forgotten.
- **Prev/next hand-maintained:** static links per page; the validator checks
  they resolve, catching a missed update when a chapter is inserted.
- **Verbatim migration:** chapter prose/callouts/theme values must be moved
  unchanged; the plan diffs migrated content against the current `codex.html`
  to guarantee no drift.
- Not a git repo (`practice/`) — no commits; save + validator checkpoints.
  (Deployment later will put `codex/` into a git repo; out of scope here.)
