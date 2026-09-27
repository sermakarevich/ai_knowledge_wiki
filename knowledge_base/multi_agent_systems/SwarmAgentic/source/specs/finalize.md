# finalize: SwarmAgentic (judgment — read wiki, not raw source)

Paper: "SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence" (Yao Zhang et al., 2025), https://arxiv.org/abs/2506.15672
Entry: `/Users/sergii/.ai/knowledge/research/SwarmAgentic/`

## Task — write four files + one append
1. `/Users/sergii/.ai/knowledge/research/SwarmAgentic/summary.md` — EXACTLY the structure below (classic form, match precisely):
```
# SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence

**Paper:** [SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence (Yao Zhang et al., 2025)](https://arxiv.org/abs/2506.15672)

## Human Readable TL;DR

A 3-5 sentence explanation using everyday analogies that someone outside AI/tech can understand. No jargon.

---

## TL;DR

A concise technical summary (3-5 sentences) covering the core contribution, method, and key result.

---

## Problem & Motivation

What gap or limitation does this paper address? Why does it matter?

---

## Main Original Ideas

Numbered list of the paper's novel contributions. Each item: bold concept name followed by a 2-3 sentence explanation.

---

## Key Findings

- Include a results table if the paper has quantitative comparisons
- Bullet points for qualitative findings and ablation insights

---

## Suggestions & Future Directions

Numbered list of the authors' proposed next steps, limitations acknowledged, and open questions.

---

## Authors & Institutions

Comma-separated list of authors with affiliations.
```
Derive it from the wiki pages' headlines + key points (spot-check numbers against `source/full.md`). Binding prose rules: flowing paragraphs, NEVER one sentence per line; abbreviations expanded on first use only; NO `**Wiki:**`/`**Digest:**` header lines.
2. `/Users/sergii/.ai/knowledge/research/SwarmAgentic/critical_thinking.md`: Claims vs. evidence / Genuinely new vs. repackaged / Weaknesses and blind spots / Applicability / What this changes / Verdict.
3. `/Users/sergii/.ai/knowledge/research/SwarmAgentic/connections.md`: links to related KB entries — read `/Users/sergii/.ai/knowledge/research_topics/index.md` and `ls /Users/sergii/.ai/knowledge/research/`; path-qualified links only, never invented paths.
4. `/Users/sergii/.ai/knowledge/research/SwarmAgentic/index.md`: wiki hub — front-matter (`type: Paper`), orientation paragraph, reading ladder, wiki page table in reading order, original source link https://arxiv.org/abs/2506.15672.
5. Append ONE evaluation question to `/Users/sergii/.ai/knowledge/research/SwarmAgentic/questions.md` whose answer links to `critical_thinking.md`.

## Tests
- `ls /Users/sergii/.ai/knowledge/research/SwarmAgentic/summary.md /Users/sergii/.ai/knowledge/research/SwarmAgentic/index.md /Users/sergii/.ai/knowledge/research/SwarmAgentic/critical_thinking.md /Users/sergii/.ai/knowledge/research/SwarmAgentic/connections.md` all exist
- `grep -c '^## ' /Users/sergii/.ai/knowledge/research/SwarmAgentic/summary.md` >= 6
- `grep -c '^\*\*Wiki:' /Users/sergii/.ai/knowledge/research/SwarmAgentic/summary.md` == 0
- `wc -l /Users/sergii/.ai/knowledge/research/SwarmAgentic/summary.md` < 300

## DoD (close-out shape c — shared tree)
1. Tests green (exact commands above).
2. `git add` ONLY the files named above (never `git add -A` / `.` / `-a`; never reset/checkout/stash/restore — shared tree).
3. `git commit -m "<msg>"`.
4. Verify: `git show HEAD:<path> | grep -c "<token>"` >= 1.
5. `bd close <your-own-id> --reason "<done>"`. Close ONLY your own bead. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai. Touch ONLY the paths named above.
- Do not run `fleet serve restart` / `fleet run`. No live-LLM tests.
