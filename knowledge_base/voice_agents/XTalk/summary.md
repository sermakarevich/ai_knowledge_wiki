# Technical Analysis: xcc-zach/xtalk

**Repository:** https://github.com/xcc-zach/xtalk
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

> Coverage note: at analysis time `wiki/` contains two component pages — `01-overview.md` (repo README: features, demo, install, quickstart) and `02-top-level-files.md` (repo hygiene/toolchain/docs config). No pipeline source files, manifests, or dependency lockfiles are covered by any component page, so per-function `file.py:line` references, exact runtime version pins, and internal module structure are reported as unknown rather than inferred.

## 1. Overview

Spoken-dialogue prototypes typically behave as half-duplex systems: the user waits for the system to finish, tolerates multi-second latency, and loses paralinguistic signal (interruptions, background noise, emotion, multi-speaker overlap). Researchers who want to improve this face codebases that are hard to install, hard to extend with a new model, and hard to deploy beyond a local script; production use additionally demands concurrency and browser-to-edge serving.

X-Talk addresses this with a full-duplex cascaded spoken-dialogue framework: a modular ASR → LLM-agent → TTS pipeline engineered for low-latency, user-interruptible speech flow with parallel paralinguistic encoding (environment noise, emotion) (01-overview.md:20-24). The primary user is the dialogue/speech researcher-experimenter who wants to add a model or dialogue logic in one Python script and run it through the default pipeline (01-overview.md:25-26), with a secondary path to production via an asynchronous backend and WebSocket-based serving from browsers to edge devices (01-overview.md:29-31). Distribution is pure Python, installed with `pip install` and nothing to build (01-overview.md:27-28). The documented reference deployment runs on a 4090 cluster with 8-bit quantized SenseVoice (ASR), IndexTTS 1.5 (TTS), and 4-bit quantized Qwen3-30B-A3B (LLM) (01-overview.md:47-50). The project warns it is in active prototyping and interfaces are subject to change (01-overview.md:18).

## 2. High-Level Architecture

```
 Browser / edge client
        │  WebSocket (full-duplex audio + events)
        ▼
 Async Python server (examples/sample_app/configurable_server.py)
        │
        ├──► ASR stage  (e.g. Qwen3ASRFlashRealtime / SenseVoice)
        │         │
        │         ▼
        ├──► LLM-agent stage (e.g. DefaultAgent over qwen-plus-2025-12-01)
        │         │
        │         ▼
        └──► TTS stage (e.g. CosyVoice / IndexTTS 1.5)
                  │
                  ▼
         WebSocket audio back to client (interruptible playback)
```

Data-flow narrative (all stage identities from 01-overview.md:47-50, 01-overview.md:57-90):

1. The client opens a WebSocket session against the async Python server started by `examples/sample_app/configurable_server.py --port 7635 --config <config>.json` (01-overview.md:154-161). The framework's production-readiness claim rests on this async backend plus WebSocket transport (01-overview.md:29-31).
2. Streaming user audio enters the ASR stage (reference: SenseVoice 8-bit; quickstart: `Qwen3ASRFlashRealtime`) and is converted to text plus paralinguistic side-signals (noise, emotion) encoded in parallel (01-overview.md:21-24, 01-overview.md:47-50).
3. Text (and side-signals) pass to the LLM-agent stage (reference: Qwen3-30B-A3B 4-bit; quickstart: `DefaultAgent` on `qwen-plus-2025-12-01` via the DashScope compatible-mode endpoint), which produces the response turn (01-overview.md:47-50, 01-overview.md:65-74).
4. Response text enters the TTS stage (reference: IndexTTS 1.5; quickstart: `CosyVoice`), which synthesizes speech streamed back over the WebSocket (01-overview.md:47-50, 01-overview.md:75-81).
5. The speech flow supports natural user interruption: the user can cut in while the system is speaking rather than waiting for playback to finish (01-overview.md:21-24). Internal barge-in signalling is not covered by any component page, so the mechanism is unknown.
6. Tour-guiding demos substitute `Qwen3-Next-80B-A3B-Instruct` as the language model; all other demos match the online configuration, documenting an explicit latency-vs-intelligence trade-off (01-overview.md:98).

