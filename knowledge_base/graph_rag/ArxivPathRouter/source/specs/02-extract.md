# Extract task: ArxivPathRouter wiki page 02

**Context is tight on this model — read ONLY the input file(s) listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- `/Users/sergii/.kb/papers/ArxivPathRouter/source/chunks/02.txt` — plain text covering: Section 3.1 Task Formulation, Section 3.2 Path-Aware Routing of the paper "PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation" (arXiv 2606.16409). This chunk contains the paper's core method equations (Eq. 1-3) for trajectory correctness C_i, evidence-path overlap P_i, and the four-way route classification.
- Figure description (read this too): `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/images/02-fig2-overview-description.md` — describes Figure 2, the overall PathRouter method diagram, to embed as `![Figure 2: PathRouter overview](images/02-fig2-overview.png)`.

## Output

Write the full wiki page to: `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/02-pathrouter-method.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# PathRouter Method: Path-Aware Routing

**In one sentence:** <the core mechanism in one sentence — how PathRouter jointly scores answer correctness and evidence-path overlap to classify trajectories and reweight GRPO advantages>

## Key points

- <5-8 bullets with real content: the multi-turn agent-environment formulation, the exact definitions of C_i and P_i, the four route categories and their names, how route weight modulates GRPO advantage. Include the key equations in inline/LaTeX-like notation as they appear in the source.>

---

## Task formulation

<full detail on the multi-turn agent-environment interaction: think/query/answer tags, knowledge graph G, trajectory tau, turns T. Reproduce Eq. numbers if present.>

![Figure 2: PathRouter overview](images/02-fig2-overview.png)

## Path-aware routing

<full detail on trajectory evaluation: exact formulas for C_i (Eq. 1) and P_i (Eq. 2), the evidence-overlap threshold theta_P, the four-category route classification (Eq. 3) with each category's name (Faithful Success, Shortcut Failure, Evidence Retrieved, Joint Failure) and its (C,P) signature, and how the route weight w_route modulates the GRPO advantage (Eq. 4).>

**Covers:** Section 3.1 (Task Formulation), Section 3.2 (Path-Aware Routing)
```

## Rules

- Reproduce the mathematical definitions precisely (use the exact variable names C_i, P_i, theta_C, theta_P, w_route as in the source).
- The page must be self-contained.
- No line limit — be thorough.
- Do not invent content not present in the chunk or figure description.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 02 extracted"`

## Scope

Touch ONLY `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/02-pathrouter-method.md`. Do not run any fleet commands other than `bd close`. No git commands.
