> [[index|Wiki]] | [[summary|Summary]]

# ECHO: A Matched-Contrast Benchmark for Context-Sensitive Turn-Taking in Full-Duplex Dialogue — Digest

## 1. [[wiki/01-matched-contrast-benchmark-overview|ECHO: A Matched-Contrast Benchmark for Context-Sensitive Turn-Taking in Full-Duplex Dialogue]]

**In one sentence:** The source chunk for this page is truncated/garbled and contains only the paper title, author list, affiliation, and the start of the abstract, so no substantive claims can be extracted.

## Key points
- The chunk contains only the title "ECHO: A MATCHED-CONTRAST BENCHMARK FOR CONTEXT-SENSITIVE TURN-TAKING IN FULL-DUPLEX DIALOGUE" and no body claims.
- The chunk lists authors Shuofeng Zhao, Hongwei Cai, Wenke Fan, Qingxiang Guo, Dawei Yang, Zhou Wang, Zhiyang Zhou, Yingxin Shang, Weixu Wang, Lin Yang, Shuran Zhou, and Yang Song.
- The chunk lists the affiliation as Zuoyebang Education Technology, Beijing, China.
- The chunk contains only the heading "ABSTRACT" plus the fragment "semantic evidence for turn management [8, 9, 10, 11], alongside" with no complete sentence.
- No methods, numbers, mechanisms, results, tables, or verbatim complete quotes are present in the chunk, so none are reproduced here to avoid invention.

## 2. [[wiki/02-background-roles-contrast-generation|Background, Interaction Roles, and Contrast Generation]]

**In one sentence:** ECHO tests whether a full-duplex system can output YIELD versus KEEP for the exact same overlapping utterance when only the preceding multi-turn dialogue context is rewritten to change its interactional role.

## Key points
- Full-duplex systems must decide between YIELD (user claims the floor) and KEEP (backchannel, self-talk, or third-party speech that permits continued speaking), not merely detect overlapping speech.
- Existing benchmarks evaluate independently occurring events where insertion text and preceding dialogue vary together, so they can reward a fixed action preference rather than context-sensitive decisions.
- Non-interruptive sampling in prior work is lexically closed: in SID-Bench [7] 81.8% of non-interruptive instances consist entirely of the fifteen most frequent characters, and in Easy Turn [17] backchannel and turn-taking vocabularies are disjoint.
- ECHO is a paired Chinese multi-turn diagnostic benchmark that holds the overlap transcript lexically fixed while contrasting the preceding dialogue context, with one member requiring YIELD and the other KEEP, plus off-talk examples for diagnosing unnecessary yielding.
- It introduces pair accuracy, which requires correct decisions on both members of a pair and assigns no credit to constant-action policies.
- Construction uses an insertion-text-matched contrastive design inspired by minimal-pair testing: Claude-3.5-Sonnet [21] rewrites the history under role definitions, DeepSeek-V4-Pro screens for consistency, then manual review discards incompatible examples.
- Retained instances achieve 97.45% human-evaluation accuracy, confirming rewritten contexts induce the intended roles; experiments previewed here find three of four speech systems yield to most backchannels despite substantial interruption response, a Yield bias concealed by interruption-only accuracy.

## 3. [[wiki/03-speech-synthesis-overlap-rendering|Speech Synthesis and Overlap Rendering]]

**In one sentence:** All turns are independently synthesized with IndexTTS2 and rendered as speaker-separated dual-channel audio with role-dependent overlap handling, holding insertion text and selected synthesis conditions fixed within each linked group so that only context and interactional role change.

