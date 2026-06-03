# Personal Codex Book — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `/home/lakshay/practice/codex.html` — a single self-contained, growing HTML study book that explains topics and resurfaces the exact points the user fumbled/skipped during grill sessions.

**Architecture:** One portable HTML file (inline CSS + minimal inline vanilla JS), no sidebar — a home/landing index at the top with linked chapter cards, collapsible chapters, in-page anchor nav. A small Python validator script (`codex_check.py`) acts as the test harness: each task adds a structural assertion (red), then the HTML to satisfy it (green).

**Tech Stack:** HTML5, inline CSS (polished **dark** theme — deep ink page, soft off-white text, magenta/teal/amber accents tuned for dark), inline vanilla JS, Python 3 stdlib (`html.parser`) for structural verification.

**Environment note:** `practice/` is **not** a git repository. There are no `git commit` steps. Each task ends with a **Checkpoint** (save + run validator + visual confirm) instead.

**Source material (read during implementation, do not invent):**
- `/home/lakshay/practice/login/EXPLAINER.html` — borrow ONLY the typography convention (serif headings, sans body, mono code); do NOT use its light Solarized colors
- `/home/lakshay/practice/login/backend/index.js` — auth backend (paths quoted in tasks)
- `/home/lakshay/practice/login/frontend/src/lib/api.ts` — frontend auth client
- `/home/lakshay/practice/login/frontend/src/App.tsx` — the `useEffect` boot logic
- Spec: `/home/lakshay/practice/docs/superpowers/specs/2026-05-19-personal-codex-book-design.md`

---

## File Structure

- **Create** `/home/lakshay/practice/codex.html` — the book (single file).
- **Create** `/home/lakshay/practice/docs/superpowers/codex_check.py` — structural validator (test harness; grows one check per task).

---

## Task 1: Validator harness + HTML skeleton & design system

**Files:**
- Create: `/home/lakshay/practice/docs/superpowers/codex_check.py`
- Create: `/home/lakshay/practice/codex.html`

- [ ] **Step 1: Write the failing test (validator v1)**

Create `/home/lakshay/practice/docs/superpowers/codex_check.py`:

