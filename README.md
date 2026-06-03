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
