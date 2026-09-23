# Technical Analysis: OpenMOSS/MOSS-TTS

**Repository:** https://github.com/OpenMOSS/MOSS-TTS
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Single-model TTS fails when one audio artifact must simultaneously sound like a real person, pronounce every word accurately, switch speaking styles across content, remain stable over tens of minutes, and support dialogue, role-play, and real-time interaction (README.md:151). MOSS-TTS answers by splitting the workload into five production-ready models usable independently (README.md:151, sentence truncated in source).

The repo addresses this as the MOSS-TTS Family: an open-source speech and sound generation model family from MOSI.AI and the OpenMOSS team for high-fidelity, high-expressiveness, complex real-world scenarios, covering stable long-form speech, multi-speaker dialogue, voice/character design, environmental sound effects, and real-time streaming TTS (README.md:47; README_zh.md:43). The Chinese landing page enumerates the five roles explicitly: flagship MOSS-TTS (zero-shot cloning, long-form, pinyin/phoneme/duration control, multilingual plus Chinese-English mix), MOSS-TTSD v1.0 (dialogue), MOSS-VoiceGenerator (reference-free voice design from style prompts), MOSS-TTS-Realtime (multi-turn context-aware streaming, 180 ms TTFB, 377 ms combined LLM-first-sentence plus TTS latency), MOSS-SoundEffect (controllable-duration SFX for film, game, interaction, data use) (README_zh.md:149-155).

The primary user is an application builder assembling speech or sound features (narration, podcast/dubbing, voice agents, voice design, SFX) who picks a starting model from the task-chooser table rather than training a base model (README.md:54-60; README_zh.md:50-56).

## 2. High-Level Architecture

```
User task ─► Task chooser ─┬─► MOSS-TTS-Nano ──────────► CPU / browser output
                           ├─► MOSS-TTS-v1.5 / Local-Transformer-v1.5 ─► long-form narration
                           ├─► MOSS-TTSD ──────────────► dialogue / podcast / dubbing
                           ├─► MOSS-TTS-Realtime ──────► streaming speech
                           └─► Released models / SoundEffect-v2 ───────► voice design / SFX
                                │
                                ▼
                    Serving backends ─► SGLang-Omni ─► OpenAI-compatible /v1/audio/speech
                                     ─► vLLM-Omni
                                     ─► llama.cpp (torch-free GGUF/ONNX)
                                │
                                ▼
                    Persistent state: Hugging Face weight collection +
                                      moss_audio_tokenizer submodule +
                                      local weights/ + outputs/* (both git-ignored)
```

Data-flow narrative, as attested:

1. The builder classifies the task and follows the chooser row to one entry point: Nano for CPU/browser cloning, v1.5 or Local Transformer v1.5 for multilingual long-form, TTSD for dialogue/podcasts/dubbing, Realtime (`moss_tts_realtime/README.md`) for streaming, released models / SoundEffect v2 (`moss_soundeffect_v2/README.md`) for voice design and SFX (README.md:54-60; README_zh.md:50-56).
2. Weights are fetched from the Hugging Face collection linked under "Start here" (README.md:50; README_zh.md:46); the audio codec arrives via the `moss_audio_tokenizer` submodule pointing at `https://github.com/OpenMOSS/MOSS-Audio-Tokenizer` (.gitmodules:1-3). Local `weights` and `outputs/*` directories are git-ignored and therefore not part of the checkout (.gitignore:213-216).
3. Synthesis runs on the selected model path: `MossTTSDelay` and `MossTTSLocal` act as complementary baselines (long-context stability/speed/engineering vs. lightweight streaming-oriented synthesis), while `MossTTSRealtime` conditions on history text plus user voice acoustics for incremental multi-turn output (README_zh.md:158-169).
4. For serving, Day-0 SGLang-Omni support exposes the `MossTTSLocal` architecture over an OpenAI-compatible `/v1/audio/speech` endpoint with streaming and voice cloning; vLLM-Omni covers the full series and a llama.cpp path provides torch-free inference (README.md:63-88; README_zh.md:58-82).
5. Samples, quickstart (Conda / `uv` / FlashAttention 2), fine-tuning, evaluation, and per-architecture READMEs sit behind the Contents index (README.md:96-142; README_zh.md:93-139); generated audio lands in `outputs/*` (ignored, not versioned).

