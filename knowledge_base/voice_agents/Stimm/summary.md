# Technical Analysis: stimm-ai/stimm

**Repository:** https://github.com/stimm-ai/stimm
**Version analyzed:** 0.1.13 (Python package `.`; `@stimm/protocol` 0.1.3 per `.release-please-manifest.json:2-3`)
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Real-time voice products fail on perceived latency: waiting for a full retrieval, planning, and tool-call chain before speaking makes agents feel slow, while answering from a single fast model discards supervision and correctness. The primary user is the builder of speech-first products — customer-support voice agents, phone/SIP assistants, realtime copilots, embedded/kiosk experiences (README.md:70-73).

Stimm addresses this with an Optimistic VUI runtime built on `livekit-agents` (README.md:36-38): acknowledge early, speak early, keep the response interruptible and steerable, and let deeper reasoning continue in parallel (README.md:60-63). Concretely it pairs a low-latency `VAD -> STT -> fast LLM -> TTS` loop with pre-TTS buffering (README.md:46, README.md:79-84) and a dual-agent runtime where `VoiceAgent` owns the live turn and `Supervisor` watches the transcript, reasons asynchronously, and steers without blocking the first response (README.md:94-96, README.md:192-198). Onboarding is wizard-first: the catalog API displays providers and parameters, then extras are derived from the selection and installed as `stimm[...]` extras, never vendored in the wheel (README.md:50, README.md:114-115, README.md:174-184).

## 2. High-Level Architecture

```
User speech
    │
    ▼
VoiceAgent ──► VAD + STT ──► Fast LLM ──► Pre-TTS buffering ──► TTS ──► Spoken response
    │
    ▼
StimmProtocol (LiveKit data channels)
    │
    ▼
Supervisor ──► Reasoning, tools, planning ──► Steering instructions ──► VoiceAgent
```

Mermaid source for this flow is verbatim in README.md:77-92; the component roles are `VoiceAgent` (live turn-by-turn speech), `Supervisor` (watches transcript, steers asynchronously), `StimmProtocol` (structured messages over LiveKit data channels) per README.md:200-204.

Data-flow narrative:

1. User speech enters `VoiceAgent`, which runs VAD + STT to obtain transcript text (README.md:46, README.md:77-92).
2. The fast LLM produces tokens immediately; pre-TTS buffering holds them per level (`NONE`/`LOW`/`MEDIUM`/`HIGH`) before synthesis (README.md:79-84, README.md:212-217).
3. TTS renders the buffered text and the agent starts speaking as early as possible while staying interruptible (README.md:61-62).
4. In parallel, `Supervisor` observes transcript messages over `StimmProtocol` on LiveKit data channels and runs deeper reasoning, tools, and planning (README.md:94-96, README.md:197-198).
5. The supervisor returns steering instructions that modify the live turn; in `hybrid` (default) mode the first response is autonomous and steering applies after, in `relay` the agent speaks only supervisor instructions, in `autonomous` it acts independently (README.md:207-210).
6. Provider selection and install are out-of-band at onboarding time via the catalog API and extras install, followed by a process restart before plugin instantiation (README.md:176-188).

Persistent state: the wiki pages describe no database or on-disk store. Durable artifacts named are the generated provider catalog / provider metadata rebuilt by `scripts/dev_build.sh` (README.md:243-244), docs under `website` (README.md:248-253), and protocol artifacts rebuilt by the same script. App-side persistence per the integration contract stores only user choices and parameter values (AGENT.md:64-65), e.g. provider names plus `stt_params`/`tts_params`/`llm_params` (AGENT.md:67-76); provider module paths/constructors must never be stored (AGENT.md:20-21).

## 3. StimmProtocol: The Core Abstraction

The central concept is Optimistic VUI executed by two agents coordinated through a typed protocol. Representation in the wiki is at the README level: `VoiceAgent` optimized for low-latency spoken interaction (README.md:194), `Supervisor` optimized for deeper reasoning, planning, and tool orchestration (README.md:195), exchanging typed protocol messages over LiveKit data channels (README.md:197-198), with a typed protocol for Python and TypeScript supervisors (README.md:48).

Named kinds/types attested in the wiki pages:

