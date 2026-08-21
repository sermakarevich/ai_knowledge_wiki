> [[index|Wiki]] | [[summary|Summary]]

# GraphPlanner — Digest

The whole paper at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-problem-and-preliminaries|Problem, Motivation & Preliminaries]]

**In one sentence:** Routing among multi-agent LLMs should be generalized from one-shot or sequential model selection into an agentic, memory-augmented workflow-generation problem — where the router jointly picks an *agent role* and an *LLM backbone* at each step, modeled as a Markov Decision Process (MDP) whose state is enriched by a heterogeneous graph of historical and workflow memories (GARNet), and optimized end-to-end with reinforcement learning.

- **Problem raised:** most existing LLM routers are confined to simplified/static settings; agentic LLM settings — task planning, multi-round cooperation among heterogeneous agents, and memory utilization — require a new routing paradigm. The paper's guiding question is: *"How can we extend routers to agentic LLM settings?"*
- **Two existing router families (Table 1):** single-round routers (RouterDC, GraphRouter) make one-shot assignments from query embeddings/classifiers and cannot reason, decompose, or coordinate; multi-round routers (R2-Reasoner, Router-R1) interleave reasoning and routing over multiple calls but treat each call as independent, causing redundant calls, context conflicts, and under-use of complementary strengths.
- **Three concrete challenges of agentic routing:** (1) relations among queries, responses, and LLM candidates are highly diverse and complex (queries may branch, responses interact, models contribute complementary but sometimes conflicting information); (2) **deferred rewards** — early misallocation can cascade into redundant calls or degraded downstream reasoning, creating a hard credit-assignment problem; (3) **historical memories** from past multi-agent workflows (successful collaboration patterns, error modes, efficient division of labor) are rarely exploited systematically.
- **GraphPlanner core design:** casts agentic routing-workflow generation as *graph generation within an MDP*; at each step it jointly selects the LLM backbone and the agent role — defined as **Planner, Executor, Summarizer**; a heterogeneous graph **GARNet** captures memories among LLM agents, queries, and responses to build richer state representations; **PPO** (Proximal Policy Optimization) is used to jointly optimize task-specific performance of final answers and computational cost.
- **Evaluation:** two phases across **14 tasks spanning 6 domains** — Phase 1 optimizes agentic routing within existing workflows (+3.8% average accuracy), Phase 2 generates workflows for complex agentic tasks (+9.3% average accuracy).
- **Result magnitudes:** outperforms strong single- and multi-round routers, improving accuracy by up to **9.3%** while reducing GPU cost from **186.26 GiB to 1.04 GiB**, staying on the Pareto frontier.
- **Generalization:** **78% average accuracy on unseen tasks** (20–40% higher than previous routers) and robust handling of unseen LLMs without additional fine-tuning.
- **Memory modes:** by modeling historical memories alongside current workflow memories through GARNet, GraphPlanner supports both **inductive** (greater efficiency) and **transductive** (stronger performance at higher cost) inference.

## 2. [[wiki/02-graphplanner-method|GraphPlanner Method]]

**In one sentence:** GraphPlanner casts agentic LLM routing as an MDP over a heterogeneous graph that unifies a per-step workflow memory graph and an end-of-episode historical memory graph through shared (LLM, role) hub nodes, and trains the resulting graph policy network (GARNet) end-to-end with PPO to jointly pick the agent role and LLM backbone at each step.

