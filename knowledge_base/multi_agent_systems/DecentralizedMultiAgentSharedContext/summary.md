# Decentralized Multi-Agent Systems with Shared Context

**Paper:** [Decentralized Multi-Agent Systems with Shared Context (Mao & Mirhoseini, 2026)](https://arxiv.org/abs/2606.10662)

## Human Readable TL;DR

Imagine a team of researchers working on a big problem. In most teams today, there's one manager who assigns tasks, collects everyone's results, and tells others what was found -- this manager becomes a bottleneck. This paper proposes giving the whole team a shared whiteboard: anyone can write down what they discovered (after a fact-check), and anyone else can read it directly. The whiteboard uses a smart layered system -- headlines first, full details available on demand -- so no one gets overwhelmed. The result is a faster, cheaper team that avoids repeating dead ends and builds on each other's work naturally.

## TL;DR

DELM (Decentralized Language Models) replaces centralized orchestration in multi-agent LLM systems with a shared verified context and asynchronous task queue. Agents write compact, admission-verified gist entries into shared state that all peers can read directly, eliminating the bottleneck of routing every update through a main controller. On SWE-bench Verified, DELM gains up to 10.5 pp over the strongest baseline while cutting cost per task by ~50%; on LongBench-v2 Multi-Doc QA, it improves accuracy by up to 5.7 pp across four frontier model families.

---

## Problem & Motivation

Most LLM multi-agent systems (Claude Code Subagents, Kimi Agent Swarm, AOrchestra) use centralized orchestration: a main agent decomposes tasks, assigns subcontexts, collects sub-agent outputs, and merges results. This creates two compounding failures as scale increases:

1. **Communication bottleneck** -- every finding, failure, or partial solution must pass through the main agent, which then decides what to rebroadcast. This serializes what should be parallel progress sharing, and the main agent becomes increasingly overloaded.
2. **Fidelity loss** -- during the routing and rewriting process, the main agent may dilute, omit, or soften constraints and negative results. A sub-agent's critical failure can become a reopened suggestion by the time it reaches the next worker.

In long-context tasks (multi-document QA), the same problem manifests differently: the controller pre-assigns evidence clusters before knowing their relevance, forcing slow iterative back-and-forth when a sub-agent needs more context.

---

## Main Original Ideas

1. **State-based coordination via shared verified context** -- Instead of prompt-routing intermediate progress through a central controller, agents write compact verified updates to a global shared context (C) and asynchronous task queue (T). Any agent can read C directly. Coordination becomes accumulative shared state rather than serialized message passing.

2. **Hierarchical unfoldable context (Gist → Summary → Raw)** -- The shared context stores three levels of representation per evidence unit: (a) a compact gist G_i (~100 tokens) as the default view, (b) a reference-grounded summary S_i with atomic bullets and verbatim ref-tags tied to source spans, and (c) the raw source R. Agents read gists by default and explicitly `UNFOLD` or `DEEP_UNFOLD` when precision is needed, incurring detail costs only for relevant evidence.

3. **Admission-time verification** -- Before any gist enters the shared context, it is checked against its supporting evidence. For summaries: each bullet must have its head and tail verbatim appear in-order in the source (failed bullets are regenerated or dropped). For gists: a lightweight LLM verifier checks for hallucination and semantic drift relative to the parent summary. Only verified entries become reusable shared state.

4. **Dynamic subtask generation** -- When the task queue empties, the most-recently-completed agent inspects the current shared context and determines whether additional subtasks are needed, generating and enqueuing them conditioned on accumulated state. This avoids both premature termination and deadlocks from over-aggressive up-front decomposition.

5. **DELM+RLM hybrid** -- DELM is a coordination layer, not a reasoner. Combining it with Recursive Language Models (which provide code-mediated REPL execution) yields best-of-both: RLM's precise programmatic aggregation plus DELM's decentralized verified state sharing.

---

## Key Findings

### SWE-bench Verified (test-time scaling, Gemini 3 Flash base)

| Method | Avg.@1 | Pass@2 | Pass@4 | Cost/Task |
|---|---|---|---|---|
| mini-SWE-agent | 54.7% | 65.6% | 75.1% | $0.26 |
| Claude Code | 49.3% | 57.1% | 66.3% | ~$1.00 |
| AOrchestra | 55.2% | 64.5% | 73.2% | $0.24 |
| AOrchestra-Parallel | 56.4% | 63.2% | 71.8% | $0.25 |
| **DELM** | **65.7%** | **72.9%** | **77.4%** | **$0.12** |

- DELM gains +9.3 pp Avg.@1 over the strongest baseline while halving cost
- Three concrete mechanisms: (1) failed hypotheses become shared FAIL facts preventing redundant exploration; (2) constraints (e.g., Django ORM M2M filter semantics) admitted as binding state can't be reopened by the controller; (3) compact PATCH_SUMMARY entries hand off discoveries without exposing peers to full command histories ($0.125 vs $0.399 for same task)

### LongBench-v2 Multi-Doc QA (average accuracy, 125 samples)

| Base Model | Best Baseline | **DELM** | Gain |
|---|---|---|---|
| GPT-5.4 | 54.4% | **60.1%** | +5.7 pp |
| Claude Sonnet 4.6 | 54.5% | **59.8%** | +5.3 pp |
| Gemini 3 Flash | 57.1% | **61.5%** | +4.4 pp |
| DeepSeek-V4-Pro | 63.9% | **67.5%** | +3.6 pp |

- Ablation: removing admission-time verification drops accuracy most sharply (60.1% → 55.2%); removing hierarchical summarization drops to 57.7%; gist length stabilizes at 100 tokens
- Summarization model quality barely matters -- cheapest available (DeepSeek-V4-Flash) performs comparably to frontier models

### OOLONG + RLM hybrid (GPT-5, programmatic aggregation)

| Method | OOLONG Acc. | Cost | LB-v2 Acc. | Cost |
|---|---|---|---|---|
| RLM | 56.0% | $0.43 | 55.8% | $0.29 |
| DELM | 53.3% | $0.47 | 57.9% | $0.30 |
| **DELM+RLM** | **64.0%** | **$0.40** | **60.3%** | **$0.24** |

- Hybrid is strictly better and cheaper than either method alone across both benchmarks

---

## Suggestions & Future Directions

1. **Lighter-weight verifiers** -- Admission-time verification adds modest overhead; learned or rule-based verifiers for common claim types could reduce this cost while preserving grounding guarantees.

2. **Adaptive decomposition agents** -- Current decomposition quality bounds system performance. Training agents to decide when to split, merge, or terminate subtasks based on shared context state is a direct improvement lever.

3. **Prompt evolution per model family** -- DELM's decomposition, summarization, and verification prompts are not universally optimal across model families; combining with prompt-evolution methods (e.g., GEPA) could close the per-model gap.

4. **Automated research workflows** -- The authors identify this as the natural application domain: agents exploring alternative hypotheses, inspecting large paper collections, comparing cross-source evidence, and iteratively refining conclusions -- all directly addressed by DELM's design. A decentralized verified context prevents repeated reading of the same papers and enables findings to propagate across parallel research threads.

---

## Authors & Institutions

Yuzhen Mao (Stanford University), Azalia Mirhoseini (Stanford University)
