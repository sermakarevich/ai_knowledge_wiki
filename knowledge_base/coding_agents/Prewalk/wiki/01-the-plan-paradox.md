> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The /plan Paradox

**In one sentence:** Handing a "senior" frontier model the planning step and a "junior" cheap model the execution step — the standard cost-saving pattern behind slash-commands like `/plan` — actually costs *more* than just letting the frontier model do the whole task itself, because the expensive resource in an agent's run is reading tokens, not thinking or editing them, and a plan handoff forces both models to pay full price for the same reads.

## Key points

- On SWE-Bench Pro, `Opus 4.8 + /plan` (Opus plans read-only, Gemini Flash implements) lands at **$3.18/task, 12.7 min, 84.6% pass**. Opus doing the entire task alone, no handoff, costs **$2.78/task, 10.1 min, 84.6% pass** — same pass rate, 14% cheaper, faster.
- The intuitive mental model — "senior architect writes the plan, junior engineer executes it, so save the expensive senior's time" — is borrowed from how *people* are priced. It doesn't transfer to LLM agents.
- In an agent's token spend, "doing the task" (every edit and write call) is only **9%** of tokens across a sampled 1.81B-token, ~2M-tool-call distribution; the remaining ~91% is reading. This split held across harnesses and models the author tested — not a quirk of one scaffold.
- Because reading dominates cost, the real rule is: **any agent, any model, any scaffold — the bill is essentially O(reads)**.
- `/plan` makes the frontier model read the whole codebase once at frontier prices to write the plan, then the cheap executor re-reads the same files at its own (lower, but nonzero) price to rebuild the context the plan document couldn't transmit. The reading step is duplicated, not eliminated.
- Three common justifications for `/plan` are each addressed and rejected:
  - *"I want the deep understanding of the big model."* That understanding lives in 100K+ tokens of grounded context (files read, dead ends eliminated, hypotheses tested). The plan document is only a ~2K-token "postcard" from that context — the executor gets the postcard, not the understanding, and has to reconstruct the rest itself.
  - *"The task is very complicated."* Then a single read-only planning turn isn't the fix either — dispatch sub-agents to explore and do the work; a plan handoff is "a game of telephone."
  - *"I'm cost constrained."* Reading is the cost, and `/plan` makes the frontier model read everything at frontier prices, then makes the cheap model read it again — duplicating the expensive part rather than moving it.
- Headline numbers for the article's proposed alternative (`/prewalk`, see [[02-how-prewalk-works|How Prewalk Works]]): **97% of frontier pass-rate performance, 41% cheaper, 1.9× faster completion, ~3× less likely to cheat** (cheating discussed in [[05-cheating-and-prefill|Cheating and the Prefill Connection]]).

---

## The setup

The article opens with a chart (SWE-Bench Pro, cost vs. pass rate across 7 experimental "arms") built around one counterintuitive finding: the "obvious" cost optimization of splitting an agentic coding task between an expensive planning model and a cheap execution model is not actually a cost optimization at all, on this benchmark. Every dollar figure quoted in the article includes the frontier model's opening turns, so the comparisons are apples-to-apples task-level totals, not just executor-side costs.

## Where the mistake happens

The author locates the error "upstream of the architecture diagram" — it's not a bug in any particular `/plan` implementation, it's a category error in how the cost of an LLM agent is modeled in the first place. Fixing, building, and thinking are treated as if they cost the money; in practice, the meter runs on reading. A model that reads a file pays for every token of that file whether it then makes one edit or none.

## Covers

The article's opening section, through "Now walk through every reason you'd reach for `/plan`, with that in mind" and the three rebutted justifications for `/plan`.
