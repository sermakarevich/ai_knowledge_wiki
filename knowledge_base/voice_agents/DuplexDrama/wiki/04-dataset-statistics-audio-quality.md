> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Dataset Statistics and Audio Quality
**In one sentence:** The chunk presents the released-corpus overview (Table 1), full-duplex behavior-tag distribution (Table 2), environment/event tag distributions (Fig. 4, Fig. 5), per-dialogue objective audio metrics (Table 3), and a prior-corpora comparison (Table 5).
## Key points
- The chunk references an overview table (Table 1), a full-duplex behavior-tag table (Table 2), and two bar charts for environment background and sound-event tag distributions (Fig. 4, Fig. 5).
- Fig. 4 shows the distribution of environment background tags across seven scene categories; Fig. 5 shows top-10 sound-event tags across five macro-classes, sorted descending by share (12.44%, 8.92%, 8.48%, 8.10%, 6.26%, 5.20%, 4.68%, 4.67%, 4.37%, 4.22%), though tag labels are garbled in the chunk.
- UTMOSv2 and NISQA are predicted on both clean TTS audio and mixed (with background) audio as comparison, since speech quality "should not be affected by additive background noise."
- Table 3 reports per-dialogue scores with a middle column flagging clean (✗), mixed (✓), or both: WER 1.8%, SpkCons 97.3%, UTMOSv2 2.57 / 2.52, NISQA-MOS 3.65 / 3.18.
- Mixing background costs UTMOSv2 only 0.05 but NISQA-MOS 0.47, because UTMOSv2 "targets the naturalness of synthetic speech while NISQA also penalises additive noise" and "the speech itself is therefore left intact."
- Lower-than-typical UTMOSv2 scores are attributed "primarily to the diverse persona stylings and emotion injection in our synthesized audio."
- Table 5 compares six corpora on duration, type, persona+scenario, full-duplex status, and sound events: Ours (800 hr, synth., ✓/✓/✓) is stated as "the only corpus that jointly covers all four annotation dimensions, with the script-aware sound event tags being unique to our work."
---
## Overview tables and tag distributions
**Covers:** chunk secs: overview table (Table 1), full-duplex behavior-tag table (Table 2), Fig. 4–Fig. 5

The chunk states the release includes an "overview table (Table 1), a full-duplex behavior-tag table (Table 2), and two bar charts depicting the distributions of environment background and sound-event tags (Fig. 4, Fig. 5)."

- Fig. 4 caption (verbatim): "Distribution of environment background tags across the seven scene categories."
- Fig. 5 caption (verbatim): "Top-10 sound-event tags across five macro-classes, sorted descending by share."
- Fig. 5 bar values visible in chunk, descending: 12.44%, 8.92%, 8.48%, 8.10%, 6.26%, 5.20%, 4.68%, 4.67%, 4.37%, 4.22%.
- Tag labels in Fig. 4 / Fig. 5 are garbled by OCR in the chunk (fragments such as "obje ct", "push", "shuffle", "paper", "vibration", "motor", "door", "knock", etc. are not reliably reconstructible), so exact label-to-share mapping is not stated here.
- Table 1 and Table 2 cell values are not legible in the chunk beyond their titles.

## Objective audio-side metrics (Table 3)
**Covers:** chunk secs: UTMOSv2 / NISQA clean-vs-mixed comparison; Table 3

Verbatim mechanism statements:

- "and should not be affected by additive background noise."
- "UTMOSv2 and NISQA are predicted on both the clean TTS audio and the mixed (with background) audio as comparison."
- "Table 3 reports the per-dialogue scores; the middle column flags whether each metric is evaluated on clean, mixed, or both audio."
- "As expected, mixing the background costs UTMOSv2 only 0.05 but NISQA-MOS 0.47, since UTMOSv2 targets the naturalness of synthetic speech while NISQA also penalises additive noise; the speech itself is therefore left intact."
- "We attribute the lower-than-typical UTMOSv2 scores primarily to the diverse persona stylings and emotion injection in our synthesized audio."

Table 3. Per-dialogue audio-side objective metrics (verbatim caption: "WER / SpkCons / UTMOSv2 / NISQA. Middle column: ✗ clean speech, ✓ mixed audio."):

| Metric | w. bg | Value |
|---|---|---|
| WER | ✗ | 1.8% |
| SpkCons | ✗ | 97.3% |
| UTMOSv2 | ✗/✓ | 2.57 / 2.52 |
| NISQA — MOS | ✗/✓ | 3.65 / 3.18 |

## Comparison with prior corpora (Table 5)
**Covers:** chunk secs: Table 5 and surrounding comparison prose

Table 5 caption (verbatim): "Comparison with prior corpora: Dur. (hr) total audio duration in hours; Type (natural / synthesized); ① persona + scenario; ② full-duplex status; ③ sound event. SDF abbreviates SpeechDialogueFactory. Legend: ✗ absent, ✓ present."

| Dataset | Dur. (hr) | Type | ① | ② | ③ |
|---|---|---|---|---|---|
| Fisher [6] | 2,000 | natural | ✗ | ✗ | ✗ |
| CANDOR [7] | 850 | natural | ✗ | ✗ | ✗ |
| Open-Yap-1K [9] | 1,000 | natural | ✗ | ✗ | ✗ |
| DuplexConv [8] | 2,000 | natural | ✗ | ✓ | ✓ |
| SDF [4] | 146 | synth. | ✓ | ✗ | ✗ |
| Ours | 800 | synth. | ✓ | ✓ | ✓ |

Verbatim comparison claims in chunk:

- "sational speech as acoustic baselines but ship without any of our four annotation dimensions." (sentence start truncated in chunk)
- "Open-Yap-1K [9] and DuplexConv [8] ship large-scale natural conversational recordings with speaker overlap, yet both lack scripted scenarios, persona attributes, and sound-event annotations."
- "SpeechDialogueFactory [4] is a synthesized corpus that provides persona and scenario annotations but does not cover full-duplex scenarios."
- "Our proposed DuplexDrama is the only corpus that jointly covers all four annotation dimensions, with the script-aware sound event tags being unique to our work."

**Covers:** Released corpus stats, behavior/environment/event distributions, and objective audio metrics (chunk 04-overview-table-table-1-a-full-duplex; Table 1–Table 3, Table 5, Fig. 4–Fig. 5 as legible through garbled OCR).