```python
#!/usr/bin/env python3
"""Structural validator for codex.html. Exit 0 = pass, 1 = fail."""
import sys, pathlib

CODEX = pathlib.Path(__file__).resolve().parents[2] / "codex.html"

def main():
    if not CODEX.exists():
        print(f"FAIL: {CODEX} does not exist"); return 1
    html = CODEX.read_text(encoding="utf-8")
    failures = []

    def need(token, label):
        if token not in html:
            failures.append(f"missing {label}: {token!r}")

    # Task 1: skeleton + design system
    need("<!DOCTYPE html>", "doctype")
    need('lang="en"', "html lang")
    need("--bg: #0e1116", "dark page bg var")
    need("--primary: #f778ba", "primary accent var")
    need('id="home"', "home landing section")
    need('id="book"', "book main container")
    need("function toggleAll(", "expand/collapse-all JS")
    need("</html>", "closing html")

    if failures:
        print("FAIL:"); [print("  -", f) for f in failures]; return 1
    print(f"PASS: codex.html OK ({len(html)} bytes)"); return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run validator to verify it fails**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `FAIL: /home/lakshay/practice/codex.html does not exist` (exit 1)

- [ ] **Step 3: Create the HTML skeleton + design system**

Read `/home/lakshay/practice/login/EXPLAINER.html` lines 1–60 ONLY to confirm
the typography convention (serif headings / sans body / mono code) — do NOT
copy its light colors. Then create `/home/lakshay/practice/codex.html` with this
content (the `:root` block below is the polished **dark** theme; use it exactly
as written):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Codex — Personal Study Book</title>
<style>
:root {
  /* Polished dark theme — deep ink page, soft off-white text */
  --bg: #0e1116; --bg-card: #161b22; --bg-code: #1b2330;
  --text: #c9d1d9; --text-dim: #8b949e; --text-bright: #f0f6fc;
  --border: #232b36; --border-strong: #30363d;
  --primary: #f778ba; --secondary: #2ec9b8; --accent: #f0883e;
  --on-color: #0e1116; --accent-2: var(--secondary); --accent-3: var(--primary);
  --yellow: #e3b341; --red: #ff7b72; --violet: #bc8cff; --blue: #79c0ff; --green: #7ee787;
  --mono: "JetBrains Mono","Fira Code",ui-monospace,Consolas,monospace;
  --serif: "Iowan Old Style","Georgia",serif;
  --sans: "Inter",system-ui,sans-serif;
}
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--text); font-family:var(--sans); line-height:1.7; font-size:15px; -webkit-font-smoothing:antialiased; }
main { max-width: 860px; margin: 0 auto; padding: 56px 32px 140px; }
h1 { font-family:var(--serif); font-size:46px; color:var(--text-bright); margin:0 0 10px; letter-spacing:-0.01em; }
h2 { font-family:var(--serif); font-size:30px; color:var(--text-bright); margin:0; letter-spacing:-0.01em; }
h3 { color:var(--text-bright); margin:28px 0 8px; }
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
strong { color: var(--text-bright); }
code, pre { font-family: var(--mono); }
pre { background:var(--bg-code); border:1px solid var(--border); border-radius:8px; padding:14px 16px; overflow:auto; font-size:13px; color:#d6deeb; }
code { background:var(--bg-code); padding:1px 5px; border-radius:4px; font-size:13px; color:#d6deeb; }

/* Home / landing index */
#home { margin-bottom: 64px; }
.lede { color: var(--text-dim); font-size: 17px; max-width: 640px; }
.chapter-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:14px; margin-top:28px; }
.chapter-card { display:block; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:16px 18px; }
.chapter-card:hover { border-color:var(--primary); text-decoration:none; }
.chapter-card .ct { font-family:var(--serif); font-size:18px; color:var(--text-bright); }
.chapter-card .cd { font-size:13px; color:var(--text-dim); margin-top:4px; }

/* Chapters (collapsible) */
.chapter { border-top:1px solid var(--border); padding:28px 0; }
.chapter > summary { list-style:none; cursor:pointer; display:flex; align-items:baseline; gap:12px; }
.chapter > summary::-webkit-details-marker { display:none; }
.chapter > summary::before { content:"▸"; color:var(--primary); transition:transform .15s; }
.chapter[open] > summary::before { transform:rotate(90deg); }
.chapter-body { padding-top:16px; }
.tohome { display:inline-block; margin-top:24px; font-size:13px; color:var(--text-dim); }

/* Callouts */
.callout { border-radius:10px; padding:14px 18px; margin:18px 0; border:1px solid; border-left-width:3px; }
.slip { background:rgba(240,136,62,0.10); border-color:rgba(240,136,62,0.35); border-left-color:var(--accent); }
.slip .lbl { color:var(--accent); font-weight:700; font-size:12px; letter-spacing:.06em; }
.caveat { background:rgba(46,201,184,0.10); border-color:rgba(46,201,184,0.35); border-left-color:var(--secondary); }
.caveat .lbl { color:var(--secondary); font-weight:700; font-size:12px; letter-spacing:.06em; }
.callout .said { font-style:italic; color:var(--text-dim); }
.controls { position:sticky; top:0; background:rgba(14,17,22,0.92); backdrop-filter:blur(6px); padding:10px 0; border-bottom:1px solid var(--border); margin-bottom:24px; font-size:13px; z-index:5; }
.controls button { background:var(--bg-card); border:1px solid var(--border); border-radius:6px; padding:5px 12px; cursor:pointer; color:var(--text); font-family:var(--sans); }
.controls button:hover { border-color:var(--primary); color:var(--text-bright); }
</style>
</head>
<body>
<main>
  <div class="controls">
    <button onclick="toggleAll(true)">Expand all</button>
    <button onclick="toggleAll(false)">Collapse all</button>
  </div>

  <section id="home">
    <!-- Task 2 fills the landing index here -->
  </section>

  <div id="book">
    <!-- Tasks 3–7 append <details class="chapter"> blocks here -->
  </div>

  <!-- Task 8 appends the "How to add a chapter" section here -->
</main>
<script>
function toggleAll(open) {
  document.querySelectorAll('details.chapter').forEach(function (d) { d.open = open; });
}
// Auto-open the chapter targeted by the URL hash
function openHashTarget() {
  if (!location.hash) return;
  var el = document.querySelector(location.hash);
  while (el) { if (el.tagName === 'DETAILS') el.open = true; el = el.parentElement; }
  if (document.querySelector(location.hash)) document.querySelector(location.hash).scrollIntoView();
}
window.addEventListener('DOMContentLoaded', openHashTarget);
window.addEventListener('hashchange', openHashTarget);
</script>
</body>
</html>
```

