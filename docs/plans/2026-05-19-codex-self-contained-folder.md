# Codex Self-Contained Folder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move everything codex-related under `/home/lakshay/practice/codex/` (deployable `site/`, `tooling/` validator, `docs/`, `legacy/`, `README.md`) with the validator relocated + path-fixed and operational references updated.

**Architecture:** Pure filesystem reorg (`mv`) plus a small path fix in `codex_check.py` (its site root derivation) and text updates in `DEPLOY.md` / `how-to-add.html` / memory / a new `README.md`. The validator remains the single test harness; it goes red while the site root mismatches and green once it points at `codex/site/`.

**Tech Stack:** shell `mv`/`mkdir`/`rm`, Python 3 stdlib `codex_check.py`.

**Environment note:** `/home/lakshay/practice/` is **not** a git repo. No `git` steps — each task ends with a **Checkpoint** (save + validator/parse).

**Spec:** `/home/lakshay/practice/docs/superpowers/specs/2026-05-19-codex-self-contained-folder-design.md`

**Sequencing note:** the design docs (specs/plans, including THIS plan) are moved in the LAST task so the plan stays at its original path during execution of Tasks 1–4.

---

## File Structure (target)

```
codex/
  site/   index.html ch-rolling.html ch-authflow.html ch-bcrypt.html ch-jwt.html
          ch-useeffect.html how-to-add.html ch-TEMPLATE.html
          assets/codex.css assets/codex.js  .nojekyll  DEPLOY.md
  tooling/codex_check.py
  docs/specs/  (5 *-design.md)   docs/plans/  (5 plan .md)
  legacy/codex-singlefile.html
  README.md
```

Current → moves: `codex/*` (pages/assets/.nojekyll/DEPLOY.md) → `codex/site/`;
`docs/superpowers/codex_check.py` → `codex/tooling/codex_check.py`;
`docs/superpowers/{specs,plans}/2026-05-19-*codex*|*personal-codex*` →
`codex/docs/{specs,plans}/`; `codex.html`+`codex.legacy.html` → one
`codex/legacy/codex-singlefile.html`.

---

## Task 1: New skeleton + relocate & path-fix the validator (red)

**Files:**
- Create dirs: `codex/site/`, `codex/tooling/`, `codex/docs/specs/`, `codex/docs/plans/`, `codex/legacy/`
- Move + modify: `docs/superpowers/codex_check.py` → `codex/tooling/codex_check.py`

- [ ] **Step 1: Create the project skeleton dirs**

Run:
```bash
cd /home/lakshay/practice/codex
mkdir -p site tooling docs/specs docs/plans legacy
```