Persistent state lives outside the repo checkout: model weights on Hugging Face, the separately cloned tokenizer submodule, and local `weights/` and `outputs/*` directories.

## 3. The Model Family (Core Abstraction)

The central concept is the model family: a fixed set of named, task-routed models plus a shared landing page, not a single checkpoint. Representation is tabular: a "What you want to build | Start with" chooser (README.md:54-60) mirrored in Chinese (README_zh.md:50-56).

Named kinds/types attested with file:line:

- `MOSS-TTS-Nano` — CPU/browser speech and voice cloning; separate repo `OpenMOSS/MOSS-TTS-Nano`, ~100M params (README.md:54-60; README.md:67-88).
- `MOSS-TTS-v1.5` / `MOSS-TTS-Local-Transformer-v1.5` — multilingual long-form narration and cloning; 4B `MossTTSLocal` checkpoint, Qwen3-1.7B → Qwen3-4B backbone, `MOSS-Audio-Tokenizer-v2`, native 48 kHz stereo (README.md:54-60; README.md:64).
- `MOSS-TTSD` — multi-speaker dialogue, podcasts, dubbing; separate repo `OpenMOSS/MOSS-TTSD` (README.md:54-60).
- `MOSS-TTS-Realtime` — real-time streaming speech; `moss_tts_realtime/README.md`, 180 ms TTFB design (README.md:54-60; README_zh.md:149-155).
- `MOSS-SoundEffect v2` / released models — voice design and environmental SFX; `moss_soundeffect_v2/README.md`, DiT plus Flow Matching, 48 kHz, up to 30 s (README.md:54-60; README.md:67-88).
- `MOSS-Audio-Tokenizer-v2` — shared discrete audio interface, 48 kHz stereo input/output (README.md:65).
- Architecture types `MossTTSDelay` / `MossTTSLocal` / `MossTTSRealtime`, each with a per-architecture README link and a distinct core mechanism (README_zh.md:158-169).

Key query pattern: the chooser is itself the query interface — match the task row, follow the link. Verbatim (README.md:54-60):

```
| What you want to build | Start with |
| --- | --- |
| Speech and voice cloning on a CPU or in a browser | [MOSS-TTS-Nano](https://github.com/OpenMOSS/MOSS-TTS-Nano) |
| Multilingual long-form narration and voice cloning | [MOSS-TTS-v1.5](#moss-tts-v15) · [Local Transformer v1.5](#moss-tts-local-transformer-v15) |
| Multi-speaker dialogue, podcasts, and dubbing | [MOSS-TTSD](https://github.com/OpenMOSS/MOSS-TTSD) |
| Real-time streaming speech | [MOSS-TTS-Realtime](moss_tts_realtime/README.md) |
| Voice design or environmental sound effects | [Released models](#released-models) · [MOSS-SoundEffect v2](moss_soundeffect_v2/README.md) |
```

## 4. LLM / External Service Integration

The repo embeds LLM backbones as model weights; it calls no third-party LLM API at synthesis time in the attested material. The one named backbone is Qwen3: Local-Transformer-v1.5 moves the backbone from Qwen3-1.7B to Qwen3-4B (README.md:64). Serving integrations are inference backends, not model providers: SGLang-Omni (Day-0 support for `MossTTSLocal`, OpenAI-compatible `/v1/audio/speech`, streaming, voice cloning), vLLM-Omni (full-series support for `MossTTSDelay`, `MossTTSRealtime`, `MossTTSNano`), and a llama.cpp backend with GGUF/ONNX torch-free inference (README.md:63-88). Weight distribution runs through the Hugging Face collection `OpenMOSS-Team/moss-tts` (README.md:50). No required or optional remote API calls and no environment variables are attested in the available wiki pages; the Quickstart's Conda / `uv` / FlashAttention 2 setup, fine-tuning guides, and backend configuration live beyond the truncated chunk boundary (README.md:96-142; 01-overview.md:42).

## 5. Task-Routed Synthesis Pipeline