- [ ] **Step 4: Run validator to verify it passes**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `PASS: codex.html OK (<n> bytes)` (exit 0)

- [ ] **Step 5: Visual confirm**

Run: `python3 -c "import webbrowser; webbrowser.open('file:///home/lakshay/practice/codex.html')"` (or note: open `file:///home/lakshay/practice/codex.html` manually).
Expected: dark deep-ink page, soft off-white text, sticky "Expand all / Collapse all" buttons, no console errors. (If running headless, skip the open and rely on the validator.)

- [ ] **Step 6: Checkpoint**

No git in `practice/`. Confirm both files saved on disk:
Run: `ls -l /home/lakshay/practice/codex.html /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: both files present, `codex.html` non-trivial size.

---

## Task 2: Home / landing index

**Files:**
- Modify: `/home/lakshay/practice/codex.html` (`<section id="home">`)
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 1: Add the failing assertions**

In `codex_check.py`, after the Task 1 `need(...)` calls, add:

```python
    # Task 2: home landing index
    need("Codex", "book title text")
    need('href="#ch-rolling"', "link to rolling-sessions chapter")
    need('href="#ch-authflow"', "link to auth-flow chapter")
    need('href="#ch-bcrypt"', "link to bcrypt chapter")
    need('href="#ch-jwt"', "link to jwt chapter")
    need('href="#ch-useeffect"', "link to useEffect chapter")
    need('class="chapter-grid"', "chapter grid")
```

- [ ] **Step 2: Run validator to verify it fails**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL listing the 7 new missing tokens.

- [ ] **Step 3: Fill the home section**

Replace the `<section id="home">…</section>` block with:

```html
  <section id="home">
    <h1>Codex</h1>
    <p class="lede">A personal study book. Each chapter explains a topic, then
    resurfaces the exact points I got wrong, was imprecise about, or skipped in
    past grilling sessions — so the corrections don't get buried when sessions
    roll over. Start with <a href="#ch-rolling">Read me first</a>.</p>
    <div class="chapter-grid">
      <a class="chapter-card" href="#ch-rolling"><div class="ct">Read me first: rolling sessions</div><div class="cd">Why this book exists and how to read the ⚠️ and 🔄 callouts.</div></a>
      <a class="chapter-card" href="#ch-authflow"><div class="ct">The auth flow, end to end</div><div class="cd">Signup → login → /me → refresh → logout, frontend ↔ backend.</div></a>
      <a class="chapter-card" href="#ch-bcrypt"><div class="ct">Password hashing &amp; bcrypt cost</div><div class="cd">What <code>bcrypt.hashSync(pw, 10)</code> really does, and the cost factor.</div></a>
      <a class="chapter-card" href="#ch-jwt"><div class="ct">JWT: access, refresh, secrets</div><div class="cd">Two tokens, two secrets, and what a leaked secret lets an attacker do.</div></a>
      <a class="chapter-card" href="#ch-useeffect"><div class="ct">The useEffect auth-load bug</div><div class="cd">Why React effect callbacks must be synchronous.</div></a>
    </div>
  </section>
```

- [ ] **Step 4: Run validator to verify it passes**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: PASS.

- [ ] **Step 5: Checkpoint**

Open `file:///home/lakshay/practice/codex.html`; confirm 5 chapter cards render in a grid and clicking a card jumps (will land on empty anchors until later tasks). Confirm file saved.

---

## Task 3: Chapter pattern + "Read me first: rolling sessions"

**Files:**
- Modify: `/home/lakshay/practice/codex.html` (`<div id="book">`)
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

This task also establishes the **reusable chapter block pattern** every later chapter copies.

