[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Per-Type Recovery Breakdown and Audio-vs-Text Recovery Quality (Table 4, Figure 8)
**In one sentence:** Human validation shows the judge agrees with annotators at least as well as annotators agree with each other and preserves model rankings, while per-type results single out filler backchannels as the hardest case with the largest model gap and show audio input never beats text for open-weight models on recovery quality.
## Key points
- The two human studies used disjoint annotator pools with 616 paired human–judge decisions each across 5 study models, and all 300 items rated by two or more annotators to estimate inter-annotator agreement.
- Human–judge agreement slightly exceeds inter-annotator agreement (κ = 0.45–0.51 vs. 0.43 on TF; 0.41–0.44 vs. 0.40 on RQ), attributed to the judge being one consistent rater versus ~30 annotators spread thinly at about 20 items each.
- Per-model human rankings match the judge almost exactly: recovery quality rank-for-rank (ρ = 1.0) and task fulfillment off by one adjacent swap of GPT-REALTIME-MINI and MIMO-AUDIO-7B-THINKING (ρ = 0.90), scored 0.489 vs. 0.494 and essentially tied.
- No annotator was excluded: leave-one-out majority agreement tested by one-sided binomial test against the cohort base rate with Holm correction never referenced the judge and found no annotator significantly worse than chance in either study.
- Filler backchannels like "mm-hm" are hardest for GPT models (0.07 for GPT Realtime Mini to 0.31 for GPT Realtime), with failure modes of restarting, acknowledging the filler, or producing a new response, versus 0.62–0.68 for the Gemini 2.5 family and sharp regression to 0.13–0.32 in Gemini 3.x.
- Normal interruptions (0.71–0.85) and topic switches (0.65–0.90) are well-handled across models, while impatient recovery clusters at 0.45–0.68 and correction spreads 0.52–0.75, partly from smaller per-type samples.
- On recovery quality, six frontier Gemini models are statistically equivalent across audio and text input (within ±0.02), while nine open-weight configurations gain from text input (RQ Pass audio−text = −0.062) and audio never wins.
---
## Human–judge validation design
Task-fulfillment annotators chose which of two responses better satisfied the restated criterion — "exactly the comparative call the judge makes" — while recovery-quality annotators answered per-criterion yes/no pass questions for a single response. Items are "a stratified subset of 60 of the 428 interruption points (300 model×sample items per axis), chosen to span interruption types and conversation depth", so "per-model rates therefore carry sampling uncertainty, while the sample-level agreement in Table 3 is computed on the full set of human judgments."
## Agreement levels and ranking preservation
> "Human–judge agreement slightly exceeds inter-annotator agreement (κ = 0.45–0.51 vs. 0.43 on TF; 0.41–0.44 vs. 0.40 on RQ). This is expected rather than surprising: the judge is a single fixed rater applied uniformly to all items, whereas each study spreads its ∼30 annotators thinly (about 20 items each)."

This holds for primary or secondary judge, so validation "is not specific to one judge." Per-model human ranking matches the judge across all five study models with either judge.
## D — Per-type recovery quality breakdown
Table 4 gives "the full per-model recovery quality pass rate broken down by the six interruption types, summarized in the main text (Section 5.2)."
### Filler is hardest for GPT models
> "When a user produces a brief backchannel like “mm-hm” mid-utterance, the correct recovery is to continue the utterance from where it was cut off, without repeating or restarting."

GPT filler pass rates are 0.07 (GPT Realtime Mini) to 0.31 (GPT Realtime); modes are "restarting the utterance, acknowledging the filler (“Glad you’re following along!”), or producing an entirely new response." Gemini 2.5 family: "Gem. 2.5 Pro 0.62, Gem. 2.5 Flash thinking 0.68, Gem. 2.5 Flash 0.64", but "Gemini 3.x regresses sharply (0.13–0.32), suggesting filler handling did not carry over to the newer model line. This is the single largest model-to-model gap among the six interruption types."
### Normal and topic switch are well-handled
"Across models, normal interruptions are handled at 0.71–0.85 pass rate and topic switches at 0.65–0.90, suggesting that addressing a relevant cut-in and engaging with a new topic are relatively natural capabilities for current LLMs."
### Impatient and correction are middle difficulty
"Impatient recovery (skipping content the user asked to skip) clusters around 0.45–0.68, with Gemini 3.1 Pro the best at 0.66 and GPT Audio Mini the worst at 0.47. Correction recovery (accepting a self-correction without pushback) shows a wider spread of 0.52–0.75, partly driven by smaller per-type sample sizes (Section A)."
### Table 4: Recovery quality pass rate by interruption type (audio input, 3 epochs)
Mean ± half-width of 95% percentile bootstrap CI (1000 resamples). Best per column in bold. † = Thinking/reasoning-enabled.

| Model | Normal | Impat. | Corr. | Topic | Filler | Push. |
|---|---|---|---|---|---|---|
| GPT Realtime 2 (medium) | .76±.08 | .52±.09 | .73±.14 | .76±.08 | .19±.08 | .72±.07 |
| GPT Realtime 2 (xhigh)† | .78±.08 | .49±.09 | .68±.15 | .76±.08 | .16±.07 | .72±.08 |
| GPT Realtime 1.5 | .82±.07 | .57±.09 | .68±.15 | .90±.06 | .13±.07 | .72±.07 |
| GPT Audio | .82±.08 | .54±.10 | .76±.13 | .77±.08 | .22±.09 | .74±.07 |
| Gem. 3 Flash† | .77±.08 | .54±.10 | .63±.16 | .80±.07 | .14±.07 | .66±.07 |
| Gem. 3 Flash | .81±.07 | .53±.09 | .76±.13 | .87±.06 | .32±.10 | .68±.08 |
| GPT Realtime | .83±.07 | .60±.09 | .72±.15 | .80±.07 | .31±.11 | .74±.08 |
| Gem. 2.5 Flash† | .75±.08 | .58±.09 | .63±.15 | .78±.08 | .68±.11 | .75±.08 |
| Gem. 3.1 Pro† | .82±.07 | .66±.10 | .57±.18 | .82±.08 | .13±.07 | .71±.07 |
| Gem. 2.5 Pro† | .75±.08 | .69±.08 | .65±.15 | .77±.07 | .62±.10 | .66±.08 |
| Gem. 2.5 Flash | .76±.08 | .58±.09 | .61±.17 | .77±.08 | .64±.10 | .67±.08 |
| GPT Audio Mini | .77±.08 | .48±.09 | .72±.15 | .65±.08 | .08±.06 | .71±.07 |
| GPT-4o Audio | .82±.08 | .64±.11 | .76±.16 | .85±.09 | .08±.08 | .71±.09 |
| Gem. 3.1 Flash Live | .75±.08 | .58±.09 | .57±.19 | .74±.08 | .24±.09 | .66±.08 |
| GPT Realtime Mini | .80±.07 | .55±.09 | .60±.17 | .82±.07 | .07±.06 | .72±.08 |
| Gem. 3.1 Flash Live† | .74±.08 | .57±.09 | .63±.15 | .74±.08 | .23±.08 | .64±.08 |
| GPT-4o Mini Audio | .83±.08 | .64±.10 | .52±.20 | .88±.07 | .15±.08 | .70±.09 |
| Gemma 4 12B Instruct† | .66±.09 | .52±.09 | .44±.16 | .70±.07 | .25±.08 | .58±.07 |
| Gemma 4 12B Instruct | .63±.09 | .51±.09 | .48±.15 | .67±.08 | .22±.08 | .60±.08 |
| MiMo-Audio-7B† | .68±.08 | .36±.08 | .47±.16 | .72±.07 | .03±.03 | .68±.07 |
| MiMo-Audio-7B | .68±.06 | .47±.09 | .45±.15 | .66±.07 | .40±.11 | .67±.07 |
| Voxtral-Small-24B | .74±.07 | .53±.09 | .49±.15 | .70±.08 | .36±.10 | .61±.08 |
| Qwen3-Omni-30B | .80±.07 | .63±.08 | .55±.17 | .80±.06 | .46±.10 | .69±.07 |
| Kimi-Audio-7B | .61±.09 | .45±.08 | .44±.16 | .68±.08 | .32±.10 | .53±.07 |
| Qwen2.5-Omni-7B | .65±.08 | .53±.08 | .33±.14 | .66±.08 | .35±.09 | .49±.07 |
| Phi-4-Multimodal | .52±.09 | .56±.08 | .28±.13 | .63±.07 | .18±.07 | .44±.07 |
| Qwen2-Audio-7B | .51±.10 | .44±.08 | .31±.13 | .58±.10 | .14±.07 | .30±.07 |
## E — Audio vs. text-only recovery quality
"Figure 8 is the recovery-quality counterpart of the task-fulfillment audio-vs-text comparison in the main text (Figure 6, Section 5.6). The same conclusion holds on the RQ Pass axis: the six frontier Gemini models are statistically equivalent across modalities (within ±0.02), while the nine open-weight configurations are better with text input (RQ Pass audio−text = −0.062), and audio never wins."
## F — AudioMultiChallenge scoring (chunk truncated)
Chunk ends mid-sentence: "The cross-benchmark analysis in Section 5.5 pairs each of" — no further claims present in this chunk.
**Covers:** Human–judge validation tail; Section D per-type recovery quality breakdown with Table 4; Section E audio-vs-text recovery quality (Figure 8); Section F opening fragment
