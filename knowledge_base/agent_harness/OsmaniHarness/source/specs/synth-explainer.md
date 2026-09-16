# React synth explainer (worker)

## Problem
Write `explainer.md` from the digest only — plain-language layer for a smart non-expert.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/papers/OsmaniHarness/digest.md` (headlines + key points). Never the source, never full wiki pages, never fleet artifacts.
2. Write `/Users/sergii/.ai/knowledge/papers/OsmaniHarness/explainer.md` COMPLETELY (overwrite on retry) with exactly: backlink line, `# ReAct: Synergizing Reasoning and Acting in Language Models — In Plain Language`, `## What is this about?` (2-3 paras, analogy-first), `## Why does it matter?`, `## How does it work?` (numbered walkthrough), `## Where can this be used?`, `## Conclusions & takeaways` (honest limits), `## Jargon decoder` (5-12 terms table). ~60-150 lines. No claim beyond the digest. No meta-junk.
3. No git. Touch ONLY explainer.md.

## Tests
- `test -f /Users/sergii/.ai/knowledge/papers/OsmaniHarness/explainer.md && wc -l /Users/sergii/.ai/knowledge/papers/OsmaniHarness/explainer.md` >= 60; `grep -c "|" /Users/sergii/.ai/knowledge/papers/OsmaniHarness/explainer.md` >= 5.

## DoD
Tests green, then `bd close <own-id> --reason "explainer done"` (own task only).

## Scope & constraints
- No fleet commands except `bd close`. No network.
