# Memory Transfer Learning: How Memories are Transferred Across Domains in Coding Agents

**Paper:** [Memory Transfer Learning (Kim, Kang, Kim, Yang, Ren, Hwang, 2026)](https://arxiv.org/pdf/2604.14004)

## Human Readable TL;DR

Imagine a junior developer who keeps a notebook of lessons learned. If they only write down lessons from one kind of project (say, web apps), the notebook is useful only for web apps. This paper asks: what if the notebook contained lessons from every kind of coding they have ever done -- competitive puzzles, fixing open-source bugs, ML experiments -- and they could flip to relevant pages for a brand-new task? The authors find that cross-domain notes do help, but only when the notes are written as general advice ("always run tests before declaring success") rather than specific code snippets ("here is exactly how I fixed bug X"). Abstract wisdom travels; concrete recipes do not.

## TL;DR

This paper introduces Memory Transfer Learning (MTL) for self-evolving coding agents and shows that a unified memory pool spanning heterogeneous coding benchmarks (competitive, function-level, repo-level, ML research, scientific replication) lifts Pass@3 by 3.7% on average for GPT-5-mini. They systematically compare four memory representations (Trajectory, Workflow, Summary, Insight) and find that transfer effectiveness scales with abstraction -- high-level Insight memories win because they encode transferable "meta-knowledge" (workflow discipline, test-driven verification, anti-pattern avoidance) rather than algorithmic code. Benefits scale with memory-pool size and number of source domains, transfer across models (DeepSeek, Qwen3-Coder), and even beat ReasoningBank and AgentKB despite using smaller pools. Low-abstraction traces can cause negative transfer by anchoring the agent to brittle, context-specific details.

---

## Problem & Motivation

Memory-augmented coding agents have so far trained and retrieved memories only within a single task domain (e.g., only SWE-Bench, only competitive programming). This siloed design ignores the shared infrastructural substrate -- Linux shells, programming languages, runtimes, repository layouts, test harnesses -- that underlies essentially all coding tasks. The result: agents cannot exploit a rich, heterogeneous memory pool that would reflect how human engineers actually learn, by generalizing across problem types. The authors argue this is a significant lost opportunity given that raw scaling of training data has plateaued for code LLMs, making self-evolving memory one of the few remaining axes of improvement.

---

## Main Original Ideas

1. **Memory Transfer Learning (MTL) formulation.** A systematic study of cross-domain memory for coding agents, posed via three research questions: (RQ1) does heterogeneous memory help, (RQ2) why, and (RQ3) which design factors matter. This reframes self-evolving agents away from single-domain memory silos toward a unified, transferable knowledge pool.

2. **Four-tier memory-abstraction taxonomy.** The authors construct and compare Trajectory (raw action+observation logs), Workflow (extracted reusable action sequences), Summary (LLM-written analysis of success/failure), and Insight (task-agnostic title/description/content inspired by ReasoningBank). This ladder of abstraction is the experimental knob that isolates what actually transfers.

3. **Empirical identification of "meta-knowledge" as the transferable unit.** Through qualitative analysis of successful transfers they quantify categories of transferred knowledge: iterative workflow discipline (15.0%), test-driven verification (14.5%), anti-pattern avoidance (10.4%), input validation (8.5%), API/interface compliance (8.1%), etc. Direct algorithmic strategy transfer is only 5.5% -- the value is procedural, not algorithmic.

4. **Abstraction-dictates-transferability principle.** t-SNE, DBI, and LISI analyses show Insight embeddings are domain-intermingled while Trajectory embeddings cluster by domain. A controlled "task-specific vs task-agnostic insights" ablation isolates abstraction from format and confirms abstraction alone drives a 1.1% average gain.

5. **Negative-transfer taxonomy.** The paper catalogs three failure modes of cross-domain memory: domain-mismatched anchoring (superficially similar but irrelevant memories), false validation confidence (verification memories encouraging superficial checks), and misapplied best-practice transfer (indiscriminately applying successful patterns). This gives designers a checklist of risks to defend against.

6. **Retrieval-method finding.** LLM reranking and task-adaptive memory rewriting underperform plain cosine-similarity retrieval on embeddings in the dynamic multi-step agent setting -- a counterintuitive result suggesting retrieval methods tuned for static QA do not transfer to agentic use.

---

## Key Findings

### Core performance results (Pass@3, six coding benchmarks)

| Setting | GPT-5-mini | DeepSeek V3.2 | Qwen3-Coder-480B |
|--------|-----------|---------------|------------------|
| Zero-shot baseline | -- | -- | -- |
| **MTL (Insight)** | **+3.7%** avg, up to +8.3% | **+2.6%** avg | **+1.8%** avg |

### Method comparison (subset of benchmarks)

| Method | Pass@3 | Memory pool size |
|--------|--------|------------------|
| ReasoningBank | 0.601 | 97 |
| AgentKB | 0.613 | 5,899 |
| **MTL (Insight)** | **0.630** | **431** |

### Qualitative breakdown of transferred knowledge

- Iterative workflow discipline: **15.0%**
- Test-driven verification: **14.5%**
- Anti-pattern avoidance: **10.4%**
- Input validation & robustness: 8.5%
- API & interface compliance: 8.1%
- Interaction protocol adherence: 7.8%
- Environmental adaptation: 6.4%
- File and syntax management: 5.5%
- Repository exploration tactics: 5.5%
- Algorithmic strategy transfer: only **5.5%** -- the paper's central "meta > code" claim

### Other findings

- **Abstraction ranking:** Insight > Summary > Workflow > Trajectory (monotonic with abstraction level).
- **Task-agnostic vs task-specific Insight:** task-agnostic wins by 1.1% avg, isolating abstraction as the driver.
- **Scaling:** MTL performance scales positively with memory-pool size and with number of source domains (up to 9 tested).
- **Cross-model transfer:** memories generated by GPT-5-mini still help DeepSeek V3.2 and Qwen3-Coder, though self-generated memories remain best -- meta-knowledge is largely model-agnostic but has mild model-specific bias.
- **Retrieval:** simple cosine similarity on OpenAI `text-embedding-3-small` with top-3 retrieval beats LLM reranking and adaptive rewriting.

---

## Suggestions & Future Directions

1. **Advanced domain routing.** Build retrievers that recognize when a memory is from a mismatched domain and should be filtered out, mitigating domain-mismatched anchoring.
2. **Step-wise memory adaptation.** Rather than injecting memories once at the system prompt, adaptively refine or swap memories as the multi-step trajectory unfolds.
3. **Safer memory utilization under negative transfer.** Design guardrails so memories that suggest unsafe shortcuts or insecure patterns are downweighted.
4. **Retrieval for agentic settings.** Develop retrieval techniques tailored to dynamic, multi-step agent contexts, since static-context reranking methods did not generalize.
5. **Scaling memory diversity.** Extend beyond the 9 domains tested to understand saturation behavior of cross-domain memory pools.
6. **Generalization to non-coding agents.** The meta-knowledge hypothesis (procedural, abstraction-sensitive) is a natural candidate to test in other agentic settings (research, web navigation, tool use).

---

## Authors & Institutions

Kangsan Kim (KAIST), Minki Kang (KAIST), Taeil Kim (KAIST), Yanlai Yang (NYU), Mengye Ren (NYU, equal advising), Sung Ju Hwang (KAIST & DeepAuto.ai, equal advising).
