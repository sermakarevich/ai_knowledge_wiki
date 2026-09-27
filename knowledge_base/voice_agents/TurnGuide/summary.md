# Technical Analysis: dreamtheater123/TurnGuide

**Repository:** https://github.com/dreamtheater123/TurnGuide
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Full-duplex spoken dialogue — simultaneous listening and speaking with overlaps, backchannels, and interruptions — is the normal mode of human conversation, but most spoken dialogue systems remain half-duplex, alternating strict turns. End-to-end full-duplex speech language models reproduce simultaneity but tend to generate fluent yet incoherent or semantically thin output.

TurnGuide addresses the coherence gap by introducing dynamic turn-level text-speech interleaving: the model plans utterance content in text at turn granularity before or alongside streaming speech-token generation, so simultaneous output remains semantically guided (01-overview.md:3, 01-overview.md:15-17). The repository is the inference-and-benchmarking release for the Interspeech 2026 Long Paper Track paper (arXiv:2508.07375), not a training release: it ships the TurnGuide inference demo, the GLM-4-Voice tokenizer/decoder modules required to run it, and Fisher/Candor test splits for fair benchmarking (01-overview.md:5-8, 01-overview.md:19-22). Model weights are excluded and fetched separately from Hugging Face (01-overview.md:9).

Primary user: speech-dialogue researchers and engineers benchmarking or demoing coherent full-duplex interaction on Fisher/Candor-style two-party conversational audio.

## 2. High-Level Architecture

```
mono user WAV ─► SpeechProcessor ─► WhisperVQEncoder + WhisperFeatureExtractor ─► user speech tokens
                        │
                        ▼
          TurnGuide checkpoint (qqjz/turnguide_loss_2_1 | _3_1)
          double-channel loop: 5-token user chunk ─► 1 assistant chunk
                        │
                        ▼
          Assistant speech tokens ─► AudioDecoder (flow + HiFi-GAN) ─► assistant.wav
                        │                                              stereo_user_left_assistant_right.wav
                        ▼
                   ./turnguide_demo_output (--output-dir)
```

Data flow:

1. User audio ingest and tokenization. `SpeechProcessor.generate_conditional_interleaved_speech_token_only` takes a mono user-audio WAV (e.g. `examples/audio/fe_03_05844_first_2min_left.wav`), extracts discrete speech tokens via `extract_speech_token`, rejects the sentinel token `16383`, and drops a short trailing chunk (02-top-level-files.md:77, 01-overview.md:88-100).
2. Double-channel interleaved generation. The token stream is seeded with `<|begin_of_audio|><|begin_of_audio|>`; per 5-token user chunk (`chunk_size = 5`) the processor appends speaker framing (`<|reserved_151347|>`, audio-id tokens, `<|reserved_151348|>`) and generates one assistant chunk with the TurnGuide checkpoint selected by `--model-path` (02-top-level-files.md:54-77).
3. Chunk-shape enforcement. The current script constrains each assistant chunk with `AssistantChunkGrammarProcessor` / `AssistantChunkStoppingCriteria` and `generate(max_new_tokens=chunk_size * 2 + 1)`; the reproducible variant instead loops `generate(max_new_tokens=chunk_size, eos_token_id=[...])` until `check_speech_token_num` passes (02-top-level-files.md:78).
4. Waveform synthesis. Assistant speech tokens pass to `AudioDecoder.token2wav` (`flow_inference.py`), which runs flow-mel inference, cross-fades against a cached mel overlap via `fade_in_out`, prepends the HiFi-GAN mel cache, and synthesizes waveform chunks; `stream_inference` concatenates blocks and finalizes only the last one (02-top-level-files.md:51).
5. Output materialization. Decoded mono assistant audio and a stereo mix (user left, assistant right) are written under `--output-dir` (default `./turnguide_demo_output`); runs are skipped when both outputs already exist and failures are dumped to `./error_input_ids/error_<timestamp>.pt` (02-top-level-files.md:77-78, 01-overview.md:89-95).

