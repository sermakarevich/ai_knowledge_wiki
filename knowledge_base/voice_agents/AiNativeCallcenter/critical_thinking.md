> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: AI Native Call Center

## Claims vs. evidence
- Claim: a voice model answers every call by default over an app-terminated speech-to-speech link. Evidence: strong within the docs — the AI leg is a SIP endpoint in the Go app bridged by FreeSWITCH, verified against live providers. No independent latency or MOS numbers accompany it.
- Claim: audio passes straight through (G.711 byte-for-byte where accepted, no decode/resample). Evidence: plausible as an implementation detail, but the digest scopes it with "where accepted" — codec negotiation failures and provider-specific behavior are undocumented here.
- Claim: the flow steers without scripting (phases carry instructions plus tool lists; transitions fire on tool results; tools may conversationally refuse). Evidence: internally coherent and seeded with six published bilingual flows, but no data on task-completion rate, fallback rate, or refusal precision.
- Claim: handover is seamless — screen pops via `PARTY_RINGING` SSE before the phone rings, bot transcript already present via pre-minted call id. Evidence: specific mechanism, verified against live FreeSWITCH per the wiki. Still a design assertion, not a measured handover-latency result.
- Claim: one conversation equals one CDR, one transcript, one recording. Evidence: credible as a schema decision; no evidence on dedup edge cases (transfers, callbacks, failed legs).
- Claim: the stack is operable — one Go binary plus PostgreSQL and FreeSWITCH, DB-driven switch config, reproducible docker compose seed. Evidence: strongest claim; concrete seed (team, queues, flows, numbers, simulated phones, history) plus spec-first API and `-race` test discipline.
- Explicit non-claim (to its credit): performance. The wiki states the capacity budget and load harness exist but "the benchmark campaign itself is still to come." Treat all scaling implications as intention, not measurement.
- Claim: agents work from the browser with screen-pop, presence, call control, and callbacks. Evidence: mechanism is concrete (SSE `userData`, REST over ESL `uuid_phone_event`) but split across browser UI plus `web-sip-phone` extension — "works" depends on extension health, which is not evidenced here.
- Claim: extension without forking — new providers, flows, screens, and integrations via profiles, JSON validation, design-system binding, and backend URLs. Evidence: plausible interface design with in-repo examples, but no third-party extension case is cited.

## Genuinely new vs. repackaged
- Genuinely new: terminating the provider's realtime speech-to-speech session inside the telephony app as a SIP endpoint, rather than cascading ASR → LLM → TTS in-process. The refusal to ship a cascade at all is a real architectural bet.
- Genuinely new: the division of labor — model owns the words, flow owns the phase — with phase-scoped tool lists and tool-result transitions plus conversational refusal ("queue is closed" as dialogue, not exception). That is a cleaner guardrail pattern than most IVR prompt-scripts.
- Genuinely new: minting the call id before any leg exists so bot-phase transcript, agent-phase audio, and recording share one identity from birth. Small decision, large payoff for observability.
- Repackaged: the domain model is Genesys-lineage (call aggregates parties, `PARTY_*`/`CALL_*` events), and handover rides standard `mod_callcenter` queues. Solid reuse, not invention.
- Repackaged: the surrounding stack — Go REST/SSE server, embedded web UI, PostgreSQL, static XML dialplan delegating to Lua, ESL event plumbing — is conventional, well-assembled commodity engineering.
- Repackaged: bilingual flows, seeded demo data, and provider profiles are good product packaging, not research novelty.
- Genuinely new at the process level: spec-first API (`docs/openapi.json` generates server and client) plus database-driven switch configuration — telephony config becomes data migration, not XML surgery.
- Repackaged but well-judged: versioning persona, rules, and voice together per published flow, and keeping external integration behind a backend URL rather than in-tree code.

