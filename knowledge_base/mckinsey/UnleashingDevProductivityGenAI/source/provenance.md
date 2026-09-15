# Provenance — Unleashing developer productivity with generative AI

- Article URL: https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/unleashing-developer-productivity-with-generative-ai
- Canonical/mirror URL found during research: https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/unleashing-developer-productivity-with-generative-ai
- Official PDF: https://www.mckinsey.com/~/media/mckinsey/business%20functions/mckinsey%20digital/our%20insights/unleashing%20developer%20productivity%20with%20generative%20ai/unleashing-developer-productivity-with-generative-ai.pdf
- Retrieval date: 2026-09-14. Retriever: fleet worker fleet-ywva.

## Routes tried (in spec order)

1. `curl --http1.1` with browser User-Agent — FAILED (recv failure / operation timeout,
   HTTP 000, 0 bytes; McKinsey edge network drops bot-like TLS clients).
2. WebFetch of the URL — FAILED (transport error / read timeout on both
   opencode webfetch and web_fetch paths, for both the mckinsey-digital and
   tech-and-ai URLs and the .com.br mirror).
3. Reader proxies — FAILED: `https://r.jina.ai/<url>` returned HTTP 403
   ("You don't have permission to access ... on this server", Akamai/EdgeSuite
   reference). Google cache had no usable copy.
4. Reconstruction from multiple search-result extracts — WORKED. Four targeted
   searches against the article URL, its tech-and-ai mirror, the .com.br mirror,
   and the official PDF produced verbatim extracts covering every major section
   (standfirst, headline numbers, About-the-research method box, four key areas,
   complex-task results, developer-experience results, quality findings, junior
   caveat, three oversight areas, four leadership priorities, four risk bullets,
   closing, authors). `source/full.md` is that reconstruction; uncertain wording
   is marked `[unverified]`. The third human-oversight bullet ("Navigating
   tricky…") was truncated in every extract and is flagged accordingly.
