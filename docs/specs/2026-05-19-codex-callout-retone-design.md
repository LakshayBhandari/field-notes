# Codex Callout Retone — Design Spec

**Date:** 2026-05-19
**Status:** Approved by user ("approced" — user waived the spec-review gate; proceed to plan)
**Artifact:** the multi-page site `/home/lakshay/practice/codex/`
**Builds on:** `2026-05-19-codex-multipage-split-design.md`

---

## 1. Purpose

The ⚠️ callout's language ("WHERE YOU SLIPPED", "what I said [wrong]") reads as
self-critical and brings negative feelings. Retone it to neutral, blame-free
"IMPORTANT" language **without changing any layout, color, structure, or the
substance of the content**. Reader-facing wording only.

### Success criteria

- No reader-visible page contains `WHERE YOU SLIPPED`, the old `What's true:`
  framing label, or the legend phrase `something I got wrong while grilled` /
  `what I said`.
- Every chapter that had a ⚠️ callout now shows header `⚠️ IMPORTANT` and the
  inner labels `Common misread:` / `Actually:` / `Why it matters:`.
- `ch-TEMPLATE.html` and the skeleton text in `how-to-add.html` use the new
  wording (so new chapters inherit the neutral tone).
- The "Read me first" legend (ch-rolling.html) describes the new framing.
- The factual substance of every callout (the misread statement, the
  correction, the consequence) is preserved — only framing words change.
- `codex_check.py` passes and now regression-locks the new wording.

### Non-goals (YAGNI)

- No change to the CSS class `.callout.slip`, the `.slip .lbl` rule, or the
  `--slip-*` CSS variables (invisible to readers; keeping them avoids churn
  across CSS/JS/template/validator and preserves the verbatim-CSS guarantee).
- No change to the 🔄 "Rolling-session caveat" callout (no name collision now).
- No layout/color/structure change; no new content; no re-migration.

---

## 2. Transformation rules

Applied to every `<div class="callout slip">` block on the 5 chapter pages,
plus `ch-TEMPLATE.html` and the escaped skeleton inside `how-to-add.html`:

1. **Header:** `<div class="lbl">⚠️ WHERE YOU SLIPPED</div>` →
   `<div class="lbl">⚠️ IMPORTANT</div>`.
2. **`.said` line:** prefix its content with `<strong>Common misread:</strong> `.
   The existing text stays, EXCEPT the two callouts whose `.said` opens with a
   "Skipped…" lead-in are restated as a concrete neutral wrong belief that the
   existing "Actually:" line already rebuts (so the three-line structure stays
   coherent — a topic phrase is not a "misread"):
   - ch-jwt: `Skipped the scary part: what happens if JWT_ACCESS_SECRET leaks.`
     → `"A leaked JWT_ACCESS_SECRET isn't that bad — an attacker still needs a
     password or DB access."`
   - ch-bcrypt: `Skipped: why a slow hash beats a fast one (SHA-256).`
     → `"Any hash works for passwords — SHA-256 is fine."`
   (Exact before/after HTML strings are enumerated in the implementation plan.)
3. **Correction label:** `<strong>What's true:</strong>` →
   `<strong>Actually:</strong>` (within slip callouts).
4. **Consequence label:** `<strong>Why it matters:</strong>` — unchanged.
5. **Legend** (ch-rolling.html "How to read this book" list): the line
   `<span style="color:var(--accent);font-weight:700">⚠️ Where you slipped</span>
   = something I got wrong while grilled, in the form <em>what I said →
   what's true → why it matters</em>.` becomes
   `<span style="color:var(--accent);font-weight:700">⚠️ Important</span>
   = a point that's easy to get wrong, as <em>common misread → actually →
   why it matters</em>.`

The `<p class="said">` element/class is kept (only its inner text gets the
`<strong>Common misread:</strong>` prefix and, for the two cases, the
"Skipped" lead-in trimmed). Caveat callouts (`.callout.caveat`,
`🔄 ROLLING-SESSION CAVEAT`) are untouched.

## 3. Validator additions

`codex_check.py` gains, run over the reader pages (the 5 chapters + how-to-add
+ ch-TEMPLATE.html):

- **Forbidden (must NOT appear anywhere in any codex/*.html):**
  `WHERE YOU SLIPPED`, `What's true:`, `something I got wrong while grilled`,
  `what I said`.
- **Required:** each of the 5 chapter pages that had a ⚠️ callout, plus
  `ch-TEMPLATE.html`, contains `⚠️ IMPORTANT` and `Actually:`; at least one
  contains `Common misread:`; ch-rolling.html contains the new legend phrase
  `common misread → actually → why it matters`.

These are added to the existing validator without weakening prior checks; the
full suite must still print `PASS: codex site OK (8 pages)`.

## 4. Risks / decisions

- **Verbatim guarantee:** §1 of the multipage spec promised verbatim content
  migration. This change deliberately and narrowly overrides that for the
  callout *framing words only* (header + the three inline labels + the two
  "Skipped" lead-ins + the legend sentence) — at the author's explicit request.
  All factual substance is preserved; the plan enumerates exact strings so the
  edit is deterministic and reviewable.
- **"Skipped" cases:** only two callouts; handled by explicit per-file
  before/after strings in the plan (no heuristic rewriting).
- `practice/` is NOT a git repo — no commits; save + validator checkpoints.