The primary workflow is task classification followed by model-specific synthesis and backend serving. No function-level signatures are attested in the available pages; steps below cite the document location for each.

1. Classify the build goal against the five chooser rows (CPU/browser cloning, multilingual long-form, dialogue/podcast/dubbing, streaming, voice design/SFX) (README.md:54-60; README_zh.md:50-56).
2. Fetch artifacts: model weights from the Hugging Face collection (README.md:50) and the codec via the `moss_audio_tokenizer` submodule (`.gitmodules:1-3`); confirm `weights` and `outputs/*` exist locally since both are ignored (.gitignore:213-216).
3. Select the architecture mechanism: multi-head parallel RVQ prediction with delay-pattern scheduling (`MossTTSDelay`, long-context stability/speed), time-synchronous RVQ blocks over a depth Transformer (`MossTTSLocal`, lightweight/streaming), or hierarchical text-audio input over history text plus user acoustics (`MossTTSRealtime`, incremental multi-turn) (README_zh.md:158-169).
4. Apply generation controls where supported: language tags and inline `[pause X.Ys]` markers on TTS-v1.5 (README.md:67-88); pinyin/phoneme/duration control and Chinese-English mixing on the flagship TTS; style-prompt conditioning on VoiceGenerator; controllable duration on SoundEffect (README_zh.md:149-155).
5. Serve or export: SGLang-Omni `/v1/audio/speech` for `MossTTSLocal` (README.md:63), vLLM-Omni for the full series (README.md:67-88), or the llama.cpp torch-free path with GGUF/ONNX weights (README.md:67-88); verify against the samples demo video and the Evaluation section (README.md:92-142).

## 6. Key Files

