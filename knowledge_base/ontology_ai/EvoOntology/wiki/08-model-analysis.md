> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Per-Backbone Analysis and Insight Metrics
**In one sentence:** Per-backbone results show the builder-constructed ontology improves scores and the self-evolution loop adds further gains through monotonically converging accepted rounds, with ablations identifying the gate and attribution steps (and mappings/evidence families) as the largest contributors.
## Key points
- On BIRD, the mean EX score improves by 5.1 percentage points with the initial ontology and by a further 3.7 percentage points after evolution, while another metric "increases by 0.8 points and then gains another 0.2 points through evolution."
- Under Oracle Knowledge on BIRD (Table 4, VES on a 0–100 scale, parentheses = gain over Baseline), EvoOntology reaches: GPT-5.5 68.9 (+7.4) / 71.1 (+7.7), GPT-5.6-sol 70.7 (+7.2) / 73.0 (+7.4), Claude-Sonnet-5 71.8 (+9.9) / 74.1 (+10.4), Claude-Opus-4.8 78.3 (+10.8) / 80.5 (+10.9), DeepSeek-V4-Flash 39.4 (+6.4) / 44.1 (+7.6), Qwen3.5-Flash 49.1 (+2.5) / 55.2 (+7.3).
- Baseline + SL (ReAct + Semantic Layer) rows in the same table include GPT-5.5 55.9 (−5.6) / 67.7 (+4.3), GPT-5.6-sol 63.0 (−0.5) / 68.9 (+3.3), Claude-Sonnet-5 60.8 (−1.1) / 65.8 (+2.1), Claude-Opus-4.8 66.2 (−1.3) / 75.0 (+5.4), DeepSeek-V4-Flash 36.3 (+3.2) / 37.2 (+0.7), and Qwen3.5-Flash 48.0 (+1.5) / 51.9 (+4.0).
- Figure 4 tracks the primary score across accepted evolution rounds (Traj-Wise on DDR-Bench, Insight on InsightBench, EX on BIRD); all four backbones improve monotonically from Initial, with GPT-5.6-sol reaching 93.5 Traj-Wise after five accepted rounds and Claude-Opus-4.8 reaching 92.3 after four.
- Trajectories "flatten by the last two rounds, which is consistent with the failure signatures becoming rarer once the ontology covers the recurrent cross-filing concepts," supporting that Table 1 gains come from "a converging refinement and not a single fortunate patch."
- Evolution-loop ablation (Table 5, DDR-Bench Traj-Wise %, averaged across four backbones): Full loop 89.5; w/o Gate 78.3 (−11.2); w/o Attribution 83.2 (−6.3); w/o Diagnose 84.7 (−4.8); w/o Patch (free-form) 87.8 (−1.7).
- Content-layer object-family ablation (Table 7, DDR-Bench Traj-Wise %, averaged across four backbones): Full EvoOntology 89.5; w/o Mappings 76.1 (−13.4); w/o Evidence 80.8 (−8.7); w/o Constraints 86.0 (−3.5); w/o Relations 87.4 (−2.1), with terms noted as "cannot be masked in isolation and are omitted."
---
## Analyses setup
Unless otherwise stated, all analyses in this section are conducted on DDR-Bench across the four backbones (GPT-5.5, GPT-5.6-sol, Claude-Sonnet-5, Claude-Opus-4.8).

**Covers:** per-backbone analysis and insight metrics (e.g. GPT-5.5 findings).
## BIRD under Oracle Knowledge (Table 4)
Table 4 reports main results on BIRD under Oracle Knowledge with VES on a 0–100 scale, where "Parentheses report the gain over the corresponding Baseline result."

