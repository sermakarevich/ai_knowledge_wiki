> [[index|Wiki]] | [[summary|Summary]]

# Seven Failure Points When Engineering a Retrieval Augmented Generation System — Digest

The whole source at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-background-and-rag-pipeline|Background & RAG Pipeline]]

**In one sentence:** RAG is the pragmatic alternative to fine-tuning for grounding LLM answers in an organisation's unstructured knowledge, and this page lays out why it is chosen, the two-stage Index/Query pipeline it runs on, and the design decisions engineers must make at each stage.

- RAG is preferred over fine-tuning because it avoids the cost of training/serving a fine-tuned LLM and lets the knowledge base be continuously updated with new documents; both options carry tradeoffs around privacy/security, scalability, cost, and required skills, and the paper focuses on RAG.
- RAG systems aim to (a) reduce hallucinated LLM responses, (b) link sources/references to generated answers, and (c) remove the need for annotating documents with metadata — any unstructured content can be indexed and queried without knowledge-graph construction or heavy data curation.
- LLMs used directly as QA systems face two fundamental challenges that RAG addresses: hallucinations (responses that look right but are incorrect) and unboundedness (no way to direct or update output content other than prompt engineering).
- The Index process is a development-time pipeline: documents are split into chunks, each chunk is converted to a vector embedding and stored alongside the chunk in a vector database; chunk size is a core tradeoff — too small and some questions can't be answered, too long and answers contain generated noise.
- Changing the embedding model requires re-indexing all chunks, so the embedding choice should be validated on the application domain, expected question types, chunk size, and content structure before committing.
- The Query process runs at runtime: an LLM rewriter generalises the raw question (folding in chat history), the new query is embedded, and top-k chunks are retrieved via similarity search (vector databases use tricks like inverted indexes to speed this up).
- Retrieved chunks are re-ranked to push the answer-bearing chunk near the top, then a Consolidator must compress them to fit LLM token limits and API rate limits — often chaining prompts (a reduction strategy) — before the Reader extracts a formatted answer from the generated text.
- RAG systems are hard to test because no ground-truth question/answer data exists for newly indexed documents, so test data must be discovered experimentally via synthetic data generation or minimal piloting — validation is feasible only during operation.

## 2. [[wiki/02-case-studies|Case Studies]]

**In one sentence:** Three RAG systems — a running literature-review tool, a running university tutor, and a BioASQ biomedical experiment — are described to ground the paper's catalogue of RAG failure points in real implementations across research, education, and biomedical domains.

- The three case studies deliberately span different scales: Cognitive Reviewer handles arbitrary-sized PDF collections, AI Tutor works over a fixed unit of 38 learning resources (videos, HTML, PDFs), and BioASQ is a large-scale experiment over 4,017 open-access biomedical documents.
- Cognitive Reviewer is the only case study that performs the Index process at run time (documents are uploaded by the user per session), which removes the possibility of development-time quality control and forces a robust data-processing pipeline.
- Two of the three case studies (Cognitive Reviewer and AI Tutor) are running systems in active use at Deakin University, which is why their scripts and data cannot be made public for confidentiality reasons, unlike BioASQ.
- AI Tutor was built in three months (August–November 2023) specifically to pilot in one unit of ~200 students starting 30 October 2023, making it a deployment-constrained, real-education use case rather than a benchmark.
- AI Tutor's only case study with a query rewriter uses chat history as context to resolve ambiguous follow-up requests such as "Explain this concept further," showing why rewriters matter in conversational RAG settings.
- AI Tutor and BioASQ both index heterogeneous content (videos and HTML in the former, scientific PDFs in the latter), and AI Tutor transcribes videos with the Whisper deep-learning model before chunking them.
- BioASQ is the only case study with pre-existing labelled question–answer pairs, which enables automated evaluation of generated answers with OpenAI's OpenEvals — something the other two, user-facing systems, cannot do at development time.
- In the BioASQ evaluation, 1,000 questions were generated against the indexed documents, 40 generated answers were manually inspected, and every answer OpenEvals flagged as incorrect was reviewed, revealing that the automated evaluator is more pessimistic than human raters in this domain (with the caveat that BioASQ is domain-specific and the human reviewers were not experts).
- The paper's failure-point catalogue (Section 5) is derived directly from these three case studies, and case studies marked with an asterisk in Table 1 are the running systems.

## 3. [[wiki/03-seven-failure-points|The Seven Failure Points]]

