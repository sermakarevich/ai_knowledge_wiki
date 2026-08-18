# Task: write wiki page 03 — When to Use Graph Engineering

Context is tight on this model — read ONLY the chunk file listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

**Input (read this exact file, nothing else):**
`/Users/sergii/.kb/papers/YouTubeWhatIsGraphEngineering/source/chunks/03.txt`

This is the closing transcript segment (timestamps `[06:23-08:26]`) from the YouTube video "What Is Graph Engineering?" by KGP Talkie. It argues graph engineering should NOT be used for everything: for a simple task (e.g., summarizing one PDF), decomposing it into a multi-node graph is "overdoing it." The presenter gives approximate cost multipliers versus a plain LLM call baseline: using an agent costs roughly 4x the tokens/cost of the base task, while using a graph of agents (graph engineering) costs roughly 15x. The practical takeaway is a decision framework: choose between a simple LLM call, an agent, harness engineering, loop engineering, or graph engineering based on task complexity, not by default reaching for the most sophisticated technique.

**Output (write exactly this file; if it already exists — a retry — overwrite it completely):**
`/Users/sergii/.kb/papers/YouTubeWhatIsGraphEngineering/wiki/03-when-to-use-graph-engineering.md`

**Write the page using exactly this structure:**

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# When to Use Graph Engineering

**In one sentence:** <one sentence stating that graph engineering is powerful but should be reserved for genuinely complex, multi-part problems, not simple tasks>

## Key points

- <5-8 bullets, each a complete standalone claim — cover: graph engineering can technically be applied to anything but should not be used for everything, the PDF-summarization example of "overdoing it", the ~4x token/cost multiplier for a single agent vs a plain LLM call, the ~15x token/cost multiplier for a graph of agents vs a plain LLM call, and the decision framework of picking the cheapest technique (LLM call / agent / harness engineering / loop engineering / graph engineering) that fits the task's actual complexity>

---

## The overdoing-it problem

<explain the PDF-summarization example: a simple, single-task problem decomposed into a multi-node graph is unnecessary overhead>

## Cost multipliers vs a plain LLM call

<table or bullets: baseline = X tokens for a plain LLM call; a single agent ≈ 4X tokens/cost; a graph of agents (graph engineering) ≈ 15X tokens/cost>

## Decision framework

<the practical rule: match the technique — simple LLM call, agent, harness engineering, loop engineering, or graph engineering — to the actual complexity of the task rather than defaulting to the most sophisticated option; this is framed as a common interview question>

---

**Covers:** 06:23-08:26
```

**Scope:** touch ONLY the one output file listed above. Do not run any fleet commands other than `bd close`.

**DoD:** output file written → `bd close <own-id> --reason "chunk 03 extracted"`. No git commands — `.kb` auto-syncs.
