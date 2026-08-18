# Task: write wiki page 03 for ArxivGoAgentTopologyGeneration

Context is tight on this model — read ONLY the files listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

**Input (read exactly these):**
- `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/source/chunks/03.txt` — extracted paper text: Section 4 Experiments (4.1 Performance Comparison, 4.2 Ablation Study, 4.3 Token Efficiency, 4.4 Robustness Analysis, 4.5 Case Study), Section 5 Related Work, Section 6 Conclusion, Limitations, Ethics Statement
- `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/images/03a-description.md` — vision-model description of Figure 3 (token cost vs. accuracy on MMLU/GSM8K, robustness under attack)
- `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/images/03b-description.md` — vision-model description of Figure 4 (case study: ARG-Designer vs GoAgent on an MMLU item)

**Output:** `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/03-experiments-and-related-work.md`

If this file already exists (a retry), overwrite it completely.

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments, Related Work, and Conclusion

**In one sentence:** <the whole section's overall finding, in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim WITH NUMBERS (accuracy figures, token counts, benchmark names) — not "discusses X">

---

## Experimental setup
## Performance comparison
## Ablation study
## Token efficiency
## Robustness analysis
## Case study
## Related work
## Conclusion, limitations, and ethics

<Full detail under each subsection. Include the results table from the source (Model/MMLU/GSM8K/HumanEval/Avg with exact numbers, e.g. GoAgent 91.50/95.30/94.21/93.67) reproduced as a markdown table. Describe the ablation findings, the token-cost-vs-accuracy trade-off, the robustness-to-prompt-injection results (before/after attack accuracy numbers), and the qualitative case study. Summarize Related Work's positioning against prior multi-agent-system and graph-generation methods. State the paper's conclusion, acknowledged limitations, and ethics statement.>

Embed figures inline at the points where they are discussed:
![Token cost vs. accuracy trade-off on MMLU and GSM8K, and robustness under prompt injection attack](images/fig3-token-efficiency-robustness.png)

<paragraph integrating the Figure 3 description into prose>

![Case study: ARG-Designer (node-centric, incorrect) vs GoAgent (group-centric, correct) on an MMLU item](images/fig4-case-study.png)

<paragraph integrating the Figure 4 description into prose>

**Covers:** Section 4 (Experiments: 4.1-4.5), Section 5 (Related Work), Section 6 (Conclusion), Limitations, Ethics Statement
```

## Rules
- Cover the WHOLE chunk, including the end (Related Work, Conclusion, Limitations, Ethics Statement) — do not stop after the experiments.
- Preserve exact numbers from the source; do not round or invent figures.
- No meta-commentary, no "as an AI", no repeating these instructions in the output.
- Scope: touch ONLY the one output file `wiki/03-experiments-and-related-work.md`. Do not run any fleet commands other than the final `bd close`.
- No git commands — this repo auto-syncs.

## DoD
1. `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/03-experiments-and-related-work.md` written per the contract above.
2. `bd close <own-id> --reason "chunk 03 extracted"`
