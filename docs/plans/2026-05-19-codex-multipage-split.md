# Codex Multi-Page Split Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the single `/home/lakshay/practice/codex.html` into a deploy-ready multi-page static site under `/home/lakshay/practice/codex/` (one HTML per chapter, shared CSS/JS, relative links), with content migrated verbatim.

**Architecture:** Shared `assets/codex.css` (all styling + both theme palettes, single source) and `assets/codex.js` (setTheme + persistence + select-sync). Each page is a full standalone HTML built from one shell (a tiny inline `<head>` no-flash theme script — the only intentionally duplicated code — + nav bar + content + shared `<script src>`). A **one-time** Python migration script extracts the 5 chapters + home + how-to-add verbatim from `codex.html` and emits the pages; ongoing chapter additions are done by copying `ch-TEMPLATE.html` (no build step). `codex_check.py` is rewritten as a directory validator and remains the single test harness.

**Tech Stack:** Static HTML/CSS/JS; Python 3 stdlib (`re`, `pathlib`, `html.parser`) for the one-time migration script and the validator.

**Environment note:** `/home/lakshay/practice/` is **not** a git repo. No `git commit` steps — each task ends with a **Checkpoint** (save + run validator + parse).

**Spec:** `/home/lakshay/practice/docs/superpowers/specs/2026-05-19-codex-multipage-split-design.md`

---

## File Structure

- **Create dir** `/home/lakshay/practice/codex/` — the deployable site.
  - `index.html`, `ch-rolling.html`, `ch-authflow.html`, `ch-bcrypt.html`, `ch-jwt.html`, `ch-useeffect.html`, `how-to-add.html`, `ch-TEMPLATE.html`
  - `assets/codex.css`, `assets/codex.js`
  - `.nojekyll`, `DEPLOY.md`
- **Create** `/home/lakshay/practice/codex.legacy.html` — copy of the current single file (nothing lost; not deployed).
- **Rewrite** `/home/lakshay/practice/docs/superpowers/codex_check.py` — directory validator (single test harness).
- **Create then delete** `/home/lakshay/practice/_migrate_codex.py` — one-time migration helper (removed in Task 5; not part of the site, not a build step).
- **Source (read-only, do not modify)** `/home/lakshay/practice/codex.html`.

**Design decision (verbatim-safety):** the nav bar reuses the existing `.controls` class and CSS verbatim (no rename to `.topnav`); a single `.controls a` rule is appended for nav links. This satisfies the spec's intent (variable-driven, single-source, theme-aware) with zero risk of restyling regressions. The old Expand/Collapse buttons are dropped (meaningless in multi-page); `toggleAll`/`openHashTarget` JS is dropped.

**Per-task validator reality:** the validator is rewritten whole in Task 1 (directory validation is not naturally incremental). It FAILS in Task 1 and each later task drives it greener; only Task 5 reaches full PASS. Each task below states its expected remaining failures so "green for this task" is unambiguous.

---

## Task 1: Directory validator (full rewrite) + scaffold

**Files:**
- Rewrite: `/home/lakshay/practice/docs/superpowers/codex_check.py`
- Create: `/home/lakshay/practice/codex/` (dir), `/home/lakshay/practice/codex/.nojekyll`
- Create: `/home/lakshay/practice/codex.legacy.html` (copy of `codex.html`)

- [ ] **Step 1: Write the new validator (this is the failing test harness)**

Overwrite `/home/lakshay/practice/docs/superpowers/codex_check.py` with exactly:

