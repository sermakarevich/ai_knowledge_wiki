> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows

## Claims vs. evidence
- Central claim — post-interruption recovery is a distinct, undermeasured capability — is well supported: RQ is the lowest-correlated axis (r̄ = 0.56) against four AudioMultiChallenge axes, and TF/RQ leaders diverge (GPT Realtime 2 medium TF .728±.03 vs. Gemini 2.5 Flash thinking RQ .704±.04).
- Closed-weight robustness claim is strong: 10/10 open-weight configs degrade with depth (mean slope −0.053) vs. closed mean −0.016, Welch t = 7.74, p < 1e-6; overall 24/26 slopes negative, mean −0.030/turn.
- Modality-gap claim is carefully bounded: TOST shows Gemini audio≡text within ±0.02 (diffs −0.007 TF, −0.001 RQ) while open-weight text wins by ~8 pts TF / ~6 pts RQ, and "audio never wins" holds across 15 dual-modality configs — but OpenAI models were excluded from this comparison.
- Judge-validity claim is credible but not airtight: second-judge ranking preserved (ρ = 0.99 TF, 0.95 RQ; κ = 0.75/0.70) and judge–human κ (0.45–0.51 TF, 0.41–0.44 RQ) matches human–human (0.43/0.40), yet absolute agreement remains in the moderate "substantial" band, not near-perfect.
- Filler-backchannel differentiator (GPT 7–31%, Gemini 2.5 62–68%, Gemini 3.x 13–32%) is striking but rests on only 60 filler cases (14% of 428), so family rankings on this slice have wide uncertainty.
- Normal (0.71–0.85) and topic-switch (0.65–0.90) pass bands show most models handle cooperative and return-to-workflow cases, bounding the novelty claim: the benchmark discriminates on filler, impatient (0.45–0.68), and correction (0.52–0.75), not everywhere.
- Depth analysis excludes the TF baseline (26 configs, t(25) = −7.04, p < 1e-6), a sound choice, but only two GPT Realtime configs escape negative slopes — the "closed robustness" story leans heavily on one family.
- Cross-benchmark distinctness rests on n=27 paired models with TF itself correlating at r̄ = 0.71 inside the AMC band, so the "distinct axis" claim applies to RQ specifically, not the benchmark as a whole.

## Genuinely new vs. repackaged
- Genuinely new: reframing evaluation from interruption *timing* (barge-in, endpointing, turn-taking) to *what the agent says next* — resume-at-correct-step with type-specific recovery rules across six intents.
- Genuinely new: per-interruption rubrics fixed at construction time (before any model response), enabling both comparative TF judging and all-criteria-met RQ pass/fail on the same sample.
- Adapted, not invented: multi-agent generation pipeline (round planner, user/assistant simulators, verifier, verify–modify loop) extends MultiChallenge/SOTOPIA/self-evolving-judge patterns to workflow-grounded mid-utterance cut-ins with grounding and type-isolation constraints.
- Adapted: LLM-as-judge with TOST equivalence, bootstrap CIs (1000-iteration, N=428), and greedy-entropy distinctness analysis applies standard statistical machinery rather than new methodology.
- Clarifying contribution: the TF-vs-RQ partial independence (leaders differ per axis) gives practitioners two knobs instead of one blended score.
- Incremental honesty: thinking/reasoning variants lift Gemini TF but not consistently RQ, and the secondary judge's near-constant RQ leniency offset is disclosed rather than hidden — small signs of careful reporting.
- Positioning vs. InterruptBench [50] and proactive-agent work [46] is fair: those cover text web-navigation and digression-return, not speech-native mid-utterance cut-ins with overlap timing (0.15–1.20s) and truncation grounding.