| File | Lines | What It Does |
| --- | --- | --- |
| README.md | family definition :47; entry links :50; chooser :54-60; news :63-88; demo :92-94; contents index :96-142; introduction opening :151 | Landing page: family definition, task routing, releases, entry points, section index |
| README_zh.md | toggle :40; family :43; entries :46; chooser :50-56; news :58-82; contents :93-139; five-model intro :149-155; architecture table :158-169; cut at :179 | Chinese mirror of the landing page with five-model and architecture detail |
| .gitignore | 1-216; project entries 213-216 | Standard Python ignores plus `weights` and `outputs/*` excludes |
| .gitmodules | 1-3 | Declares the single `moss_audio_tokenizer` submodule and its URL |
| MANIFEST.in | 1-22 | sdist allowlist: includes READMEs/LICENSE/pyproject, grafts assets/docs/package dirs, prunes VCS/IDE dirs, excludes bytecode/artifacts |
| moss_audio_tokenizer/ (submodule) | attested via .gitmodules:1-3; grafted in MANIFEST.in | Shared audio codec dependency, cloned separately |
| moss_tts_delay/ (package dir) | attested via MANIFEST.in graft | Sources for the `MossTTSDelay` architecture path |
| moss_tts_local/ (package dir) | attested via MANIFEST.in graft | Sources for the `MossTTSLocal` architecture path |
| moss_tts_realtime/ (package dir) | attested via MANIFEST.in graft; README at moss_tts_realtime/README.md | Sources and docs for the realtime streaming path |
| moss_soundeffect_v2/README.md | attested via chooser (README.md:54-60) | Docs for the SoundEffect v2 voice-design/SFX path |
| docs/ | attested via MANIFEST.in graft | Shipped documentation directory |
| assets/ | attested via MANIFEST.in graft | Shipped static assets (demo media) |
| pyproject.toml | attested via MANIFEST.in include | Build metadata; dependency contents not quoted in wiki pages |
| weights/ (ignored dir) | .gitignore:213-216 | Local weight storage, never committed |
| outputs/* (ignored path) | .gitignore:213-216 | Generation output location, never committed |

## 7. Dependencies

No package dependency with an exact version constraint string is quoted in the available wiki pages; `pyproject.toml` is only attested as included in the sdist (MANIFEST.in:1-22), and the Conda / `uv` / FlashAttention 2 quickstart contents sit beyond the chunk boundary (README.md:96-142). The table below lists only runtime components attested by name, with versions marked accordingly.

| Package | Version constraint | Purpose |
| --- | --- | --- |
| MOSS-Audio-Tokenizer-v2 (via moss_audio_tokenizer submodule) | unknown (submodule URL only, .gitmodules:1-3; 48 kHz stereo per README.md:65) | Discrete audio codec for tokenize/detokenize |
| Qwen3-1.7B / Qwen3-4B backbone | unknown (named as Local-Transformer-v1.5 backbone, README.md:64) | Language-model backbone for the Local path |
| SGLang-Omni | unknown (Day-0 support, README.md:63) | Production serving with OpenAI-compatible streaming endpoint |
| vLLM-Omni | unknown (full-series support, README.md:67-88) | High-throughput serving backend |
| llama.cpp + ONNX weights path | unknown (GGUF/ONNX torch-free inference, README.md:67-88) | CPU/torch-free inference backend |
| FlashAttention 2 | unknown (quickstart prerequisite, README.md:96-142) | Accelerated attention for training/inference setup |
| Hugging Face collection OpenMOSS-Team/moss-tts | unknown (README.md:50) | Weight distribution channel |

## 8. CLI / Usage Surface

Entry points attested (no verbatim shell commands are quoted in the available pages; quickstart command bodies are beyond the truncation point):

- Quickstart (Conda / `uv` / FlashAttention 2) — standard local setup path (README.md:96-142).
- Hugging Face weight collection — model download entry (README.md:50; README_zh.md:46).
- Samples demo (embedded `<video>`) — listening entry before use (README.md:92-94).
- Fine-tuning guides — per-model adaptation entry (README.md:96-142).
- `moss_tts_realtime/README.md` — realtime streaming entry (README.md:54-60).
- `moss_soundeffect_v2/README.md` — voice-design/SFX entry (README.md:54-60).
- SGLang-Omni OpenAI-compatible `/v1/audio/speech` endpoint — serving entry with streaming and voice cloning (README.md:63).
- vLLM-Omni backend — full-series serving entry (README.md:67-88).
- llama.cpp backend with `configs/llama_cpp/`-style profiles — torch-free inference entry (per collapsed news block, exact config filenames not quoted in these two wiki pages).

| Config / Env | Source | Notes |
| --- | --- | --- |
| `weights` directory | .gitignore:213-216 | Expected local weight location; ignored by git, must be populated by download |
| `outputs/*` path | .gitignore:213-216 | Generation output location; ignored by git |
| `moss_audio_tokenizer` submodule | .gitmodules:1-3 | Must be initialized (`git submodule update --init` semantics; command itself not quoted in pages) |
| Environment variables | none attested | No env vars are quoted in the available pages |
| `[pause X.Ys]` inline marker | README.md:67-88 | In-text duration control for TTS-v1.5 |
| Language-tag selection | README.md:67-88 | Language-tag control for TTS-v1.5 |

## 9. Extensibility Points

- New synthesis capability or model variant → follow the family pattern: add a per-architecture directory and README alongside `moss_tts_delay/`, `moss_tts_local/`, `moss_tts_realtime/` (all grafted in MANIFEST.in:1-22) and add a chooser row in README.md:54-60.
- New audio codec behavior → extend the `moss_audio_tokenizer` submodule (`.gitmodules:1-3`), not the landing repo; v2 precedent is 48 kHz stereo I/O (README.md:65).
- New serving backend or endpoint shape → mirror the SGLang-Omni (`/v1/audio/speech`, streaming, cloning) or vLLM-Omni integration notes in the News/backends sections (README.md:63-88).
- New language or voice-control behavior → extend the TTS-v1.5 language-tag and `[pause X.Ys]` mechanism (README.md:67-88) and the flagship pinyin/phoneme/duration controls (README_zh.md:149-155).
- New packaged content → update MANIFEST.in graft/prune lists (MANIFEST.in:1-22) and the Contents index (README.md:96-142).

## 10. Limitations and Gotchas

- **Source truncation bounds every claim:** README.md coverage stops mid-sentence at the Introduction (`README.md:151`); architecture, released-models, languages, quickstart, fine-tuning, backends, and evaluation sections are outside the chunk (01-overview.md:42). README_zh.md is cut at line 179 with 32118 further characters missing (02-top-level-files.md:84).
- **`weights` and `outputs/*` are invisible to git:** both are ignored (.gitignore:213-216), so a fresh clone synthesizes nothing until weights are fetched from Hugging Face and the output directory is created; generated audio is never versioned.
- **The codec is a submodule, not a directory:** `moss_audio_tokenizer` points at a separate GitHub repo (.gitmodules:1-3) and must be initialized separately; MANIFEST.in grafts it for the sdist but that does not populate a git checkout.
- **Two flagship paths live in other repositories:** Nano and TTSD resolve to `OpenMOSS/MOSS-TTS-Nano` and `OpenMOSS/MOSS-TTSD` (README.md:54-60), so issues, versions, and docs for those tasks are not in this checkout.
- **Backend support is version-coupled:** SGLang-Omni Day-0 support targets a dated Local-Transformer-v1.5 release (2026.6.18, README.md:63-64), and earlier vLLM-Omni / GGUF / ONNX support is recorded per-release inside a collapsed block (README.md:67-88) — pin backend and checkpoint dates together.

## 11. How It Compares to Alternatives

- **MOSS-TTS-Nano** (separate repo `OpenMOSS/MOSS-TTS-Nano`, ~100M params): the CPU/browser cloning specialist; choose it when the constraint is local realtime inference rather than maximum fidelity long-form (README.md:54-60; README.md:67-88).
- **MOSS-TTSD** (separate repo `OpenMOSS/MOSS-TTSD`): the multi-speaker dialogue/podcast/dubbing specialist; choose it when the artifact is conversational with speaker turns rather than single-voice narration (README.md:54-60).
- **MOSS-Audio-Tokenizer** (separate repo, `moss_audio_tokenizer` submodule, v2 with 48 kHz stereo): the shared codec layer; it is a dependency, not a synthesis competitor, and determines the ceiling on output bandwidth (`.gitmodules:1-3`; README.md:65).
- **MOSS-SoundEffect v2** (`moss_soundeffect_v2/README.md`, DiT plus Flow Matching, up to 30 s at 48 kHz): the non-speech SFX path for film/game/interaction; choose it when the output is environmental sound rather than speech (README.md:54-60; README.md:67-88).

Positioning: this repository is the family hub and router — it defines the task map, publishes dated releases, and documents the serving backends (SGLang-Omni, vLLM-Omni, llama.cpp), while the heavy synthesis logic is partitioned across the routed model paths and sibling repos.

## Appendix: Selected Code Snippets

1. Task-chooser table, README.md:54-60:

```
| What you want to build | Start with |
| --- | --- |
| Speech and voice cloning on a CPU or in a browser | [MOSS-TTS-Nano](https://github.com/OpenMOSS/MOSS-TTS-Nano) |
| Multilingual long-form narration and voice cloning | [MOSS-TTS-v1.5](#moss-tts-v15) · [Local Transformer v1.5](#moss-tts-local-transformer-v15) |
| Multi-speaker dialogue, podcasts, and dubbing | [MOSS-TTSD](https://github.com/OpenMOSS/MOSS-TTSD) |
| Real-time streaming speech | [MOSS-TTS-Realtime](moss_tts_realtime/README.md) |
| Voice design or environmental sound effects | [Released models](#released-models) · [MOSS-SoundEffect v2](moss_soundeffect_v2/README.md) |
```

2. Submodule declaration, .gitmodules:1-3:

```
[submodule "moss_audio_tokenizer"]
	path = moss_audio_tokenizer
	url = https://github.com/OpenMOSS/MOSS-Audio-Tokenizer
```

3. Packaging allowlist, MANIFEST.in:1-22:

```
include README.md
include README_zh.md
include LICENSE
include pyproject.toml

graft assets
graft docs
graft moss_tts_delay
graft moss_tts_local
graft moss_tts_realtime
graft moss_audio_tokenizer

prune .git
prune .github
prune .vscode
prune moss_tts.egg-info

global-exclude __pycache__
global-exclude __pycache__/*
global-exclude *.py[cod]
global-exclude .DS_Store
global-exclude *.so
```

4. Git-ignored runtime state, .gitignore:213-216:

```
# Weights
weights

outputs/*
```
