# Task: write wiki page 04 for ArxivGoAgentTopologyGeneration

Context is tight on this model — read ONLY the two files listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

**Input (read exactly these):**
- `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/source/chunks/04.txt` — extracted paper text: Appendix A (More Related Work), Appendix B (Algorithm and Complexity Analysis, Algorithms 1-2), Appendix C (Dataset Details), Appendix D (Baseline Details), Appendix E (Parameter Sensitivity Analysis), Appendix F (Implementation Details: training config, architecture, LLM prompt templates, group role prompts)
- `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/images/04-description.md` — vision-model description of Figure 5 (parameter sensitivity heatmaps: accuracy and token cost vs. beta_g/beta_e)

**Output:** `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/04-appendix-and-implementation.md`

If this file already exists (a retry), overwrite it completely.

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Algorithms, Complexity, and Implementation Details

**In one sentence:** <what this appendix material adds beyond the main paper, in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (complexity bounds, dataset sizes, baseline descriptions, key hyperparameters, prompt structure) — not "discusses X">

---

## More related work (Information Bottleneck in Graph Learning)
## Algorithm and complexity analysis
## Dataset details
## Baseline details
## Parameter sensitivity analysis
## Implementation details (training, architecture, prompts)

<Full detail under each subsection. For "Algorithm and complexity analysis": describe Algorithm 1 (Training Procedure) and Algorithm 2 (Inference Procedure) as numbered pseudocode steps, and state the time/space complexity results (in terms of the paper's own notation, e.g. T, number of agents/groups). For "Dataset details" and "Baseline details": list what's covered (benchmarks, single-agent methods like Self-Consistency, fixed topologies like Random/LLM-Debate, learning-based methods like Prune/G-Designer/ARG-Designer) with their one-line descriptions from the source. For "Implementation details": training configuration, architecture (hidden dimensions etc.), and describe the LLM prompt templates and group role prompts structurally (do not fabricate exact prompt text if not present verbatim in the chunk — quote it verbatim if it is present).>

Embed the figure inline at the point where parameter sensitivity is discussed:
![Parameter sensitivity heatmaps: accuracy and token cost vs. beta_g and beta_e on MMLU](images/fig5-parameter-sensitivity-heatmap.png)

<paragraph integrating the Figure 5 description into prose — note the trade-off between accuracy stability and token-cost sensitivity to beta_e>

**Covers:** Appendix A-F (More Related Work, Algorithm and Complexity Analysis, Dataset Details, Baseline Details, Parameter Sensitivity Analysis, Implementation Details)
```

## Rules
- Cover the WHOLE chunk, including the end (Appendix F implementation details / prompts) — do not stop after Appendix B.
- No meta-commentary, no "as an AI", no repeating these instructions in the output.
- Scope: touch ONLY the one output file `wiki/04-appendix-and-implementation.md`. Do not run any fleet commands other than the final `bd close`.
- No git commands — this repo auto-syncs.

## DoD
1. `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/04-appendix-and-implementation.md` written per the contract above.
2. `bd close <own-id> --reason "chunk 04 extracted"`
