> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: SteerDuplex: Steerable Duplex Speech Dialogue Models

## Claims vs. evidence

- Claim: SFT on natural + synthetic dialogues delivers the main steerability gain. Evidence is strong within its own harness: 65.10 ± 1.13% audio-steering APR vs 20.55% Moshi / 16.44% PersonaPlex (+44.5pp), AudioMC APR 13.64% vs 6.64%, FDB-v2 4.17 vs ~2.6, VoiceBench 40.87 vs 38.55/30.51 — all three-run means with SDs.
- Claim: two-stage RL refines interruption/pause handling without harming capability. Evidence is mixed but honest: interruption response 72.5%→82.5%, backchannel continuation 71.4%→80.6%, pause barge-in 26.5%→9% — yet background-speech recovery is flat (60%→59%), semantics slip 3.94→3.88, takeover latency grows +40ms.
- Claim: capability is "retained" under RL. Retention table supports "broadly retained" only: AudioMC +0.74pp, VoiceBench +0.51, SteerBench rubric +1.47pp, FDB-v2 mean −0.003, interruption semantics −0.069. Small deltas, not uniform wins.
- Claim: timing rewards are made hack-resistant via speech-gating + continuity terms. Only partially demonstrated: promptness-only probe scores 0.670 scalar yet 0 on duplex with 25/96 empty; joint composite still leaves 4/96 empty; stage 2 raises interruption reward 0.450→0.793 while backchannel continuation falls 3.20→2.00s and noise-robustness 1.96→0.77.
- Strongest point: the paper reports its own counter-evidence (judge-sensitivity losses of −0.083/−0.098 on identical generations, staging confounds, CANDOR overlap), so headline numbers arrive pre-qualified.
- Caveat on magnitudes: the +44.5pp steering jump is SFT-vs-weak-baseline on a new benchmark the authors built; the RL deltas that matter for deployment (semantics, latency, background speech) are near-zero or negative.
- Bottom line on evidence: steering claim is convincing as a gap-closing result; interaction-RL claim is convincing only as "targeted timing improves, everything else must be watched."

## Genuinely new vs. repackaged

- Genuinely new: SteerBench — 390 spoken prompts, 1,067 human binary rubrics (438 audio / 629 text), separate content-vs-delivery scoring with fixed reference clips across tone, persona, style/accent, speed/length.
- Genuinely new: speech-gated interruption credit (no speech before interruption → no yield credit) plus response-continuity (0.5, 4s target) and continuation-duration (2.0, 4s) terms aimed at silence/truncation hacks.
- Genuinely new: component-normalized GDPO applied to duplex speech with text-stream-only policy loss (padding tokens included for pause/onset timing) and adaptive sampled-action KL instead of full-distribution KL.
- Genuinely new: the hacking/trade-off analysis itself — isolated single-family probes all collapse (≥26% empty, duplex ≤0.055) vs joint 0.371, and continued optimization eroding continuity.
- Repackaged: Moshi 7B backbone, joint temporal+depth transformer with 8 RVQ codebooks at 12.5 Hz; CANDOR/Fisher conversational data; FDB-v1/v1.5/v2, VoiceBench, AudioMC harnesses; Gemini 3.6 Flash + gpt-5.4-mini judges and TTS-synthesized eval audio.
- Synthesis: architecture is incremental; the contribution is problem framing (steerability ≠ fluency), benchmark, and RL reward engineering with unusually candid ablations.

## Weaknesses and blind spots

