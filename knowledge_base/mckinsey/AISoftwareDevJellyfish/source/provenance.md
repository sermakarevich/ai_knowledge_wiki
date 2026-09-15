# Provenance — AISoftwareDevJellyfish retrieval

**URL:** https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/measuring-ai-in-software-development-interview-with-jellyfish-ceo-andrew-lau
**Date tried:** 2026-09-14
**Winning route:** 4 — reconstruction from verbatim search-index extracts.

## Routes tried

1. `curl --http1.1` with browser User-Agent (Chrome 126 on macOS) — FAILED: `(28) Operation timed out after 60084 ms with 0 bytes received`.
2. WebFetch (markdown) of the URL — FAILED: request timed out. Second fetch engine (`web_fetch`) — FAILED: "fetch failed: The read operation timed out".
3. Reader proxies:
   - `https://r.jina.ai/<url>` — FAILED: target returned 403 Forbidden (Akamai edge deny, `Reference #18.ad643017.1789403393.17ff57f1`).
   - Publisher-authorized mirror `https://jellyfish.co/newsroom/measuring-ai-in-software-development-interview-with-jellyfish-ceo-andrew-lau` — FAILED as a text source: page fetch succeeded but contains only navigation boilerplate, no interview text.
   - `https://api.allorigins.win/raw?url=<encoded>` — FAILED: non-2xx (HTTP 500).
   - Google cache — not attempted: product discontinued; no cache available.
4. Reconstruction from search-result extracts — WORKED. Three web searches against the McKinsey page returned long verbatim extracts (intro, all five Q/A exchanges, adoption statistics with both footnotes, closing line), mutually consistent across searches. Each claim in `full.md` is sourced to these extracts; bridging/ordering guesses are flagged `[unverified]`. Secondary summaries (gend.co) used only for cross-checking.
