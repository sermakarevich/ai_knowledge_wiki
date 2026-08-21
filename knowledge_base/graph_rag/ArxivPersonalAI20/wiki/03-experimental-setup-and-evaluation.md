> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental Setup and Evaluation Design

**In one sentence:** PAI-2 is evaluated against four baselines on six QA benchmarks (100 QA pairs each, 90 configurations total) using a validated LLM-as-a-Judge framework (Qwen2.5 7B) plus RAGAS Context Relevance, Faithfulness and Groundedness, with the LLM backbone chosen by a few-shot ablation on HotpotQA that favored Qwen2.5 7B.

## Key points

- Three research questions drive the evaluation: RQ1 — whether PAI-2 achieves superior results compared to baselines; RQ2 — whether graph traversal algorithms improve PAI efficiency compared to PAI with a naive flattened retriever; RQ3 — how PAI-2 efficiency varies with the number of generating clue-queries per step of the search plan.
- LLM backbone selection used few-shot evaluation on HotpotQA over four 7–9B models (Qwen2.5 7B, Llama3.1 8B, Granite3.3 8B, Gemma2 9B); Qwen2.5 7B was the best across all four metrics for PAI-2 (0.70 / 0.82 / 0.44 / 0.52) and is used in the main experiments, with the same LLM used for both response generation and memory graph construction.
- Vector representations combine dense and sparse embeddings: `intfloat/multilingual-e5-large` and BM25; graph traversal uses two algorithm combinations from PAI-1 — "BS + WC" (BeamSearch + WaterCircles) and "BS + NR" (BeamSearch + NaiveRetriever) — with fixed base hyperparameters, no vertex-type constraints during traversal, but episodic triples discarded during filtering.
- Each PAI-2 configuration was evaluated on 100 question-answer pairs from each of the six benchmarks, yielding 15 distinct QA configurations per dataset and 90 QA configurations in total, plus 44 configurations for the LLM few-shot ablation study on HotpotQA; six memory graphs were constructed, with an average ingestion speed of ≈1.63 documents (492 average length) per minute.
- Evaluation rejects BLEU/ROUGE/Meteor (syntactic) and BERTScore (insufficient differentiability), adopting LLM-as-a-Judge with Qwen2.5 7B (labels 1 for correct, 0 for incorrect; accuracy is the main metric), with RAGAS Context Relevance (two independent 0/1/2-judged LLM calls, rescaled to [0,1] and averaged), Faithfulness (0–1, answer claims supported by retrieved context) and Groundedness (0 = not grounded, 1 = partially, 2 = fully grounded).
- Judge reliability was validated by human annotation with Overlap-3 for the best PAI-2 and HippoRAG 2 setups, giving Krippendorff's α = 0.935 and a Pearson correlation r = 0.86 between judge scores and majority-vote human annotations.
- Baselines are LightRAG (dual-level entity/knowledge retrieval over graph + vectors), RAPTOR (recursive clustering and summary tree), HippoRAG 2 (Personalized PageRank over LLM-triple knowledge graph), and PAI-1 (hybrid graph with standard edges and two hyperedge types); baselines run with Qwen2.5 and specific embedders (LightRAG — `BAAI/bge-m3`, RAPTOR — `sentence-transformers/multi-qa-mpnet-base-cos-v1`, HippoRAG 2 — `facebook/contriever`, PAI-1 — fusion of `intfloat/multilingual-e5-large` and BM25).
- Infrastructure: Neo4j for the graph part, Qdrant (dense) and OpenSearch (sparse) for embeddings, Redis and MongoDB for caching (enabled during experiments), all in Docker containers on a single machine; LLMs served via local Ollama on a single NVIDIA TITAN RTX 24GB GPU; the query preprocessing stage is disabled because it did not sufficiently boost QA accuracy.

---

## Research questions, LLM selection and configuration

Definitions of the experiment: RQ1 (PAI-2 superiority over baselines), RQ2 (graph traversal vs. naive flattened retriever efficiency), RQ3 (efficiency vs. number of generating clue-queries per search-plan step).

To choose the LLM backbone, a few-shot evaluation was performed on HotpotQA with four 7–9B tier LLMs: Qwen2.5 7B, Llama3.1 8B, Granite3.3 8B, Gemma2 9B. Best performer by all four metrics was Qwen2.5 7B (Table 1).

