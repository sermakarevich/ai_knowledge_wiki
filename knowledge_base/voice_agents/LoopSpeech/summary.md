# Technical Analysis: FreedomIntelligence/LoopSpeech

**Repository:** https://github.com/FreedomIntelligence/LoopSpeech
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Full-duplex speech models listen and speak simultaneously, enabling interruptions and backchannels, but text generation, speech synthesis, and audio playback run asynchronously: a model may have generated content the user has not actually heard (README.md:21). This creates an anchoring gap between what the model believes it has said and what was really played to the user (README.md:23). The gap breaks interruption queries — "What did you just say?", "Repeat the last item.", "Where did you stop?", "Continue from there." (README.md:25-28) — because the model answers from internally generated text rather than realized audio.

LoopSpeech introduces Self-Listening, a playback-grounded approach that lets a full-duplex model track its own realized speech and recover consistently after interruptions (README.md:30). Only waveform already reaching user-side playback is fed back through the model's speech-input pathway, giving a causal record of what the user actually heard without delaying generation or playback (README.md:43, README.md:46). The paper also introduces AnchorSpeech, a time-aligned collection for training and evaluating anchoring-sensitive interruptions, whose test split measures consistency with the last completed played item (README.md:52, README.md:54).

Primary user: researchers and engineers building full-duplex voice agents who need post-interruption responses anchored to actually played speech. Repository status is Preprint with code, models, data, and paper link still to be added (README.md:9, README.md:11).

## 2. High-Level Architecture

```
  user microphone                    playback monitor
        │                                    │
        ▼                                    ▼
 ┌──────────────┐  ┌──────────────────┐  ┌───────────────┐
 │ User speech  │  │ Played model     │  │ Model text +  │
 │ (incoming    │  │ speech (only     │  │ control tokens│
 │  audio)      │  │ waveform already │  │ (response +   │
 │              │  │ reaching user)   │  │ overlap/stop/ │
 └──────┬───────┘  └────────┬─────────┘  │ wait/silence) │
        │                   │            └───────┬───────┘
        └─────────► 40 ms shared interleaved timeline ◄─┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Thinker branch (Qwen2.5-Omni-7B)│
              │ + frozen MOSS-TTS-Realtime      │
              │ streaming synthesizer           │
              └────────────────┬────────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
        generated text ─► synthesis ─► playback
        (async, ahead of user)         (feeds back
                                        only played
                                        portion)
```

Data-flow narrative:

1. The interaction is organized as three time-aligned streams — user speech, played model speech, and model text with control tokens — interleaved on a shared 40 ms timeline (README.md:40-46).
2. The Thinker branch of Qwen2.5-Omni-7B consumes user speech and the fed-back played speech through its speech-input pathway alongside model text tokens (README.md:46, README.md:48).
3. Generated response tokens drive a frozen MOSS-TTS-Realtime streaming synthesizer whose output goes to user-side playback asynchronously (README.md:48).
4. Only waveform that has already reached playback is returned as the played-model-speech channel, so the model holds a causal record of what the user heard without stalling generation or playback (README.md:43, README.md:46).
5. Native control tokens handle overlap, interruption stopping, backchannel continuation, waiting, and silence (README.md:48).
6. After an interruption, the response is conditioned on the last completed played item, which is what AnchorSpeech-test scores (README.md:54).

Persistent state: no database or on-disk state is documented. The only state attested in the source is the in-context causal record of played speech carried on the shared timeline plus the (unreleased) AnchorSpeech training/evaluation collection (README.md:46, README.md:52). Checkpoints, data, and eval scripts are roadmap items, all unchecked (README.md:102-106).

## 3. Self-Listening Three-Channel Timeline