```python
#!/usr/bin/env python3
"""Directory validator for the multi-page codex site. Exit 0 = pass, 1 = fail."""
import sys, re, pathlib, html.parser

ROOT = pathlib.Path(__file__).resolve().parents[2]   # /home/lakshay/practice
SITE = ROOT / "codex"

PAGES = ["index.html", "ch-rolling.html", "ch-authflow.html", "ch-bcrypt.html",
         "ch-jwt.html", "ch-useeffect.html", "how-to-add.html", "ch-TEMPLATE.html"]
CHAPTERS = ["ch-rolling.html", "ch-authflow.html", "ch-bcrypt.html",
            "ch-jwt.html", "ch-useeffect.html"]  # prev/next chain order

LIGHT_VARS = ["--bg:", "--bg-card:", "--bg-code:", "--text:", "--text-dim:",
              "--text-bright:", "--border:", "--border-strong:", "--primary:",
              "--secondary:", "--accent:", "--on-color:", "--yellow:", "--red:",
              "--violet:", "--blue:", "--green:", "--code-text:", "--slip-bg:",
              "--slip-border:", "--caveat-bg:", "--caveat-border:", "--controls-bg:"]

# token -> page that must contain it (verbatim-migration content sanity)
CONTENT = {
    "ch-rolling.html":   ["1f808049", "Read me first"],
    "ch-authflow.html":  ["authMiddleware", "httpOnly", "401", "GET /me"],
    "ch-bcrypt.html":    ["2ⁿ", "compareSync(password, user.password)"],
    "ch-jwt.html":       ["JWT_REFRESH_SECRET", "jwt.sign({ id:"],
    "ch-useeffect.html": ["useEffect(async", "synchronous", "let cancelled = false;"],
    "how-to-add.html":   ["How to add a chapter", "How to add a theme"],
    "index.html":        ["<h1>Codex</h1>"],
}

def main():
    failures = []
    def fail(m): failures.append(m)

    if not SITE.is_dir():
        print(f"FAIL: {SITE} is not a directory"); return 1

    # Required files exist
    required = PAGES + ["assets/codex.css", "assets/codex.js", ".nojekyll", "DEPLOY.md"]
    for rel in required:
        if not (SITE / rel).exists():
            fail(f"missing file: codex/{rel}")

    # Per-page HTML checks
    for name in PAGES:
        p = SITE / name
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        # well-formed: html.parser is lenient (rarely raises); also assert structural bookends
        try:
            html.parser.HTMLParser().feed(h)
        except Exception as e:
            fail(f"{name}: html.parser error: {e}")
        if "<!DOCTYPE html>" not in h[:60]:
            fail(f"{name}: missing/late DOCTYPE")
        if "</html>" not in h:
            fail(f"{name}: missing closing </html>")
        # shared assets linked
        if 'href="assets/codex.css"' not in h:
            fail(f"{name}: missing link to assets/codex.css")
        if 'src="assets/codex.js"' not in h:
            fail(f"{name}: missing script assets/codex.js")
        # inline no-flash + theme select
        if "localStorage.getItem('codex-theme')" not in h:
            fail(f"{name}: missing inline no-flash theme script")
        if 'id="theme-select"' not in h:
            fail(f"{name}: missing theme select")
        if '<option value="dark">Dark</option>' not in h or \
           '<option value="light">Light</option>' not in h:
            fail(f"{name}: missing theme options")
        # relative links only: absolute-path refs anywhere, external URLs only in href/src attrs
        for bad in ['href="/', "href='/", 'src="/', "src='/"]:
            if bad in h:
                fail(f"{name}: non-relative ref {bad!r}")
        if re.search(r'(?:href|src)=["\']https?://', h):
            fail(f"{name}: external URL in href/src attr")
        # content sanity
        for tok in CONTENT.get(name, []):
            if tok not in h:
                fail(f"{name}: missing expected content {tok!r}")

    # index grid links resolve
    idx = SITE / "index.html"
    if idx.exists():
        ih = idx.read_text(encoding="utf-8")
        for tgt in re.findall(r'class="chapter-card" href="([^"]+)"', ih):
            if not (SITE / tgt).exists():
                fail(f"index.html: chapter-card target missing: {tgt}")
        for must in CHAPTERS + ["how-to-add.html"]:
            if f'href="{must}"' not in ih:
                fail(f"index.html: no card linking {must}")

    # each real chapter has Home link; prev/next (if present) resolve
    for name in CHAPTERS + ["how-to-add.html"]:
        p = SITE / name
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        if 'href="index.html"' not in h:
            fail(f"{name}: missing Home link to index.html")
        for tgt in re.findall(r'class="navlink[^"]*" href="([^"]+)"', h):
            if not (SITE / tgt).exists():
                fail(f"{name}: nav target missing: {tgt}")

    # shared CSS
    css_p = SITE / "assets/codex.css"
    if css_p.exists():
        c = css_p.read_text(encoding="utf-8")
        if ':root, :root[data-theme="dark"]' not in c:
            fail("codex.css: missing dark theme block")
        m = re.search(r':root\[data-theme="light"\] \{(.+?)\}', c, re.S)
        if not m:
            fail("codex.css: missing light theme block")
        else:
            for v in LIGHT_VARS:
                if v not in m.group(1):
                    fail(f"codex.css: light theme missing {v}")
        if ".controls a" not in c:
            fail("codex.css: missing .controls a nav-link rule")
        for v in ["--slip-bg:", "--caveat-bg:", "--controls-bg:", "--code-text:"]:
            if v not in c:
                fail(f"codex.css: missing promoted var {v}")

    # shared JS
    js_p = SITE / "assets/codex.js"
    if js_p.exists():
        j = js_p.read_text(encoding="utf-8")
        for tok in ["function setTheme(name)",
                    "localStorage.setItem('codex-theme', name)",
                    "getElementById('theme-select')"]:
            if tok not in j:
                fail(f"codex.js: missing {tok!r}")

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        return 1
    print(f"PASS: codex site OK ({len(PAGES)} pages)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run validator — expect FAIL**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `FAIL: /home/lakshay/practice/codex is not a directory` (exit 1).

- [ ] **Step 3: Scaffold the site dir + legacy copy**

Run:
```bash
mkdir -p /home/lakshay/practice/codex/assets
touch /home/lakshay/practice/codex/.nojekyll
cp /home/lakshay/practice/codex.html /home/lakshay/practice/codex.legacy.html
```

- [ ] **Step 4: Run validator — expect FAIL with the file-missing list**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL listing `missing file: codex/index.html`, the `ch-*.html`, `assets/codex.css`, `assets/codex.js`, `DEPLOY.md` (the dir + `.nojekyll` now exist; everything else still missing). This is the correct Task 1 red state.

- [ ] **Step 5: Checkpoint**

Run: `ls -la /home/lakshay/practice/codex /home/lakshay/practice/codex.legacy.html`
Confirm: `codex/` and `codex/assets/` dirs, `.nojekyll`, and `codex.legacy.html` exist. No git.

---

## Task 2: Shared assets — `codex.css` and `codex.js`

**Files:**
- Create: `/home/lakshay/practice/codex/assets/codex.css`
- Create: `/home/lakshay/practice/codex/assets/codex.js`

- [ ] **Step 1: Run validator (red for this task)**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL still lists `missing file: codex/assets/codex.css` and `codex/assets/codex.js` (plus all pages). After this task those two css/js failures and the css/js content checks must be gone.

- [ ] **Step 2: Create `assets/codex.css` from the current `<style>` verbatim + nav-link rule**

Run this exact command (extracts the inner of the current `<style>…</style>` verbatim, then appends the nav-link rule):

```bash
python3 - <<'PY'
import re, pathlib
src = pathlib.Path("/home/lakshay/practice/codex.html").read_text(encoding="utf-8")
css = re.search(r"<style>\n(.*?)\n</style>", src, re.S).group(1)
extra = (
"\n/* multi-page nav links (added for the split; variable-driven, theme-aware) */\n"
".controls a { color:var(--text); text-decoration:none; border:1px solid var(--border);"
" border-radius:6px; padding:5px 12px; font-size:13px;"
" font-family:var(--sans); }\n"
".controls a:hover { border-color:var(--primary); color:var(--text-bright); }\n"
".controls .brand { font-family:var(--serif); color:var(--text-bright);"
" font-size:16px; margin-right:auto; }\n"
".controls { display:flex; align-items:center; gap:10px; }\n"
)
pathlib.Path("/home/lakshay/practice/codex/assets/codex.css").write_text(css + extra, encoding="utf-8")
print("codex.css bytes:", len((css+extra)))
PY
```

(The verbatim `css` includes both `:root` palettes with the exact current values incl. WCAG fixes, the promoted vars, and the existing `.controls`/`.controls button`/`.controls select` rules — nothing is altered. The appended block only adds `.controls a`, `.brand`, and a flex layout for the nav bar.)

- [ ] **Step 3: Create `assets/codex.js`** with exactly:

```javascript
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
```

Write it to `/home/lakshay/practice/codex/assets/codex.js` (exact content above, no `toggleAll`/`openHashTarget`).

- [ ] **Step 4: Run validator — expect the css/js failures gone**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL no longer lists any `codex.css:` / `codex.js:` / `missing file: codex/assets/...` items. It still lists the missing pages (`index.html`, `ch-*.html`, `how-to-add.html`, `ch-TEMPLATE.html`, `DEPLOY.md`). That is correct green-for-Task-2.

- [ ] **Step 5: Checkpoint**

Run: `python3 -c "import pathlib; print(pathlib.Path('/home/lakshay/practice/codex/assets/codex.css').read_text(encoding='utf-8').count('data-theme'))"`
Expected: ≥ 2 (both palette selectors present). Confirm both asset files saved.

---

## Task 3: One-time migration — emit index + chapter pages + how-to-add

**Files:**
- Create then run: `/home/lakshay/practice/_migrate_codex.py`
- Create (by the script): `codex/index.html`, `codex/ch-rolling.html`, `codex/ch-authflow.html`, `codex/ch-bcrypt.html`, `codex/ch-jwt.html`, `codex/ch-useeffect.html`, `codex/how-to-add.html`

- [ ] **Step 1: Run validator (red for this task)**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL lists the missing `index.html` and `ch-*.html` / `how-to-add.html` pages.

- [ ] **Step 2: Create the one-time migration script**

Write `/home/lakshay/practice/_migrate_codex.py` with exactly:

```python
#!/usr/bin/env python3
"""ONE-TIME migration: split codex.html into codex/ pages. Deleted after use."""
import re, pathlib