Persistent state lives outside the repo: Hugging Face or local checkpoint directories (`--model-path`, `--tokenizer-path`, `--flow-path` clone of `glm-4-voice-decoder`), per-UUID mel/hift caches held in memory during decoding (`mel_overlap_dict` / `hift_cache_dict`), and on-disk outputs under `--output-dir` plus `error_input_ids/` dumps. The repo itself carries no database; `.gitignore` explicitly excludes checkpoints, models, outputs, and `*.wav` except the single example clip (02-top-level-files.md:26-34).

## 3. Turn-Level Text-Speech Interleaving

Representation: dialogue is modeled as two parallel discrete-token channels (user, assistant) over a shared vocabulary that mixes text tokens, speech (audio-id) tokens, role tokens, and framing tokens. Generation proceeds by interleaving fixed-size user speech-token chunks with per-chunk assistant generations, where text planning at turn granularity steers the assistant's speech tokens — the "think before you talk" mechanism summarized in the one-sentence wiki statement (01-overview.md:3).

Named token kinds (shared table in both inference scripts, `turnguide_inference.py:38-50`):

| Kind | Token | ID |
|---|---|---|
| Audio framing | `<|begin_of_audio|>`, `<|end_of_audio|>` | 151343, 151344 |
| Roles | `<|system|>`, `<|user|>`, `<|assistant|>` | 151335, 151336, 151337 |
| Audio-id base | `<|audio_0|>` (`audio_offset`) | 152353 |
| Transcription framing | `<|begin_of_transcription|>`, `<|end_of_transcription|>` | 151345, 151346 |
| Speaker ids | `<|reserved_151347|>`, `<|reserved_151348|>` | 151347, 151348 |
| End-of-text | `<|reserved_151349|>` | 151349 |

Chunking constants (`turnguide_inference.py:10-23`): `temperature = 1.3`, `p_value = 0.9`, `chunk_size = 5`; decoder hop bounds derived in `AudioDecoder.__init__` (`flow_inference.py:19-45`) as `token_min_hop_len = 2 * flow.input_frame_rate`, `token_max_hop_len = 4 * flow.input_frame_rate`, `token_overlap_len = 5`, `mel_cache_len = 1`.

Key query — the per-chunk interleave step (`turnguide_inference.py:163-178`):

```python
def generate_conditional_interleaved_speech_token_only(self, input_audio_path, temperature, top_p, output_dir, assistant_audio_name="assistant.wav", stereo_audio_name="stereo_user_left_assistant_right.wav"):
```

It encodes the user WAV to speech tokens, seeds `<|begin_of_audio|><|begin_of_audio|>`, then iterates: append `<|reserved_151347|>` + audio-id tokens + `<|reserved_151348|>` for each 5-token user chunk and generates one assistant chunk (02-top-level-files.md:77).

## 4. LLM / External Service Integration

The repo calls no LLM or other remote API at inference time. All generation is local: a TurnGuide checkpoint loaded via `--model-path` plus the GLM-4-Voice tokenizer (`--tokenizer-path`) and decoder (`--flow-path`) (01-overview.md:30-43, 01-overview.md:77-87).

| Asset | Identifier / path | Required? |
|---|---|---|
| TurnGuide checkpoint, text:speech loss 2:1 | `qqjz/turnguide_loss_2_1` | Yes — one of the two checkpoints |
| TurnGuide checkpoint, text:speech loss 3:1 | `qqjz/turnguide_loss_3_1` | Alternative to the 2:1 checkpoint |
| GLM-4-Voice tokenizer | `zai-org/glm-4-voice-tokenizer` (default constant `THUDM/glm-4-voice-tokenizer`) | Required |
| GLM-4-Voice decoder clone | `zai-org/glm-4-voice-decoder` (default `./glm-4-voice-decoder`) | Required |

Checkpoint selection differs only in training text:speech token loss ratio (2:1 vs 3:1) and is switched by changing `--model-path`; a local directory may be passed instead of a Hub id (01-overview.md:39-43, 01-overview.md:97-100). No API keys, bearer tokens, or service env vars are documented; the only forced env assignment in the shared script header is `os.environ["CUDA_VISIBLE_DEVICES"] = str(cuda_num)` with `cuda_num = 0` (02-top-level-files.md:54-66). GLM-4-Voice code is Apache-2.0; its weights are under a separate model license and must be downloaded separately (01-overview.md:113-115).

