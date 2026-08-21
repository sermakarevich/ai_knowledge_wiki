# Task: Extract wiki page 03 — Experiments, Results, and Conclusion (AgentGL paper)

Context is tight on this model — read ONLY the files listed below, nothing else. Do NOT read this
task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`,
`PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention
reference" — the format contract below is the only convention you need.

## Input

1. Read this file in full: `/Users/sergii/.kb/papers/ArxivAgentGL/source/chunks/03.txt`
   (the Experiments, Results, Ablations, Conclusion, and Limitations sections of "AgentGL: Towards
   Agentic Graph Learning with LLMs via Reinforcement Learning", Sun et al., 2026).

2. Read this figure description (a vision model's description of Figures 2 and 3, the ablation-study
   charts): `/Users/sergii/.kb/papers/ArxivAgentGL/wiki/images/02-description.md`

## Output

Write the result to: `/Users/sergii/.kb/papers/ArxivAgentGL/wiki/03-experiments-results-and-conclusion.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments, Results, and Conclusion

**In one sentence:** <the whole experimental argument, in one sentence>

## Key points

- <complete claim with concrete numbers, e.g. the 17.5% node classification / 28.4% link
  prediction improvements>
- ... (6-8 bullets total)

---

## Experimental Setup

<datasets/benchmarks used (name the 7 TAG benchmarks and 2 tasks: node classification, link
prediction), baseline categories compared against (GNNs, GraphLLMs, GraphRAG, standard agentic
search), backbones tested>

## Main Results

<the headline numbers: in-domain and zero-shot transfer performance vs baselines, by how much
AgentGL wins, any tables reproduced as markdown tables with exact numbers from the chunk>

## Ablation Studies

![Ablation Figures](images/02-ablation-figures.png)

<describe what the ablations show using the figure description provided above: effect of
r_COV, of CDR/RTT termination terms, of GCCL at each stage>

## Conclusion and Limitations

<the paper's own stated conclusion and any limitations it names>

**Covers:** Experiments, Results, Conclusion, Limitations (source pages 6-9)
```

Requirements:
- Reproduce exact numbers from the chunk (percentages, dataset names, table values) — do not round
  or approximate figures that appear as exact numbers in the text.
- The image MUST be embedded exactly once at `images/02-ablation-figures.png` — do not invent any
  other image paths.
- Cover the WHOLE chunk, including the Conclusion and Limitations at the end — do not stop after
  the results tables.
- No meta-commentary about being an AI or about this task. Output ONLY the markdown page content.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the close command below.

## Done

After writing the file, close your own bead:

```
bd close <own-bead-id> --reason "chunk 03 extracted"
```