SRC = pathlib.Path("/home/lakshay/practice/codex.html").read_text(encoding="utf-8")
OUT = pathlib.Path("/home/lakshay/practice/codex")

CHAIN = ["ch-rolling", "ch-authflow", "ch-bcrypt", "ch-jwt", "ch-useeffect"]

def relink(s):
    s = s.replace('href="#home"', 'href="index.html"')
    s = s.replace('href="#how-to-add"', 'href="how-to-add.html"')
    s = re.sub(r'href="#(ch-[\w-]+)"', r'href="\1.html"', s)
    return s

NOFLASH = (
    '<script>\n'
    '  /* no-flash: apply saved theme before first paint */\n'
    "  try { var _t = localStorage.getItem('codex-theme');"
    " if (_t) document.documentElement.setAttribute('data-theme', _t); } catch (e) {}\n"
    '</script>'
)
SELECT = ('<select id="theme-select" onchange="setTheme(this.value)" aria-label="Theme">'
          '<option value="dark">Dark</option><option value="light">Light</option></select>')

def page(title, nav_html, main_html):
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{title}</title>\n'
        '<link rel="stylesheet" href="assets/codex.css">\n'
        f'{NOFLASH}\n</head>\n<body>\n<main>\n'
        f'  <div class="controls">{nav_html}{SELECT}</div>\n'
        f'{main_html}\n'
        '</main>\n<script src="assets/codex.js"></script>\n</body>\n</html>\n'
    )

