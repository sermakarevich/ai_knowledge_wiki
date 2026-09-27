> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Comparisons: mem0, RAG, pgvector, Graph Stores
**In one sentence:** Honcho trades simple storage and manual lookup work for built-in reasoning that returns ready-to-use memory, which pays off when agents must stay consistent across many sessions.
## Key points
- Compared with mem0-style store-and-retrieve, Honcho trades a simple facts database for compounding reasoning, but you accept async (background, not instant) processing and a new peer-session mental model.
- Compared with mem0-style search assembly, Honcho trades manual context building for ready `context()` and `chat()` calls, at the cost of less direct control over exactly which facts are inserted.
- Compared with RAG (Retrieval-Augmented Generation, a method where the AI looks up text chunks before answering), Honcho trades explicit recall of what was said for inferred conclusions about what it means, which helps with implicit facts but adds model-reasoning cost.
- Compared with RAG (Retrieval-Augmented Generation, a method where the AI looks up text chunks before answering), Honcho trades raw-chunk stuffing for token-efficient conclusions, with vendor-reported 60-90% token savings that still need independent confirmation.
- Compared with Postgres plus pgvector DIY (Do-It-Yourself storage where you build your own search over a regular database plus vector extension), Honcho trades full control, ownership, and cheap small-scale start for freedom from building chunking, embeddings, contradiction handling, and evals yourself.
- Compared with graph stores such as mem0-graph, Zep-style stores, or GraphRAG (Graph Retrieval-Augmented Generation, RAG over an entity-relation graph), Honcho trades explicit schema (predefined entity types) plus traversals for schema-free logic conclusions in pair-scoped vectors, gaining flexibility but losing explicit graph explainability.
- As a rule of thumb for a backend engineer, prototype memory-heavy features on managed Honcho and only move to self-hosted Honcho or Postgres plus pgvector DIY when data-residency (data must stay in your own servers), cost at scale, or simple similarity queries dominate.
---
## Honcho vs mem0-style store-and-retrieve
An API (Application Programming Interface, a way for programs to talk to a service) for mem0-style memory works like a facts database: you save facts with `add`, you look them up with `search`, and your own code assembles the answer context.
Honcho works differently. You store messages in sessions between peers, the Deriver powered by Neuromancer (Plastic Labs' family of small custom reasoning models for formal logic, here Neuromancer XR for extracting explicit statements and deductive conclusions) reasons over them in the background, and later calls return finished products: `context()` returns ready context with summaries plus recent messages, and `chat()` returns a synthesized answer.
In short: mem0 stores what you said, Honcho also stores what follows from what you said — explicit statements plus deductive, inductive, and abductive conclusions that build on each other over time.
Migration paths, adapted from the official migration guide:
- Best quality: import raw messages. This gives Honcho full conversation order, speaker attribution, and session boundaries, so it can build session summaries, peer cards (stable biographical facts like name and preferences), and layered conclusions.
- Fast start: import existing mem0 memories directly as conclusions. This skips re-reasoning and makes old facts searchable at once, but you lose summaries and deductive depth.
API (Application Programming Interface, a way for programs to talk to a service) comparison, adapted from the migration doc:
| Operation | mem0 | Honcho | Notes |
| --- | --- | --- | --- |
| Initialize | `MemoryClient(api_key=...)` | `Honcho(api_key=...)` | Both use an API key |
| Identity | `user_id` string parameter | `peer = honcho.peer("id")` | A peer can be a user, an agent, or a group |
| Add messages | `client.add(messages, user_id=...)` | `session.add_messages([peer.message(...)])` | Honcho is session-scoped and triggers background reasoning |
| Add conclusions | — | `peer.conclusions.create([...])` | Direct fact import, no reasoning step |
| Search | `client.search(query, filters={"user_id": ...})` | `peer.search(query)` or `peer.conclusions.query(...)` | Honcho search is scoped to a peer or session |
| List all | `client.get_all(filters={"user_id": ...})` | `session.messages()` or `peer.conclusions.list()` | Messages are raw history, conclusions are reasoned outputs |
| Update | `client.update(memory_id, data=...)` | `honcho.update_message(message, metadata=...)` | Honcho updates message metadata only |
| Delete | `client.delete(memory_id)` | `peer.conclusions.delete(id)` or `session.delete()` | Delete one conclusion or a whole session |
Honcho-only capabilities with no mem0 equivalent:
| Honcho method | What it does | When to use it |
| --- | --- | --- |
| `session.context()` with `.to_openai()` / `.to_anthropic()` | Returns ready context with token (word-piece billing unit) limits and auto-included summaries | Drop-in prompt context without manual assembly |
| `peer.chat()` / `honcho.chat()` | Reasoning query that synthesizes a natural-language answer | Ask "what do we know" instead of fetching raw facts |
| `peer.get_card()` / `peer.set_card()` | Stable biographical facts | User profiles and personalization |
| `session.representation(peer)` | Cached view of a peer's state and intentions | Real-time adaptation |
| `session.summaries()` | Auto short summary every ~20 messages, long summary every ~60 | Conversation continuity |
| `SessionPeerConfig` observation settings | Controls who learns about whom (`observe_me`, `observe_others`) | Privacy and role-based learning |
Pricing difference to know: mem0 charges on retrieval (you pay to access your own data), while Honcho storage plus retrieval is free and you pay for reasoning — ingestion plus Neuromancer reasoning at vendor-reported $2.00 per million input tokens, and per-query reasoning from $0.001 to $0.50 by level (vendor-reported, verify-date 2026-09-10).
## Honcho vs RAG (Retrieval-Augmented Generation)
RAG (Retrieval-Augmented Generation, a method where the AI looks up text chunks before answering) means: split documents into chunks, turn them into embeddings (number lists that capture meaning), fetch top matches, and stuff them into the prompt of an LLM (Large Language Model, the AI model that writes the answer).
That works for explicit recall — "find the sentence where the user said X" — but it struggles when the answer was never stated directly, when facts contradict or change over time, and when the model must predict under uncertainty.
Honcho is reasoning-first rather than retrieval-first. Neuromancer builds a logic scaffolding: explicit statements, deductive conclusions (what must follow), inductive conclusions (patterns seen at least twice), and abductive conclusions (best guesses under uncertainty), plus contradiction reconciliation during dreaming (periodic background consolidation). A query then reads compact conclusions instead of 100K tokens (basic units the model bills and processes) of raw history.
Tradeoff: RAG is simple, transparent, and cheap to understand — you can inspect the exact chunks returned. Honcho is more token-efficient and better at latent (hidden, implied) state, but you trust background inference you did not hand-assemble, and you pay per reasoning step.
## Honcho vs Postgres + pgvector DIY
Postgres plus pgvector DIY means you own everything: a Postgres database plus the pgvector extension for similarity search, your own chunking, your own embeddings, your own summarizer, and your data stays in your own VPC (Virtual Private Cloud, your isolated network area in the cloud).
That is attractive when scale is small, queries are simple similarity ("find near-duplicates"), the team already owns retrieval code, or data must not leave your servers.
The cost is the RAG treadmill: you must build and maintain chunking, embedding refresh, retrieval tuning, summary jobs, contradiction handling, and evals (tests that score memory quality) yourself. Most teams underestimate update logic — what happens when a user changes their mind — and long-horizon evals.
Choose Honcho when cross-session statefulness is the product requirement and memory quality is the differentiator. Choose Postgres plus pgvector when control, ownership, and cheap small-scale operation matter more than reasoning depth.
Self-hosting is a middle path: the Honcho core is open source under AGPL-3.0 (Affero General Public License version 3.0, a license that requires sharing source if you run it as a network service), runnable with Docker via `honcho start --setup` with your own LLM (Large Language Model, the AI model that writes the answer) key using an SDK (Software Development Kit, a library for talking to the service).
## Honcho vs graph stores
Graph stores — mem0-graph, Zep-style temporal graphs, GraphRAG (Graph Retrieval-Augmented Generation, RAG over an entity-relation graph) — store explicit entities and relations ("Alex — works at — Bank", "Alex — prefers — concise answers") and answer by traversing (walking) those links. That is strong for stable domains with clear entities and multi-hop questions, and the path itself is explainable.
The price is schema work: you design entity and relation types upfront, extraction errors pollute the graph, and updates require deletes, merges, and conflict rules.
Honcho skips upfront schema. Conclusions are stored in vector collections (search indexes of meaning-vectors), one collection per observer-observed peer pair, so perspectives stay separate — what A knows about B is stored apart from what B knows about A. There is no graph traversal, only semantic search over logic conclusions plus session summaries.
Choose a graph when your domain has stable entities and relations and you need traversals and audit trails. Choose Honcho when you model identity and behavior over open-ended dialogue where you cannot list all relation types in advance.
## Decision guide for a backend engineer
1. Start on managed Honcho if you need cross-session memory fast: new accounts include vendor-reported $100 free credits, and the quickstart costs about $0.04 vendor-reported.
2. Stay on Honcho if memory quality wins customers: compounding representations, ready `context()`, and `peer.chat()` reasoning save prompt assembly code and tokens.
3. Consider self-hosted Honcho (AGPL-3.0, Docker, bring your own model key) if data-residency or long-run cost dominates but you still want the reasoning model.
4. Choose Postgres plus pgvector DIY only if queries stay simple, scale stays small, data must remain in your VPC (Virtual Private Cloud, your isolated network area in the cloud), or your team already owns a tuned retrieval stack.
5. Choose a graph store only if your domain is entity-heavy with stable relations and you need explicit multi-hop traversals.
All accuracy and token-saving numbers above are vendor-reported and lack independent replication at time of writing; treat the open benchmark harness as provenance, not proof.
**Covers:** mem0 migration guide + architecture/reasoning docs (retrieved 2026-09-10)