| Method | Qwen2.5 7B | Llama3.1 8B | Granite3.3 8B | Gemma2 9B | Mean |
|---|---|---|---|---|---|
| PAI-1 | **0.60** / 0.59 / 0.41 / 0.13 | 0.52 / 0.46 / 0.38 / 0.11 | 0.59 / **0.61** / 0.44 / **0.32** | 0.54 / 0.58 / **0.48** / 0.13 | 0.56 / 0.56 / 0.43 / 0.17 |
| PAI-2 | **0.70** / **0.82** / **0.44** / **0.52** | 0.64 / 0.70 / **0.44** / 0.42 | 0.54 / 0.72 / 0.39 / 0.51 | 0.65 / 0.66 / **0.44** / 0.45 | 0.63 / 0.73 / 0.43 / 0.48 |
| Mean | 0.65 / 0.7 / 0.42 / 0.32 | 0.58 / 0.58 / 0.41 / 0.26 | 0.56 / 0.66 / 0.42 / 0.42 | 0.6 / 0.62 / 0.46 / 0.29 | 0.6 / 0.64 / 0.43 / 0.32 |

**Table 1.** Best performance in a few-shot ablation experiment for PAI-1 and PAI-2 on HotpotQA dataset across four LLMs. Cells contain Context Relevance, Faithfulness, LLM-as-a-Judge and Groundedness scores, respectively, to identify optimal LLM, that should be used in main experiments.

Memory representations: dense + sparse embeddings, `intfloat/multilingual-e5-large` and BM25. Graph traversal: two combinations of BeamSearch (BS), WaterCircles (WC) and NaiveRetriever (NR) algorithms from PAI-1 — "BS + WC" and "BS + NR" — selected for their superior and comparative performance in prior research. Base algorithm hyperparameters are fixed (Appendix E); no constraints on vertex types during graph traversal; episodic triples discarded during the filtering stage.

Configuration summary: each PAI-2 configuration evaluated on 100 question-answer pairs per benchmark; the same LLM used for both response generation under a given QA configuration and the corresponding memory graph construction; 15 distinct QA configurations per dataset; 90 QA configurations in total; plus 44 configurations for the LLM few-shot ablation study on HotpotQA.

Implementation details: memory graph has a graph part (textual representations of object, thesis and episodic vertices with properties and edges, stored in Neo4j) and a vector part (embeddings of graph elements for semantic similarity, stored in Qdrant for dense and OpenSearch for sparse). A caching mechanism for intermediate QA pipeline results uses Redis and MongoDB; cache was enabled during experiments. All databases hosted in separate Docker containers on a single machine. Medium-sized LLMs (7–14B) hosted in local Ollama; inference on a single NVIDIA TITAN RTX 24GB GPU. Six memory graphs built from the six benchmarks; average speed of adding documents (492 average length) ≈1.63 per minute (Appendix G). Query preprocessing disabled: insufficient accuracy boost (per ablation; LLM prompts need additional tuning) and out of scope of the research questions.

## Benchmarks

Experiments span six benchmarks chosen for varying domains, structural complexities, reasoning requirements, and to mitigate bias from limited domain diversity:

- **Natural Questions** [18] — large-scale corpus for open-domain questions by Google, over 307K samples, each a natural language query paired with relevant Wikipedia pages containing the answer spans; questions from real Google Search user queries. Distinguishing features: (1) diversity in question types — factual, definitional, list-based, comparative, opinion-oriented; (2) complex answer requirements — answers can be short snippets or long passages requiring deeper reasoning.
- **TriviaQA** [19] — open-domain factoid QA, over 95K question-answer pairs sourced from Bing search engine. Distinguishing characteristics: (1) multi-evidence reasoning — answers often require synthesizing information across multiple documents; (2) contextual complexity — diverse question types from domains like history, science, literature. Unlike SQuAD/Natural Questions (extractive QA in structured contexts), TriviaQA emphasizes multi-hop inference and retrieval-based tasks.
- **HotpotQA** [20] — crowdsourced QA on English Wikipedia, ≈113K questions; each requires combining information from the introductory sections of two Wikipedia articles. Provides two gold paragraphs per question plus a list of sentences identified as supporting facts. Includes reasoning strategies: bridge questions (missing entities), intersection questions (e.g., "what satisfies both property A and property B?"), and comparison questions (comparing two entities through a common attribute).
- **2WikiMultihopQA** [21] — multi-hop QA with complex questions requiring reasoning over multiple Wikipedia paragraphs; each question necessitates logical connections across different pieces of information.
- **MuSiQue** [22] — ≈25K 2–4 hop questions constructed by composing single-hop questions from five existing single-hop QA datasets; diverse, complex reasoning paths requiring integration of information from multiple hops.
- **DiaASQ** [23] — user dialogues from a Chinese forum focused on mobile device characteristics; includes structured "true statements" encapsulating the core semantic content of each dialogue. For evaluation, complex multi-hop questions were procedurally generated based on these statements.

