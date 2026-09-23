---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: ECHO: A Matched-Contrast Benchmark for Context-Sensitive Turn-Taking in Full-Duplex Dialogue

### Q1. What substantive claims can be extracted from the opening chunk of the ECHO paper, and why is the answer "almost none"?

> [!tip]- Answer
> The opening chunk contains only the title, the author list (Shuofeng Zhao et al.), the Zuoyebang Education Technology affiliation, and an abstract fragment with no complete sentence. No methods, numbers, mechanisms, or results are present, so nothing beyond paper framing may be claimed from it without invention. See [[wiki/01-matched-contrast-benchmark-overview|ECHO: A Matched-Contrast Benchmark for Context-Sensitive Turn-Taking in Full-Duplex Dialogue]].

### Q2. What is the YIELD-versus-KEEP decision in full-duplex dialogue, and why is overlap detection alone insufficient?

> [!tip]- Answer
> YIELD means the user claims the floor and the assistant should stop, while KEEP means the overlap is a backchannel, self-talk, or third-party speech that permits continued speaking. The same utterance (e.g., "This pen has run out of ink again") can be an affiliative backchannel or a genuine interruption depending on preceding context, so lexical form alone does not determine the action. See [[wiki/02-background-roles-contrast-generation|Background, Interaction Roles, and Contrast Generation]].

### Q3. How does ECHO's matched-contrast construction work, and how was the quality of the rewritten contexts validated?

> [!tip]- Answer
> ECHO holds the insertion text fixed (ui^(a) = ui^(b)) while rewriting the preceding multi-turn context so the interactional role flips and the target labels differ (yi^(a) ≠ yi^(b)), with pair accuracy requiring correct decisions on both members. Claude-3.5-Sonnet rewrites the history under role definitions, DeepSeek-V4-Pro screens for consistency, manual review discards incompatible examples, and retained instances reach 97.45% human-evaluation accuracy. See [[wiki/02-background-roles-contrast-generation|Background, Interaction Roles, and Contrast Generation]].

### Q4. How are ECHO dialogues synthesized and rendered as audio, and what is held fixed within each linked group?

> [!tip]- Answer
> All turns are independently synthesized with IndexTTS2 and rendered as speaker-separated dual-channel audio with RMS normalization, bounded speaking-rate normalization, and forced-alignment-based overlap placement. Within each linked group the insertion text, emotion condition, and TTS inference configuration are fixed while the preceding context and intended role change. See [[wiki/03-speech-synthesis-overlap-rendering|Speech Synthesis and Overlap Rendering]].

### Q5. How does overlap rendering differ by role, and what control caveat applies to paired insertions?

> [!tip]- Answer
> Backchannel and off-talk speech are overlaid without modifying the assistant track, whereas an interruption gets onset emphasis and fades the assistant track to silence after a short reaction interval, with the faded waveform excluded from model inputs. Paired insertions are controlled in lexical and selected synthesis conditions but are not waveform-identical, since speaker-reference audio may differ and utterances are synthesized independently. See [[wiki/03-speech-synthesis-overlap-rendering|Speech Synthesis and Overlap Rendering]].

### Q6. What Yield bias did the experiments reveal, and why can it not be explained by limited context access?

> [!tip]- Answer
> Three of four speech systems yield to most backchannels despite responding to interruptions; Lychee-FD keeps the floor on only 12.02% of backchannels and 8.20% of off-talk (4.00% PASRI−B) despite seeing five prior turns plus the full planned assistant utterance. A text-conditioned reference seeing only the already-spoken assistant prefix reaches 86.34% on backchannels, so the limiting factor is how floor decisions use context, not how much is available. See [[wiki/04-experiments-pair-metrics-findings|Experiments, pair-level metrics, findings, conclusion and limitations]].

### Q7. Should a lab adopt ECHO's pair-accuracy protocol plus class-conditioned Keep rates as its standard turn-taking evaluation, displacing interruption-only accuracy?

> [!tip]- Answer
> Yes, adopt it as a diagnostic complement: pair metrics (52.00% PASRI−O versus 82.88% binary accuracy for the text reference) expose inconsistent context use that sample-level accuracy hides and give no credit to constant-action policies. Treat results as a synthetic paired diagnostic rather than natural-prevalence estimates, given TTS control limits, scenario-labeled off-talk, and modality-mismatched behavioral auditing. See [[wiki/04-experiments-pair-metrics-findings|Experiments, pair-level metrics, findings, conclusion and limitations]].
