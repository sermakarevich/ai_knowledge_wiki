> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: Latency in Voice AI Agent

## Claims vs. evidence
- Claim: latency is the full hear-process-generate-speak-back loop, and any
  awkward pause is that loop made audible. Evidence: definition plus one
  order-status example. Plausible framing, but no pipeline breakdown or
  measurement method is given.
- Claim: even 200–300 ms can break conversational flow and feel robotic.
  Evidence: asserted, not measured — no A/B test, MOS score, CSAT delta, or
  cited study in the digest or wiki page.
- Claim: >500 ms for simple Q&A is a red flag; >800 ms risks overlaps,
  interruptions, and dropped experiences. Evidence: thresholds stated as rules
  of thumb with no distribution, percentile (p50/p95?), network condition, or
  task-complexity qualifier.
- Claim: energy-based plus AI-powered VAD, optimized models, and a turn buffer
  make Boop agents fast and human-sounding. Evidence: architecture names only —
  no latency numbers, no baseline comparison, no ablation of what each piece adds.
- Claim: buyers should demand observability and pre-live test/tweak.
  Evidence: reasonable advice, but self-serving without showing what Boop's
  observability actually exposes (per-stage timings? interruption handling?).
- Net: directionally sound claims about timing and turn-taking, supported by
  assertion rather than data. Treat thresholds as hypotheses, not benchmarks.

## Genuinely new vs. repackaged
- Genuinely useful: the buyer-oriented reframing — don't just ask what an agent
  can do, ask how fast. The 500/800 ms split (simple-Q&A bar vs. breakdown
  zone) is a compact, memorable procurement heuristic.
- Repackaged: VAD, endpointing, barge-in, and turn-taking are decades-old
  speech-system concerns; "energy-based + neural VAD" is standard hybrid
  practice, not a novel invention.
- Repackaged: "optimized models for faster processing" is a generic vendor
  claim with no disclosed technique (distillation? streaming ASR/LLM/TTS?
  speculative decoding? edge inference?).
- Repackaged: the "turn buffer that replicates natural pauses" restates normal
  floor-holding / response-shaping behavior without explaining the policy
  (fixed delay vs. adaptive vs. backchannel-aware).
- Verdict on novelty: packaging is new, components are not. Value is the
  checklist (latency bar + turn-taking + observability), not the mechanism.

## Weaknesses and blind spots
- No numbers that matter: no end-to-end latency distribution, no per-stage
  budget (ASR → LLM → TTS → playout), no p95/tail behavior, no comparison
  against any baseline or competitor.
- Thresholds without context: 500 ms for "simple Q&A" ignores language, accent,
  noise, telephony codec, streaming vs. batch TTS, and first-token vs.
  full-response timing.
- Tail latency ignored: real support calls fail at p95/p99 (hesitations,
  retries, overlapping speech), yet only single-point thresholds are offered.
- Interruption semantics undefined: "understands interruption" could mean hard
  cutoff, graceful yield, or overlap-tolerant duplex — each has different
  latency and UX trade-offs, none specified.
- No cost/quality trade-off: faster models and streaming cut latency but can
  hurt accuracy and naturalness; the piece never discusses what is sacrificed.
- No evaluation protocol: "test and tweak before going live" names no harness,
  load profile, interruption test set, or acceptance metric.
- Single-vendor lens: Boop's stack is presented as the answer with no
  falsifiable comparison, so confirmation bias is unchecked.

## Applicability
- Directly applicable as a procurement and design checklist: set an explicit
  latency SLO, require per-stage timing telemetry, and test barge-in/overlap
  behavior before launch.
- Useful as a разговорный starting point for SLOs: adopt sub-500 ms for simple
  turns as a target to validate, not a contract to sign blindly.
- Not directly applicable as an engineering blueprint: no architecture detail,
  tuning guidance, or measurement recipe to copy.
- **Relevance to my work**
  - AI/ML engineering: adopt per-stage latency budgets (VAD/endpointing, ASR,
    LLM first-token, TTS first-audio) with p50/p95 dashboards; add chaos cases
    (noise, accents, packet loss, user barge-in) to regression suites.
  - Agentic systems: treat turn-taking as an agent skill — explicit policies
    for yield-on-interruption, backchannels, and overlap handling — and log
    every floor-change decision for post-call review.
  - Elisity data platform: latency telemetry is event data worth capturing at
    scale — per-turn timings, interruption outcomes, retry/overlap flags — so
    support-call quality can be sliced by model version, region, and cohort.

## What this changes
- Changes the buying question: capability demos are insufficient; require a
  timed demo with visible per-stage latency and an interruption stress test.
- Changes the design default: ship the latency dashboard before the voice,
  with SLOs, tail-latency alerts, and a pre-live gate on barge-in behavior.
- Does not change the build-vs-buy calculus by itself: without Boop benchmarks
  or a reproducible test, this is a pointer toward rigor, not proof of it.
- Practical takeaway: steal the checklist (500 ms probe, 800 ms alarm,
  VAD + turn policy + observability), then validate every number on your own
  traffic before committing.

## Verdict
- keep the thresholds as working hypotheses, keep the turn-taking plus
  observability checklist, discard the vendor conclusion until numbers arrive.
- Strongest reason to care: latency-as-trust is the right frame, and the
  three-part gate (speed, interruption handling, testability) is genuinely
  useful for the next voice-agent review or SLO doc.
- Strongest reason to discount: zero measurements, zero baselines, and a
  single-vendor narrative mean nothing here is proven or transferable as-is.
- Next step if interested: run a one-day spike — time 50 scripted turns with
  scripted interruptions, record per-stage p50/p95, and see whether the
  500/800 ms lines survive contact with your stack.
- Call: **watch**
