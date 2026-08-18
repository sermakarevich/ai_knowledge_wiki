# Zero-Mem: Zero-Token Memory Operations for LLM Agents

**Paper:** [Zero-Mem: Zero-Token Memory Operations for LLM Agents (Xiao et al., 2026)](https://arxiv.org/abs/2607.29377)
**Wiki:** [[index]] | **Digest:** [[digest]]

## Human Readable TL;DR

Imagine an assistant that has to remember everything you've ever told it -- but instead of constantly re-reading and re-summarizing your entire conversation history (which costs time and money), it keeps your original messages untouched and just builds two simple, free-to-use "maps" over them: one map of who/what is connected to what (like a contacts web), and one map of when things happened (like a timeline with zoom levels). When you ask a question, the system checks both maps, pulls out the most relevant original messages, double-checks them against each other, and only then hands them to the AI to write the final answer. Because the map-building and map-searching steps never call an AI model themselves, this "remembering" step is essentially free and fast, yet it still finds better answers than systems that do use AI to build and search their memory.

## TL;DR

Zero-Mem is an LLM-agent memory framework that eliminates every LLM call and LLM token from memory construction, organization, routing, retrieval, evidence closure, and calibration -- the only LLM call in the whole pipeline is the final-QA reader. It achieves this by keeping raw interaction traces as the sole source of record and deriving two non-generative structural views over them (an entity-context co-occurrence graph and a four-level temporal hierarchy), coordinated per query by a deterministic routing profile, fused via Personalized PageRank and coarse-to-fine hierarchical search, and refined by deterministic evidence/answer calibration. On LoCoMo and HotpotQA, across two backbone LLMs, Zero-Mem beats the strongest baseline (GAM) by 4.9-5.5 F1 points while consuming zero memory-operation tokens and cutting memory-operation latency by 57.6% versus the fastest baseline.

---

## Problem & Motivation

LLM agents accumulate growing interaction histories, and their reliability hinges on recovering the *right* evidence tied to the correct entity, session, and temporal state -- not simply storing more context. Existing approaches fall into two camps, both flawed: **generative memory** (LLM-generated summaries, compressed notes, graph indexes) turns every memory update into a recurring generative workload, and omitted details, merged subjects, or blurred temporal updates can weaken traceability back to the original interaction. **Raw retrieval** (flat lexical/dense search over unstructured traces) preserves source evidence but confuses semantically similar traces from different users/sessions/times and can miss evidence distributed across multiple interactions. Recent systems (SimpleMem, LightMem) reduce but do not eliminate LLM dependence in the memory pipeline. Zero-Mem's motivating question: can an agent memory system eliminate LLM calls from every operation outside final question answering, while retaining structured access beyond flat similarity retrieval?

---

## Main Original Ideas

1. **Zero-token memory operating regime** -- The paper defines and targets a new regime in which construction, organization, routing, retrieval, evidence closure, and both pre- and post-reader calibration use zero LLM calls and zero LLM input/output tokens. Only the final-QA reader invokes an LLM; encoder computation (NER, embeddings) is accounted for separately as non-generative processing.

2. **Entity-context graph** -- A relational graph G = (V_d ∪ V_e, E_de ∪ E_dd) built with a non-generative NER model (e.g., spaCy): context nodes and entity nodes linked by weighted co-occurrence edges, plus adjacency edges between neighboring context units. It records only *observed* co-occurrence and adjacency, never generated semantic triples or inferred relations.

3. **Temporal hierarchy** -- Traces are organized at four granularities, T(H) = U_turn ∪ U_window ∪ U_episode ∪ U_local: turns (atomic utterances), windows (short-range context), episodes (coherent event regions via semantic continuity and session boundaries), and local spans (immediate neighborhood of a candidate turn). All units inherit provenance from the raw traces they derive from.

4. **Query-conditioned dual-view routing and retrieval** -- A lightweight, gold-answer-free query profile phi(q) = {subject, keywords, answer-type, temporal-cues, boundary} drives a deterministic binary route (relational vs. local) that sets a shared weight rho / 1-rho between the graph and hierarchical views. Both views always run in full; graph retrieval uses entity alignment plus Personalized PageRank propagation, hierarchical retrieval is coarse-to-fine (episode -> window -> turn -> local span); their rankings are normalized and fused, then closed with graph bridges and local neighbors into a Closed Evidence Set.

5. **Deterministic evidence and answer calibration** -- After closure, evidence is filtered against hard provenance/boundary constraints and ranked by profile compatibility to produce R(q). After the reader emits an initial answer, it is checked against evidence-extracted candidates and either preserved (if supported and well-formed) or corrected via evidence-preserving normalization, extractive shortening, or list pruning -- never by inventing new content.

---

## Key Findings

**LoCoMo -- average F1/BLEU-1, Zero-Mem vs. strongest baseline (GAM):**

| Backbone | Method | F1 | BLEU-1 |
|:---|:---|---:|---:|
| GPT-4o-mini | GAM | 53.75 | 47.51 |
| GPT-4o-mini | **Zero-Mem** | **59.15** | **52.96** |
| Qwen2.5-14B | GAM | 52.70 | 46.55 |
| Qwen2.5-14B | **Zero-Mem** | **57.57** | **51.41** |

- **Efficiency:** In the unified efficiency comparison, Zero-Mem consumes exactly 0 memory-operation tokens (versus 28,570,674 for GAM and 877,086 for LightMem, the most token-efficient baseline) -- a 100% token reduction -- while still improving F1/BLEU-1 over GAM by 10.0%/11.5%. Total memory-operation time is 334.77s (0.22s/query), a 57.6% latency reduction relative to LightMem, the fastest baseline (788.76s / 0.51s per query).
- **HotpotQA:** Zero-Mem achieves the highest F1 across all six backbone/context-length combinations (56K/224K/448K tokens, GPT-4o-mini and Qwen2.5-14B), e.g. 72.07 F1 at 56K and 65.04 F1 at 448K with GPT-4o-mini, averaging +5.52 F1 over the strongest baseline (GAM) as context length scales up.
- **Ablations (HotpotQA, 56K, GPT-4o-mini):** the full model (72.07 F1/69.66 BLEU-1) drops to 62.50/59.90 with graph-view only and to 54.88/51.40 with hierarchical-view only, confirming the two views are complementary rather than redundant. Removing evidence closure lowers scores to 67.90/65.43, and removing evidence calibration lowers them to 70.13/66.45 -- each component contributes independently.
- **Retrieval budget (LoCoMo, GPT-4o-mini):** average F1/BLEU-1 rises from 52.59/46.79 at Top-1 to 59.15/52.96 at Top-5, peaking near Top-10; the paper's chosen Top-5 setting trails the Top-10 peak by only 0.65 F1 and 0.83 BLEU-1.

---

## Suggestions & Future Directions

1. **Code release** -- The wiki notes that code will be released post peer-review at https://github.com/TheMoon0815/Zero-mem.
2. **No explicit future-work section surfaced in the wiki** -- The wiki pages summarize the paper's conclusion (restating the three contributions and the zero-token regime) but do not present a dedicated limitations or future-work discussion beyond that. Being honest rather than inventing one: the closest thing to a caveat visible in the results is that Zero-Mem is not uniformly first on every sub-metric -- with GPT-4o-mini it remains merely competitive with GAM on multi-hop questions, and CompassMem occasionally edges ahead on isolated multi-hop cells in the LoCoMo table -- suggesting multi-hop reasoning under the graph view is an area where the margin over baselines is narrowest.

---

## Authors & Institutions

Yilin Xiao, Zhehan Zhu, Yujing Zhang, Jin Chen, Zijin Hong, Luyao Zhuang, Qinggang Zhang, Shengyuan Chen, Xiaocao Ouyang, Lingfei Ren, Xiao Huang -- The Hong Kong Polytechnic University; School of Computing and Artificial Intelligence, Southwestern University of Finance and Economics; School of Artificial Intelligence, Jilin University.

## Figures

![Comparison of agent-memory operating regimes](wiki/images/fig1-memory-operating-regimes.png)
![Zero-Mem architecture overview](wiki/images/fig2-zero-mem-architecture.png)