- [ ] **Step 1: Add the failing assertions**

In `codex_check.py` add:

```python
    # Task 3: rolling-sessions intro chapter
    need('id="ch-rolling"', "rolling chapter id")
    need('class="chapter"', "chapter component class")
    need("1f808049", "concrete rolled-session example")
    need("Read me first", "intro chapter title")
    need('href="#home"', "back-to-home link")
```

- [ ] **Step 2: Run validator to verify it fails**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: FAIL listing the 5 new tokens.

- [ ] **Step 3: Append the intro chapter inside `<div id="book">`**

This is the canonical chapter pattern (`<details class="chapter" id="ch-...">` → `<summary><h2>` → `.chapter-body` → optional `.callout` → `.tohome`). Append:

```html
    <details class="chapter" id="ch-rolling" open>
      <summary><h2>Read me first: rolling sessions</h2></summary>
      <div class="chapter-body">
        <p>This book exists because of a specific failure mode. When I get
        grilled by Claude, the sharpest moments are corrections — "half-right
        but imprecise", "you skipped the scary part". Those moments are the
        most valuable thing in the whole session.</p>
        <p>But Claude Code sessions <em>roll</em>: a long conversation gets
        compacted or continued in a new chat. The auth grill that produced most
        of this book spans two transcript files —
        <code>1f808049…</code> continued into <code>5ecebe87…</code>. After a
        roll, the early corrections are summarized away or pushed out of
        context. They're effectively lost unless I write them down.</p>
        <h3>How to read this book</h3>
        <ul>
          <li>Normal text = the explanation / refresher.</li>
          <li><span style="color:var(--accent);font-weight:700">⚠️ Where you slipped</span> = something I got wrong while grilled, in the form <em>what I said → what's true → why it matters</em>.</li>
          <li><span style="color:var(--secondary);font-weight:700">🔄 Rolling-session caveat</span> = a point that got buried by a session roll and must not be lost again.</li>
        </ul>
        <a class="tohome" href="#home">↑ Back to index</a>
      </div>
    </details>
```

- [ ] **Step 4: Run validator to verify it passes**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: PASS.

- [ ] **Step 5: Visual confirm + Checkpoint**

Open the file: the intro chapter is expanded by default, collapse arrow works, "↑ Back to index" returns to the grid. Confirm saved.

---

## Task 4: Chapter — The auth flow, end to end

**Files:**
- Modify: `/home/lakshay/practice/codex.html`
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

Content is grounded in `backend/index.js` (`/signup` L55, `/login` L80, `/refresh` L123, `/logout` L152, `/me` L199, `authMiddleware` L36) and `frontend/src/lib/api.ts` (`login` L23, `refreshToken` L38, `authedFetch` L60). Read those ranges before writing prose.

- [ ] **Step 1: Add the failing assertions**

```python
    # Task 4: auth-flow chapter
    need('id="ch-authflow"', "authflow chapter id")
    need("authMiddleware", "auth flow mentions middleware")
    need("httpOnly", "refresh-cookie detail")
    need("401", "401/refresh/retry detail")
```

- [ ] **Step 2: Run validator — expect FAIL** on the 4 new tokens.

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 3: Append the chapter inside `<div id="book">`** (after the rolling chapter)

