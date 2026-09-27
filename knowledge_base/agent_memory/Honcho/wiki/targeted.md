> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Targeted Answers: the Four Deep Questions
**In one sentence:** This page answers the four hard questions about Honcho — how it differs from simpler memory tools, what its per-message reasoning step costs, what its test scores really mean, and when to choose it over building your own storage.
## Key points
- Honcho reasons over everything you store into growing peer representations, while mem0-style tools only save facts and return matches for your app to assemble, and RAG (Retrieval-Augmented Generation, a method that cuts text into chunks, turns them into number vectors, and returns the closest chunks) only finds what was said word-for-word.
- Every message triggers an async (background, not blocking the reply) Neuromancer step that extracts explicit facts and logical conclusions; storage and lookup are vendor-reported as free and fast (~200 milliseconds), and you pay $2.00 per million input tokens for that reasoning plus $0.001–$0.50 per question asked.
- The headline test scores are all vendor-reported: LongMemEval-S 90.4%, LoCoMo 89.9%, and BEAM scores around 0.63 down to 0.41 at 10 million tokens, each measured against a weak no-memory baseline and judged by an LLM (Large Language Model, the AI model that reads and writes text), so independent re-testing is still needed.
- Choose Honcho when memory quality across many chats is the product feature, choose Postgres plus pgvector when data must stay in your own VPC (Virtual Private Cloud, your own private section of the cloud) or queries are simple, and choose a graph store when your data has stable people-places-things links to walk step by step.
---
## How does Honcho differ from store-and-retrieve memory (mem0-style) and from RAG?
Store-and-retrieve means: save a fact, then search for it later. A mem0-style tool reads each message, pulls out facts (for example "user likes tea"), saves them in a database, and its search function returns the closest matches. Your app code must then paste those matches into the prompt (the text sent to the AI model) by hand.

Honcho instead builds a living picture of each peer (a peer is any person, agent, or project that persists over time). The data model is Workspace (top-level isolated area, for example one per customer) holding Peers plus Sessions (one chat thread) holding Messages (one chat entry). Two observation settings control learning: observe_me learns from all of a peer's own messages, and observe_others lets one peer form a view of another peer only from chats they shared, so there is no all-seeing mind.

On every message Honcho runs reasoning that compounds over time:

- Explicit statements: what was directly said.
- Deductive conclusions: what must logically follow.
- Inductive conclusions: patterns seen in at least two cases, with a confidence score.
- Abductive conclusions: best guesses under uncertainty.
- Session summaries (short every about 20 messages, long every about 60) and peer cards (short biography facts such as name, job, interests).

These live in vector collections (searchable stores of number vectors), one collection per observer-observed pair. The read path then returns finished work, not raw matches: the context function returns a ready blend of summary plus recent messages, and the chat function is an agent that prefetches conclusions and writes a cited answer with observer-to-observed labels.

RAG (Retrieval-Augmented Generation, defined above) retrieves only what was explicitly written. It misses hidden meaning, breaks when facts change ("I moved from Paris to Rome"), and at large scale forces you to paste 100,000 raw tokens (pieces of words the model reads) into the prompt. Honcho is reasoning-first: it writes down the logic chain once, resolves contradictions during quiet consolidation, and then reads back small token-efficient conclusions. The vendor-reported saving is 60–90% fewer tokens per question.

| Feature | mem0-style store-and-retrieve | Plain RAG | Honcho |
|---|---|---|---|
| What is stored | Isolated facts | Text chunks with vectors | Messages plus conclusions, summaries, peer cards |
| What query returns | Matching facts, app assembles prompt | Matching chunks, app assembles prompt | Ready context or synthesized cited answer |
| Contradictions and updates | Left to app code | Brittle, old chunk can win | Dedicated consolidation step resolves them |
| Hidden patterns and guesses | No | No | Yes, inductive and abductive conclusions |
| Migration path | N/A (not applicable) | Re-chunk data | Vendor migration guide: import raw messages for best quality, or import conclusions directly for speed |

## What is the Neuromancer reasoning step per message and what does it cost in latency/tokens?
Neuromancer is Honcho's family of small custom reasoning models built for formal logic work. The first member, Neuromancer XR, is a fine-tune (a base model retrained on extra examples) of Qwen3-8B that handles explicit plus deductive extraction. The vendor-reported claim is that it is more reliable and cheaper and faster than using a large frontier model for the same job. In the vendor-reported LoCoMo ablation (a test where only the extraction model is swapped), XR scored 86.9% overall against 80.0% for Claude 4 Sonnet and 69.6% for the plain Qwen3-8B base, with the final answer step always done by Claude 4 Sonnet.

The per-message flow has a fast sync (immediate) part and a slow async (background) part:

1. Sync write: the message is saved in PostgreSQL (the main database) and a reasoning task is queued. The API (Application Programming Interface, the way your code talks to Honcho) returns at once. Context lookup is vendor-reported at about 200 milliseconds and is free and unlimited.
2. Deriver, async per message: Neuromancer XR reads the message in order (each peer has its own queue so order is kept) and writes explicit facts plus deductive conclusions.
3. Summarizer, async per message: updates the rolling short and long session summaries.
4. Dreamer, periodic and experimental: a quiet consolidation that runs only when there are 50 or more new conclusions since the last dream, at least 8 hours have passed, dreaming is enabled, and the peer has been idle 60 minutes (new activity cancels it; a manual schedule call skips the thresholds). Two specialists run: Deduction (knowledge updates, implications, contradiction fixes, peer-card updates) and Induction (patterns needing at least 2 supporting conclusions).
5. Query: the Dialectic agent answers. One-peer chat is anchored to a single observer-observed pair and prefetches conclusions; workspace-wide chat has no anchor and must search pair by pair with attribution labels.

