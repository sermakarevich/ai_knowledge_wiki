> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Lessons Learned & Future Research

**In one sentence:** The three case studies yield nine concrete lessons (summarised in Table 2) that identify RAG-system engineering as an ongoing, runtime-calibrated activity rather than a one-off build, and point to three open research frontiers — chunking & embeddings, RAG vs finetuning, and testing & monitoring.

## Key points

- RAG-system validation is only feasible during operation: systems receive unknown, application-specific input at runtime (performance characteristics, jailbreaks, ambiguous queries) that offline test suites cannot exhaustively cover, so testing of performance characteristics is possible only at runtime.
- Robustness of a RAG system evolves over time rather than being designed in upfront: chunk size, embedding strategy, chunking strategy, retrieval strategy, consolidation strategy, context size, and prompts all require continuous calibration as documents, the LLM, and workloads change.
- Context and caching are leverable wins: a larger context window produced more accurate responses (8K vs 4K, contrary to prior "lost in the middle" results with GPT-3.5), and prepopulating a semantic cache with frequently asked questions drives down cost and latency.
- Safety and access control need explicit handling: jailbreak attacks bypass the RAG layer and hit the LLM's safety training (and research shows fine-tuning can reverse it, so fine-tuned RAG LLMs must be re-tested), while RAG gives the pragmatic route to per-user control over which chunks are accessible.
- Open-source embedding models perform as well as (and for small text, as well as) closed-source alternatives, and adding metadata such as file name and chunk number into the retrieved context measurably improves a reader's/LLM's ability to extract the needed information.
- Pipelines assembled from bespoke point solutions are suboptimal; end-to-end training enhances domain adaptation, and offline evaluation techniques such as G-Evals are promising but require labelled question–answer pairs that application-specific RAG systems often lack.
- Generating realistic, domain-relevant test questions (e.g. with LLMs that synthesise questions from multiple documents) and adopting self-adaptive-systems ideas for runtime monitoring remain open problems for RAG engineering.

---

## Lessons learned (Table 2)

**Table 2: The lessons learned from the three case studies with key takeaways for future RAG implementations**

| FP | Lesson | Description | Case Studies |
|---|---|---|---|
| FP4 | Larger context get better results (Context refers to a particular setting or situation in which the content occurs) | A larger context enabled more accurate responses (8K vs 4K). Contrary to prior work with GPT-3.5 | AI Tutor |
| FP1 | Semantic caching drives cost and latency down | RAG systems struggle with concurrent users due to rate limits and the cost of LLMs. Prepopulate the semantic cache with frequently asked questions | AI Tutor |
| FP5–7 | Jailbreaks bypass the RAG system and hit the safety training | Research suggests fine-tuning LLMs reverses safety training; test all fine-tuned LLMs for RAG system | AI Tutor |
| FP2, FP4 | Adding meta-data improves retrieval | Adding the file name and chunk number into the retrieved context helped the reader extract the required information. Useful for chat dialogue | AI Tutor |
| FP2, FP4–7 | Open source embedding models perform better for small text | Open-source sentence embedding models performed as well as closed-source alternatives on small text | BioASQ, AI Tutor |
| FP2–7 | RAG systems require continuous calibration | A RAG system requires calibrating chunk size, embedding strategy, chunking strategy, retrieval strategy, consolidation strategy, context size, and prompts | AI Tutor, BioASQ |
| FP1, FP2 | Implement a RAG pipeline for configuration | End-to-end training enhances domain adaptation in RAG systems | Cognitive Reviewer, AI Tutor, BioASQ |
| FP2, FP4 | RAG pipelines created by assembling bespoke solutions are suboptimal | Offline evaluation techniques such as G-Evals look promising but are premised on having access to labelled question and answer pairs | BioASQ, AI Tutor |
| FP2–7 | Testing performance characteristics are only possible at runtime | RAG systems receive unknown input at runtime requiring constant monitoring | Cognitive Reviewer, AI Tutor |

