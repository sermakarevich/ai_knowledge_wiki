> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The top-level files provide the runnable inference entry points, streaming flow-plus-HiFi-GAN audio decoder, pinned conda/pip environments, and repo-wide line-ending and ignore policy.
## Key points
- `turnguide_inference.py` is the GLM-4-Voice double-channel inference entry point that interleaves user speech-token chunks with per-chunk assistant generation and decodes to mono/stereo wav (`turnguide_inference.py:1-3`, `turnguide_inference.py:163-178`).
- `turnguide_inference_reproducible.py` is a second double-channel inference variant that replaces the logits-processor grammar with a `check_speech_token_num` retry loop and explicit `eos_token_id` stops (`turnguide_inference_reproducible.py:1-3`, `turnguide_inference_reproducible.py:51-78`, `turnguide_inference_reproducible.py:209-213`).
- `flow_inference.py` implements `AudioDecoder` plus `fade_in_out`, bridging flow-mel inference and HiFi-GAN waveform synthesis with per-UUID mel/hift caches and overlap handling (`flow_inference.py:10-16`, `flow_inference.py:19-80`, `flow_inference.py:92-97`).
- `environment.yml` pins the tested `turnguide` conda stack to `python=3.10.16`, `pytorch=2.5.0`, `torchaudio=2.5.0`, `pytorch-cuda=12.1` plus pip packages (`environment.yml:1-13`, `environment.yml:15-41`).
- `requirements.txt` mirrors the pip half of that stack and explicitly does not pin torch/CUDA packages, deferring them to `environment.yml` (`requirements.txt:1-3`, `requirements.txt:5-30`).
- `.gitattributes` forces `text eol=lf` for source/config suffixes and `.gitignore` excludes caches, venvs, checkpoints, generated audio, and experiment artifacts (`.gitattributes:1-9`, `.gitignore:1-47`).
- Both inference scripts were truncated in the chunk, so CLI/`main()` tails and post-decode stereo-mixing code are not covered here (`turnguide_inference.py:270`, `turnguide_inference_reproducible.py:260`).
---
## Repo policy files
`.gitattributes` (`.gitattributes:1-9`) contains only:
```
*.py text eol=lf
*.sh text eol=lf
*.md text eol=lf
*.txt text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.json text eol=lf
*.toml text eol=lf
*.pyx text eol=lf
```
`.gitignore` (`.gitignore:1-47`) excludes:
| Group | Entries |
|---|---|
| Caches | `__pycache__/`, `*.py[cod]`, `*.egg-info/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/` |
| Local envs | `.env`, `.venv/`, `venv/`, `env/` |
| Checkpoints/assets | `/ckpts/`, `/models/`, `/glm-4-voice-9b/`, `/glm-4-voice-tokenizer/`, `/glm-4-voice-decoder/`, `*.pt`, `*.pth`, `*.bin`, `*.safetensors`, `*.ckpt` |
| Generated outputs | `outputs/`, `turnguide_demo_output/`, `error_input_ids/`, `*.wav` (except `!examples/audio/fe_03_05844_first_2min_left.wav`), `*.mp3`, `*.flac`, `*_output.txt` |
| Experiment artifacts | `generated_ids_record*.json`, `semantic_correctness_results_*.json`, `trainer_state.json`, `training_loss.png` |
| OS/editor | `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/` |

## Environment pins
`environment.yml` (`environment.yml:1-13`) declares `name: turnguide`, channels `pytorch, nvidia, defaults`, and conda deps `python=3.10.16`, `pip`, `pytorch=2.5.0`, `torchaudio=2.5.0`, `torchvision=0.20.0`, `pytorch-cuda=12.1`, `mkl=2021.4.0`, `ffmpeg`. Its pip block (`environment.yml:15-41`) pins e.g. `accelerate==1.4.0`, `conformer==0.3.2`, `diffusers==0.38.0`, `gradio==5.21.0`, `hydra-core==1.3.3`, `HyperPyYAML==1.2.2`, `librosa==0.11.0`, `lightning==2.5.1.post0`, `transformers==4.44.1`, `tokenizers==0.19.1`, `sentencepiece==0.2.0`, `soundfile==0.13.1`.
`requirements.txt` (`requirements.txt:1-3`) states it matches the tested `torch250cu121` environment, requires installing torch/torchaudio/torchvision/CUDA via `environment.yml` first, and intentionally omits torch pins; the remainder (`requirements.txt:5-30`) repeats the same pip pins as `environment.yml`.

