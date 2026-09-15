# Provenance — The automation curve in agentic commerce

Source URL: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-automation-curve-in-agentic-commerce
Date retrieved: 2026-09-14
Worker: fleet-s562 (opencode / muse-spark)

## Routes tried (in spec order)

1. **curl --http1.1 with browser User-Agent on article URL: FAILED.**
   `curl: (28) Operation timed out after ~40s with 0 bytes received.` McKinsey (Akamai bot manager) drops plain-HTTP-client connections.
2. **WebFetch of the article URL: FAILED.** `web_fetch`: "fetch failed: The read operation timed out." `webfetch` (markdown): transport error.
3. **Reader proxies: PARTIAL then SUCCESS.**
   - `https://r.jina.ai/<article-url>`: target returned **403 Forbidden** (Akamai `Reference #18.990c0317.1789397869.8ff316a4`).
   - Web search surfaced the official McKinsey media-subdomain PDF of the same article:
     `https://www.mckinsey.com/~/media/mckinsey/business%20functions/quantumblack/our%20insights/the%20automation%20curve%20in%20agentic%20commerce/the-automation-curve-in-agentic-commerce.pdf`
   - Direct `curl` and `webfetch` on the PDF: timed out (same bot wall).
   - **`https://r.jina.ai/<pdf-url>`: SUCCESS.** Returned the full 9-page article text (title, byline, body, footnotes). This is the text saved in `source/full.md`.
4. **Search-extract reconstruction: NOT NEEDED** (route 3 succeeded).

## Fidelity notes

- `source/full.md` is the reader-proxy markdown of the official PDF, lightly reformatted (headings, paragraph flow) with no claims added. Verbatim quotes, numbers ($3–5T by 2030; 23% Subscribe & Save; level names), and footnotes are preserved as returned.
- The exhibit graphic ("optimal delegation" curve) is referenced in text but its visual contents are not recoverable from the proxy; noted where relevant, not invented.
- Page markers ("The automation curve in agentic commerce N") and the B2B sidebar placement follow the proxy output.
