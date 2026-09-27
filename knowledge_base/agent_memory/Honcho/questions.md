---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Honcho

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. Name the four core Honcho primitives and state what each one stores or bounds.
> [!tip]- Answer
> Workspace is the top-level isolated project area, Peer is any long-lived entity such as a user or agent whose learned profile is stored, Session is one interaction thread that bounds what history can be recalled together, and Message is the basic time-ordered unit of data tied to one peer. Bulk import allows up to 100 messages per call and each new message triggers background reasoning. See [[wiki/01-concepts|Concepts]].

### Q2. Contrast the Deriver, the Dreamer, and the Dialectic by when each runs and what it produces.
> [!tip]- Answer
> The Deriver is the per-message background worker that runs Neuromancer XR over each new message to extract explicit statements and deductive conclusions. The Dreamer is the periodic consolidation worker that revisits stored conclusions with a deduction specialist for updates and contradictions and an induction specialist for patterns. The Dialectic is the query-time agent that prefetches relevant conclusions and synthesizes answers for peer.chat() and honcho.chat(). See [[wiki/03-reasoning-architecture|Reasoning Architecture]].

### Q3. Recall the headline vendor-reported eval scores and the XR ablation numbers.
> [!tip]- Answer
> Honcho is vendor-reported at 90.4% on LongMemEval-S, 89.9% on LoCoMo, and 0.630 at 100K, 0.646 at 500K, 0.618 at 1M, and 0.409 at 10M on BEAM. In the LoCoMo ablation with the final writer fixed as Claude 4 Sonnet, Neuromancer XR scored 86.9% overall versus 80.0% for Claude 4 Sonnet and 69.6% for base Qwen3-8B. See [[wiki/04-evals|Evaluations]].

### Q4. What does Honcho charge for ingestion and for each reasoning level, and what is free?
> [!tip]- Answer
> HONCHO MEMORY ingestion costs vendor-reported $2.00 per million input tokens, covering storage plus Neuromancer reasoning and dreaming. Reasoning per query has five tiers: minimal $0.001, low $0.01, medium $0.05, high $0.10, and max $0.50, with high and max running async. Storage and retrieval with context() is free and unlimited at about 200 milliseconds. See [[wiki/05-pricing-limits|Pricing and Limits]].

### Q5. When do you use peer.chat() versus honcho.chat() versus session.context(), and how do you feed the result to an LLM?
> [!tip]- Answer
> Use peer.chat() to ask about one peer anchored to one observer-observed pair, honcho.chat() to ask across every peer in a workspace with pair-by-pair attribution, and session.context() to get ready-to-use history with token budgets such as tokens=1500 or 2000. Convert context with to_openai() or to_anthropic() for direct use with OpenAI or Anthropic models. See [[wiki/02-quickstart-integration|Quickstart and Integration]].

### Q6. Why does Honcho store conclusions in one vector collection per observer-observed pair instead of one shared store?
> [!tip]- Answer
> Pair-scoped collections keep viewpoints true to shared history, so Bob's view of Alice built from sessions 1 and 2 stays separate from Charlie's view from session 3 only. Without this split every agent would act all-knowing and simulations would feel false. It also lets peer.chat() prefetch only the relevant pair instead of searching the whole workspace. See [[wiki/01-concepts|Concepts]].

### Q7. What breaks or degrades if dreaming stays off, and what are the automatic dreaming thresholds?
> [!tip]- Answer
> Without dreaming there is no periodic contradiction resolution, knowledge-update handling, peer-card refresh, or inductive pattern extraction, so stale facts pile up and cross-message patterns never form. Automatic dreaming requires all of: at least 50 new conclusions since the last dream, at least 8 hours cooldown, dreaming enabled, plus a 60-minute idle timer that any new message resets. Manual schedule_dream bypasses the thresholds but still skips if a dream is pending or running. See [[wiki/targeted|Targeted Answers]].

### Q8. Why do compact logic conclusions beat raw text chunks for long-memory queries?
> [!tip]- Answer
> Raw-chunk RAG (Retrieval-Augmented Generation, chunk-embed-retrieve lookup) only returns what was said word-for-word, breaks when facts change, and forces stuffing 100K raw tokens into the prompt. Honcho reasons once at write time into explicit, deductive, inductive, and abductive conclusions, resolves contradictions during dreaming, then reads back small conclusions for vendor-reported 60-90% token savings. See [[wiki/06-comparisons|Comparisons]].

### Q9. Design a peer/session/scope layout for a tutoring app with one student, three subjects, and a tutor agent.
> [!tip]- Answer
> Create peers for the student and the tutor agent plus one peer per subject project if subject identity must persist, one session per tutoring meeting or ticket, and named scopes per subject such as math versus history to bound recall. Enable observe_others in shared sessions so the tutor builds a limited view of the student from only shared sessions. Query with peer_target on the student plus scope filtering, and use limit_to_session for within-lesson-only recall. See [[wiki/02-quickstart-integration|Quickstart and Integration]].

### Q10. A bank needs auditability, data residency in its own VPC (Virtual Private Cloud, its private cloud section), and simple similarity search over small support logs. Honcho or Postgres plus pgvector, and why?
> [!tip]- Answer
> Choose Postgres plus pgvector DIY (Do-It-Yourself storage over a regular database plus vector extension) because data must stay in the bank's VPC, queries are simple similarity over small data, and full control and ownership outweigh reasoning depth. Choose Honcho only when cross-session statefulness and memory quality are the product differentiator, or self-hosted Honcho as a middle path if residency plus reasoning are both required. Graph stores fit only if the domain has stable entities needing explicit multi-hop traversals. See [[wiki/06-comparisons|Comparisons]].

### Q11. What is the weakest link in the Honcho evidence base, and what would you demand before trusting the headline scores?
> [!tip]- Answer
> The weakest link is that all headline scores are vendor-reported with no independent replication, judged by an LLM where judge choice alone swings results by 15-25 percentage points, against vendor-picked weak no-memory baselines. Before trusting 90.4% or 89.9%, demand an independent rerun from the open harness with a fixed judge, a strong full-context baseline, and joint accuracy-cost-token reporting. See [[critical_thinking|Critical Thinking]].