## 5. Double-Channel Interleaved Inference Pipeline

Step by step (function per step with defining location):

1. Process setup — module header of `turnguide_inference.py:10-23` (`turnguide_inference_reproducible.py:9-22`): fixes `REPO_ROOT` on `sys.path` (plus `third_party/Matcha-TTS`), pins `CUDA_VISIBLE_DEVICES` to GPU 0, and sets defaults `DEFAULT_MODEL_PATH = "qqjz/turnguide_loss_2_1"`, `DEFAULT_TOKENIZER_PATH`, `DEFAULT_FLOW_PATH`, `temperature = 1.3`, `p_value = 0.9`, `chunk_size = 5` (02-top-level-files.md:54-66).
2. Processor construction — `SpeechProcessor.__init__(self, model_path, tokenizer_path, flow_path, device="cuda", dtype="bfloat16")` (`turnguide_inference.py:116-160`): loads the GLM backbone (optional 4-bit `BitsAndBytesConfig` when `dtype == "int4"`), the `WhisperVQEncoder` speech tokenizer with `WhisperFeatureExtractor`, and `AudioDecoder` from `config.yaml` / `flow.pt` / `hift.pt` (02-top-level-files.md:77).
3. User-token encoding — `extract_speech_token` (called inside `generate_conditional_interleaved_speech_token_only`, `turnguide_inference.py:163-178`): converts the input WAV to discrete tokens; aborts with `"unsupported_token"` on id `16383` and drops the short trailing chunk (02-top-level-files.md:77).
4. Interleaved assistant generation — `generate_conditional_interleaved_speech_token_only(...)` (`turnguide_inference.py:163-178`): early-returns `"exist"` when both output wavs exist; otherwise seeds the audio framing and alternates 5-token user chunks with one assistant chunk each (02-top-level-files.md:77).
5a. Current-script chunk control — `AssistantChunkGrammarProcessor(prompt_len, audio_offset, vocab_size, pad_token_id=None, chunk_size=5)` and `AssistantChunkStoppingCriteria(prompt_len, audio_offset, chunk_size=5)` (`turnguide_inference.py:54-114`): enforce chunk shape during `generate(max_new_tokens=chunk_size * 2 + 1, ...)` (`turnguide_inference.py:229-261`); failures dump inputs to `./error_input_ids/error_<timestamp>.pt` with `"sampling_error"` (02-top-level-files.md:78).
5b. Reproducible-variant chunk control — `check_speech_token_num(token_sequence, audio_offset)` (`turnguide_inference_reproducible.py:51-78`): retry loop around `generate(max_new_tokens=chunk_size, ..., eos_token_id=[end_of_audio_offset, 151347, 151348])` (`turnguide_inference_reproducible.py:209-247`); appends `151349` when a chunk is all text, asserts `new_token >= audio_offset` before subtracting the offset, reports `"while_true_generation_error"` (02-top-level-files.md:78).
6. Mel synthesis — `AudioDecoder.token2wav(self, token, uuid, prompt_token, prompt_feat, embedding, finalize)` (`flow_inference.py:48-49`): runs `flow.inference`, applies `fade_in_out(fade_in_mel, fade_out_mel, window)` (`flow_inference.py:10-16`) against the cached overlap, and manages per-UUID `mel_overlap_dict` / `hift_cache_dict` (retain tails unless `finalize is True`, then clear) (02-top-level-files.md:51).
7. Streaming assembly — `AudioDecoder.stream_inference(self, token)` (`flow_inference.py:48-49` listed set) vs `AudioDecoder.offline_inference(self, token)`: streaming blocks tokens by `flow.encoder.block_size`, threads prior mels/tokens as `prompt_feat`/`prompt_token`, finalizes only the last block, concatenates waveforms; offline mints `uuid.uuid1()` and calls `token2wav(..., finalize=True)` (02-top-level-files.md:51).
8. Output write — tail of `generate_conditional_interleaved_speech_token_only` plus CLI/`main()` (truncated in wiki coverage after `turnguide_inference.py:270` / `turnguide_inference_reproducible.py:260`): writes `assistant.wav` and `stereo_user_left_assistant_right.wav` to `--output-dir` (02-top-level-files.md:77, 02-top-level-files.md:80-81).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | ~122 (citation block at README.md:115-122) | Paper identity, demo links, checkpoint table, env setup, inference command, data sources, license/citation |
| `turnguide_inference.py` | 454 (wiki coverage truncated at ~line 269) | Current double-channel inference entry point; grammar-processor chunk control, per-chunk assistant generation, wav/stereo decode |
| `turnguide_inference_reproducible.py` | 435 (wiki coverage truncated at ~line 264) | Legacy inference variant; retry-loop chunk control via `check_speech_token_num`, explicit EOS stops |
| `flow_inference.py` | ~97+ (`AudioDecoder` at flow_inference.py:19-20, methods at 48-49, caches at 92-97) | Streaming vocoder bridge: `AudioDecoder` + `fade_in_out`, flow-mel to HiFi-GAN waveform with overlap/cache handling |
| `speech_tokenizer/` | directory | GLM-4-Voice-derived discrete speech tokenizer (`WhisperVQEncoder` + `WhisperFeatureExtractor`) used for user-audio encoding |
| `cosyvoice/` | directory | GLM-4-Voice-derived decoder-stack code supporting flow/HiFi-GAN synthesis |
| `third_party/Matcha-TTS/` | directory (appended to `sys.path`) | Bundled TTS dependency required by the inference imports |
| `environment.yml` | ~41 | Pinned conda stack (`turnguide` env): Python, PyTorch/CUDA, MKL, ffmpeg + pip block |
| `requirements.txt` | ~30 | Pip-only mirror of the conda pip block; defers torch/CUDA to `environment.yml` |
| `examples/audio/fe_03_05844_first_2min_left.wav` | binary example | Bundled mono user-audio demo input (first 2 min, left channel) |
| `.gitattributes` | 9 | Forces `text eol=lf` for `.py/.sh/.md/.txt/.yml/.yaml/.json/.toml/.pyx` |
| `.gitignore` | 47 | Excludes caches, venvs, checkpoints/models, outputs, generated audio, experiment artifacts, OS/editor files |
| `glm-4-voice-decoder/` (clone target) | external clone | Flow decoder assets (`config.yaml`, `flow.pt`, `hift.pt`) loaded by `AudioDecoder` via `--flow-path` |
| `error_input_ids/` (runtime) | generated | Failure dumps `error_<timestamp>.pt` on sampling/generation errors |