- [ ] **Step 2: Move the validator into tooling/**

Run:
```bash
mv /home/lakshay/practice/docs/superpowers/codex_check.py /home/lakshay/practice/codex/tooling/codex_check.py
```

- [ ] **Step 3: Fix the validator's site-root derivation**

In `/home/lakshay/practice/codex/tooling/codex_check.py`, replace exactly:

```python
ROOT = pathlib.Path(__file__).resolve().parents[2]   # /home/lakshay/practice
SITE = ROOT / "codex"
```

with:

```python
PROJECT = pathlib.Path(__file__).resolve().parent.parent   # /home/lakshay/practice/codex
SITE = PROJECT / "site"
```

Then, in `def main():`, replace exactly:

```python
    if not SITE.is_dir():
        print(f"FAIL: {SITE} is not a directory"); return 1
```

with:

```python
    for _d in ("site", "tooling", "docs"):
        if not (PROJECT / _d).is_dir():
            print(f"FAIL: project structure broken — missing codex/{_d}/"); return 1
    if not SITE.is_dir():
        print(f"FAIL: {SITE} is not a directory"); return 1
```

Also fix the now-stale FAIL message prefix — replace exactly:

```python
            fail(f"missing file: codex/{rel}")
```

with:

```python
            fail(f"missing file: codex/site/{rel}")
```

(Every `rel` — pages, `assets/codex.css`, `.nojekyll`, `DEPLOY.md` — now lives
under `codex/site/`, so the `codex/site/` prefix is correct and the diagnostic
matches the real checked path.)

No other validator logic changes (PAGES, CHAPTERS, CONTENT, retone
assertions, light-var coverage, relative-link/parse/DOCTYPE checks stay).

- [ ] **Step 4: Run validator — expect FAIL (site/ empty)**

Run: `python3 /home/lakshay/practice/codex/tooling/codex_check.py`
Expected: `FAIL:` listing `missing file: codex/site/index.html` and the other
pages/assets/.nojekyll/DEPLOY.md (site/ exists but is empty; the structure
pre-check passes because site/tooling/docs dirs exist). Python runs with no
error. This is the intended Task 1 red.

- [ ] **Step 5: Confirm the old validator path is gone**

Run: `test ! -e /home/lakshay/practice/docs/superpowers/codex_check.py && echo "old path clear"`
Expected: `old path clear`.

- [ ] **Step 6: Checkpoint**

`ls -la /home/lakshay/practice/codex` shows `site/ tooling/ docs/ legacy/` and
the original page files still directly under `codex/` (not yet moved).
`ls /home/lakshay/practice/codex/tooling/` shows `codex_check.py`. No git.

---

## Task 2: Move the site into `codex/site/` (green)

**Files:**
- Move: all current `codex/*.html`, `codex/assets/`, `codex/.nojekyll`, `codex/DEPLOY.md` → `codex/site/`

- [ ] **Step 1: Run validator — red for this task**

Run: `python3 /home/lakshay/practice/codex/tooling/codex_check.py`
Expected: FAIL — pages missing under `codex/site/`.

- [ ] **Step 2: Move every site file into site/**

Run (move the 8 html, the assets dir, the dotfile, DEPLOY.md — and nothing else):
```bash
cd /home/lakshay/practice/codex
mv index.html ch-rolling.html ch-authflow.html ch-bcrypt.html ch-jwt.html ch-useeffect.html how-to-add.html ch-TEMPLATE.html assets .nojekyll DEPLOY.md site/
```

- [ ] **Step 3: Run validator — expect PASS**

Run: `python3 /home/lakshay/practice/codex/tooling/codex_check.py`
Expected: `PASS: codex site OK (8 pages)` exit 0 (SITE now resolves to
`codex/site/` which holds all required files; all structural/content/retone
checks pass — content is unchanged, only relocated).

- [ ] **Step 4: Parse + structure check**

Run:
```bash
python3 -c "import html.parser,glob; [html.parser.HTMLParser().feed(open(f,encoding='utf-8').read()) for f in glob.glob('/home/lakshay/practice/codex/site/*.html')]; print('all parse')"
ls /home/lakshay/practice/codex
```
Expected: `all parse`; `ls codex/` shows ONLY `site tooling docs legacy`
(no stray html/assets left at `codex/` root).

- [ ] **Step 5: Checkpoint** — validator PASS from the new location; site fully under `codex/site/`.

---

## Task 3: Consolidate legacy + add README

**Files:**
- Create: `codex/legacy/codex-singlefile.html` (from the byte-identical pair)
- Delete: `/home/lakshay/practice/codex.html`, `/home/lakshay/practice/codex.legacy.html`
- Create: `codex/README.md`

- [ ] **Step 1: Verify the two legacy files are byte-identical, then keep one**

Run:
```bash
cmp /home/lakshay/practice/codex.html /home/lakshay/practice/codex.legacy.html && echo "identical"
mv /home/lakshay/practice/codex.legacy.html /home/lakshay/practice/codex/legacy/codex-singlefile.html
rm /home/lakshay/practice/codex.html
```
Expected: `identical`; afterward only `codex/legacy/codex-singlefile.html`
remains (both practice-root copies gone).

- [ ] **Step 2: Confirm no codex files left at practice root**

Run: `ls /home/lakshay/practice/ | grep -i '^codex' || echo "only the codex/ dir remains"`
Expected: shows just `codex` (the directory) — no `codex.html`/`codex.legacy.html`.

- [ ] **Step 3: Create `codex/README.md`**

Write `/home/lakshay/practice/codex/README.md` with exactly:

```markdown
# Codex — personal study book

A personal study book that explains a topic and resurfaces points that are
easy to get wrong, so they survive across rolling sessions.

## Layout
- `site/` — the deployable static site (the ONLY thing that gets served)
- `tooling/codex_check.py` — structural validator / test harness
- `docs/specs`, `docs/plans` — design records (point-in-time; their internal
  paths are historical — THIS README and the live `site/` are authoritative)
- `legacy/codex-singlefile.html` — the original pre-split single-file book

## Validate (after any change)
```
cd /home/lakshay/practice/codex
python3 tooling/codex_check.py
```
Must print `PASS: codex site OK (8 pages)`.

## Deploy
Serve `site/` as a static site. See `site/DEPLOY.md` (GitHub Pages / Vercel;
point the host at `codex/site/`).

## Add a chapter / theme
Open `site/how-to-add.html` and follow it; then run the validator above.
```

- [ ] **Step 4: Validator unaffected**

Run: `python3 /home/lakshay/practice/codex/tooling/codex_check.py`
Expected: still `PASS: codex site OK (8 pages)` (legacy/README are outside
`site/`; validator only gates `site/`).

- [ ] **Step 5: Checkpoint** — one legacy file under `codex/legacy/`, `README.md` present, validator PASS.

---

## Task 4: Update operational references

**Files:**
- Modify: `codex/site/DEPLOY.md`, `codex/site/how-to-add.html`
- Modify: `/home/lakshay/.claude/projects/-home-lakshay-practice-login/memory/personal-codex-book.md`

- [ ] **Step 1: DEPLOY.md — new deploy target + validate path**

In `/home/lakshay/practice/codex/site/DEPLOY.md`:

Replace `1. Put the contents of \`codex/\` at the root of a repo (or in \`/docs\`).`
with `1. Put the contents of \`codex/site/\` at the root of a repo (or in \`/docs\`).`

Replace the Vercel root-dir line `2. Set the project **Root Directory** to \`codex/\`. Leave Build Command empty`
with `2. Set the project **Root Directory** to \`codex/site\`. Leave Build Command empty`

Replace `  \`python3 docs/superpowers/codex_check.py\` from the source repo to validate.`
with `  \`python3 ../tooling/codex_check.py\` (from \`codex/site/\`) to validate.`

(If any line's surrounding text differs slightly, preserve it and change only
the `codex/`→`codex/site/` and the validator-path fragment.)

- [ ] **Step 2: how-to-add.html — validate command**

In `/home/lakshay/practice/codex/site/how-to-add.html`, replace exactly:
```
        <li>Run <code>python3 docs/superpowers/codex_check.py</code> — it must print <code>PASS</code> (it checks the new page's shell, relative-only links, callout structure, and that the index card resolves).</li>
```
with:
```
        <li>Run <code>python3 ../tooling/codex_check.py</code> (from <code>codex/site/</code>) — it must print <code>PASS</code> (it checks the new page's shell, relative-only links, callout structure, and that the index card resolves).</li>
```

- [ ] **Step 3: Update project memory**

In `/home/lakshay/.claude/projects/-home-lakshay-practice-login/memory/personal-codex-book.md`,
update the paths to the new layout:
- site is now `/home/lakshay/practice/codex/site/` (pages: `codex/site/ch-*.html`, assets `codex/site/assets/`)
- validator is now `python3 /home/lakshay/practice/codex/tooling/codex_check.py` (still must print `PASS: codex site OK (8 pages)`)
- specs/plans now under `/home/lakshay/practice/codex/docs/{specs,plans}/`
- legacy is `/home/lakshay/practice/codex/legacy/codex-singlefile.html`
- everything codex lives under `/home/lakshay/practice/codex/`; deploy target is `codex/site/`
Make the minimal edits to the existing memory file's path references (do not
rewrite unrelated content); keep it accurate and concise.

- [ ] **Step 4: Validator + parse unaffected**

Run:
```bash
python3 /home/lakshay/practice/codex/tooling/codex_check.py
python3 -c "import html.parser; html.parser.HTMLParser().feed(open('/home/lakshay/practice/codex/site/how-to-add.html',encoding='utf-8').read()); print('how-to-add parses')"
```
Expected: `PASS: codex site OK (8 pages)`; `how-to-add parses`. (The validator
does not assert the validate-command text, so these edits don't change its
result — but how-to-add must still parse and keep its `How to add a chapter`/
`How to add a theme` tokens, which are untouched.)

- [ ] **Step 5: Checkpoint** — DEPLOY.md/how-to-add point at new paths; memory synced; validator PASS.

---

## Task 5: Move design docs + final verification

**Files:**
- Move: the 5 codex specs + 5 codex plans (incl. this spec & plan) → `codex/docs/`

- [ ] **Step 1: Move all codex specs/plans into codex/docs/**

Run:
```bash
mv /home/lakshay/practice/docs/superpowers/specs/2026-05-19-personal-codex-book-design.md \
   /home/lakshay/practice/docs/superpowers/specs/2026-05-19-codex-theme-switcher-design.md \
   /home/lakshay/practice/docs/superpowers/specs/2026-05-19-codex-multipage-split-design.md \
   /home/lakshay/practice/docs/superpowers/specs/2026-05-19-codex-callout-retone-design.md \
   /home/lakshay/practice/docs/superpowers/specs/2026-05-19-codex-self-contained-folder-design.md \
   /home/lakshay/practice/codex/docs/specs/
mv /home/lakshay/practice/docs/superpowers/plans/2026-05-19-personal-codex-book.md \
   /home/lakshay/practice/docs/superpowers/plans/2026-05-19-codex-theme-switcher.md \
   /home/lakshay/practice/docs/superpowers/plans/2026-05-19-codex-multipage-split.md \
   /home/lakshay/practice/docs/superpowers/plans/2026-05-19-codex-callout-retone.md \
   /home/lakshay/practice/docs/superpowers/plans/2026-05-19-codex-self-contained-folder.md \
   /home/lakshay/practice/codex/docs/plans/
```
Expected: all 10 files moved; `ls /home/lakshay/practice/codex/docs/specs /home/lakshay/practice/codex/docs/plans` shows 5 each.

- [ ] **Step 2: Confirm nothing codex remains outside codex/**

Run:
```bash
ls /home/lakshay/practice/docs/superpowers/specs/ /home/lakshay/practice/docs/superpowers/plans/ 2>/dev/null | grep -i codex && echo "LEAK (bad)" || echo "no codex docs outside codex/"
ls /home/lakshay/practice/ | grep -i '^codex' 
find /home/lakshay/practice -maxdepth 1 -name 'codex*.html' | grep . && echo "LEAK (bad)" || echo "no codex html at practice root"
```
Expected: `no codex docs outside codex/`; the only practice-root match is the
`codex` directory; `no codex html at practice root`.

- [ ] **Step 3: Full validator pass from the new location**

Run: `python3 /home/lakshay/practice/codex/tooling/codex_check.py`
Expected: `PASS: codex site OK (8 pages)` exit 0.

- [ ] **Step 4: Parse all + structure proof**

Run:
```bash
python3 -c "import html.parser,glob; [html.parser.HTMLParser().feed(open(f,encoding='utf-8').read()) for f in glob.glob('/home/lakshay/practice/codex/site/*.html')]; print('all parse')"
find /home/lakshay/practice/codex -maxdepth 2 -type d | sort
ls /home/lakshay/practice/codex/docs/specs /home/lakshay/practice/codex/docs/plans /home/lakshay/practice/codex/legacy /home/lakshay/practice/codex/tooling
```
Expected: `all parse`; dirs show `codex/{site,site/assets,tooling,docs,docs/specs,docs/plans,legacy}`; specs=5, plans=5, legacy=`codex-singlefile.html`, tooling=`codex_check.py`.

- [ ] **Step 5: Final report (Checkpoint)**

Report: validator `PASS: codex site OK (8 pages)`; everything codex under
`/home/lakshay/practice/codex/`; nothing codex outside it; site clean
(`codex/site/` only); README + DEPLOY + how-to-add + memory consistent with
the new layout. (Manual browser check is the user's; headless relies on the
validator + parse.)

---

## Self-Review (completed during planning)

- **Spec coverage:** §1 success (nothing codex outside `codex/`; deployable=`site/`; validator runs new path & gates; DEPLOY/how-to-add/memory updated; README; one legacy file) → Tasks 1–5; §2 layout → Task 1 skeleton + Tasks 2/3/5 moves; §3 validator relocation & exact path fix + structure pre-check → Task 1 Step 3; §4 reference updates → Task 4 (+ README Task 3); §5 legacy de-dup → Task 3; §6 README → Task 3 Step 3; §7 risks (validator red→green sequencing; historical docs not rewritten — only moved; deploy target change in DEPLOY.md; not git; docs moved last so plan stays put) → task ordering + Task 5 last. Full coverage.
- **Placeholder scan:** every step is an exact command or exact old→new string or literal file content. No TBD/loose instructions. The DEPLOY.md edit notes "if surrounding text differs slightly, preserve it" — this is a precise fallback rule for a known-small textual drift, not a placeholder; the change fragments (`codex/`→`codex/site/`, validator path) are exact.
- **Name/type consistency:** `PROJECT`/`SITE`, `codex/site`, `codex/tooling/codex_check.py`, `codex/docs/{specs,plans}`, `codex/legacy/codex-singlefile.html`, `python3 ../tooling/codex_check.py`, success string `PASS: codex site OK (8 pages)` are spelled identically across the validator fix (Task 1), the moves (Tasks 2/5), references (Task 4), README (Task 3), and verification (Task 5).