# --- chapters + how-to-add ---
block = re.compile(
    r'<details class="chapter" id="(?P<id>[\w-]+)"[^>]*>\s*'
    r'<summary><h2>(?P<title>.*?)</h2></summary>\s*'
    r'<div class="chapter-body">(?P<body>.*?)'
    r'\s*<a class="tohome" href="#home">↑ Back to index</a>\s*'
    r'</div>\s*</details>', re.S)

found = {}
for m in block.finditer(SRC):
    found[m.group("id")] = (m.group("title").strip(), m.group("body"))

assert set(found) >= set(CHAIN) | {"how-to-add"}, f"missing blocks: {set(CHAIN)|{'how-to-add'} - set(found)}"

def nav_for(cid):
    parts = ['<a class="navlink" href="index.html">← Home</a>']
    if cid in CHAIN:
        i = CHAIN.index(cid)
        if i > 0:
            parts.append(f'<a class="navlink navprev" href="{CHAIN[i-1]}.html">‹ Prev</a>')
        if i < len(CHAIN) - 1:
            parts.append(f'<a class="navlink navnext" href="{CHAIN[i+1]}.html">Next ›</a>')
    return "".join(parts)

for cid, (title, body) in found.items():
    main = f'  <h1>{title}</h1>\n  <div class="chapter-body">{relink(body)}</div>'
    (OUT / f"{cid}.html").write_text(page(title + " — Codex", nav_for(cid), main),
                                     encoding="utf-8")