## Weaknesses and blind spots
- Single provider per deployment, chosen at startup, and call language never selects the provider. No per-call routing, failover, or A/B comparison — a serious limitation for multilingual production and for resilience when a provider degrades.
- Protocol fragmentation: three providers share one protocol profile while `doubao` and `gemini` each need a separate client. Extension is "a profile, not a client" except when it is not; expect maintenance drag.
- Prompt-fidelity split: one provider is handed words to speak, the others are "instructed to repeat them word for word." Verbatim compliance across providers is asserted, not measured — greeting and legal-disclaimer flows are at risk.
- Split agent audio: browser does presence/control while a separate Chrome extension holds SIP registration, with no dialpad. Two-component agent desktop means two failure modes, extension-store dependence, and awkward ad-hoc dialing.
- Security and compliance surface is undocumented in this material: SIP credentials issued at sign-in, recordings to filesystem/S3, transcripts unified per call — no word on retention, redaction, PII handling, or tenant isolation.
- No evaluation story: no task success, containment rate, handover accuracy, transcription quality, or voice-quality metrics. Six seeded flows demonstrate buildability, not effectiveness.
- Scaling is actor-per-call (one goroutine as sole mutator, mailbox snapshots) but unmeasured; the AI-leg mutex carve-out hints at the concurrency hotspot without quantifying it.
- Vendor and geography coupling: `qwen`/`doubao` inside China vs `openai`/`gemini` elsewhere bakes deployment topology into provider choice, complicating global rollouts.
- Demo realism gap: eighteen simulated telephones and a week of seeded history exercise the happy path; adversarial callers, noisy audio, overlapping speech, and provider outages are absent from this material.
- Operability gaps: no story here on schema migration for live queues, Lua-script versioning against the DB-driven config, or rollback of a published flow mid-day.

## Applicability
- Good fit as a reference build for voice-first intake with human fallback: after-hours answering, queue-closed handling, callback management, and unified transcripts for QA.
- Good fit as a pattern source even without adopting the repo: app-terminated S2S endpoint, flow-owns-phase steering, pre-minted conversation id, DB-driven switch config, spec-first API contract.
- Poor fit where per-call provider routing, measured scale targets, or compliance-certified recording handling are required on day one.
- Trial shape: stand up the compose seed, run the load harness to replace the budget with numbers, and score containment plus handover accuracy on your own call sample before any production commitment.
- **Relevance to my work**
  - AI/ML engineering: borrow the no-cascade S2S posture and phase-scoped tool lists for intake bots; replicate the "edit the contract, then generate" OpenAPI discipline; do not copy single-provider-per-deployment without adding failover.
  - Agentic systems: the conversational-refusal tool pattern and tool-result transitions generalize to any agent with bounded authority; the actor-per-conversation concurrency model maps directly onto long-lived agent sessions with mailbox state.
  - The Elisity data platform: the pre-minted conversation id unifying transcript, CDR, and recording is directly reusable for unifying telemetry/identity records; the "one conversation, one record" invariant is worth enforcing in any pipeline that currently fragments bot and human phases.

## What this changes
- It moves the default from menu-first to model-first answering while keeping a real human queue behind it — the honest version of "AI receptionist" that most demos skip.
- It reframes guardrails from scripted prompts to phase-scoped authority: what the model may do changes with the phase, and refusal is a first-class conversational act.
- It collapses three artifacts (bot log, agent log, recording) into one addressable conversation, which changes what QA, analytics, and audit can assume downstream.
- It proves a solo-binary-plus-switch topology can carry both AI and human paths without a separate contact-center platform — at demo scale, with production scale still to be shown.
- It normalizes treating "the queue is closed" and similar vetoes as dialogue rather than errors, which simplifies flow graphs and keeps the caller experience coherent.
- It sets a packaging bar: seed data, simulated phones, and history on first boot mean every evaluator hears the same demo, a practice worth copying.

## Verdict
- Useful, opinionated, and reproducible — but unmeasured on performance and unevaluated on dialogue quality, with a single-provider deployment model that limits production use.
- Best consumed as a lab system and pattern mine: deploy the compose seed, stress the flow engine and handover path, and extract the phase/tool and unified-record ideas into your own stack.
- Watch item: if a benchmark campaign or per-call provider routing lands upstream, reassess — those two fixes remove the main objections.
- Skip only if you need a cascaded ASR+LLM+TTS pipeline in-process or a multi-provider production cutover today; this project explicitly will not give you either.
- Call: **trial**