- Judge dependence: SteerBench/FDB-v2 hinge on Gemini 3.6 Flash; AudioMC/VoiceBench on gpt-5.4-mini. Identical-generation rescoring flips headline deltas negative under both judges — scoring convention, not just capability, moves the leaderboard.
- Synthetic benchmark construction: neutral TTS user utterances (Gemini 3.1 Flash), reference scripts from Gemini 3 Pro Preview, voices from Kore/Schedar pools. Measures single-turn English steering under explicit requests; no long-term personalization, multilingual, noisy-far-field, or real-user evaluation.
- Train-test leakage caveats: 100/216 CANDOR pause transcripts overlap 96 SFT conversations; official pause clips end 0.02–0.11s after the last word, so pause handling is partly diagnostic, not generalization proof.
- No clean ablations: controls differ in budget and configuration; seed replicate beats reported RL on turn-taking (+0.155 vs −0.003); single-stage-from-SFT underperforms with less training — staging effect is not isolated.
- Unresolved objective interference: group normalization silences any constant-within-group component, so nothing resists the dominant gradient; yielding vs continuing remains a conflict, mitigated not solved.
- Practical costs: SFT at 80×H100 (2.304M draws budget), RL ~195 GPU-h plus hosted-judge compute; SteerBench/synthetic data under restricted research licenses; in-house audio not redistributable — reproduction is heavyweight.
- Missing: human preference/MOS studies, safety under persona/accent steering, latency-quality Pareto analysis, and error bars on several RL probe deltas.
- No calibration of rubric difficulty: sample APR (32–51%) sits well below rubric pass rate (63–77%), so a few hard audio criteria dominate failures — the paper does not say which ones or whether they are the most deployment-relevant.
- Accent/style control via TTS references risks judging TTS-likeness rather than human-plausible delivery; speaker-identity handling ("fixed voice") sidesteps the hardest real-world steering conflicts.

## Applicability

- Directly reusable: separate text/audio rubric pattern with fixed reference clips; speech-gating + continuity-target pattern for any timing/segmentation reward; component-wise group normalization when combining heterogeneous rewards.
- Conditionally reusable: two-stage continuity→continuation RL recipe, but only with held-out semantic judges and empty/short-response monitors, given demonstrated erosion.
- Not transferable as-is: exact weights (1.0 timing, 0.75 transcript judge, 0.5/2.0 duration terms), 4-second targets, and TTS-anchored accent/style rubrics — all tuned to this backbone and English benchmark.

- **Relevance to my work**
  - AI/ML engineering: adopt the binary-rubric + judge-error-budget (>5% invalid run) evaluation discipline; add empty/short-output rate as a first-class RL gate alongside reward curves.
  - Agentic systems: treat "when to yield vs continue" as an explicit multi-objective conflict (as in interruption vs backchannel-continuation), not a single helpfulness score; port the speech-gating idea to tool-use/agentic interruption (no credit for yielding without a substantive partial action).
  - Elisity data platform: SteerBench-style fixed-reference rubrics fit voice-interface QA for data agents (tone/persona/speed compliance per query type); keep benchmark audio and judge prompts versioned, since regeneration changes the target; note licensing blocks redistributing raw audio — store transcripts + generation metadata instead.

## What this changes

- Reframes duplex progress: fluent turn-taking (~500ms response, backchannels) is necessary but insufficient; steerable delivery is the gap, and 16–21% baseline audio-steering pass rates make it measurable.
- Shifts RL practice for speech agents: promptness-only or single-family rewards reliably hack to silence; joint composites with continuity/validity gates are the minimum viable design, and timing wins must be reported with completeness, semantics, and latency side by side.
- Lowers the bar for honest reporting: seed replicates, judge-sensitivity rescoring, and overlap disclosures are presented as standard appendix material — a template worth copying.
- Does not change: the need for real-user, multilingual, noisy-condition evidence before claiming deployable steerable duplex dialogue.

## Verdict

- SFT steerability gains are large and well-measured enough to learn from; RL timing gains are real but narrow, fragile, and judge-sensitive.
- Reuse the benchmark design and reward-gating patterns; do not lift hyperparameters, TTS-anchored style targets, or the two-stage recipe wholesale.
- Next step if trialing: re-implement separate content/delivery rubrics on one internal voice task, add empty-rate + semantic-retention gates, and require judge-swap robustness before any rollout claim.
- Scope the trial to evaluation methodology and reward-gating patterns first; treat the full duplex model weights as reference, not a drop-in dependency.
- Bold call: **trial**