**In one sentence:** RAG systems fail at seven distinct points along the retrieval-and-generation pipeline — from content that simply isn't in the corpus, through ranking, context, extraction, format, specificity, and completeness mistakes — and engineers must design and calibrate for each one.

- **Missing Content:** the question has no answer in the indexed documents; the system should ideally say "I don't know", but can be fooled into fabricating a response for questions related to the content.
- **Missed the Top Ranked Documents:** the answer is in a document, but that document ranked below the top-K cutoff (K chosen based on performance) and was never returned to the next pipeline stage.
- **Not in Context (Consolidation Strategy Limitations):** the answer documents were retrieved from the database but dropped during consolidation, so they never made it into the LLM's generation context.
- **Not Extracted:** the answer is present in the context, yet the LLM fails to extract the correct answer — typically because of too much noise or contradicting information.
- **Wrong Format:** the question requires a specific output format (a table or list) and the LLM ignores the formatting instruction.
- **Incorrect Specificity:** the returned answer is not specific enough — or is too specific — for the user's need, e.g. an educational system that should give specific contextual content, not a bare answer, or a user who asks too general a question.
- **Incomplete:** the answer is not incorrect but omits some of the available information that was in the context, especially for multi-part questions spanning several documents.

## 4. [[wiki/04-lessons-and-future-research|Lessons & Future Research]]

**In one sentence:** The three case studies yield nine concrete lessons (summarised in Table 2) that identify RAG-system engineering as an ongoing, runtime-calibrated activity rather than a one-off build, and point to three open research frontiers — chunking & embeddings, RAG vs finetuning, and testing & monitoring.

- RAG-system validation is only feasible during operation: systems receive unknown, application-specific input at runtime (performance characteristics, jailbreaks, ambiguous queries) that offline test suites cannot exhaustively cover, so testing of performance characteristics is possible only at runtime.
- Robustness of a RAG system evolves over time rather than being designed in upfront: chunk size, embedding strategy, chunking strategy, retrieval strategy, consolidation strategy, context size, and prompts all require continuous calibration as documents, the LLM, and workloads change.
- Context and caching are leverable wins: a larger context window produced more accurate responses (8K vs 4K, contrary to prior "lost in the middle" results with GPT-3.5), and prepopulating a semantic cache with frequently asked questions drives down cost and latency.
- Safety and access control need explicit handling: jailbreak attacks bypass the RAG layer and hit the LLM's safety training (and research shows fine-tuning can reverse it, so fine-tuned RAG LLMs must be re-tested), while RAG gives the pragmatic route to per-user control over which chunks are accessible.
- Open-source embedding models perform as well as (and for small text, as well as) closed-source alternatives, and adding metadata such as file name and chunk number into the retrieved context measurably improves a reader's/LLM's ability to extract the needed information.
- Pipelines assembled from bespoke point solutions are suboptimal; end-to-end training enhances domain adaptation, and offline evaluation techniques such as G-Evals are promising but require labelled question–answer pairs that application-specific RAG systems often lack.
- Generating realistic, domain-relevant test questions (e.g. with LLMs that synthesise questions from multiple documents) and adopting self-adaptive-systems ideas for runtime monitoring remain open problems for RAG engineering.

## The argument in five moves

1. LLMs alone can't reliably answer domain-specific questions — they hallucinate and can't be steered other than by prompting.
2. RAG fixes this pragmatically: index documents once, retrieve relevant chunks at query time, and let the LLM generate from that grounded context — avoiding the cost and rigidity of fine-tuning.
3. But building three real RAG systems (research, education, biomedical) revealed that things go wrong at every pipeline stage, not just at retrieval.
4. Those failures cluster into exactly seven repeatable points — Missing Content, Missed Top Ranked, Not in Context, Not Extracted, Wrong Format, Incorrect Specificity, Incomplete — each traceable to one stage of the Index/Query pipeline.
5. Fixing them isn't a one-time engineering task: chunk size, embeddings, retrieval, and consolidation must be continuously recalibrated as the system operates, because RAG systems can't be validated offline before real usage begins.
6. The three deployments also yielded concrete wins (bigger context windows, semantic caching, metadata-in-context, open-source embeddings) that partially mitigate specific failure points.
7. What remains open is systematic: better chunking/embedding theory, a clearer RAG-vs-fine-tuning tradeoff analysis, and RAG-specific testing and monitoring practices — none of which yet have mature software-engineering tooling.
