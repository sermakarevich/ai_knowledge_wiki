---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: GraphScout

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What are the two classes of prior GraphRAG methods, and what specific limitation do both classes share?

> [!tip]- Answer
> Passive retrieval-driven methods (static node selection + fixed-hop subgraph expansion, then linearized to text) and active traversal-based methods (LLMs given basic graph tools like node querying/relation expansion, driven by hand-designed prompting). Both rely on manually designed, limited interaction primitives and give the LLM no intrinsic prior for structured graph exploration — they lean on external workflow constraints instead of training the model's own exploration ability. See [[wiki/01-motivation-and-related-work|Motivation and Related Work]].

### Q2. Why does the Graph Solver's reward combine an F1-based answer reward with an evidence-clue reward, rather than using answer correctness alone?

> [!tip]- Answer
> Answer-only rewards are sparse for multi-turn graph reasoning — a long trajectory either gets the final answer right or not, giving little signal about intermediate steps. The auxiliary evidence-clue reward (checking whether the trajectory touched the same clue nodes the Graph Quizzer used) is added only when the answer reward is below a threshold δ, and the combined score is capped at δ, so it guides exploration without letting evidence-matching substitute for actually being correct. See [[wiki/02-graphscout-method|The GraphScout Method]].

### Q3. In the ablation study, which single component's removal caused the largest performance drop on Healthcare, and what does that imply?

> [!tip]- Answer
> Removing the Code Interpreter tool caused the largest drop (0.819→0.107 QwenScore), larger than removing the Graph Solver entirely (→0.211) or the clue-based reward (→0.785). This implies tool-mediated, programmable graph interaction is the single most load-bearing piece of the system — more important than either the RL training itself or the auxiliary reward. See [[wiki/03-experiments-and-results|Experiments and Results]].

### Q4. Why does GraphScout show only mild degradation when trained on one domain (e.g. Healthcare) and tested on a completely different domain (e.g. Legal)?

> [!tip]- Answer
> The paper argues this shows GraphScout learns transferable, intrinsic graph-exploration *behaviors* (how to decompose a question, pick tools, and verify evidence) rather than memorizing domain-specific structure or traversal heuristics — so the skill carries over even though the graph's entities and relations are completely different. See [[wiki/03-experiments-and-results|Experiments and Results]].

### Q5. In the worked case study, what specific mistake caused GraphCoT to fail, and what did GraphScout do differently to succeed?

> [!tip]- Answer
> GraphCoT misidentified node D018888 as a Disease when it was actually a Symptom, then repeatedly queried disease-specific relation types that didn't exist on it, retrying the same failing query for 6 turns before giving up. GraphScout used its Code Interpreter to check the node's actual outgoing relations, discovered the type mismatch, traced through `DISEASE_PRESENTS_SYMPTOM` to the correct disease (Alzheimer's), and aggregated downregulated genes to the correct cellular component. See [[wiki/04-implementation-details-and-appendix|Implementation Details and Appendix]].

### Q6. Why did the researchers use a "de-conditioned" LLM judge to evaluate the Graph Quizzer's generated question set, instead of just checking the generation parameters were followed?

> [!tip]- Answer
> Checking the generation parameters only verifies the generator's own bookkeeping — it can't catch cases where the generator claims a category but the resulting question doesn't actually fit it. By having DeepSeek-Chat independently judge each question's difficulty/pattern/answer-type without seeing the original parameters, the analysis is an honest, blind check on whether the synthetic dataset is genuinely diverse rather than diverse only on paper. See [[wiki/04-implementation-details-and-appendix|Implementation Details and Appendix]].

### Q7. Suppose you wanted to apply the GraphScout approach to a company's internal support-ticket graph (tickets linked to customers, products, and prior resolutions) instead of a scientific/biomedical KG. What would need to change, and what would likely carry over unchanged?

> [!tip]- Answer
> The Agentic Graph Exploration Tools (Code Interpreter + Node Retriever) and the overall Quizzer→Solver training pipeline would carry over largely unchanged, since they're graph-schema-agnostic. What would need to change: the graph would need to be loaded into a query-able store (e.g. Neo4j) with schema/property indexes, the Graph Quizzer's task specification (answer types, query patterns) would need re-tuning to ticket-domain questions, and — per the paper's own cross-domain results — some in-domain training data would still be worth generating even if a differently-trained GraphScout model were reused, since transfer is good but not perfect (mild degradation, not zero). See [[wiki/02-graphscout-method|The GraphScout Method]].

### Q8. The paper's evidence rests heavily on ablations and a single benchmark (GRBENCH). What is the weakest link in this evidence, and why does it matter for deciding whether to trust the 16.7% headline number?

> [!tip]- Answer
> The Graph Quizzer's training-data diversity is validated by a single judge model (DeepSeek-Chat) that is not independent of the broader model family used elsewhere in the pipeline, and all quantitative results come from one benchmark (GRBENCH) with no replication on an unrelated graph-QA benchmark — so the 16.7% figure could partly reflect properties specific to GRBENCH's question style rather than a fully general graph-exploration skill. See [[critical_thinking|Critical Analysis]].
