# Provenance — The AI revolution in software development

**URL:** https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-ai-revolution-in-software-development
**Retrieved:** 2026-09-14
**Route that worked:** 4 of 4 — reconstruction from multiple search-result extracts (see `full.md`, "Sources per claim"). No route yielded the publisher's full text.

## Routes tried

1. `curl --http1.1` with browser User-Agent (direct, then `http://` variant):
   `curl: (56) Recv failure: Operation timed out` / `(28) Operation timed out
   after 40099ms with 0 bytes received`. HTTP 000.
2. WebFetch tools (two fetchers): read timeout / request timed out.
3. Reader proxies: `https://r.jina.ai/<url>` returned HTTP 200 wrapping an
   origin `403 Forbidden` (Akamai "Access Denied", EdgeSuite reference).
   Google cache: discontinued product, not attempted beyond confirming
   unavailability. Wayback Machine: `archive.org/wayback/available` → `429
   Too Many Requests`; CDX query timed out; `web.archive.org/web/2026/<url>`
   → 403. O'Reilly chapter preview (same chapter text): 403.
4. Playwright (real Chromium): `net::ERR_HTTP2_PROTOCOL_ERROR` on the
   McKinsey URL.
5. Web search extracts: **successful** — 6+ independent secondary sources
   quoting the article verbatim (O'Reilly chapter preview, LinkedIn
   republication with full passages, JustEnoughArchitecture, HumanizeAI,
   Growth Acceleration Partners, InsightArea, Appverticals, Seldemirov).
   Convergent verbatim quotes (vignette, thesis paragraph, four levels,
   context line) plus attributed figures. Reconstruction written to
   `full.md` with `[unverified]` flags on joinery and on figures whose
   exact in-article context is unconfirmed.
