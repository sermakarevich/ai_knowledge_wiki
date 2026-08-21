> [[index|Wiki]] | [[summary|Summary]]

# AgentGL — Digest

The whole paper at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-motivation-and-related-work|Motivation and Related Work]]

**In one sentence:** LLM agentic reasoning operates only on unstructured text and ignores the topology of real-world Text-Attributed Graphs, so AgentGL formulates graph learning as an RL-optimized, topology-aware navigation process — the first RL-driven Agentic Graph Learning framework, outperforming GraphLLMs and GraphRAG by up to 17.5% (node classification) and 28.4% (link prediction).

- Central question: can the agentic learning paradigm (iterative retrieval, tool use, decision-making over external resources) be extended to graph-structured environments to enable dynamic, topology-aware reasoning — and how can such a system be built efficiently?
- Motivation: RAG and agentic search let LLMs move beyond static parametric knowledge, but they treat external information as flat text; in citation networks, social platforms, and commercial ecosystems, meaning arises from the interplay of text content and graph topology, which lexical-similarity agents cannot harness.
- Challenge C1 (topology-aware navigation): graph evidence is multi-scale — some clues live in tight local neighborhoods, others emerge only via broad structural patterns — so the agent must choose the next move in a combinatorial space while avoiding redundant or uninformative regions.
- Challenge C2 (long-horizon policy optimization): effective graph reasoning needs multi-step exploration, but ground-truth search trajectories are rarely available, making it hard to learn policies balancing exploration/exploitation/reasoning depth without drifting into irrelevant branches or wasteful tool calls.
- AgentGL's three mechanisms: (i) graph-native search tools — local neighborhood expansion, hop-constrained traversal, global evidence probing — for multi-scale exploration; (ii) search-constrained thinking, which biases the agent toward reflective inference before issuing further graph queries, balancing accuracy against efficiency; (iii) graph-conditioned curriculum RL that progressively raises topology-exploration difficulty, uses multi-faceted rewards, and enforces efficient tool use under limited budgets — learning without step-wise trajectory supervision.
- Position vs GraphLLMs: GraphGPT and GraphICL integrate LLMs with graph information via graph-guided prompting or instruction tuning, but rely on static graph context extracted once at inference time, preventing adaptive exploration.
- Position vs GraphRAG: these systems build large text-enriched knowledge graphs from corpora — costly to construct and lacking the native topological correlations of real TAGs.
- Results: across diverse TAG benchmarks and multiple LLM backbones, AgentGL delivers absolute accuracy improvements of up to 17.5% in node classification and 28.4% in link prediction over leading GraphLLM and GraphRAG baselines; code is public at github.com/sunyuanfu/AgentGL.

## 2. [[wiki/02-agentgl-method|The AgentGL Method]]

**In one sentence:** AgentGL trains an LLM agent to reason over a graph by casting it as a two-stage RL problem — learn to navigate the graph with a small set of graph-native search tools, then learn to stop searching when evidence is sufficient — with graph-conditioned curriculum scheduling to stabilize and accelerate convergence.

- **The RL objective.** The policy is trained with `J(θ) = E[ R(ŷ, y*) − β·D_KL(π_θ ∥ π_ref) ]`, where `π_θ` navigates the typed graph (TAG) via the toolset, `R` is the outcome-based reward, `β` is the KL coefficient, and `π_ref` is the reference policy.
- **Two complementary stages.** (1) *Graph-native policy bootstrapping* (§4.1) — learn to navigate the graph with search tools; (2) *search-efficiency optimization* (§4.2) — curb tool overuse during long-horizon reasoning. Both run under a graph-conditioned curriculum (GCCL, §4.3).
- **Four GNS tools** spanning local/global × structure/semantics: 1-hop neighborhood search (`τ₁HOP`), 2-hop neighborhood search (`τ₂HOP`), structure salience search (`τ_SS`, PPR-based), and graph dense search (`τ_DENSE`, semantic).
- **Composite rewards, two stages.** Stage 1: `R(τ) = r_FMT(τ) + r_ACC(ŷ, y) + r_COV(τ)` (format + accuracy + GNS coverage to explore all tools and prevent mode collapse). Stage 2: `R(τ) = r_FMT(τ) + r_ACC(ŷ, y) + r_depth(z)` (coverage dropped, depth added).
- **Critic-free RL optimizers.** AgentGL is instantiated with GRPO and REINFORCE++, explicitly avoiding the cost of building SFT-style supervision.
- **Reason–act–observe loop.** Rollout is a strict, machine-parseable interface: at most one retrieval action per round (a pool-specific query tag), evidence returned in documents tags; terminates on an `<answer>` or a budget `B`.
- **GCCL difficulty scoring.** Node classification uses an analytical score `S_NC(v)` from a Wilson lower bound on neighbor-label consistency plus degree; link prediction uses `S_LP(e)` from node-feature cosine similarity.
- **Curriculum progression.** Training progresses easy → hard: confident instances (structurally prominent hubs; high-similarity positives, low-similarity negatives) first, deferring ambiguous/heterophilous/high-similarity-negative cases.

## 3. [[wiki/03-experiments-results-and-conclusion|Experiments, Results, and Conclusion]]

**In one sentence:** AgentGL, an RL-trained agentic framework that interleaves graph search with LLM reasoning, beats GNN, GraphLLM, GraphRAG, and agentic-search baselines by 12.7–26.6% (node classification) and 22.4–28.4% (link prediction) across 7 datasets and two Qwen backbones, with ablations showing that every RL stage (GNSPB, MSO) and every reward component (rCOV, CDR, RTT, GCCL) is individually necessary for both accuracy and search efficiency.

