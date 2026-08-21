---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: AgentGL

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. Why does the paper argue that standard agentic-search/RAG systems can't fully exploit Text-Attributed Graphs, even though they can already retrieve external text?

> [!tip]- Answer
> Because those systems treat all external information as flat, unstructured text and select evidence by lexical/semantic similarity alone. In a TAG, meaning comes from the interplay of text content *and* graph topology (who cites whom, who's connected to whom) — a purely text-similarity agent has no mechanism to exploit that structural signal. See [[wiki/01-motivation-and-related-work|Motivation and Related Work]].

### Q2. What is the key structural difference between how AgentGL acquires graph context and how GraphLLMs (e.g., GraphGPT, GraphICL) do it?

> [!tip]- Answer
> GraphLLMs extract a graph context once, statically, at inference time (via graph-guided prompting or instruction tuning) — no further adaptation is possible mid-reasoning. AgentGL's agent dynamically navigates the *native* TAG step by step during inference, choosing its next move based on evidence gathered so far. See [[wiki/01-motivation-and-related-work|Motivation and Related Work]].

### Q3. Name the four Graph-Native Search (GNS) tools and the two axes they're designed to cover.

> [!tip]- Answer
> 1-hop neighborhood search, 2-hop neighborhood search, structure salience search (PageRank-based), and graph dense search (semantic-embedding based). They're designed to jointly cover Local vs. Global and Structure vs. Semantics, so the agent can pick the right kind of evidence for a given instance. See [[wiki/02-agentgl-method|The AgentGL Method]].

### Q4. Why does Stage 1 training include a coverage reward (r_COV), and what happens in the ablation when it's removed?

> [!tip]- Answer
> r_COV pays the model for trying each of the four tools at least once per rollout, to prevent early mode collapse onto a single default tool (or no tool at all) in the large discrete action space. Without it, the ablation shows valid-GNS-tool usage collapses to near zero after a brief spike — the agent effectively stops searching, and the reward plateaus at a suboptimal level. See [[wiki/03-experiments-results-and-conclusion|Experiments, Results, and Conclusion]].

### Q5. What is the purpose of Stage 2 ("search-efficiency optimization" / search-constrained thinking), and what two mechanisms implement it?

> [!tip]- Answer
> Stage 2 curbs excessive, low-value searching once the agent has already learned to search effectively in Stage 1 — the goal is to substitute redundant retrieval with deeper reasoning ("think more, search less"). It's implemented via (1) a Retrospective Termination Trigger, a "cognitive interrupt" injected after each tool call that forces the model to explicitly decide whether more searching is needed, and (2) Cognitive Density Regularization, a reward penalty on reasoning segments that are too short/shallow. See [[wiki/02-agentgl-method|The AgentGL Method]].

### Q6. How does GCCL (Graph-Conditioned Curriculum Learning) decide which training examples are "easy" vs. "hard" — without any human annotation?

> [!tip]- Answer
> It uses purely structural/semantic priors computed from the graph itself: for node classification, a Wilson-lower-bound-based homophily score plus node degree (structurally prominent, label-consistent hubs are easy); for link prediction, the cosine similarity between the two nodes' features relative to the true edge label (a high-similarity positive edge or low-similarity negative edge is easy; a high-similarity negative or low-similarity positive is hard). See [[wiki/02-agentgl-method|The AgentGL Method]].

### Q7. On the main results table, roughly how much does AgentGL outperform GraphRAG and GraphLLM baselines specifically on link prediction with the 7B backbone, and what does the paper attribute this margin to?

> [!tip]- Answer
> On Qwen2.5-7B link prediction, AgentGL beats GraphRAG by 47.4% in-domain (35.4% zero-shot) and GraphLLM by 23.2% in-domain (26.9% zero-shot). The paper attributes this to static-context methods being brittle under distribution shift, whereas AgentGL's interleaved search-and-reasoning loop adaptively acquires relevant evidence per instance and suppresses irrelevant context. See [[wiki/03-experiments-results-and-conclusion|Experiments, Results, and Conclusion]].

### Q8. According to the appendix, how does the paper distinguish "Agentic Graph Learning" (its own paradigm) from "GraphRAG," and why does this distinction matter for how the retrieval graph is built for GraphRAG baselines in the experiments?

> [!tip]- Answer
> In GraphRAG, the graph is an auxiliary index/scaffold used to retrieve textual evidence to ground open-ended generation — the graph is not the object being reasoned about. In AGL, the graph *is* the primary problem instance, and the episode ends in a discrete task decision via graph-native operators rather than free-form text generation. Practically, this is why the GraphRAG baselines' retrieval graphs are built by subsampling only 500 nodes per TAG and indexing raw node text — they need a *retrieval corpus*, not the full native graph AgentGL operates on. See [[wiki/04-appendix-datasets-and-implementation|Appendix: Datasets, Implementation, and Case Study]].

### Q9. The paper reports large accuracy gains (up to 17.5%/28.4%) over strong baselines, but the appendix reveals the training data is subsampled (3,000 train / 1,000 test nodes on the two largest datasets). Does this weaken the headline claim?

> [!tip]- Answer
> It's a legitimate caveat rather than a fatal flaw: the subsampling follows an existing published protocol (GraphICL) applied identically to AgentGL and all baselines, so the comparison stays fair, but it does mean the reported numbers describe performance in a reduced-scale, cleaned-up regime rather than full production-scale graphs (169K nodes on OGB-Arxiv, for instance). Generalization to full-scale, denser graphs is explicitly untested — the paper's own limitations section flags graph density as an open direction. See [[critical_thinking|Critical Analysis]].
