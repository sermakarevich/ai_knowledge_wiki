> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Results, SNR Ablation, Human Study, Limitations and Conclusion
**In one sentence:** This chunk reports that speaker count does not explain failures, that background-speech recovery collapses at low SNR while some models compound misses with fabrication, that the LLM judge agrees with humans at 82.6%, and that no system is reliable with multi-speaker memory weakest and open-weight bottlenecks perceptual versus frontier bottlenecks reasoning.
## Key points
- Open-weight configurations execute anyway — treating silence as consent — on 28.6% of cases with audio and 33.3% with transcripts, and the lift is not a formatting artifact.
- Under constrained decoding, invalid predictions stay below 3.2% in both modalities for every configuration except MiMo-Audio-7B's audio runs, and Gemma 4-12B with no format errors in either modality still gains 42–47 points — the gain is perceptual, not syntactic.
- Within balanced pattern-by-scene cells every model's three- versus two-speaker contrast is statistically indistinguishable from zero (Figure 4), and pooling four models leaves −0.5 ARS and +1.5 APR points, both within sampling error: speaker count is not the primary bottleneck.
- The SNR ablation remixes 96 English background-speech retrieval cases at seven fixed background-to-foreground SNRs from +8 to −8 dB in a take-paired design, with three hired Prolific workers performing the same task.
- Gemini 3.1 Pro capture falls from 62.5% at +8 dB to 15.6% at −8 dB versus human average 98.5% to 15.5%, while GPT Realtime 2.1 admits 42–56% of misses at every level but Gemini 3.1 Pro admits 44.4% at +8 dB down to 6.2% at −8 dB and GPT Audio 1.5 declines from 23.3% to 10.5%.
- The LLM judge agrees with humans on 82.6% of judgments (Cohen's κ = 0.63, 95% CI [0.57, 0.69]; Gwet's AC1 = 0.67) while marginally stricter (60.2% vs. 61.9% pass), exceeding inter-annotator agreement (κ = 0.56, 79.3%).
- Across 12 models and 15 configurations the strongest configuration passes all rubrics on only 66.8% of English and 54.5% of Mandarin cases (strongest open-weight: 34.0% and 19.3%), with multi-speaker memory the weakest capability family.
---
## Silence-as-consent and constrained-decoding check
> "hold), open-weight configurations execute anyway—treating silence as consent—on 28.6% of cases with audio and 33.3% with transcripts."

> "And the lift is not a formatting artifact: under constrained decoding, invalid predictions stay below 3.2% in both modalities for every configuration except MiMo-Audio-7B's audio runs, and Gemma 4-12B, with no format errors in either modality, still gains 42–47 points—the gain is perceptual, not syntactic."

## Speaker count is not the bottleneck
> "Since every added speaker is another voice to separate and another identity to track, more speakers might be expected to make a test case harder. But for the strongest hosted and open-weight configurations they do not: within balanced pattern-by-scene cells, every model's three- versus two-speaker contrast is statistically indistinguishable from zero (Figure 4), and pooling the four models leaves −0.5 ARS and +1.5 APR points, both within sampling error. Speaker count is not the primary bottleneck."

## 5.3 SNR Ablation
> "To test whether audio models can recover task-relevant background speech amid competing foreground speech, and whether they admit failure rather than fabricate the missing information, we remix the 96 English background speech retrieval cases at seven fixed background-to-foreground SNRs from +8 to −8 dB, holding the underlying audio takes constant across levels in a take-paired design; three hired Prolific workers (Palan and Schitter 2018) performed the same task."

> "Figure 5 reveals two patterns. First, recovery degrades sharply as the background speech becomes quieter for both humans and models, but models remain far from human level: Gemini 3.1 Pro, the strongest configuration on capture, falls from 62.5% at +8 dB to 15.6% at −8 dB, whereas the human average falls from 98.5% to 15.5%. Second, models differ in whether they acknowledge the miss. GPT Realtime 2.1 admits 42–56% of its misses at every level, with no clear dependence on overlay difficulty, whereas Gemini 3.1 Pro admits 44.4% at +8 dB but only 6.2% at −8 dB, and GPT Audio 1.5 declines similarly, from 23.3% to 10.5%, within per-level sampling error. For these two models the errors compound: as the speech gets harder to recover, they miss more often and admit less, leaving more unsupported answers"