Persistent state: no database or dialogue-store schema is described in the available pages. The only state-like artifacts attested are the JSON model config file supplied via `--config` (01-overview.md:125-159), the ignored-at-runtime directories `/logs/`, `server_configs/`, and `/data/` (02-top-level-files.md:26-46), and Gradio/asset caches (`asset/`, `.gradio/`) (02-top-level-files.md:26-46). Conversation-history persistence, if any, is unknown.

## 3. The Cascaded Dialogue Stage

The central concept is the **cascaded full-duplex dialogue stage**: each of ASR, LLM agent, and TTS is a named, single-script-swappable component wired into one default pipeline (01-overview.md:25-26). Representation is a JSON service config mapping each pipeline slot to a `type` plus `params` (01-overview.md:125-152). Named kinds attested in the quickstart config (01-overview.md:84-90):

- `asr.type = "Qwen3ASRFlashRealtime"`, params: `api_key` (01-overview.md:59-64).
- `llm_agent.type = "DefaultAgent"`, params: `model.api_key`, `model.model`, `model.base_url` (01-overview.md:65-74).
- `tts.type = "CosyVoice"`, params: `api_key` (01-overview.md:75-81).
- Reference-deployment kinds: SenseVoice (ASR, 8-bit), IndexTTS 1.5 (TTS), Qwen3-30B-A3B (LLM, 4-bit), Qwen3-Next-80B-A3B-Instruct (tour-guide LLM) (01-overview.md:47-50, 01-overview.md:98).

Key query over the abstraction — "which models back each stage" — is answered by reading the config sections, verbatim (01-overview.md:57-82):

```json
{
    "asr": {
        "type": "Qwen3ASRFlashRealtime",
        "params": {
            "api_key": "<API_KEY>"
        }
    },
    "llm_agent": {
        "type": "DefaultAgent",
        "params": {
            "model": {
                "api_key": "<API_KEY>",
                "model": "qwen-plus-2025-12-01",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
            }
        }
    },
    "tts": {
        "type": "CosyVoice",
        "params": {
            "api_key": "<API_KEY>"
        }
    }
}
```

Component class definitions, registration decorators, and per-stage Python APIs are not covered by any component page; no `file.py:line` for the stage base class can be given.

## 4. LLM / External Service Integration

The repo calls external model APIs; there is no local-only path documented in the available pages.

- Providers: AliCloud Bailian Platform (API key source; free-tier at time of writing) for the quickstart ASR/LLM/TTS path (01-overview.md:121-123); DashScope OpenAI-compatible endpoint `https://dashscope.aliyuncs.com/compatible-mode/v1` as the LLM `base_url` (01-overview.md:65-74); locally deployed models named as alternatives for SenseVoice / IndexTTS 1.5 / Qwen3-30B-A3B on a 4090 cluster (01-overview.md:47-50).
- Required calls: one ASR transcription call per turn (`Qwen3ASRFlashRealtime`), one LLM-agent call per turn (`DefaultAgent` → `qwen-plus-2025-12-01`), one TTS synthesis call per turn (`CosyVoice`) — all three sections are present in the minimal config (01-overview.md:57-82).
- Optional calls: none documented in the available pages; tool-use / web-search capabilities are hinted only by docs-nav entries (`LLM agent`, `tools`, `web search` in the mkdocs nav tree) without endpoint detail (02-top-level-files.md:137).
- Credentials: a single `<API_KEY>` placeholder fills `asr.params.api_key`, `llm_agent.params.model.api_key`, and `tts.params.api_key` (01-overview.md:55, 01-overview.md:57-82). No environment-variable names (e.g. `DASHSCOPE_API_KEY`-style) are stated in any component page; secrets travel in the JSON config file, not env vars, as far as the covered material shows.

## 5. The Configure-and-Serve Pipeline

Primary workflow: pick hosted or local models, write a JSON config, launch the sample server, open the browser demo. No per-function `file.py:line` is available (no pipeline source is covered by any component page); steps below cite the attested user-visible operations.