- `VoiceAgent` — live turn owner (README.md:194, README.md:200-204)
- `Supervisor` / `StimmSupervisorClient` (TypeScript) — async reasoner/steerer (README.md:195, README.md:154-172)
- `StimmProtocol` — structured message layer (README.md:197-198)
- `TranscriptMessage` — transcript event with `text` and `partial` fields (README.md:141-151)
- Runtime modes `autonomous` / `relay` / `hybrid` (README.md:207-210)
- Buffering levels `NONE` / `LOW` / `MEDIUM` / `HIGH` (README.md:212-217)
- Catalog API surface: `get_provider_catalog()`, `extras_install_command(...)`, `required_extras_for_selection(...)`, `list_runtime_providers()` (discovery must not use the latter) (AGENT.md:13-21, README.md:176-177)

Key queries in the wiki are provider-catalog lookups and instruction calls, verbatim:

```python
from stimm import extras_install_command, get_provider_catalog
catalog = get_provider_catalog()
cmd = extras_install_command(stt="deepgram", tts="openai", llm="azure-openai")
print(cmd)  # pip install stimm[deepgram,openai]
```

(RREADME.md:176-184). Supervisor steering verbatim:

```python
from stimm import Supervisor, TranscriptMessage
class MySupervisor(Supervisor):
    async def on_transcript(self, msg: TranscriptMessage):
        if not msg.partial:
            result = await my_big_llm.process(msg.text)
            await self.instruct(result.text, speak=True)
```

(README.md:141-151).

## 4. LLM / External Service Integration

Providers are LiveKit plugins resolved in the integrator app environment, not vendored in the wheel (README.md:114-115). Attested providers in examples: `deepgram` (STT), `openai` (TTS, LLM), `azure-openai` (LLM), `silero` (VAD) (README.md:125-133, README.md:176-184). The runtime-safe provider contract and generated provider catalog derive from LiveKit docs (README.md:49); the catalog is the source of truth for wizard UIs (AGENT.md:14-15).

Required vs optional: the wiki draws no required/optional line among model calls. The fast LLM in the voice loop and STT/TTS/VAD are structural to the quick-start agent (README.md:125-133); the supervisor's "big LLM" (`my_big_llm.process`, `myAgent.process`) is integrator-supplied in examples (README.md:141-172). Local infra is provided via `docker compose up -d` (README.md:224-241), implying a LiveKit server dependency for data channels and WebRTC, but connection parameters are not recorded in the wiki pages.

Env vars: the wiki pages list no variable names. `.gitignore` excludes `.env` (.gitignore:1-5), and the integration contract forbids exposing secrets (API keys/tokens) in logs, telemetry, or UI snapshots (AGENT.md:20-21). No LLM provider names beyond the examples, no endpoints, and no key names are attested; treat all such detail as unknown from this source.

## 5. Optimistic Voice Loop: The Main Pipeline

Primary workflow is the optimistic turn with async supervision. Each step cites the function/symbol as named in the wiki; line-level implementation bodies are not in the wiki pages, so citations are to the documenting excerpt:

1. `VoiceAgent(...)` construction — `stt=deepgram.STT()`, `tts=openai.TTS()`, `vad=silero.VAD.load()`, `fast_llm=openai.LLM(model="gpt-4o-mini")`, `buffering_level="MEDIUM"`, `mode="hybrid"` (README.md:125-133).
2. `cli.run_app(WorkerOptions(entrypoint_fnc=agent.entrypoint))` — voice agent entrypoint serving the live turn (README.md:121-139).
3. VAD + STT transcription producing transcript events consumed as `TranscriptMessage` with `msg.partial` / `msg.text` (README.md:77-92, README.md:141-151).
4. Fast-LLM generation into pre-TTS buffering; level semantics `NONE` (immediate), `LOW` (word completion), `MEDIUM` (4 words or punctuation, default), `HIGH` (punctuation) (README.md:212-217); tradeoff statement at README.md:219-220.
5. TTS synthesis and spoken response, interruptible and steerable (README.md:61-62, README.md:79-84).
6. `Supervisor.on_transcript(msg)` — on non-partial messages, run background reasoning and call `self.instruct(result.text, speak=True)` (Python) or `client.instruct({ text, speak: true, priority: "normal" })` after `client.on("transcript", ...)` and `client.connect()` (TypeScript) (README.md:141-172).
7. Wizard flow (onboarding-time, precedes runtime): `get_provider_catalog()` → render `catalog["stt"]`/`catalog["llm"]`/`catalog["tts"]` with parameter rules for `Literal[...]`, `presets`, `required`, `default`, `description` (AGENT.md:40-47) → `extras_install_command(stt=..., tts=..., llm=...)` with exact parameter names `stt`, `tts`, `llm` (AGENT.md:51-56, README.md:183) → install in the app environment, restart the Python process, instantiate plugin classes (AGENT.md:57-60, README.md:187-188).
8. Dev/contract loop: `bash scripts/dev_build.sh` rebuilds protocol artifacts and provider metadata from the LiveKit source of truth (README.md:243-244); checks `python3 scripts/sync_livekit_plugins.py --check` and `python3 scripts/validate_runtime_contract.py --import-check` (README.md:224-241).