- At each step the router emits an action `a_t = (α_t, m_t)` — a pair of agent role (planner / executor / summarizer) and LLM backbone `m_t ∈ {1..K}` — giving `|A| = 3K` possible actions, guided by a dynamic validity mask `M_t ⊆ A`.
- The MDP `(S, A, T, r, γ)` defines the state as the current query under resolution (`s_t = q_t`), transitions as updates of the workflow memory `(s_{t+1}, o_t) = T(s_t, a_t)`, and a reward that balances task utility against routing cost.
- Reward: `r_t = U(ŷ, y*) − αC(a_t)` at the terminal step `t = T`, and `r_t = −αC(a_t)` otherwise, where `U` is a task-specific utility (accuracy, BLEU, MRR), `C(a_t)` the computational cost, `α > 0` the cost–utility trade-off.
- The objective is `max_π E_{q∼Q} [Σ_{t=0}^{T} γ^t r(s_t, a_t)]`, `a_t ~ π(s_t)`, with episodes terminating when the root query is resolved.
- GARNet, a heterogeneous GNN, parameterizes `π(a_t | s_t)` over `G_t = G_workflow ∪ G_history`; node types are query nodes (`x_q`, Longformer embeddings), response nodes (`x_r`), and role hub nodes `x_m = [e_role; U; C]`.
- One fixed set of role hub nodes, one per (LLM, role) pair, is shared across both graphs and all rounds — a bridge for message passing and a mechanism for aggregating current workflow, historical signals, and role-specific utility–cost profiles without redundant nodes.
- A nested dual-graph encoding computes `H(his) = GARNet_θhis(G_history)` and injects it into the workflow encoder `H(loc) = GARNet_θloc(G_workflow; H(his))`; actions are scored as `score_j = z_t^⊤ h_{m,j}` with `z_t = f_trans(s_t)`, masked by `M_t` and softmax-normalized.
- Training uses PPO (actor–critic RL); the trailing Phase 1/Phase 2 tables show GraphPlanner reaching 58.60% / 60.40% average accuracy (Phase 1) and 63.6% (Phase 2, +23.2% ΔAcc) at lower cost than all router baselines.

## 3. [[wiki/03-experiments-and-results|Experiments, Results & Conclusion]]

**In one sentence:** Across 14 tasks in 6 domains, GraphPlanner attains SOTA in 4 of 5 scenarios in both evaluation phases (minimum +3.8% in Phase 1, +9.3% in Phase 2 over the best baseline), generalizes zero-shot to unseen tasks (78% avg Acc vs. 38–58% for baselines) and unseen LLMs, and forms the Pareto frontier on accuracy vs. cost — all with the lowest GPU training compute (1.04 GiB).

- Phase 1: GraphPlanner achieves SOTA in 4 of 5 tasks with the highest overall average accuracy, a minimum +3.8% improvement over the strongest baseline.
- Phase 2: SOTA in 4 of 5 tasks, +9.3% overall accuracy gain over the best baseline; its Phase-2 average beats the best Phase-1 results by ~5%, showing that generating query-specific workflows outperforms optimizing within fixed workflows.
- Gains concentrate in reasoning tasks: +5.0% on Math, +4.0% on Code, versus only ~1.0% on recognition-focused tasks.
- Lowest training GPU compute of all routers: 1.04 GiB vs. GraphRouter 1.54 GiB, RouterDC 10.56 GiB, Router-R1 186.26 GiB; token usage 182.45k (Router-R1 150.36k), with the most LLM training calls (4.25 vs. ~1).
- Zero-shot generalization on unseen datasets (Phase 2): 60% LogicGrid, 92% MGSM, 82% CommonGen, 78% average — vs. GraphRouter 12/68/57 avg 46%, RouterDC 32/82/60 avg 58%, Router-R1 24/40/48 avg 38%.
- Three LLMs (Mistral-Nemo 12b, Mixtral 8×7b, Mixtral 8×22b) were deliberately withheld from training and used only at evaluation; GraphPlanner still dominates GraphRouter and Router-R1 across all five domains, confirming zero-shot transfer to unseen backbones.
- Ablations: removing history (w/o History) causes the biggest drop; Hetero-Graph > Homo-Graph, yet both remain clearly inferior to the full GARNet, which models not only who interacts but how interactions evolve over time.
- Transductive inference (reusing stored training-time interactions) achieves slightly higher accuracy than inductive inference; the inductive setting is more resource-efficient and still consistently beats the best multi-round router, Router-R1.

## 4. [[wiki/04-related-work-and-implementation|Related Work & Implementation Details]]

**In one sentence:** GraphPlanner positions itself as an *agentic* router that jointly selects heterogeneous LLM agents (role *and* backbone) and composes per-query workflow graphs, differentiating from single-round/RL backbone-only routers and homogeneous MAS, and is reproduced with a GARNet-parameterized PPO policy trained on a single NVIDIA A6000 across 6 domains, 14 tasks, and 12 LLM backbones.