```html
    <details class="chapter" id="ch-authflow">
      <summary><h2>The auth flow, end to end</h2></summary>
      <div class="chapter-body">
        <p>Two tokens. A short-lived <strong>access token</strong> (15&nbsp;min,
        returned in JSON, kept in a JS variable) and a long-lived
        <strong>refresh token</strong> (7&nbsp;days, set as an
        <code>httpOnly</code> cookie the JS can't read).</p>
        <ol>
          <li><strong>Signup</strong> — <code>POST /signup</code> hashes the password with bcrypt and stores the user (<code>backend/index.js</code> L55).</li>
          <li><strong>Login</strong> — <code>POST /login</code> verifies with <code>bcrypt.compareSync</code>, signs an access token, signs a refresh token, sets it as an <code>httpOnly</code> cookie, and records a server-side session row (L80–L115).</li>
          <li><strong>Protected calls</strong> — <code>authMiddleware</code> reads <code>Authorization: Bearer &lt;token&gt;</code>, runs <code>jwt.verify(token, JWT_ACCESS_SECRET)</code>, attaches <code>request.user</code> (L36).</li>
          <li><strong>Expiry &amp; refresh</strong> — when the access token expires the API returns <strong>401</strong>; <code>authedFetch</code> calls <code>POST /refresh</code> (cookie sent automatically), gets a fresh access token, and retries the original request once (<code>api.ts</code> L60+).</li>
          <li><strong>Logout</strong> — <code>POST /logout</code> deletes the server session and clears the cookie (L152).</li>
        </ol>
        <div class="callout slip">
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">"After login the backend just says 'yes you're valid' and that's it."</p>
          <p><strong>What's true:</strong> a plain login that "forgets" leaves no way for the <em>next</em> request to prove you're logged in — that statelessness is exactly the problem JWT solves here. The access token <em>is</em> the proof carried on every later request.</p>
          <p><strong>Why it matters:</strong> if you don't see why the token has to travel on each call, the whole <code>authMiddleware</code> / <code>Authorization: Bearer</code> step looks like ceremony instead of the load-bearing part.</p>
        </div>
        <div class="callout caveat">
          <div class="lbl">🔄 ROLLING-SESSION CAVEAT</div>
          <p>The refresh-then-retry-once mechanism in <code>authedFetch</code> was explained late in the grill, just before the session rolled — it's the piece most likely to be summarized away. The retry happens <em>once</em>; a second 401 means the refresh token is dead and the user must log in again.</p>
        </div>
        <a class="tohome" href="#home">↑ Back to index</a>
      </div>
    </details>
```

- [ ] **Step 4: Run validator — expect PASS.**

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 5: Checkpoint** — open file, confirm chapter collapses/expands and callouts render with orange (slip) and teal (caveat) styling. Confirm saved.

---

## Task 5: Chapter — Password hashing & bcrypt cost

**Files:**
- Modify: `/home/lakshay/practice/codex.html`
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

Grounded in `backend/index.js` L62 (`bcrypt.hashSync(password, 10)`) and L89 (`bcrypt.compareSync`). Grill fact (verbatim from transcript): cost `n` = `2ⁿ` iterations; cost 10 = 1024, cost 14 = 16384; a slow hash means a few thousand guesses/sec instead of billions/sec.

- [ ] **Step 1: Add the failing assertions**

```python
    # Task 5: bcrypt chapter
    need('id="ch-bcrypt"', "bcrypt chapter id")
    need("2&#8319;", "cost = 2^n notation")  # or the literal you choose; keep consistent
    need("compareSync", "verify path")
```

(If you prefer the literal `2ⁿ` rather than the HTML entity, use `need("2ⁿ", ...)` and write `2ⁿ` in the HTML — just keep the assertion and the HTML identical.)

- [ ] **Step 2: Run validator — expect FAIL.**

- [ ] **Step 3: Append the chapter**

```html
    <details class="chapter" id="ch-bcrypt">
      <summary><h2>Password hashing &amp; the bcrypt cost factor</h2></summary>
      <div class="chapter-body">
        <p><code>bcrypt.hashSync(password, 10)</code> (<code>backend/index.js</code> L62)
        does three things: generates a random <strong>salt</strong>, runs a
        deliberately slow key-derivation <code>2ⁿ</code> times, and returns a
        single string that embeds the cost, the salt, and the hash. Login uses
        <code>bcrypt.compareSync(password, user.password)</code> (L89), which
        re-derives with the embedded salt/cost and compares.</p>
        <p>The <code>10</code> is the <strong>cost factor</strong>: iterations =
        <code>2ⁿ</code>. Cost 10 → 1024 rounds; cost 14 → 16384 rounds — 16×
        slower. Slowness is the feature: it turns an attacker's billions of
        guesses/sec into a few thousand/sec.</p>
        <div class="callout slip">
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">"Higher cost just makes it 'more complex'."</p>
          <p><strong>What's true:</strong> it's not vaguely "more complex" — it's exactly <code>2ⁿ</code> iterations. The math is the point: cost 14 vs 10 is 16384 ÷ 1024 = exactly 16× the work, per guess, for everyone including the attacker.</p>
          <p><strong>Why it matters:</strong> "more complex" hides that you can <em>quantify</em> the attacker's slowdown and tune it deliberately as hardware gets faster.</p>
        </div>
        <div class="callout slip">
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">Skipped: why a <em>slow</em> hash beats a fast one (SHA-256).</p>
          <p><strong>What's true:</strong> a fast hash lets an attacker test billions of stolen-hash guesses/sec; bcrypt's slowness caps that at maybe a few thousand/sec. Same security goal, opposite design choice from a normal hash.</p>
          <p><strong>Why it matters:</strong> it's the reason you don't just <code>sha256(password)</code> and call it done.</p>
        </div>
        <a class="tohome" href="#home">↑ Back to index</a>
      </div>
    </details>
```

