# Task: Extract wiki page 04 — Appendix: Datasets and Implementation (AgentGL paper)

Context is tight on this model — read ONLY the chunk file listed below, nothing else. Do NOT read this
task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`,
`PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention
reference" — the format contract below is the only convention you need.

## Input

Read this file in full: `/Users/sergii/.kb/papers/ArxivAgentGL/source/chunks/04.txt`

It contains Appendix sections A.1-A.5 of "AgentGL: Towards Agentic Graph Learning with LLMs via
Reinforcement Learning" (Sun et al., 2026): Dataset Details, More Related Work (GraphRAG vs. AGL),
Implementation Details, Additional Experiments, and Case Study.

## Output

Write the result to: `/Users/sergii/.kb/papers/ArxivAgentGL/wiki/04-appendix-datasets-and-implementation.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Datasets, Implementation, and Case Study

**In one sentence:** <what this appendix material adds beyond the main paper, in one sentence>

## Key points

- <complete claim>
- ... (5-7 bullets total)

---

## Dataset Details

<the 7 TAG benchmarks with their domains and any statistics table from the chunk, reproduced as
a markdown table (nodes, edges, classes)>

## GraphRAG vs. Agentic Graph Learning

<the paper's own framing of how AGL differs conceptually from GraphRAG — graph as primary problem
instance vs. graph as auxiliary retrieval index>

## Implementation Details

<hyperparameters, training framework (OpenRLHF), RL algorithm details, hardware used, and any
other reproducibility details given in the chunk>

## Additional Experiments and Case Study

<any additional ablation/sensitivity results (e.g. sensitivity to K value) and a description of
the qualitative case studies mentioned (node classification and link prediction rollout examples),
without needing the actual case-study figures>

**Covers:** Appendix A.1-A.5: Dataset Details, More Related Work, Implementation Details,
Additional Experiments, Case Study (source pages 12-15)
```

Requirements:
- Reproduce the dataset statistics table exactly as given in the chunk (dataset names, node/edge/
  class counts).
- This chunk has NO images provided — do not fabricate any `![...]` image references.
- No meta-commentary about being an AI or about this task. Output ONLY the markdown page content.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the close command below.

## Done

After writing the file, close your own bead:

```
bd close <own-bead-id> --reason "chunk 04 extracted"
```
