# Technical Analysis: hyzhang24/DuplexSLA

**Repository:** https://github.com/hyzhang24/DuplexSLA
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Full-duplex spoken dialogue systems must listen and speak simultaneously while also deciding when to yield, interrupt, or acknowledge, and when to plan and invoke tools. Existing duplex backbones provide coupled audio streams but lack a native channel for in-conversation planning and tool calling, forcing turn-taking onto an external semantic VAD and tool use onto a turn boundary that halts speech (README.md:38, README.md:48, README.md:50).

DuplexSLA addresses this with a dual-stream three-channel formulation decoded jointly on a shared 160 ms chunk timeline: continuous user audio plus discrete assistant speech plus a rate-limited textual action stream (README.md:36, README.md:44). Turn-taking (`pause`, `interrupt`, `backchannel`) is emitted internally from semantic state, and planning text plus structured tool calls are emitted on the action channel without halting assistant audio, anchored to their own chunks in semantic order (README.md:48, README.md:50). The primary user is a speech-system researcher or dialogue engineer building interruptible voice agents that call tools mid-utterance. The analyzed snapshot is a release stub: technical report plus README; inference code, checkpoints, and DuplexSLA-Bench are announced as coming soon (README.md:20, README.md:22, README.md:23, README.md:56).

## 2. High-Level Architecture

```
User Audio (continuous features, 80 ms stride) ──────────────────┐
                                                                │
                                                                ▼
                                         ┌─────────────────────────────────┐
                                         │ Single Backbone (Step-Audio-2-  │
                                         │ mini ~7B + CPT / post-training) │
                                         └─────────────────────────────────┘
                                                                │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
                    ▼                       ▼                       ▼
  Assistant Audio Channel   Action Channel (text,       Internal Turn-Taking
  (discrete TA4: 1 text     ≤10 tokens / chunk):        Decisions:
  anchor + 4 audio tokens,  delayed transcripts │       pause │ interrupt │
  40 ms stride per chunk)   planning text │ control    backchannel
                            labels │ structured
                            tool calls
```

Data-flow narrative:

1. User audio is ingested as continuous features at 80 ms stride into the joint decoder context (README.md:40).
2. Each 160 ms chunk, the single backbone jointly decodes the assistant audio channel in TA4 layout (1 text anchor + 4 audio tokens at 40 ms stride) and the action channel at ≤10 tokens per chunk (README.md:41, README.md:42, README.md:44).
3. Semantic state inside the backbone produces turn-taking decisions (`pause`, `interrupt`, `backchannel`) directly, with no external semantic VAD in the loop (README.md:48).
4. Planning fragments, delayed transcripts, interaction-control labels, and structured tool calls are serialized onto the action channel, each tool call anchored to its own chunk and ordered semantically along the request, including multi-action and backchannel-triggered sequences interleaved with ongoing speech (README.md:42, README.md:50).
5. The reference figure `assets/architecture.png` documents this chunk-level layout (README.md:32); evaluation of the same behaviors is assigned to the pending DuplexSLA-Bench harness (README.md:52).

Persistent state lives nowhere in this snapshot: the repository contains no database, cache, checkpoint, or server state. The only persistent artefacts are the technical report (`DuplexSLA.pdf`), the architecture figure (`assets/architecture.png`), and version-control hygiene (`.gitignore` excludes weights `*.pt`, `*.pth`, `*.bin`, `*.safetensors`, `*.ckpt` as Hugging Face-hosted, `.gitignore:54`–`.gitignore:58`). Model weights and runtime state are explicitly out of the checkout.

## 3. The Dual-Stream Three-Channel Chunk

Representation: the conversational clock is a fixed 160 ms chunk. Within one chunk the model reads user features (2 frames at 80 ms stride), writes one TA4 assistant-audio group (1 text anchor + 4 audio tokens at 40 ms stride), and writes up to 10 action-channel text tokens (README.md:36, README.md:40, README.md:41, README.md:42, README.md:44).

