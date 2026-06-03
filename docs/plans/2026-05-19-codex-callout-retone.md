# Codex Callout Retone Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retone the ⚠️ callout across the multi-page Codex site from self-critical "WHERE YOU SLIPPED / what I said" language to neutral "⚠️ IMPORTANT / Common misread → Actually → Why it matters", reader-facing wording only.

**Architecture:** Pure text replacements in the 5 chapter pages + `ch-TEMPLATE.html` + the legend in `ch-rolling.html`. No CSS/JS/class/structure changes. The directory validator gains forbidden-token + required-token assertions that lock the new wording in.

**Tech Stack:** Static HTML edits; Python 3 stdlib `codex_check.py` as the test harness.

**Environment note:** `/home/lakshay/practice/` is **not** a git repo. No `git commit` steps — each task ends with a **Checkpoint** (save + run validator + parse).

**Spec:** `/home/lakshay/practice/docs/superpowers/specs/2026-05-19-codex-callout-retone-design.md`

**Note on `how-to-add.html`:** it was rewritten earlier to the multi-page workflow and contains NO callout skeleton — it needs no edit here (the Task 1 forbidden-token scan confirms it stays clean).

---

## File Structure

- **Modify** `/home/lakshay/practice/codex/ch-authflow.html` (1 callout)
- **Modify** `/home/lakshay/practice/codex/ch-bcrypt.html` (2 callouts)
- **Modify** `/home/lakshay/practice/codex/ch-jwt.html` (1 callout)
- **Modify** `/home/lakshay/practice/codex/ch-useeffect.html` (1 callout)
- **Modify** `/home/lakshay/practice/codex/ch-TEMPLATE.html` (skeleton callout)
- **Modify** `/home/lakshay/practice/codex/ch-rolling.html` (legend line)
- **Modify** `/home/lakshay/practice/docs/superpowers/codex_check.py` (assertions)

No other file changes. All edits are exact `old_string → new_string` replacements.

---

## Task 1: Validator assertions (red)

**Files:**
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 1: Add the assertions**

In `/home/lakshay/practice/docs/superpowers/codex_check.py`, immediately **before** the `if failures:` line (after all existing checks), add exactly:

```python
    # Callout retone — forbidden old wording (any page) + required new wording
    _FORBIDDEN = ["WHERE YOU SLIPPED", "Where you slipped", "What's true:",
                  "something I got wrong while grilled", "what I said"]
    _RETONE_CH = ["ch-authflow.html", "ch-bcrypt.html", "ch-jwt.html",
                  "ch-useeffect.html", "ch-TEMPLATE.html"]
    for name in PAGES:
        p = SITE / name
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        for bad in _FORBIDDEN:
            if bad in h:
                fail(f"{name}: forbidden old callout wording {bad!r}")
    for name in _RETONE_CH:
        p = SITE / name
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        for need_tok in ["⚠️ IMPORTANT", "Actually:", "Common misread:"]:
            if need_tok not in h:
                fail(f"{name}: missing new callout wording {need_tok!r}")
    rp = SITE / "ch-rolling.html"
    if rp.exists() and "common misread → actually → why it matters" not in \
            rp.read_text(encoding="utf-8"):
        fail("ch-rolling.html: legend not retoned")
```

- [ ] **Step 2: Run validator — expect FAIL**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL — lists `forbidden old callout wording 'WHERE YOU SLIPPED'` / `"What's true:"` for ch-authflow/ch-bcrypt/ch-jwt/ch-useeffect/ch-TEMPLATE, `'Where you slipped'` + `'something I got wrong while grilled'` + `'what I said'` for ch-rolling.html, missing `'⚠️ IMPORTANT'`/`'Actually:'`/`'Common misread:'` for the 5 retone pages, and `ch-rolling.html: legend not retoned`. (All pre-existing checks still pass; site otherwise PASS-worthy.)

- [ ] **Step 3: Checkpoint**

The validator now fails ONLY on the new retone assertions (existing structural checks unaffected). Confirm `codex_check.py` saved.

---

## Task 2: Apply the retone edits

**Files:**
- Modify: `ch-rolling.html`, `ch-authflow.html`, `ch-bcrypt.html`, `ch-jwt.html`, `ch-useeffect.html`, `ch-TEMPLATE.html` (all under `/home/lakshay/practice/codex/`)

Each edit below is an exact `old → new` string replacement. Substance is unchanged; only framing words change.

- [ ] **Step 1: ch-rolling.html — legend line**

