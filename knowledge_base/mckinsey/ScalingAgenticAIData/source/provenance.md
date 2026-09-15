# Provenance — Scaling agentic AI with data transformations

- Canonical URL: https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/building-the-foundations-for-agentic-ai-at-scale
- Retrieval date: 2026-09-14
- Route that worked: **Route 4 — reconstruction from multiple search-result extracts**
(each claim sourced; uncertain passages marked `[unverified]` in `source/full.md`).

## Routes tried

1. `curl --http1.1` with browser User-Agent: **FAILED** — operation timed out after 40 s, 0 bytes received.
2. WebFetch (markdown) of the URL: **FAILED** — transport error.
   WebFetch-distilled fetch variant: **FAILED** — `[Errno 60] Operation timed out`.
3. Reader proxy `https://r.jina.ai/<url>`: **FAILED** — target returned 403 Forbidden
   (Akamai/EdgeSuite denial, reference `18.9c0c0317.1789396477.54adc487`).
   McKinsey Brazil mirror (`mckinsey.com.br/...` same slug) via WebFetch: **FAILED** — request timed out.
   Google cache: retired product, not attempted beyond search coverage.
   Headless-browser render (Playwright navigate, extra attempt): **FAILED** —
   `net::ERR_HTTP2_PROTOCOL_ERROR`.
4. Search-extract reconstruction: **SUCCEEDED** — deep web search returned extensive verbatim extracts
   of the McKinsey page (lede, architecture passage, sidebar principles, four steps, layer/model passages,
   quality and governance passages, closing) plus mirrors carrying the byline, date, and dek
   (informedi.org, ramaonhealthcare.com, ralonline.com) and close secondary analyses used only for
   corroboration (haxitag.ai, agenticaiinstitute.org, plastergroup.com, datafi.co, synteratech.com,
   Stanford Tech Review). Saved as `source/full.md` with per-source tags [S1]–[S8].
