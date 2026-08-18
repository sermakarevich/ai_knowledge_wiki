# Task: write wiki page 02 for ArxivGoAgentTopologyGeneration

Context is tight on this model — read ONLY the two files listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

**Input (read exactly these):**
- `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/source/chunks/02.txt` — extracted paper text: Section 3 Methodology (3.1 Task Encoding and Group Discovery, 3.2 Autoregressive Group-Centric Generation, 3.3 Conditional Information Bottleneck, 3.4 Training and Inference Strategy)
- `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/images/02-description.md` — a vision-model description of Figure 2 (GoAgent system overview: Materials → Design → Optimize → Execution pipeline)

**Output:** `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/02-method.md`

If this file already exists (a retry), overwrite it completely.

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Method: GoAgent

**In one sentence:** <the whole method's core idea, in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (mechanisms, formulas' role, training procedure) — not "discusses X">

---

## Task encoding and group discovery
## Autoregressive group-centric generation
## Conditional information bottleneck (CIB)
## Training and inference strategy

<Full technical detail under each subsection: how the task query and candidate groups are encoded (sentence encoder, task vector z_Q, embedding matrix X), how groups/edges are predicted step-by-step (the group prediction and edge prediction probability terms), what CIB does differently from a standard information bottleneck (task-conditioned prior vs blind compression, the KL term, beta warm-up schedule), and the training objective / inference procedure (Teacher Forcing, avoiding online RL, the loss terms). Preserve notation from the source exactly (z_Q, X, K, M, E, β_g, β_e, D_KL, etc).>

Embed the figure inline at the point where the overall pipeline is introduced:
![GoAgent system overview: task encoding, autoregressive group/edge generation via CIB, and execution](images/fig2-goagent-overview.png)

<Then a paragraph describing what the figure shows, based on the description file — integrate it into the prose, do not just repeat the description verbatim.>

**Covers:** Section 3 (Methodology: 3.1-3.4)
```

## Rules
- Cover the WHOLE chunk, including the end (3.4 Training and Inference Strategy) — do not stop after 3.1 or 3.2.
- No meta-commentary, no "as an AI", no repeating these instructions in the output.
- Scope: touch ONLY the one output file `wiki/02-method.md`. Do not run any fleet commands other than the final `bd close`.
- No git commands — this repo auto-syncs.

## DoD
1. `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/02-method.md` written per the contract above.
2. `bd close <own-id> --reason "chunk 02 extracted"`
