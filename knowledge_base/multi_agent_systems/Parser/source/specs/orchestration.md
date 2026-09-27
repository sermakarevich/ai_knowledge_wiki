# Papers research — PARSER paper (ai:summary:get, full depth)

## Problem
arXiv 2609.06702 ("PARSER: Read in Parallel, Reason in Depth for Long-Context LLM Agents", Sept 2026) needs a full KB entry: parallel chunk-bound subagents + lead-agent scatter-gather reasoning, RL on the lead agent, multi-hop QA up to 896K tokens. No entry exists yet.

## Fix
This is an `ai:summary:get` order for https://arxiv.org/html/2609.06702. BEFORE ANYTHING ELSE run `ai show summary/get` and read the whole recipe, then follow it exactly (full wiki pipeline — NOT --fast).
- Folder (cwd `/Users/sergii/.ai`, PascalCase, NO date prefix): `knowledge/research/Parser/` — if it already exists when you start, STOP and close with reason "already exists".
- Key claims to capture (verify against the paper, never invent): decoupling reading (frozen subagent bank, one chunk each) from reasoning (lead agent, iterative scatter-gather rounds); learnable behavior concentrated in lead agent optimized with RL (Reinforcement Learning); +5.7 pts avg over strongest sequential-memory baseline (7K-896K ctx), +12.0 at 896K; 9B backbone beats DeepSeek-V4-Pro by 6.3.
- `wiki/targeted.md` answering: (1) scatter-gather round in concrete steps; (2) why freezing subagents helps training; (3) where the 896K-token wins come from vs sequential memory; (4) cost/latency trade-offs of the subagent bank.
- Style: simple language, abbreviations first use. Marketing-free: this is a paper, report claims + evidence + limits in critical_thinking.md.

## Tests
- `ls knowledge/research/Parser/summary.md knowledge/research/Parser/index.md knowledge/research/Parser/wiki/targeted.md` all exist; `wc -l knowledge/research/Parser/summary.md` >= 60; `ls knowledge/research/Parser/wiki/*.md | wc -l` >= 5.
- `grep -ci "scatter" knowledge/research/Parser/summary.md knowledge/research/Parser/wiki/*.md` >= 2.

## DoD
1. tests green.
2. `git add knowledge/research/Parser` then `git commit -m "papers(Parser): parallel-reading agents research"`. NEVER `git add -A`/`.`/`-a`, NEVER reset/checkout/stash/restore — shared tree.
3. verify: `git show HEAD --stat | grep -c Parser` >= 1.
4. `bd close <your-id> --reason "PARSER landed"` — only your own task.

## Scope & constraints
- cwd `/Users/sergii/.ai`. Do NOT run `fleet serve restart` / `fleet run`. Do NOT touch other research/, tutorials/, or specs/. Web reads only. No secrets.