| Model | Capture +8 dB | Capture −8 dB | Admit rate +8 dB | Admit rate −8 dB |
|---|---|---|---|---|
| Gemini 3.1 Pro (strongest on capture) | 62.5% | 15.6% | 44.4% | 6.2% |
| Human average | 98.5% | 15.5% | — | — |
| GPT Realtime 2.1 | — | — | 42–56% at every level, no clear dependence on overlay difficulty | 42–56% at every level |
| GPT Audio 1.5 | — | — | 23.3% | 10.5% |

> "Figure 5: Overlay-SNR ablation on background speech retrieval. (a) Rate of capturing the background detail. (b) Rate of admitting not hearing instead of fabricating, over each level's missed cases. Bands: Wilson 95% intervals."

> "Appendix C reports the full behavior composition per SNR level."

Appendix C behavior-composition table/figure body is not legible in this chunk beyond the header fragment ("Statistic English Mandarin Total", "Base testcases 576 576 1,152", "Behavior settings 8", "Patterns 6", "Fabrication / silent", "Foreground decoy").

## 5.4 Human Study
> "To validate the LLM judge, we collected human labels on Prolific for 216 judged responses, stratified over all patterns and scenes from five configurations, each scored against 2–4 atomic rubrics (472 in total). Annotators saw the judge's textual evidence and labeled every rubric pass/fail, with two-fold redundancy, embedded attention checks. After excluding four submissions (two failed attention checks, two incomplete), 11 annotators contributed 869 labels covering 458 of the 472 rubrics, 340 with at least two independent labels. The judge agrees with humans on 82.6% of judgments (Table 2; Cohen's κ = 0.63, 95% CI [0.57, 0.69]; Gwet's AC1 = 0.67) while being marginally stricter (60.2% vs. 61.9% pass), and exceeds inter-annotator agreement (κ = 0.56, 79.3%): statistically indistinguishable from an additional annotator."

## 6 Limitations
> "The benchmark uses synthesized, scripted speech; it should be expanded with more languages, accents, spontaneous speech, and human recordings. The two bystander-speech metrics rest on negative cases only: every injected utterance is irrelevant to the assistant's task, so they measure restraint but not selective engagement; future versions will add pattern-specific positive cases in which the interjection genuinely changes the task."

## 7 Conclusion
> "MSI-Bench reframes voice-agent evaluation around the next interaction regime—AI as a shared collaborative entity among multiple humans—testing whether a model can preserve speaker-scoped memory, follow disclosure and authority constraints, and reason over interleaved group constraints. Across 12 models and 15 configurations, no system is reliable: the strongest configuration on each split passes all rubrics on only 66.8% of English and 54.5% of Mandarin cases (strongest open-weight: 34.0% and 19.3%), and multi-speaker memory is the weakest capability family."

> "Our analyses locate two distinct bottlenecks: open-weight models fail chiefly at perceiving who said what—speaker-labeled transcripts lift the Gemma and MiMo configurations by 21–44 APR points—whereas frontier models gain little from transcripts and their residual errors are reasoning failures that persist on clean text."

> "Restraint is a third, largely independent axis: models that answer well still speak when no one has addressed them, and as background speech becomes harder to hear, several models miss more task facts while admitting fewer misses."

> "Progress toward collaborative voice agents therefore requires speaker-grounded audio perception, speaker-scoped decision making, and knowing when not to speak—the capabilities MSI-Bench measures directly."

## Disclosure
> "Generative AI Use Disclosure: The authors used Claude for code completion, debugging, and refactoring; all AI-assisted code was reviewed and validated by the authors, who take full responsibility for the reported results."

**Covers:** Silence-as-consent fragment and constrained-decoding check; speaker-count three- vs two-speaker result (Figure 4 text); Section 5.3 SNR Ablation with Figure 5 and Appendix C pointer; Section 5.4 Human Study; Section 6 Limitations; Section 7 Conclusion; Generative AI Use Disclosure
