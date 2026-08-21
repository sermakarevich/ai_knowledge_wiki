# Extract task: ArxivPathRouter wiki page 03

**Context is tight on this model — read ONLY the input file(s) listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- `/Users/sergii/.kb/papers/ArxivPathRouter/source/chunks/03.txt` — plain text covering: Section 3.3 Distillation for Retrieval-Token, Section 3.4 Training Objective of the paper "PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation" (arXiv 2606.16409). This chunk covers the frozen gold-evidence teacher, selective token-level KL guidance, KL warmup schedule, and the combined training loss.
- No figures in this chunk — do not fabricate any image references.

## Output

Write the full wiki page to: `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/03-distillation-and-training-objective.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Distillation and Training Objective

**In one sentence:** <the core mechanism in one sentence — how a frozen gold-evidence teacher provides selective token-level KL guidance to evidence-poor trajectories, combined with route-conditioned GRPO into the final training loss>

## Key points

- <5-8 bullets with real content: which trajectories get teacher guidance (evidence-poor / low P_i), which tokens receive the KL term (reasoning + search-query, excluding answer tokens), why answer tokens are excluded, the KL warmup mechanism and its purpose, the final combined objective.>

---

## Selective teacher-KL distillation

<full detail: the frozen teacher conditioned on gold evidence, how trajectories are selected for KL guidance (low P_i), the token-level masking that includes reasoning/query tokens but excludes answer and knowledge tokens, and why (to avoid direct response imitation while still correcting search behavior). Reproduce any equations verbatim with their numbers.>

## Training objective

<full detail: the KL warmup schedule (coefficient lambda_T(s) ramping over W steps), the rationale (let the student explore before applying the correction signal), and how this combines with the route-conditioned GRPO advantage from the previous section into the final loss.>

**Covers:** Section 3.3 (Distillation for Retrieval-Token), Section 3.4 (Training Objective)
```

## Rules

- Reproduce equations and variable names exactly as in the source (e.g., lambda_T(s), W, KL coefficient).
- The page must be self-contained.
- No line limit — be thorough.
- Do not invent content not present in the chunk. Do not add an images/figures section since this chunk has no figures.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 03 extracted"`

## Scope

Touch ONLY `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/03-distillation-and-training-objective.md`. Do not run any fleet commands other than `bd close`. No git commands.
