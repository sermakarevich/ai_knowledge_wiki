> [[index|Wiki]] | [[digest|Digest]]

# Summary

**Paper:** GoAgent: Group-of-Agents Communication Topology Generation for LLM-based Multi-Agent Systems (arXiv:2603.19677)

## Human Readable TL;DR

When you put a team of AI agents together to solve a hard task, someone (or something) has to decide who talks to whom. Most existing methods build that conversation map one agent-connection at a time, the way you'd wire up light switches one by one. GoAgent instead notices that real teams work in *sub-teams* — a "solver" trio, a "verifier" pair — and builds the map by choosing whole sub-teams and then wiring the sub-teams together, not the individual agents. It also has a filter that strips out irrelevant chatter between sub-teams, keeping only what actually matters for the specific question being asked. The result: better answers, ~17% fewer tokens spent, and it holds up better when one agent in the team gets sabotaged.

## TL;DR

GoAgent generates task-specific multi-agent communication topologies by treating LLM-proposed collaborative *groups* — not individual agents — as the atomic construction unit, autoregressively selecting and connecting groups, and applying a Conditional Information Bottleneck (CIB) to compress inter-group communication down to task-relevant signal only. It achieves 93.84% average accuracy across six benchmarks (best of all methods compared) while using ~17% fewer tokens than the strongest baseline, and it degrades least under a simulated prompt-injection attack.

## Problem & Motivation

LLM-based multi-agent systems (MAS) depend heavily on their communication topology — the directed graph of who shares information with whom. Existing approaches evolved from hand-crafted static graphs (chains, trees, fully-connected debate) to template-based pruning (AgentPrune, AgentDropout, G-Designer) to fully autoregressive from-scratch generation (ARG-Designer) — but all of them are **node-centric**: they predict one agent-connection at a time as an isolated local decision. This has two failure modes: (1) higher-order divide-and-conquer structures (e.g. a decomposer→solver→verifier sub-team) have to emerge implicitly from many small edge decisions, producing disjointed workflows, and (2) without explicit group boundaries, graphs become dense and unconstrained, wasting tokens on redundant message-passing and letting task-irrelevant historical noise accumulate.

## Main Original Ideas

- **Group-centric generation:** flip the atomic unit of graph construction from individual agents to whole collaborative groups. An LLM first proposes a pool of K candidate groups (each with a name, expertise, roles, and a fixed intra-group topology template); a learned autoregressive model then selects which groups to use and predicts the edges *between* groups only.
- **Conditional Information Bottleneck (CIB):** replaces the standard information bottleneck's fixed prior with a task-conditioned prior, so compression of inter-group communication features is explicitly guided by the specific task query — filtering noise relative to *this* task rather than blindly.
- **Auto-curated training data, no RL:** ground-truth (task, topology) pairs are collected by sampling diverse candidate graphs, executing them with LLMs, and keeping the minimal viable graphs that solved the task — then trained end-to-end with supervised Teacher Forcing, avoiding the high variance of online reinforcement learning.

## Key Findings

**Accuracy across six benchmarks** (from [[wiki/03-experiments-and-related-work]]):

| Method | MMLU | GSM8K | AQuA | MultiArith | SVAMP | HumanEval | Average |
|---|---|---|---|---|---|---|---|
| Vanilla | — | — | — | — | — | 71.39 | 80.80 |
| ARG-Designer (best baseline) | 89.54 | — | — | — | — | 91.74 | 92.62 |
| **GoAgent** | **91.50** | **95.30** | **86.45** | **99.11** | **96.46** | **94.21** | **93.84** |

- GoAgent beats Vanilla by 13.04 points average and the strongest node-centric baseline (ARG-Designer) by 1.22 points; gains are largest on hard tasks (MMLU +1.96 pts, HumanEval +2.47 pts over ARG-Designer).
- **Ablation:** removing group-centric generation costs −2.61 avg accuracy; removing CIB costs −3.27; removing both costs −4.12 — the two mechanisms are complementary, not redundant.
- **Token efficiency:** GoAgent uses ~17% fewer tokens than ARG-Designer at equal or better accuracy (e.g. 1.9×10⁵ tokens on MMLU vs. LLM-Debate's 1.6×10⁶ and Complete's 6.7×10⁵).
- **Robustness:** under a simulated prompt-injection attack (one agent compromised), GoAgent drops only 91.5%→89.5% accuracy, while the Full/fully-connected baseline collapses from 82.3%→70.6%.

## Suggestions & Future Directions

The paper's own limitations (from [[wiki/03-experiments-and-related-work]]) point to two directions: (1) the group pool is fixed offline by an LLM, so GoAgent cannot synthesize entirely new group structures or roles at inference time if a task needs expertise outside the predefined pool; (2) evaluation is limited to static reasoning tasks (MMLU, GSM8K, code generation) — effectiveness in dynamic, interactive settings (embodied AI, multi-agent RL) is untested.

## Authors & Institutions

Hangzhou Dianzi University, RMIT University, Griffith University.

## Figures

- `wiki/images/fig1-node-vs-group-paradigm.png` — contrasts node-centric (agent-by-agent) vs. group-centric (GoAgent) topology generation paradigms.
- `wiki/images/fig3-token-efficiency-robustness.png` — token cost vs. accuracy trade-off on MMLU/GSM8K and accuracy drop under the prompt-injection attack, across methods.

See [[wiki/01-problem-and-motivation]] and [[wiki/03-experiments-and-related-work]] for the full figure walkthroughs.
