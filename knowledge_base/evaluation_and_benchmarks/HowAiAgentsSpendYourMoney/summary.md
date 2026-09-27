# How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks

**Paper:** [How Do AI Agents Spend Your Money? (Bai et al., 2026)](https://arxiv.org/abs/2604.22750)

## Human Readable TL;DR

Imagine you hired a contractor who charges by the hour. You expect smart workers to finish faster, but it turns out the smartest worker just reads your house blueprint over and over again -- thousands of times more than you expected -- and still can't guarantee a better result. That's what this study found with AI agents: they consume up to 1000x more computing resources than simpler AI tools, mostly because they keep re-reading their own work history on every step. Even worse, they can't tell you upfront how much it'll cost, and spending more doesn't mean getting better results.

## TL;DR

The first systematic study of token consumption in agentic coding tasks across eight frontier LLMs on SWE-bench Verified. Agents consume ~1000x more tokens than code reasoning/chat tasks, driven by input token accumulation. Token usage varies up to 30x on identical tasks, accuracy peaks at intermediate costs (not maximum), models differ dramatically in efficiency (Kimi-K2 and Claude Sonnet-4.5 use 1.5M+ more tokens per task than GPT-5), and frontier models systematically underestimate their own costs with correlations only up to 0.39.

---

## Problem & Motivation

AI agents are increasingly deployed in production workflows, but their inference costs are opaque and unpredictable. Users face no cost guarantees before execution, may pay for failed attempts, and have no reliable way to estimate expenses. The paper addresses three core questions: (1) Where do agents actually spend tokens? (2) Which models are token-efficient? (3) Can agents predict their own costs before running?

---

## Main Original Ideas

1. **First systematic token consumption study for agentic coding** -- Prior work studied chat/reasoning costs; this is the first to characterize the uniquely different cost structure of long-horizon agentic tasks with tool use and context accumulation.

2. **Input token dominance framing** -- Reframes the cost problem: agents are expensive not because they generate long outputs, but because they re-ingest exponentially growing context (repo state, tool outputs, conversation history) on every step. Input/output ratio is 0.16 for code reasoning vs. ~153 for agentic coding.

3. **Cost-accuracy non-monotonicity** -- Formally demonstrates that accuracy peaks at intermediate token costs and saturates or declines at higher costs, disproving the intuition that spending more reliably yields better outcomes.

4. **Pre-execution token prediction benchmark** -- Formalizes and benchmarks a new task: asking agents to self-predict their own token usage before execution, establishing baselines and exposing a fundamental capability gap.

5. **Phase-level cost decomposition** -- Introduces a five-phase trajectory decomposition (Setup, Explore, Fix, Validate, Closeout) revealing that cache-read tokens dominate cost despite being cheapest per token due to sheer volume.

---

## Key Findings

| Finding | Detail |
|---|---|
| Agentic vs. reasoning tokens | ~3,500x more tokens than single-turn reasoning; ~1,200x more than multi-turn chat |
| Agentic vs. chat cost | $1.857 avg vs. $0.023 for chat per task |
| Cross-run variance | Same task, same model: up to **30x** token difference between cheapest and most expensive run |
| Cross-problem variance | Most expensive problem uses ~7M more tokens than cheapest |
| Accuracy-cost relationship | Accuracy peaks at intermediate cost; declines at MaxCost due to redundant file actions |
| Model efficiency gap | Kimi-K2 and Claude Sonnet-4.5 use **1.5M+ more tokens per task** than GPT-5 on identical tasks |
| Human difficulty alignment | Kendall τb = **0.32** -- weak correlation between expert-rated difficulty and actual token cost |
| Self-prediction correlation | Best model achieves Pearson r = **0.39**; all models systematically underestimate input tokens |
| Dominant cost driver | Cache-read input tokens dominate all five task phases despite low per-token price |
| High-cost failure pattern | Failed high-cost runs show significantly more repeated file view/modification actions |

- Token efficiency ranking is consistent across shared-success and shared-failure task subsets -- it's a model property, not task-dependent
- GPT-5/GPT-5.2 show only mild token increase on failures (<0.5M), while Kimi-K2 spikes ~2M, suggesting poor early-stopping mechanisms
- Self-prediction overhead is generally <50% of task cost (Sonnet 4.5: 0.32x, GPT-5.2: <6%)

---

## Suggestions & Future Directions

1. **Budget-aware tool-use policies** -- Agents need mechanisms to recognize unsolvable tasks and stop early rather than continuing expensive exploration cycles.

2. **Token-efficiency as a primary model selection criterion** -- Teams should benchmark models on cost-per-correct-outcome alongside capability benchmarks; a model solving 5% more tasks with 40% more tokens may be the wrong choice.

3. **Better prediction mechanisms** -- Current self-prediction is too weak for reliable cost transparency; future work should explore external predictors trained on observed trajectory distributions.

4. **Context management strategies** -- Research into alternative approaches for managing growing agent context to mitigate input token dominance.

5. **Outcome-based pricing models** -- The current consumption-based pricing penalizes users for agent inefficiencies; providers should explore pricing tied to task outcomes rather than raw token counts.

6. **Instrumentation over introspection** -- Cost-aware routing must use observed production data, not model self-reports, since models systematically underestimate their costs.

---

## Authors & Institutions

Longju Bai (University of Michigan), Zhemin Huang (Stanford University, Microsoft AI), Xingyao Wang (All Hands AI), Jiao Sun (Google DeepMind), Rada Mihalcea (University of Michigan), Erik Brynjolfsson (Stanford University), Alex Pentland (Stanford University, MIT), Jiaxin Pei (Stanford University)