Because of the computational/engineering complexity of constructing and traversing large memory graphs, manageable yet representative subsets were created to enable iterative experimentation (tuning multiple retrieval algorithms and LLM configurations) within practical resource constraints (preprocessing and statistics in Appendix D):

| Dataset | #qa-pairs | #documents |
|---|---|---|
| Natural Questions | 3970 | 2000 |
| TriviaQA | 500 | 4925 |
| HotpotQA | 2000 | 3933 |
| 2WikiMultihopQA | 2000 | 4596 |
| MuSiQue | 1931 | 4185 |
| DiaASQ | 4800 | 3483 |

**Table 2.** Characteristics of prepared datasets for PAI-2 and baselines evaluation.

## Evaluation metrics and protocol

Motivation: traditional statistical metrics (BLEU, ROUGE, Meteor Universal) struggle to distinguish syntactically similar but semantically distinct texts; BERTScore was tried but the authors found it lacks sufficient differentiability, often failing to capture nuanced distinctions between correct and incorrect answers.

**LLM-as-a-Judge** [28] framework with Qwen2.5 7B: the judge evaluates question-answer pairs using a structured prompt containing question, ground truth and generated answer; it labels 1 for correct answers and 0 for incorrect ones; accuracy is the main metric (prompts in Appendix F).

Judge validation via human annotation for the best PAI-2 and HippoRAG 2 experimental setups: responses generated by Qwen2.5 7B annotated using the Overlap-3 metric by domain experts under the same criteria as the automated judge. Inter-annotator agreement via Krippendorff's α: mean α = 0.935 (high assessment reliability). Alignment between judge and humans: Pearson correlation r between judge scores and majority vote of human annotations; strong mean correlation r = 0.86 (annotation procedure in Appendix J).

Additional LLM-based metrics from the RAGAS [2] library:

- **Context Relevance** — whether the retrieved contexts are pertinent to the user query; two independent LLM-as-a-Judge prompt calls each rate relevance on a scale of 0, 1 or 2; ratings converted to a [0, 1] scale and averaged to produce the final score; higher scores indicate contexts more closely aligned with the query.
- **Faithfulness** — how factually consistent an answer is with the retrieved context; ranges from 0 to 1; an answer is faithful if all its claims can be supported by the retrieved context.
- **Groundedness** — how well an answer is supported by the retrieved contexts; assesses whether each claim can be found, wholly or partially, in the contexts: 0 if not grounded at all; 1 if partially grounded; 2 if fully grounded (every statement found or inferable from the retrieved context).

## Baselines

- **LightRAG** [30] — a simpler, efficiency-focused alternative to modern GraphRAG methods; a graph-structured RAG framework with a dual-level retrieval system combining low-level entity retrieval with high-level knowledge discovery; integrates graph structures with vector representations for efficient retrieval of related entities and relationships.
- **RAPTOR** [31] — a RAG framework enhancing retrieval via recursive summary and hierarchical clustering into a tree; recursively clusters text chunks based on vector embeddings and generates text summaries of those clusters, building the tree bottom-up; clustered nodes are siblings, and a parent node contains the text summary of that cluster.
- **HippoRAG 2** [32] — a non-parametric continual learning framework leveraging Personalized PageRank over an open knowledge graph constructed from LLM-extracted triples; enhances multi-hop reasoning through sophisticated graph traversal and passage integration mechanisms.
- **PersonalAI 1.0 (PAI-1)** [12] — a flexible framework for creating external memory based on a knowledge graph for AI Agents; building on AriGraph [33], PAI-1 introduces a novel hybrid graph design supporting standard edges and two types of hyperedges for rich semantic and temporal representations; supports diverse retrieval mechanisms (A*, WaterCircles traversal, BeamSearch and hybrid methods), adaptable to different datasets and LLM capacities.

Baseline evaluation used Qwen2.5 as LLM backbone for graph construction and information search; per-method embedders: LightRAG — `BAAI/bge-m3`; RAPTOR — `sentence-transformers/multi-qa-mpnet-base-cos-v1`; HippoRAG 2 — `facebook/contriever`; PAI-1 — fusion of `intfloat/multilingual-e5-large` and BM25.

**Covers:** Sections IV (Experiment Set-up) and V (Evaluation) of the paper.
