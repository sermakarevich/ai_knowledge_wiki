> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: Architecting Real-Time Voice AI: Beyond STT-LLM-TTS (2026 Guide)

## Claims vs. evidence

- **Claim: voice is a turn-taking problem, not a transcription problem.** Framing is persuasive and internally coherent — every component targets timing, not WER or model quality — but no comparative evidence is offered (no A/B of better STT vs. better orchestration).
- **Claim: sequential STT→LLM→TTS can never meet human timing.** Plausible given additive latencies, yet stated as axiomatic; no measured baseline (e.g., p50/p95 of a sequential pipeline) is shown to prove the gap.
- **Claim: sub-500 ms budget, 200–300 ms human gap, ~3 s abandonment.** Numbers are asserted without citation or methodology — are they telephony studies, product analytics, or rules of thumb? Treated as design constraints, they are useful, but their evidential status is weak.
- **Claim: the five-component streaming blueprint achieves the budget.** This is an architecture sketch, not a report: no latency breakdown per stage, no load test, no tail-latency analysis, no cost/latency trade-off curve.
- **Claim: specific tunables work (50 ms STT chunks, 600/1,500 ms turn thresholds, −45 to −35 dBFS + VAD + 200–300 ms barge-in guard).** Concrete and actionable — the strongest part — but presented as vendor-neutral defaults with only anecdotal tuning examples (300 ms for support, 2,500 ms ceiling for healthcare), not measured precision/recall of interruption behavior.
- **Claim: preamble narration + result buffering solves tool-call dead air.** Good UX pattern with a sound staleness argument (discard on interruption), but no data on perceived-latency improvement or failure modes (e.g., preamble lies when the tool errors).
- **Overall pattern:** strong mechanistic reasoning (each tactic plausibly reduces perceived or actual latency) paired with zero quantitative validation — a credible blueprint argued from first principles, not a measured result.
- **Rhetorical tell:** the closing "better listener than most humans" provocation signals explainer genre, not empirical report; read the thresholds as starting points to tune, not findings to cite.

## Genuinely new vs. repackaged

- **Genuinely useful synthesis:** the end-to-end checklist in one place — partials-for-liveness vs. finals-for-action, semantic-gated minimum silence plus hard maximum ceiling, sentence (not token) handoff unit, three-signal barge-in, buffer-or-discard tool results. Few explainers connect all five.
- **Repackaged:** sequential-vs-streaming history, websocket streaming STT, VAD-based barge-in, and "narrate before tool call" filler are all established telephony/dialog-systems practice, relabeled for the LLM era.
- **Reframing as the contribution:** the "single persistent websocket orchestrating overlapping stages" mental model. Not novel as infrastructure, but a clarifying corrective against the naive "microphone → LLM → speaker" demo mindset.
- **Missing novelty:** no new algorithm, benchmark, or component comparison (no end-to-end speech models vs. cascaded pipelines, no mention of full-duplex / speech-to-speech models that would complicate the cascade assumption).

## Weaknesses and blind spots

- **No evaluation of any kind:** no latency histograms, no interruption precision/recall, no user-satisfaction or task-completion metrics; all thresholds are best-practice folklore.
- **Happy-path bias:** assumes clean single-speaker audio; no treatment of accents, code-switching, overlapping speech, echo/noise cancellation, diarization, or multi-party calls.
- **STT semantic-completeness gate is hand-waved:** "STT judges the sentence complete" hides the hardest classifier in the pipeline — its errors directly cause the rude interruptions the design claims to fix.
- **Sentence-boundary handoff is fragile:** period/question-mark splitting breaks on numbers, abbreviations, and agglutinative languages; no discussion of prosody-aware or streaming-TTS alternatives.
- **Barge-in triple-gate is under-specified:** energy thresholds vary wildly by device/mic gain; no calibration procedure, no false-accept/false-reject trade-off, no handling of user backchannels ("uh-huh") vs. true interruptions.
- **Tool-calling pattern ignores hard problems:** auth, idempotency on retry-after-interruption, partial tool results, multi-tool dependency chains, and what the agent says when the tool fails after promising "let me check that."
- **Ops absent:** no cost per minute, no streaming-LLM/TTS vendor lock-in analysis, no fallback when the websocket drops, no observability (turn-level tracing), no safety/compliance (recording consent, PII in partials, healthcare HIPAA implications of the tuning example).
- **No adversarial view:** prompt injection via audio, TTS-spoken sensitive data overheard on speakerphone, and logging of partial transcripts containing PII are unmentioned despite mattering more in voice than in text.
- **Single-chunk scope:** material covers one explainer chunk only; depth on TTS streaming, LLM streaming protocols, and frontend playback buffering is thin.

## Applicability

- Directly applicable whenever building a live voice agent where >500 ms feels robotic: support lines, booking flows, intake triage.
- The tunables table is a usable starting config for a first prototype and a tuning backlog (silence thresholds per domain, barge-in duration guard).
- The partials/finals discipline ("never fire a lookup on a partial order number") is a transferable guardrail for any streaming-input agent.
- Less applicable to async voice (voicemail, transcription pipelines), push-to-talk, or text-first agents where the orchestration overhead buys nothing.

- **Relevance to my work**
  - **AI/ML engineering:** adopt the latency-budget discipline (per-stage budgets, p95 targets) and the sentence-handoff + preamble-masking patterns for any user-facing streaming demo; instrument turn-detection and barge-in decisions as first-class evals rather than magic numbers.
  - **Agentic systems:** the buffer-or-discard tool-result rule generalizes to interruptible agents — stale tool outputs must be versioned against conversation state, and narration-before-action is a cheap perceived-latency win for slow tools.
  - **Elisity data platform:** partial transcripts and interrupted tool calls are PII/toxic-data hazards — partials must not hit persistent stores or lookups, discarded tool results need retention policies, and per-domain silence tuning (e.g., deliberate speech) maps to configurable pipeline profiles rather than hardcoded constants.

## What this changes

- Shifts the design question from "which STT/LLM/TTS?" to "what is each stage's latency budget and what happens on interruption?" — the bill of materials stays the same, the architecture does not.
- Makes turn detection and barge-in explicit product decisions (thresholds per use case) instead of vendor defaults nobody tunes.
- Reframes tool calling for voice as a UX problem (mask + buffer + discard) rather than a function-calling accuracy problem.
- Practical consequence: prototype in the order of risk — turn detection and barge-in tuning first (they determine whether the agent feels rude or deaf), then sentence handoff, then tool masking — instead of starting with model selection.
- Lowers the barrier to a credible prototype: five checkable patterns over one websocket, each independently testable before full integration.

## Verdict

Solid practitioner explainer, weak as evidence: take the checklist and tunables, distrust the unattributed numbers, and measure everything yourself before committing to vendors or thresholds. For prototype voice work the patterns pay off immediately; for production, the missing evals, edge cases, and ops guidance mean significant work remains.
Keep it as the team's reference sketch for the next voice prototype, not as a production architecture sign-off.

**trial**
