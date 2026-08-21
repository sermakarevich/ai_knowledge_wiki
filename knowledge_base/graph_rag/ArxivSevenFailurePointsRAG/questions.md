---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Seven Failure Points When Engineering a Retrieval Augmented Generation System

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. Why do the authors choose RAG over fine-tuning as the way to ground an LLM in domain-specific knowledge?

> [!tip]- Answer
> Fine-tuning requires curating a training dataset, retraining and serving a custom model, and re-running the whole process whenever the base model or the data changes — it bakes data into model weights. RAG instead retrieves relevant chunks at query time and lets the LLM generate from that context, so the knowledge base can be continuously updated by just re-indexing documents, without retraining. Both still carry tradeoffs around privacy/security, scalability, cost, and skills. See [[wiki/01-background-and-rag-pipeline|Background & RAG Pipeline]].

### Q2. Why does changing an embedding model force a full re-index, and what should that make an engineer check before committing to one?

> [!tip]- Answer
> Embeddings are the numerical representation chunks are matched against; if the embedding model changes, existing stored embeddings are no longer comparable to newly generated query embeddings, so every chunk must be re-embedded and re-indexed. Before committing, an engineer should validate the embedding choice against the application domain, expected question types, chunk size, and content structure — because the "same" question may need very different chunk granularity in different domains. See [[wiki/01-background-and-rag-pipeline|Background & RAG Pipeline]].

### Q3. Of the three case studies, which one cannot be evaluated automatically before deployment, and why?

> [!tip]- Answer
> Cognitive Reviewer and AI Tutor — the two user-facing, running systems — cannot be automatically evaluated at development time because they lack pre-existing labelled question-answer pairs; only BioASQ has such pairs (from its dataset), which is what let the authors run automated OpenEvals scoring against 1,000 generated answers. See [[wiki/02-case-studies|Case Studies]].

### Q4. What made Cognitive Reviewer's engineering problem harder than AI Tutor's or BioASQ's?

> [!tip]- Answer
> Cognitive Reviewer performs the Index process at *run time* — documents are uploaded by the researcher per session rather than indexed ahead of deployment — so there is no opportunity for development-time quality control over the documents being indexed; the data-processing pipeline itself must be robust to arbitrary user-supplied PDFs. See [[wiki/02-case-studies|Case Studies]].

### Q5. A user asks a compound question spanning three documents and the system answers only two parts correctly. Which failure point is this, and why is it distinct from "Not Extracted"?

> [!tip]- Answer
> This is **Incomplete** — the answer is not wrong, it just omits available information, typically for multi-part/multi-document questions. It differs from "Not Extracted," where the LLM has the right context but fails to pull out any correct answer at all; here the LLM successfully extracts *some* correct parts but stops short of the full compound answer. The paper's suggested fix is to ask compound questions as separate single questions rather than one prompt. See [[wiki/03-seven-failure-points|The Seven Failure Points]].

### Q6. A retrieved chunk contains the correct answer, but it's not in the LLM's final answer because too many documents came back and had to be trimmed to fit the prompt. Which failure point is this?

> [!tip]- Answer
> **Not in Context (Consolidation Strategy Limitations)** — the retriever worked correctly and found the answer-bearing chunk, but the consolidation/reduction step used to fit results within the token limit dropped it before it reached the LLM's generation context. This is distinct from "Missed the Top Ranked Documents," which is a retrieval/ranking-cutoff failure, not a consolidation failure. See [[wiki/03-seven-failure-points|The Seven Failure Points]].

### Q7. Why does the paper claim RAG systems can only be validated "during operation," not fully tested beforehand?

> [!tip]- Answer
> Because newly indexed documents have no pre-existing (question, answer) ground truth, so there's no offline test set to check retrieval and generation quality against before going live. Test data has to be discovered experimentally — via synthetic question generation or minimal piloting — and even then, real users at runtime will surface unknown inputs, ambiguous phrasing, and jailbreak attempts that no offline suite anticipated. This is why the paper frames RAG robustness as continuous calibration rather than a one-time build. See [[wiki/04-lessons-and-future-research|Lessons & Future Research]].

### Q8. This paper draws its failure-point catalogue from three case studies rather than a controlled benchmark. What is the strongest limitation this creates, and does that undermine the paper's usefulness?

> [!tip]- Answer
> The main limitation is that the seven failure points and nine lessons are qualitative generalizations from three specific systems built by one team, with no claim about which failure points are most frequent, no inter-rater reliability check on the failure categorization, and no comparison against alternative RAG architectures. That weakens any claim to completeness or universal ranking. It does not undermine the paper's practical usefulness, though: as a debugging checklist mapped cleanly onto pipeline stages, the catalogue is reusable regardless of whether it is exhaustive — see [[critical_thinking|Critical Analysis]] for the full assessment.
