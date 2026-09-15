# Provenance — AINextAct2026 retrieval (2026-09-14)

Canonical URL: https://www.mckinsey.com/uk/our-insights/uk-insights/ais-next-act-mckinsey-ai-leaders-on-the-year-ahead
Working mirror URL: https://www.mckinsey.com/uk/our-insights/uk-blog/ais-next-act-mckinsey-ai-leaders-on-the-year-ahead
(same title and body; confirmed identical excerpts via web search)

## Routes tried, in order

1. `curl --http1.1` with browser User-Agent (Chrome 126 on macOS) against canonical URL → FAILED: operation timed out after 40 s, 0 bytes received (HTTP 000). Retry against uk-blog mirror → FAILED: timed out after 50 s, 0 bytes.
2. WebFetch of canonical URL → FAILED: transport error. WebFetch of uk-blog mirror → FAILED: request timed out.
3. Reader proxy `https://r.jina.ai/<url>`:
   - on canonical uk-insights URL → FAILED (returned only a tracking-pixel stub, no article text).
   - on uk-blog mirror URL → WORKED: returned the full article text (title, dek, intro, all seven leader quotes, closing synthesis, compiler credit). This is the text saved in `source/full.md`.
   - Local-model web_fetch of canonical URL → FAILED: read operation timed out.
4. Web search reconstruction (not needed as primary source, used only as corroboration): search excerpts for both URLs match the retrieved text verbatim (Patnaik, Smaje, Sukharevsky, Kerr quotes identical).

## Result

`source/full.md` = reader-proxy retrieval of the uk-blog mirror, cross-checked against search-result extracts. No content invented. Article date: January 16, 2026.