## 6. Key Files

Wiki coverage is limited to the repo root plus named directories; `src/` internals, per-module layout, and line counts are not recorded. Table below lists structurally important paths attested in the two wiki pages.

| File | Lines | What It Does |
|---|---|---|
| README.md | Cited through README.md:255-257 (full length not stated) | Product/architecture source of truth: Optimistic VUI definition, dual-agent design, modes, buffering, install, quick-starts, dev workflow |
| AGENT.md | Cited through AGENT.md:85-88 | Implementation contract for app/extension integration: wizard rules, install/restart, config and secret handling |
| `src/` (tree) | Unknown | Python package root; scanned by `bandit -r src/` and linted by ruff hooks (.pre-commit-config.yaml:15-20) |
| `packages/protocol-ts` (tree) | Unknown | TypeScript supervisor client (`@stimm/protocol`, npm); typechecked via `npm run check` (.pre-commit-config.yaml:32-40) |
| `website/` (tree) | Unknown | Documentation site: getting-started, quickstart, providers-catalog, wizard, supervisor observability (README.md:248-253) |
| `scripts/dev_build.sh` | Unknown | Single local rebuild: protocol artifacts + provider sync + runtime-contract validation (README.md:243-244) |
| `scripts/sync_livekit_plugins.py` | Unknown | Provider catalog sync from LiveKit source of truth; `--check` used in CI-equivalent flow (README.md:224-241) |
| `scripts/validate_runtime_contract.py` | Unknown | Runtime-contract validation incl. `--import-check` (README.md:224-241) |
| `.pre-commit-config.yaml` | Cited through .pre-commit-config.yaml:38-40 | Hook wiring: ruff format/check, bandit, pip-audit, protocol-ts typecheck |
| `.release-please-manifest.json` | 4 lines (cited .release-please-manifest.json:1-4) | Pinned release state: `.` 0.1.13, `packages/protocol-ts` 0.1.3 |
| `release-please-config.json` | Cited through release-please-config.json:19-21 | Joint Python/Node release config with `linked-versions` |
| `.gitignore` | Cited through .gitignore:46-47 | Excludes envs, build outputs, caches, logs, leftover `bin/` |
| `docker-compose.yml` (implied by `docker compose up -d`) | Unknown | Local infra for development (service list not in wiki) |
| `pyproject.toml` (implied by `pip install -e ".[dev]"`, `stimm[...]` extras) | Unknown | Packaging and extras definition (contents not in wiki) |

## 7. Dependencies

The wiki pages record no version-constraint strings. Runtime/plugin names below are attested in examples; constraints are stated as unknown rather than invented.

| Package | Version constraint | Purpose |
|---|---|---|
| livekit-agents | unknown (wiki states built on it, README.md:36) | Agent runtime: entrypoint, worker, data channels |
| livekit plugins: deepgram | unknown (example README.md:125-133) | STT provider in quick-start |
| livekit plugins: openai | unknown (example README.md:125-133) | TTS + fast-LLM provider in quick-start |
| livekit plugins: silero | unknown (example README.md:125-133) | VAD provider in quick-start |
| livekit plugins: azure-openai | unknown (example README.md:176-184) | Alternate LLM provider in wizard example |
| `@stimm/protocol` (npm) | 0.1.3 (manifest .release-please-manifest.json:2-3) | TypeScript supervisor client (README.md:100-112) |
| dev: pytest | unknown (README.md:224-241) | Test runner |
| dev: ruff | unknown (README.md:224-241, .pre-commit-config.yaml:5-14) | Format + lint |
| dev: bandit | unknown (.pre-commit-config.yaml:15-20) | Security scan over `src/` |
| dev: pip-audit | unknown (.pre-commit-config.yaml:22-27) | Dependency audit |
| dev: semgrep (CI-only) | unknown (.pre-commit-config.yaml:22) | Static analysis; CI-only per venv note |

