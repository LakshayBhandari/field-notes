# Deploying the Codex site

This is a static site — no build step. Everything in `codex/site/` is the site.

## GitHub Pages
1. Put the contents of `codex/site/` at the root of a repo (or in `/docs`).
2. Repo → Settings → Pages → Source: the branch, folder `/ (root)` (or `/docs`).
3. Wait for the build; site is at `https://<user>.github.io/<repo>/`.
4. `.nojekyll` is included so Pages serves every file untouched.
   All links are relative, so the subpath URL works as-is.

## Vercel
1. Import the repo. Framework Preset: **Other**.
2. Set the project **Root Directory** to `codex/site`. Leave Build Command empty
   (no build step — Vercel serves that folder's static files directly).
3. Deploy. No env vars, no server.

## Notes
- localStorage theme persistence is reliable on https:// (the file:// caveat
  does not apply once deployed).
- To add a chapter: copy `ch-TEMPLATE.html` (see `how-to-add.html`), then run
  `python3 ../tooling/codex_check.py` (from `codex/site/`) to validate.
