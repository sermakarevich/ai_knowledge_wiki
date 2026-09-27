> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Controlled second-provider simulator swap (Table 7)
**In one sentence:** Swapping the user simulator from Sonnet-4.5 to GPT-5.4 leaves the satisfied-but-failed gap large and highly significant and preserves the 25-agent ranking, so neither finding is a Sonnet-simulator artifact.
## Key points
- Controlled swap design: identical 12 variants × 6 strata × task ids (n=216 each) on the retail degradation grid, same Sonnet-4.5 agent, only the user-simulator provider differs.
- "Satisfied" means ≥5/7 and "failed" means verifiable reward = 0; the satisfied-but-failed (false-accept) rate stays far above the 20% null under both simulators.
- The two simulators steer the same agent into different trajectories: mean verifiable reward is GPT-5.4 0.21 vs. Sonnet 0.32, with the harsher simulator surfacing more task failures.
- Because mean reward differs, compare each false-accept rate to the null, not to each other — the reward shift mechanically shifts the absolute false-accept rate.
- Full 25-agent ranking grid re-run under the GPT-5.4 user simulator: 114 tasks per agent, 2,850 transcripts, holding agent, tasks, rubrics, judge, and oracle fixed.
- Agent ordering is preserved across simulators: Spearman ρ=0.93 (Pearson 0.97; base-model cluster-bootstrap 95% CI [0.71, 0.98]) vs. 0.94 under Sonnet-4.5.
- The near-equal top-11 degradation reproduces under GPT-5.4 (top-11 ρ=0.51), so same-family simulator–agent affinity does not account for the ranking result (§4.2).
---
## Controlled swap design (Table 7)
**Covers:** Table 7: Controlled second-provider simulator swap, retail degradation grid

On the retail degradation grid: identical 12 variants × 6 strata × task ids (n=216 each), same Sonnet-4.5 agent, only the user-simulator provider differs. "Satisfied" is ≥5/7; "failed" is verifiable reward = 0.

## False-accept rate vs. the null under both simulators
**Covers:** Table 7 construct-gap claim

The satisfied-but-failed (false-accept) rate stays far above the 20% null under both simulators, so it is not a Sonnet-simulator artifact. The two simulators yield different mean agent reward (GPT-5.4 harsher), so compare each rate to the null, not to each other.

> "track success under an independent simulator), not as a rate comparison: the two simulators steer the same agent into different trajectories and so yield different mean verifiable reward (GPT-5.4 0.21 vs. Sonnet 0.32, the harsher simulator surfacing more task failures), which mechanically shifts the absolute false-accept rate. The defensible claim is therefore that the gap is large and highly significant under both simulator families."

## Full ranking grid under GPT-5.4
**Covers:** 25-agent ranking-grid swap, §4.2

| Fact | Value |
|---|---|
| Simulator | GPT-5.4 user simulator |
| Agents | 25-agent ranking grid |
| Tasks per agent | 114 |
| Total transcripts | 2,850 |
| Held fixed | agent, tasks, rubrics, judge, oracle |
| Ordering vs. Sonnet-4.5 | Spearman ρ=0.93 (Pearson 0.97; base-model cluster-bootstrap 95% CI [0.71, 0.98]), against 0.94 under Sonnet-4.5 |
| Near-equal top-11 | ρ=0.51 |

> "The swap above isolates the construct gap; we also re-ran the entire 25-agent ranking grid with the GPT-5.4 user-simulator (114 tasks per agent, 2,850 transcripts), holding agent, tasks, rubrics, judge, and oracle fixed. The agent ordering is preserved: Spearman ρ=0.93 (Pearson 0.97; base-model cluster-bootstrap 95% CI [0.71, 0.98]), against 0.94 under Sonnet-4.5, and the near-equal degradation reproduces (top-11 ρ=0.51). Same-family simulator–agent affinity therefore does not account for the ranking result (§4.2)."
