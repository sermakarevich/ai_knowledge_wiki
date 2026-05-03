# How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks

**Paper:** [How Do AI Agents Spend Your Money? (Bai, Huang, Wang et al., 2026)](https://arxiv.org/abs/2604.22750)

## Human Readable TL;DR

Imagine hiring a contractor who charges by the word -- and you only find out the final bill after the job is done. This paper studies how AI coding assistants "spend" your API budget, discovering that costs are wildly unpredictable, vary up to 30x for the same task, and that giving the AI more budget to think rarely produces better results. The researchers also tried asking the AI to estimate its own costs upfront, but found it consistently underestimates -- like a contractor who always quotes low. The findings push for better pricing transparency and smarter agents that know when to stop.

## TL;DR

This paper provides the first systematic empirical study of token consumption in agentic coding tasks. Using OpenHands on SWE-Bench-Verified with 8 frontier LLMs, the authors find that agentic tasks consume ~3500x more tokens than single-round reasoning, costs are heavy-tailed and highly stochastic (up to 30x variance for the same task), more tokens do not improve accuracy, and frontier models systematically underestimate their own token usage when asked to self-predict (peak Pearson r = 0.39).

---

## Problem & Motivation

AI agents are being deployed in complex software engineering workflows, but users face a fundamental problem: they cannot know the cost of a task before it runs, and are billed even for failed attempts. There is no systematic understanding of where tokens are spent in agentic pipelines, which models are efficient, or whether costs can be predicted pre-execution. This opacity undermines trust and budget management for both users and providers.

---

## Main Original Ideas

1. **Systematic token anatomy of agentic coding** -- The paper breaks down token consumption across five semantically meaningful phases (Setup, Explore, Fix, Validate, Closeout) and by token type (non-cached input, output, cache creation, cache read), revealing that cache-read tokens dominate volume while output tokens drive per-round cost spikes.

2. **Accuracy-cost decoupling** -- Contrary to intuition, higher token spend does not correlate with higher task accuracy. At the problem level, expensive tasks have lower accuracy; for repeated runs of the same task, accuracy peaks at intermediate cost and degrades at the highest expenditure, implicating unproductive loops.

3. **Human difficulty vs. agent cost misalignment** -- Human expert difficulty ratings (SWE-Bench-Verified "<15 min" vs. ">1 hour") correlate only weakly with actual agent token costs (Kendall τb = 0.32), showing that agent complexity is fundamentally different from human-perceived complexity.

4. **Cross-model token efficiency analysis** -- Among 8 frontier LLMs, token-efficient models (GPT-5, GPT-5.2) performed fewer redundant file view/modify actions; costly models (Kimi-K2, Qwen3-Coder-480B, Claude Sonnet 4) showed exploratory and repetitive interaction patterns -- even on tasks all models solved correctly.

5. **Self-prediction of token consumption** -- The same agent is repurposed pre-execution to estimate its own token costs using a phase-decomposition prompt with an in-context example. This establishes the first benchmark for agent self-cost-awareness, finding systematic underestimation across all models.

---

## Key Findings

| Metric | Value |
|--------|-------|
| Agentic vs. single-round reasoning tokens | ~3500x more |
| Agentic vs. multi-round chat tokens | ~1200x more |
| Max token spread across problems | ~7M tokens |
| Same-task run variance (max/min ratio) | up to 30x tokens, ~2x monetary cost |
| Kimi-K2 / Claude Sonnet 4.5 vs. GPT-5 extra tokens | >1.5M tokens more |
| Human difficulty vs. agent cost correlation | Kendall τb = 0.32 |
| Best self-prediction correlation (output tokens, Sonnet 4.5) | Pearson r = 0.39 |
| Prediction overhead vs. actual task cost | typically < 50% |

- Cache-read tokens are the dominant cost category by volume in every phase, despite output tokens being priced much higher per token.
- Per-round cost spikes occur at discrete events: repo exploration, file creation, test execution, and summarization.
- 6.7% of "easy" (<15 min) tasks consumed more tokens than the average "hard" (>1 hour) task.
- All tested models systematically underestimate token usage; underestimation worsens without in-context examples.
- Input-token prediction is consistently harder than output-token prediction.

---

## Suggestions & Future Directions

1. **Budget-aware agent policies** -- Design agents with explicit budget caps, "stop-early" mechanisms, and self-monitoring to terminate unproductive loops before costs spiral.
2. **Coarse-grained cost signals** -- Even if precise prediction is infeasible, relative cost signals (cheap/medium/expensive) could enable early warnings or user approval prompts before high-cost execution.
3. **Improved behavioral self-modeling** -- Future work should enhance agents' ability to model their own resource usage, which is a prerequisite for reliable pre-execution planning and pricing.
4. **Novel pricing architectures** -- The heavy-tailed, stochastic nature of costs makes flat-rate pricing impractical; the authors call for budget-aware, tiered, or hybrid pricing models.
5. **Open dataset** -- All agent trajectories are open-sourced to support follow-on research into token efficiency, cost estimation, and agent economics.

---

## Authors & Institutions

Longju Bai (University of Michigan), Zhemin Huang (Stanford / Microsoft AI), Xingyao Wang (All Hands AI), Jiao Sun (Google DeepMind), Erik Brynjolfsson (Stanford), Alex Pentland (Stanford / MIT), Jiaxin Pei (Stanford), Rada Mihalcea (University of Michigan)
