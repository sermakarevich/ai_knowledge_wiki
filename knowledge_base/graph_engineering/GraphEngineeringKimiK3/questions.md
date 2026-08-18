---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Graph Engineering with Kimi K3

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. Why does standard vector-similarity RAG fail on a question like "why did our sales drop in March?" even with perfect embeddings?

> [!tip]- Answer
> Because the real answer is a causal chain spread across several documents (release delay → supplier problem → warehouse failure → negative reviews → lower conversion) that share no keywords with each other or with "sales drop." Vector similarity finds documents that *look alike*, not facts that *connect* — no amount of better embeddings recovers a chain the retrieval method structurally cannot represent. See [[wiki/01-the-problem-and-what-graph-engineering-is|The Problem]].

### Q2. What does "graph engineering" mean in THIS article, and how does that differ from the agent-topology sense used elsewhere in this research batch?

> [!tip]- Answer
> Here it means the knowledge-graph / GraphRAG sense: storing facts as subject→relation→object triples in a graph database and querying relationship paths directly. The agent-topology sense (used by sources like [[YouTubeWhatIsGraphEngineering/summary]] and [[LangGraph3YearsGraphEngineering/summary]]) means wiring multiple AI agents/loops into a graph of who calls whom. Same buzzword, two unrelated techniques. See [[wiki/01-the-problem-and-what-graph-engineering-is|The Problem]].

### Q3. What is the difference between Microsoft's "local search" and "global search," and how does standard RAG perform on each?

> [!tip]- Answer
> Local search finds a node and its immediate connections (e.g. "what happened with supplier X in July?"); global search finds patterns across the whole graph (e.g. recurring risk patterns across all suppliers). Standard RAG handles local-style questions badly and global-style questions not at all — a graph handles both. See [[wiki/01-the-problem-and-what-graph-engineering-is|The Problem]].

### Q4. Kimi K3 is recommended for this architecture — but the article is explicit that it is not chosen for raw capability. What is the actual justification, and what is the honest caveat?

> [!tip]- Answer
> The justification is economic/architectural: a 1,048,576-token context window lets a full retrieved subgraph fit without truncation, Kimi Delta Attention gives up to 6.3x faster decoding on long contexts, and Attention Residuals reduce signal degradation between early and late context. The honest caveat: Moonshot's own blog admits K3's overall performance still trails Claude Fable 5 and GPT-5.6 Sol — it's the best model *for this architecture*, not the strongest model overall. See [[wiki/02-why-kimi-k3-and-the-model-vs-graph-finding|Why Kimi K3]].

### Q5. What did the 26-model comparison find about model size versus graph quality, and what is the practical implication?

> [!tip]- Answer
> Bigger model + bad graph → worse results; smaller model + good graph → better results, consistently. The practical implication: when results are bad, the article argues you should fix your retrieval structure before upgrading to a more expensive model — it's cheaper and works better. See [[wiki/02-why-kimi-k3-and-the-model-vs-graph-finding|Why Kimi K3]].

### Q6. Name the 8 layers of the pipeline in order, and explain why the loop "closing" at Update matters.

> [!tip]- Answer
> Ingestion → Extraction → Resolution → Storage → Retrieval → Agent → Verification → Update. The loop closes at Update and restarts at Extraction — new facts feed back into extraction/resolution on the next pass, which is what makes the system compound (get structurally better over time) rather than run as a one-pass, static pipeline. See [[wiki/03-the-8-layer-architecture-and-5-prompts|The 8-Layer Architecture]].

### Q7. Why is the Resolution layer described as "the layer everyone skips and everyone regrets skipping," and what concrete symptom shows up when it's skipped?

> [!tip]- Answer
> Skipping entity resolution means name variants like "OpenAI," "Open AI," and "OpenAI Inc." each become separate graph nodes instead of one canonical entity. This fragments the graph, so queries return partial, fragmented results instead of the complete picture — and retrofitting resolution onto an already-polluted graph is significantly harder than doing it upfront. See [[wiki/03-the-8-layer-architecture-and-5-prompts|The 8-Layer Architecture]] and [[wiki/04-stack-week-one-plan-and-troubleshooting|Troubleshooting]].

### Q8. The article cites "85% lower cost, 18% better accuracy" for graph engineering. What does [[critical_thinking|the critical analysis]] say is the problem with taking that figure at face value, and what should you do instead?

> [!tip]- Answer
> The figures come from specific research on specific document sets against an unstated (and highly consequential) baseline — "85% cheaper than loading raw files into context" is a very different claim from "85% cheaper than your current production RAG." The direction (graphs help) is well-supported across independent groups, but the magnitude is not a universal guarantee. The article itself, and the critical analysis, recommend measuring your own accuracy/cost/latency numbers on your own data during week one rather than assuming the published percentages transfer. See [[critical_thinking|Critical Analysis]].