- [ ] **Step 4: Run validator — expect PASS.**

- [ ] **Step 5: Checkpoint** — open file, confirm chapter + two slip callouts render. Confirm saved.

---

## Task 6: Chapter — JWT: access, refresh, secrets, and the leakage attack

**Files:**
- Modify: `/home/lakshay/practice/codex.html`
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

Grounded in `backend/index.js` L93 (access `jwt.sign(... JWT_ACCESS_SECRET, {expiresIn:"15m"})`), L94–97 (refresh `JWT_REFRESH_SECRET`, 7d), L42 (`jwt.verify` in middleware), L129 (refresh verify). Grill fact (verbatim): if `JWT_ACCESS_SECRET` leaks, the attacker runs `jwt.sign({ id: <anyone> }, leakedSecret)` and forges a valid token for any user.

- [ ] **Step 1: Add the failing assertions**

```python
    # Task 6: jwt chapter
    need('id="ch-jwt"', "jwt chapter id")
    need("JWT_ACCESS_SECRET", "access secret named")
    need("JWT_REFRESH_SECRET", "refresh secret named")
    need("jwt.sign({ id:", "forgery example")
```

- [ ] **Step 2: Run validator — expect FAIL.**

- [ ] **Step 3: Append the chapter**

```html
    <details class="chapter" id="ch-jwt">
      <summary><h2>JWT: access vs refresh, secrets, and the leakage attack</h2></summary>
      <div class="chapter-body">
        <p>Two independently-signed tokens with <strong>two different
        secrets</strong>. The access token is signed with
        <code>JWT_ACCESS_SECRET</code>, 15&nbsp;min (<code>backend/index.js</code>
        L93). The refresh token is signed with <code>JWT_REFRESH_SECRET</code>,
        7&nbsp;days, and also carries a <code>sessionId</code> checked against a
        server-side session row on <code>/refresh</code> (L94–97, L129).
        <code>authMiddleware</code> trusts a request only if
        <code>jwt.verify(token, JWT_ACCESS_SECRET)</code> succeeds (L42).</p>
        <p>A signature proves "this was signed by whoever holds the secret" —
        nothing more. The server doesn't store access tokens; it re-verifies
        the signature every time.</p>
        <div class="callout slip">
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">Skipped the scary part: what happens if <code>JWT_ACCESS_SECRET</code> leaks.</p>
          <p><strong>What's true:</strong> the secret is the <em>only</em> thing standing between an attacker and a valid token. With it, the attacker runs <code>jwt.sign({ id: &lt;anyone&gt; }, leakedSecret)</code> locally and produces a token <code>authMiddleware</code> will happily accept as <em>any</em> user — no password, no DB access needed.</p>
          <p><strong>Why it matters:</strong> it's why the secret lives in <code>.env</code>, never in code, and why access ≠ refresh secret — a leak of one shouldn't grant the other.</p>
        </div>
        <div class="callout caveat">
          <div class="lbl">🔄 ROLLING-SESSION CAVEAT</div>
          <p>The reason the refresh token <em>also</em> checks a server-side <code>sessionId</code> (so it can be revoked, unlike the stateless access token) was made near a session boundary. Without it you'd "explain" JWT as fully stateless and miss why <code>/logout</code> and <code>/devices</code> can exist at all.</p>
        </div>
        <a class="tohome" href="#home">↑ Back to index</a>
      </div>
    </details>
```

