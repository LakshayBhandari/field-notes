# Codex Self-Contained Folder — Design Spec

**Date:** 2026-05-19
**Status:** Approved by user ("approve" — user waived the spec-review gate; proceed to plan)
**Artifact:** restructure of everything codex-related under `/home/lakshay/practice/codex/`
**Builds on:** the multipage/theme/retone specs (which move into this layout)

---

## 1. Purpose

Make the codex a single self-contained project folder — all of its contents
(deployable site, validator, design docs, legacy snapshot) under
`/home/lakshay/practice/codex/` and nowhere else — while keeping the
deployable subset clean (only `site/` is ever served).

This is **sub-project 1**. A global maintenance skill is **sub-project 2** —
explicitly out of scope here; it gets its own spec/plan after this lands so it
can target the final layout.

### Success criteria

- Nothing codex-related lives outside `/home/lakshay/practice/codex/`.
- The deployable site is exactly `codex/site/` and contains only what should be
  served (pages + assets + `.nojekyll` + `DEPLOY.md`).
- `codex_check.py` runs from its new location and still gates the site:
  `PASS: codex site OK (8 pages)` exit 0.
- `DEPLOY.md`, `how-to-add.html`, and the project memory reference the new
  validator path and the new deploy target (`codex/site/`).
- A `codex/README.md` documents the layout, how to validate, how to deploy.
- Exactly one legacy single-file snapshot retained; practice-root copies gone.

### Non-goals (YAGNI)

- The maintenance skill (sub-project 2).
- Any content/wording/visual/theme change to the book.
- Rewriting the internal historical paths inside the moved design docs.
- Git (still not a repo); no CI.

---

## 2. Target layout

```
/home/lakshay/practice/codex/                 ← project root (everything here)
  site/                                        ← deployable (only this is served)
    index.html  ch-rolling.html  ch-authflow.html  ch-bcrypt.html
    ch-jwt.html  ch-useeffect.html  how-to-add.html  ch-TEMPLATE.html
    assets/codex.css  assets/codex.js
    .nojekyll  DEPLOY.md
  tooling/
    codex_check.py                             ← moved from practice/docs/superpowers/
  docs/
    specs/  2026-05-19-personal-codex-book-design.md
            2026-05-19-codex-theme-switcher-design.md
            2026-05-19-codex-multipage-split-design.md
            2026-05-19-codex-callout-retone-design.md
            2026-05-19-codex-self-contained-folder-design.md   (this doc)
    plans/  2026-05-19-personal-codex-book.md
            2026-05-19-codex-theme-switcher.md
            2026-05-19-codex-multipage-split.md
            2026-05-19-codex-callout-retone.md
            2026-05-19-codex-self-contained-folder.md           (its plan)
  legacy/
    codex-singlefile.html                      ← one copy of the pre-split book
  README.md
```

The current site files (currently directly under `codex/`) move into
`codex/site/`. `.nojekyll` moves with them.

## 3. Validator relocation & path fix

`codex_check.py` moves to `codex/tooling/codex_check.py`. Its path derivation
changes from:

```python
ROOT = pathlib.Path(__file__).resolve().parents[2]   # practice/
SITE = ROOT / "codex"
```

to:

```python
PROJECT = pathlib.Path(__file__).resolve().parent.parent   # codex/
SITE = PROJECT / "site"
```

All other validator logic (PAGES, CHAPTERS, content tokens, retone
assertions, light-var coverage, relative-link / parse / DOCTYPE checks) is
unchanged — only the site-root derivation moves. Add a structural
pre-check: fail clearly if `PROJECT/"site"`, `PROJECT/"tooling"`, or
`PROJECT/"docs"` is missing. Success message stays
`PASS: codex site OK (8 pages)`.

## 4. Reference updates (operational only)

- `codex/site/DEPLOY.md`: deploy target becomes `codex/site/` (GH Pages folder
  / Vercel Root Directory = `codex/site`); the validate command becomes
  `python3 ../tooling/codex_check.py` (run from `site/`) — or the absolute
  path; phrased so it's unambiguous from the source checkout.
- `codex/site/how-to-add.html`: the "run the validator" line updated to
  `python3 ../tooling/codex_check.py` (the page lives in `site/`, validator is
  a sibling dir up).
- Project memory `personal-codex-book.md`: all paths updated to the new
  layout (site at `codex/site/`, validator at `codex/tooling/codex_check.py`,
  docs under `codex/docs/`, legacy at `codex/legacy/codex-singlefile.html`).
- The moved design docs (`codex/docs/specs|plans/*`) are **not** edited; a line
  in `README.md` states their internal paths are historical and the current
  layout is authoritative.

## 5. Legacy de-duplication

`/home/lakshay/practice/codex.html` and
`/home/lakshay/practice/codex.legacy.html` are byte-identical (21345 bytes).
Retain one as `codex/legacy/codex-singlefile.html`; delete both
practice-root files. Nothing references them programmatically (personal
artifact); memory updated to the new path.

## 6. README.md

`codex/README.md` (concise): what the codex is; the `site/ tooling/ docs/
legacy/` layout; `python3 tooling/codex_check.py` to validate (must PASS);
deploy = serve `codex/site/` (point to `site/DEPLOY.md`); note that
`docs/` are historical design records and this README + the live `site/` are
authoritative.

## 7. Risks / decisions

- **Validator is the test harness for its own move.** Sequence so the
  validator is fixed and re-greened after the site move (red while paths
  mismatch, green once `SITE` points at `codex/site/`).
- **No path rewrite of historical docs** — deliberate (churn/error risk;
  non-executable). README disambiguates.
- **Deploy target changed** (`codex/` → `codex/site/`): DEPLOY.md is the only
  deploy-facing doc and is updated; no deployment exists yet so no live break.
- `practice/` is NOT a git repo — file moves are `mv`; no commits; save +
  validator checkpoints.
- Every spec/plan currently under `practice/docs/superpowers/` is
  codex-related, so all of them move into `codex/docs/`. The now-empty
  `practice/docs/superpowers/{specs,plans}/` dirs are left in place (harmless;
  not deleted). This spec + its plan are written there first, then moved with
  the rest.
