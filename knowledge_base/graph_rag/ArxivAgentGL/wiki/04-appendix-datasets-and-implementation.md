> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Datasets, Implementation, and Case Study

**In one sentence:** This appendix adds the full experimental setup behind the main paper — the 7 TAG benchmarks and their splits, the conceptual distinction between AGL and GraphRAG, complete OpenRLHF/GRPO hyperparameters and GCCL reward engineering, and stability/K-sensitivity results with qualitative case studies.

## Key points

- AgentGL is evaluated on 7 text-attributed graph (TAG) benchmarks across three domains (citation networks, e-commerce product graphs, social networks), on two tasks each: node classification (multi-class, original label space) and link prediction (binary).
- Data splits follow the GraphICL protocol with subsampling (3,000 train / 1,000 test nodes on OGB-Arxiv and OGB-Products); Reddit is converted from multimodal to TAG by dropping image attributes; all node texts are rewritten by Qwen2.5-72B-Instruct as a shared preprocessing step applied to AgentGL and all baselines.
- The paper draws a sharp line between AGL and GraphRAG: in GraphRAG the graph is an auxiliary index/scaffold for retrieving textual evidence to ground open-ended generation, whereas in AGL the graph is the primary problem instance and episodes terminate in a discrete task decision via graph-native operators.
- AgentGL is trained with OpenRLHF (GRPO-style RL): 16 rollouts per prompt, batch size 128, rollout batch 32, KL coefficient 0, learning rate 2e-6, max sequence length 1600, temperature 1.0, no warmup, on 8 NVIDIA H100-80G GPUs; reported as average accuracy over 2 rounds.
- Reward engineering is stage-specific: Stage 1 combines classification reward (1.5/-1.0/-0.5), format rewards (think/answer blocks, delimiter balance, leakage and verbosity penalties), and a search-coverage reward (+0.5 per distinct tool, capped at 2.0); Stage 2 swaps in a cognitive-density reward (+0.5/-0.2, 100-token segment threshold).
- Additional experiments show modest run-to-run variance (larger for 3B models than 7B) and K sensitivity: accuracy improves from K=1 to K=5 (68.9% OGB-Arxiv, 59.9% Amazon-Photo) and drops slightly at K=7, justifying the default K=5.
- Case studies show the agent forming a hypothesis from anchor text, verifying it with 1-hop/2-hop neighborhood and PageRank queries (NC, Amazon), and validating candidate edges via common 1-hop neighbor co-post structure (LP, Reddit), typically terminating early once evidence becomes self-consistent.

---

## Dataset Details

AgentGL is evaluated on 7 TAG benchmarks spanning three domains: citation networks, e-commerce product graphs, and social networks. Each node carries a natural language text (title/abstract for papers, product descriptions for items, post text for forums) as semantic grounding, while edges encode native relational structure (citations, co-purchase/co-view, interactions/co-posting). This forces the agent to jointly leverage topology (where to search) and semantics (what evidence says).