Requires Python `>=3.10` (README.md:19-24). Install shapes: `pip install stimm`, `pip install stimm[deepgram,openai]`, `pip install stimm[all]`, `npm install @stimm/protocol` (README.md:100-112).

## 8. CLI / Usage Surface

No standalone CLI binary is attested; entry points are library classes plus scripts.

| Entry point | Form |
|---|---|
| `VoiceAgent` | `from stimm import VoiceAgent; agent = VoiceAgent(stt=..., tts=..., vad=..., fast_llm=..., buffering_level="MEDIUM", mode="hybrid", instructions=...); cli.run_app(WorkerOptions(entrypoint_fnc=agent.entrypoint))` (README.md:121-139) |
| `Supervisor` (Python) | `from stimm import Supervisor, TranscriptMessage; class MySupervisor(Supervisor): async def on_transcript(...)` + `await self.instruct(text, speak=True)` (README.md:141-151) |
| `StimmSupervisorClient` (TypeScript) | `new StimmSupervisorClient({livekitUrl, token})`, `.on("transcript", ...)`, `.instruct({text, speak, priority})`, `.connect()` (README.md:154-172) |
| Catalog/wizard API | `get_provider_catalog()`, `extras_install_command(stt=, tts=, llm=)`, `required_extras_for_selection(...)`, `list_runtime_providers()` (runtime listing, not for discovery UI) (AGENT.md:13-21) |
| Dev scripts | `bash scripts/dev_build.sh`; `python3 scripts/sync_livekit_plugins.py --check`; `python3 scripts/validate_runtime_contract.py --import-check`; `pytest`; `ruff check src/ tests/`; `docker compose up -d` (README.md:224-241) |

Env-var table: no variable names are attested in the wiki pages. Only indirect evidence is `.env` ignored (.gitignore:1-5) and the secrets rule (AGENT.md:20-21).

Config table: app config persists user choices and parameter values only — `stt_provider`, `tts_provider`, `llm_provider`, `stt_params`, `tts_params`, `llm_params` (AGENT.md:67-76); exact wizard parameter names are `stt`, `tts`, `llm` (README.md:183). Agent parameters attested: `stt`, `tts`, `vad`, `fast_llm`, `buffering_level`, `mode`, `instructions` (README.md:125-133). `mode ∈ {autonomous, relay, hybrid}` default `hybrid` (README.md:207-210); `buffering_level ∈ {NONE, LOW, MEDIUM, HIGH}` default `MEDIUM` (README.md:212-217).

## 9. Extensibility Points

- New supervisor behavior: subclass Python `Supervisor` and override `on_transcript` (README.md:141-151); or implement a TypeScript supervisor on `StimmSupervisorClient` transcript events (README.md:154-172).
- New steering policy: vary `instruct(..., speak=True/False)` and `priority` (e.g. `"normal"`) per decision path (README.md:141-172).
- New provider support: extend the generated catalog / runtime contract pipeline via `scripts/sync_livekit_plugins.py` and `scripts/validate_runtime_contract.py`, rebuilt with `scripts/dev_build.sh` (README.md:243-244); surface new providers through `get_provider_catalog()` wizard rendering (AGENT.md:40-47), not `list_runtime_providers()` (AGENT.md:14-15).
- New voice character/behavior: pass `instructions`, swap `stt`/`tts`/`vad`/`fast_llm` plugin instances, tune `mode` and `buffering_level` on `VoiceAgent` (README.md:125-133, README.md:207-217).
- New onboarding UI: build the wizard from `catalog["stt"]`/`catalog["llm"]`/`catalog["tts"]` with `Literal`/`presets`/`required`/`default`/`description` rendering rules (AGENT.md:40-47), deriving installs from `required_extras_for_selection(...)` / `extras_install_command(...)` (AGENT.md:16-19).
- New docs pages: add under `website/` alongside the attested getting-started/quickstart/catalog/wizard/observability pages (README.md:248-253).

## 10. Limitations and Gotchas

