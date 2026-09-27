> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Pricing and Limits
**In one sentence:** Honcho charges for input and thinking, not for storage — you pay $2.00 per million input tokens for memory and $0.001 to $0.50 per question for reasoning, while reading saved memory is free.
## Key points
- HONCHO MEMORY ingestion costs $2.00 per million input tokens (vendor-reported), and that single fee covers storage plus Neuromancer reasoning and dreaming.
- Reading memory with context() is free and unlimited (vendor-reported), with about 200 milliseconds response time for a ready-made session context.
- HONCHO REASONING has 5 per-question tiers (vendor-reported): minimal $0.001, low $0.01, medium $0.05, high $0.10, and max $0.50.
- New accounts get $100 in free credits (vendor-reported), and the official quickstart tutorial costs about $0.04 to run.
- Startups that raised less than $5 million get $1,000 in credits plus lower prices (vendor-reported), and large companies get custom enterprise plans with forward-deployed engineers.
- Honcho's rule is "storage plus retrieval is free, pay for reasoning", while mem0-style rivals charge a fee each time you search your own saved data.
- Operational limits are strict numbers: at most 100 messages per batch upload, dream consolidation needs 50 or more new conclusions plus an 8-hour cooldown plus a 60-minute idle wait, and high/max questions run async (asynchronous, in the background) with queue-status checks and webhooks (automatic completion alerts).
- Access keys come in 4 scopes — admin, workspace, peer, and session — and workspace-wide chat needs a workspace-level key or higher, while self-hosting the open core is free under AGPL (Affero General Public License, a license that requires sharing changes if you run it as a service).
---
## How the two-part price works
Honcho splits the bill into two parts. MEMORY is what you pay when new messages go in. REASONING is what you pay when you ask a hard question.
An API (Application Programming Interface, the way your code talks to Honcho) write returns fast while the heavy thinking happens in the background. That is why reads stay cheap.
Neuromancer, Honcho's family of small reasoning models, does the background extraction of facts and logic conclusions. Its cost is bundled into the $2.00 per million ingestion fee, so you do not pay extra for Deriver or Dreamer runs.
## Pricing table
All prices below are vendor-reported from the honcho.dev homepage, retrieved 2026-09-10. M means million input tokens ingested.
| Product | Price (vendor-reported) | What you get |
|---|---|---|
| HONCHO MEMORY | $2.00 per M tokens | Store messages in PostgreSQL (a database), Neuromancer reasoning, summaries, and dreaming included |
| context() reads | $0, unlimited | Session context in about 200 ms, with token-budget blend of summary plus recent messages |
| REASONING minimal | $0.001 per query | Instant, single semantic search, cheapest prefetch |
| REASONING low | $0.01 per query, default | Standard chat() answer with anchored peer reasoning |
| REASONING medium | $0.05 per query | More tools and thinking steps |
| REASONING high | $0.10 per query, async | Longer background job, check queue-status or wait for webhook |
| REASONING max | $0.50 per query, async | Research-grade, most iterations and output tokens |
## Free credits, startups, and enterprise
- Trial: $100 free credits on signup, enough for about 50 million ingestion tokens at $2.00 per M, and the quickstart costs about $0.04.
- Startups: teams that raised less than $5M get $1,000 in credits plus subsidized (discounted) pricing.
- Enterprise: custom price and volume deals plus forward-deployed engineers who help install and tune Honcho inside your company.
- Versus mem0: mem0-style tools charge for retrieval, meaning you pay to search data you already stored. Honcho storage and retrieval is free — you only pay when Neuromancer reasons on write or the Dialectic agent reasons on query.
## Operational limits you must design for
- Batch uploads: at most 100 messages per session.add_messages call, so split larger imports into chunks.
- Async (asynchronous) queues: high and max reasoning tiers plus heavy writes run in the background; poll queue-status or register a webhook to get notified on completion.
- Dreaming thresholds: periodic consolidation only starts when there are 50 or more new conclusions since the last dream, at least 8 hours have passed, dreaming is enabled, and the session has been idle for 60 minutes; new activity cancels the timer, and schedule_dream skips these checks.
- Key scoping: keys come as admin, workspace, peer, or session, with narrower keys able to do less; workspace-wide honcho.chat() needs a workspace-level key or higher because it searches across all peers.
- File uploads: PDF, text, and JSON (JavaScript Object Notation, a common data format) files become messages, so they count toward the same ingestion tokens and 100-message batch limit.
## Worked unit-economics example
Take a small $5-per-month companion app with 1,000 active users.
- Assume each user chats 30 messages per month, at 100 tokens per message: 1,000 x 30 x 100 = 3,000,000 tokens ingested.
- MEMORY cost: 3 M x $2.00 per M = $6.00 total, or $0.006 per user per month.
- Assume each user asks 20 low-tier questions per month: 1,000 x 20 x $0.01 = $200 total, or $0.20 per user per month.
- Total Honcho cost is about $0.21 per user per month, leaving wide margin inside a $5.00 subscription; switching routine questions to minimal at $0.001 cuts reasoning to $20 total, while moving power users to medium at $0.05 raises 20 queries to $1.00 per user.
- An LLM (Large Language Model, the AI that writes answers) baseline that stuffs 115,000 raw tokens per conversation into the prompt would cost dollars per user, which is why Honcho claims 60-90% token savings (vendor-reported).
## Self-host alternative
If data must stay in your own VPC (Virtual Private Cloud, your private section of the cloud) or usage is very large, you can self-host the open core from GitHub with Docker (a tool that runs packaged software) via honcho start --setup and bring your own LLM (Large Language Model) key. Self-hosting avoids the $2.00 per M and per-query fees but you run the database, queues, Neuromancer models, and updates yourself, under AGPL rules.
**Covers:** honcho.dev homepage pricing + platform docs (retrieved 2026-09-10; prices may change — verify at app.honcho.dev)
