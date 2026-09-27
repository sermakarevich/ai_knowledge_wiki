# From Passive Retrieval to Active Memory Navigation: Learning to Use Memory as a Structured Action Space

**Paper:** [From Passive Retrieval to Active Memory Navigation (Xu, Sun, Liu, Zhou, Qiao, Ma, Tang, Wang, Jiang, Jiang, 2026)](https://arxiv.org/abs/2607.05794)

## Human Readable TL;DR

Imagine a personal assistant that keeps a giant filing cabinet of everything you've ever told it, but every time you ask a question, a clerk grabs one random folder and hands it over without checking if it actually answers your question. That's how most AI memory systems work today -- passive retrieval. This paper's system, NapMem, instead gives the assistant its own set of hands: it can search the filing cabinet, pull specific documents, or read a summary sheet on top, deciding for itself what to check before answering. It's trained (via trial-and-reward practice) to know when digging deeper is worth it and when to stop. The result answers personal questions more accurately, without becoming slower or forgetting how to reason about normal, memory-free questions.

## TL;DR

NapMem reframes long-term user memory as a structured action space rather than a passively retrieved context blob. It organizes user history into a four-level "memory pyramid" (raw conversations, memory records, topic tracks, user profile) linked by provenance relations, and exposes each level through five memory tools (search/get for conversations and records, plus file-reading for topic tracks/profile). A Qwen3.5-9B agent is trained with GRPO reinforcement learning over multi-turn tool-use trajectories, using a terminal reward combining format validity, answer correctness, and memory-tool usage. Across PersonaMem-v2, LongMemEval, and LoCoMo, the RL-trained 9B agent beats five memory-system baselines (Mem0, Zep, MemOS, MemoryOS, AgeMem) and even untrained 122B/397B NapMem variants, while barely touching memory on non-memory tasks (GPQA-Diamond, BFCL-v3, V*Bench) and using less storage and fewer completion tokens than most baselines.

---

## Problem & Motivation

Long-term user memory is becoming essential for personalized conversational agents across personal assistance, education, and workplace-productivity settings that span many sessions. The challenge: user information is multi-faceted, and different future queries impose heterogeneous memory requirements, so a single fixed memory representation or access strategy generalizes poorly.

Existing work improves memory along two axes -- **construction** (richer storage structures, finer-grained categories, agentic memory-entry management, e.g. Mem0, Zep, MemOS) and **retrieval** (reflective retrieval, personalized queries, reranking). Both treat memory access as a system-level, passive retrieval function or a fixed pipeline that hands the agent pre-selected context, leaving it no control over how memory gets used. The paper's motivating example: asked "Which device did I get first, the Samsung Galaxy S22 or the Dell XPS 13?", a passive-retrieval system hands over "The user has Dell XPS 13 and Samsung Galaxy S22" -- insufficient to answer, causing failure. An agent that can actively search conversation history for order dates ("Dell XPS 13... arrived Feb 25", "Galaxy S22... got on Feb 20") answers correctly. The core claim: long-term memory use should move from system-level passive retrieval to **agent-native memory navigation**.

---

## Main Original Ideas

1. **Active memory navigation as a reframing.** Long-term memory is formulated as a structured action space the agent learns to use, rather than context passively injected by the system.
2. **The memory pyramid.** Four linked levels -- raw conversations, memory records (typed: fact/event/instruction/preference), topic tracks, user profile -- connected by provenance relations, built incrementally bottom-up and navigable both top-down and bottom-up.
3. **Five memory tools as the action space.** `get_conversations`, `search_conversations` (hybrid RRF search), `get_records`, `search_records` (hybrid RRF search), `read_files` (topic-track/profile files) -- giving the agent explicit, sequential control over which granularity to consult.
4. **GRPO-trained navigation policy.** A Qwen3.5-9B agent trained with Group Relative Policy Optimization over multi-turn tool trajectories, using only a terminal (trajectory-level) reward that jointly scores format validity, answer correctness, and memory-tool usage -- so tool-use decisions and final answers are optimized against the same outcome.
5. **Framework name / naming note.** NapMem = "Navigate over Pyramid Memory." Appendix C refers to the trained policy once as "PyraNav," trained with multi-turn GRPO via the `verl` framework -- likely an internal alias for the same system.

---

## Methodology

**Memory pyramid construction** is incremental and per-user: new sessions append to the raw-conversation layer, which triggers extraction/reconciliation of memory records (store/skip/update/merge against existing records via hybrid retrieval), which in turn can trigger topic-track updates (agent decides to update, merge, or start a track; max 20 tracks maintained) and eventually a user-profile refresh (revised under a length budget, invalid writes rolled back). Lower two layers are stored as indexed JSONL; upper two layers as directly readable Markdown files.

**Navigation as sequential decision-making:** given query `q` and pyramid `M`, at each step the agent either calls a memory tool or terminates and answers: `a_t ~ π_θ(· | q, M, a_<t, o_<t)`, producing trajectory `τ = (a_1, o_1, ..., a_k, o_k, y)`.

**Reward rubric** (rule-based, three binary criteria -- format `F`, correctness `C`, memory-tool usage `U`):

| F | C | U | Reward |
|---|---|---|---|
| 0 | - | - | -1 |
| 1 | 1 | 1 | **+1** |
| 1 | 1 | 0 | 0 |
| 1 | 0 | 1 | -0.5 |
| 1 | 0 | 0 | -1 |

Optimized with clipped GRPO: group-relative advantage `A_i = r_i - mean(r_j for j in G)`, applied uniformly across all output tokens (including tool-call tokens) with a KL penalty against the reference policy.

**RL setup:** base model Qwen3.5-9B, batch size 8, rollout group size 4, LR 1e-6, max 5 assistant turns, KL coeff 0.001, 5 epochs, bfloat16, on NVIDIA H20. Embeddings via Qwen3-Embedding-0.6B; search tools use hybrid RRF (k=60) over keyword + vector retrieval. Inference budget: at most 4 tool-call steps per query; each retrieval returns up to 5 items.

---

## Key Findings

**Table 1 -- Memory-intensive tasks** (LoCoMo F1/L-J, LongMemEval F1/L-J, PersonaMem-v2 Acc., Avg.):

| Method | LoCoMo F1 | LoCoMo L-J | LongMemEval F1 | LongMemEval L-J | PersonaMem-v2 | **Avg.** |
|---|---|---|---|---|---|---|
| Mem0 | 41.19 | 60.86 | 53.86 | 78.00 | 38.89 | 59.25 |
| Zep | 36.09 | 52.21 | 52.61 | 73.33 | 36.33 | 53.96 |
| MemOS | 35.22 | 55.82 | 39.16 | 54.33 | 37.58 | 49.24 |
| MemoryOS | 31.40 | 44.28 | 22.68 | 23.67 | 35.82 | 34.59 |
| AgeMem | 38.00 | 45.02 | 37.83 | 51.33 | 24.19 | 40.18 |
| NapMem-122B (no RL) | 35.39 | 51.69 | 48.86 | 70.00 | 41.38 | 54.36 |
| NapMem-397B (no RL) | 38.31 | 54.42 | 53.85 | 78.33 | 46.10 | 59.85 |
| **NapMem-9B w/ RL** | **41.28** | 59.92 | **57.41** | **80.33** | **47.97** | **62.74** |

NapMem-9B w/ RL posts the best average (62.74) despite being far smaller than the 122B/397B untrained variants, best on LongMemEval and PersonaMem-v2, and best/near-best on LoCoMo.

**Table 2 -- Generalization to non-memory tasks** (GPQA-Diamond, BFCL-v3, V*Bench): NapMem-9B w/ RL is competitive-to-improved vs. the untouched base model (e.g. GPQA-D accuracy 53.03 → 57.58; V*Bench answer acc. 84.82 → 91.10), and RL sharply cuts *unnecessary* memory-tool calls on GPQA-D (34.51% w/o RL → 6.90% w/ RL), while keeping memory calls at 0% on BFCL-v3 and V*Bench -- RL calibrates *when* to use memory, not just how often.

**Table 3 -- Storage footprint (GiB):** NapMem totals 4.83 GiB across all three benchmarks vs. 10.44 (Mem0), 23.10 (MemOS), 14.10 (Zep), 6.68 (MemoryOS); only AgeMem is smaller (2.99) but scores far worse on task performance -- storage size alone doesn't predict quality.

**Figure 3 (efficiency):** NapMem clusters at low latency / low completion-token counts vs. baselines on 100 PersonaMem-v2 samples -- it stops once sufficient evidence is gathered instead of reasoning over a large passively-retrieved context.

**Table 4 -- Ablations** (Avg. score): Full NapMem 62.74 vs. w/o RL 48.39, w/o navigation (passive retrieval) 54.08, records-only tools 44.93, w/o upper levels (no topic tracks/profile) 54.11 -- RL training, active navigation, and the full multi-level pyramid each contribute independently.

**Table 5 -- Tool-use behavior:** RL cuts tool calls per query (3.97 → 2.15) while raising evidence-hit ratio (20.66% → 34.92%) at similar multi-level navigation rate (~80%) -- the trained policy learns to stop early once it has enough evidence, not to search less broadly.

**Table 8 (judge validation):** Claude-Opus-4.6 as LLM judge vs. human-majority labels on 100 open-ended QA items: accuracy 99.0%, F1 99.0%, Cohen's κ 0.980.

---

## Suggestions & Future Directions

1. Evaluate on more realistic, open-ended personalization scenarios beyond existing long-term-memory benchmarks.
2. Address privacy and forgetting/deletion requirements in user-memory systems, which the current work does not tackle.
3. Run broader scaling studies of how model size affects preferred memory-access strategies (the paper observes 9B models favor record-level tools first while 122B/397B favor file-reading first, but doesn't fully explain why).
4. From the failure-case analysis (Appendix D): future navigation policies should better distinguish one-off *event* evidence from stable *preference* evidence, to avoid over-generalizing a single occurrence into a durable personal trait.

---

## Authors & Institutions

Yue Xu (Qwen Large Model Application Team, Alibaba; ShanghaiTech University), Yutao Sun (Zhejiang University), Yihao Liu (Peking University), Mengyu Zhou (Qwen Large Model Application Team, Alibaba -- corresponding author), Jiayi Qiao (National University of Singapore), Lu Ma (Alibaba), Kai Tang (Alibaba), Wenjie Wang (ShanghaiTech University -- corresponding author), Xiaoxi Jiang (Alibaba), Guanjun Jiang (Alibaba).
