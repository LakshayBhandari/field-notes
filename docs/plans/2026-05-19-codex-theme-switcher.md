# Codex Theme Switcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a centralized, live, persisted Dark/Light theme switcher to `/home/lakshay/practice/codex.html`.

**Architecture:** All palettes become CSS custom-property blocks scoped by `data-theme` on `<html>` (`:root, :root[data-theme="dark"]` = default dark; `:root[data-theme="light"]` overrides). A `<select>` in the existing sticky control bar calls `setTheme()` which sets the attribute and writes `localStorage["codex-theme"]`. A tiny `<head>` script applies the saved theme before first paint. The remaining hardcoded colors are promoted to variables so a theme is one self-contained block.

**Tech Stack:** HTML/CSS custom properties, vanilla JS, `localStorage`; `codex_check.py` (Python 3 stdlib) as the structural test harness.

**Environment note:** `/home/lakshay/practice/` is **not** a git repo. No `git commit` steps — each task ends with a **Checkpoint** (save + validator PASS + `html.parser` parses).

**Spec:** `/home/lakshay/practice/docs/superpowers/specs/2026-05-19-codex-theme-switcher-design.md`

---

## File Structure

- **Modify** `/home/lakshay/practice/codex.html` — the book (CSS `:root`/rules, controls markup, head script, body script, how-to-add note).
- **Modify** `/home/lakshay/practice/docs/superpowers/codex_check.py` — append theme assertions + a light-coverage check.

No new files. Each task's HTML edits use exact `old_string → new_string` replacements; all earlier (chapter/validator) content stays untouched and the existing assertions must keep passing.

---

## Task 1: Centralize palettes (Dark default + Light) and promote hardcoded colors to variables

**Files:**
- Modify: `/home/lakshay/practice/codex.html` (CSS `:root` block + `pre`/`code`/`.slip`/`.caveat`/`.controls` rules)
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 1: Add failing assertions**

In `/home/lakshay/practice/docs/superpowers/codex_check.py`, immediately **before** the `if failures:` line, add:

```python
    # Theme switcher — Task 1: centralized palettes
    need(':root[data-theme="dark"]', "dark theme block")
    need(':root[data-theme="light"]', "light theme block")
    need("--slip-bg:", "promoted slip-bg var")
    need("--caveat-bg:", "promoted caveat-bg var")
    need("--controls-bg:", "promoted controls-bg var")
    need("--code-text:", "promoted code-text var")
    need("background:var(--slip-bg)", "slip uses var")
    need("background:var(--controls-bg)", "controls uses var")
    need("color:var(--code-text)", "code uses var")
```

- [ ] **Step 2: Run validator — expect FAIL**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL listing the 9 new missing tokens (existing checks still pass).

- [ ] **Step 3: Replace the `:root {` opener with the dark-scoped selector**

Edit `/home/lakshay/practice/codex.html`. Replace exactly:

```
:root {
  /* Polished dark theme — deep ink page, soft off-white text */
```

with:

```
:root, :root[data-theme="dark"] {
  /* Polished dark theme — deep ink page, soft off-white text (default) */
```

- [ ] **Step 4: Add promoted dark vars + the full Light block**

In `/home/lakshay/practice/codex.html`, replace exactly:

```
  --sans: "Inter",system-ui,sans-serif;
}
* { box-sizing: border-box; }
```

with:

```
  --sans: "Inter",system-ui,sans-serif;
  --code-text: #d6deeb;
  --slip-bg: rgba(240,136,62,0.10); --slip-border: rgba(240,136,62,0.35);
  --caveat-bg: rgba(46,201,184,0.10); --caveat-border: rgba(46,201,184,0.35);
  --controls-bg: rgba(14,17,22,0.92);
}
:root[data-theme="light"] {
  /* Light theme — bright page, dark ink, accents tuned for light */
  --bg: #fbfbfd; --bg-card: #f1f2f5; --bg-code: #f3f4f7;
  --text: #3a4250; --text-dim: #5a6170; --text-bright: #0f1419;
  --border: #dfe2e8; --border-strong: #c4c9d4;
  --primary: #c2185b; --secondary: #0a7a6f; --accent: #b83a0a;
  --on-color: #ffffff;
  --yellow: #b7791f; --red: #c0392b; --violet: #6d28d9; --blue: #1d4ed8; --green: #15803d;
  --code-text: #1f2430;
  --slip-bg: rgba(194,65,12,0.08); --slip-border: rgba(194,65,12,0.30);
  --caveat-bg: rgba(13,143,130,0.08); --caveat-border: rgba(13,143,130,0.30);
  --controls-bg: rgba(251,251,253,0.92);
}
* { box-sizing: border-box; }
```

