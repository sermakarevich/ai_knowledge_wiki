> [[index|Wiki]] | [[summary|Summary]]

# Honcho — Digest

The whole source at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-concepts|Concepts: Workspaces, Peers, Sessions, Messages]]
**In one sentence:** Honcho stores small interaction records inside threads inside an isolated project area, then reasons over them to maintain a living learned profile for each person or agent.
- A Workspace is the top-level isolated project area, used for example for development versus staging versus production or for one customer each, and login keys are issued at this level.
- A Peer is any long-lived entity that changes over time, such as a user, an agent, a group, a project, or an idea, with one unique ID (Identifier, a unique name) per Workspace, and everything Honcho learns is stored as that peer's representation.
- A Session is one interaction thread between peers with a start and an end, such as one support ticket or one meeting, and sessions are the unit of visibility that controls what history can be recalled together.
- A Message is the basic unit of data in a session, always linked to one peer and ordered by time, and each new message triggers background reasoning; bulk import allows up to 100 messages in one API (Application Programming Interface, a way for programs to talk to Honcho) call.
- A Representation is Honcho's learned understanding of a peer, made of logic conclusions plus rolling session summaries plus a short peer card with basic facts, stored in vector collections with one collection per observer-and-observed pair.
- Observation has two modes: observe_me builds Honcho's own view of a peer from all of that peer's messages and is on by default, while observe_others lets one peer build a limited view of another peer using only sessions they shared, which keeps simulated viewpoints from becoming all-knowing.
- Settings cascade from Workspace to Peer to Session, so a default set at the Workspace level can be replaced for one peer or one session, and named scopes group sessions to bound recall to only those sessions.

## 2. [[wiki/02-quickstart-integration|Quickstart and Integration]]
**In one sentence:** You install a Honcho SDK (Software Development Kit, a ready-made code library), connect with an API (Application Programming Interface, a key that lets your code talk to Honcho) key, save messages into workspaces, peers, and sessions, then ask questions or pull context for your LLM (Large Language Model, the AI model that writes answers).
- Install with `uv add honcho-ai` or `pip install honcho-ai` for Python, or `npm install @honcho-ai/sdk` (also `yarn add @honcho-ai/sdk` or `pnpm add @honcho-ai/sdk`) for TypeScript (TypeScript, a typed version of JavaScript).
- Get an API (Application Programming Interface) key at app.honcho.dev under API KEYS; every new account gets $100 in free credits (vendor-reported), and the full quickstart example costs about $0.04 to run (vendor-reported).
- A Workspace is the top-level isolation space, a Peer is any lasting entity such as a user or assistant, and a Session is one interaction thread; the quickstart creates workspace `first-honcho-test`, peers `user` and `assistant`, and ingests a 14-message example across 4 sessions.
- Use `peer.chat()` to ask about one peer and `honcho.chat()` to ask across every peer in a workspace, because peer chat is anchored to one observer-observed pair while workspace chat searches first and reads pair by pair.
- Use `session.context()` to get ready-to-use history with token budgets such as `tokens=1500` or `tokens=2000`, then convert with `to_openai()` or `to_anthropic()` for direct use with OpenAI or Anthropic (two LLM providers) models; storage and retrieval with context() is free and fast at about 200 milliseconds (vendor-reported), you pay only for reasoning.
- API (Application Programming Interface) keys are scoped as admin, workspace, peer, or session, where workspace chat needs a workspace-level or higher key, and the context() `scope` option needs a workspace-level or admin-level key and cannot be combined with `peer_perspective`.
- Self-host locally with `uv tool install honcho-cli` then `honcho start --setup`, which uses Docker (a tool that runs packaged software containers) plus your own LLM (Large Language Model) provider key, instead of the managed cloud at app.honcho.dev.
- Extend through an MCP (Model Context Protocol, a standard way for AI tools to connect) server plus `npx skills add plastic-labs/honcho`, plugins for Claude Code, Codex, Cursor, OpenCode, OpenClaw, DeepSeek Harness, Hermes, Zo, Paperclip, and SillyTavern, frameworks such as LangGraph, CrewAI, Vercel AI SDK, and n8n, plus file uploads as messages, webhooks (automatic notifications) on job completion, and queue-status checks for background reasoning.

