# LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling

**Paper:** [LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling (Zheng et al., 2026)](https://arxiv.org/abs/2605.08083)

## Human Readable TL;DR

Imagine you're solving a hard math problem and you can choose how many times to re-read it, how many different approaches to try at once, and when to give up on a dead-end strategy. Researchers have been hand-crafting these "thinking time" rules for AI models by gut feeling. This paper builds a robot coach (AutoTTS) that watches AI models solve problems, figures out better rules automatically, and -- remarkably -- the coach it trains using just one set of problems also works well on completely different problems and different AI models. The whole coaching process cost about $40 and took under 3 hours.

## TL;DR

AutoTTS is an environment-driven framework that automates the discovery of Test-Time Scaling (TTS) strategies for LLMs. Instead of hand-crafting branching, pruning, and stopping heuristics, researchers define a structured control space and let an explorer LLM iteratively propose and refine code-defined controllers evaluated against pre-collected reasoning trajectories (offline replay). Two key innovations -- beta parameterization (single scalar hyperparameter) and fine-grained execution trace feedback -- make search tractable. Discovered controllers outperform hand-crafted baselines on AIME24/25 and HMMT25 across four Qwen3 model sizes, generalize to held-out tasks and model families, and cost only $39.9 and 160 minutes to discover.

---

## Problem & Motivation

Existing TTS strategies (Self-Consistency, Adaptive Self-Consistency, Parallel-Probe, etc.) are all hand-crafted: researchers manually hypothesize when to branch, deepen, probe, prune, or stop reasoning paths, then tune thresholds by intuition. This approach is labor-intensive, cognitively biased, and leaves most of the computation-allocation space unexplored. Performance depends not just on *how much* computation is used, but critically on *how* it is allocated -- suggesting that systematic automated search could find significantly better policies than human intuition produces.

---

## Main Original Ideas

1. **AutoTTS Framework -- TTS as Controller Synthesis** Instead of designing individual TTS heuristics, humans define a discovery environment (states, actions, feedback, objectives) and an explorer LLM searches for optimal controllers within it. This reframes human expertise from strategy design to environment construction.

2. **Offline Replay Environment** For each problem, 128 reasoning trajectories and intermediate probe signals are pre-collected from the base LLM. Candidate controllers replay their decisions (BRANCH, CONTINUE, PROBE, PRUNE, ANSWER) against this static data, enabling fast, deterministic, LLM-call-free evaluation -- the key to affordable search.

3. **Beta Parameterization** Each discovered controller exposes only a single scalar trade-off parameter β from which all internal hyperparameters are derived deterministically via monotonic functions. This collapses the high-dimensional hyperparameter space to a 1D sweep, preventing overfitting to the search set and promoting robustness.

4. **Fine-Grained Execution Trace Feedback** Beyond scalar accuracy-cost outcomes, the explorer LLM receives full execution traces logging which branches were expanded, pruned, or stopped at each step. This lets the agent diagnose *why* a controller fails and propose targeted fixes rather than guessing from aggregated metrics.

5. **Confidence Momentum Controller (CMC)** The final discovered controller implements four non-obvious mechanisms: EMA-based trend stopping (not just instantaneous confidence), coupled width-depth control driven by EMA delta, alignment-aware depth allocation (favoring branches agreeing with current pool winner), and conservative branch abandonment (pruning only after persistent deviation, always keeping ≥2 branches). These are difficult to arrive at by manual intuition.

---

## Key Findings

| Setting | Method | Accuracy | Tokens |
|---------|--------|----------|--------|
| Qwen3 avg (AIME25+HMMT25) | SC@64 | ~45.2% | ~830K |
| Qwen3 avg (AIME25+HMMT25) | AutoTTS β=0.5 | **45.3%** | **253K (-69.5%)** |
| Qwen3 avg (AIME25+HMMT25) | AutoTTS β=1.0 | **53.1%** | 575.5K |
| DeepSeek-R1-Llama-8B (HMMT25) | AutoTTS β=1.0 | **highest** | significantly lower |
| Qwen3-1.7B (GPQA-Diamond) | AutoTTS β=0.5 | comparable | 151K vs 510K SC |

- AutoTTS improves the accuracy-cost Pareto frontier in 3 out of 4 Qwen3 model sizes on held-out benchmarks
- β=0.5 achieves ~69.5% token reduction vs SC@64 with equivalent accuracy
- β=1.0 pushes peak accuracy beyond all hand-crafted baselines in 5 out of 8 model-benchmark combinations
- **Ablation:** Removing beta parameterization → overfitting (49.0% vs 53.1% on held-out, 93.3K tokens -- over-pruning)
- **Ablation:** Removing execution traces → worse accuracy (51.6%) and more tokens (824.3K)
- Discovery cost: $39.9 and 160 minutes wall-clock for 5 rounds

---

## Suggestions & Future Directions

1. **Richer action spaces** -- Expand beyond width-depth control (e.g., tree search, verifier-guided refinement) to enable discovery of more complex control structures.
2. **Open-source explorer agents** -- Investigate whether open-source coding LLMs can match Claude's discovery performance in the explorer role.
3. **Broader task generalization** -- Further validate discovered controllers on diverse non-mathematical reasoning tasks and domains beyond AIME, HMMT, and GPQA.
4. **Richer environment feedback** -- Explore additional feedback signals beyond execution traces (e.g., per-branch confidence trajectories, error categorization).
5. **Misuse risk** -- Acknowledge that more efficient reasoning systems could lower the barrier to misuse of powerful LLMs; inference optimization research carries inherent dual-use concerns.

---

## Authors & Institutions

Tong Zheng (UMD), Haolin Liu (UVA), Chengsong Huang (WUSTL), Huiwen Bao, Sheng Zhang (UMD), Rui Liu (UMD), Runpeng Dai (UNC), Ruibo Chen (UMD), Chenxi Liu (UMD), Tianyi Xiong (UMD), Xidong Wu (Google), Hongming Zhang (Meta), Heng Huang (UMD)