Costs are vendor-reported, dated 2026-09-10. Ingestion, meaning storage plus Neuromancer reasoning, is $2.00 per million input tokens. Lookup with the context function and dreaming are included. You pay separately per question by reasoning level (which controls model choice, tools, thinking budget, and steps):

| Level | Vendor-reported price per query | Behavior |
|---|---|---|
| minimal | $0.001 | Instant, single semantic (meaning-based) search |
| low (default) | $0.01 | Standard answer |
| medium | $0.05 | Deeper reasoning |
| high | $0.10 | Async (background) job |
| max | $0.50 | Async research-grade job |

Batch uploads allow up to 100 messages per call. Queue status can be polled and webhooks (automatic callbacks on completion) notify when background work finishes. Signup includes $100 in free credits, vendor-reported, and the quickstart tutorial costs about $0.04. API (defined above) keys are scoped by role: admin, workspace, peer, or session, with workspace-wide chat needing a workspace-level key or higher.

## What do the LongMemEval/LoCoMo/BEAM eval claims actually measure — what is the baseline?
All scores below are vendor-reported and come from the vendor's open test harness. Each benchmark (a standard test set) checks long-term memory with questions over very long histories, graded by an LLM (Large Language Model, defined above) acting as judge. Judge choice alone can move scores by 15–25 points, so the baseline (the simple system Honcho is compared against) matters more than the headline number.

LongMemEval-S measures question answering over 500 conversations of about 115,000 tokens each. The baseline is plain Claude Haiku 4.5 with no memory layer, at 62.6% overall. Honcho is vendor-reported at 90.4% overall (a gain of 27.8 points), with single-session preference 90.0% against 23.3% and multi-session reasoning 85.0% against 46.6%.

LoCoMo measures four question types: single-hop (answer in one place), temporal (time and order), multi-hop (combine several facts), and open-domain plus adversarial (tricky or off-topic questions). The homepage headline is vendor-reported 89.9%. A separate vendor-reported ablation keeps the final answer model fixed (always Claude 4 Sonnet) and swaps only the conclusion-writing model: Neuromancer XR 86.9% overall (single 81.0, temporal 89.4, multi 84.4, open 88.4), Claude 4 Sonnet 80.0%, plain Qwen3-8B 69.6%. For context, outside reports vary widely by judge and protocol: the mem0 paper reports mem0 at 66.9% against 72.9% full-context, and a third-party replication reports Zep 58.4%, Letta 74%, Omi 86.6%, and mem0's own platform at 92.5%.

BEAM (Beyond a Million Tokens, an ICLR 2026 test set — ICLR is the International Conference on Learning Representations) measures 10 memory skills over 100 conversations and 2,000 questions at scales of 128K, 500K, 1M, and 10M tokens. The baseline method is called LIGHT. Honcho is vendor-reported at about 0.630 at 100K, 0.646 at 500K, 0.618 at 1M, and 0.409 at 10M. Outside context: Omi reports 55–62.5% at 100K with LIGHT near 34% at 1M and the best outside system near 73% at 100K.

Caveats: the vendor picks favorable baselines, the "Pareto dominant on accuracy, cost, speed, and tokens" line is a vendor-reported marketing claim, and the open harness helps but independent replication is still pending.

## When should a backend engineer choose Honcho vs Postgres+pgvector vs a graph store?
Postgres plus pgvector means storing your own text chunks and number vectors inside your own Postgres database and writing search yourself. You get full control, data ownership, and low cost at small scale, but you build everything: chunking, embeddings (text turned into number vectors), retrieval, summaries, contradiction handling, and your own tests. Teams call this the "RAG (Retrieval-Augmented Generation, defined above) treadmill" because every quality fix is your work.

A graph store (for example mem0-graph, Zep-style, or GraphRAG) saves explicit entity-and-relation triples such as "Sergii — works on — Honcho". Graphs are strong for multi-step walks ("who works with whom on what") and for explaining an answer by showing the path. The price is upfront schema (structure) design, extraction mistakes that pollute the graph, and harder updates when facts change.

Honcho sits between them: logic conclusions in pair-scoped vector collections, with no schema to design upfront. It wins when the product needs memory of who someone is and how they change across many open-ended chats, including contradictions and guesses.

| Signal | Choose Honcho | Choose Postgres plus pgvector | Choose a graph store |
|---|---|---|---|
| Data must stay in your VPC (Virtual Private Cloud, defined above) | No, unless self-hosted | Yes | Only if graph runs in your VPC |
| Queries are simple similarity over small data | Overkill | Yes | Overkill |
| Memory across sessions is the selling point | Yes | You rebuild it yourself | Partial, only for linked entities |
| Domain has stable entities and multi-hop walks | Possible | Weak | Yes |
| Team wants fastest prototype | Yes, managed cloud plus $100 vendor-reported credits | Slower, you build retrieval | Slower, you design schema |

Rule of thumb from the research brief: prototype on Honcho managed for speed, stay if memory quality is what makes your product different, and self-host the core (AGPL (Affero General Public License, an open-source license that requires sharing changes to network users) licensed, runs with Docker, bring your own model key) or build DIY (do-it-yourself) pgvector if data-residency rules or cost at very large scale dominate.
**Covers:** targeted questions across all docs pages (retrieved 2026-09-10)