On each dataset two problems are considered: node classification (predict a node's category; uses the original multi-class label space) and link prediction (binary edge-existence decision). Splits follow the GraphICL default protocol with subsampling (3,000 training nodes on OGB-Arxiv and OGB-Products; 1,000 test nodes sampled for evaluation). Arxiv-2023 keeps the original split with test-split subsampling. Reddit, originally a multimodal benchmark, is converted to a TAG by removing image attributes and retaining textual fields. All node attributes are rewritten by Qwen2.5-72B-Instruct as a unified preprocessing step, used consistently for AgentGL and all baselines to control context length and ensure fair comparison.

| Domain | Dataset | #Nodes | #Edges | #Classes |
|---|---|---|---|---|
| Citation Network | OGB-Arxiv | 169,343 | 1,166,245 | 40 |
| Citation Network | PubMed | 19,717 | 44,338 | 3 |
| Citation Network | Arxiv-2023 | 46198 | 78548 | 40 |
| Amazon Products | OGB-Products (subset) | 54,025 | 74,420 | 47 |
| Amazon Products | Amazon-Photo | 48,362 | 500,939 | 12 |
| Amazon Products | Amazon-Computers | 87,229 | 721,107 | 10 |
| Social Network | Reddit | 15,894 | 566,160 | 20 |

#Classes correspond to the node classification label space; link prediction is treated as binary.

## GraphRAG vs. Agentic Graph Learning

GraphRAG-style methods extend classical RAG by incorporating graph structure into evidence selection and organization, typically for open-ended question answering or long-form generation. In that paradigm a graph (often a knowledge graph) serves as an index or scaffold that helps retrieve and aggregate textual evidence to ground an LLM's generation; the core objective is generation quality (factuality, faithfulness, relevance), and the graph is an auxiliary structure.

In contrast, Agentic Graph Learning (AGL) treats the graph as the primary problem instance rather than an external knowledge base. The goal is to solve graph learning/reasoning tasks whose correctness depends on structural signals (neighborhood composition, multi-hop dependencies, structural ranking), such as node classification, link prediction, and other graph-native queries. The agent interacts with the environment through graph-native operators that return nodes' text attributes, and the episode terminates with a discrete task decision instead of free-form generation. Trajectories are thus inherently graph-operational: the policy learns which structural context to acquire under a budget and when to stop, rather than retrieving text to write an answer. The paper notes that agentic GraphRAG work exists but is not equivalent to agentic graph learning since the two lines target fundamentally different objectives; it therefore adapts canonical GraphRAG baselines for graph reasoning and reports an empirical comparison in the experiments.

## Implementation Details

**Baselines.** GraphRAG baselines follow original settings where applicable: HippoRAG2 uses gpt-4o-mini for entity extraction and nv-embed-v2 for retrieval embeddings; LinearRAG uses spaCy for NER and all-mpnet-base-v2 for embeddings. The retrieval graph for GraphRAG baselines is built by subsampling 500 nodes from each TAG and indexing their original (unprocessed) node text; this subsampled graph is used solely for retrieval/augmentation and applied consistently. GraphCoT is categorized as a GraphRAG method (designed for knowledge-intensive QA with graph-augmented evidence retrieval). GraphLLM baselines keep their original prompting, graph-to-text serialization, and hyperparameters. GNN baselines adopt the multi-dataset training/transfer protocol of LLaGA. Standard agentic search baselines keep their original settings, with online search replaced by a constrained variant restricted to nodes in the input graph (to prevent web-based answer leakage); Search-R1 uses GRPO training.

**AgentGL training (OpenRLHF).** Graph-native search tools return at most 5 retrieved nodes per call (node classification), with node text appended as evidence. RL setup: 16 rollouts sampled per prompt, a single episode per update, zero warmup, total training batch size 128, rollout batch size 32, KL regularization coefficient 0, learning rate 2e-6, max sequence length 1600, sampling temperature 1.0. Text encoding uses the RoBERTa-Large encoder (all-roberta-large-v1). GCCL uses normal quantile z = 1.96 and η = 0.05. Hardware: one node with 8 NVIDIA H100-80G-SXM5 GPUs and 32 Intel Xeon Platinum 8462Y+ CPU cores (2.8 GHz). Accuracy is reported as the average over 2 rounds.

**GCCL (curriculum learning).** Training nodes are pre-partitioned into three difficulty strata (easy/medium/hard) with a fixed per-stage quota. For OGB-Arxiv and OGB-Products, Stage 1 uses 800 easy / 500 medium / 500 hard samples and Stage 2 uses 200 easy / 500 medium / 500 hard samples; within each stage, training proceeds in ascending order of difficulty.

**Reward details.** Stage 1 reward = (i) task correctness, (ii) format compliance, (iii) tool-usage coverage. The predicted label is extracted and compared to the gold category via normalized string match: +1.5 for an exact match, 0 for a mismatch, -1.0 if the answer is missing, -0.5 if the sample index is invalid. Format rewards: +0.5 for exactly one `think` block and one `answer` block (else -0.5); +0.1 if query/document delimiters are balanced (else -0.3); penalties for tool I/O leaking into the answer (-0.5), overly verbose answers (>12 whitespace-separated tokens, -0.2), or residual `think` content in the answer (-0.3). Search-coverage reward: +0.5 per distinct graph-native search tool used in the rollout, capped at 2.0. Stage 2 keeps the format and classification rewards unchanged and adds a cognitive-density reward: +0.5 bonus if all reasoning segments meet the density criterion, -0.2 penalty if any fails (segment-length threshold 100 tokens). For link prediction, only the per-tool evidence count changes: 1-hop and 2-hop Neighborhood Search return up to 5 nodes per call, Structure Salience Search returns 2, and Graph Dense Search returns 3.

**AI usage.** AI was used exclusively for proofreading assistance.

## Additional Experiments and Case Study

**Variance analysis.** Performance over three independent runs under the RL training setup shows modest variance on both node classification and link prediction, indicating reasonably stable training. Smaller backbones exhibit larger variance than larger ones (3B vs 7B), most noticeably on Amazon-Photo for the 3B variants on both tasks — consistent with smaller models being more sensitive to sampling and policy-optimization stochasticity.

| Model | OGB-Products Var(NC) | OGB-Products Var(LP) | Amazon-Photo Var(NC) | Amazon-Photo Var(LP) |
|---|---|---|---|---|
| AgentGL-7B-GRPO | 0.3 | 0.4 | 0.2 | 0.3 |
| AgentGL-3B-GRPO | 0.6 | 0.3 | 0.7 | 1.1 |
| AgentGL-7B-R++ | 0.2 | 0.4 | 0.5 | 0.7 |
| AgentGL-3B-R++ | 0.4 | 0.6 | 0.7 | 0.8 |

**Sensitivity to K (neighborhood size).** Increasing K from 1 to 5 consistently improves accuracy on both OGB-Arxiv and Amazon-Photo, with the best results at K=5 (68.9% and 59.9%, respectively) — a moderately expanded neighborhood supplies more informative structural context. Further increasing K to 7 causes a slight drop on both datasets, suggesting oversized neighborhoods introduce redundant or noisy information. This justifies the default choice K=5.

**Case study.** Representative rollouts are presented for both tasks to make the decision process interpretable. The node-classification example (Amazon domain): the model forms a hypothesis from the anchor text, then verifies it by querying local neighborhoods (1-hop/2-hop) and a global prior (PageRank); highlighted reasoning sentences show how evidence aggregation over the graph reduces ambiguity and prevents over-reliance on anchor text alone. The link-prediction example (Reddit): the model validates a potential edge by searching common 1-hop neighbors; the shared co-post motif provides strong structural evidence that the two endpoints lie in the same tight cluster. Across cases, the agent typically terminates early once the searched evidence becomes self-consistent.

**Covers:** Appendix A.1-A.5: Dataset Details, More Related Work, Implementation Details, Additional Experiments, Case Study (source pages 12-15)