Coverage notes: inference-script tails (decode-to-wav, stereo mixing, CLI `main()`) were truncated in the wiki source and are not line-cited beyond the truncation markers (02-top-level-files.md:80-81); `speech_tokenizer/`, `cosyvoice/`, and `third_party/Matcha-TTS/` internals have no per-file breakdown in the two wiki pages (01-overview.md:24-28).

## 7. Dependencies

Required runtime (exact constraint strings from `environment.yml:1-41` pip block and `README.md:49-71` version check):

| Package | Version constraint | Purpose |
|---|---|---|
| `python` | `=3.10.16` (conda) | Interpreter for the tested `torch250cu121` stack |
| `pytorch` | `=2.5.0` (conda) | Model inference backend |
| `torchaudio` | `=2.5.0` (conda) | Audio I/O and feature handling |
| `torchvision` | `=0.20.0` (conda) | Pinned alongside torch |
| `pytorch-cuda` | `=12.1` (conda; `CUDA 12.1`) | CUDA toolkit binding |
| `mkl` | `=2021.4.0` | Avoids `iJIT_NotifyEvent` import breakage on newer MKL with torch 2.5.0 |
| `ffmpeg` | (conda, unpinned) | Audio transcoding for example/decoder I/O |
| `transformers` | `==4.44.1` | GLM backbone + tokenizer loading |
| `tokenizers` | `==0.19.1` | Tokenizer backend |
| `tiktoken` | (pip, noted in README.md:56) | TurnGuide tokenizer remote code |
| `accelerate` | `==1.4.0` | Model loading/dispatch |
| `conformer` | `==0.3.2` | Speech-encoder component |
| `diffusers` | `==0.38.0` | Decoder-stack dependency |
| `gradio` | `==5.21.0` | Demo UI dependency |
| `hydra-core` | `==1.3.3` | Config handling |
| `HyperPyYAML` | `==1.2.2` | `load_hyperpyyaml` for flow/hift configs |
| `ruamel.yaml` | `==0.18.6` | YAML loading for decoder configs through HyperPyYAML |
| `librosa` | `==0.11.0` | Audio feature utilities |
| `lightning` | `==2.5.1.post0` | Training-stack residue / decoder dependency |
| `sentencepiece` | `==0.2.0` | Subword tokenization backend |
| `soundfile` | `==0.13.1` | WAV read/write |