# --- index (home) ---
home = re.search(r'<section id="home">(.*?)</section>', SRC, re.S).group(1)
home = relink(home)
# insert a how-to-add card before the closing </div> of the chapter-grid
home = re.sub(
    r'(\s*)</div>\s*$',
    r'\1  <a class="chapter-card" href="how-to-add.html"><div class="ct">'
    r'How to add a chapter / theme</div><div class="cd">The growth guide: '
    r'new chapter or new theme.</div></a>\n\1</div>',
    home, count=1, flags=re.S)
nav_home = '<span class="brand">Codex</span>'
(OUT / "index.html").write_text(
    page("Codex — Personal Study Book", nav_home, f'  <section id="home">{home}</section>'),
    encoding="utf-8")

print("emitted:", sorted(p.name for p in OUT.glob("*.html")))
```

- [ ] **Step 3: Run the migration script**

Run: `python3 /home/lakshay/practice/_migrate_codex.py`
Expected: `emitted: ['ch-authflow.html', 'ch-bcrypt.html', 'ch-jwt.html', 'ch-rolling.html', 'ch-useeffect.html', 'how-to-add.html', 'index.html']`

- [ ] **Step 4: Run validator — expect pages now pass**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL now lists ONLY `missing file: codex/ch-TEMPLATE.html` and `missing file: codex/DEPLOY.md` (and the per-`ch-TEMPLATE.html` page checks). No content/parse/relative-link failures for the 7 emitted pages. That is correct green-for-Task-3.

- [ ] **Step 5: Verbatim spot-check**

Run:
```bash
python3 - <<'PY'
import pathlib
leg = pathlib.Path("/home/lakshay/practice/codex.legacy.html").read_text(encoding="utf-8")
jwt = pathlib.Path("/home/lakshay/practice/codex/ch-jwt.html").read_text(encoding="utf-8")
snippet = "jwt.sign({ id: &lt;anyone&gt; }, leakedSecret)"
print("legacy has snippet:", snippet in leg, "| ch-jwt has snippet:", snippet in jwt)
PY
```
Expected: `legacy has snippet: True | ch-jwt has snippet: True` (proves callout content migrated verbatim).

- [ ] **Step 6: Checkpoint** — `ls -l /home/lakshay/practice/codex/*.html`; 7 files present.

---

## Task 4: `ch-TEMPLATE.html` + `DEPLOY.md`

**Files:**
- Create: `/home/lakshay/practice/codex/ch-TEMPLATE.html`
- Create: `/home/lakshay/practice/codex/DEPLOY.md`

- [ ] **Step 1: Run validator (red for this task)**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL lists `missing file: codex/ch-TEMPLATE.html` and `missing file: codex/DEPLOY.md` (and the TEMPLATE page checks). Nothing else.

- [ ] **Step 2: Create `codex/ch-TEMPLATE.html`** with exactly:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NEW CHAPTER TITLE — Codex</title>
<link rel="stylesheet" href="assets/codex.css">
<script>
  /* no-flash: apply saved theme before first paint */
  try { var _t = localStorage.getItem('codex-theme'); if (_t) document.documentElement.setAttribute('data-theme', _t); } catch (e) {}
