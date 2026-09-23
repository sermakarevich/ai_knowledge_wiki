# get_local: Gen AI's next inflection point: from employee experimentation to organizational transformation

Article-track `summary/get_local` for a single McKinsey article.
Entry: `/Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/` (absolute paths everywhere below).

## Source

- URL: https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/gen-ais-next-inflection-point-from-employee-experimentation-to-organizational-transformation
- Title: Gen AI's next inflection point: from employee experimentation to organizational transformation

## Step 1 — Retrieve (do NOT invent content)

McKinsey blocks plain bots (curl timeouts, 403 on reader proxies observed 2026-09-14).
Try in order, stop at the first that yields the real article text:
1. `curl --http1.1` with a browser User-Agent.
2. WebFetch of the URL.
3. Reader proxies (`https://r.jina.ai/<url>`, Google cache).
4. Reconstruction from multiple search-result extracts (only if each claim is sourced; mark uncertain passages `[unverified]`).
Save raw text to `/Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/source/full.md` plus provenance (which route worked) in
`/Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/source/provenance.md`.
If NOTHING yields the text: write `/Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/source/fetch_blocked.md` listing every route
tried with its error, skip to DoD clause (b), and STOP. Never fabricate article content.

## Step 2 — Chunk

Split `source/full.md` into ~45k-char chunks at section boundaries:
`/Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/source/chunks/01.txt`, `02.txt`, ... plus `chunks.json` manifest.

## Step 3 — Wiki (4-7 pages, classic contract)

One page per article section: `/Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/wiki/NN-<kebab-topic>.md`, each with:
backlink line, `**In one sentence:**`, `## Key points` (5-8 bullets, each a complete claim
with numbers/mechanisms/conclusions, never "discusses X"), `---`, then hierarchical `##`
detail subsections with exact numbers and verbatim quotes where they matter, `**Covers:**` footer.

## Step 4 — Derived files (from the wiki, never the raw source)

- `digest.md`: copy each page's headline + key points VERBATIM (no paraphrase), then close
  with `## The argument in five moves` (5-7 numbered one-clause steps).
- `explainer.md`: plain-language layer (what it is / why it matters / how it works /
  where used / takeaways / jargon decoder) for a smart non-expert.
- `questions.md`: retrieval practice, >=1 question per digest section, answers in collapsed
  `<details>` blocks; ~half core recall with numbers, ~a third "why / what breaks if", rest transfer.
- `critical_thinking.md`: claims vs evidence, genuinely new vs repackaged, weaknesses,
  applicability, what this changes, verdict.
- `connections.md`: links to related KB entries (read
  `/Users/sergii/.ai/knowledge/structured_papers/index.md` and `ls /Users/sergii/.ai/knowledge/research/`;
  path-qualified links only, no invented paths).
- `index.md`: wiki hub with front-matter, reading ladder, page table.
- `summary.md`: EXACTLY this classic structure (match it precisely):

```markdown
# Gen AI's next inflection point: from employee experimentation to organizational transformation

**Article:** [Gen AI's next inflection point: from employee experimentation to organizational transformation](https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/gen-ais-next-inflection-point-from-employee-experimentation-to-organizational-transformation)

## Human Readable TL;DR

A 3-5 sentence explanation using everyday analogies that someone outside AI/tech can understand. No jargon.

---

## TL;DR

A concise technical summary (3-5 sentences) covering the core contribution, method, and key result.

---

## Problem & Motivation

What gap or limitation does this article address? Why does it matter?

---

## Main Original Ideas

Numbered list of the article's novel contributions. Each item: bold concept name followed by a 2-3 sentence explanation.

---

## Key Findings

- Include a results table if the article has quantitative comparisons
- Bullet points for qualitative findings and insights

---

## Suggestions & Future Directions

Numbered list of proposed next steps, limitations acknowledged, and open questions.

---

## Authors & Institutions

Comma-separated list of authors with affiliations.
```

Prose rules (binding): flowing paragraphs, NEVER one sentence per line; abbreviations expanded
on first use only, no inline dictionary parentheticals; NO `**Wiki:**`/`**Digest:**` header lines.

## Tests

- `ls /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/summary.md /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/index.md /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/digest.md /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/explainer.md /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/questions.md /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/critical_thinking.md /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/connections.md` all exist
- `ls /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/wiki/*.md | wc -l` >= 4
- `grep -c '^## ' /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/summary.md` >= 6 (TL;DR x2 + 4 classic sections)
- `grep -c '^\*\*Wiki:' /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/summary.md` == 0
- `wc -l /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/summary.md` < 300

## DoD

(a) Tests green:
1. `git add /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint` (this entry only — shared tree, NEVER `git add -A`, never touch other paths).
2. `git commit -m "papers(GenAINextInflectionPoint): McKinsey get_local — <one-line>"`.
3. Verify: `git show HEAD:knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/summary.md | grep -c '^## '` >= 6.
4. `bd close <your-own-id> --reason "research/GenAINextInflectionPoint McKinsey get_local done"`.
   Close ONLY your own bead. Never exit rc=0 without closing.
(b) Source unfetchable: `git add /Users/sergii/.ai/knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/GenAINextInflectionPoint/source/fetch_blocked.md`, commit
    `papers(GenAINextInflectionPoint): McKinsey source blocked, routes logged`, verify the file landed,
    `bd close <your-own-id> --reason "research/GenAINextInflectionPoint BLOCKED: McKinsey fetch failed on all routes"`.

## Scope & constraints

- cwd: /Users/sergii/.ai. Touch ONLY `knowledge/structured_papers/mckinsey/GenAINextInflectionPoint/`.
- Do not run `fleet serve restart` / `fleet run`. No live-LLM tests.