Representation: an interaction is three time-aligned streams interleaved on a shared 40 ms timeline (README.md:40, README.md:46). Played model speech is defined restrictively as only the model waveform that has already reached user-side playback (README.md:43), fed back through the model's speech-input pathway (README.md:46). The stated purpose mirrors human speech self-monitoring: Self-Listening feeds the model speech already played to the user back into the listening pathway (README.md:17).

Named kinds/types with file:line:

- User speech — the incoming audio from the user (README.md:42)
- Played model speech — only waveform already reaching user-side playback (README.md:43)
- Model text — response tokens and full-duplex control tokens (README.md:44)
- Control tokens — native tokens for overlap handling, interruption stopping, backchannel continuation, waiting, and silence (README.md:48)
- AnchorSpeech-test item — a post-interruption case scored on consistency with the last completed played item rather than internally generated-only text (README.md:54)

Key queries: the evaluation query pattern is whether a model's response after an interruption is consistent with the last completed item that was actually played (README.md:54). Verbatim:

> "AnchorSpeech-test measures whether a model's response after an interruption is consistent with the last completed item that was actually played, rather than with text that may only have been generated internally" (README.md:54)

## 4. LLM / External Service Integration

Providers: Thinker branch of Qwen2.5-Omni-7B as the base model and a frozen MOSS-TTS-Realtime model for streaming synthesis (README.md:48). GPT-Realtime-2.1 appears only as an evaluated commercial baseline, not as a repo dependency (README.md:60-64).

Required vs optional calls: no API-call structure is documented because no inference or training code is released. Architecturally, the Thinker forward pass and the frozen synthesizer are required per generation step; no optional external calls are attested.

Env vars: none documented in the wiki source.

## 5. Playback-Grounded Interruption Recovery

Step by step (function-level file.py:line references are unavailable — no code files are released; steps below cite the README lines that specify each behavior):

1. Interleave the three streams — user speech (README.md:42), played model speech (README.md:43), model text with control tokens (README.md:44) — on the shared 40 ms timeline (README.md:46).
2. Detect overlap and interruption with native control tokens covering overlap handling and interruption stopping (README.md:48).
3. Stop playback on interruption; the played-speech channel retains exactly what reached the user, since it contains only waveform already at user-side playback (README.md:43).
4. Condition the recovery response on the causal played-speech record supplied through the speech-input pathway without delaying generation or playback (README.md:46).
5. Emit continuation behavior — backchannel continuation, waiting, or silence — via control tokens (README.md:48).
6. Answer anchoring queries ("What did you just say?", "Repeat the last item.", "Where did you stop?", "Continue from there.", README.md:25-28) against the last completed played item, as scored by AnchorSpeech-test (README.md:54).

Reported outcome on AnchorSpeech-test: three-channel Self-Listening 73.0% anchoring accuracy at 0.434 s stop / 0.564 s response latency, versus matched two-channel 7.8% at 0.425 s / 0.567 s and GPT-Realtime-2.1 43.8% at 0.296 s / 1.548 s (README.md:60-64). Gains: 65.2 points over the matched two-channel model and 29.2 points over GPT-Realtime-2.1 (README.md:66-69). The source attributes the gain to playback-grounded context rather than a slower interruption strategy given the nearly unchanged latencies in the controlled comparison (README.md:71). Full-Duplex-Bench v1.5 shows sub-second response latency in interruption and backchannel scenarios with a trade-off between anchoring and conventional turn-management performance (README.md:73).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| README.md | 9-11 | Declares preprint status; code, models, data, paper link pending |
| README.md | 17 | Figure caption: self-monitoring analogy for playback feedback |
| README.md | 21-28 | Defines the anchoring gap and the four motivating interruption queries |
| README.md | 30 | States the Self-Listening fix |
| README.md | 38-46 | Specifies the three-channel 40 ms interleaved architecture |
| README.md | 48 | Names the base stack (Qwen2.5-Omni-7B Thinker, frozen MOSS-TTS-Realtime) and control-token set |
| README.md | 52-54 | Defines the AnchorSpeech collection and test metric |
| README.md | 58-71 | Reports AnchorSpeech-test results table, gains, latency interpretation |
| README.md | 73 | Reports Full-Duplex-Bench v1.5 latency and anchoring/turn-management trade-off |
| README.md | 77-83 | Lists authors, affiliations, equal-contribution and corresponding marks |
| README.md | 89-96 | Gives the `zhou2026loopspeech` citation entry |
| README.md | 102-106 | Roadmap checklist (paper, code, checkpoints, data/eval, demos), all unchecked |
| README.md | 110 | Contact route: open a repo issue |
| README.md | 112-114 | Notes no component directories (code not yet present) |
| assets/self-listening-overview.png | — | Referenced figure asset (content not transcribed in source) |
| assets/self-listening-architecture.png | — | Referenced figure asset (content not transcribed in source) |