- AgentGL (Qwen2.5-7B) outperforms baselines by an average of **12.7%** in-domain and **24.4%** zero-shot on node classification, and **26.3%** in-domain and **22.4%** zero-shot on link prediction.
- With Qwen2.5-3B, gains are **14.5%** (in-domain NC), **26.3%** (in-domain LP), **26.6%** (zero-shot NC), and **22.4%** (zero-shot LP).
- On Qwen7B link prediction, AgentGL is **47.4%** higher in-domain than GraphRAG and **23.2%** higher than GraphLLM, with margins of **35.4%** and **26.9%** under zero-shot transfer.
- The paper reports best-average gains across all backbones of up to **17.5%** on node classification and **28.4%** on link prediction over strong baselines (including GraphLLMs and GraphRAG).
- RL algorithm choice is task-dependent: GRPO beats R++ on NC by an average of **0.9%** (Qwen3B/7B average), while R++ beats GRPO on LP by **3.3%** on average.
- Scaling the backbone 3B→7B improves AgentGL by **9.0%** (in-domain NC), **11.8%** (zero-shot NC), **5.6%** (in-domain LP), and **8.7%** (zero-shot LP).
- The full two-stage method (GNSPB + MSO) reduces tool calls by about **17.5%** while improving NC accuracy by an average of **2.4%** over GNSPB alone; RTT+CDR together save ~**22%** of search cost with a **3%** accuracy gain; GCCL contributes ~**0.65%** accuracy and faster, more stable convergence.
- Ablations show no single component suffices: dropping rCOV causes valid-GNS counts to collapse to near zero (agent stops searching), dropping either CDR or RTT loses the Stage-2 efficiency gain, and MSO-only training degenerates to zero searches (worst results).

## 4. [[wiki/04-appendix-datasets-and-implementation|Appendix: Datasets, Implementation, and Case Study]]

**In one sentence:** This appendix adds the full experimental setup behind the main paper — the 7 TAG benchmarks and their splits, the conceptual distinction between AGL and GraphRAG, complete OpenRLHF/GRPO hyperparameters and GCCL reward engineering, and stability/K-sensitivity results with qualitative case studies.

- AgentGL is evaluated on 7 text-attributed graph (TAG) benchmarks across three domains (citation networks, e-commerce product graphs, social networks), on two tasks each: node classification (multi-class, original label space) and link prediction (binary).
- Data splits follow the GraphICL protocol with subsampling (3,000 train / 1,000 test nodes on OGB-Arxiv and OGB-Products); Reddit is converted from multimodal to TAG by dropping image attributes; all node texts are rewritten by Qwen2.5-72B-Instruct as a shared preprocessing step applied to AgentGL and all baselines.
- The paper draws a sharp line between AGL and GraphRAG: in GraphRAG the graph is an auxiliary index/scaffold for retrieving textual evidence to ground open-ended generation, whereas in AGL the graph is the primary problem instance and episodes terminate in a discrete task decision via graph-native operators.
- AgentGL is trained with OpenRLHF (GRPO-style RL): 16 rollouts per prompt, batch size 128, rollout batch 32, KL coefficient 0, learning rate 2e-6, max sequence length 1600, temperature 1.0, no warmup, on 8 NVIDIA H100-80G GPUs; reported as average accuracy over 2 rounds.
- Reward engineering is stage-specific: Stage 1 combines classification reward (1.5/-1.0/-0.5), format rewards (think/answer blocks, delimiter balance, leakage and verbosity penalties), and a search-coverage reward (+0.5 per distinct tool, capped at 2.0); Stage 2 swaps in a cognitive-density reward (+0.5/-0.2, 100-token segment threshold).
- Additional experiments show modest run-to-run variance (larger for 3B models than 7B) and K sensitivity: accuracy improves from K=1 to K=5 (68.9% OGB-Arxiv, 59.9% Amazon-Photo) and drops slightly at K=7, justifying the default K=5.
- Case studies show the agent forming a hypothesis from anchor text, verifying it with 1-hop/2-hop neighborhood and PageRank queries (NC, Amazon), and validating candidate edges via common 1-hop neighbor co-post structure (LP, Reddit), typically terminating early once evidence becomes self-consistent.

## The argument in five moves

1. Agentic LLM systems (RAG, agentic search) are great at flat text but blind to graph topology, even though many real corpora are Text-Attributed Graphs where meaning depends on structure, not just words.
2. Existing fixes are half-measures: GraphLLMs freeze the graph context once at inference time, and GraphRAG rebuilds a synthetic knowledge graph instead of using the native TAG.
3. AgentGL instead trains an LLM agent to navigate the *real* graph directly, using four search tools that cover local/global and structural/semantic axes of evidence.
4. Training is staged: first learn to search broadly (coverage reward, GCCL curriculum), then learn to search less by rewarding dense reasoning between searches and prompting retrospective stop-decisions.
5. Across 7 TAG benchmarks and two model sizes, this beats every baseline family — GNNs, GraphLLMs, GraphRAG, and standard agentic search — by double-digit margins.
6. Ablations confirm the design is not over-engineered: remove any single reward term or curriculum and either accuracy or search efficiency collapses.
7. The authors are explicit that this is TAG-only, Stage-2 training is delicate, and denser/multimodal graphs are untested — an early but rigorous instantiation of "graph learning as agentic RL," not a finished system.