## Streaming vocoder bridge (`flow_inference.py`)
Verbatim entry points (`flow_inference.py:10-16`, `flow_inference.py:19-20`, `flow_inference.py:48-49`):
```
def fade_in_out(fade_in_mel, fade_out_mel, window):
class AudioDecoder:
    def __init__(self, config_path, flow_ckpt_path, hift_ckpt_path, device="cuda"):
    def token2wav(self, token, uuid, prompt_token=torch.zeros(1, 0, dtype=torch.int32),
                  prompt_feat=torch.zeros(1, 0, 80), embedding=torch.zeros(1, 192), finalize=False):
    def offline_inference(self, token):
    def stream_inference(self, token):
```
Behavior (`flow_inference.py:19-45`, `flow_inference.py:60-91`): `__init__` loads flow/hift configs via `load_hyperpyyaml`, loads both checkpoints, sets per-UUID `mel_overlap_dict`/`hift_cache_dict`, derives `token_min_hop_len = 2 * flow.input_frame_rate`, `token_max_hop_len = 4 * flow.input_frame_rate`, `token_overlap_len = 5`, Hamming `mel_window`/`speech_window`, and `mel_cache_len = 1`. `token2wav` runs `flow.inference`, applies `fade_in_out` against the cached mel overlap, prepends the HiFi-GAN mel cache, keeps tail caches when `finalize is False` (trimming `mel_overlap_len` mels and `source_cache_len` samples), and clears both dict entries when `finalize is True`. `offline_inference` mints `uuid.uuid1()` and calls `token2wav(..., finalize=True)`; `stream_inference` blocks tokens by `flow.encoder.block_size`, threads prior mels/tokens as `prompt_feat`/`prompt_token`, finalizes only the last block, and concatenates chunk waveforms.

## Main inference entry points
Shared header (`turnguide_inference.py:10-23`, `turnguide_inference_reproducible.py:9-22`):
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
Shared token table (`turnguide_inference.py:38-50`, `turnguide_inference_reproducible.py:36-48`):
| Token | ID | Role noted in chunk |
|---|---|---|
| `<|begin_of_audio|>` | 151343 | audio framing |
| `<|end_of_audio|>` | 151344 | audio framing |
| `<|system|>` / `<|user|>` / `<|assistant|>` | 151335 / 151336 / 151337 | roles |
| `<|audio_0|>` | 152353 | `audio_offset` base |
| `<|begin_of_transcription|>` / `<|end_of_transcription|>` | 151345 / 151346 | transcription framing |
| `<|reserved_151347|>` / `<|reserved_151348|>` | 151347 / 151348 | speaker1/speaker2 id tokens |
| `<|reserved_151349|>` | 151349 | end-of-text token |
Shared `SpeechProcessor.__init__(self, model_path="./glm-4-voice-9b", tokenizer_path="./glm-4-voice-tokenizer", flow_path="./glm-4-voice-decoder", device="cuda", dtype="bfloat16")` (`turnguide_inference.py:116-160`, `turnguide_inference_reproducible.py:81-125`) loads the GLM model (optional 4-bit `BitsAndBytesConfig` when `dtype == "int4"`), the `WhisperVQEncoder` speech tokenizer plus `WhisperFeatureExtractor`, and an `AudioDecoder` from `config.yaml`/`flow.pt`/`hift.pt`. Shared `generate_conditional_interleaved_speech_token_only(self, input_audio_path, temperature, top_p, output_dir, assistant_audio_name="assistant.wav", stereo_audio_name="stereo_user_left_assistant_right.wav")` (`turnguide_inference.py:163-178`, `turnguide_inference_reproducible.py:128-143`) skips when both outputs exist (`"exist"`), tokenizes user audio via `extract_speech_token`, rejects token `16383` (`"unsupported_token"`), drops a short trailing user chunk, seeds `<|begin_of_audio|><|begin_of_audio|>`, and per 5-token user chunk appends `<|reserved_151347|>` + `<|audio_id|>`s + `<|reserved_151348|>` before generating one assistant chunk.
Divergence: `turnguide_inference.py` enforces chunk shape with `AssistantChunkGrammarProcessor(prompt_len, audio_offset, vocab_size, pad_token_id=None, chunk_size=5)` and `AssistantChunkStoppingCriteria(prompt_len, audio_offset, chunk_size=5)`, calling `generate(max_new_tokens=chunk_size * 2 + 1, ...)` and dumping failures to `./error_input_ids/error_<timestamp>.pt` with status `"sampling_error"` (`turnguide_inference.py:54-114`, `turnguide_inference.py:229-261`); the reproducible variant loops `generate(max_new_tokens=chunk_size, ..., eos_token_id=[end_of_audio_offset, 151347, 151348])` until `check_speech_token_num(token_sequence, audio_offset)` returns `True`, appends `151349` when a chunk is all text tokens, asserts `new_token >= audio_offset` before subtracting `audio_offset`, and reports `"while_true_generation_error"` (`turnguide_inference_reproducible.py:51-78`, `turnguide_inference_reproducible.py:209-247`).

## Truncation note
The chunk truncates `turnguide_inference.py` after ~269 of 454 lines (`... (truncated, 9157 more characters)`) and `turnguide_inference_reproducible.py` after ~264 of 435 lines (`... (truncated, 8499 more characters)`); decoding-to-wav, stereo mixing, and CLI/`main()` tails are therefore not described above.

**Covers:** `.gitattributes`, `.gitignore`, `environment.yml`, `requirements.txt`, `flow_inference.py`, `turnguide_inference.py` (partial, truncated), `turnguide_inference_reproducible.py` (partial, truncated)
