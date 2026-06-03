# Codex Theme Switcher — Design Spec

**Date:** 2026-05-19
**Status:** Approved by user ("approve, just start doing it" — user waived the spec-review gate; proceed straight to plan)
**Artifact:** `/home/lakshay/practice/codex.html` (enhancement) + `/home/lakshay/practice/docs/superpowers/codex_check.py` (validator)
**Builds on:** `2026-05-19-personal-codex-book-design.md`

---

## 1. Purpose

Make `codex.html`'s theme centralized and live-switchable, with the choice
remembered across reloads. Ship two themes: **Dark** (current, default) and
**Light**. Adding more themes later must be a one-block edit.

### Success criteria

- A `<select>` in the existing sticky control bar switches the whole page's
  theme instantly.
- The chosen theme persists across reloads (best-effort on `file://`).
- No flash of the wrong theme on load.
- All theme colors live in one CSS section; the rest of the CSS is unchanged
  and still references `var(--…)`.
- `codex_check.py` still passes and now regression-checks the theme system.

### Non-goals (YAGNI)

- No `prefers-color-scheme` auto-detection.
- No per-chapter / per-section theming.
- No themes beyond Dark and Light in this iteration.

---

## 2. Centralized palettes

Replace the single `:root{…}` rule with theme-scoped blocks in one contiguous
CSS section:

- `:root, :root[data-theme="dark"] { … }` — the **current dark values
  verbatim**, serves as the default when no `data-theme` is set.
- `:root[data-theme="light"] { … }` — a light value for **every** variable the
  dark block defines.

To make each theme a single self-contained block, the few remaining hardcoded
colors are promoted to CSS variables (this is the "centralized" requirement):

| Currently hardcoded | New variable | Dark value | Light value |
|---|---|---|---|
| `.slip` bg `rgba(240,136,62,0.10)` / border `rgba(240,136,62,0.35)` | `--slip-bg` / `--slip-border` | as today | light-tuned amber tint |
| `.caveat` bg `rgba(46,201,184,0.10)` / border `rgba(46,201,184,0.35)` | `--caveat-bg` / `--caveat-border` | as today | light-tuned teal tint |
| `.controls` bg `rgba(14,17,22,0.92)` | `--controls-bg` | as today | translucent light |
| `pre`/`code` `color:#d6deeb` | `--code-text` | `#d6deeb` | dark-on-light code text |

`.slip`/`.caveat` keep `border-left-color:var(--accent)`/`var(--secondary)`
(already variables). No selector other than these and `:root` changes; all
other rules already use `var(--…)`.

Light theme palette (concrete values, to be finalized in the plan; readable,
WCAG-reasonable contrast, same accent family tuned for light):
`--bg:#fbfbfd; --bg-card:#f1f2f5; --bg-code:#f3f4f7; --text:#3a4250;
--text-dim:#5a6170; --text-bright:#0f1419; --border:#dfe2e8;
--border-strong:#c4c9d4; --primary:#c2185b; --secondary:#0a7a6f;
--accent:#b83a0a; --on-color:#ffffff; --blue:#1d4ed8; --code-text:#1f2430;`
(secondary/accent darkened for WCAG-AA contrast on light; plus light
variants of yellow/red/violet/green and the callout/controls vars).

---

## 3. Switcher UI

A `<select id="theme-select">` placed in the existing `.controls` bar, after
the Expand all / Collapse all buttons:

```html
<select id="theme-select" onchange="setTheme(this.value)" aria-label="Theme">
  <option value="dark">Dark</option>
  <option value="light">Light</option>
</select>
```

`setTheme(name)` (added to the existing `<script>` at end of body):
- sets `document.documentElement.setAttribute('data-theme', name)`
- `try { localStorage.setItem('codex-theme', name) } catch (e) {}`
- keeps the select's value in sync.

Minimal CSS so the select matches the existing control buttons (reuse
`.controls button` styling family via a shared rule or a `.controls select`
rule using the same vars).

---

## 4. Persistence + no-flash

An inline script in `<head>` (before `<body>`, so it runs before first paint):

```html
<script>
  try {
    var t = localStorage.getItem('codex-theme');
    if (t) document.documentElement.setAttribute('data-theme', t);
  } catch (e) {}
</script>
```

On `DOMContentLoaded`, sync `#theme-select.value` to the current
`data-theme` (default `'dark'` when absent). No saved value → Dark (the
default `:root` block). All `localStorage` access wrapped in try/catch so a
blocked store degrades silently to Dark.

**Caveat (documented, accepted):** `localStorage` on `file://` persists in
Firefox and Chrome but is not guaranteed in every browser; worst case the book
opens in Dark each time. Acceptable for a personal local file.

---

## 5. Growth + tests

- Append a one-line "How to add a theme" note to the existing
  `id="how-to-add"` section: add one `:root[data-theme="NAME"]{…}` block and
  one `<option value="NAME">`.
- `codex_check.py` gains assertions: `:root[data-theme="dark"]`,
  `:root[data-theme="light"]`, `id="theme-select"`, `function setTheme(`,
  `'codex-theme'` localStorage key, the no-flash head script, and the new
  `--slip-bg` / `--controls-bg` / `--code-text` variables (presence in both
  theme blocks). Existing assertions remain; validator must stay `PASS` and the
  HTML must still parse via `html.parser`.

---

## 6. Risks

- **Variable coverage:** the Light block must define every variable the Dark
  block defines (including the newly promoted ones) or some elements fall back
  to inherited/invalid values. The validator checks presence; the plan lists
  the full variable set explicitly.
- **No-flash ordering:** the head script must appear before any `<body>`
  content and before the stylesheet's visual paint; placing it in `<head>`
  after the `<style>` is fine since it only sets an attribute.
- Not a git repo (`practice/`) — no commits; save + validator checkpoints.
