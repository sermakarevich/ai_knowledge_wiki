# AREX: Towards a Recursively Self-Improving Agent for Deep Research

**Paper:** [AREX: Towards a Recursively Self-Improving Agent for Deep Research (Lu, Li, Luo, Zhang, Wang, Xiao, Liu et al., BAAI, 2026)](https://www.alphaxiv.org/abs/2607.21461)

## Human Readable TL;DR

Imagine you're trying to book a trip that must satisfy a dozen picky requirements at once (budget, dates, layover length, hotel rating, visa rules...). It's really hard to *find* an itinerary that hits all of them, but once someone hands you a candidate itinerary, it's much easier to *check* it requirement-by-requirement and say which ones fail. AREX is an AI research agent built around exactly that asymmetry: instead of just searching longer and longer, it keeps a running scorecard of which requirements are still unmet, uses that scorecard to decide what to search for next, and periodically compresses its own memory so it doesn't drown in its own notes. It comes in a small "Turbo" version and a bigger "Base" version, and both do well on hard research benchmarks compared to other AI systems.

## TL;DR

AREX is a deep-research agent architecture built around a "discovery-verification asymmetry": finding an answer that jointly satisfies many constraints is expensive, but verifying a candidate answer decomposes cheaply into per-constraint checks. It pairs an inner research loop (gathers evidence, drafts candidate answers) with an outer self-improvement loop (audits the draft constraint-by-constraint and decides to accept/refine/restart), plus a learned "context updating" mechanism that compresses interaction history while preserving verified evidence and open constraints. Training combines agentic mid-training with long-horizon RL that weights credit assignment toward critical decision steps. Two model sizes — a 4B dense "Turbo" and a 122B-A10B MoE "Base" — post strong, sometimes SOTA, results on six deep-research benchmarks.

---

## Problem & Motivation

Deep-research agents are increasingly asked to answer queries with several coupled constraints that must all hold simultaneously (e.g., "find X such that A, B, and C are all true"). Existing agents mostly cope by extending the search trajectory — more reasoning steps, more tool calls — but this doesn't fix the underlying failure mode: early mistakes persist uncorrected, already-exhausted search directions get revisited, and partially-valid candidates get accepted prematurely because the agent has no explicit bookkeeping of which constraints are still open.

The paper's central observation is a **discovery-verification asymmetry**: discovering a candidate that satisfies every constraint requires navigating a large, sparsely-informative search space, but *checking* a given candidate can be decomposed into much simpler, independent constraint-wise verifications. AREX is designed to exploit this asymmetry directly rather than trying to brute-force better single-pass search.

---

## Main Original Ideas

1. **Recursive self-improvement via two nested loops.** An inner *research loop* gathers evidence through tool use and constructs a provisional answer; an outer *self-improvement loop* audits that answer constraint-by-constraint, assigns a confidence assessment, and decides whether to accept, refine, or restart the trajectory.

2. **Autonomous context updating.** A learned compression step rewrites the interaction history into a compact state that preserves verified evidence and the list of unresolved constraints (rather than truncating or naively summarizing), so the agent can run long, multi-round research without losing track of what's already settled.

3. **Progressive, key-step-aware training.** Training is staged: browse-intensive tool-use skills are established before reasoning-intensive skills, and a key-step supervision mechanism concentrates the learning signal on decision-critical moments in a trajectory rather than spreading it uniformly.

4. **Step-aware reinforcement learning with hierarchical normalization.** The RL stage normalizes credit assignment hierarchically so that trajectory length doesn't dominate the reward signal — long meandering trajectories aren't implicitly favored over short decisive ones.

5. **Two implementation variants.** A 4B dense model ("Turbo") for lower-cost deployment and a 122B-A10B Mixture-of-Experts model ("Base") for maximum capability, both trained with the same recipe.

---

## Key Findings

Evaluated across six deep-research benchmarks (BrowseComp, GAIA, xbench-2510, DeepSearchQA, WideSearch, HLE):

| Model | BrowseComp | GAIA | xbench-2510 | DeepSearchQA | WideSearch-en | HLE (tool) |
|---|---|---|---|---|---|---|
| AREX-Turbo (4B) | 70.7 | 81.6 | 57.0 | 78.5 | 68.5 | 40.6 |
| **AREX-Base (122B-A10B MoE)** | 82.5 | 85.4 | 71.0 | 89.9 | **82.0** | 52.4 |
| GPT-5.4 | 82.7 | – | – | 88.5 | 77.5 | 52.1 |
| Opus-4.6 | 83.7 | – | – | 91.3 | 77.5 | 53.0 |
| Gemini-3.1-Pro | **85.9** | 80.6 | 53.0 | **93.3** | 66.4 | 51.4 |
| Kimi-K2.6 | 83.2 | 80.6 | **90.0** | 92.5 | 80.8 | **54.0** |
| DeepSeek-V4-Pro | 83.4 | – | 80.0 | 88.7 | 78.0 | 48.2 |
| Qwen3.5-397B | 78.6 | 83.5 | 61.0 | 82.1 | 74.0 | 48.3 |
| MiroThinker-H1 | **88.2** | **88.5** | 72.0 | 80.6 | – | 47.7 |

- AREX-Base achieves the **best reported WideSearch-en score** (82.0) and is competitive with models using substantially more activated parameters (e.g., beats GPT-5.4 and Opus-4.6 head-to-head on WideSearch-en and GAIA).
- Ablations: the full recursive system (context updating + outer self-improvement loop) gains **22.9 points** over a variant with neither component.
- Context updating triggers in 80.3% of cases, and when it does it preserves unresolved constraints 95.5% of the time and next-step plans 96.4% of the time — evidence the compression mechanism isn't silently dropping important state.
- Progressive training ordering (browse-intensive before reasoning-intensive) and key-step supervision each contribute substantial standalone gains in ablations.

---

## Suggestions & Future Directions

1. The paper offers limited discussion of failure cases or systematic limitations of the approach itself.
2. **Trajectory self-distillation** (explored in an appendix) showed promise but was not integrated into the final system — flagged as "a promising direction for future iterations."
3. The current key-step detection is rule-based; the authors explicitly call for **more general and autonomous mechanisms for estimating step utility** and assigning fine-grained training signal, rather than hand-specified rules.

---

## Authors & Institutions

Shuqi Lu, Chaofan Li, Kun Luo, Zhang Zhang, Hui Wang, Hongwang Xiao, Zheng Liu (project lead), Lei Xiong, Jiahao Wang, Sen Wang, Xiyan Jiang, Wanli Li, Yuyang Hu, Hongjin Qian, Bingyu Yan, Jianlyu Chen, Ziyi Xia — Beijing Academy of Artificial Intelligence (BAAI).
