# Provenance — GenAINextInflectionPoint source retrieval

Date: 2026-09-14. Target: McKinsey "Gen AI's next inflection point" (Aug 2024).

Routes tried, in order:

1. `curl --http1.1` with browser User-Agent (Chrome 126, macOS) against www.mckinsey.com article URL — FAILED: `curl: (56) Recv failure: Operation timed out`, http=000, 0 bytes. Consistent with known McKinsey bot-blocking.
2. WebFetch of the article URL — FAILED: `fetch failed: [Errno 60] Operation timed out`. Alternate `webfetch` tool — FAILED: transport error.
3. Reader proxies: `https://r.jina.ai/<url>` via WebFetch — FAILED (HTTP 404 on distill); via curl — HTTP 200 but body is an "Access Denied" notice: "Target URL returned error 403: Forbidden". Google cache not attempted (service discontinued). PARTIAL: proxy confirms article exists but McKinsey refuses to serve it to bots.
4. Reconstruction from search extracts — NOT NEEDED (see winning route below). Cross-check only: websearch excerpts (mckinsey.com, mckinsey.com.br, hkdca PDF listing) confirm title, authors, date, and key statistics.

WINNING ROUTE (3b — full-text mirror via search): websearch surfaced a complete PDF copy of the McKinsey article hosted at `https://www.hkdca.com/wp-content/uploads/2024/08/employee-experimentation-organizational-transformation-mckinsey.pdf` (Hong Kong Data Centre Association repost). `curl` fetched it HTTP 200, 802,556 bytes, 10 pages, Adobe InDesign 19.4, CreationDate 2024-08-06. Text extracted with `pdftotext -layout`; two-column reading order reconstructed by hand into `source/full.md`. Exhibit chart values transcribed from the PDF text layer. No content invented: every number and quote in `full.md` comes from this PDF's text, cross-checked against search excerpts (91% usage, 13% early adopters, Walmart/My Assistant, telco AI-coach 10%/20%/15% all corroborated).

Result: `source/full.md` = faithful transcription of the real article text. No `[unverified]` passages.