Install discipline: `requirements.txt:1-3` requires torch/torchaudio/torchvision/CUDA via `environment.yml` first and intentionally omits torch pins; the remainder repeats the same pip pins (02-top-level-files.md:36-38). Conda-first path is `conda env create -f environment.yml && conda activate turnguide`; pip-only path is `pip install -r requirements.txt` inside a pre-existing CUDA 12.1 torch environment (01-overview.md:45-74).

## 8. CLI / Usage Surface

Entry points: `turnguide_inference.py` (current) and `turnguide_inference_reproducible.py` (legacy variant); both expose `SpeechProcessor` programmatically and a CLI `main()` tail (truncated in wiki coverage) (02-top-level-files.md:5-11, 02-top-level-files.md:80-81).

Commands:

```bash
git clone https://huggingface.co/zai-org/glm-4-voice-decoder
python turnguide_inference.py \
  --input-audio examples/audio/fe_03_05844_first_2min_left.wav \
  --model-path qqjz/turnguide_loss_2_1 \
  --tokenizer-path zai-org/glm-4-voice-tokenizer \
  --flow-path ./glm-4-voice-decoder \
  --output-dir ./turnguide_demo_output
```

| Flag | Example value | Meaning |
|---|---|---|
| `--input-audio` | `examples/audio/fe_03_05844_first_2min_left.wav` | Mono user-audio WAV; replaceable with any mono WAV |
| `--model-path` | `qqjz/turnguide_loss_2_1` | TurnGuide checkpoint; swap to `qqjz/turnguide_loss_3_1` or a local dir for the 3:1 variant |
| `--tokenizer-path` | `zai-org/glm-4-voice-tokenizer` | Speech/text tokenizer source |
| `--flow-path` | `./glm-4-voice-decoder` | Cloned decoder directory holding `config.yaml`, `flow.pt`, `hift.pt` |
| `--output-dir` | `./turnguide_demo_output` | Destination for `assistant.wav` + stereo mix |

Env-var and config tables:

| Env var | Value / effect |
|---|---|
| `CUDA_VISIBLE_DEVICES` | Forced to `"0"` (`cuda_num = 0`) in both script headers |

| Config surface | Location | Notes |
|---|---|---|
| Conda env | `environment.yml:1-13` | `name: turnguide`, channels `pytorch, nvidia, defaults` |
| Pip pins | `environment.yml:15-41`, `requirements.txt:5-30` | Identical pip blocks; see Dependencies |
| Decoder configs | `<flow-path>/config.yaml` | Loaded via `load_hyperpyyaml` in `AudioDecoder.__init__` |
| Generation constants | Script headers (`turnguide_inference.py:10-23`) | `temperature = 1.3`, `p_value = 0.9`, `chunk_size = 5`, default Hub paths |
| Benchmark data ids | README.md:98-105 | Fisher `fe_03_11632` (60–180s), Candor `46f8e9b8-…` (420–540s); full corpora via LDC / Candor site |

## 9. Extensibility Points