Replace:
```
          <li><span style="color:var(--accent);font-weight:700">⚠️ Where you slipped</span> = something I got wrong while grilled, in the form <em>what I said → what's true → why it matters</em>.</li>
```
with:
```
          <li><span style="color:var(--accent);font-weight:700">⚠️ Important</span> = a point that's easy to get wrong, as <em>common misread → actually → why it matters</em>.</li>
```

- [ ] **Step 2: ch-authflow.html — the callout**

Replace:
```
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">"After login the backend just says 'yes you're valid' and that's it."</p>
          <p><strong>What's true:</strong> a plain login that "forgets" leaves no way for the <em>next</em> request to prove you're logged in — that statelessness is exactly the problem JWT solves here. The access token <em>is</em> the proof carried on every later request.</p>
```
with:
```
          <div class="lbl">⚠️ IMPORTANT</div>
          <p class="said"><strong>Common misread:</strong> "After login the backend just says 'yes you're valid' and that's it."</p>
          <p><strong>Actually:</strong> a plain login that "forgets" leaves no way for the <em>next</em> request to prove you're logged in — that statelessness is exactly the problem JWT solves here. The access token <em>is</em> the proof carried on every later request.</p>
```

- [ ] **Step 3: ch-bcrypt.html — first callout**

Replace:
```
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">"Higher cost just makes it 'more complex'."</p>
          <p><strong>What's true:</strong> it's not vaguely "more complex" — it's exactly <code>2ⁿ</code> iterations. The math is the point: cost 14 vs 10 is 16384 ÷ 1024 = exactly 16× the work, per guess, for everyone including the attacker.</p>
```
with:
```
          <div class="lbl">⚠️ IMPORTANT</div>
          <p class="said"><strong>Common misread:</strong> "Higher cost just makes it 'more complex'."</p>
          <p><strong>Actually:</strong> it's not vaguely "more complex" — it's exactly <code>2ⁿ</code> iterations. The math is the point: cost 14 vs 10 is 16384 ÷ 1024 = exactly 16× the work, per guess, for everyone including the attacker.</p>
```

- [ ] **Step 4: ch-bcrypt.html — second callout (drop "Skipped:" lead-in)**

Replace:
```
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">Skipped: why a <em>slow</em> hash beats a fast one (SHA-256).</p>
          <p><strong>What's true:</strong> a fast hash lets an attacker test billions of stolen-hash guesses/sec; bcrypt's slowness caps that at maybe a few thousand/sec. Same security goal, opposite design choice from a normal hash.</p>
```
with:
```
          <div class="lbl">⚠️ IMPORTANT</div>
          <p class="said"><strong>Common misread:</strong> "Any hash works for passwords — SHA-256 is fine."</p>
          <p><strong>Actually:</strong> a fast hash lets an attacker test billions of stolen-hash guesses/sec; bcrypt's slowness caps that at maybe a few thousand/sec. Same security goal, opposite design choice from a normal hash.</p>
```

- [ ] **Step 5: ch-jwt.html — the callout (drop "Skipped the scary part:" lead-in)**

Replace:
```
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">Skipped the scary part: what happens if <code>JWT_ACCESS_SECRET</code> leaks.</p>
          <p><strong>What's true:</strong> the secret is the <em>only</em> thing standing between an attacker and a valid token. With it, the attacker runs <code>jwt.sign({ id: &lt;anyone&gt; }, leakedSecret)</code> locally and produces a token <code>authMiddleware</code> will happily accept as <em>any</em> user — no password, no DB access needed.</p>
```
with:
```
          <div class="lbl">⚠️ IMPORTANT</div>
          <p class="said"><strong>Common misread:</strong> "A leaked <code>JWT_ACCESS_SECRET</code> isn't that bad — an attacker still needs a password or DB access."</p>
          <p><strong>Actually:</strong> the secret is the <em>only</em> thing standing between an attacker and a valid token. With it, the attacker runs <code>jwt.sign({ id: &lt;anyone&gt; }, leakedSecret)</code> locally and produces a token <code>authMiddleware</code> will happily accept as <em>any</em> user — no password, no DB access needed.</p>
```

- [ ] **Step 6: ch-useeffect.html — the callout**

Replace:
```
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">"<code>useEffect(async () =&gt; …)</code> is fine, it just runs the async code."</p>
          <p><strong>What's true:</strong> it <em>runs</em>, but the callback now returns a Promise instead of a cleanup function. React can't cancel it, so a stale in-flight <code>fetchMe</code> can resolve after a newer one and overwrite state — the wrong-account race.</p>
```
with:
```
          <div class="lbl">⚠️ IMPORTANT</div>
          <p class="said"><strong>Common misread:</strong> "<code>useEffect(async () =&gt; …)</code> is fine, it just runs the async code."</p>
          <p><strong>Actually:</strong> it <em>runs</em>, but the callback now returns a Promise instead of a cleanup function. React can't cancel it, so a stale in-flight <code>fetchMe</code> can resolve after a newer one and overwrite state — the wrong-account race.</p>
```

