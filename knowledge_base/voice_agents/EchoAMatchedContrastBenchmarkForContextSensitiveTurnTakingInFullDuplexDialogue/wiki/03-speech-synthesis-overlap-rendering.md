> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Speech Synthesis and Overlap Rendering
**In one sentence:** All turns are independently synthesized with IndexTTS2 and rendered as speaker-separated dual-channel audio with role-dependent overlap handling, holding insertion text and selected synthesis conditions fixed within each linked group so that only context and interactional role change.
## Key points
- All dialogue turns are independently synthesized with IndexTTS2 [22] and rendered as speaker-separated dual-channel audio.
- The same synthesis and post-processing pipeline is applied to all examples, including speaker-prompt RMS normalization, bounded speaking-rate normalization, forced-alignment-based overlap placement, and role-dependent overlap rendering.
- Within each linked group, the insertion text, emotion condition, and TTS inference configuration are held fixed, while the preceding multi-turn context and the intended interaction role are changed.
- Backchannel and off-talk speech are overlaid without modifying the assistant track, whereas an interruption receives onset emphasis and causes the assistant track to fade to silence after a short reaction interval.
- Speaker-reference audio may differ across paired instances and all utterances are synthesized independently, so paired insertions are controlled in lexical and selected synthesis conditions but are not waveform-identical or fully acoustically matched.
- The faded assistant waveform is excluded from evaluated model inputs, so post-decision floor release cannot serve as a label cue.
- The Fig. 1 example shares one insertion transcript, glossed "This pen has run out of ink again", placed at the annotated overlap position located by forced alignment, with the rewrite changing the role from backchannel to interruption to off-talk and the target action from KEEP to YIELD to KEEP, making lexical form uninformative.
---
## Synthesis pipeline
All dialogue turns are independently synthesized with IndexTTS2 [22] and rendered as speaker-separated dual-channel audio. The chunk states:

> "We apply the same synthesis and post-processing pipeline to all examples, including speaker-prompt RMS normalization, bounded speaking-rate normalization, forced-alignment-based overlap placement, and role-dependent overlap rendering."

**Covers:** Sec. 2.3, synthesis pipeline
## Within-group controls
Within each linked group, the insertion text, emotion condition, and TTS inference configuration are held fixed, while the preceding multi-turn context and the intended interaction role are changed. Speaker-reference audio may differ across paired instances, and all utterances are synthesized independently; the chunk states paired insertions are "therefore controlled in lexical and selected synthesis conditions, but are not waveform-identical or fully acoustically matched."

**Covers:** Sec. 2.3, within-group fixed vs. changed conditions
## Role-dependent overlap rendering
The role determines the rendered interaction: backchannel and off-talk speech is overlaid without modifying the assistant track, whereas an interruption receives onset emphasis and causes the assistant track to fade to silence after a short reaction interval. The faded assistant waveform is excluded from evaluated model inputs, so post-decision floor release cannot serve as a label cue.

**Covers:** Sec. 2.3, overlap rendering and input exclusion rule
## Matched-contrast illustration (Fig. 1)
From the chunk's Fig. 1 caption/text: "One insertion, three required actions. All three ECHO branches share the same user insertion transcript, glossed 'This pen has run out of ink again'. In each branch, the insertion is placed at the annotated overlap position located by forced alignment, while the preceding multi-turn dialogue context is rewritten. The rewrite changes the interactional role from backchannel to interruption to off-talk, and with it the target action from KEEP to YIELD to KEEP." The chunk adds: "Lexical form is therefore uninformative, and a system must decide before the assistant track terminates."

**Covers:** Sec. 2.3 / Fig. 1
