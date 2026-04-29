# Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models

**Paper:** [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models (Zhang, Hu et al., 2025)](https://arxiv.org/abs/2510.04618)

## Human Readable TL;DR

Imagine you're training a new employee. Instead of retraining their brain every time they make a mistake, you give them an ever-growing playbook of tips, common pitfalls, and best practices -- and they keep getting better just by reading updated notes. This paper does exactly that for AI: instead of expensive retraining, it evolves a structured cheat sheet that the AI reads before each task, automatically adding lessons learned from past successes and failures. The result is an AI that improves itself cheaply and transparently.

## TL;DR

ACE (Agentic Context Engineering) is a framework that treats LLM contexts as evolving "playbooks" -- structured, itemized collections of strategies that grow incrementally via a Generator-Reflector-Curator pipeline. By using delta updates instead of monolithic rewrites, ACE prevents context collapse, achieves +10.6% on agent benchmarks and +8.6% on domain tasks, matches GPT-4.1-powered production agents using a smaller open-source model, and reduces adaptation latency by up to 91.5%.

---

## Problem & Motivation

Current context adaptation methods for LLMs suffer from two critical limitations:

1. **Brevity Bias** -- Prompt optimization techniques prioritize concise summaries, stripping out detailed domain heuristics, tool-use guidelines, and failure modes that complex tasks require.
2. **Context Collapse** -- Methods that monolithically rewrite contexts cause progressive information loss, where accumulated knowledge gets compressed into increasingly shallow summaries over iterations.

These limitations prevent LLM agents and domain-specific reasoning systems from retaining the granular, evolving knowledge needed for reliable performance on complex tasks. ACE is motivated by the need for a self-improving mechanism that accumulates comprehensive knowledge without expensive model fine-tuning.

---

## Main Original Ideas

1. **Modular Generator-Reflector-Curator Architecture** -- Separates context evolution into three specialized roles: a Generator that uses the current playbook, a Reflector that diagnoses errors and extracts actionable insights from execution traces, and a Curator that distills these into compact delta entries. This modularity prevents overloading a single model.

2. **Incremental Delta Updates** -- Contexts are represented as structured, itemized "bullets" with metadata (unique IDs, helpful/harmful counters). Instead of full rewrites, only small delta sets are merged via deterministic non-LLM logic, localizing updates and preserving past knowledge to prevent context collapse.

3. **Grow-and-Refine Mechanism** -- New bullets are appended while existing ones are updated in-place. Semantic embedding-based deduplication prunes redundancy, either proactively after each delta or lazily when context limits approach.

4. **Self-Supervision via Execution Feedback** -- ACE can adapt without labeled ground truth by leveraging natural execution signals (unit test results, environment feedback), reducing dependency on manually curated supervision.

5. **Dual-Mode Adaptation** -- The framework supports both offline optimization (system prompt engineering) and online adaptation (test-time agent memory), making it applicable across deployment scenarios.

---

## Key Findings

| Benchmark | Setting | ACE Improvement |
|-----------|---------|-----------------|
| AppWorld (agent) | Offline | **+12.3%** over ICL, **+11.9%** over GEPA |
| AppWorld (agent) | Online | **+7.6%** over Dynamic Cheatsheet |
| AppWorld (agent) | Self-supervised | **+14.8%** over ReAct baseline |
| FiNER (finance) | Offline | **+10.9%** avg over ICL/MIPROv2/GEPA |
| Formula (finance) | Offline | **+18.0%** |
| DDXPlus (medical) | -- | **+15.0%** |
| BIRD-SQL (text-to-SQL) | -- | **+5.1%** avg |

- On the AppWorld leaderboard, ReAct + ACE (59.4%) matched the top-ranked IBM-CUGA (60.3%) powered by GPT-4.1, despite using the smaller DeepSeek-V3.1 model. With online adaptation, ACE surpassed IBM-CUGA by 8.4% in Task Goal Completion.
- **Efficiency gains:** 82.3% reduction in adaptation latency vs. GEPA; 91.5% reduction vs. Dynamic Cheatsheet; 83.6% reduction in token costs. KV cache reuse reached 91.8% on GPT-5.1 API.
- Gains generalized across backbone LLMs (GPT-OSS-120B, GPT-5.1, Llama-3.3-70B).
- Ablation confirmed all components (Reflector, multi-epoch refinement, delta updates, offline warmup) contribute meaningfully to performance.

---

## Suggestions & Future Directions

1. **Reflector robustness** -- ACE's effectiveness depends on Reflector quality; future work should explore automated mechanisms for detecting and mitigating noisy or harmful reflections.
2. **Feedback quality dependency** -- Without reliable execution signals or ground-truth labels, performance can degrade; improving adaptation under sparse or noisy feedback is an open challenge.
3. **Task-type fit** -- ACE is most beneficial for knowledge-intensive tasks with complex tool use; tasks requiring only concise high-level instructions may not benefit as much.
4. **Responsible AI applications** -- The human-interpretable, itemized playbook structure enables selective unlearning for privacy, legal compliance, or knowledge correction.
5. **Integration with KV cache systems** -- Further research on advanced cache management could make long-context playbooks even more cost-effective at serving time.
6. **Continuous and online learning** -- ACE offers a lightweight alternative to fine-tuning for continual adaptation, with potential for broader deployment in dynamic environments.

---

## Authors & Institutions

Qizheng Zhang (Stanford University, SambaNova Systems), Changran Hu (SambaNova Systems, UC Berkeley), Shubhangi Upasani (SambaNova Systems), Boyuan Ma (SambaNova Systems), Fenglu Hong (SambaNova Systems), Vamsidhar Kamanuru (SambaNova Systems), Jay Rainton (SambaNova Systems), Chen Wu (SambaNova Systems), Mengmeng Ji (SambaNova Systems), Urmish Thakker (SambaNova Systems), Hanchen Li (UC Berkeley), James Zou (Stanford University), Kunle Olukotun (Stanford University).