(Fonts and the `--accent-2`/`--accent-3` aliases are intentionally **not** repeated in the light block — they are declared once in `:root` and inherit; `var()` aliases re-resolve against the light `--primary`/`--secondary` automatically.)

- [ ] **Step 5: Rewire the remaining hardcoded colors to the new variables**

Make these four exact replacements in `/home/lakshay/practice/codex.html`:

Replace `pre { background:var(--bg-code); border:1px solid var(--border); border-radius:8px; padding:14px 16px; overflow:auto; font-size:13px; color:#d6deeb; }`
with `pre { background:var(--bg-code); border:1px solid var(--border); border-radius:8px; padding:14px 16px; overflow:auto; font-size:13px; color:var(--code-text); }`

Replace `code { background:var(--bg-code); padding:1px 5px; border-radius:4px; font-size:13px; color:#d6deeb; }`
with `code { background:var(--bg-code); padding:1px 5px; border-radius:4px; font-size:13px; color:var(--code-text); }`

Replace `.slip { background:rgba(240,136,62,0.10); border-color:rgba(240,136,62,0.35); border-left-color:var(--accent); }`
with `.slip { background:var(--slip-bg); border-color:var(--slip-border); border-left-color:var(--accent); }`

Replace `.caveat { background:rgba(46,201,184,0.10); border-color:rgba(46,201,184,0.35); border-left-color:var(--secondary); }`
with `.caveat { background:var(--caveat-bg); border-color:var(--caveat-border); border-left-color:var(--secondary); }`

Replace `.controls { position:sticky; top:0; background:rgba(14,17,22,0.92); backdrop-filter:blur(6px); padding:10px 0; border-bottom:1px solid var(--border); margin-bottom:24px; font-size:13px; z-index:5; }`
with `.controls { position:sticky; top:0; background:var(--controls-bg); backdrop-filter:blur(6px); padding:10px 0; border-bottom:1px solid var(--border); margin-bottom:24px; font-size:13px; z-index:5; }`

- [ ] **Step 6: Run validator — expect PASS**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `PASS: codex.html OK (<n> bytes)`. The pre-existing dark assertions (`--bg: #0e1116`, `--primary: #f778ba`, etc.) must still pass because the dark values are unchanged.

- [ ] **Step 7: Parse + dark-unchanged check**

Run:
```bash
python3 -c "import html.parser; p=html.parser.HTMLParser(); p.feed(open('/home/lakshay/practice/codex.html',encoding='utf-8').read()); print('parsed OK')"
grep -c '#d6deeb\|rgba(240,136,62\|rgba(14,17,22' /home/lakshay/practice/codex.html
```
Expected: `parsed OK`; the grep count is `0` (all old hardcoded colors now exist only as the new `--*` variable *values*, not in rules — note: the literal `rgba(240,136,62,0.10)` still appears once as the value of `--slip-bg`, so expect that grep to match the var definitions only — adjust expectation: the dark var **definitions** still contain these literals; what must be gone is their use in `.slip`/`.controls`/`pre` rules. Verify instead: `grep -n 'background:rgba(240,136,62\|background:rgba(14,17,22\|color:#d6deeb' codex.html` returns nothing.)

- [ ] **Step 8: Checkpoint**

Run: `ls -l /home/lakshay/practice/codex.html` — confirm saved. No git.

---

## Task 2: Theme switcher control in the sticky bar

**Files:**
- Modify: `/home/lakshay/practice/codex.html` (`.controls` markup + a `.controls select` CSS rule)
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 1: Add failing assertions**