- [ ] **Step 7: ch-TEMPLATE.html — skeleton callout**

Replace:
```
      <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
      <p class="said">What I said…</p>
      <p><strong>What's true:</strong> …</p>
```
with:
```
      <div class="lbl">⚠️ IMPORTANT</div>
      <p class="said"><strong>Common misread:</strong> …</p>
      <p><strong>Actually:</strong> …</p>
```

- [ ] **Step 8: Run validator — expect PASS**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `PASS: codex site OK (8 pages)` (exit 0) — all forbidden tokens gone, all required new tokens present, and every pre-existing structural/content check still passes.

- [ ] **Step 9: Checkpoint**

Run: `python3 -c "import html.parser,glob; [html.parser.HTMLParser().feed(open(f,encoding='utf-8').read()) for f in glob.glob('/home/lakshay/practice/codex/*.html')]; print('all parse')"`
Expected: `all parse`. Confirm the 6 edited files saved.

---

## Task 3: Final verification

**Files:** none modified (verification only)

- [ ] **Step 1: Full validator pass**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `PASS: codex site OK (8 pages)` exit 0.

- [ ] **Step 2: Zero old wording anywhere**

Run:
```bash
cd /home/lakshay/practice/codex
grep -RE 'WHERE YOU SLIPPED|Where you slipped|What.s true:|something I got wrong while grilled|what I said' *.html && echo "FOUND old wording (BAD)" || echo "clean: no old callout wording"
```
Expected: `clean: no old callout wording`.

- [ ] **Step 3: New wording present where expected**

Run:
```bash
cd /home/lakshay/practice/codex
grep -c '⚠️ IMPORTANT' ch-authflow.html ch-bcrypt.html ch-jwt.html ch-useeffect.html ch-TEMPLATE.html
grep -q 'common misread → actually → why it matters' ch-rolling.html && echo "legend retoned"
```
Expected: counts ≥ 1 each (ch-bcrypt = 2); `legend retoned`.

- [ ] **Step 4: Substance preserved (no content loss)**

Run:
```bash
cd /home/lakshay/practice/codex
for s in 'statelessness is exactly the problem JWT solves' 'exactly 16× the work' 'bcrypt'"'"'s slowness caps that' 'jwt.sign({ id: &lt;anyone&gt; }, leakedSecret)' 'the wrong-account race'; do
  grep -qF "$s" *.html && echo "OK: $s" || echo "MISSING: $s"
done
```
Expected: every line `OK:` (the factual substance of each callout survived the retone).

- [ ] **Step 5: Parse + Checkpoint**

Run: `python3 -c "import html.parser,glob; [html.parser.HTMLParser().feed(open(f,encoding='utf-8').read()) for f in glob.glob('/home/lakshay/practice/codex/*.html')]; print('all parse')"`
Expected: `all parse`. Report final state: validator PASS, zero old wording, substance intact.

---

## Self-Review (completed during planning)

- **Spec coverage:** §1 success (no old wording / new header+labels / template+legend / substance preserved / validator gated) → Task 1 (assertions) + Task 2 (edits) + Task 3 (proofs); §2 transformation rules (header, .said prefix incl. the two "Skipped" trims, What's true:→Actually:, Why it matters: unchanged, legend) → Task 2 Steps 1–7 (exact strings); §3 validator additions (forbidden + required) → Task 1; §4 risks (verbatim override is narrow + enumerated; "Skipped" handled by explicit strings; not git) → Task 2 Steps 4–5 explicit, no-git checkpoints. `how-to-add.html` no-op noted (no callout skeleton post-rewrite). Full coverage.
- **Placeholder scan:** every edit is a literal exact old→new block; the only `…` are inside `ch-TEMPLATE.html`'s skeleton (intentional author fill-ins) and the validator command strings. No plan placeholders.
- **Name/type consistency:** `⚠️ IMPORTANT`, `Common misread:`, `Actually:`, `Why it matters:` (unchanged), the forbidden list, `_RETONE_CH`, and the legend phrase `common misread → actually → why it matters` are spelled identically across the validator assertions (Task 1), every replacement (Task 2), and the verification greps (Task 3). `.said`/`.callout.slip` classes deliberately unchanged (spec §1 non-goal).