- MAS frameworks (AutoGen, LLM-Debate, AgentVerse) and workflow-generators (ADAS, AFlow, AgentSquare) use manually designed protocols or assume homogeneous agent capabilities; GraphPlanner **automatically selects heterogeneous LLM agents** and composes workflows per query.
- Single-round routers (RouterKNN, RouterMLP, RouterSVM, RouterDC, GraphRouter) are efficient but lack sequential reasoning; multi-round/RL routers (Prompt LLM, Router-KNN-MR, R2-Reasoner, Router-R1) do backbone selection only — GraphPlanner jointly picks agent *and* backbone.
- Policy trained with **PPO** (Schulman et al., 2017), both policy and value functions parameterized by **GARNet** via `torch_scatter` for graph message passing and meta-key aggregation.
- Hyperparameters: γ = 0.99, ϵ = 0.2, k = 4 epochs/update, hidden dim 32, candidate embedding dim 1536, state embedding dim 768, Adam LR 3×10⁻⁴ (doubled for value), gradient clip norm 0.5, BF16, gradient checkpointing, multi-threaded parallel rollouts.
- Training capped at **1000 episodes** with early stopping when **policy entropy drops below a threshold**; evaluation uses **greedy decoding**, best model by running reward.
- All experiments on a **single NVIDIA A6000 GPU**.
- Datasets: 6 domains / 14 tasks (incl. held-out out-of-domain: LogicGrid, MGSM, CommonGen); 12 LLMs across Small (7–12B, $0.20–0.30/M tokens), Medium (49–56B, $0.60–0.90/M tokens), Large (70–176B, $0.90–1.20/M tokens).

## 5. [[wiki/05-additional-ablations-and-generalization|Additional Ablations & Generalization]]

**In one sentence:** A battery of extra experiments (new roles, alternative encoders, LLM-based history processing, an unseen dataset, and cost analysis) consistently shows GraphPlanner improving or matching baselines everywhere while training in 120 minutes (vs. 300–406 min) and inferring at 1.2 s/query (the fastest of all methods).

- Adding Thinker and Verifier roles always helps: New-role-train reaches 70.5% / 78.5% / 79.0% / 39.5% / 52.5% (Math/Code/CS/WK/Popular), above the 3-role baseline (67.0/76.0/78.0/38.0/52.0) and also above zero-shot (68.5/77.0/78.3/38.5/52.2) and few-shot (69.6/77.8/78.8/39.0/52.4) settings with the new roles.
- On the unseen AIME dataset (Phase-2, 2016–2025), GraphPlanner scores 14.7% accuracy — almost twice the best baseline (RouterDC at 7.56%), with all other single-round and multi-round routers below ~8%.
- GARNet beats both alternative encoders across all five scenarios: GAT (0.643/0.739/0.756/0.358/0.493) and GraphTransformer (0.647/0.743/0.759/0.353/0.491) are 2.8%–6.1% and 2.3%–7.6% behind GraphPlanner (0.670/0.760/0.780/0.380/0.520) respectively.
- LLM-based history processing barely helps: History-summary (Router-R1 + summaries, 32,768-token limit) gets 0.51/0.62/0.75/0.14/0.36 and History-retrieval (top K=5 retrieved histories) gets 0.46/0.62/0.73/0.12/0.39, while GraphPlanner (0.67/0.76/0.78/0.38/0.52) outperforms the best history-based method by 31.4% (Math), 22.6% (Code), 4.0% (CS), 171.4% (WK), and 33.3% (Popular).
- GraphPlanner has the lowest total training time of any Phase-2 method: 120 min (RL-based data collection, no up-front data sweep) vs. R2-Reasoner 360 min, Router-R1 300 min, and supervised routers at 400.4–406 min (dominated by 395 min of data collecting).
- GraphPlanner also has the lowest inference latency: 1.2 s/query, versus 2.1–2.4 s for single-round routers and 3.6–10.5 s for multi-round routers.
- GraphPlanner's zero-shot generalization to new roles works without role-specific training (New-role-zero-shot beats the original on all five domains at 68.5/77.0/78.3/38.5/52.2), and few-shot with just 50 historical interactions (1% of training queries) lifts performance further to 69.6/77.8/78.8/39.0/52.4.
- Appendix J's illustrative examples (Figure 6, Tables 16–18) show GraphPlanner adapting its workflow topology to task type: a direct executor-only path for natural QA, parallel decompose-execute-summarize for math, and recursively nested (two-level) planning for code.