Only the files above are attested in the wiki source. No training, inference, evaluation, or configuration files are documented; the chunk's macro-components section reports no component directories (README.md:112-114).

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| Qwen2.5-Omni-7B (Thinker branch) | unknown (no constraint string in source) | Base full-duplex model stack (README.md:48) |
| MOSS-TTS-Realtime (frozen) | unknown (no constraint string in source) | Streaming speech synthesis (README.md:48) |
| AnchorSpeech data and evaluation scripts | unknown (unreleased roadmap item) | Anchoring training and test metric (README.md:52-54, README.md:102-106) |
| Full-Duplex-Bench v1.5 | unknown (version label only, no constraint string) | Secondary latency / turn-management evaluation (README.md:73) |

No `requirements.txt`, `pyproject.toml`, or manifest constraint strings are attested in the wiki source. Required-first ordering above reflects architectural necessity; all entries lack exact pins because the code is unreleased (README.md:11, README.md:102-106).

## 8. CLI / Usage Surface

Entry points: none documented. Inference and training code, model checkpoints, AnchorSpeech data and evaluation scripts, and reproducible examples/demos are all unchecked roadmap items (README.md:102-106).

Commands: none documented.

| Env var | Required? | Purpose |
|---|---|---|
| — | — | No environment variables documented in source |

| Config | Purpose |
|---|---|
| Native control tokens (overlap, interruption stopping, backchannel continuation, waiting, silence) | Full-duplex turn behavior, token-level (README.md:48) |
| 40 ms interleave timeline | Time alignment of the three streams (README.md:46) |

## 9. Extensibility Points

No code is released, so the points below are projected from the documented architecture; file/class targets cannot be named beyond the README:

- Played-speech feedback tap — to change what counts as "played" (e.g., device-acknowledged vs. rendered audio), modify the producer of the played-model-speech channel defined as only waveform already reaching user-side playback (README.md:43).
- Timeline resolution — to change the 40 ms interleave grid, modify the stream-interleaving logic (README.md:46).
- Control-token policy — to add or retune overlap, stopping, backchannel-continuation, waiting, or silence behaviors, extend the native control-token set (README.md:48).
- Synthesizer swap — to replace streaming synthesis, substitute the frozen MOSS-TTS-Realtime component (README.md:48).
- Base-model swap — to port Self-Listening to another full-duplex backbone, replace the Qwen2.5-Omni-7B Thinker branch (README.md:48).
- Metric extension — to score new interruption types, extend AnchorSpeech-test beyond consistency with the last completed played item (README.md:54).

## 10. Limitations and Gotchas