1. Install the framework — verbatim (01-overview.md:41-43): `pip install git+https://github.com/xcc-zach/xtalk.git@main`. This is the only install path attested for the base package.
2. Install the AliCloud/example extras — verbatim (01-overview.md:47-51): `pip install "xtalk[ali,example] @ git+https://github.com/xcc-zach/xtalk.git@main"`.
3. Obtain an API key from the AliCloud Bailian Platform (01-overview.md:121-123). The pages note the hosted service may be unstable with high latency and recommend locally deployed models instead (01-overview.md:121-123).
4. Write the JSON config mapping `asr` / `llm_agent` / `tts` to `type` + `params` and substitute the key (01-overview.md:125-152; schema table at 01-overview.md:84-90).
5. Clone and launch — verbatim (01-overview.md:94-98): `git clone https://github.com/xcc-zach/xtalk.git`, `cd xtalk`, `python examples/sample_app/configurable_server.py --port 7635 --config <PATH_TO_CONFIG>.json`. Flags: `--port 7635` selects the demo port; `--config` points at the JSON from step 4 (01-overview.md:100-105).
6. Open `http://localhost:7635` in the browser and converse, including interrupting the system mid-utterance (01-overview.md:107, 01-overview.md:21-24).

## 6. Key Files

Ordered by structural importance within the limits of the two covered pages. Only files/paths named in the component pages are listed; line counts are from the wiki citations, not independent measurement.

| File | Lines | What It Does |
|---|---|---|
| `README.md` | overview chunk (01-overview.md:18-172) | Sole runtime-facing doc covered: features, demo matrix, install, AliCloud quickstart |
| `examples/sample_app/configurable_server.py` | cited at 01-overview.md:94-98 | Config-driven demo server entry point (`--port`, `--config`) |
| `<PATH_TO_CONFIG>.json` (user-created) | schema at 01-overview.md:57-90 | Binds `asr` / `llm_agent` / `tts` types + params for the run |
| `mkdocs.yml` | 141 lines (02-top-level-files.md:123-138) | Docs-site definition: Material theme, en/zh i18n, nav for tutorials, technical reference, API |
| `docs/` (incl. `docs/requirements.txt`) | referenced at 02-top-level-files.md:74-98 | Published docs source; requirements installed by ReadTheDocs build |
| `AGENTS.md` | 28 lines (02-top-level-files.md:99-122) | Contribution rules: no self-commits, `feature:`/`docs:`/`refactor:`/`fix:`/`chore:` prefixes, bilingual docs, frontend/backend design constraints |
| `.pre-commit-config.yaml` | 14 lines (02-top-level-files.md:47-72) | Pins black / ruff / mypy hooks (see §7) |
| `.readthedocs.yaml` | 13 lines (02-top-level-files.md:74-98) | Docs build pin: Ubuntu 24.04, Python 3.13, `mkdocs.yml`, `docs/requirements.txt` |
| `.gitignore` | 188 lines (02-top-level-files.md:21-46) | Python-standard ignores plus `asset/`, `.gradio/`, `.vscode`, `examples/sample_server/node_modules/`, `/logs/`, `server_configs/`, `/data/` |
| `.gitattributes` | 1 line (02-top-level-files.md:13-20) | Routes `pysc/**` through Git LFS; everything else default handling |

No pipeline, model-wrapper, client, or test source files are covered by any component page and are therefore absent from this table.

## 7. Dependencies

Only pins stated verbatim in the component pages are listed. No runtime `pyproject`/`requirements` manifest is covered, so the runtime dependency set is unknown.

| Package | Version constraint | Purpose |
|---|---|---|
| `xtalk[ali,example]` (from git `@main`) | `git+https://github.com/xcc-zach/xtalk.git@main` (01-overview.md:47-51) | Quickstart install: AliCloud model integrations + example server |
| `xtalk` (base, from git) | `git+https://github.com/xcc-zach/xtalk.git@main` (01-overview.md:41-43) | Framework itself (pure-Python backend, 01-overview.md:27-28) |
| Python (docs build) | `"3.13"` on `ubuntu-24.04` (02-top-level-files.md:74-98) | ReadTheDocs build toolchain pin |
| `psf/black` (pre-commit hook) | `rev: 24.3.0`, `id: black` (02-top-level-files.md:47-72) | Formatting |
| `charliermarsh/ruff-pre-commit` (pre-commit hook) | `rev: v0.3.2`, `id: ruff` (02-top-level-files.md:47-72) | Linting |
| `pre-commit/mirrors-mypy` (pre-commit hook) | `rev: v1.9.0`, `id: mypy` (02-top-level-files.md:47-72) | Type checking |
| mkdocs stack (`material` theme, `i18n`, `pymdownx.*`) | versions unstated; requirements in `docs/requirements.txt` (02-top-level-files.md:74-98, 02-top-level-files.md:133-135) | Documentation site |