- [ ] **Step 4: Run validator — expect PASS.**

- [ ] **Step 5: Checkpoint** — open, confirm rendering + callouts. Confirm saved.

---

## Task 7: Chapter — The `useEffect` async auth-load bug

**Files:**
- Modify: `/home/lakshay/practice/codex.html`
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

Grounded in `frontend/src/App.tsx` L21–39 (the `load` async fn + the `useEffect(() => { refreshToken().then(...) }, [])` boot). Grill fact (verbatim): React effect callbacks must be synchronous to prevent race conditions; the fix is to define an inner async function and call it (the codebase resolves it by keeping the effect callback sync and calling `.then`).

- [ ] **Step 1: Add the failing assertions**

```python
    # Task 7: useEffect chapter
    need('id="ch-useeffect"', "useEffect chapter id")
    need("useEffect(async", "the buggy form is shown")
    need("synchronous", "explains why it's wrong")
```

- [ ] **Step 2: Run validator — expect FAIL.**

- [ ] **Step 3: Append the chapter**

```html
    <details class="chapter" id="ch-useeffect">
      <summary><h2>The <code>useEffect</code> async auth-load bug</h2></summary>
      <div class="chapter-body">
        <p>The original boot code looked like this:</p>
<pre>useEffect(async () =&gt; {
  if (token &amp;&amp; !user) {
    const res = await fetchMe(token)
    // ...
  }
}, [])</pre>
        <p>An <code>async</code> function always returns a Promise. React expects
        the effect callback to return either nothing or a
        <em>synchronous cleanup function</em> — never a Promise. An
        <code>async</code> effect callback returns a Promise, which React treats
        as garbage, so cleanup never runs and you get races / "logged into the
        wrong account" bugs.</p>
        <p>The fix: keep the effect callback <strong>synchronous</strong> and put
        the awaiting inside. The current <code>App.tsx</code> (L35–39) does the
        equivalent by chaining a promise instead of awaiting:</p>
<pre>useEffect(() =&gt; {
  refreshToken().then(res =&gt; {
    if (res?.token) load(res.token)
  }).finally(() =&gt; setBooting(false))
}, [])</pre>
        <div class="callout slip">
          <div class="lbl">⚠️ WHERE YOU SLIPPED</div>
          <p class="said">"<code>useEffect(async () =&gt; …)</code> is fine, it just runs the async code."</p>
          <p><strong>What's true:</strong> it <em>runs</em>, but the callback now returns a Promise instead of a cleanup function. React can't cancel it, so a stale in-flight <code>fetchMe</code> can resolve after a newer one and overwrite state — the wrong-account race.</p>
          <p><strong>Why it matters:</strong> the rule "effect callbacks are synchronous" isn't style — it's what makes cleanup and cancellation possible.</p>
        </div>
        <a class="tohome" href="#home">↑ Back to index</a>
      </div>
    </details>
```

- [ ] **Step 4: Run validator — expect PASS.**

- [ ] **Step 5: Checkpoint** — open, confirm both code blocks + slip callout render. Confirm saved.

---

## Task 8: "How to add a chapter" template + final verification

**Files:**
- Modify: `/home/lakshay/practice/codex.html`
- Modify: `/home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 1: Add the failing assertions**

```python
    # Task 8: growth template + integrity
    need('id="how-to-add"', "how-to-add section")
    need("&lt;details class=&quot;chapter&quot;", "escaped template skeleton")
    # Integrity: every home-grid link must resolve to a real chapter id
    import re as _re
    ids = set(_re.findall(r'id="(ch-[\w-]+)"', html))
    for href in _re.findall(r'href="#(ch-[\w-]+)"', html):
        if href not in ids:
            failures.append(f"home link #{href} has no matching chapter id")
```

- [ ] **Step 2: Run validator — expect FAIL** (`how-to-add` missing).

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`

- [ ] **Step 3: Append the growth section** after `<div id="book">…</div>` (still inside `<main>`)