| Variant | Col. A | Col. B |
|---|---|---|
| Baseline + SL (ReAct + Semantic Layer) GPT-5.5 | 55.9 (−5.6) | 67.7 (+4.3) |
| Baseline + SL GPT-5.6-sol | 63.0 (−0.5) | 68.9 (+3.3) |
| Baseline + SL Claude-Sonnet-5 | 60.8 (−1.1) | 65.8 (+2.1) |
| Baseline + SL Claude-Opus-4.8 | 66.2 (−1.3) | 75.0 (+5.4) |
| Baseline + SL DeepSeek-V4-Flash | 36.3 (+3.2) | 37.2 (+0.7) |
| Baseline + SL Qwen3.5-Flash | 48.0 (+1.5) | 51.9 (+4.0) |
| EvoOntology GPT-5.5 | 68.9 (+7.4) | 71.1 (+7.7) |
| EvoOntology GPT-5.6-sol | 70.7 (+7.2) | 73.0 (+7.4) |
| EvoOntology Claude-Sonnet-5 | 71.8 (+9.9) | 74.1 (+10.4) |
| EvoOntology Claude-Opus-4.8 | 78.3 (+10.8) | 80.5 (+10.9) |
| EvoOntology DeepSeek-V4-Flash | 39.4 (+6.4) | 44.1 (+7.6) |
| EvoOntology Qwen3.5-Flash | 49.1 (+2.5) | 55.2 (+7.3) |

The chunk states the builder-constructed ontology "provides an effective starting point, whereas the self-evolution loop is essential for realizing the full performance gain and consistently improves the ontology beyond its initial state."

**Covers:** per-backbone analysis and insight metrics (e.g. GPT-5.5 findings).
## Effect of Iterative Evolution (Figure 4)
Figure 4 plots "Primary metric across accepted evolution rounds on the three benchmarks: Traj-Wise on DDR-Bench, Insight on InsightBench, and EX on BIRD," where "Each round corresponds to one candidate that passed the paired gate, and the parent line traces the score of the ontology version that would remain if no more rounds were run."

- "All four backbones improve monotonically from Initial through the accepted rounds, with GPT-5.6-sol reaching 93.5 Traj-Wise after five accepted rounds and Claude-Opus-4.8 reaching 92.3 after four."
- "The results show that the gains reported in Table 1 are the outcome of a converging refinement and not a single fortunate patch, which validates the design of the four-step evolution loop."

**Covers:** per-backbone analysis and insight metrics (e.g. GPT-5.5 findings).
## Ablation Study on Evolution Loop (Table 5)
Disabled variants are defined in the chunk as: "w/o Diagnose skips the failure-trace clustering step and asks the evolution agent to propose an edit from a random sample of recent traces; w/o Attribution drops the level tag and lets the agent commit an edit at any level without stating a hypothesis; w/o Patch stage replaces the typed, hypothesis-conditioned edit with a free-form ontology rewrite that the evolution agent produces directly from the diagnosis; w/o Gate accepts every candidate patch."

| Variant | Traj-Wise (%, ↑) | ∆ |
|---|---|---|
| Full loop | 89.5 | – |
| w/o Gate | 78.3 | −11.2 |
| w/o Attribution | 83.2 | −6.3 |
| w/o Diagnose | 84.7 | −4.8 |
| w/o Patch (free-form) | 87.8 | −1.7 |

Quoted mechanisms: "removing the gate causes the largest drop (−11.2 Traj-Wise), because unfiltered candidates admit regressions that the next round cannot always undo"; "Removing the attribution step drops by −6.3, because without a level tag the loop tends to make content edits when the failure is a manifest problem, and vice versa"; "Removing the diagnose step drops by −4.8, and replacing the typed patch with a free-form rewrite drops by −1.7"; "the gate and attribution are the two load-bearing pieces, which validates the design of an evolution loop that is more selective than iterative."

**Covers:** per-backbone analysis and insight metrics (e.g. GPT-5.5 findings).
## Content-layer object families (Table 7) and level restriction
| Variant | Traj-Wise (%, ↑) | ∆ |
|---|---|---|
| Full EvoOntology | 89.5 | – |
| w/o Mappings | 76.1 | −13.4 |
| w/o Evidence | 80.8 | −8.7 |
| w/o Constraints | 86.0 | −3.5 |
| w/o Relations | 87.4 | −2.1 |

The chunk notes "Terms cannot be masked in isolation and are omitted." A further truncated table in the chunk lists Baseline 69.5 (–) and Content-only evolution 78.2 (+8.7), and mentions restricting evolution to the three editable levels (Content / Tool / Schema) to test whether they are jointly required.

**Covers:** per-backbone analysis and insight metrics (e.g. GPT-5.5 findings).
