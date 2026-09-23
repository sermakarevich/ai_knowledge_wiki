> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluation Protocol and Metrics (Table 1, Figures 3–4)
**In one sentence:** Table 1 reports English capability metrics, bystander-speech metrics, and per-pattern APR (Mandarin in Appendix B), and the chunk's legible failure-analysis text attributes most open-weight failures to the multi-speaker audio front-end rather than reasoning, based on transcript-lift and speaker-count ablations.
## Key points
- Table 1 covers English capability metrics, bystander-speech metrics, and per-pattern APR, with corresponding Mandarin results reported in Appendix B, and APR shown with a 95% Wilson score interval.
- Pattern abbreviations are Auth. (speaker authority constraint), Discl. (selective disclosure), Prior. (constraint prioritization), Seq. (sequential constraint integration), Scope (scope tracking), and Retr. (background speech retrieval).
- Dashes mean a probe was not run or no valid prediction was produced; best hosted / open-weight result per column is marked in light orange / cream, and muted teal model cells mark configurations affected by output-format errors.
- Qwen2-Audio-7B's PRR is not highlighted because it stays silent — it rarely produces an answer at all.
- Nine configurations were re-evaluated on speaker authority and selective disclosure with audio replaced by a speaker-labeled transcript under an otherwise identical protocol (96 cases per pattern; Figure 3), with right-margin deltas in APR points and a dashed line separating hosted from open-weight configurations.
- Hosted Gemini configurations gain at most 10.4 APR points on transcript and still fail 10–22% of cases on clean labels (residual reasoning failures), while Gemma 4-12B and MiMo-Audio-7B configurations gain 21–44 points averaged over the two patterns, with Gemma 4-12B reaching 84.4% and 85.4% APR.
- Figure 4 reports relative ARS between three- and two-speaker cases with 95% confidence-interval bars, including Gemini 3.1 Pro −2.4 pp, Gemini 3.5 Flash −1.6 pp, GPT RT 2.1 +1.3 pp, Qwen3-Omni-30B +1.0 pp, and across-models −0.5 pp.
- The chunk's Table 2 fragment reports rater agreement over paired binary rubric decisions: LLM judge ↔ Human n=869, agree .83, κ .63; Human ↔ Human n=482, agree .79, κ .56.
---
## Table 1 caption and legend
Table 1: English capability metrics, bystander-speech metrics, and per-pattern APR; corresponding Mandarin results are reported in Appendix B. APR is shown with a 95% Wilson score interval. Dashes: probe not run, or no valid prediction produced.

> "Auth.: speaker authority constraint, Discl.: selective disclosure, Prior.: constraint prioritization, Seq.: sequential constraint integration, Scope: scope tracking, and Retr.: background speech retrieval. Light orange / cream: best hosted / open-weight result per column; muted teal model cells: configurations affected by output-format errors. Qwen2-Audio-7B's PRR is not highlighted: it stays silent because it rarely produces an answer at all."

No Table 1 body numbers are legible in this chunk (OCR garble); only the caption and legend above are usable.

## Figure 3: interleaved audio vs speaker-labeled transcript
> "Figure 3: APR with interleaved audio versus a speaker-labeled transcript of the same conversations, under an otherwise identical protocol (96 cases per pattern). Right margins give the change in points; the dashed line separates hosted from open-weight configurations. † Thinking enabled."

Legible transcript-lift deltas (speaker authority / selective disclosure):

| Configuration | Speaker authority lift | Selective disclosure lift |
|---|---|---|
| Gemini 3.1 Pro† | +2.1 | +4.2 |
| Gemini 3.5 Flash† | +2.1 | +10.4 |
| Qwen3-Omni-30B | +2.1 | +0.0 |
| Gemma 4-12B† | +28.1 | +54.2 |
| Gemma 4-12B | +41.7 | +46.9 |
| MiMo-Audio-7B† | +21.9 | +19.8 |
| MiMo-Audio-7B | +24.0 | +42.7 |
| Qwen2.5-Omni-7B | +9.4 | +7.3 |
| Phi-4-Multimodal | +26.0 | -21.9 |

Axes are APR (%) 0 / 50 / 100 for interleaved audio versus labeled transcript.

## Section 5.2 Failure Analysis (verbatim fragments)
> "A failed case can break at either of two stages: mishearing who said what, or misreasoning over what was heard."

> "To separate them, we re-evaluate nine configurations on the speaker authority constraint and selective disclosure patterns, replacing the audio with a speaker-labeled transcript under an otherwise identical protocol (Figure 3)."

> "The transcript lift orders inversely with audio capability: the two hosted Gemini configurations gain at most 10.4 APR points and still fail 10–22% of cases on clean labels—their residual failures are reasoning—while the Gemma 4-12B and MiMo-Audio-7B configurations gain 21–44 points averaged over the two patterns; Gemma 4-12B reaches 84.4% and 85.4% APR, hosted level."

> "Qwen2.5-Omni-7B and Phi-4-Multimodal gain less (8.3 and 2.1 points), the latter because its transcript APR falls on selective disclosure while rising on speaker authority."

> "For open-weight models the bottleneck is the multi-speaker audio front-end, not the reasoning behind it."

A further sentence is truncated in the chunk: "Two checks sharpen this. The surviving reasoning failures survive the transcript: on speaker authority cases whose authorized speaker never states a stance (gold behavior: with-…" — remainder not legible.

## Figure 4: three- vs two-speaker relative ARS
> "Figure 4: Relative ARS between three- and two-speaker cases. Bars denote 95% confidence intervals. † Reasoning/thinking enabled."

Legible values (percentage points):

| Configuration | Relative ARS |
|---|---|
| Gemini 3.1 Pro† | −2.4 pp |
| Gemini 3.5 Flash† | −1.6 pp |
| GPT RT 2.1 xh† | +1.3 pp |
| Qwen3-Omni-30B | +1.0 pp |
| Across models | −0.5 pp |

Axis ticks: −10 −5 0 +5 +10.

## Table 2 fragment (rater agreement)
Table 2: Agreement across raters in the human study, over n paired binary rubric decisions: one pair per human label for the judge, and one pair per distinct annotator pair for Human ↔ Human.

| Rater pair | n | agree ↑ | κ↑ |
|---|---|---|---|
| LLM judge ↔ Human | 869 | .83 | .63 |
| Human ↔ Human | 482 | .79 | .56 |

**Covers:** Table 1 caption/legend; Figure 3 transcript-vs-audio ablation with per-model APR lifts; Section 5.2 Failure Analysis text; Figure 4 three- vs two-speaker relative ARS; Table 2 rater-agreement fragment
