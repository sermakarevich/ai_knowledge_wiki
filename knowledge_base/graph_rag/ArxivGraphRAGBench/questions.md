---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: GraphRAG-Bench

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What three specific limitations of prior GraphRAG benchmarks does GraphRAG-Bench claim to fix, and why does each one make graph-specific reasoning hard to measure?

> [!tip]- Answer
> (1) They use only commonsense questions likely already in the LLM's training data, so a correct answer doesn't prove retrieval helped. (2) They test single-hop or shallow multi-hop reasoning over explicit connections, which doesn't stress the unique value of graph structure. (3) Their answer formats are narrow (short names/dates, multiple-choice), which can't reflect genuine multi-step reasoning ability. See [[wiki/01-introduction-and-motivation|Introduction & Motivation]].

### Q2. Why does GraphRAG-Bench need a 4-stage extraction pipeline (LayoutLMv3, YOLO formula detection, PaddleOCR, MinerU) instead of just extracting text directly from the textbook PDFs?

> [!tip]- Answer
> Direct PDF extraction is unreliable because pages mix text-based and scanned formats, inline mathematical formulas get garbled by generic OCR, and extracted elements arrive out of natural reading order. The pipeline classifies pages by type, isolates formulas before OCR so they aren't corrupted, and reorders/merges fragmented elements to restore human reading order and build a Book→Chapter→Section→Unit hierarchy. See [[wiki/02-benchmark-design|Benchmark Design & Construction]].

### Q3. What is the purpose of the expert-crafted "rationale" attached to every question, and how does it change what the benchmark can measure compared to grading final answers alone?

> [!tip]- Answer
> The rationale isolates prerequisite concepts, describes their relationships, and specifies the inferential operations needed to reach the answer. This lets evaluation compare a model's own generated rationale against the gold one, measuring whether the model's reasoning is genuinely faithful rather than pattern-matched — distinguishing correct answers reached by real reasoning from lucky guesses. See [[wiki/02-benchmark-design|Benchmark Design & Construction]].

### Q4. On the generation accuracy results, which two methods actually score below the plain GPT-4o-mini baseline, and what does the paper say causes this?

> [!tip]- Answer
> DALK (69.30) and G-Retriever (69.84), both below the 70.68 baseline. The paper attributes this to over-reliance on structural graph information at the expense of semantic content, which introduces excessive generation noise and impairs the LLM's judgment. See [[wiki/03-evaluation-protocol-and-core-results|Evaluation Protocol, Metrics & Core Results]].

### Q5. Why do RAPTOR and GFM-RAG sit at opposite extremes of retrieval speed and indexing speed, and what structural choice explains each?

> [!tip]- Answer
> RAPTOR retrieves fastest (0.02s average) because its clustered tree structure lets it localize relevant information quickly, though building that tree is itself slow. GFM-RAG indexes fastest (93.55s) because it skips building a traditional vector database entirely, storing only question-corresponding entities during graph construction — but its retrieval (1.96s) is still slower than RAPTOR's. See [[wiki/03-evaluation-protocol-and-core-results|Evaluation Protocol, Metrics & Core Results]].

### Q6. On the reasoning-capability results (Table 5), why does GPT-4o-mini's R and AR score decline so much even though its raw generation accuracy is high, and how do GraphRAG methods address this?

> [!tip]- Answer
> GPT-4o-mini's high accuracy is partly achieved by conjecture or pattern matching rather than real reasoning, so its R score (rationale alignment) and especially its AR score (correct answer + correct reasoning) drop sharply — many "correct" answers are effectively lucky guesses. GraphRAG methods retrieve not just semantically similar text but multi-hop dependent evidence, giving the LLM material to reason over rather than rely on internal conjecture, which raises R/AR scores across all nine methods. See [[wiki/03-evaluation-protocol-and-core-results|Evaluation Protocol, Metrics & Core Results]].

### Q7. Why does every GraphRAG method degrade generation accuracy in the Mathematics domain specifically, while the effect on Ethics questions is merely mediocre rather than degraded?

> [!tip]- Answer
> Mathematics requires rigorous symbolic manipulation and precise deductive chains computed internally by the model; the explanatory/conceptual documents GraphRAG retrieves have symbolic notation and formula layouts that are misaligned with the problem, causing ambiguity or lost steps — actively hurting accuracy. Ethics questions instead hinge on subjective value judgments and dynamic moral context that neither the base LLM nor retrieved graph content can represent well, so performance is flatly mediocre for both, not actively worsened by retrieval. See [[wiki/04-topic-analysis-observations-and-conclusion|Topic-Specific Analysis, Observations, Case Study & Conclusion]].

### Q8. The paper uses an LLM to judge open-ended/fill-in-blank accuracy and to score the R/AR reasoning metrics. What is the strongest reason to be skeptical of this design choice, and would you trust the paper's method rankings if that judge were biased?

> [!tip]- Answer
> LLM-as-judge scoring is itself an unvalidated measurement instrument — there's no reported inter-rater agreement with human experts, and if the judge model shares blind spots or stylistic preferences with GPT-4o-mini (the very model being evaluated), scores could be systematically biased in ways a different judge wouldn't reproduce. Because every method is judged by the same instrument, *relative* rankings between methods are more trustworthy than the absolute numbers, but a judge bias that favors a particular answer style (e.g., longer, more structured rationales) could still distort which methods look best. See [[critical_thinking|Critical Analysis]].
