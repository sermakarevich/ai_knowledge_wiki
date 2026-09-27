# Papers research — A-MLE paper (ai:summary:get, full depth)

## Problem
arXiv 2609.08248 ("Agentic ML Exploration (A-MLE) for Ads Ranking", Meta, Sept 2026 — the paper behind DAIR.AI's viral Sept 10 post) needs a full KB entry: autonomous agent running the ML iteration cycle across production ads ranking models. No entry exists yet.

## Fix
This is an `ai:summary:get` order for https://arxiv.org/pdf/2609.08248 (fallback HTML: https://arxiv.org/html/2609.08248; companion reading: https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/ on the REA system). BEFORE ANYTHING ELSE run `ai show summary/get` and read the whole recipe, then follow it exactly (full wiki pipeline — NOT --fast).
- Folder (cwd `/Users/sergii/.ai`, PascalCase, NO date prefix): `knowledge/research/AgenticMLExploration/` — if it already exists when you start, STOP and close with reason "already exists".
- Key claims to capture (verify against the paper, never invent): bottleneck is human ML-iteration throughput, not capacity/compute; five stages (hypothesis generation, exploration strategy, experiment execution, result analysis, shared knowledge substrate) orchestrated by one agent with domain skills over a sandboxed execution layer, human-in-the-loop at stage boundaries; tiered eval (tool availability, autonomous workflow execution, open-ended exploration); cross-LLM study (Claude Sonnet vs Gemini vs GPT on execution reliability and exploration aggressiveness); force multiplier especially for long-tail models.
- `wiki/targeted.md` answering: (1) the five stages as a concrete loop; (2) what the sandboxed execution layer + HITL checkpoints buy in reliability; (3) how A-MLE relates to Meta's REA (hibernate-and-wake, hypothesis engine); (4) failure modes and limits (what still needs senior engineers).
- Style: simple language, abbreviations first use. Claims vs evidence separated in critical_thinking.md.

## Tests
- `ls knowledge/research/AgenticMLExploration/summary.md knowledge/research/AgenticMLExploration/index.md knowledge/research/AgenticMLExploration/wiki/targeted.md` all exist; `wc -l knowledge/research/AgenticMLExploration/summary.md` >= 60; `ls knowledge/research/AgenticMLExploration/wiki/*.md | wc -l` >= 5.
- `grep -ci "hypothesis" knowledge/research/AgenticMLExploration/summary.md knowledge/research/AgenticMLExploration/wiki/*.md` >= 2.

## DoD
1. tests green.
2. `git add knowledge/research/AgenticMLExploration` then `git commit -m "papers(A-MLE): agentic ads-ranking exploration"`. NEVER `git add -A`/`.`/`-a`, NEVER reset/checkout/stash/restore — shared tree.
3. verify: `git show HEAD --stat | grep -c AgenticMLExploration` >= 1.
4. `bd close <your-id> --reason "A-MLE landed"` — only your own task.

## Scope & constraints
- cwd `/Users/sergii/.ai`. Do NOT run `fleet serve restart` / `fleet run`. Do NOT touch other research/, tutorials/, or specs/. Web reads only. No secrets.
