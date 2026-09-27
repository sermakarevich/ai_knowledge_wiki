> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: renan-martini/saybench

## Claims vs. evidence
- Claim: benchmark your own audio — accents, jargon, failure modes —
  not vendor lab numbers, yielding accuracy, latency, and cost.
- Evidence for that claim is strong on mechanism: JSONL manifests for own
  clips, per-category splits, and a `compare -max-wer-regression` CI gate
  are concrete, implemented workflow, not aspiration.
- Claim: five modes cover each pipeline failure point (batch STT,
  streaming STT, LLM turn, S2S, TTS), each runnable with zero keys.
- Evidence is moderate: per-mode metrics are specific (WER breakdown,
  TTFP/finalization/survival, TTFT/tok-per-s, voice-to-voice/echo/barge-in,
  time-to-first-audio), but all definitions come from project docs with no
  independent validation visible in the digest or wiki notes.
- Claim: "scoring you can trust" via corpus WER, keyterm recall, opt-in
  digit normalization, opt-in LLM-judge, and `—` where there is no data.
- Evidence is moderate: the honest-`—` doctrine and condition-aware compare
  warnings (warm-vs-cold, echo-vs-conversational, cross-mode refusal) are
  credible trust signals, yet judge rubrics and normalization edge cases
  are uncharacterized in the material reviewed.
- Claim: golden-set findings generalize (ranking inversions, 5x TTFP gap,
  3x cold-TLS effect, speech-native latency advantage).
- Evidence is weak-to-moderate: results are September 2026 live-API runs on
  a small bundled set (14 clips in the example), so they read as
  illustrative rather than generalizable.
- Claim: single static Go binary, stdlib plus one dependency, env-only
  keys, deadlines plus bounded reads.
- Evidence is strong: go.sum pins exactly `coder/websocket v1.8.15`, and
  the SECURITY/CLAUDE rules corroborate env-only keys, `io.LimitReader`,
  and the 100 MiB / 1 MiB input caps.

## Genuinely new vs. repackaged
- Genuinely new: the combination is the contribution — own-clip,
  per-failure-mode voice benchmarking fused with live-call latency
  dimensions, cost columns, deterministic fakes, and a CI gate in one
  binary.
- Genuinely new: streaming metrics as first-class citizens
  (time-to-first-partial, finalization lag, interim word survival fed at
  real-time pace) instead of batch-WER-only leaderboards.
- Genuinely new: honesty engineering as product feature — `—` over fake
  zeros, README/docs examples restricted to pasted real output, and
  batch-vs-streaming framing that refuses to flatter.
- Repackaged: per-vendor adapters and `custom` escape hatches follow
  standard harness practice; the two-method provider interface is good
  design, not novel.
- Repackaged: JSON reports plus single-file HTML dashboard are conventional
  tooling, competently scoped (A/B compare, trends, worst-clips table).
- Repackaged: the MCP server and Pipecat mapping extend reach into agent
  stacks but reuse existing protocols rather than inventing new ones.

## Weaknesses and blind spots
- Small golden set: the headline example is 14 clips, so inversion claims
  on acronyms, names, and conversational speech need larger stratified
  corpora before carrying weight.
- Synthetic-audio caveat: golden audio is repo-original and locally
  synthesized, which solves licensing but understates telephony noise,
  overlap, and accent breadth.
- Statistical thinness: no confidence intervals, significance tests, or
  run-to-run variance appear in the digest; a 2-point WER gate looks
  arbitrary without variance data.
- Judge risk: opt-in LLM-rated semantic preservation sits beside WER with
  no visible rubric, agreement study, or cost accounting here.
- Single-maintainer surface: env-only keys, a personal-inbox vuln address
  with a one-week reply promise, and roadmap "order is intent, not promise"
  signal bus-factor and support risk for production-CI reliance.
- Coverage gaps: cost columns depend on user-supplied pricing tables, which
  drift; reports embed reference transcripts with no redaction tooling, so
  sensitive corpora need external handling.
- Live-API brittleness: published findings implicitly depend on vendor
  behavior at measurement time and will rot as endpoints change.

## Applicability
- Fits where voice quality gates decisions: provider selection, endpoint
  or transport swaps, and pre-release regression checks on your own clips.
- Does not fit as a general speech-science benchmark or a substitute for
  production call analytics; it measures a sampled harness, not live
  traffic distributions.
- **Relevance to my work**
  - AI/ML engineering: adoptable eval-harness pattern — deterministic
    fakes, stable schema with `SchemaVersion`, numeric `compare` gate, and
    real-output-only docs map directly onto model and pipeline CI.
  - Agentic systems: the MCP server makes the whole tool drivable by coding
    agents, and S2S echo/barge-in metrics cover turn-taking failures that
    text-only evals miss in voice-agent stacks.
  - Elisity data platform: directly applicable wherever voice touches the
    platform (support calls, field-ops input) — per-category WER plus
    keyterm recall on internal jargon is the right acceptance shape.
  - Elisity data platform (transferable): even without a voice surface, the
    template — own-corpus manifests, cost columns, condition-aware gates,
    dashboard — ports to data-pipeline quality checks.

## What this changes
- Shifts vendor evaluation from lab leaderboards to own-corpus,
  per-failure-mode numbers: a vendor can win aggregate WER yet lose on the
  acronyms and names that decide your purchase.
- Makes streaming latency a selection criterion independent of batch
  accuracy — a ~400ms batch gap hiding a 5x time-to-first-partial gap
  changes architecture, not just vendor choice.
- Normalizes cold-start and transport hygiene (default-on warmup, quantified
  TLS effects) as part of benchmarking rather than folklore.
- Lowers continuous voice regression to unit-test ergonomics: zero-key
  `fake` mode plus one binary plus a numeric gate means voice checks can
  live in the same pipeline as everything else.

## Verdict
- Strengths (own-corpus focus, streaming metrics, honest-scoring doctrine,
  minimal-dependency binary, agent-accessible surface) outweigh the
  small-sample and single-maintainer caveats for evaluation use.
- The failure mode it prevents — shipping a vendor or transport change that
  silently degrades the utterances you actually care about — is expensive
  and common enough to justify the setup cost.
- Keep the CI gate advisory until run-to-run variance on your corpus is
  understood, then promote it to blocking on the categories that matter.
- **trial**: run it against your own clips on one voice surface, hold the
  gate advisory, and revisit on a larger corpus before wider rollout.