Runtime model/pipeline libraries (ASR/LLM/TTS clients, async/WebSocket server deps) are not enumerated in any component page and are omitted rather than guessed.

## 8. CLI / Usage Surface

Entry points attested in the covered pages:

| Entry point | Form | Effect |
|---|---|---|
| `examples/sample_app/configurable_server.py` | `python examples/sample_app/configurable_server.py --port 7635 --config <PATH>.json` (01-overview.md:94-98) | Starts the configurable demo server |
| Browser demo | `http://localhost:7635` (01-overview.md:107) | Interactive voice-dialogue UI |
| Online demo | hosted link on a 4090 cluster (01-overview.md:47-50) | Pre-built demo with SenseVoice + IndexTTS 1.5 + Qwen3-30B-A3B |
| Docs site | `https://xtalk.readthedocs.io/` (01-overview.md:166-168) | Tutorials, technical reference, API reference |

Commands:

| Command | Purpose |
|---|---|
| `pip install git+https://github.com/xcc-zach/xtalk.git@main` (01-overview.md:41-43) | Base framework install |
| `pip install "xtalk[ali,example] @ git+https://github.com/xcc-zach/xtalk.git@main"` (01-overview.md:47-51) | Quickstart install with AliCloud + example extras |
| `git clone https://github.com/xcc-zach/xtalk.git && cd xtalk` (01-overview.md:94-98) | Fetch source for running the sample server |

Server flags:

| Flag | Meaning |
|---|---|
| `--port 7635` (01-overview.md:100-105) | Port the demo server listens on |
| `--config <PATH_TO_CONFIG>.json` (01-overview.md:100-105) | Path to the `asr`/`llm_agent`/`tts` JSON config |

Config keys:

| Section | `type` | `params` fields (01-overview.md:84-90) |
|---|---|---|
| `asr` | `Qwen3ASRFlashRealtime` | `api_key` |
| `llm_agent` | `DefaultAgent` | `model.api_key`, `model.model` (`qwen-plus-2025-12-01`), `model.base_url` |
| `tts` | `CosyVoice` | `api_key` |

Environment variables: no variable names are stated in any component page. The table is therefore empty by evidence: credentials are supplied as `<API_KEY>` inside the JSON config (01-overview.md:55-82), not via env vars, as far as the covered material shows.

## 9. Extensibility Points

- New model or dialogue logic: add it in one Python script and integrate with the default pipeline (01-overview.md:25-26). The exact base class / registration function is not covered by any component page — locate the stage-registration module under the pipeline source (uncovered) before writing the script.
- New pipeline configuration: author a JSON config with different `asr` / `llm_agent` / `tts` `type` values (pattern at 01-overview.md:57-90); launch via `examples/sample_app/configurable_server.py --config` (01-overview.md:94-98).
- New demo scenario: the README embeds ten scenarios (tour guiding EN/ZH, twenty questions, word-chain, web search, noisy, multi-speaker) as a video grid (01-overview.md:54-96) and the docs nav lists `customize_the_service`, `introduce_a_new_model`, `text input`, `voice wake`, `bot2bot`, and logging/testing recipes (02-top-level-files.md:137) — extend the sample app and the corresponding docs tutorial page.
- Docs and API surface: `mkdocs.yml` nav (02-top-level-files.md:137) plus `AGENTS.md` design rules — frontend platform code stays under `frontend/src/platforms` behind platform abstractions, NumPy-style backend docstrings and TypeDoc JSDoc frontend docstrings are required, direct attribute access is preferred, and `try/catch` is used sparingly (02-top-level-files.md:116-122); bilingual `*.zh.md` updates are required with doc changes (02-top-level-files.md:99-114).

## 10. Limitations and Gotchas

