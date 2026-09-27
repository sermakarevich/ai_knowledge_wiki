> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Main Experimental Results (Overall EX)
**In one sentence:** This chunk is a garbled extraction of Figure 3 and a baseline table reporting Overall EX values of 82.9, 73.2, and 71.8 (with 81.3 and 70.7 also present) across three benchmarks and several backbones under Baseline, Initial, and Evolved (EvoOntology) conditions.
## Key points
- The chunk's headline numbers are Overall EX (%) values of 82.9, 73.2, and 71.8, with additional Overall EX (%) values of 81.3 and 70.7 present in the same extraction.
- Figure 3 is described verbatim as comparing the "Primary metric on the three benchmarks under three conditions: Baseline, Initial, and Evolved (EvoOntology)".
- The three benchmarks named in the chunk are BIRD, DDR-Bench (10-K), and InsightBench.
- The backbones named on the figure axes/legends are GPT-5.5, GPT-5.6-sol, Claude-Sonnet-5, and Claude-Opus-4.8 (with a fragmented "GPT-5" label also present).
- The metrics named in the chunk are Overall EX (%), Traj-Wise (%)/Trajectory-Wise (%), and Insight (%).
- A block labeled "Baseline (ReAct w/o Ontology)" lists paired numbers per backbone: GPT-5.5 (61.5, 63.4), GPT-5.6-sol (63.5, 65.6), Claude-Sonnet-5 (61.9, 63.7), Claude-Opus-4.8 (67.5, 69.6), DeepSeek-V4-Flash (33.1, 36.4), and Qwen3.5-Flash (46.5, 47.9).
- Prior-method rows appear with paired numbers or dashes: DIN-SQL GPT-4 (50.7, 58.8), DAIL-SQL GPT-4 (54.8, 56.1), TA-SQL GPT-4 (56.2, –), MAC-SQL GPT-4 (57.6, 58.8), MCS-SQL GPT-4 (63.4, –), and CHESS GPT-4o (65.0, 62.8).
---
## Figure 3: primary metric under three conditions
Figure caption (verbatim):
> "Figure 3: Primary metric on the three benchmarks under three conditions: Baseline , Initial, and Evolved (EvoOntology)."

Figure context present in the chunk:
- Conditions: Baseline, Initial, Evolved (EvoOntology).
- Benchmarks: BIRD, DDR-Bench (10-K), InsightBench.
- Backbones on axes: GPT-5.5, GPT-5.6-sol, Claude-Sonnet-5, Claude-Opus-4.8 (plus a fragmented "GPT-5" label).
- Headline Overall EX (%) values: 82.9, 73.2, 71.8 (plus 81.3 and 70.7 in the same Overall EX context).
- Metric labels present: Overall EX (%), Traj-Wise (%)/Trajectory-Wise (%), Insight (%).
- Note: the extraction is spatially garbled (overlapping axis/chart labels and scattered values such as 78.2, 68.9, 68.2, 73.0, 72.5, 68.5, 67.5, 66.1), so individual bar-to-value assignments cannot be recovered from this chunk alone.

## Baseline comparison table (as extracted)
Label (verbatim):
> "Baseline (ReAct w/o Ontology)"

| Method | Backbone | Col 1 | Col 2 |
|---|---|---:|---:|
| DIN-SQL | GPT-4 | 50.7 | 58.8 |
| DAIL-SQL | GPT-4 | 54.8 | 56.1 |
| TA-SQL | GPT-4 | 56.2 | – |
| MAC-SQL | GPT-4 | 57.6 | 58.8 |
| MCS-SQL | GPT-4 | 63.4 | – |
| CHESS | GPT-4o | 65.0 | 62.8 |
| Baseline (ReAct w/o Ontology) | GPT-5.5 | 61.5 | 63.4 |
| Baseline (ReAct w/o Ontology) | GPT-5.6-sol | 63.5 | 65.6 |
| Baseline (ReAct w/o Ontology) | Claude-Sonnet-5 | 61.9 | 63.7 |
| Baseline (ReAct w/o Ontology) | Claude-Opus-4.8 | 67.5 | 69.6 |
| Baseline (ReAct w/o Ontology) | DeepSeek-V4-Flash | 33.1 | 36.4 |
| Baseline (ReAct w/o Ontology) | Qwen3.5-Flash | 46.5 | 47.9 |

Note: column headers for the two numeric columns are not preserved in this chunk extraction; values are reproduced in the order shown.

**Covers:** main experimental results (overall EX scores) across benchmarks and backbones.
