# Provenance — AgenticOrganizationContours retrieval

Article: The agentic organization: Contours of the next paradigm for the AI era (McKinsey, September 26, 2025).
URL: https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-agentic-organization-contours-of-the-next-paradigm-for-the-ai-era

## Route results (tried in order, 2026-09-14)

1. **curl --http1.1 with browser User-Agent — FAILED.** `curl: (56) Recv failure: Operation timed out`, http=000, size=0 after 60s.
2. **WebFetch — FAILED (two fetchers).** `webfetch` tool: "Transport error"; `web_fetch` MCP tool: "fetch failed: The read operation timed out". Regional `.com.br` mirror also timed out.
3. **Reader proxies / mirrors — FAILED for full text.**
   - `https://r.jina.ai/<url>` → 403 Forbidden (Akamai/EdgeSuite denial, ref 18.a643717.1789391610.175dddea).
   - Playwright (Chromium) direct navigation → `net::ERR_HTTP2_PROTOCOL_ERROR`.
   - industry-5.net repost (2025-10-01) loads but is a stub (dek paragraph + outbound link only, no article body).
4. **Reconstruction from search-result extracts — WORKED.** The search provider's index contains extensive verbatim
   highlights of the McKinsey page (both `.com` and `.com.br` variants), corroborated by secondary sources quoting the
   article verbatim (usecompai.com playbook, fluentaone.com, brianheger.com, rayscuration blog, Medium analyses).
   `source/full.md` is therefore a **reconstruction, not a complete verbatim copy**: passages confirmed by primary
   indexed extracts are unmarked; claims resting only on secondary summaries carry `[unverified]`.

No content was fabricated: every number, quote, and example in `full.md` traces to at least one retrieved extract.