- **Extras install without process restart fails at runtime.** Post-selection failures mean the extras install or restart was missed; extras must be installed in the same environment that runs the app and the Python process restarted before instantiating plugin classes (AGENT.md:78-83, AGENT.md:16-19, README.md:187-188).
- **Discovery UI built on the wrong API drifts.** Wizard UIs must use `get_provider_catalog()`; building from `list_runtime_providers()` violates the contract and diverges from the source of truth (AGENT.md:14-15). Docs-only providers with few model values and a "static" provider list are expected, not bugs (AGENT.md:78-83).
- **Buffering and mode tradeoffs are unmeasured in the wiki.** `NONE→HIGH` trades raw latency for cleaner delivery (README.md:219-220) and `relay`/`hybrid`/`autonomous` trade control for responsiveness (README.md:207-210), but the pages give no latency numbers, benchmarks, or interruption semantics; tuning is empirical.
- **Supervisor steering is eventually consistent by design.** The first response goes out before background reasoning completes (README.md:94-96); supervisors that assume synchronous control (e.g. gating every token) fight the architecture — `relay` mode is the only speak-only-instructions option (README.md:207-210).
- **Sparse source coverage constrains this analysis.** The wiki snapshot covers the README overview plus five root files (README chunk note at 01-overview.md:164; 02-top-level-files.md:89); `src/` modules, protocol schema fields, error handling, auth/token minting, and SIP/telephone paths are not documented in these pages.

## 11. How It Compares to Alternatives

The wiki pages name one direct dependency-comparison point, `livekit-agents` (README.md:36), and no competing projects; the comparisons below are positioned against widely known voice-agent options, with the caveat that the wiki does not itself make these comparisons.

- **livekit-agents (LiveKit)**: the substrate Stimm builds on — single-agent pipelines assembled from VAD/STT/LLM/TTS plugins. Stimm adds the optimistic second agent, typed `StimmProtocol` supervision, modes, and pre-TTS buffering rather than replacing the plugin ecosystem.
- **Pipecat (Daily)**: pipeline-runner voice framework with processors and transports. Stimm's differentiator per the wiki is the opinionated dual-agent split (fast talker + deep supervisor) and wizard-first catalog flow instead of a general pipeline DAG.
- **Vocode**: turn-based voice SDK with events and endpoints. Stimm positions toward interruptible early speech with parallel background reasoning, where Vocode-style designs center on endpoint management and telephony plumbing.
- **Bland / Vapi / Retell (managed voice platforms)**: hosted APIs that hide infra. Stimm is a self-hosted open-source runtime (MIT, README.md:255-257) where the integrator owns the LiveKit infra, provider extras, and supervisor logic.

Positioning sentence: Stimm is not another STT/LLM/TTS wrapper or hosted agent API but an optimistic coordination layer over LiveKit — useful when perceived latency and async supervision matter more than owning every pipeline primitive or offloading everything to a managed service.

## Appendix: Selected Code Snippets

1. `VoiceAgent` construction and entrypoint (README.md:125-133, run form README.md:121-139):

```python
agent = VoiceAgent(
    stt=deepgram.STT(),
    tts=openai.TTS(),
    vad=silero.VAD.load(),
    fast_llm=openai.LLM(model="gpt-4o-mini"),
    buffering_level="MEDIUM",
    mode="hybrid",
    instructions="You are a helpful voice assistant.",
)
```

2. Python supervisor steering on finalized transcripts (README.md:141-151):

```python
from stimm import Supervisor, TranscriptMessage
class MySupervisor(Supervisor):
    async def on_transcript(self, msg: TranscriptMessage):
        if not msg.partial:
            result = await my_big_llm.process(msg.text)
            await self.instruct(result.text, speak=True)
```

3. TypeScript supervisor client (README.md:154-172):

```typescript
import { StimmSupervisorClient } from "@stimm/protocol";
const client = new StimmSupervisorClient({
  livekitUrl: "ws://localhost:7880",
  token: supervisorToken,
});
client.on("transcript", async (msg) => {
  if (!msg.partial) {
    const result = await myAgent.process(msg.text);
    await client.instruct({ text: result, speak: true, priority: "normal" });
  }
});
await client.connect();
```

4. Wizard catalog → install derivation and persisted config (README.md:176-184, AGENT.md:67-76):

```python
from stimm import extras_install_command, get_provider_catalog
catalog = get_provider_catalog()
cmd = extras_install_command(stt="deepgram", tts="openai", llm="azure-openai")
print(cmd)  # pip install stimm[deepgram,openai]
```

```json
{
  "stt_provider": "deepgram",
  "tts_provider": "openai",
  "llm_provider": "azure-openai",
  "stt_params": {"model": "nova-3"},
  "tts_params": {"voice": "ash"},
  "llm_params": {"model": "gpt-4o-mini"}
}
```