</script>
</head>
<body>
<main>
  <!-- TEMPLATE: replace ch-PREV.html / ch-NEXT.html with the real adjacent chapter filenames, or delete the link that does not apply (the first chapter has no Prev, the last has no Next). -->
  <div class="controls"><a class="navlink" href="index.html">← Home</a><a class="navlink navprev" href="ch-PREV.html">‹ Prev</a><a class="navlink navnext" href="ch-NEXT.html">Next ›</a><select id="theme-select" onchange="setTheme(this.value)" aria-label="Theme"><option value="dark">Dark</option><option value="light">Light</option></select></div>
  <h1>NEW CHAPTER TITLE</h1>
  <div class="chapter-body">
    <p>Explanation…</p>
    <div class="callout slip">
      <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
      <p class="said">What I said…</p>
      <p><strong>What's true:</strong> …</p>
      <p><strong>Why it matters:</strong> …</p>
    </div>
    <div class="callout caveat">
      <div class="lbl">🔄 ROLLING-SESSION CAVEAT</div>
      <p>Only if a point got buried by a session roll.</p>
    </div>
  </div>
</main>
<script src="assets/codex.js"></script>
</body>
</html>
```

(To use: copy to `ch-NAME.html`, set `<title>`/`<h1>`, fill content, fix the `ch-PREV`/`ch-NEXT` hrefs and the previous last chapter's `Next ›`, then add an `<a class="chapter-card" href="ch-NAME.html">` card to `index.html`. The validator excludes `ch-TEMPLATE.html` from the chapter chain and index-grid requirements but still checks its shell.)

- [ ] **Step 3: Create `codex/DEPLOY.md`** with exactly:

```markdown
# Deploying the Codex site

This is a static site — no build step. Everything in `codex/` is the site.

## GitHub Pages
1. Put the contents of `codex/` at the root of a repo (or in `/docs`).
2. Repo → Settings → Pages → Source: the branch, folder `/ (root)` (or `/docs`).
3. Wait for the build; site is at `https://<user>.github.io/<repo>/`.
4. `.nojekyll` is included so Pages serves every file untouched.
   All links are relative, so the subpath URL works as-is.

## Vercel
1. Import the repo. Framework Preset: **Other**.
2. Set the project **Root Directory** to `codex/`. Leave Build Command empty
   (no build step — Vercel serves that folder's static files directly).
3. Deploy. No env vars, no server.

## Notes
- localStorage theme persistence is reliable on https:// (the file:// caveat
  does not apply once deployed).
- To add a chapter: copy `ch-TEMPLATE.html` (see `how-to-add.html`), then run
  `python3 docs/superpowers/codex_check.py` from the source repo to validate.
```

- [ ] **Step 4: Run validator — expect near-full pass**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `PASS: codex site OK (8 pages)` (exit 0) — all files now exist and pass. If anything still fails, fix per the message before proceeding.

- [ ] **Step 5: Checkpoint** — `ls -l /home/lakshay/practice/codex/` shows all 8 html + assets/ + .nojekyll + DEPLOY.md.

---

## Task 5: Final verification + remove one-time migration script

**Files:**
- Delete: `/home/lakshay/practice/_migrate_codex.py`
- Verify: whole `/home/lakshay/practice/codex/`

- [ ] **Step 1: Remove the one-time migration helper**

Run: `rm /home/lakshay/practice/_migrate_codex.py`
(The site is committed static files; the script was one-time and is not part of deploy or the validator.)

- [ ] **Step 2: Full validator pass (must be green now)**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `PASS: codex site OK (8 pages)` (exit 0). The validator does not depend on the deleted script.

- [ ] **Step 3: Parse every page independently**

Run:
```bash
python3 - <<'PY'
import pathlib, html.parser
d = pathlib.Path("/home/lakshay/practice/codex")
for f in sorted(d.glob("*.html")):
    html.parser.HTMLParser().feed(f.read_text(encoding="utf-8"))
    print("parsed OK:", f.name)
