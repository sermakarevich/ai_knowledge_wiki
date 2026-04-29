# How Claude Code's Memory Actually Works — Lessons from the Accidental Source Leak

On March 31, 2026, Anthropic accidentally shipped a 59.8 MB source map file inside their Claude Code npm package (v2.1.88). The file exposed roughly 512,000 lines of TypeScript across ~1,900 files — system prompts, feature flags, the full agentic runtime, and something that immediately caught the AI engineering community's attention: a production-grade memory architecture unlike anything publicly documented before.

This isn't a post about the leak itself or its implications for Anthropic. It's about what engineers can *learn* from it.

---

## Memory as an Index, Not a Store

The foundational principle running through the entire codebase is deceptively simple:

> *Memory = index, not storage.*

`MEMORY.md` — the single file loaded into every session — contains no knowledge. It holds only pointers: IDs, timestamps, topic keys, confidence scores, each entry deliberately capped at ~150 characters. The actual knowledge lives in separate topic files and is fetched on-demand, only when needed.

This one design decision solves the problem that kills most long-running agents: context bloat. The index loads instantly. Heavy data never enters the prompt unless it's explicitly required.

---

## A Six-Layer Hierarchy

What looks like a simple notes file at the surface is backed by a structured, six-layer system:

- **Layer 1 — `MEMORY.md` (pointer index):** loaded every single turn, always. Tiny entries, no raw content.
- **Layer 2 — Topic files (structured knowledge chunks):** fetched on-demand, only when the model actually needs them.
- **Layer 3 — Transcripts (raw session history):** never read back fully into context. Treated as append-only logs, searched by ID when provenance is needed.
- **Layers 4–5 — Snip, Microcompact + additional compression strategies:** summarization and pruning, run inside isolated background fork agents.
- **Layer 6 — `autoDream` output:** merged, deduplicated, contradiction-resolved memory produced by a periodic background rewrite.

The key insight in Layer 3 is easy to overlook: transcripts are *never* fully re-ingested. They exist for audit purposes only. This keeps the context window clean regardless of how long the session has been running.

---

## The Compaction Pipeline: Obsessive Context Hygiene

One of the most impressive pieces of engineering is the five-layer compaction pipeline. When the API returns a `413` (payload too large), Claude Code intercepts it silently, compacts the context on the fly, and retries. The user never sees an error.

The constraints are strict by design:

- Maximum 5 files restored post-compaction
- Maximum 5K tokens per file
- ~50K total token budget

Compaction runs inside isolated fork agents — sub-processes that summarize and prune history without touching the main context. This isolation is what prevents the maintenance process itself from corrupting the agent's working state.

---

## autoDream: The Self-Healing Loop

The feature that elevates Claude Code from a coding assistant to a genuine agent architecture is `autoDream` — a background consolidation process that runs periodically (typically after ~24 hours or during idle time).

What it does:

- Merges duplicate memory entries
- Resolves contradictions
- Converts vague or hedged statements into absolute facts
- Aggressively prunes low-confidence and stale data

The staleness model is unambiguous: *if memory ≠ reality, memory is wrong.* Code-derived facts are never stored permanently if they can be re-derived at query time. A recurring principle throughout the codebase: **if it's derivable, don't persist it.**

The result is a memory system that is continuously *edited*, not just appended — the direct opposite of most agents, which accumulate ever-growing, increasingly noisy context until performance degrades.

---

## What This Means for Anyone Building Agents

The broader architecture reflects a clear design philosophy: give routing and high-level orchestration to the prompt (plain English instructions), and give safety, memory management, and execution hygiene to deterministic code.

The scaffolding — the agentic loop, compaction pipeline, `autoDream` consolidation — is the real moat. Not the model weights.

For engineers building long-running autonomous systems, the leaked architecture is essentially a reference implementation for:

| Principle | What it means in practice |
|---|---|
| Token-efficient hierarchical memory | Index pointers in context, knowledge on disk |
| Self-healing consolidation | Background rewrites that improve quality over time |
| Forked isolation | Maintenance tasks that can't corrupt the main agent state |
| Skeptical retrieval | Memory treated as a hint, never as ground truth |

---

## The Takeaway

Claude Code's memory system behaves like a living, self-editing operating system for context. It treats context as expensive RAM, staleness as a first-class error, and consolidation as a daemon process — not an afterthought.

The longer it runs, the smarter it gets. That's not a model capability. That's an engineering decision.

If you're designing agent memory today, the question isn't whether to use a vector store or a notes file. The question is: *what is your `autoDream`?*
