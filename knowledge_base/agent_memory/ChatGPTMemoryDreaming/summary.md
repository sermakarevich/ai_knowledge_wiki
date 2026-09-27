# ChatGPT Started Dreaming: How Its Memory Actually Works

**Article:** [ChatGPT Started Dreaming: How Its Memory Actually Works (Mem0, 2026)](https://x.com/mem0ai/status/2071990201531118063)

## Human Readable TL;DR

ChatGPT does not "look up" old chats like a search engine. Instead it keeps a running cheat-sheet about you -- a summary of facts, preferences, and recent messages -- and staples that whole cheat-sheet to every new conversation before you even type. In June 2026 OpenAI added "Dreaming": a background process that rewrites this cheat-sheet over time so stale facts (like "you're going to Singapore in July") get updated to the past tense once the trip is over, without you asking. It's less like a librarian fetching the one book you need, and more like handing the model your entire diary every single time you talk to it.

## TL;DR

ChatGPT memory has two documented parts (saved memories via a `bio` tool call, and reference chat history), but the actual retrieval mechanism -- reverse-engineered by Johann Rehberger and Simon Willison -- is not RAG or vector search: a standing, human-readable profile (~6 sections: Model Set Context, Assistant Response Preferences, Notable Past Conversation Topic Highlights, Helpful User Insights, Recent Conversation Content, User Interaction Metadata) is injected into the system prompt on every turn. In June 2026 OpenAI shipped "Dreaming," a background consolidation process that rewrites this profile to fix staleness/correctness/scale, reportedly lifting internal factual-recall eval from 41.5% (2024) to 82.8% (2026). The design trades retrieval precision for brute-force context stuffing ("the bitter lesson"), which creates privacy exposure (a full dossier with no granular control) and a write-surface attack vector (prompt injection into memory, demonstrated by Rehberger and arXiv:2406.00199).

---

## Problem & Motivation

Consumer chat products need to "remember" users across sessions to feel personal, but nobody outside OpenAI had confirmed how ChatGPT's memory is actually implemented under the hood -- official docs describe *what* it does (saved memories, reference chat history) but not *how* it retrieves or assembles that information. Independent researchers set out to reverse-engineer the mechanism, and OpenAI's own June 2026 "Dreaming" update is presented as solving a real scaling problem: a pre-loaded profile accumulates stale, contradictory facts across years of chats and hundreds of millions of users, and hand-curated saved memories don't scale to that volume.

---

## Main Original Ideas

1. **Profile injection, not retrieval.** ChatGPT does not search or vector-query past conversations per message. It maintains a standing, editable summary of the user that gets re-injected into the system prompt on every new chat -- confirmed independently by Rehberger and Willison after both initially assumed RAG was involved.
2. **The six-section memory profile.** Rehberger documented the injected profile as roughly six named blocks (Model Set Context, Assistant Response Preferences, Notable Past Conversation Topic Highlights, Helpful User Insights, Recent Conversation Content, User Interaction Metadata), with Recent Conversation Content storing only the user's own messages (not the model's replies) to limit prompt-injection/hallucination risk, split by a `||||` delimiter and tagged with `intent_tags`.
3. **The `bio` tool for saved memories.** Discrete facts ("remember that I am vegetarian") are persisted via a `to=bio` tool call and surface later as dated entries inside the `# Model Set Context` section of future system prompts.
4. **"Dreaming" as background memory consolidation.** Launched June 4, 2026 to Plus/Pro users in the US, Dreaming rewrites the profile between sessions without user action -- e.g., turning "You're going to Singapore in July" into "You went to Singapore in July 2026" once the trip has passed. It mirrors a broader industry trend toward idle-time memory consolidation (Google's "Language Models Need Sleep," Mem0, GBrain).
5. **The "bitter lesson" framing.** Rather than building extraction pipelines, vector DBs, or knowledge graphs, OpenAI's approach is to include the entire compressed profile with every message and let the model's attention do the sorting -- betting scale beats engineered retrieval.

---

## Key Findings

| Metric | 2024 architecture | 2026 (Dreaming) architecture |
|---|---|---|
| Factual recall (OpenAI internal eval) | 41.5% | 82.8% |
| Preference adherence | -- | 71.3% |
| Time-sensitive accuracy | -- | 75.1% |

- These figures are OpenAI-reported on an unreleased evaluation -- vendor-stated, not independently audited.
- Mem0 claims its retrieval-based approach (parallel semantic similarity + keyword + entity scoring, fused at query time) runs under 7,000 tokens per call vs. 25,000+ for full-context stuffing, at comparable accuracy (Mem0's own benchmark).
- Security research (Rehberger; arXiv:2406.00199) demonstrated that untrusted content (e.g., a referenced Google Doc) could write attacker-controlled entries into long-term memory, and a 2024 study showed the same mechanism could be turned into a standing data-exfiltration channel. These were proof-of-concept attacks; OpenAI has since hardened exfiltration paths.
- ChatGPT's memory is closed, single-app, and pre-loaded wholesale -- there is no way to scope which memory surfaces for a given task, and Custom GPTs / other apps cannot read or write it.

---

## Suggestions & Future Directions

1. The mechanism described (six-section profile, injection pattern) was mapped through 2024-2025 probing; Dreaming changed how the profile is built, and no independent researcher has published a look at the post-update internals -- this is flagged explicitly as a known gap.
2. OpenAI's Dreaming eval numbers have not been independently reproduced; the article recommends treating them as vendor claims pending third-party audit.
3. The article positions a dedicated, developer-facing memory layer (Mem0) as the complement to ChatGPT's closed consumer profile: identity-scoped, portable memory (tagged with `user_id`, `agent_id`, `run_id`) that can be retrieved deliberately and carried across apps/agents, rather than living inside one product.

---

## Authors & Institutions

Published by Mem0 (@mem0ai) as entry #15 in its "In Context" blog series on AI agent memory and context engineering. Synthesizes reporting/research credited to Johann Rehberger (Embrace The Red), Simon Willison (simonwillison.net), shloked.com, OpenAI, and Tech Times.
