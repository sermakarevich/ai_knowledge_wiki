# Provenance — The human side of generative AI: Creating a path to productivity

- Canonical URL: https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-human-side-of-generative-ai-creating-a-path-to-productivity
- Retrieval date: 2026-09-14. Routes tried in spec order:
  1. `curl --http1.1` with Chrome browser User-Agent → FAILED (timeout, 0 bytes after 60s).
  2. WebFetch of canonical URL → FAILED (request timed out).
  3a. Reader proxy `https://r.jina.ai/<url>` → FAILED (target returned 403 Forbidden, Akamai edge denial).
  3b. Alternate fetcher (web_fetch MCP) → FAILED (read timeout).
  3c. Alternate hosted copy of the SAME article as PDF → **SUCCESS**: `https://savanta-confirmit.s3.amazonaws.com/P030200_McKinsey_State+of+AI+2024/The-human-side-of-generative-ai.pdf` (HTTP 200, 1,773,204 bytes). Savanta/Confirmit is the survey platform vendor that fielded the McKinsey Talent Trends Survey cited in the article; the PDF is the 12-page McKinsey Global Publishing-designed article PDF (March 2024, same title, authors, exhibits).
- Extraction: `pdftotext -layout`, ~48KB raw text, cleaned into `source/full.md`. Exhibit charts transcribed as "(described)" data tables; percentages preserved verbatim.
- Verification: title, author byline (De Smet, Durth, Hancock, Mugayar-Baldocchi, Reich), date (March 18, 2024), survey sidebar (n = 12,802; Canada/UK/US; Jul 28–Aug 15, 2023), and key figures (12%/88%, 51%, 30% by 2030) all cross-checked against McKinsey search-result extracts for the canonical URL — consistent. No content invented.
