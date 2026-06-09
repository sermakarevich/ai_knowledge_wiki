# Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions

**Paper:** [Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions (Hu, Wang, McAuley, 2025)](https://arxiv.org/abs/2507.05257)

## Human Readable TL;DR

Imagine hiring an assistant who handles many tasks over months -- you'd want them to remember your preferences, learn new things on the job, understand the whole project history, and update their knowledge when facts change. This paper reveals that today's AI assistants are being tested mostly on short-term tasks, so nobody really knows how well they handle long-term memory. The authors built a new exam (MemoryAgentBench) covering all four memory skills, tested many AI systems, and found that none of them pass all four tests -- especially when it comes to forgetting outdated information.

## TL;DR

This paper introduces MemoryAgentBench, a comprehensive benchmark evaluating LLM agent memory across four core competencies: accurate retrieval (AR), test-time learning (TTL), long-range understanding (LRU), and selective forgetting (SF). Unlike prior work that evaluates static long-context models, it feeds information incrementally over multi-turn interactions to better reflect real agentic use. Empirical results across RAG agents, long-context models, and agentic memory systems reveal that no existing method excels at all four competencies -- selective forgetting in particular remains nearly unsolved (≤7% on multi-hop scenarios).

---

## Problem & Motivation

Current LLM agent benchmarks (GAIA, SWE-Bench) evaluate reasoning, planning, and tool use -- but systematically ignore memory quality. Memory architectures have proliferated (MemGPT, Mem0, RAG variants, parametric memory), yet no unified benchmark exists to compare them. Critically, existing long-context benchmarks provide the entire history in a single pass; real memory agents must absorb information incrementally, compress it, and selectively update it over many turns -- a fundamentally different challenge.

---

## Main Original Ideas

1. **MemoryAgentBench** -- A unified benchmark covering four memory competencies via incremental multi-turn interactions, combining reconstructed existing datasets with two newly constructed ones (EventQA, FactConsolidation).

2. **Four Core Memory Competencies** -- Grounded in cognitive science: Accurate Retrieval (AR), Test-Time Learning (TTL), Long-Range Understanding (LRU), and Selective Forgetting (SF). Prior benchmarks covered at most one or two of these.

3. **EventQA (new)** -- Automatically constructed from novels to test temporal reasoning: given past events, predict the correct next event from multiple choices across 100k+ token narratives.

4. **FactConsolidation (new)** -- Built from counterfactual edit pairs (MQUAKE), testing whether agents correctly prioritize newer contradictory facts over older ones in 262K-token contexts, in both single-hop and multi-hop variants.

5. **Incremental Evaluation Protocol** -- All tasks are reformulated as `chunks → questions` pipelines: each chunk is fed one at a time with memorization instructions, simulating real deployment conditions rather than providing the full context upfront.

---

## Key Findings

| Competency | Best Performer | Key Finding |
|---|---|---|
| **Accurate Retrieval** | RAG agents (HippoRAG-v2) | RAG excels; designed for snippet extraction |
| **Test-Time Learning** | Long-context models (GPT-4o, Claude-3.7) | RAG lacks holistic learning capacity |
| **Long-Range Understanding** | Long-context models | RAG retrieves partial info; fails at global reasoning |
| **Selective Forgetting (SH)** | Long-context models (barely) | Remains very challenging for all agents |
| **Selective Forgetting (MH)** | None (max ~7%) | Near-unsolved for all current systems |

- **RAG bottleneck is retrieval, not LLM:** Upgrading from GPT-4o-mini to GPT-4.1-mini backbone yields only marginal gains for RAG agents -- the retriever itself is the bottleneck.
- **Agentic memory benefits from stronger LLMs:** MIRIX shows substantial gains with a stronger backbone, indicating iterative reasoning loops leverage LLM capacity effectively.
- **Smaller chunk sizes help AR:** Finer segmentation improves RAG retrieval precision. Larger Top-K helps most tasks but increases context load.
- **Selective forgetting is solvable in short contexts:** GPT-4o and O4-mini achieve 80% on FactCon-MH at 6K tokens, confirming the task is valid -- but performance collapses as context grows to 32K+.
- **Prompt policies insufficient for SF:** Instructing agents to "always prefer later facts" helps marginally for single-hop but fails multi-hop; dedicated memory mechanism design is required.

---

## Suggestions & Future Directions

1. Develop memory architectures that go beyond retrieval -- enabling holistic integration of distributed information for test-time learning and long-range understanding.
2. Design dedicated selective forgetting mechanisms that can actively revise or overwrite stored knowledge when contradictions are encountered at scale.
3. Explore hybrid approaches combining long-context retention with structured memory compression to achieve coverage across all four competencies simultaneously.
4. Investigate whether reasoning-specialized models (O4-mini class) can be adapted for long-context memory updating, given their strong short-context SF performance.
5. Extend MemoryAgentBench to cover multimodal inputs, domain-specific agents (medical, legal), and more complex multi-hop TTL scenarios.

---

## Authors & Institutions

Yuanzhe Hu (UC San Diego), Yu Wang (UC San Diego), Julian McAuley (UC San Diego)