- New decoding/chunking policy: extend or replace `AssistantChunkGrammarProcessor` / `AssistantChunkStoppingCriteria` in `turnguide_inference.py:54-114`, or port the `check_speech_token_num` retry loop in `turnguide_inference_reproducible.py:51-78` for deterministic-shape generation.
- Alternative checkpoint or loss-ratio study: subclass or reconfigure `SpeechProcessor.__init__` (`turnguide_inference.py:116-160`) to point `--model-path` at a new checkpoint; the 2:1 vs 3:1 switch is already just a path change (01-overview.md:39-43).
- Tokenizer/encoder swap: replace the `WhisperVQEncoder` + `WhisperFeatureExtractor` construction inside `SpeechProcessor.__init__` (`turnguide_inference.py:116-160`) and update the shared token-id table (`turnguide_inference.py:38-50`).
- Vocoder/synthesis upgrade: extend `AudioDecoder` in `flow_inference.py:19-80` (`token2wav`, `stream_inference`, `offline_inference`) or override `fade_in_out` (`flow_inference.py:10-16`) to change overlap, windowing (Hamming `mel_window`/`speech_window`), hop lengths, or cache policy.
- Input/output handling: extend `generate_conditional_interleaved_speech_token_only` (`turnguide_inference.py:163-178`) to support stereo input, streaming input, different `assistant_audio_name` / `stereo_audio_name`, or non-skip (`"exist"`) caching behavior.
- Environment extension: add packages to both `environment.yml:15-41` and `requirements.txt:5-30` (they must be kept in sync; torch/CUDA stays conda-side per `requirements.txt:1-3`).

## 10. Limitations and Gotchas

- **Weights and decoder are external and version-sensitive.** Nothing generates audio from a bare clone: the TurnGuide checkpoint, the GLM-4-Voice tokenizer, and a separately cloned `glm-4-voice-decoder` must all be fetched and their paths passed explicitly; GLM-4-Voice weights sit under their own license (01-overview.md:9, 01-overview.md:30-38, 01-overview.md:113-115).
- **Tightly pinned, brittle runtime.** The tested stack (Python 3.10.16, torch/torchaudio 2.5.0, CUDA 12.1, transformers 4.44.1, `mkl=2021.4.0`) is load-bearing — newer MKL breaks torch imports with an `iJIT_NotifyEvent` error — and `requirements.txt` silently defers torch/CUDA to `environment.yml`, so pip-only installs in a mismatched env fail late (01-overview.md:45-56, 02-top-level-files.md:36-38).
- **Two divergent inference scripts with no selection guide.** The current grammar-processor path and the reproducible retry-loop path differ in EOS handling, `max_new_tokens` (`chunk_size * 2 + 1` vs `chunk_size`), failure modes (`"sampling_error"` vs `"while_true_generation_error"`), and the `151349` end-of-text fixup, but the wiki states no rule for which to use (02-top-level-files.md:78).
- **Truncated coverage of the output tail.** Wiki chunking stops at `turnguide_inference.py:270` (of 454) and `turnguide_inference_reproducible.py:260` (of 435), so decode-to-wav, stereo mixing, and CLI/`main()` argument definitions are undescribed — verify flags against the actual file before scripting around them (02-top-level-files.md:80-81).
- **Narrow, dated input contract.** The demo assumes mono user-audio WAV, single-GPU (`cuda_num = 0`), and sentinel-token rejection (`16383` → `"unsupported_token"`); stereo input, multi-GPU, and streaming microphone use are unhandled in the documented path (01-overview.md:97-100, 02-top-level-files.md:54-77).
- **Benchmark splits without bundled audio.** Only Fisher/Candor test-split references ship (example: `fe_03_11632` 60–180s; Candor `46f8e9b8-…` 420–540s); full corpora require separate LDC/Candor downloads, and only one example clip (`fe_03_05844_first_2min_left.wav`) is whitelisted past the `*.wav` gitignore (01-overview.md:102-111, 02-top-level-files.md:26-34).

## 11. How It Compares to Alternatives

