> [[index|Wiki]] | [[summary|Summary]]

# Seven Failure Points When Engineering a Retrieval Augmented Generation System — In Plain Language

## What is this about?

Imagine asking a very well-read friend a question, but that friend only knows things they memorized years ago and can't look anything up. If you ask about last week's news, or about your company's internal policy document, they'll either say "I don't know" or — worse — confidently make something up that sounds right but isn't. That's roughly the problem with a large language model (LLM, the technology behind ChatGPT and similar tools) used on its own.

RAG — Retrieval Augmented Generation — solves this by giving the friend a librarian. Before answering, the librarian quickly finds the few most relevant pages from your actual documents and hands them to the friend, who then answers using those pages instead of guessing from memory. This paper is a field report from a team that built three such "friend + librarian" systems for real use — one for researchers reviewing papers, one for university students asking about course content, and one large experiment answering biomedical questions — and wrote down everything that went wrong.

## Why does it matter?

Anyone building a chatbot that answers questions from a company's documents, a product manual, or a knowledge base runs into the same problems this paper documents. Knowing the seven specific ways these systems break — before you build one — saves months of confusing debugging where "the AI just isn't very good" turns out to actually be one of seven very specific, fixable technical problems.

## How does it work?

A RAG system works in two phases, like organizing a filing cabinet and then using it:

1. **Filing (Index) — done once, ahead of time.** Every document gets cut into bite-sized pieces ("chunks"), and each piece gets a numerical fingerprint (an "embedding") that captures its meaning, not just its words. Piece and fingerprint go into a searchable database (a "vector database").
2. **Looking things up (Query) — done every time someone asks a question.** The question gets cleaned up (e.g. "what about that?" becomes "what about the pricing tier discussed earlier?" using chat history), turned into its own fingerprint, and matched against the filed pieces to find the closest ones. Those candidates get sorted by relevance, trimmed down to fit what the AI can read at once, and finally the AI reads them and writes an answer.

Six things can go wrong along this assembly line, one at each stage, plus one that's really a symptom of asking too much in one question:

1. **Missing Content** — the answer simply isn't filed anywhere; the AI should say "I don't know" but sometimes invents an answer instead.
2. **Missed the Top Ranked Documents** — the right piece was filed, but the search only looks at the top few results and the right piece didn't make that shortlist.
3. **Not in Context** — the right piece was found, but got cut when trimming everything down to fit what the AI can read.
4. **Not Extracted** — the right piece made it all the way to the AI, but it got lost among noise or contradictions and the AI didn't pull it out.
5. **Wrong Format** — the AI ignores an instruction like "answer as a table."
6. **Incorrect Specificity** — the answer is too vague or too detailed for what the person actually needed.
7. **Incomplete** — for a question with several parts, the AI answers some parts and silently drops others.

## Where can this be used?

Anywhere you're building a "chatbot over my documents" system: internal company wikis, customer support over product docs, research assistants, tutoring systems, legal or medical document Q&A. The seven failure points act as a debugging checklist — when an answer is wrong, you can localize which pipeline stage broke instead of guessing.

## Conclusions & takeaways

A month from now, remember this: RAG failures are not random "the AI is dumb" moments — they map to seven concrete pipeline stages, and each has its own fix (adjust chunk size, adjust how many results you retrieve, fix the trimming logic, clean up noisy context, tighten format instructions, calibrate answer length, or split compound questions). Also remember that these systems can't be fully tested before they go live — there's no way to know every question a real user will ask — so ongoing monitoring and recalibration is part of the job, not a one-time setup task. Limitation: this comes from three specific systems the authors built themselves, not from a large controlled study, so treat the seven points as a well-grounded starting checklist, not a proven-complete or universally-ranked list.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| RAG (Retrieval Augmented Generation) | Giving an AI a "librarian" that fetches relevant documents before it answers, instead of relying only on what it memorized during training. |
| LLM (Large Language Model) | The AI model itself (e.g. GPT-4) — the "friend" who writes the answer. |
| Chunking | Cutting a long document into smaller pieces so each piece can be searched and handled individually. |
| Embedding | A list of numbers that represents the *meaning* of a piece of text, so similar meanings end up as similar number-lists and can be matched by a computer. |
| Vector database | A specialized filing system built to quickly find the embeddings most similar to a given query. |
| Rewriter | A step that rephrases a raw user question into a clearer, self-contained search query, folding in prior chat context. |
| Retriever | The component that fetches the top-matching chunks for a given query. |
| Re-ranker | A step that re-orders retrieved chunks so the most useful one is more likely to be near the top. |
| Consolidator | A step that trims/compresses retrieved chunks down to fit the AI's reading limit ("token limit"). |
| Reader | The final step where the AI reads the trimmed context and writes the actual answer. |
| Hallucination | When an AI confidently states something false as if it were true. |
| Token limit | The maximum amount of text an AI model can read or write in one go. |
| Fine-tuning | Retraining an AI model itself on your own data, as an alternative to RAG. |
| Jailbreak | A trick prompt designed to bypass an AI's safety rules. |
