# Task: Extract wiki page 02 — The AgentGL Method (AgentGL paper)

Context is tight on this model — read ONLY the files listed below, nothing else. Do NOT read this
task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`,
`PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention
reference" — the format contract below is the only convention you need.

## Input

1. Read this file in full: `/Users/sergii/.kb/papers/ArxivAgentGL/source/chunks/02.txt`
   (the Methodology section of "AgentGL: Towards Agentic Graph Learning with LLMs via Reinforcement
   Learning", Sun et al., 2026 — covers the AgentGL framework, graph-native search (GNS) tools,
   search-constrained thinking, and graph-conditioned curriculum learning (GCCL)).

2. Read this figure description (a vision model's description of Figure 1, the method-overview
   diagram): `/Users/sergii/.kb/papers/ArxivAgentGL/wiki/images/01-description.md`

## Output

Write the result to: `/Users/sergii/.kb/papers/ArxivAgentGL/wiki/02-agentgl-method.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The AgentGL Method

**In one sentence:** <the method's whole job, in one sentence>

## Key points

- <complete claim>
- ... (5-8 bullets total, carrying real content: the tool set, the reward formulation, the
  curriculum stages, key equations by name)

---

## Graph-Native Search (GNS) Tools

<describe the tool set: 1-hop neighborhood search, 2-hop neighborhood search, structure salience
search, graph dense search — what each returns and when it is useful>

![Method Overview](images/01-method-overview.png)

<embed the figure right after introducing the overall framework, and describe what it shows
using the figure description provided above>

## Search-Constrained Thinking

<the mechanism that biases the agent toward reflective inference before invoking more graph
queries; include the coverage reward r_COV(τ) formula and its purpose (preventing mode collapse
to a single default action)>

## Graph-Conditioned Curriculum Learning (GCCL)

<the curriculum RL strategy: difficulty staging, multi-faceted rewards, budget constraints;
include any formulas for structural priors (neighbor label consistency, degree, standard normal
quantile) verbatim with their symbols>

**Covers:** Methodology section (source pages 3-6)
```

Requirements:
- Preserve exact equations/symbols from the chunk (e.g. r_COV(τ), η, z, degree d_v, p̂_v) using
  LaTeX-like notation as it appears in the text.
- The image MUST be embedded exactly once at `images/01-method-overview.png` — do not invent any
  other image paths.
- No meta-commentary about being an AI or about this task. Output ONLY the markdown page content.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the close command below.

## Done

After writing the file, close your own bead:

```
bd close <own-bead-id> --reason "chunk 02 extracted"
```