In `codex_check.py`, before `if failures:` (after Task 1's block), add:

```python
    # Theme switcher — Task 2: switcher control
    need('id="theme-select"', "theme select control")
    need('<option value="dark">Dark</option>', "dark option")
    need('<option value="light">Light</option>', "light option")
    need('onchange="setTheme(this.value)"', "select wired to setTheme")
    need(".controls select {", "controls select styling")
```

- [ ] **Step 2: Run validator — expect FAIL** on the 5 new tokens.

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 3: Add the `<select>` to the controls bar**

In `/home/lakshay/practice/codex.html`, replace exactly:

```
  <div class="controls">
    <button onclick="toggleAll(true)">Expand all</button>
    <button onclick="toggleAll(false)">Collapse all</button>
  </div>
```

with:

```
  <div class="controls">
    <button onclick="toggleAll(true)">Expand all</button>
    <button onclick="toggleAll(false)">Collapse all</button>
    <select id="theme-select" onchange="setTheme(this.value)" aria-label="Theme">
      <option value="dark">Dark</option>
      <option value="light">Light</option>
    </select>
  </div>
```

- [ ] **Step 4: Add the `.controls select` CSS rule**

In `/home/lakshay/practice/codex.html`, replace exactly:

```
.controls button:hover { border-color:var(--primary); color:var(--text-bright); }
```

with:

```
.controls button:hover { border-color:var(--primary); color:var(--text-bright); }
.controls select { background:var(--bg-card); border:1px solid var(--border); border-radius:6px; padding:5px 10px; margin-left:6px; cursor:pointer; color:var(--text); font-family:var(--sans); font-size:13px; }
.controls select:hover { border-color:var(--primary); color:var(--text-bright); }
```

- [ ] **Step 5: Run validator — expect PASS.**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 6: Parse + Checkpoint**

Run: `python3 -c "import html.parser; p=html.parser.HTMLParser(); p.feed(open('/home/lakshay/practice/codex.html',encoding='utf-8').read()); print('parsed OK')"`
Expected: `parsed OK`. `ls -l` confirm saved. (Switcher will be inert until Task 3 adds `setTheme`.)

---

## Task 3: Persistence, no-flash head script, and `setTheme()`

**Files:**
- Modify: `/home/lakshay/practice/codex.html` (head script + end-of-body script)
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 1: Add failing assertions**

In `codex_check.py`, before `if failures:` (after Task 2's block), add:

```python
    # Theme switcher — Task 3: persistence + no-flash
    need("no-flash: apply saved theme", "head no-flash script")
    need("localStorage.getItem('codex-theme')", "reads saved theme")
    need("function setTheme(name)", "setTheme function")
    need("localStorage.setItem('codex-theme', name)", "persists theme")
    need("getElementById('theme-select')", "syncs select on load")
```

- [ ] **Step 2: Run validator — expect FAIL** on the 5 new tokens.

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 3: Add the no-flash head script**

In `/home/lakshay/practice/codex.html`, replace exactly:

```
</style>
</head>
```

with:

```
</style>
<script>
  /* no-flash: apply saved theme before first paint */
  try { var _t = localStorage.getItem('codex-theme'); if (_t) document.documentElement.setAttribute('data-theme', _t); } catch (e) {}
</script>
</head>
```

- [ ] **Step 4: Add `setTheme()` + load-sync to the end-of-body script**

In `/home/lakshay/practice/codex.html`, replace exactly:

```
window.addEventListener('DOMContentLoaded', openHashTarget);
window.addEventListener('hashchange', openHashTarget);
</script>
```

with:

```
window.addEventListener('DOMContentLoaded', openHashTarget);
window.addEventListener('hashchange', openHashTarget);

function setTheme(name) {
  document.documentElement.setAttribute('data-theme', name);
  try { localStorage.setItem('codex-theme', name); } catch (e) {}
  var sel = document.getElementById('theme-select');
  if (sel) sel.value = name;
}
window.addEventListener('DOMContentLoaded', function () {
  var cur = document.documentElement.getAttribute('data-theme') || 'dark';
  var sel = document.getElementById('theme-select');
  if (sel) sel.value = cur;
});
</script>
```

- [ ] **Step 5: Run validator — expect PASS.**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 6: Functional sanity (headless) + Checkpoint**

Run:
```bash
python3 -c "import html.parser; p=html.parser.HTMLParser(); p.feed(open('/home/lakshay/practice/codex.html',encoding='utf-8').read()); print('parsed OK')"
grep -n "data-theme=\"light\"\|setTheme(this.value)\|function setTheme(name)\|codex-theme" /home/lakshay/practice/codex.html
```
Expected: `parsed OK`; grep shows the light block, the select wiring, the function, and both localStorage references. The no-flash `<script>` sits between `</style>` and `</head>` (sets only an attribute, safe before paint). `ls -l` confirm saved.

---

## Task 4: "How to add a theme" note + light-coverage check + final verification

**Files:**
- Modify: `/home/lakshay/practice/codex.html` (how-to-add section)
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 1: Add failing assertions + light-coverage check**

In `codex_check.py`, before `if failures:` (after Task 3's block), add:

```python
    # Theme switcher — Task 4: growth note + light coverage
    need("How to add a theme", "how-to-add-theme note")
    import re as _re2
    _dark = _re2.search(r':root, :root\[data-theme="dark"\] \{(.+?)\}', html, _re2.S)
    _light = _re2.search(r':root\[data-theme="light"\] \{(.+?)\}', html, _re2.S)
    if not _dark or not _light:
        failures.append("could not locate dark/light theme blocks for coverage check")
    else:
        _required = ["--bg:", "--bg-card:", "--bg-code:", "--text:", "--text-dim:",
                     "--text-bright:", "--border:", "--border-strong:", "--primary:",
                     "--secondary:", "--accent:", "--on-color:", "--yellow:", "--red:",
                     "--violet:", "--blue:", "--green:", "--code-text:", "--slip-bg:",
                     "--slip-border:", "--caveat-bg:", "--caveat-border:", "--controls-bg:"]
        for _v in _required:
            if _v not in _light.group(1):
                failures.append(f"light theme missing variable {_v}")
```

- [ ] **Step 2: Run validator — expect FAIL** (`How to add a theme` missing; coverage check should otherwise already pass given Task 1).

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 3: Append the theme note to the how-to-add section**

In `/home/lakshay/practice/codex.html`, replace exactly:

```
<pre>&lt;a class=&quot;chapter-card&quot; href=&quot;#ch-NEW&quot;&gt;&lt;div class=&quot;ct&quot;&gt;Title&lt;/div&gt;&lt;div class=&quot;cd&quot;&gt;One line.&lt;/div&gt;&lt;/a&gt;</pre>
      <a class="tohome" href="#home">↑ Back to index</a>
```

with:

```
<pre>&lt;a class=&quot;chapter-card&quot; href=&quot;#ch-NEW&quot;&gt;&lt;div class=&quot;ct&quot;&gt;Title&lt;/div&gt;&lt;div class=&quot;cd&quot;&gt;One line.&lt;/div&gt;&lt;/a&gt;</pre>
      <h3>How to add a theme</h3>
      <p>Add one block next to the existing palettes — copy every variable from
      the light block and retune the values — then add one matching
      <code>&lt;option&gt;</code> to the theme select:</p>
<pre>:root[data-theme=&quot;NAME&quot;] { --bg: …; --text: …; /* …all vars from the light block… */ }

&lt;option value=&quot;NAME&quot;&gt;Label&lt;/option&gt;</pre>
      <a class="tohome" href="#home">↑ Back to index</a>
```

- [ ] **Step 4: Run validator — expect PASS** (note + full light coverage).

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `PASS: codex.html OK (<n> bytes)`

- [ ] **Step 5: Full well-formedness + final checks**

Run:
```bash
python3 -c "import html.parser,sys; p=html.parser.HTMLParser(); p.feed(open('/home/lakshay/practice/codex.html',encoding='utf-8').read()); print('parsed OK')"
grep -c 'data-theme' /home/lakshay/practice/codex.html
```
Expected: `parsed OK`; `data-theme` count ≥ 4 (dark scoped selector, light block, no-flash setAttribute, setTheme setAttribute, load-sync getAttribute).

- [ ] **Step 6: Final manual confirmation (note for the user, not blocking headless)**

Open `file:///home/lakshay/practice/codex.html`. Verify: default loads Dark; selecting **Light** instantly recolors the whole page (page, cards, code wells, ⚠️/🔄 callouts, control bar) with readable contrast; reload keeps Light; selecting Dark and reloading keeps Dark. (Headless: rely on validator + parse; this step is the user's acceptance check.)

- [ ] **Step 7: Checkpoint**

Run: `ls -l /home/lakshay/practice/codex.html` — confirm complete and saved. Report final byte size and that all validator checks pass.

---

## Self-Review (completed during planning)

- **Spec coverage:** §1 success → Tasks 1–4; §2 centralized palettes + promoted vars (table) → Task 1 Steps 3–5; §3 switcher in control bar → Task 2; §4 persistence + no-flash + load sync → Task 3; §5 growth note + validator assertions + light-coverage → Task 4 (+ assertions appended every task); §6 risks: variable coverage → Task 4 coverage check, no-flash ordering → Task 3 Step 3 places script between `</style>` and `</head>`, not-git → checkpoints. All covered.
- **Placeholder scan:** every step has exact `old_string → new_string` and exact commands; the only "…" are *inside* the how-to-add `<pre>` sample text shown to the reader (intentional template ellipsis), not plan placeholders.
- **Name/type consistency:** `data-theme`, `:root[data-theme="dark"]`/`["light"]`, `localStorage` key `'codex-theme'`, `function setTheme(name)`, `id="theme-select"`, vars `--slip-bg/--slip-border/--caveat-bg/--caveat-border/--controls-bg/--code-text` are spelled identically across Task 1 (definitions + rewire), Task 2 (select), Task 3 (scripts), Task 4 (coverage list), and every validator assertion.
