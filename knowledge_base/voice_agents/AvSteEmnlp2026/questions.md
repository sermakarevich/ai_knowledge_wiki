---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: AV-STE: Audio-Visual Speech Token Enhancement

### Q1. What problem does AV-STE solve, and how does it fit into a Mimi-based dialogue stack?

> [!tip]- Answer
> Noisy speech corrupts Mimi semantic (cb0) tokens, which breaks downstream Mimi-based dialogue models like Moshi, so AV-STE recovers clean cb0 tokens at 12.5 Hz by fusing noisy audio with lip-ROI video through an entropy-gated cross-attention AV-HuBERT module. The enhanced tokens are a drop-in replacement that any Mimi-based TTS or codec LM consumes without architectural changes. See [[wiki/01-av-ste-audio-visual-speech-token-enhancement|AV-STE: Audio-Visual Speech Token Enhancement]].

### Q2. What is AV-STE's exact input/output contract?

> [!tip]- Answer
> The input is a noisy 16 kHz WAV plus a 96×96 grayscale mouth-ROI MP4 at 25 fps, and the output is an enhanced Mimi semantic (cb0) token sequence at 12.5 Hz. This fixed contract is what makes the enhanced tokens directly substitutable for noisy tokens in systems like Moshi. See [[wiki/01-av-ste-audio-visual-speech-token-enhancement|AV-STE: Audio-Visual Speech Token Enhancement]].

### Q3. Which checkpoint should you use for background noise versus same-corpus competing speakers?

> [!tip]- Answer
> Use `avste.pt` for clean speech, non-speech background noise, and cross-dataset speaker interference, and `avste_lrs3_interference.pt` for same-corpus-style competing speakers and out-of-domain video. Together they reproduce every semantic-token-accuracy row in the paper's main table. See [[wiki/01-av-ste-audio-visual-speech-token-enhancement|AV-STE: Audio-Visual Speech Token Enhancement]].

### Q4. What does the speech-noise −5 dB demo show, and what is its key limitation?

> [!tip]- Answer
> On the bundled clip, AV-STE reaches 79.3% token accuracy and 38.5% WER versus 27.6% and 61.5% for the noisy Mimi baseline, and Moshi generates a topical response ("try to stay in the city") instead of the baseline's generic reply. These four clips were picked for a clear before/after contrast, not as averages — the paper's Table 1 numbers are averaged over the full 1321-clip test set. See [[wiki/01-av-ste-audio-visual-speech-token-enhancement|AV-STE: Audio-Visual Speech Token Enhancement]].

### Q5. What is the silent failure mode when running inference on your own audio with `compare_demo.py`?

> [!tip]- Answer
> The flags `--pred_json`, `--utt_id`, `--clean`, and `--noisy` must all be passed together; omitting any one makes `compare_demo.py` silently fall back to the bundled demo clips instead of your audio. The full custom-audio path is lip-ROI extraction with `scripts/prepare_lip_roi.py` plus the dlib landmark model, ffmpeg resampling to 16 kHz mono, `scripts/infer_avste.py`, then the comparison script. See [[wiki/01-av-ste-audio-visual-speech-token-enhancement|AV-STE: Audio-Visual Speech Token Enhancement]].

### Q6. How are the two checkpoints trained, and how is enhancement quality measured?

> [!tip]- Answer
> Both are `av_hubert_crossattn_ent` models with 4-frame lookahead fine-tuned from `large_vox_iter5.pt` under config `configs/large_lrs3_433h_crossattn_ent.yaml` on a 20/40/40 clean/non-speech/speaker-interference mix with SNR uniform in [-10, 10] dB; Stage 1 (`avste.pt`, peak LR 1e-4, AudioSet interference) seeds Stage 2 (`avste_lrs3_interference.pt`, peak LR 3e-5, 1–4 LRS3 interfering speakers). The primary metric is semantic-token accuracy against clean-audio tokens, with Whisper-large-v3 WER on Mimi-decoded audio as a secondary diagnostic over the 1321-clip noisy_test split. See [[wiki/01-av-ste-audio-visual-speech-token-enhancement|AV-STE: Audio-Visual Speech Token Enhancement]].

### Q7. A team building a noisy-environment kiosk on a Mimi-based dialogue model asks whether to adopt AV-STE — what do you recommend?

> [!tip]- Answer
> Recommend adopting AV-STE as a token-level front end if the kiosk has a camera for lip-ROI video and the noise matches a released checkpoint regime, since the demo shows large token-accuracy and topical-response gains with no downstream architecture changes. Condition the recommendation on validating against the full 1321-clip protocol rather than the four showcase clips, and on holding an LRS3 license since only clip IDs plus a sampling script are published for reproduction. See [[wiki/01-av-ste-audio-visual-speech-token-enhancement|AV-STE: Audio-Visual Speech Token Enhancement]].
