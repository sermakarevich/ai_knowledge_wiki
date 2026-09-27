> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Design Docs as the Source of Truth

**In one sentence:** The master branch is a DAG of self-contained markdown design docs with machine-discovered dependency edges, regenerated into code by one coding sub-agent per doc in topological order under an orchestrator that logs interpretation struggles to guide human doc refinement.

## Key points

- Main branch contains almost no code: a folder of markdown design docs forming a DAG, where ordering constraints are semantic (e.g. hardware topology and numerics must be generated before collective-cost models, which precede the model catalog).
- DAG edges are machine-discovered, not hand-maintained: read-only agents analyze the docs and infer dependency edges; an orchestrator then walks the DAG in topological order, assigning a dedicated coding sub-agent to implement each self-contained doc.
- The orchestrator keeps a central log of where sub-agents struggled to interpret prose and bugs found in earlier topological waves — this log tells human engineers exactly which docs need prose refinement next version (targeted human iteration).
- Benefit 1, bounded context windows: each generation step is scoped to a single document, limiting each LLM's context and task length and raising per-task correctness odds — a direct attack on context-window myopia.
- Benefit 2/3, dynamic model routing plus cost and speed: foundational docs (e.g. core DSL design) can go to a larger model while downstream docs use smaller cheaper models; a full clean-slate regeneration takes 1.5–3 hours and costs ~100 USD via Claude Code (~20% of a weekly Claude Max budget), making continuous full rebuilds practical.
- Doc style is bottom-up, not top-down: instead of only tests and high-level rules ("a constitution the generator must obey"), docs center on step-by-step worked examples — executable-in-your-head vignettes ("on a 2x2x2 torus with wraparound, the per-node link count is 3, not 6; the all-gather of V bytes therefore costs ...") that act as in-context demonstrations pinning down semantics prose leaves ambiguous.
- Every number-bearing doc ends with a reconciliation anchor: a small preset whose expected outputs are stated exactly and enforced by generated tests.

---

## The DAG and the orchestration process

The repo layout is a folder structure of markdown files composing into a directed acyclic graph. The ordering example given — hardware topology and numerics before collective-cost models before the model catalog — shows edges encode genuine generation dependencies: later code cannot be correct until earlier concepts exist. Crucially, humans do not maintain these edges; distributed read-only agents infer them from the prose, so adding or editing a doc does not require hand-updating a build graph.

The orchestrator's walk assigns one dedicated coding sub-agent per self-contained doc. Factoring the codebase into self-contained documents with one agent each is what yields the three benefits (bounded context, targeted iteration, dynamic routing). The central log is the feedback instrument: it records interpretation struggles and bugs from earlier waves, converting agent failure into a prioritized editing list for humans.

## Cost and iteration speed

Concrete numbers are given: 1.5–3 hours for a full clean-slate regeneration, ~100 USD API cost per rebuild with Claude Code, roughly 20% of a weekly high-tier usage budget. The point of stating this is to establish that regeneration is not a thought experiment — at this price and latency it can be the default development loop rather than an occasional big-bang rewrite.

## An opinionated way of writing design docs

The paper contrasts two philosophies. The conventional AI-age approach is top-down: write the right tests and high-level rules, a constitution the generator must obey. SMART's complementary bottom-up ingredient is worked examples: trace how pseudo-code executes on a given input step by step — intermediate shapes, intermediate values, the exact closed-form cost expression that should result. The justification cites in-context learning literature (Brown et al., 2020; Dong et al., 2022): like a human learner, a generator benefits from a concrete trace that pins down semantics prose alone leaves ambiguous. This directly attacks failure mode 2 (context-window myopia) from Section 1. The reconciliation anchor at the end of every number-bearing doc closes the loop: stated-exactly expected outputs become generated tests.

**Covers:** Section 2 (Design docs as the source of truth), including DAG/orchestrator description, benefits 1–3, cost figures, worked-examples doctrine, reconciliation anchors.