Named kinds/types with citations:

- User audio channel — continuous user audio features, 80 ms stride (README.md:40).
- Assistant audio channel — discrete speech tokens, TA4 layout (README.md:41).
- Action channel — delayed transcripts, planning text, interaction-control labels, structured tool calls, ≤10 tokens per chunk (README.md:42).
- Turn-taking labels — `pause`, `interrupt`, `backchannel`, emitted from internal semantic state (README.md:48).
- Tool-call styles — single-action, multi-action, backchannel-triggered tool calls (README.md:50, README.md:52).
- Backbone — Step-Audio-2-mini (~7B parameters), continued pretraining plus post-training on duplex dialogue, turn-taking, and tool-call data (README.md:44).

Key queries (verbatim snippets from the wiki component pages):

```
User audio channel carries continuous user audio features at an 80 ms stride (README.md:40).
Assistant audio channel carries discrete assistant speech tokens in a TA4 layout — 1 text anchor + 4 audio tokens at 40 ms stride per chunk (README.md:41).
Action channel is a rate-limited textual stream carrying delayed transcripts, planning text, interaction-control labels, and structured tool calls at ≤10 tokens per chunk (README.md:42).
```

## 4. LLM / External Service Integration

The repository calls no LLM or external API. It is itself a foundation-model release (backbone initialised from Step-Audio-2-mini, ~7B parameters, adapted via continued pretraining and post-training) and ships no client code, server code, provider adapter, or API call site (README.md:44). There are no required calls, no optional calls, no provider keys, and no environment variables documented in the analyzed wiki pages. Planned (not present) artefacts are a Hugging Face checkpoint, a reference inference/streaming server, and the DuplexSLA-Bench harness (README.md:56, README.md:60, README.md:61, README.md:62).

## 5. The Joint Speech-Language-Action Decoding Workflow

This is the primary workflow: per-chunk joint decoding of assistant audio and action text conditioned on streaming user audio. The snapshot contains no source files and therefore no functions; every step below cites the README line via the wiki instead of a `file.py:line`, and the absence of callable functions is explicit.

1. Buffer one 160 ms chunk of dialogue time; accumulate user-audio features at 80 ms stride (README.md:36, README.md:40). No function exists in the snapshot.
2. Decode the assistant-audio TA4 group for the chunk: 1 text anchor followed by 4 discrete audio tokens at 40 ms stride (README.md:41). No function exists in the snapshot.
3. In the same chunk, decode up to 10 action-channel tokens: delayed transcript, planning text, control label, or structured tool-call fragment (README.md:42). No function exists in the snapshot.
4. Resolve semantic turn-taking from internal state and emit `pause`, `interrupt`, or `backchannel` without invoking an external VAD (README.md:48). No function exists in the snapshot.
5. Anchor each structured tool call to its own chunk, emit multi-action and backchannel-triggered sequences in semantic order, and continue assistant audio uninterrupted (README.md:50). No function exists in the snapshot.
6. Score the resulting behavior with DuplexSLA-Bench across turn-taking plus single-action, multi-action, and backchannel-triggered tool calling once the harness lands (README.md:52). No function exists in the snapshot.

## 6. Key Files

The snapshot contains five tracked artefacts plus the ignore policy; there is no source tree, so the table lists every known file rather than a 10–20 file selection.

| File | Lines | What It Does |
|---|---|---|
| README.md | cited to :79 | Sole technical document: formulation, chunk timing, highlights, release plan, citation, license pointer |
| DuplexSLA.pdf | n/a (binary report) | Technical report artefact, marked done in the open-source checklist (README.md:25) |
| LICENSE | n/a (license text) | MIT license grant for the project (README.md:79) |
| assets/architecture.png | n/a (figure) | Chunk-level architecture diagram at 92% width (README.md:32) |
| .gitignore | 58 | Excludes OS, Python, env, IDE, log, weight, and cache artefacts from version control |

