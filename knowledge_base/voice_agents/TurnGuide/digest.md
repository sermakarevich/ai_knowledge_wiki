> [[index|Wiki]] | [[summary|Summary]]

# dreamtheater123/TurnGuide — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** TurnGuide is an end-to-end full-duplex speech language model that generates coherent, meaningful full-duplex dialogues via dynamic turn-level text-speech interleaving, released with an inference demo and Fisher/Candor test splits for benchmarking.

## Key points

- TurnGuide introduces an end-to-end full-duplex speech language model for coherent, meaningful full-duplex dialogues (README.md:21).
- The initial release provides test splits from the Fisher and Candor datasets to support fair benchmarking (README.md:21).
- The repository includes the TurnGuide inference demo plus GLM-4-Voice code modules needed to run it (README.md:25).
- The inference stack consists of `turnguide_inference.py`, `turnguide_inference_reproducible.py`, `flow_inference.py`, `speech_tokenizer/`, `cosyvoice/`, and `third_party/Matcha-TTS/` (README.md:27-29).
- Model weights are not included; the GLM-4-Voice decoder must be downloaded separately and model paths passed explicitly (README.md:31).
- Two TurnGuide checkpoints differ only in text:speech token loss ratio — `qqjz/turnguide_loss_2_1` (2:1) versus `qqjz/turnguide_loss_3_1` (3:1) — selectable via `--model-path` (README.md:35-45).
- The tested runtime is Python 3.10 with PyTorch 2.5.0, torchaudio 2.5.0, CUDA 12.1, and transformers 4.44.1 (README.md:49-70).
- Inference runs on mono user-audio WAV files, exemplified by `examples/audio/fe_03_05844_first_2min_left.wav`, with outputs written to `--output-dir` (README.md:84-94).

## 2. [[wiki/02-top-level-files|top-level-files]]

**In one sentence:** The top-level files provide the runnable inference entry points, streaming flow-plus-HiFi-GAN audio decoder, pinned conda/pip environments, and repo-wide line-ending and ignore policy.

## Key points

- `turnguide_inference.py` is the GLM-4-Voice double-channel inference entry point that interleaves user speech-token chunks with per-chunk assistant generation and decodes to mono/stereo wav (`turnguide_inference.py:1-3`, `turnguide_inference.py:163-178`).
- `turnguide_inference_reproducible.py` is a second double-channel inference variant that replaces the logits-processor grammar with a `check_speech_token_num` retry loop and explicit `eos_token_id` stops (`turnguide_inference_reproducible.py:1-3`, `turnguide_inference_reproducible.py:51-78`, `turnguide_inference_reproducible.py:209-213`).
- `flow_inference.py` implements `AudioDecoder` plus `fade_in_out`, bridging flow-mel inference and HiFi-GAN waveform synthesis with per-UUID mel/hift caches and overlap handling (`flow_inference.py:10-16`, `flow_inference.py:19-80`, `flow_inference.py:92-97`).
- `environment.yml` pins the tested `turnguide` conda stack to `python=3.10.16`, `pytorch=2.5.0`, `torchaudio=2.5.0`, `pytorch-cuda=12.1` plus pip packages (`environment.yml:1-13`, `environment.yml:15-41`).
- `requirements.txt` mirrors the pip half of that stack and explicitly does not pin torch/CUDA packages, deferring them to `environment.yml` (`requirements.txt:1-3`, `requirements.txt:5-30`).
- `.gitattributes` forces `text eol=lf` for source/config suffixes and `.gitignore` excludes caches, venvs, checkpoints, generated audio, and experiment artifacts (`.gitattributes:1-9`, `.gitignore:1-47`).
- Both inference scripts were truncated in the chunk, so CLI/`main()` tails and post-decode stereo-mixing code are not covered here (`turnguide_inference.py:270`, `turnguide_inference_reproducible.py:260`).

## The system in five moves

1. TurnGuide frames the goal as coherent, meaningful full-duplex dialogue generated end-to-end via dynamic turn-level text-speech interleaving.
2. The release supports fair benchmarking with Fisher and Candor test splits while keeping model weights and full datasets as separate downloads.
3. Two checkpoints isolate one design choice — text:speech token loss ratios of 2:1 versus 3:1 — selectable through a shared `--model-path` flag.
4. Inference runs double-channel: mono user-audio WAV input is tokenized into 5-token chunks, each triggering one assistant chunk, then decoded to mono/stereo wav.
5. The audio path is bridged by a streaming flow-plus-HiFi-GAN `AudioDecoder` with per-UUID caches, overlap fading, and block-wise streaming synthesis.
6. A pinned Python 3.10 / PyTorch 2.5.0 / CUDA 12.1 / transformers 4.44.1 stack plus repo-wide LF and ignore policy makes the demo reproducible.