PY
```
Expected: `parsed OK:` for all 8 html files, no exceptions.

- [ ] **Step 4: Relative-links + theme-chain integrity sweep**

Run:
```bash
cd /home/lakshay/practice/codex
grep -RE 'href="/|src="/|http://|https://' *.html assets/ && echo "FOUND absolute/external refs (BAD)" || echo "NO absolute/external refs"
grep -c "localStorage.getItem('codex-theme')" *.html | grep -v ':1$' || echo "every page has exactly one no-flash snippet"
```
Expected: `NO absolute/external refs`; the second line prints `every page has exactly one no-flash snippet` (every page count = 1).

- [ ] **Step 5: Verbatim migration proof (content unchanged vs legacy)**

Run:
```bash
python3 - <<'PY'
import pathlib, re
leg = pathlib.Path("/home/lakshay/practice/codex.legacy.html").read_text(encoding="utf-8")
d = pathlib.Path("/home/lakshay/practice/codex")
checks = {
 "ch-bcrypt.html": "<code>2ⁿ</code> iterations",
 "ch-useeffect.html": "let cancelled = false;",
 "ch-authflow.html": "Protected calls (e.g. <code>GET /me</code>, L199)",
 "ch-jwt.html": "jwt.sign({ id: &lt;anyone&gt; }, leakedSecret)",
}
for f, snip in checks.items():
    in_leg = snip in leg
    in_new = snip in (d / f).read_text(encoding="utf-8")
    print(f, "legacy=", in_leg, "new=", in_new, "OK" if (in_leg and in_new) else "MISMATCH")
PY
```
Expected: every line ends `OK` (each chapter's distinctive content survived verbatim). If any `MISMATCH`, the migration altered content — stop and fix the migration before deleting was done (re-create script from Task 3, re-run, re-verify).

- [ ] **Step 6: Final manual confirmation (user acceptance — headless, deferred)**

State to the user: open `file:///home/lakshay/practice/codex/index.html`. Verify: home grid links to each chapter page; a chapter page shows ← Home / ‹ Prev / Next › + theme select; switching to Light then navigating Next keeps Light (no flash); deep-linking `…/ch-jwt.html` opens directly. (Headless: rely on validator + parse + the sweeps above; this step is the user's check.)

- [ ] **Step 7: Checkpoint**

Run: `ls -lR /home/lakshay/practice/codex` and report the final tree, that `_migrate_codex.py` is gone, `codex.legacy.html` is retained, and the validator PASSes.

---

## Self-Review (completed during planning)

- **Spec coverage:** §1 success → Tasks 1–5; §2 layout (all files incl. `.nojekyll`, `codex.legacy.html`) → Task 1/3/4; §3 page anatomy (link css, inline no-flash, nav bar, `<script src>`) → migration `page()` template Task 3 + `ch-TEMPLATE.html` Task 4; §4 shared assets verbatim CSS + minimal JS → Task 2; §5 growth model (`ch-TEMPLATE.html` + how-to-add page) → Task 3/4; §6 validator rework (every listed check) → Task 1 validator code; §7 deployment → `DEPLOY.md` + `.nojekyll` Task 4; §8 risks (no-flash dup asserted per page, prev/next resolve check, verbatim diff) → validator + Task 3 Step 5 / Task 5 Step 5. The `.controls`-vs-`.topnav` deviation is documented in File Structure with rationale (verbatim-safety) and the validator checks `.controls a` + nav-target resolution accordingly.
- **Placeholder scan:** all code is complete and literal (validator, migration script, css-extraction command, codex.js, ch-TEMPLATE.html, DEPLOY.md). The only `…` are inside the `ch-TEMPLATE.html` sample prose (intentional template fill-ins for the human/agent author), not plan placeholders.
- **Name/type consistency:** validator `CHAIN`/`CHAPTERS` order, `class="navlink"` (used by migration `nav_for` and asserted by the validator's `class="navlink[^"]*"` regex and `ch-TEMPLATE.html`), `id="theme-select"`, no-flash token `localStorage.getItem('codex-theme')`, `function setTheme(name)`, the `.controls` container + `.controls a` rule, and the page filenames (`ch-<id>.html`, `how-to-add.html`, `index.html`) are spelled identically across the validator, the migration script, the template, and every task.