Ignore-policy detail (`.gitignore` line groups from the wiki): macOS artefacts `.DS_Store`, `.AppleDouble`, `.LSOverride` (`.gitignore:9`–`.gitignore:11`); Python build artefacts `__pycache__/`, `*.py[cod]`, `*$py.class`, `*.so`, `build/`, `dist/`, `*.egg-info/`, `*.egg` (`.gitignore:15`–`.gitignore:34`); environments `.venv/`, `venv/`, `ENV/`, `env/` (`.gitignore:37`–`.gitignore:40`); IDE `.idea/`, `.vscode/`, `*.swp`, `*.swo` (`.gitignore:43`–`.gitignore:46`); Jupyter/logs/caches `.ipynb_checkpoints/`, `*.log`, `.cache/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/` (`.gitignore:49`–`.gitignore:65`); weights `*.pt`, `*.pth`, `*.bin`, `*.safetensors`, `*.ckpt` hosted on Hugging Face (`.gitignore:54`–`.gitignore:58`).

## 7. Dependencies

The repository declares no software dependencies: there is no manifest, requirements file, or lockfile in the analyzed wiki pages, and no import statements exist to constrain.

| Package | Version constraint | Purpose |
|---|---|---|
| (none declared) | n/a | No runtime, training, or evaluation packages are pinned in this snapshot |
| Step-Audio-2-mini weights (model, not package) | ~7B parameters, exact checkpoint unspecified | Initialization point for continued pretraining (README.md:44) |

## 8. CLI / Usage Surface

There is no CLI, entry point, server, or configuration surface in this snapshot. Inference code, deployment recipes, and checkpoints are explicitly not yet released (README.md:56).

| Surface | Status |
|---|---|
| Entry points | None |
| Commands | None |
| Environment variables | None documented |
| Config files / flags | None documented |

Planned usage surface, per the repo (README.md:60, README.md:61, README.md:62):

| Planned artefact | Purpose |
|---|---|
| Pretrained DuplexSLA checkpoint on Hugging Face | Model weights for inference and fine-tuning |
| Reference inference / streaming server | Chunk-level joint decoding runtime |
| DuplexSLA-Bench evaluation harness and data | Turn-taking and in-conversation tool-call scoring |

Open-source checklist verbatim (README.md:25, README.md:27, README.md:28): technical report (`DuplexSLA.pdf`) done (`[x]`); DuplexSLA-Bench evaluation code and data pending (`[ ]`).

## 9. Extensibility Points

No classes or modules exist to subclass in this snapshot, so extensibility is at the data-and-specification level until code lands:

- New turn-taking behavior — extend the `pause` / `interrupt` / `backchannel` label semantics and CPT/post-training dialogue mix described in README.md:44 and README.md:48; no handler file exists yet.
- New tool-call schema or multi-action ordering — extend the action-channel serialization (delayed transcripts, planning text, control labels, structured calls, ≤10 tokens/chunk) per README.md:42 and README.md:50; no parser/decoder file exists yet.
- New benchmark dimension — extend the DuplexSLA-Bench matrix (turn-taking plus single-action, multi-action, backchannel-triggered calls) per README.md:52; no harness file exists yet.
- New backbone or timing — replace the Step-Audio-2-mini initialization or the 160 ms / 80 ms / TA4-40 ms timing grid per README.md:44; no model-definition file exists yet.
- Repository hygiene — weight and cache exclusions already reserve large-artefact hosting on Hugging Face (`.gitignore:54`–`.gitignore:58`); a future contributor adds code without touching the ignore policy.

## 10. Limitations and Gotchas

