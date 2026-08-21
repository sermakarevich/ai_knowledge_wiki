> [[index|Wiki]] | [[digest|Digest]]

# AgentGL: Towards Agentic Graph Learning with LLMs via Reinforcement Learning

**Paper:** [AgentGL: Towards Agentic Graph Learning with LLMs via Reinforcement Learning (Sun et al., 2026)](https://arxiv.org/abs/2604.05846)

---

LLM agents that do agentic search over external resources — RAG, tool-use agents — still treat the world as flat unstructured text, even when the underlying data is a Text-Attributed Graph (TAG) like a citation network, a product co-purchase graph, or a social platform, where meaning depends on topology as much as text. AgentGL proposes Agentic Graph Learning (AGL): an LLM agent that navigates the *native* graph directly, rather than a reconstructed knowledge graph (GraphRAG) or a one-shot static graph context (GraphLLMs like GraphGPT/GraphICL).

The agent is given four graph-native search tools — 1-hop and 2-hop neighborhood search, a PageRank-based structure-salience search, and a semantic dense search — so it can explore both locally and globally, structurally and semantically. Training is a two-stage RL curriculum: Stage 1 (graph-native policy bootstrapping) teaches the agent to use all four tools via a coverage reward; Stage 2 (search-efficiency optimization, "Search-Constrained Thinking") teaches it to stop over-searching via a cognitive-density penalty and a retrospective-termination prompt, once accuracy is already learned. Both stages run under a graph-conditioned curriculum (GCCL) that orders training examples from easy to hard using purely structural/semantic difficulty scores — no manual annotation needed. The RL optimizer is critic-free (GRPO or REINFORCE++).

Evaluated on 7 TAG benchmarks (citation, e-commerce, social) across node classification and link prediction, with Qwen2.5-3B/7B backbones, AgentGL beats 13 baselines across five families (GNNs, GraphLLMs, GraphRAG, standard agentic search, SFT LLMs) by an average of 12.7-26.6% (node classification) and 22.4-28.4% (link prediction), with best-average gains up to 17.5% and 28.4% respectively. Ablations confirm every component is load-bearing: dropping the coverage reward collapses search to zero; dropping the two efficiency terms (cognitive-density regularization, retrospective-termination trigger) loses the Stage-2 efficiency gain; the curriculum (GCCL) adds ~0.65% accuracy and more stable convergence. Stated limitations: text-only graphs (no multimodal support yet), a fragile Stage-2 training balance, an intentionally simple search-efficiency mechanism, and untested behavior on denser graphs.
