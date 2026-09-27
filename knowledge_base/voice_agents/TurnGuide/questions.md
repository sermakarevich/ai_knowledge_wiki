---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: dreamtheater123/TurnGuide

### Q1. What is TurnGuide and what is its core modeling idea?

> [!tip]- Answer
> TurnGuide is an end-to-end full-duplex speech language model that generates coherent, meaningful full-duplex dialogues via dynamic turn-level text-speech interleaving. It was accepted to the Interspeech 2026 Long Paper Track and released with an inference demo plus Fisher/Candor test splits for fair benchmarking. See [[wiki/01-overview|Overview]].

### Q2. What checkpoints and external model assets does the TurnGuide demo require?

> [!tip]- Answer
> The two TurnGuide checkpoints are `qqjz/turnguide_loss_2_1` and `qqjz/turnguide_loss_3_1`, which differ only in text:speech token loss ratio (2:1 versus 3:1) and are selected via `--model-path`. Model weights are not bundled, so the GLM-4-Voice tokenizer (`zai-org/glm-4-voice-tokenizer`) and decoder (`zai-org/glm-4-voice-decoder`) must be downloaded separately and passed explicitly. See [[wiki/01-overview|Overview]].

### Q3. What is the tested runtime and the canonical inference command?

> [!tip]- Answer
> The tested runtime is Python 3.10 with PyTorch 2.5.0, torchaudio 2.5.0, CUDA 12.1, and transformers 4.44.1, with an `mkl=2021.4.0` pin to avoid a PyTorch import symbol error. The demo runs `turnguide_inference.py` on a mono user-audio WAV such as `examples/audio/fe_03_05844_first_2min_left.wav`, writing outputs to `--output-dir` with `--model-path`, `--tokenizer-path`, and `--flow-path` set explicitly. See [[wiki/01-overview|Overview]].

### Q4. How do the two top-level inference entry points differ?

> [!tip]- Answer
> `turnguide_inference.py` enforces per-chunk shape with an `AssistantChunkGrammarProcessor` plus `AssistantChunkStoppingCriteria`, generating `chunk_size * 2 + 1` tokens and dumping failures to `error_input_ids/` as `"sampling_error"`. The reproducible variant `turnguide_inference_reproducible.py` instead loops `generate()` until `check_speech_token_num` passes, appends end-of-text token 151349 for all-text chunks, and reports `"while_true_generation_error"`. Both share the double-channel loop that tokenizes user audio into 5-token chunks, each triggering one assistant chunk. See [[wiki/02-top-level-files|top-level-files]].

### Q5. How does `flow_inference.py` bridge tokens to waveforms during streaming?

> [!tip]- Answer
> `AudioDecoder.token2wav` runs flow-mel inference, blends the result against a cached mel overlap with `fade_in_out`, then synthesizes the waveform through HiFi-GAN while carrying per-UUID mel and hift caches. With `finalize=False` it trims and retains tail caches for continuity, and with `finalize=True` it clears both caches; `stream_inference` blocks tokens by encoder block size and finalizes only the last block. See [[wiki/02-top-level-files|top-level-files]].

### Q6. How are the environment and repo-policy files organized?

> [!tip]- Answer
> `environment.yml` pins the `turnguide` conda stack to `python=3.10.16`, `pytorch=2.5.0`, `torchaudio=2.5.0`, and `pytorch-cuda=12.1` plus a full pip block, while `requirements.txt` mirrors only the pip half and defers torch/CUDA to the conda file. `.gitattributes` forces `text eol=lf` across source and config suffixes, and `.gitignore` excludes caches, venvs, checkpoints, generated audio, and experiment artifacts while keeping the example clip. See [[wiki/02-top-level-files|top-level-files]].

### Q7. A colleague wants the most faithful reproduction of the paper demo on a fresh CUDA box — which script, checkpoint, and checks would you recommend and why?

> [!tip]- Answer
> I recommend the reproducible variant `turnguide_inference_reproducible.py` with the `qqjz/turnguide_loss_2_1` checkpoint on the pinned Python 3.10 / PyTorch 2.5.0 / CUDA 12.1 stack, validating first with the bundled `fe_03_05844` clip before custom audio. This is the conservative baseline because the retry-loop variant plus the lower text-guidance checkpoint minimizes behavioral drift, and the known-good clip separates setup errors from audio-format issues. Only switch to the current grammar-based script or the 3:1 checkpoint when comparing guidance strength or latest behavior. See [[wiki/02-top-level-files|top-level-files]].
