> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Seven Failure Points of RAG Systems

**In one sentence:** RAG systems fail at seven distinct points along the retrieval-and-generation pipeline — from content that simply isn't in the corpus, through ranking, context, extraction, format, specificity, and completeness mistakes — and engineers must design and calibrate for each one.

## Key points

- **Missing Content:** the question has no answer in the indexed documents; the system should ideally say "I don't know", but can be fooled into fabricating a response for questions related to the content.
- **Missed the Top Ranked Documents:** the answer is in a document, but that document ranked below the top-K cutoff (K chosen based on performance) and was never returned to the next pipeline stage.
- **Not in Context (Consolidation Strategy Limitations):** the answer documents were retrieved from the database but dropped during consolidation, so they never made it into the LLM's generation context.
- **Not Extracted:** the answer is present in the context, yet the LLM fails to extract the correct answer — typically because of too much noise or contradicting information.
- **Wrong Format:** the question requires a specific output format (a table or list) and the LLM ignores the formatting instruction.
- **Incorrect Specificity:** the returned answer is not specific enough — or is too specific — for the user's need, e.g. an educational system that should give specific contextual content, not a bare answer, or a user who asks too general a question.
- **Incomplete:** the answer is not incorrect but omits some of the available information that was in the context, especially for multi-part questions spanning several documents.

---

## 1. Missing Content

The first failure case is asking a question that cannot be answered from the available documents. In the happy path, a RAG system responds with something like "Sorry, I don't know". However, for questions that are *related to* the indexed content but nevertheless lack an answer, the system can be fooled into producing a (hallucinated) response. This is the most fundamental failure point: retrieval finds plausible-looking material, and the generative component turns proximity into a false answer.

## 2. Missed the Top Ranked Documents

The answer to the question is in the document collection, but the containing document did not rank highly enough to be passed on to the user. In theory, all documents are ranked and used in the next steps of the pipeline. In practice, though, only the top-*K* documents are returned, where *K* is a value selected based on performance. Any document ranking below *K* is invisible to the generation stage regardless of how relevant it actually is — a pure ranking/cutoff failure.

## 3. Not in Context — Consolidation Strategy Limitations

Documents that contain the answer were successfully retrieved from the database, but they did not make it into the context used for generating the answer. This occurs when many documents are returned from the database and a consolidation process takes place to reduce them to what can fit the prompt. The retriever worked; the consolidation/reduction strategy silently discarded the evidence, so the LLM could not extract an answer it never saw.

## 4. Not Extracted

Here the answer *is* present in the context, but the large language model fails to extract the correct answer from it. This typically occurs when there is too much noise or contradicting information in the context, so the correct information is buried or cancelled out by competing content. The failure lies in the reader/extraction stage of the pipeline, not in retrieval.

## 5. Wrong Format

The question involves extracting information in a certain format — such as a table or a list — and the large language model ignores the instruction and returns a differently formatted response. This is a failure of instruction adherence: the content may be right, but the output format does not match what the question (or the consuming application) requires.

## 6. Incorrect Specificity

The answer is returned in the response, but it is not specific enough — or is too specific — to address the user's need. This occurs when the RAG system designers have a desired outcome for a given type of question (for example, teachers serving students), in which case specific educational content should be provided *with* the answer, not just the bare answer. Incorrect specificity also occurs on the user side, when users are unsure how to phrase a question and end up asking too generally.

## 7. Incomplete

Incomplete answers are *not* incorrect, but they miss some of the information even though that information was present in the context and available for extraction. A typical example is a question such as "What are the key points covered in documents A, B, and C?" — a multi-document, multi-part question that the system partially answers. The paper's suggested approach is to ask such compound questions separately rather than expecting one prompt to exhaustively cover multiple sources.

**Covers:** Section 5 (Failure Points of RAG Systems)