## 3. [[wiki/03-reasoning-architecture|Reasoning Architecture: Neuromancer, Deriver, Dreamer, Dialectic]]
**In one sentence:** Honcho treats memory as reasoning, using the Neuromancer model family to turn messages into formal-logic conclusions in the background and a query agent to assemble answers on demand.
- Neuromancer is Honcho's family of small custom reasoning models, where Neuromancer XR is a fine-tune of Qwen3-8B that extracts explicit statements and deductive conclusions (vendor-reported to beat frontier models on this task while running cheaper and faster).
- The Deriver is the per-message background worker that runs Neuromancer over each new message to produce explicit and deductive conclusions, keeping chronological order per peer through session queues.
- The Dreamer is the periodic consolidation worker that revisits stored conclusions with a deduction specialist for updates and contradictions and an induction specialist for patterns, and it only runs when all schedule conditions are met.
- Dreamer scheduling is vendor-reported as: at least 50 new conclusions since the last dream, at least 8 hours cooldown since the last dream, plus a 60-minute idle timer that resets if new messages arrive.
- The Dialectic is the query-time agent that answers peer.chat() and honcho.chat() requests by prefetching relevant conclusions and synthesizing a response, rather than returning raw matches.
- Query reasoning levels control cost and depth from minimal ($0.001 per query, single semantic search) through low ($0.01, default), medium ($0.05), high ($0.10, async (asynchronous, runs in background)), to max ($0.50, async research-grade).
- Storage and retrieval with context() is vendor-reported as free and unlimited, so users pay for ingestion reasoning at $2.00 per million tokens and for Dialectic queries, not for keeping data.

## 4. [[wiki/04-evals|Evaluations: LongMemEval, LoCoMo, BEAM]]
**In one sentence:** Honcho's maker reports top scores on three long-memory tests for LLM (Large Language Model, an AI system that reads and writes text) agents, with 90.4% on LongMemEval-S, 89.9% on LoCoMo, and 0.630 to 0.409 across BEAM scales, plus 60-90% token savings.
- On LongMemEval-S (500 long chats of about 115,000 tokens each), Honcho scored 90.4% vendor-reported, which is 27.8 percentage points above the Claude Haiku 4.5 baseline of 62.6% vendor-reported.
- On LongMemEval-S parts, Honcho scored 90.0% vendor-reported on single-session preference against 23.3% for the baseline, and 85.0% vendor-reported on multi-session reasoning against 46.6% for the baseline.
- On LoCoMo (a long-conversation question-answering test with single-hop, temporal, multi-hop, and open-domain questions), Honcho scored 89.9% vendor-reported overall.
- The custom XR reasoning model (Neuromancer XR, a fine-tune of Qwen3-8B) scored 86.9% vendor-reported overall as the conclusion-writing model, against 80.0% for Claude 4 Sonnet and 69.6% for Qwen3-8B base, with final answers always from Claude 4 Sonnet.
- On BEAM (Beyond a Million Tokens, an ICLR 2026 test with 100 conversations, 2,000 questions, and 10 memory skills), Honcho scored 0.630 at 100K tokens, 0.646 at 500K, 0.618 at 1M, and 0.409 at 10M, all vendor-reported.
- Outside reports give useful context: the mem0 paper reports 66.9% for mem0 and 72.9% for full context on LoCoMo, while a third-party Omi repeat reports 58.4% for Zep, 74% for Letta, 86.6% for Omi, and 92.5% vendor-reported for the closed mem0 platform.
- Scores move by 15 to 25 percentage points when the LLM judge or test setup changes, so vendor baseline choices matter; Honcho's maker publishes an open test kit at github.com/plastic-labs/honcho-benchmarks and claims 60-90% token savings, but independent repeats are still pending.

## 5. [[wiki/05-pricing-limits|Pricing and Limits]]
**In one sentence:** Honcho charges for input and thinking, not for storage — you pay $2.00 per million input tokens for memory and $0.001 to $0.50 per question for reasoning, while reading saved memory is free.
- HONCHO MEMORY ingestion costs $2.00 per million input tokens (vendor-reported), and that single fee covers storage plus Neuromancer reasoning and dreaming.
- Reading memory with context() is free and unlimited (vendor-reported), with about 200 milliseconds response time for a ready-made session context.
- HONCHO REASONING has 5 per-question tiers (vendor-reported): minimal $0.001, low $0.01, medium $0.05, high $0.10, and max $0.50.
- New accounts get $100 in free credits (vendor-reported), and the official quickstart tutorial costs about $0.04 to run.
- Startups that raised less than $5 million get $1,000 in credits plus lower prices (vendor-reported), and large companies get custom enterprise plans with forward-deployed engineers.
- Honcho's rule is "storage plus retrieval is free, pay for reasoning", while mem0-style rivals charge a fee each time you search your own saved data.
- Operational limits are strict numbers: at most 100 messages per batch upload, dream consolidation needs 50 or more new conclusions plus an 8-hour cooldown plus a 60-minute idle wait, and high/max questions run async (asynchronous, in the background) with queue-status checks and webhooks (automatic completion alerts).
- Access keys come in 4 scopes — admin, workspace, peer, and session — and workspace-wide chat needs a workspace-level key or higher, while self-hosting the open core is free under AGPL (Affero General Public License, a license that requires sharing changes if you run it as a service).

