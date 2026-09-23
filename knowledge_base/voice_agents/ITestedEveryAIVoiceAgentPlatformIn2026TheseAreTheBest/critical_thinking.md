> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: I Tested Every AI Voice Agent Platform in 2026. These are the Best.

## Claims vs. evidence
- Shared-stack claim: all six platforms resell the same four components
  (STT, LLM, TTS, telephony — e.g. Deepgram, GPT, ElevenLabs, Twilio).
  The ~7.8 cent/min floor is asserted, never derived line by line.
- Counter-evidence inside the piece: LiveKit self-hosted workers drop
  "from a cent a minute to 500ths cent a minute," which contradicts any
  universal floor and shows the floor only binds managed rentals.
- Voice claim: quality is a TTS-vendor decision, and ElevenLabs-native sounds
  "more crisp, and more realistic, and more smooth and natural."
  Evidence is weak: subjective impression only, no blind test, no MOS scores,
  no documented samples or listener panel.
- Latency-debunk claim: vendor numbers exclude what callers feel.
  Evidence is strong: each caveat is quoted — ElevenLabs excludes network
  round-trips and overhead, Vapi excludes endpointing and transport
  (the 300–800ms the caller feels), Retell's "as low as" 600ms excludes
  the network hop, Bland's 400ms has no methodology while its own docs
  warn the agent "could wait up to about 2 and 1/2 seconds."
- Benchmark claim: Secure Benchmark medians over ~1,100 scored turns each —
  Retell 1.69s, ElevenLabs ~1.73s, Vapi ~2.34s, LiveKit ~2.46s.
  Methodology (same agent, pinned model/temperature, real phone line) is stated,
  but variance, p90/p99, test date, authorship, and independence are missing,
  and Bland plus Voiceflow are absent (Voiceflow covered only by "~2–3s"
  personal experience).
- Cost claim: normalized on GPT-4 + ElevenLabs + Twilio, Vapi ~5c,
  Retell ~7c, ElevenLabs ~8c, Bland ~11c; Voiceflow undisclosed credits.
  Normalization basis is disclosed, but config, region, concurrency,
  and measurement window are not.
- Stability claim: 90-day status pages — Retell 9 incidents, Vapi 99.77%
  API uptime ("about 5 hours of outage"), Bland 66 incidents,
  ElevenLabs count unfound; Vapi judged "probably one of the safest bets."
  Evidence is weak-to-moderate: incident counts mix severities and definitions
  and cannot be compared directly against an uptime percentage.

## Genuinely new vs. repackaged
- Genuinely useful: the side-by-side latency-footnote audit.
  It converts marketing numbers into a buyer checklist: always ask whether
  endpointing, transport, and network hop are included.
- Genuinely useful: the cost-normalization move (same LLM + TTS + telephony).
  It reframes pricing from tier tables to stack economics,
  even though the resulting cents-per-minute figures are rough.
- Genuinely useful: the LiveKit self-hosting datapoint (20x cheaper).
  It is the only structural cost break in the piece and cleanly separates
  framework ownership from managed-platform rental.
- Repackaged: the "same four components" framing is standard voice-pipeline
  knowledge, not a 2026 discovery for practitioners.
- Repackaged: the ElevenLabs "best voice" verdict follows trivially from
  ElevenLabs owning the TTS bundle — predictable without any test.
- Repackaged: per-audience picks (Retell for phone-first agencies under
  4,000-token prompts, Vapi for developers, Bland for regulated long calls,
  Voiceflow for client dashboards) restate each vendor's own positioning.

## Weaknesses and blind spots
- Single-operator lens: an agency with 52 clients over two years is real
  experience, but still N=1 — no enterprise scale, high concurrency,
  multilingual, or noisy-audio production data.
- Missing quality dimensions: no WER/accuracy, no interruption and barge-in
  handling, no endpointing tunability comparison, no background-noise tests.
- Missing trust dimensions: no security, PII redaction, data-retention, or
  compliance evidence beyond asserting Bland fits regulated long messy calls.
- Latency gaps: medians only, no tails; no geography; no sensitivity to
  swapping STT/LLM/TTS vendors; two of six platforms lack benchmark data.
- Cost gaps: no concurrency or bursting price, no contract/support tiers,
  no engineering-labor cost for LiveKit self-hosting, no Voiceflow credit math.
  Per-minute figures alone mislead build-vs-buy math.
- Stability gaps: apples-to-oranges units (counts vs. percentages vs. missing),
  no severity weighting, no telecom-carrier vs. platform blame split.
- Bias surface undisclosed: preferred voices (Katia, Fish Audio), possible
  affiliate or agency incentives, and the Secure Benchmark's independence
  are all unstated — read picks as informed opinion, not independent results.

## Applicability
- Use the four-criteria frame (voice, latency, cost, stability) for any
  managed-voice-layer vs. own-pipeline decision, and add a fifth:
  operability (observability, evals, replay, incident severity).
- Reuse the normalization discipline: pin STT, LLM, TTS, and telecom vendors
  before comparing per-minute prices or latency medians across platforms.
- Treat "no single winner" as a routing rule: segment by operator skill and
  constraint (agency speed, developer control, infrastructure ownership,
  voice realism, client editing, regulated long calls), not by leaderboard.
- **Relevance to my work**
  - AI/ML engineering: adopt the vendor-footnote audit (endpointing,
    transport, network) as a required check in every realtime voice eval;
    demand p50/p90/p99 over real phone lines instead of time-to-first-audio.
  - Agentic systems: apply the shared-stack lesson to agent scaffolding —
    differentiation comes from tool routing, prompt and state management,
    interruption handling, and eval harnesses, not the base model;
    benchmark turn-level latency the same way.
  - Elisity data platform: treat call transcripts, metadata, and incident
    signals as pipeline data with schemas and retention rules; normalize
    per-minute cost plus engineering labor before recommending any
    managed-vs.-self-hosted ingestion path.

## What this changes
- Demotes voice quality from platform feature to procurement choice:
  select the TTS bundle first, then the thinnest reliable orchestration.
- Resets latency expectations to ~1.7–2.5s medians on managed stacks;
  sub-second vendor claims become a red flag unless endpointing and
  transport are explicitly included.
- Reframes LiveKit from "another option" to the only structural alternative:
  managed convenience (Retell/Vapi) versus owning workers and cutting
  marginal cost ~20x at the price of Python/JS engineering.
- Leaves compliance and reliability practice unchanged: Bland's regulated-fit
  and Vapi's availability edge are asserted, not evidenced, and both need
  independent verification before production bets.

## Verdict
- Worth keeping as a buyer's orientation and vendor-claim detector, not as
  a definitive benchmark: the latency-footnote method and cost-normalization
  frame survive scrutiny, while the rankings rest on thin, single-source,
  partially incomparable data.
- Before committing: rerun a pinned-config trial on your own prompts,
  regions, and concurrency; capture p50/p90/p99 turn latency, WER,
  interruption success, and cost per resolved call; weight incidents
  by severity from status history.
- **trial**