*Note: the FP column in the source extraction is OCR-jumbled; the per-row mapping above follows the row order of Table 2 in the paper.*

## Chunking and Embeddings

Chunking documents sounds trivial, but the quality of chunking affects the retrieval process in many ways — in particular the embeddings of the chunk, and hence the similarity matching of chunks to user queries. There are two chunking approaches:

- **Heuristic chunking** — based on punctuation, end of paragraph, etc.
- **Semantic chunking** — using the semantics in the text to inform the start and end of a chunk.

Further research should explore the tradeoffs between these methods and their effect on critical downstream processes like embedding and similarity matching; a systematic evaluation framework comparing chunking techniques on metrics like query relevance and retrieval accuracy would benefit the field.

Embeddings themselves are another active research area, including:

- generating embeddings for multimedia/multimodal chunks such as tables, figures, and formulas.
- the fact that chunk embeddings are typically created **once**, during system development or when a new document is indexed.
- **query preprocessing**, which significantly impacts RAG performance — particularly handling negative or ambiguous queries.
- research is needed on architectural patterns and approaches to address the inherent limitation of embeddings, namely that the quality of a match is domain-specific.

## RAG vs Finetuning

LLMs are strong "world models" thanks to their massive training data and the fine-tuning tasks applied before release, but they are general-purpose (they may not know the very specifics of your domain) and not up to date (knowledge cutoff). Fine-tuning and RAG are therefore two customisation pathways with distinct tradeoffs:

- **Fine-tuning** requires curating internal datasets and baking your data into the model, which forces you to sort out security/privacy (who can access what). Additionally, whenever the foundation model evolves or you have new data to add, you must run fine-tuning again.
- **RAG** offers a pragmatic alternative: chunk your data as needed, retrieve only the relevant chunks into context, and have the LLM generate an answer from that included context. This facilitates continuously updating knowledge with new documents and gives control over which chunks a particular user can access.

However, optimal strategies for chunk embedding, retrieval, and contextual fusion remain active research. Further work should systematically compare the finetuning and RAG paradigms across factors including accuracy, latency, operating costs, and robustness.

## Testing and Monitoring RAG systems

Software engineering best practices are still emerging for RAG systems, and several areas need refinement:

- **Testing and test-case generation**: RAG systems require questions and answers that are application-specific, often unavailable when indexing unstructured documents. Emerging work considers using LLMs to generate questions from multiple documents, but how to generate realistic, domain-relevant questions and answers remains an open problem.
- **Quality metrics**: once suitable test data is available, metrics are needed to help engineers make quality tradeoffs. LLMs are expensive, introduce latency concerns, and have performance characteristics that change with each new release — a characteristic previously studied for machine-learning systems, but whose required adaptations have yet to be applied to LLM-based systems such as RAGs.
- **Self-adaptive systems**: another direction is incorporating ideas from self-adaptive systems to support monitoring and adapting RAG systems; preliminary work has started for other machine-learning applications.

## Conclusion

RAG systems are a new information retrieval paradigm that leverages LLMs, and software engineers increasingly interact with them either by (a) implementing semantic search or (b) through new code-dependent tasks. This paper presented the lessons learned from three case studies, including an empirical investigation involving 15,000 documents and 1000 questions. Its findings guide practitioners by presenting the challenges faced when implementing RAG systems, and it identifies future research directions in three areas: 1) chunking and embeddings, 2) RAG vs finetuning, 3) testing and monitoring.

Two key takeaways stand out:

1. **Validation of a RAG system is only feasible during operation** — systems receive unknown input at runtime, so testing performance characteristics is possible only at runtime and requires constant monitoring.
2. **Robustness evolves rather than being designed in upfront** — RAG systems require continuous calibration of chunk size, embedding strategy, chunking strategy, retrieval strategy, consolidation strategy, context size, and prompts.

Large language models will continue to obtain new capabilities of interest to engineers and researchers. This paper presents the first investigation into RAG systems from a software engineering perspective.

**Covers:** Section 6 (Lessons and Future Research), Table 2, Section 7 (Conclusion)