## Key points
- All dialogue turns are independently synthesized with IndexTTS2 [22] and rendered as speaker-separated dual-channel audio.
- The same synthesis and post-processing pipeline is applied to all examples, including speaker-prompt RMS normalization, bounded speaking-rate normalization, forced-alignment-based overlap placement, and role-dependent overlap rendering.
- Within each linked group, the insertion text, emotion condition, and TTS inference configuration are held fixed, while the preceding multi-turn context and the intended interaction role are changed.
- Backchannel and off-talk speech are overlaid without modifying the assistant track, whereas an interruption receives onset emphasis and causes the assistant track to fade to silence after a short reaction interval.
- Speaker-reference audio may differ across paired instances and all utterances are synthesized independently, so paired insertions are controlled in lexical and selected synthesis conditions but are not waveform-identical or fully acoustically matched.
- The faded assistant waveform is excluded from evaluated model inputs, so post-decision floor release cannot serve as a label cue.
- The Fig. 1 example shares one insertion transcript, glossed "This pen has run out of ink again", placed at the annotated overlap position located by forced alignment, with the rewrite changing the role from backchannel to interruption to off-talk and the target action from KEEP to YIELD to KEEP, making lexical form uninformative.

## 4. [[wiki/04-experiments-pair-metrics-findings|Experiments, pair-level metrics, findings, conclusion and limitations]]

**In one sentence:** Three of four evaluated speech systems show a Yield bias that single-number interruption accuracy conceals, and the bias is not explained by limited context but by how floor decisions use available context, as exposed by pair-level metrics.

## Key points
- Lychee-FD receives up to five preceding dialogue turns plus the complete planned assistant utterance yet keeps the floor on only 12.02% of backchannels and 8.20% of off-talk, with 4.00% PASRI−B.
- The text-conditioned reference observing the same dialogue but only the already-spoken assistant prefix reaches 86.34% on backchannels.
- Among speech systems, only MiniCPM-o 4.5 is balanced (63.39%/65.57%, 54.00% PASRI−B).
- In the three-way role space, the text-conditioned reference reaches 82.33% macro accuracy but only 66.00% PRSR; in the binary space, 82.88% overall accuracy corresponds to 52.00% PASRI−O.
- The text-conditioned reference recovers the intended role for 82.33% of instances from the same observable context, bounding the share of the gap attributable to residual label ambiguity, while Yield-biased systems reach at most 35.70% overall accuracy.
- The authors conclude ECHO is a paired diagnostic set for Chinese full-duplex turn-taking holding the inserted utterance lexically fixed while rewriting preceding dialogue, and that class-conditioned Keep rates alongside interruption accuracy are necessary for meaningful evaluation.
- ECHO must not be interpreted as estimates under naturally occurring event prevalence; it is a paired diagnostic set whose synthesis enables one insertion to recur across rewritten histories at the cost of ecological validity of real-speech benchmarks [7].

## The argument in five moves

1. Full-duplex dialogue requires a context-sensitive YIELD-versus-KEEP decision on overlapping speech, since the same utterance (e.g., "This pen has run out of ink again") can be a backchannel, an interruption, or off-talk depending on the preceding dialogue.
2. Existing benchmarks test independently occurring events with lexically closed non-interruptive classes, so they let systems score well via a constant action preference rather than genuine context use.
3. ECHO answers with a paired Chinese multi-turn diagnostic that holds the insertion text fixed while rewriting the context to flip the interactional role, validated at 97.45% human accuracy, plus pair-accuracy metrics that give no credit to constant-action policies.
4. Controlled IndexTTS2 synthesis with speaker-separated dual-channel rendering and role-dependent overlap handling isolates the context manipulation, keeping lexical and selected synthesis conditions fixed within each linked group.
5. Under this protocol three of four speech systems show a pronounced Yield bias (e.g., Lychee-FD keeps only 12.02% of backchannels despite full context, versus 86.34% for a text reference seeing less), and pair-level metrics expose gaps that sample-level accuracy hides.
6. The bias therefore reflects how floor decisions use available context rather than how much context is available, so class-conditioned Keep rates must accompany interruption accuracy — with the caveat that ECHO is a synthetic paired diagnostic, not an estimate under natural event prevalence.