## 6. [[wiki/06-comparisons|Comparisons: mem0, RAG, pgvector, Graph Stores]]
**In one sentence:** Honcho trades simple storage and manual lookup work for built-in reasoning that returns ready-to-use memory, which pays off when agents must stay consistent across many sessions.
- Compared with mem0-style store-and-retrieve, Honcho trades a simple facts database for compounding reasoning, but you accept async (background, not instant) processing and a new peer-session mental model.
- Compared with mem0-style search assembly, Honcho trades manual context building for ready `context()` and `chat()` calls, at the cost of less direct control over exactly which facts are inserted.
- Compared with RAG (Retrieval-Augmented Generation, a method where the AI looks up text chunks before answering), Honcho trades explicit recall of what was said for inferred conclusions about what it means, which helps with implicit facts but adds model-reasoning cost.
- Compared with RAG (Retrieval-Augmented Generation, a method where the AI looks up text chunks before answering), Honcho trades raw-chunk stuffing for token-efficient conclusions, with vendor-reported 60-90% token savings that still need independent confirmation.
- Compared with Postgres plus pgvector DIY (Do-It-Yourself storage where you build your own search over a regular database plus vector extension), Honcho trades full control, ownership, and cheap small-scale start for freedom from building chunking, embeddings, contradiction handling, and evals yourself.
- Compared with graph stores such as mem0-graph, Zep-style stores, or GraphRAG (Graph Retrieval-Augmented Generation, RAG over an entity-relation graph), Honcho trades explicit schema (predefined entity types) plus traversals for schema-free logic conclusions in pair-scoped vectors, gaining flexibility but losing explicit graph explainability.
- As a rule of thumb for a backend engineer, prototype memory-heavy features on managed Honcho and only move to self-hosted Honcho or Postgres plus pgvector DIY when data-residency (data must stay in your own servers), cost at scale, or simple similarity queries dominate.

## 7. [[wiki/targeted|Targeted Answers: the Four Deep Questions]]
**In one sentence:** This page answers the four hard questions about Honcho — how it differs from simpler memory tools, what its per-message reasoning step costs, what its test scores really mean, and when to choose it over building your own storage.
- Honcho reasons over everything you store into growing peer representations, while mem0-style tools only save facts and return matches for your app to assemble, and RAG (Retrieval-Augmented Generation, a method that cuts text into chunks, turns them into number vectors, and returns the closest chunks) only finds what was said word-for-word.
- Every message triggers an async (background, not blocking the reply) Neuromancer step that extracts explicit facts and logical conclusions; storage and lookup are vendor-reported as free and fast (~200 milliseconds), and you pay $2.00 per million input tokens for that reasoning plus $0.001–$0.50 per question asked.
- The headline test scores are all vendor-reported: LongMemEval-S 90.4%, LoCoMo 89.9%, and BEAM scores around 0.63 down to 0.41 at 10 million tokens, each measured against a weak no-memory baseline and judged by an LLM (Large Language Model, the AI model that reads and writes text), so independent re-testing is still needed.
- Choose Honcho when memory quality across many chats is the product feature, choose Postgres plus pgvector when data must stay in your own VPC (Virtual Private Cloud, your own private section of the cloud) or queries are simple, and choose a graph store when your data has stable people-places-things links to walk step by step.

## The argument in five moves
1. Store messages in sessions between peers inside a workspace.
2. Reason over each message in the background with Neuromancer via the Deriver.
3. Compound representations over time via Dreamer consolidation.
4. Query via session context() or Dialectic chat for ready answers.
5. Beat store-and-retrieve with token-efficient statefulness across sessions.
