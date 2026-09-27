> [[index|Wiki]] | [[summary|Summary]]

# AV-STE: Audio-Visual Speech Token Enhancement — Digest

## 1. [[wiki/01-av-ste-audio-visual-speech-token-enhancement|AV-STE: Audio-Visual Speech Token Enhancement]]

**In one sentence:** AV-STE recovers clean Mimi semantic (cb0) tokens at 12.5 Hz from noisy 16 kHz speech by fusing audio with 96×96 grayscale lip-ROI video at 25 fps through an entropy-gated cross-attention module built on AV-HuBERT, so the enhanced tokens can replace noisy ones in any Mimi-based TTS or codec LM such as Moshi.

## Key points

- Input is noisy 16 kHz WAV plus 96×96 grayscale mouth-ROI MP4 at 25 fps; output is the enhanced Mimi semantic (cb0) token sequence at 12.5 Hz.
- Two checkpoints reproduce every semantic-token-accuracy row in the paper's main table: `avste.pt` for clean speech, non-speech background noise, and cross-dataset speaker interference, and `avste_lrs3_interference.pt` for same-corpus-style competing speakers and out-of-domain video.
- The demo runs AV-STE on four bundled LRS3 clips (speech vs. ambient noise at −10 dB and −5 dB) and prints semantic-token accuracy plus Mimi-decoded WER (Table A) and Moshi's generated response per condition (Table B).
- In the showcased speech-noise −5 dB example, AV-STE reaches 79.3% token accuracy and 38.5% WER versus 27.6% and 61.5% for the noisy Mimi baseline (clean upper bound 100.0% / 0.0%).
- Token accuracy is the primary metric (fraction of predicted cb0 tokens matching the clean reference at 12.5 Hz); WER is secondary/diagnostic, computed by Whisper-large-v3 on Mimi-decoded audio, with `(empty transcript)` shown when Whisper transcribes nothing at extreme noise.
- Inference requires extracting a 96×96 grayscale mouth crop at 25 fps with a visible front-facing face, resampling audio to 16 kHz mono, then running `scripts/infer_avste.py`; the `--output` extension selects enhanced tokens (`.pt`), reconstructed speech (`.wav`), or predictions JSON for Moshi streaming.
- Both checkpoints are `av_hubert_crossattn_ent` models (4-frame lookahead, entropy-gated cross-attention, `mimi_mix_loss`) fine-tuned from `large_vox_iter5.pt` on a 20/40/40 clean/non-speech/speaker-interference mix with SNR uniform in [-10, 10] dB, Adam (0.9/0.98), tri-stage LR schedule, and grad clip 5.0.

## The argument in five moves

1. Noisy speech corrupts Mimi semantic (cb0) tokens, so robust full-duplex dialogue requires recovering clean tokens rather than only denoising waveforms.
2. Lip-ROI video supplies noise-robust articulatory evidence, so fusing 96×96 grayscale mouth crops with noisy audio through entropy-gated cross-attention on AV-HuBERT recovers the clean cb0 sequence at 12.5 Hz.
3. Two checkpoints split the noise regime — `avste.pt` for clean, non-speech, and cross-dataset interference and `avste_lrs3_interference.pt` for same-corpus competing speakers and out-of-domain video — jointly covering every semantic-token-accuracy row of the main table.
4. The four-clip bundled demo makes the gain concrete: at speech-noise −5 dB AV-STE reaches 79.3% token accuracy and 38.5% WER versus 27.6% and 61.5% for noisy Mimi, with Moshi's generated response staying topical.
5. Token accuracy is the primary contract because enhanced tokens drop into any Mimi-based TTS or codec LM, while Mimi-decoded WER is only a secondary diagnostic; full-table claims rest on the 1321-clip protocol and the license-gated LRS3/AudioSet reproduction path.
