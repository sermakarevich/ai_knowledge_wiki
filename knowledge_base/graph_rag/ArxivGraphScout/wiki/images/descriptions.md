# Figure descriptions (for wiki-page embedding)

## fig1-motivation-comparison.png (Figure 1)
Bar chart, Healthcare dataset, QwenScore metric. GraphScout-4B after training: 0.819 (orange bar), vs its own untrained "Initial" score 0.211 (pale segment stacked at bottom of same bar). Baselines (grey bars): GraphCounselor 0.530, PolyG 0.493, GraphCoT 0.441, Cypher 0.422, GraphRAG 0.141, TextRAG 0.093 — all built on larger/flagship backbones (e.g. Qwen-Max). Shows a small trained model beating much larger prompted baselines.

## fig2-graphscout-architecture.png (Figure 2)
"Overview of GraphScout framework" — three stacked panels:
(a) Agentic Graph Exploration Tools: a Code Interpreter and a Node Retriever sit between the LLM and the Knowledge Graph / Graph Database, communicating via Cypher queries and returned results.
(b) Graph Quizzer (top panel, senior scout): given Task Specification (answer type, query pattern, difficulty) and Exploration Initialization (seed node, graph info), it runs an iterative Exploration Process (thought → tool call → observation, looping until a Stopping Condition is satisfied) to synthesize a question, answer, and "Clue Nodes" (the traversal evidence path).
(c) Graph Solver (bottom panel, junior scout): consumes the generated question and produces Multi-turn Tool Use Reasoning Paths (Turn1..Turn4 tool-call sequences); each resulting trajectory is scored on Final Answer correctness, F1, Clue Hit (overlap with the quizzer's clue nodes), Evid (evidence/clue reward), combined into a scalar Reward used for RL training.

## fig3-cross-domain-heatmap.png (Figure 3 + Table 2)
Left: a 5x5 heatmap (rows = training domain, columns = test domain: Healthcare/Literature/Academic/E-Commerce/Legal) showing GraphScout-4B's F1 when trained on one domain and evaluated on another, plus two reference rows for GraphCoT and base Qwen3-4B evaluated per-domain (no cross-domain training). Diagonal and off-diagonal values are close (e.g. Healthcare-trained: 0.855 on Healthcare, 0.612–0.615 on others), showing modest degradation off-domain — evidence of transferable exploration skill rather than memorized domain structure.
Right: Table 2, ablation on Healthcare/Literature (QwenScore, F1): full GraphScout 0.819/0.855 (Healthcare); removing Graph Solver drops to 0.211/0.217; removing the Code-Interpreter tool (w/o 𝒜code) drops further to 0.107/0.101 (largest single drop); removing the clue-based reward (w/o r_clue) gives 0.785/0.812 (smaller drop); replacing Graph Quizzer with random-walk-based question generation (rw Graph Quizzer) gives 0.678/0.705.

## fig456-difficulty-and-efficiency.png (Figures 4, 5, 6)
Figure 4: three grouped bar charts (Easy / Medium / Hard) comparing GraphCoT, GraphCounselor, PolyG, GraphScout-4B (F1) across the five GRBENCH domains. GraphScout-4B leads clearly on Easy and Medium; on Hard, all methods struggle and the gap narrows or reverses in places (e.g. Legal); Healthcare has no hard questions (marked with a red X) and Literature's hard split is 0% F1 for every method.
Figure 5: two bar charts by difficulty (easy/medium/hard) per domain — average output tokens (up to ~6000+ on hard Literature) and average tool calls per question (up to ~14 on hard Literature) — both increase with difficulty in most domains.
Figure 6: log-scale average token consumption per method per domain — GraphCoT and GraphCounselor use ~10^4-10^5 tokens, PolyG and GraphScout-4B use far fewer (roughly an order of magnitude less), illustrating GraphScout's efficiency claim.

## fig78-quizzer-diversity-and-tokens.png (Figures 7, 8 + Table 5)
Figure 7: three pie charts describing the Graph-Quizzer-generated training question set — (a) difficulty distribution: simple 30.6%, medium 37.2%, hard 32.2%; (b) question structural-pattern distribution: <h,*,*> 37.2%, <h,r,*> 11.5%, <h,r,t> 10.1%, Hybrid 35.2%, <h,*,t> 6.0%; (c) answer-type distribution: entity 29.2%, number 32.2%, set 22.6%, bool 16.1%. Labels were auto-judged by an LLM (DeepSeek-Chat) that was blind to the original generation parameters.
Figure 8: two histograms for the Healthcare dataset — (a) question token-length distribution, peaking around 20-30 tokens with a long right tail past 100; (b) number of clue nodes per question, peaking at 3-4 with a long tail to 15+.
Table 5: proportion of failed tool calls per domain, before training ("w/o train", 61-72%) vs after GraphScout training ("w/ train", 1.3-6.6%) — a large reliability improvement from post-training.
