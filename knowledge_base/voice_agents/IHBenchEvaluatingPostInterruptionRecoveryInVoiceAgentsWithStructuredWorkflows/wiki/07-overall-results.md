[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overall Results: Per-Model Points, Judge Agreement, Depth, and Recovery Quality
**In one sentence:** Figure 3 plots per-model points with full agreement breakdowns deferred to Appendix B, judges agree with each other and with humans at human-level, task fulfillment degrades significantly with conversation depth especially for open-weight models, and recovery quality forms a capability axis largely distinct from existing multi-turn audio evaluation.
## Key points
- Figure 3 plots per-model points; full agreement breakdown across every rater pair on both axes (sample-level agreement, Cohen's κ, per-model rank/value correlations) is deferred to Appendix B.
- Second judge Gemini 3 Flash (with thinking) preserves model ranking (Spearman ρ = 0.99 on TF and 0.95 on RQ) with sample-level 3-epoch verdict agreement in the "substantial" range (Cohen's κ = 0.75 on TF and 0.70 on RQ).
- Secondary judge is slightly more lenient on RQ but offset is near-constant (ranking preserved, fit slope close to 1), so it is described as inconsequential.
- Judge agrees with humans at human level: per-item judge-human κ = 0.45–0.51 vs human-human 0.43 on TF and 0.41–0.44 vs 0.40 on RQ; conclusion-level rankings match at ρ = 1.0 on RQ and ρ = 0.90 on TF (single adjacent swap of two mid-pack models).
- Task fulfillment degrades with depth: 24 of 26 remaining audio configurations have negative logistic-regression slopes on user message index, mean slope −0.030 per turn, one-sample t-test t(25) = −7.04, p < 10−6; only GPT Realtime 2 and GPT Realtime 1.5 have non-negative slopes.
- Open-weight models degrade faster with depth: 10 open-weight configurations all negative (−0.034 to −0.069, mean −0.053) vs 16 closed-weight mean −0.016, Welch t-test closed vs open gives t = 7.74, p < 10−6.
- IHBench RQ is a distinct axis: mean intercorrelation r̄ = 0.56 (lowest in 6×6 matrix with 4 AMC axes + TF + RQ), vs AMC axes intercorrelating r = 0.65–0.93 and TF sitting within that band at r̄ = 0.71; greedy entropy selection picks IHB-RQ #2.
- Recovery varies sharply by interruption type: filler is the largest model-to-model differentiator (GPT-family 7%–31%, Gemini 2.5 family 62%–68%, Gemini 3.x 13%–32%), while normal interruptions (0.71–0.85 pass) and topic switches (0.65–0.90) are handled well across the board.
---
## Figure 3 and agreement headline numbers
**Covers:** §5, Figure 3 and judge-agreement summary

Figure 3 plots the per-model points; the full agreement breakdown across every rater pair on both axes (sample-level agreement, Cohen's κ, and per-model rank/value correlations) is deferred to Appendix B, with headline numbers summarized below.

## The judges agree with each other
**Covers:** §5, second-judge validation

The second judge is Gemini 3 Flash (with thinking), run over all responses. The model ranking is well preserved (Spearman ρ = 0.99 on TF and 0.95 on RQ) and the two judges' 3-epoch verdicts agree at the sample level in the "substantial" range (Cohen's κ = 0.75 on TF and 0.70 on RQ), at or above the inter-judge κ values typically reported for LLM-as-judge in MT-Bench [48]. The secondary judge is slightly more lenient on RQ, but the offset is near-constant (it preserves the ranking, and the fit slope is close to 1), so it is inconsequential.

## The judge agrees with humans
**Covers:** §5, two Prolific studies (one per axis)

> "an LLM-distilled paragraph of the system message and the conversation history relevant to this turn, a self-contained restatement of the criterion, and the last two rounds as audio"

Annotators receive summarized context (above) because full system message and history are long and mostly irrelevant to any single interruption; full study design is in Appendix C. Validation is strong on two levels:

- Per item, the judge agrees with humans slightly more often than two humans agree with each other (κ = 0.45–0.51 vs. 0.43 on TF and 0.41–0.44 vs. 0.40 on RQ), so it is "statistically indistinguishable from an additional annotator."
- At conclusion level, human ranking matches judge almost exactly: recovery quality rank for rank (Spearman ρ = 1.0), task fulfillment differing only by a single adjacent swap of two mid-pack models (ρ = 0.90), so "every comparative claim in this paper would stand unchanged under human scoring."

Control: since humans saw only summarized context while the judge sees full context, the judge was re-run on the same summary (Figure 3); it agrees closely with the full-context judge, so the comparison is not confounded by context advantage.

## Task fulfillment vs. conversation depth
**Covers:** §5.4, Figure 4 across four depth bins

Figure 4 shows task fulfillment win rate across four conversation depth bins (by user message index).

| Claim | Numbers |
|---|---|
| Task fulfillment degrades with depth | 24 of 26 remaining audio configurations negative slope (all except GPT-4o Audio baseline); mean per-model slope −0.030 per additional turn; one-sample t-test vs zero t(25) = −7.04, p < 10−6 |
| Only non-negative slopes | GPT Realtime 2 and GPT Realtime 1.5 |
| Steepest declines | All on open-weight models |
| Open-weight slopes | 10 configs, all negative, −0.034 to −0.069, mean −0.053 |
| Closed-weight slopes | 16 configs, mean −0.016 |
| Closed vs open difference | Welch t-test gives t = 7.74, p < 10−6 |

Attribution note from chunk: gap is "consistent with open-weight models being trained primarily on short, single-turn or speech-recognition data, leaving them less robust to long multi-turn dialogue context, but our evaluation cannot separately attribute it to training data, model scale, or modality alignment."

## Recovery quality is a new capability axis
**Covers:** §5.5, pairing 27 configs with AMC axes (Figure 5)

To test whether IHBench adds information beyond existing multi-turn audio evaluation, the authors pair 27 model configurations with per-axis scores on AudioMultiChallenge (AMC) [15] and apply submodular benchmark-selection framework [37]. AMC inference was run for all 27 configurations (Appendix F). Score matrix: n=27 paired models, k=6 axes (four AMC axes + TF Win Rate + RQ Pass Rate); pairwise correlations in Figure 5.

| Claim | Numbers |
|---|---|
| AMC axes intercorrelate strongly | r = 0.65–0.93, "dominant general-capability factor" |
| IHBench TF within that band | mean r̄ = 0.71 |
| IHBench RQ does not | mean r̄ = 0.56, lowest in 6×6 matrix; gap to AMC-axis mean excludes zero under model-level bootstrap [8] |
| Benchmark selection | Greedy entropy selection [37] picks IHB-RQ #2, "though partly due to redundancy among the AMC sub-axes" |

Interpretation given: "IHBench-RQ measures recovery quality: a capability axis largely distinct from the long-context coherence skills AMC tests." IHBench-TF "partially overlaps with AMC" as "essentially a comparative measure of task progression"; residual disagreement still substantive: GPT Realtime 2 ranked #1 on TF but #4 on AMC, Gemini 3.1 Pro ranked #9 on TF but #1 on AMC.

## Recovery quality by interruption type
**Covers:** §5.5, six-type breakdown (full per-model table Appendix D)

Breaking recovery quality down by six interruption types exposes a strong type effect. Filler is the single largest model-to-model differentiator:

- GPT-family: continue correctly after a backchannel only 7%–31%
- Gemini 2.5 family: markedly better, 62%–68%
- Gemini 3.x: regresses sharply, 13%–32%
- Normal interruptions: 0.71–0.85 pass, handled well across the board
- Topic switches: 0.65–0.90, handled well across the board
- Spread concentrated in harder types.

## Text-only vs. audio-input evaluation (partial)
**Covers:** §5.6 opening lines only (chunk truncates)

> "To measure how much the audio modality itself contributes to the difficulty, we re-ran the six Gemini models and nine of the ten open-weight model configurations using transcripts"

Chunk ends mid-sentence after the table header fragment ("TF Win Rate", "Closed-weight", "Open-weight", depth bins 0–4, 5–9, 10–14, 15–19, logistic fit); no further §5.6 numbers are present in this chunk.
**Covers:** §5–§5.6 (Figure 3 per-model points through §5.6 opening; §5.6 body truncated in chunk)