- **THUDM GLM-4-Voice.** The direct base: TurnGuide reuses its double-channel speech-token framing, `WhisperVQEncoder` tokenizer, and flow-plus-HiFi-GAN `AudioDecoder` stack (`flow_inference.py`, `speech_tokenizer/`, `cosyvoice/`) (01-overview.md:24-28, 01-overview.md:113-115). GLM-4-Voice is the general end-to-end voice dialogue model; TurnGuide is the narrower coherence extension adding turn-level text guidance and the 2:1/3:1 loss-ratio checkpoints on top.
- **Kyutai Moshi.** A real-time full-duplex speech dialogue model (streaming, interruptible, on-device-capable) with its own inner/outer codec and latency-first design. Moshi optimizes for responsiveness and deployability; TurnGuide optimizes for semantic coherence of simultaneous dialogue and ships as a research benchmark (Fisher/Candor splits) rather than a latency-tuned product.
- **Meta Spirit LM / Expressive Spirit LM.** Interleaved text-speech foundation models mixing text and speech tokens for expressive generation. Spirit LM explores text-speech interleaving as a pretraining paradigm; TurnGuide applies the same family of idea specifically at conversational-turn granularity for full-duplex interaction, with explicit per-chunk assistant generation and speaker-id framing tokens.
- **Mini-Omni / Freeze-Omni family.** Open streaming speech-interaction models that add simultaneous generation with lightweight adapters over frozen LLMs. They prioritize cheap adaptation of existing text LLMs to voice; TurnGuide trains (and checkpoints at two loss ratios) an end-to-end full-duplex speech language model instead, trading adapter economy for joint text-speech modeling.

Positioning: TurnGuide sits between its GLM-4-Voice substrate and latency-first full-duplex systems — it keeps GLM-4-Voice's token and vocoder stack while differentiating on turn-level text planning for meaningfulness, released primarily as reproducible inference code plus benchmark splits rather than as a deployable assistant.

## Appendix: Selected Code Snippets

1. Shared inference header (`turnguide_inference.py:10-23`, mirrored in `turnguide_inference_reproducible.py:9-22`):

```
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(REPO_ROOT)
sys.path.append(os.path.join(REPO_ROOT, "third_party", "Matcha-TTS"))
os.environ["CUDA_VISIBLE_DEVICES"] = str(cuda_num)  # cuda_num = 0
DEFAULT_MODEL_PATH = "qqjz/turnguide_loss_2_1"
DEFAULT_TOKENIZER_PATH = "THUDM/glm-4-voice-tokenizer"
DEFAULT_FLOW_PATH = os.path.join(REPO_ROOT, "glm-4-voice-decoder")
temperature = 1.3
p_value = 0.9
chunk_size = 5
```

2. Streaming vocoder entry points (`flow_inference.py:10-16`, `flow_inference.py:19-20`, `flow_inference.py:48-49`):

```
def fade_in_out(fade_in_mel, fade_out_mel, window):
class AudioDecoder:
    def __init__(self, config_path, flow_ckpt_path, hift_ckpt_path, device="cuda"):
    def token2wav(self, token, uuid, prompt_token=torch.zeros(1, 0, dtype=torch.int32),
                  prompt_feat=torch.zeros(1, 0, 80), embedding=torch.zeros(1, 192), finalize=False):
    def offline_inference(self, token):
    def stream_inference(self, token):
```

3. Demo invocation (`README.md:82-90`):

```bash
git clone https://huggingface.co/zai-org/glm-4-voice-decoder

python turnguide_inference.py \
  --input-audio examples/audio/fe_03_05844_first_2min_left.wav \
  --model-path qqjz/turnguide_loss_2_1 \
  --tokenizer-path zai-org/glm-4-voice-tokenizer \
  --flow-path ./glm-4-voice-decoder \
  --output-dir ./turnguide_demo_output
```

4. Environment setup and version check (`README.md:49-54`, `README.md:60-71`):

```bash
conda env create -f environment.yml
conda activate turnguide
python -c "import torch, torchaudio, transformers; print(torch.__version__); print(torch.version.cuda); print(torchaudio.__version__); print(transformers.__version__); print(torch.cuda.is_available())"
```
