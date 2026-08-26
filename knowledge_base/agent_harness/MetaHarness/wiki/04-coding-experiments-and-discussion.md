> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Agentic Coding Experiments and Discussion

**In one sentence:** On TerminalBench-2, an automatically searched harness beats hand-engineered baselines (76.4% on Claude Opus 4.6, #2 overall; 37.6% on Claude Haiku 4.5, #1 among that model's agents), and the paper argues the key advantage is not merely code search but selective access to prior diagnostic experience.

## Key points

- TerminalBench-2 consists of 89 challenging tasks requiring long-horizon, fully autonomous execution under complex dependencies and substantial domain knowledge; prior work has shown the agent harness choice has a large effect on performance on this benchmark.
- Search was initialized from two strong open baselines, Terminus 2 and Terminus-KIRA, and both search and final evaluation were run on the same 89-task benchmark (treated as a "discovery problem"), with no separate holdout split.
- Anti-overfit safeguards were a manual inspection plus regex-based audits for task-specific string leakage into evolved harnesses.
- On Claude Opus 4.6, Meta-Harness achieves 76.4% pass rate, beating hand-engineered Terminus-KIRA (74.7%) and Capy (75.3%), ranking #2 among all Opus 4.6 agents — only ForgeCode (81.8%) scores higher.
- The authors could not reproduce ForgeCode's 81.8% result from its publicly available code alone, suggesting the leaderboard score depends on components beyond the published repository.
- On the weaker Claude Haiku 4.5, the gain is larger: Meta-Harness achieves 37.6%, outperforming the next-best reported agent (Goose, 35.5%) by 2.1 points and ranking #1 among all Haiku 4.5 agents.
- Qualitatively, the proposer initially combined structural fixes with prompt-template edits and saw both regress; it then hypothesized the regressions were confounded by the shared prompt intervention, isolated the structural changes, and pivoted to a safer additive modification that became the best candidate in the run.
- The paper concludes the main advantage of Meta-Harness is not search over code per se, but search with selective access to prior diagnostic experience — the proposer can inspect raw code, execution traces, and prior failures to form and test hypotheses — and that once a search space is accessible, stronger general-purpose agents can outperform hand-engineered solutions.

---

## TerminalBench-2 setup

TerminalBench-2 evaluates LLM agents on 89 challenging tasks that require long-horizon, fully autonomous execution under complex dependencies and substantial domain knowledge. It is an actively contested benchmark with multiple teams directly optimizing for it, and prior work has shown that the choice of agent harness has a large effect on performance on it.

Meta-Harness initializes its search from two strong open baselines — Terminus 2 and Terminus-KIRA — and performs both search and final evaluation on the same 89-task benchmark. The authors frame this as a discovery problem: the goal is to discover a harness configuration that improves performance on a hard, publicly contested benchmark. They note this is standard practice — public writeups already describe repeated benchmark-specific harness iteration on TerminalBench itself — and argue that because the benchmark is small and expensive enough, introducing a separate evaluation split would materially weaken the search signal.

To check for overfitting, the authors rely on manual inspection and regex-based audits for task-specific string leakage into the evolved harnesses. They acknowledge the resulting harness is specialized to the TerminalBench-2 regime, but note that autonomous completion of difficult long-horizon tasks from a single instruction is a core capability, and the benchmark contains many tasks that frontier models and heavily engineered harnesses still struggle with.

Baselines compared against (from the official leaderboard): Claude Code, Terminus 2, Mux, Droid, TongAgents, MAYA-V2, Terminus-KIRA, Capy, ForgeCode (Opus 4.6); OpenHands, Claude Code, Terminus 2, Mini-SWE-Agent, Terminus-KIRA, Goose (Haiku 4.5).

## Results

Results are on the full 89-task benchmark, evaluated on two base models (Table 7; results for other harnesses are from the official leaderboard, marked ×; the Meta-Harness row ✓ is the paper's own result).

| Harness | Opus 4.6 Auto Pass (%) | Haiku 4.5 Auto Pass (%) |
|---|---|---|
| OpenHands | — | × 13.9 |
| Claude Code | × 58.0 | × 27.5 |
| Terminus 2 | × 62.9 | × 28.3 |
| Mini-SWE-Agent | — | × 29.8 |
| Mux | × 66.5 | — |
| Droid | × 69.9 | — |
| TongAgents | × 71.9 | — |
| MAYA-V2 | × 72.1 | — |
| Terminus-KIRA | × 74.7 | × 33.7 |
| Capy | × 75.3 | — |
| Goose | — | × 35.5 |
| ForgeCode | × 81.8 | — |
| **Meta-Harness** | **✓ 76.4** | **✓ 37.6** |

**Meta-Harness ranks #2 among all Opus-4.6 agents and #1 among all Haiku-4.5 agents on this competitive task.**

- On **Claude Opus 4.6**: Meta-Harness discovers a harness achieving **76.4% pass rate**, surpassing the hand-engineered Terminus-KIRA (74.7%) and ranking **#2** among all Opus 4.6 agents on the leaderboard. The only higher-scoring Opus 4.6 agent is ForgeCode (81.8%); however, the authors were unable to reproduce its reported result from the publicly available code alone, suggesting its leaderboard score depends on components beyond the published repository.
- On the **weaker Claude Haiku 4.5**: the improvement is larger — Meta-Harness achieves **37.6%**, outperforming the next-best reported agent (Goose, 35.5%) by **2.1 points**.
- The authors consider it encouraging that an automatic search method achieves benefits at this frontier on an actively contested benchmark, as a signal for long-horizon text-optimization loops generally.

## Qualitative behavior of the proposer

The harness search trajectory helps explain why Meta-Harness achieves these gains (a detailed summary is in Appendix A of the paper). In early iterations, the proposer combined plausible structural fixes with prompt-template edits and observed that both candidates regressed. It then explicitly hypothesized that the regressions were confounded by the shared prompt intervention, isolated the structural changes from the prompt rewrite, and ultimately pivoted toward a safer additive modification that became the best candidate in the run. This provides qualitative evidence that **filesystem access enables the proposer to inspect prior experience in enough detail to form causal hypotheses and revise the harness accordingly.**

## Discussion

Beyond outperforming existing harnesses, the paper (Section 5) argues Meta-Harness has several practical advantages:

- **Transfer and generalization.** Discovered harnesses generalize to out-of-distribution classification datasets (Table 5) and to unseen base models in the math setting (Table 6).
- **Efficiency + reusability.** A search run completes in a few hours of wall-clock time, yet produces readable, transferable strategies that can be reused across models, including future, stronger ones.
- **Inspectability of overfitting.** Overfitting in code space is more inspectable: brittle if-chains or hard-coded class mappings are visible on inspection, in a way that weight-space overfitting is not.
- **The core claim.** The main advantage of Meta-Harness is not just search over code, but search with *selective access to prior diagnostic experience*: the proposer is not limited to scalar rewards or fixed summaries — it can inspect raw code, execution traces, and prior failures, then use that information to form and test hypotheses about what to change (illustrated directly by the qualitative search trajectories in Appendix A.2).

The paper's closing remarks frame this within a recurring pattern in machine learning: once a search space becomes accessible, stronger general-purpose agents can outperform hand-engineered solutions. A natural next step is to co-evolve the harness and the model weights, letting the strategy shape what the model learns and vice versa. As limitations, the authors note that although they evaluate on three diverse domains, the experiments demonstrate that harness search can work with one particularly strong coding-agent proposer (Claude Code); a broader study of how the effect varies across proposer agents remains for future work.

**Covers:** Section 4.3 (Evaluating Agentic Coding Harnesses on TerminalBench-2), Section 5 (Discussion)