## Weaknesses and blind spots
- Small synthetic base: 45 conversations / 428 interruption points across 10 domains is thin for 27-config comparisons; correction type has only 25 cases (5.8% vs. ~53 expected) because synthesis skips corrections without revisable prior info.
- Depth skew: 39.5% of interruptions fall in turns 0–4 and only 11.4% in turns 15–19, so "degradation with depth" is estimated where data is scarcest.
- Generator–judge circularity: rubrics are LLM-generated alongside the data and scored by LLM judges (GPT-5.4-mini primary), so shared-model biases may inflate agreement; the second judge mitigates but does not eliminate this.
- English-only, text-scored: evaluation covers textual recovery content only — no prosody, overlap acoustics, latency, or full-duplex timing — despite the voice-agent framing.
- Audio pipeline opacity: two wiki chunks (benchmark-design overview, judge-agreement page) are garbled OCR with only figure captions recoverable, limiting independent scrutiny of synthesis and agreement details from these materials.
- Rubric strictness risk: all-criteria-met RQ pass/fail is brittle — one missed sub-criterion fails the whole recovery, which may understate partially correct handling.
- Excluded comparisons: OpenAI models and Kimi-Audio-7B skipped in audio-vs-text (no text-only input), so the "audio never wins" headline does not cover the TF-leading GPT Realtime family.
- Human-study scale is modest: 616 paired decisions per study across ~30 annotators at ~20 items each, with leave-one-out/Holm checks finding no bad annotators — reassuring, but conclusion-level ranking match (ρ = 1.0 RQ, 0.90 TF) rests on just 5 study models.
- Synthetic user intents skew adversarial by design (pushback 24.5%, dominant in 26/45 conversations), so real-traffic cooperative mixes would likely show higher absolute scores than reported.
- No cost/latency reporting: reasoning variants and judge epochs (3 per config, dual judges) carry inference budgets that matter for production voice agents but go unquantified here.
- Single-threshold TOST margins (±0.02/0.03/0.05) are reasonable but stipulated, not grounded in a user-perceptible-difference study — "equivalent" means statistically, not experientially.

## Applicability
- Direct use fits teams shipping state-machine voice agents (support, scheduling, claims) who need regression tests for correction integration, filler continuation, and topic-switch-and-return.
- Method transfers to any step-driven agent eval: fix per-incident rubrics at construction time, score outcome (TF) separately from handling quality (RQ), and validate judges with a second provider plus human spot-checks.
- Statistical template is reusable: TOST equivalence for modality ablations, per-depth logistic slopes for context-rot detection, cross-benchmark correlation for "is this a new axis?" claims.
- **Relevance to my work**
  - *AI/ML engineering:* adopt the two-axis pattern (task outcome vs. recovery handling) and TOST ±0.02-style equivalence checks for our own model-comparison and modality-ablation reports.
  - *Agentic systems:* port the six-type interruption taxonomy (correction, topic switch, filler, pushback, impatient, normal) to tool-calling agents — injected mid-plan corrections and digressions with resume-at-correct-step scoring.
  - *Elisity data platform:* recovery-quality-style rubrics suit data-pipeline agent evals (e.g., interrupted onboarding or policy workflows): verify state consistency after user corrections without re-asking settled fields, mirroring the verify–modify loop.
  - *Elisity data platform (continued):* per-incident fixed rubrics plus a second-provider judge give audit-friendly evidence for workflow-agent behavior changes, complementing existing integration tests.
- Caution for transfer: our interruptions are mostly text/tool-plan digressions, not spoken overlap, so adopt the rubric-and-resume pattern without copying audio-specific thresholds (overlap times, TTS formatting).

## What this changes
- Treat "handles interruptions" as two separate release gates: does the task still complete (TF) and was the recovery itself correct (RQ) — a model can pass one and fail the other.
- Add filler/backchannel continuation ("exactly continue the cut-off utterance, no restart, no acknowledgement") to eval suites; it is the cheapest test and currently the sharpest family separator.
- Expect depth degradation as the default for open-weight audio models (~3.3× faster than closed) and budget context-management work accordingly rather than assuming flat performance.
- Do not assume audio input adds value over transcripts for open-weight stacks — text won outright here; measure audio-vs-transcript equivalence before paying audio-inference costs.
- Plan training, not just prompting, for recovery behaviors: the authors' "undertrained, not inherently hard" framing plus sharp family gaps suggests data and post-training gaps rather than prompt fixes.
- Version-pin voice models around filler handling: the Gemini 2.5 → 3.x filler regression (62–68% down to 13–32%) shows recovery behavior can silently regress across upgrades — gate releases on it.
- Weight corrections disproportionately in internal evals: with only 25 correction cases here, real workflows should over-sample "actually, use X instead" paths since correction-integration failures are high-severity.

## Verdict
- Useful benchmark with a portable evaluation pattern, but its small synthetic English-only base, thin correction slice, text-only scoring, and generator–judge circularity cap how literally to take absolute scores.
- Rank-order signals (who recovers, where depth/modalities break) are trustworthy enough to guide engineering; pass-rate point values are not.
- Next burden of proof lies with multilingual coverage, live-interaction validation, timing/acoustic integration, and showing rubric post-training actually moves RQ without TF regressions.
- For our purposes the transferable asset is the method (fixed per-incident rubrics, TF/RQ split, TOST + depth-slope + second-judge validation), not the leaderboard — **trial**.
