#!/usr/bin/env python3
"""Directory validator for the multi-page codex site. Exit 0 = pass, 1 = fail."""
import sys, re, pathlib, html.parser

PROJECT = pathlib.Path(__file__).resolve().parent.parent   # /home/lakshay/practice/codex
SITE = PROJECT / "site"

PAGES = ["index.html", "ch-rolling.html", "ch-authflow.html", "ch-bcrypt.html",
         "ch-jwt.html", "ch-useeffect.html", "ch-refresh-tokens.html",
         "ch-oauth.html", "ch-abortcontroller.html", "how-to-add.html",
         "ch-TEMPLATE.html"]
CHAPTERS = ["ch-rolling.html", "ch-authflow.html", "ch-bcrypt.html",
            "ch-jwt.html", "ch-useeffect.html", "ch-refresh-tokens.html",
            "ch-oauth.html", "ch-abortcontroller.html"]  # prev/next chain order

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
    "ch-refresh-tokens.html": ["sha256", "sameSite"],
    "ch-oauth.html":     ["findOrCreateUser", "login-CSRF", "emailVerified"],
    "ch-abortcontroller.html": ["new AbortController()", "controller.signal.aborted"],
    "how-to-add.html":   ["How to add a chapter", "How to add a theme"],
    "index.html":        ["<h1>Codex</h1>"],
}

def main():
    failures = []
    def fail(m): failures.append(m)

    for _d in ("site", "tooling", "docs"):
        if not (PROJECT / _d).is_dir():
            print(f"FAIL: project structure broken — missing codex/{_d}/"); return 1
    if not SITE.is_dir():
        print(f"FAIL: {SITE} is not a directory"); return 1

    # Required files exist
    required = PAGES + ["assets/codex.css", "assets/codex.js", ".nojekyll", "DEPLOY.md"]
    for rel in required:
        if not (SITE / rel).exists():
            fail(f"missing file: codex/site/{rel}")

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

    # Callout retone — forbidden old wording (any page) + required new wording
    _FORBIDDEN = ["WHERE YOU SLIPPED", "Where you slipped", "What's true:",
                  "something I got wrong while grilled", "what I said"]
    _RETONE_CH = ["ch-authflow.html", "ch-bcrypt.html", "ch-jwt.html",
                  "ch-useeffect.html", "ch-refresh-tokens.html",
                  "ch-oauth.html", "ch-abortcontroller.html", "ch-TEMPLATE.html"]
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

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        return 1
    print(f"PASS: codex site OK ({len(PAGES)} pages)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
