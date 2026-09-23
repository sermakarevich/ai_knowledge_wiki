> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: Announcing the Artificial Analysis Speech to Speech Index | Artificial Analysis

## Claims vs. evidence
- Claim: the index is a single valid measure of native Speech-to-Speech quality.
- Evidence offered: equal weighting of three named datasets plus an all-three inclusion
- rule. No weighting sensitivity, correlation analysis, or human-preference validation
- is reported in the digest/wiki, so the "single measure" claim is asserted, not shown.
- Claim: Conversational Dynamics and Agentic Performance differentiate frontier models.
- Evidence: strong — GPT-Realtime-2 leads Conversational Dynamics (Minimal tops 96.1%)
- while Grok Voice Think Fast 1.0 leads Agentic Performance (52.1% vs. 39.8%), with
- Speech Reasoning tightly clustered (Grok at 97.1%). The ranking pattern supports it.
- Claim: τ-Voice is "the hardest dimension by a wide margin."
- Evidence: strong within the reported numbers — every model scores below 53% on
- τ-Voice while the other two dimensions approach ceiling. Hardest *of these three*,
- not hardest in any absolute sense, is the warranted reading.
- Claim: quality trades against speed and cost.
- Evidence: moderate — TTFA spans 0.44s (Deepslate Opal, 62.1%) to 2.98s (Gemini High,
- 69.5%) and cost spans $1.50–$4.14/hr input audio, but these are point estimates with
- no variance, load conditions, or output-token pricing, so the tradeoff is directional.

## Genuinely new vs. repackaged
- Genuinely new: the synthesis itself — one public leaderboard combining Speech
- Reasoning, Conversational Dynamics, and Agentic Performance with a completeness
- gate (valid results on all three). That composite view did not exist in one place.
- Genuinely new: the τ-Voice agentic-task signal (Airline/Retail/Telecom completion)
- inside a voice leaderboard; it reframes voice models as task executors, not talkers.
- Repackaged: Big Bench Audio (1,000 reasoning questions: Fallacies, Navigate, Object
- Counting, Web of Lies) and Full Duplex Bench (pause/turn-taking/interruption) are
- pre-existing benchmarks, now re-presented as index components.
- Repackaged: the leaderboard narrative (OpenAI on top at 77.2%, Grok second at 75.7%)
- follows the familiar vendor-benchmark announcement template; speed/cost tables are
- standard Artificial Analysis dressing rather than methodological innovation.

## Weaknesses and blind spots
- Equal weighting is undefended: why should reasoning, duplex dynamics, and agentic
- completion each count exactly one-third? No ablation or buyer-weighted alternative.
- Inclusion gate creates survivorship bias: models missing one dataset vanish entirely,
- so the ranking compares only the most-evaluated, not the full market.
- Ceiling effects: Speech Reasoning near 97% and Conversational Dynamics near 96%
- mean two-thirds of the index barely separates leaders; τ-Voice dominates variance.
- τ-Voice coverage is narrow (three customer-service domains); nothing on noise,
- accents, multilingual speech, safety/refusal, or long-horizon tool-use reliability.
- Measurement opacity: no sample sizes beyond Big Bench Audio's 1,000, no confidence
- intervals, no judge-vs-human agreement, no eval harness or date/version pinning.
- Cost metric is input-audio-only ($/hr); output audio, tool calls, and idle-session
- charges — the real voice-agent bill — are invisible.
- Latency metric is TTFA alone; interruption recovery, barge-in, and sustained
- turn latency matter more for duplex feel and are not in the headline number.
- Iteration promise ("will continue to iterate, add more models") is unversioned, so
- today's 77.2% may not be comparable to next quarter's scores.

## Applicability
- Use as a shortlist filter for native S2S vendors, not as a purchase decision: start
- with the top band (GPT-Realtime-2, Grok Voice Think Fast, Gemini Live), then test
- on your own audio, tasks, and latency/cost envelope.
- Weight dimensions by use case: duplex-heavy companion → Conversational Dynamics;
- task-execution agent → τ-Voice; knowledge Q&A → Speech Reasoning. Do not use the
- equal-weight mean blindly.
- Pair every index lookup with TTFA and $/hr tables: Opal at 0.44s and Gemini Minimal
- at $1.50/hr show when "good enough + fast/cheap" beats the 77.2% leader.
- **Relevance to my work**
- - AI/ML engineering: adopt the three-axis eval pattern (reasoning, interaction
-   dynamics, task completion) for our own voice-model regression suites; enforce the
-   all-dimensions completeness gate so partial models cannot top the board.
- - Agentic systems: treat the τ-Voice sub-53% ceiling as the binding constraint —
-   tool-calling reliability over voice, not STT/TTS fidelity, is where agents fail;
-   replicate Airline/Retail/Telecom task-completion probes before trusting demos.
- - Elisity data platform: log per-turn audio features, TTFA/bARGE-in latency, task
-   outcome, and full input+output cost alongside quality scores, so our internal
-   leaderboard avoids this index's blind spots (TTFA-only, input-cost-only).

## What this changes
- Shifts voice-model comparison from "sounds fluent" to "reasons, interacts, and
- completes tasks" — the τ-Voice leg makes agentic execution a first-class criterion.
- Confirms the frontier bottleneck: reasoning and duplex behavior are near-solved at
- the top; reliable spoken task completion under 53% is the gap to close.
- Reframes buying as three-way optimization (index score vs. TTFA vs. $/hr) rather
- than chasing the single 77.2% headline.
- Signals benchmark churn ahead: expect weights, datasets, and coverage to move, so
- pin versions and keep private evals rather than hard-coding thresholds to this index.

## Verdict
- Useful composite shortlist, weak as a ground-truth quality measure: opaque methods,
- undefended equal weights, narrow domains, and thin cost/latency metrics limit trust.
- Still the best single public starting point for native S2S comparison right now.
- Therefore the call is: **trial** — use it to shortlist and structure evals, verify
- on your own tasks, latency, and full cost before any **adopt** decision.