## 6. [[wiki/06-prompt-templates-and-examples|Prompt Templates & Worked Examples]]

**In one sentence:** Appendix K exposes the literal prompt templates behind GraphPlanner's five agent roles (Planner, Executor, Summarizer, plus the appendix-introduced Thinker and Verifier) and the agent/model role descriptions, alongside three fully traced Phase-2 workflows showing how the same prompt family drives single-step, flat multi-step, and nested hierarchical decompositions.

- Five prompt templates are given verbatim: **Planner** (sub-query decomposition), **Executor** (query answering), **Summarizer** (parent-query synthesis), **Thinker** (step-by-step draft reasoning), and **Verifier** (approve/revise gate) — each sharing a common Inputs/Instructions/Output format contract.
- All templates are context-passing templates: they thread `{QUERY}`, `{ROOT QUERY}`, `{PARENT QUERIES}`, `{SIBLING RESPONSES}` (and `{SUMMARY}`/`{CHILD ANSWERS}` for summarization) so any node in the workflow graph receives its position's context.
- The Planner is limited to 1–3 atomic, non-overlapping, self-contained sub-queries, with the number adapted to complexity and redundancy suppressed via sibling responses.
- The Thinker/Verifier pair forms a draft-then-verify sub-loop: the Thinker must produce numbered Reasoning Steps plus a Draft Answer "as [its] response will be verified by a Verifier Agent," and the Verifier must emit `[APPROVED/REVISED]`, Issues Found, and a Verified Response.
- Worked example 1 (math QA) shows the flat path: Planner (LLaMA-3.1-8B) → Q1/Q2 executors (Qwen2.5-7B, Gemma-2-9B) → executor merging subtotals (LLaMA-3.1-8B) → summarizer (LLaMA-3-70B-ChatQA) → final executor (Qwen2.5-14B) answering "$18".
- Worked example 2 (code task, `remove_digits`) shows nested planning: after Q1/Q2, a second Planner pass decomposes Q2 into Q2a (filtering logic, CodeGemma-7B: `not ch.isdigit()`) and Q2b (string construction, Qwen2.5-7B), then two summarizer passes and a final Qwen2.5-14B executor produce the Python function.
- Worked example 3 (natural QA, "Who painted the Mona Lisa?") shows the degenerate path: the planner selects an executor-only route — a single Qwen2.5-14B step, Acc 1, cost 85 — demonstrating adaptive skipping of decomposition.
- The appendix also fixes per-role duties (Tables 24–28) and a model catalog with pricing (Tables 29–40), plus a compact LLM-role→function table (Table 41); all models in the examples are routed at $0.10–$0.90 per million tokens.

## The argument in five moves

1. Existing LLM routers are stuck in single-round (no reasoning/coordination) or multi-round (no collaboration modeling) settings that don't fit real agentic multi-agent workflows.
2. GraphPlanner reframes routing as generating a workflow graph within an MDP: at each step, jointly pick an agent role and an LLM backbone.
3. GARNet, a heterogeneous GNN with shared (LLM, role) hub nodes, fuses per-query workflow memory with cross-episode historical memory into one policy input, trained end-to-end with PPO against a cost-aware reward.
4. Across 14 tasks / 6 domains, this beats every single-round and multi-round baseline on accuracy (up to +9.3%) while using far less GPU compute (1.04 GiB) and inference time (1.2 s/query), and forms the accuracy/cost Pareto frontier.
5. The design generalizes cleanly — to unseen tasks (78% zero-shot accuracy), unseen LLM backbones, and even unseen agent roles (Thinker/Verifier) without retraining — suggesting the graph-memory mechanism, not just the training data, is doing the generalization work.
