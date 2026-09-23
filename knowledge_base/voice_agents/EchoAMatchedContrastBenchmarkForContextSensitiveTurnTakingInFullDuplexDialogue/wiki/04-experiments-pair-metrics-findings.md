> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Experiments, pair-level metrics, findings, conclusion and limitations
**In one sentence:** Three of four evaluated speech systems show a Yield bias that single-number interruption accuracy conceals, and the bias is not explained by limited context but by how floor decisions use available context, as exposed by pair-level metrics.
## Key points
- Lychee-FD receives up to five preceding dialogue turns plus the complete planned assistant utterance yet keeps the floor on only 12.02% of backchannels and 8.20% of off-talk, with 4.00% PASRI−B.
- The text-conditioned reference observing the same dialogue but only the already-spoken assistant prefix reaches 86.34% on backchannels.
- Among speech systems, only MiniCPM-o 4.5 is balanced (63.39%/65.57%, 54.00% PASRI−B).
- In the three-way role space, the text-conditioned reference reaches 82.33% macro accuracy but only 66.00% PRSR; in the binary space, 82.88% overall accuracy corresponds to 52.00% PASRI−O.
- The text-conditioned reference recovers the intended role for 82.33% of instances from the same observable context, bounding the share of the gap attributable to residual label ambiguity, while Yield-biased systems reach at most 35.70% overall accuracy.
- The authors conclude ECHO is a paired diagnostic set for Chinese full-duplex turn-taking holding the inserted utterance lexically fixed while rewriting preceding dialogue, and that class-conditioned Keep rates alongside interruption accuracy are necessary for meaningful evaluation.
- ECHO must not be interpreted as estimates under naturally occurring event prevalence; it is a paired diagnostic set whose synthesis enables one insertion to recur across rewritten histories at the cost of ecological validity of real-speech benchmarks [7].
---
## Finding 2: bias is not explained by limited context
Lychee-FD receives up to five preceding dialogue turns and the complete planned assistant utterance, and still keeps the floor on only 12.02% of backchannels and 8.20% of off-talk, with 4.00% PASRI−B.
The text-conditioned reference, which observes the same dialogue but only the assistant prefix already spoken, reaches 86.34% on backchannels.
The low off-talk rate is consistent with the difficulty on incidental side-talk reported in the original Lychee-FD study [13]; the comparably low backchannel rate shows that over-yielding extends to system-directed feedback that does not claim the floor.
Among the speech systems, MiniCPM-o 4.5 is the only balanced one (63.39%/65.57%, 54.00% PASRI−B).
Since the failing systems observe at least as much assistant-side context as the reference that succeeds, the limiting factor is how floor decisions use available context rather than how much context is available.
## Finding 3: pair-level metrics expose what sample-level accuracy hides
Evaluated in the original three-way role space (Table 4, last row), the text-conditioned reference reaches 82.33% macro accuracy but only 66.00% PRSR, so correct predictions on individual samples do not imply consistent predictions across linked context variants.
The same gap appears in the binary space, where 82.88% overall accuracy corresponds to 52.00% PASRI−O.
Label ambiguity affects all evaluated systems identically: the text-conditioned reference recovers the intended role for 82.33% of instances from the same observable context, which bounds the share of the observed gap that residual ambiguity can explain; the three systems exhibiting Yield bias reach at most 35.70% overall accuracy, far below that bound.
## Conclusion
> "We presented ECHO, a paired diagnostic set for Chinese full-duplex turn taking that holds the inserted utterance lexically fixed while rewriting the preceding dialogue, together with pair-level metrics that require correct actions on both members of a linked pair."
Under this protocol, three of the four evaluated speech systems show a pronounced action-level Yield bias that single-number interruption accuracy conceals.
Limited context does not explain the bias: Lychee-FD observes up to five preceding dialogue turns and the complete planned assistant utterance but maintains the floor on only 12.02% of backchannels, whereas a text-conditioned reference that sees strictly less assistant-side information reaches 86.34%.
The limiting factor is therefore how floor decisions use available context, not how much context is available.
Reporting class-conditioned Keep rates alongside interruption accuracy is necessary for meaningful turn-taking evaluation.
The authors state they release the ECHO audio, observable dialogue text, labels, and pair metadata.
## Limitations
- ECHO is a paired diagnostic set rather than an estimate of performance in naturally occurring dialogue: synthesis allows one insertion to recur across rewritten histories, at the cost of the ecological validity of real-speech benchmarks [7].
- Interruption waveforms receive label-dependent RMS scaling and onset emphasis; the design controls insertion text, emotion condition, and TTS inference configuration, but does not fully isolate dialogue context from speaker-reference variation or other acoustic factors. A waveform-reuse condition and a gain-free interruption ablation would be required for strict acoustic control.
- Off-talk is scenario-labeled and its intended addressee is not always explicit, so backchannel is treated as the primary evidence for Yield bias and off-talk as a supporting diagnostic.
- The evaluated systems differ in modality, streaming latency, and native output space, so results are a behavioral audit under supported interfaces rather than a modality-matched ranking.
- ECHO's balanced diagnostic distribution should not be interpreted as estimates under naturally occurring event prevalence.
**Covers:** plan.md chunk 04-describe-echo-s-balanced-diagnostic-distribution — Experiments, pair-level metrics (PASR/PKC), results (Findings 2–3), Conclusion (Sec. 4), Limitations, Acknowledgments/AI-use disclosure, References.