```html
  <details class="chapter" id="how-to-add">
    <summary><h2>How to add a chapter</h2></summary>
    <div class="chapter-body">
      <p>To add a concept: (1) add one card to the <code>.chapter-grid</code> in
      <code>#home</code>, (2) paste the skeleton below inside
      <code>&lt;div id="book"&gt;</code>, (3) replace <code>ch-NEW</code> with a
      unique id. Don't touch existing chapters.</p>
<pre>&lt;details class="chapter" id="ch-NEW"&gt;
  &lt;summary&gt;&lt;h2&gt;Chapter title&lt;/h2&gt;&lt;/summary&gt;
  &lt;div class="chapter-body"&gt;
    &lt;p&gt;Explanation…&lt;/p&gt;
    &lt;div class="callout slip"&gt;
      &lt;div class="lbl"&gt;⚠️ WHERE YOU SLIPPED&lt;/div&gt;
      &lt;p class="said"&gt;What I said…&lt;/p&gt;
      &lt;p&gt;&lt;strong&gt;What's true:&lt;/strong&gt; …&lt;/p&gt;
      &lt;p&gt;&lt;strong&gt;Why it matters:&lt;/strong&gt; …&lt;/p&gt;
    &lt;/div&gt;
    &lt;div class="callout caveat"&gt;
      &lt;div class="lbl"&gt;🔄 ROLLING-SESSION CAVEAT&lt;/div&gt;
      &lt;p&gt;Only if a point got buried by a session roll.&lt;/p&gt;
    &lt;/div&gt;
    &lt;a class="tohome" href="#home"&gt;↑ Back to index&lt;/a&gt;
  &lt;/div&gt;
&lt;/details&gt;</pre>
      <p>And the matching home card:</p>
<pre>&lt;a class="chapter-card" href="#ch-NEW"&gt;&lt;div class="ct"&gt;Title&lt;/div&gt;&lt;div class="cd"&gt;One line.&lt;/div&gt;&lt;/a&gt;</pre>
      <a class="tohome" href="#home">↑ Back to index</a>
    </div>
  </details>
```

- [ ] **Step 4: Run validator — expect PASS** (all checks incl. link-integrity).

Run: `python3 /home/lakshay/practice/docs/superpowers/codex_check.py`
Expected: `PASS: codex.html OK (<n> bytes)`

- [ ] **Step 5: Full HTML well-formedness check**

Run:
```bash
python3 -c "import html.parser,sys; \
p=html.parser.HTMLParser(); \
p.feed(open('/home/lakshay/practice/codex.html',encoding='utf-8').read()); \
print('parsed OK')"
```
Expected: `parsed OK` with no exception.

- [ ] **Step 6: Final visual confirmation**

Open `file:///home/lakshay/practice/codex.html`. Verify:
- Home grid shows 5 cards; every card jumps to a real, auto-expanded chapter.
- Expand all / Collapse all work on every chapter including "How to add a chapter".
- ⚠️ callouts are orange, 🔄 callouts are teal, code blocks readable.
- "↑ Back to index" returns to top from every chapter.

- [ ] **Step 7: Checkpoint**

Run: `ls -l /home/lakshay/practice/codex.html` and confirm the file is complete and saved. Report final byte size and that all validator checks pass.

---

## Self-Review (completed during planning)

- **Spec coverage:** §1 purpose → all chapters; §2 single-file/no-deps → Task 1 (inline CSS/JS, system fonts); §3 content model (3 layers + intro) → Tasks 3–7 (`.callout slip`/`caveat`, intro Task 3); §4 no sidebar / home index / in-page nav / collapsible / anchors / **dark theme** → Tasks 1–2 + chapter pattern; §5 growth model → Task 8 template; §6 v1 scope (5 chapters) → Tasks 3–7. All sections covered.
- **Placeholder scan:** every code/HTML step contains full content; chapter prose is constrained by real sourced facts and verbatim grill quotes (no "fill in later").
- **Type/name consistency:** chapter ids (`ch-rolling`, `ch-authflow`, `ch-bcrypt`, `ch-jwt`, `ch-useeffect`, `how-to-add`), classes (`chapter`, `chapter-body`, `callout slip`, `callout caveat`, `tohome`, `chapter-card`, `chapter-grid`), and JS `toggleAll(`/`openHashTarget` are identical across Task 1 definitions, all chapter tasks, the validator, and Task 8's integrity check.