- **No released artifacts — nothing here is executable.** Code, checkpoints, AnchorSpeech data, eval scripts, demos, and the paper link are all unchecked roadmap items under a preprint status banner (README.md:11, README.md:102-106). Any integration plan must treat this repo as a specification plus results, not a usable library.
- **Anchoring trades against conventional turn-management.** Full-Duplex-Bench v1.5 results reveal a trade-off between anchoring and conventional turn-management performance even as interruption/backchannel response stays sub-second (README.md:73). Optimizing for post-interruption consistency can cost standard turn-taking behavior.
- **Evaluation is narrow and self-defined.** The headline 73.0% rests on AnchorSpeech-test, a new collection introduced by the same authors that scores consistency with the last completed played item (README.md:52-54, README.md:60-64). External validity beyond that metric and Full-Duplex-Bench v1.5 is not established in the source.
- **Latency comparison flatters the baseline on one axis.** GPT-Realtime-2.1 stops faster (0.296 s vs 0.434 s) while responding slower (1.548 s vs 0.564 s); the "nearly unchanged latency" claim covers only the controlled two-channel/three-channel comparison (README.md:60-71). Deployment sizing cannot assume Pareto dominance on stop latency.
- **Control-token and feedback-tap semantics are unspecified.** The token set (overlap, stopping, backchannel continuation, waiting, silence) and the "already reached playback" boundary are named but not specified as code or protocol (README.md:43, README.md:48), so reimplementation risks divergence on exactly the anchoring behavior being measured.

## 11. How It Compares to Alternatives

- OpenAI GPT-Realtime-2.1 (Realtime API family): strongest evaluated commercial baseline in the source at 43.8% anchoring accuracy with 0.296 s stop / 1.548 s response latency, 29.2 points below Self-Listening on AnchorSpeech-test (README.md:60-69).
- Matched two-channel full-duplex ablation: same stack minus the played-speech channel, scoring 7.8% at 0.425 s / 0.567 s; the 65.2-point gap isolates the contribution of the playback-feedback channel (README.md:60-71).
- Qwen2.5-Omni-7B (base backbone): general omni-modal full-duplex starting point reused here as the Thinker branch; LoopSpeech adds the third channel and control-token policy rather than a new backbone (README.md:48).
- Kyutai Moshi / Mini-Omni / Freeze-Omni class full-duplex models: representative open full-duplex systems with interruption and overlap handling but, per the problem framing, no playback-grounded self-listening channel tying recovery to realized audio (README.md:21-30, README.md:40-48).

Positioning: LoopSpeech is not another full-duplex backbone; it is a playback-grounding modification — a third actually-played audio channel on a shared timeline — aimed specifically at post-interruption consistency, at a measured cost to conventional turn-management scores.

## Appendix: Selected Code Snippets

No code files are released, so the snippets below are verbatim source statements with file and line ranges.

1. Anchoring gap definition (README.md:21-23):

> "text generation, speech synthesis, and audio playback run asynchronously: a model may have generated content that the user has not actually heard" … "an **anchoring gap** between what the model believes it has said and what was really played to the user"

2. Three-channel specification (README.md:40-48):

> "organizes an interaction as three time-aligned streams" … "**User speech** - the incoming audio from the user" … "**Played model speech** - only the model waveform that has already reached user-side playback" … "**Model text** - response tokens and full-duplex control tokens" … "The streams are interleaved on a shared 40 ms timeline" … "Played model speech is fed back through the model's speech-input pathway, giving the model a causal record of what the user has actually heard without delaying generation or playback" … "built on the Thinker branch of **Qwen2.5-Omni-7B**" … "a frozen **MOSS-TTS-Realtime** model for streaming synthesis" … "Native control tokens support overlap handling, interruption stopping, backchannel continuation, waiting, and silence"

3. Results and interpretation (README.md:66-73):

> "**65.2 percentage points** over the matched two-channel model." … "**29.2 percentage points** over GPT-Realtime-2.1, the strongest evaluated commercial baseline." … "The nearly unchanged stopping and response latencies in the controlled two-channel/three-channel comparison indicate that the improvement comes from playback-grounded context rather than a slower interruption strategy" … "Experiments on Full-Duplex-Bench v1.5 further show sub-second response latency in interruption and backchannel scenarios, while revealing a trade-off between anchoring and conventional turn-management performance"