- **Hosted quickstart path is unstable and slow.** The pages state the AliCloud free-tier online service may be unstable with high latency and explicitly recommend locally deployed models (01-overview.md:121-123). Do not benchmark framework latency over the hosted path.
- **Active-prototyping interfaces.** Interfaces and functions are subject to change (01-overview.md:18), so code written against the current single-script extension pattern (01-overview.md:25-26) may break on update.
- **Documented intelligence-latency trade-off.** Tour-guide demos need the larger `Qwen3-Next-80B-A3B-Instruct` for smarter answers but pay higher latency; the other eight demos stay on the smaller online-demo stack (01-overview.md:98). Model choice, not pipeline tuning, is the attested lever.
- **Secrets live in a plaintext JSON file.** The quickstart puts `<API_KEY>` directly in the config's three sections (01-overview.md:57-82) with no env-var or secret-store pattern attested; the config path is one typo away from being committed, and `server_configs/` is git-ignored (02-top-level-files.md:26-46), suggesting the authors know this is fragile.
- **Evidence ceiling: internals are uncovered.** Interruption handling, paralinguistic encoding, concurrency structure, error handling, evaluation, and the full supported-model matrix are claimed or nav-listed (01-overview.md:21-31, 02-top-level-files.md:137) but no component page shows their code; treat all such claims as unverified until the pipeline sources are analyzed.

## 11. How It Compares to Alternatives

No head-to-head comparison is present in any component page; positioning below uses named external projects as context, not as wiki-attested claims.

- **LiveKit Agents (LiveKit).** Production-oriented real-time voice/video agent framework with mature transport, TURN, and telephony; X-Talk's attested edge is researcher friction (single-script model swap, pip-only install per 01-overview.md:25-28) while LiveKit's edge is production infrastructure X-Talk does not document.
- **Pipecat (Daily).** Open-source voice-agent orchestration with explicit pipeline processors, VAD/interruption services, and broad STT/LLM/TTS integrations; closest structural analogue to X-Talk's cascaded ASR → agent → TTS stages, differing mainly in ecosystem breadth and documented deployment tooling.
- **Vocode.** Turnkey voice-agent library (telephony, WebSocket, configurable pipeline) aimed at shipping voice apps quickly; X-Talk positions instead at speech-flow research (interruptibility, paralinguistic encoding per 01-overview.md:21-24) rather than telephony/out-of-box deployment.
- **Moshi (Kyutai) / native full-duplex speech models.** End-to-end full-duplex speech-to-speech models that internalize interruption instead of cascading modules; X-Talk bets the opposite way — keep the debuggable cascaded stack and engineer the flow around it — trading potential end-to-end latency/overlap quality for modularity and per-stage model choice.

Positioning: X-Talk is the lightweight, researcher-first cascaded option — easiest to install and extend for interruption-aware dialogue experiments — rather than the production-hardened transport (LiveKit), the integration-rich orchestrator (Pipecat), the fastest path to a phone bot (Vocode), or the end-to-end duplex model (Moshi).

## Appendix: Selected Code Snippets

1. Base install, verbatim (`README.md` via 01-overview.md:39-43):

```bash
pip install git+https://github.com/xcc-zach/xtalk.git@main
```

2. Quickstart install with extras, verbatim (`README.md` via 01-overview.md:47-51):

```bash
pip install "xtalk[ali,example] @ git+https://github.com/xcc-zach/xtalk.git@main"
```

3. Minimal service config binding all three pipeline stages, verbatim (`README.md` via 01-overview.md:57-82):

```json
{
    "asr": {
        "type": "Qwen3ASRFlashRealtime",
        "params": {
            "api_key": "<API_KEY>"
        }
    },
    "llm_agent": {
        "type": "DefaultAgent",
        "params": {
            "model": {
                "api_key": "<API_KEY>",
                "model": "qwen-plus-2025-12-01",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
            }
        }
    },
    "tts": {
        "type": "CosyVoice",
        "params": {
            "api_key": "<API_KEY>"
        }
    }
}
```

4. Server launch, verbatim (`README.md` via 01-overview.md:94-98):

```bash
git clone https://github.com/xcc-zach/xtalk.git
cd xtalk
python examples/sample_app/configurable_server.py  --port 7635 --config <PATH_TO_CONFIG>.json
```