- **No executable artefact:** inference code, checkpoints, and the bench harness are all pending (README.md:20, README.md:22, README.md:23, README.md:56), so no claim about latency, quality, or tool-use accuracy can be reproduced from this snapshot.
- **Fixed low-bandwidth action channel:** the ≤10 tokens per chunk cap (README.md:42) bounds how much planning text or tool-call JSON fits in one 160 ms window; long calls must fragment across chunks and any implementation must handle partial-JSON anchoring.
- **Fixed audio geometry:** TA4 (1 anchor + 4 tokens at 40 ms) and the 80 ms user stride (README.md:40, README.md:41) are baked into the formulation; changing frame rates or anchor ratios requires retraining, not a config flag.
- **Internalized turn-taking is unverifiable here:** `pause` / `interrupt` / `backchannel` from semantic state with no external VAD (README.md:48) cannot be inspected or ablated without the model and the pending bench data (README.md:52).
- **Weights excluded by policy:** `*.pt`, `*.pth`, `*.bin`, `*.safetensors`, `*.ckpt` are git-ignored as Hugging Face-hosted (`.gitignore:54`–`.gitignore:58`); cloning this repo alone never yields a runnable model.

## 11. How It Compares to Alternatives

- Step-Audio-2-mini: the stated initialization backbone (~7B) for DuplexSLA (README.md:44); DuplexSLA adds the third action channel and semantic turn-taking via continued pretraining rather than shipping the base model as-is.
- Kyutai Moshi: full-duplex speech-to-speech model with coupled user/assistant audio streams and interruption handling; DuplexSLA differs by adding a native rate-limited text action stream for planning and structured tool calls interleaved with speech.
- OpenAI GPT-4o Realtime API: server-VAD, interruption, and function-calling over a realtime audio/text channel; DuplexSLA differs by internalizing turn decisions and tool-call decoding into one jointly trained chunk timeline instead of orchestrating VAD plus discrete function-call round trips.
- Qwen2-Audio / Freeze-Omni class duplex extensions: audio-understanding models extended toward barge-in and duplex dialogue; DuplexSLA differs by formalizing the TA4 assistant layout plus the ≤10-token action channel and a dedicated bench covering multi-action and backchannel-triggered tool use.

Positioning: DuplexSLA occupies the narrow slot of natively joint speech-plus-action duplex modeling — simultaneous audio generation with in-utterance structured tool calling on a fixed chunk clock — whereas alternatives separate turn control (external VAD) or tool use (turn-boundary function calls) from the audio stream.

## Appendix: Selected Code Snippets

1. Channel timing configuration, `README.md:36`–`README.md:44` (via wiki 01-overview.md):

```
Shared chunk timeline: 160 ms; user stride 80 ms; assistant TA4 layout
(1 text anchor + 4 audio tokens, 40 ms stride per chunk);
action rate limit ≤10 tokens per chunk; backbone Step-Audio-2-mini
(~7B parameters) with CPT + post-training on duplex dialogue,
turn-taking, and tool-call data.
```

2. Citation block, `README.md:68`–`README.md:69` (via wiki 01-overview.md):

```bibtex
@article{zhang2026duplexsla,
  title   = {{DuplexSLA}: A Full-Duplex Spoken Language Model with Synchronized Speech, Language, and Action},
  author  = {Zhang, Haoyang and Chen, Jun and Wu, Donghang and Li, Yuxin and Zhang, Yuxin and Zhang, Xiangyu Tony and Liu, Che and Lin, Qingjian and Peng, Yizhou and Liu, Hexin and Chng, Eng Siong and Yan, Chao and Wu, Boyong and Huang, Yechang and Yang, Xuerui and Yu, Gang and Tian, Fei},
  journal = {arXiv preprint},
  year    = {2026}
}
```

3. Weight-exclusion policy, `.gitignore:54`–`.gitignore:58` (via wiki 02-top-level-files.md):

```
# Model weights / large artefacts (will be hosted on Hugging Face)
*.pt
*.pth
*.bin
*.safetensors
*.ckpt
```

4. OS-artefact exclusions, `.gitignore:9`–`.gitignore:11` (via wiki 02-top-level-files.md):

```
.DS_Store
.AppleDouble
.LSOverride
```
