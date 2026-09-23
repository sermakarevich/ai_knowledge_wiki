# Technical Analysis: rusty4444/hermes-voice-ha-integration

**Repository:** https://github.com/rusty4444/hermes-voice-ha-integration
**Version analyzed:** v0.0.14
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: a capable local agent (Hermes Agent) has no bidirectional path into Home Assistant (HA): stock voice control implies cloud processing, latency, and subscriptions, and the bundled Hermes HA integration only covers Hermes→HA chats/skills, not HA→Hermes use (01-overview.md:103-110). The primary user is a self-hosting HA operator who already runs Hermes Agent and wants natural-language state queries ("Is the kitchen light on?") and service calls (lights, switches, scenes, scripts, climate, media players) from chat or voice, with health visible inside HA (01-overview.md:42-48).

How the repo addresses it: it bundles three cooperating pieces — `custom_components/hermes/` (integration, services, sensors, Lovelace bar), `plugins/home_assistant/` (entity/service tools), and `plugins/voice_stack/` (wake-word/STT/TTS helpers) (01-overview.md:22-26). The HA side contributes config flow, services, status sensors, an Assist conversation-agent bridge, and a WebSocket lifecycle bridge documented in `docs/ws-protocol.md`; the Hermes side contributes 8 HA tools and 6 voice tools; distribution is HACS/manual copy for HA, plugin copy or Python wheel for Hermes, and an early-scaffold Supervisor add-on (01-overview.md:28-34). Release `v0.0.14` adds opt-in safety-filtered local HA intent handling, hardens reconnect cleanup, and fixes config-entry reloads on HA 2026.9+ (01-overview.md:36).

## 2. High-Level Architecture

```text
Voice / Chat request
        │
        ▼
Hermes Agent
  ├─ plugins/home_assistant ──► HA REST/WebSocket API
  └─ plugins/voice_stack ──► wake word / STT / TTS / media playback
        │
        ▼
Home Assistant
  ├─ custom_components/hermes ──► config flow, services, sensors
  └─ Lovelace dashboard card ──► custom:hermes-action-bar
```

Adapted from the flow diagram at 01-overview.md:63-75.

Data-flow narrative:

1. Input enters as a voice utterance or chat message ("Search my Home Assistant lights.", "Is the living room light on?") into Hermes Agent (01-overview.md:273-296).
2. Hermes dispatches to `plugins/home_assistant` tools (`ha_search_entities`, `ha_get_state`) for read-only resolution, or to guarded write tools (`ha_call_service`, `ha_bulk_control`, compound helpers) with blocked-domain / allow-list checks and JSON-line audit logging (01-overview.md:79-88; 01-overview.md:42-48).
3. The optional voice path runs wake-word → STT → LLM → TTS via `plugins/voice_stack` tools (`voice_status`, `voice_enable`, `voice_disable`, `voice_speak`, `voice_listen`, `voice_prompt`) (01-overview.md:92-99).
4. HA-originated turns travel the reverse direction: `custom_components/hermes` sends lifecycle/Assist events over the WebSocket protocol (`docs/ws-protocol.md`) to the receiver that starts when `voice_stack` loads at `ws://<hermes-host>:7860/api/hermes/ws` (01-overview.md:42-48; 01-overview.md:241-269).
5. Actuation lands in HA as service calls; observability returns as status sensors and the Lovelace `custom:hermes-action-bar` (01-overview.md:22-26).

Persistent state lives in three places per the covered pages: HA config entries and the setup-form shared secret matched by `HERMES_HA_WS_TOKEN` (01-overview.md:216-220); Hermes local config (`~/.hermes/config.yaml` plugin enablement, `~/.hermes/.env`-style `HASS_URL`/`HASS_TOKEN`) (01-overview.md:203-235); and the add-on `/data/hermes` tree (`HOME`, `HERMES_HOME`, `HERMES_VOICE_CACHE`, cache under `/data/hermes/voice_cache`) (01-overview.md:241-269). Safety audit output is JSON-line logging (01-overview.md:42-48).

## 3. The Guarded Bidirectional Bridge

The central abstraction is a guarded bidirectional bridge: Hermes operates HA as a tool provider, and HA talks back to Hermes as a conversation/voice brain, under separate plugin directories so existing skills keep working (01-overview.md:103-110).

Representation: two tool namespaces installed side by side with the bundled integration. HA namespace, 8 tools (01-overview.md:79-88):

- `ha_search_entities` (`01-overview.md:75`) — search by name, domain, area-like metadata, entity ID.
- `ha_get_state` (`01-overview.md:76`) — current state + attributes for one entity.
- `ha_call_service` (`01-overview.md:77`) — service call with safety checks.
- `ha_get_overview` (`01-overview.md:78`) — compact home overview.
- `ha_list_services` (`01-overview.md:79`) — discover domains/service names.
- `control_light_and_set_scene` (`01-overview.md:80`) — compound light + scene helper.
- `turn_off_all_except` (`01-overview.md:81`) — turn off a domain preserving chosen entities.
- `ha_bulk_control` (`01-overview.md:82`) — multiple service calls with result summary.

Voice namespace, 6 tools (01-overview.md:92-99): `voice_status`, `voice_enable`, `voice_disable`, `voice_speak`, `voice_listen`, `voice_prompt`.

Key queries (verbatim from covered pages):

- `Search my Home Assistant lights.` → expect `ha_search_entities` with live HA state (01-overview.md:273-296).
- `Is the living room light on?` / `Is the kitchen light on?` → expect `ha_get_state` (01-overview.md:273-296; 01-overview.md:42-48).
- `Let Hermes call Home Assistant services: lights, switches, scenes, scripts, climate, media players, and more.` (01-overview.md:42-48).

Coexistence rule (01-overview.md:103-110, verbatim in substance): this package installs separate plugin directories and does not replace the bundled integration; if both expose similarly named tools, keep the names existing skills reference or disable one plugin explicitly in `~/.hermes/config.yaml`.

## 4. LLM / External Service Integration

The repo calls no LLM directly in the covered pages; the LLM is Hermes Agent's configured model. The wiki states Hermes can run local models or remote providers depending on Hermes config (01-overview.md:54). Voice engines are pluggable with explicit locality consequences (01-overview.md:52-57):

| Capability | Options cited | Locality / credential requirement |
|---|---|---|
| LLM | local model or remote provider (Hermes config) | local-only requires a local model (01-overview.md:52-57) |
| TTS | Piper / Edge TTS | Edge TTS is network-backed; use Piper for offline TTS (01-overview.md:55) |
| Wake word | OpenWakeWord / Porcupine | Porcupine requires Picovoice access key; OpenWakeWord is open-source option (01-overview.md:56) |
| Playback | HA `media_player` | needs HA-accessible audio; local files may require HTTP/media bridge (01-overview.md:57) |
| HA API | HA REST/WebSocket API | requires reachable HA + Long-Lived Access Token (01-overview.md:116-122) |

Required calls: HA REST/WebSocket API via `plugins/home_assistant` (01-overview.md:63-75). Optional calls: wake-word/STT/TTS/media playback via `plugins/voice_stack`, only exercised when voice mode is enabled (01-overview.md:92-99; 01-overview.md:241-269).

Environment variables (exact names from 01-overview.md:203-220): `HASS_URL` (must include scheme, e.g. `http://192.168.1.50:8123`), `HASS_TOKEN`, `HERMES_HA_WS_TOKEN` (empty/omitted = unauthenticated WS, else must match HA setup-form field; fallback `API_SERVER_KEY` or `HERMES_API_KEY`).

## 5. The Voice-Loop and Guarded-Control Pipeline

Primary workflow: wake-word → STT → LLM → TTS → `media_player`, with a read-only-before-write onboarding gate. Per-function `file.py:line` citations are not present in the covered wiki pages (which expose only bundle paths and tool names); each step below cites the wiki line that grounds it.

1. Install Hermes Agent and verify (`hermes --version`, `hermes doctor`, `hermes setup`) (01-overview.md:130-147).
2. Create HA Long-Lived Access Token via profile → Security → Long-Lived Access Tokens (e.g. `Hermes Agent`; shown once) (01-overview.md:151-158).
3. Install Hermes plugins — recommended: `python3 -m pip install --upgrade "hermes-voice-ha-integration @ git+https://github.com/rusty4444/hermes-voice-ha-integration.git@v0.0.14"` then `hermes-ha-install-plugins` (01-overview.md:170-175); manual alternative copies `plugins/home_assistant` and `plugins/voice_stack` into `~/.hermes/hermes-agent/plugins` (01-overview.md:188-196).
4. Configure connection (`HASS_URL`, `HASS_TOKEN`, `HERMES_HA_WS_TOKEN`) and enable plugins in `~/.hermes/config.yaml` (`home_assistant`, `voice_stack`) (01-overview.md:203-235).
5. Start voice receiver implicitly on `voice_stack` load at `ws://<hermes-host>:7860/api/hermes/ws`; verify with `hermes plugins` and the `curl -N` SSE check; no standalone `server.py` exists (01-overview.md:241-269).
6. Smoke-test read-only before any write: `hermes` → `Search my Home Assistant lights.` → `Is the living room light on?`, expecting `ha_search_entities` / `ha_get_state` with live state; unreachable HA is reported gracefully (01-overview.md:273-296; truncation at 01-overview.md:297 noted — no claims beyond that line are covered).

## 6. Key Files

Covered wiki pages document bundle directories plus top-level packaging files; per-file line counts below are from the wiki's own line references, not repo `wc`.

| File | Lines | What It Does |
|---|---|---|
| `custom_components/hermes/` | dir (01-overview.md:22-26) | HA integration: config flow, services, status sensors, Lovelace action bar |
| `plugins/home_assistant/` | dir (01-overview.md:22-26) | Hermes HA tools: search, state, service calls, bulk/compound control, context |
| `plugins/voice_stack/` | dir (01-overview.md:22-26) | Wake-word, STT, TTS, pipeline helpers; starts WS receiver on load |
| `addon/` | dir (01-overview.md:28-34) | Supervisor add-on scaffold; early maturity; maps `7860/tcp` |
| `docs/ws-protocol.md` | doc (01-overview.md:42-48) | WebSocket voice-lifecycle protocol contract |
| `hacs.json` | 5 lines (`hacs.json:1-5` per 02-top-level-files.md:56-72) | HACS metadata: name, min HA version, README rendering |
| `MANIFEST.in` | 8 lines (`MANIFEST.in:1-8` per 02-top-level-files.md:75-98) | Source-distribution include/exclude rules |
| `.gitignore` | 40 lines (`.gitignore:1-40` per 02-top-level-files.md:13-54) | Excludes build artifacts, venvs, IDE/OS, coverage, Hermes-local files |
| `~/.hermes/hermes-agent/plugins` | path (01-overview.md:188-196) | Install destination for both Hermes plugins |
| `~/.hermes/config.yaml` | path (01-overview.md:228-235) | Plugin enablement (`home_assistant`, `voice_stack`); overlap resolution |
| `README.md` / `CHANGELOG.md` / `LICENSE` | shipped via `MANIFEST.in:1` | Top-level docs/licence included in source distribution |
| `logo.png` / `icon.png` | shipped via `MANIFEST.in:1` | HACS/storefront assets |

Structural note: the wheel is intentionally plugin-focused; the GitHub tag/source distribution carries the full HACS/custom-component/add-on bundle (01-overview.md:34).

## 7. Dependencies

Covered pages state no Python package version pins; constraints below are exact strings where the wiki gives them, otherwise marked not stated.

| Package | Version constraint | Purpose |
|---|---|---|
| Home Assistant | `>= 2024.8.0` (`hacs.json:3` per 02-top-level-files.md:68-72) | Host for `custom_components/hermes` |
| Python | `3.11+` (01-overview.md:116-122) | Runtime for Hermes plugins / wheel install |
| Hermes Agent | not versioned in covered pages (01-overview.md:116-122) | Agent runtime; provides LLM, plugin host, `hermes` CLI |
| HA Long-Lived Access Token | required, no version (01-overview.md:151-158) | Auth for REST/WebSocket calls |
| Audio deps | optional, unnamed in covered pages (01-overview.md:116-122) | Voice I/O for `voice_stack` |
| Piper | unpinned; offline-TTS option (01-overview.md:55) | Local TTS alternative to Edge TTS |
| OpenWakeWord | unpinned; open-source option (01-overview.md:56) | Local wake-word alternative to Porcupine |
| Porcupine | requires Picovoice access key (01-overview.md:56) | Wake-word engine (keyed) |
| Edge TTS | network-backed default path (01-overview.md:55) | Cloud TTS |
| Local LLM runtimes | Hermes-config dependent (01-overview.md:54) | Local-model option for cloud-free operation |

## 8. CLI / Usage Surface

Entry points (all from 01-overview.md):

| Entry | Command | Purpose |
|---|---|---|
| Hermes installer | `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh \| bash` | Install Hermes Agent |
| Hermes CLI | `hermes --version`, `hermes doctor`, `hermes setup`, `hermes`, `hermes plugins` | Version/doctor/setup, interactive run, plugin list |
| Plugin installer | `hermes-ha-install-plugins` (after `pip install ... @ git+https://github.com/rusty4444/hermes-voice-ha-integration.git@v0.0.14`) | Copy plugins into Hermes plugin dir |
| Manual install | `cp -R plugins/home_assistant plugins/voice_stack → ~/.hermes/hermes-agent/plugins/` | Source-copy alternative |
| WS probe | `curl -N --no-buffer -H "Accept: text/event-stream" -H "Authorization: Bearer <YOUR_TOKEN>" http://localhost:7860/api/hermes/ws` | Verify voice-stack receiver |
| HACS | custom-repository or manual copy of `custom_components/hermes/` | Install HA integration |

Environment variables:

| Variable | Required | Notes |
|---|---|---|
| `HASS_URL` | yes | Must include scheme + host/IP, e.g. `http://homeassistant.local:8123` or `http://192.168.1.50:8123` |
| `HASS_TOKEN` | yes | Long-Lived Access Token value |
| `HERMES_HA_WS_TOKEN` | no | Empty/omitted = unauthenticated WS; else must match HA setup-form field |
| `API_SERVER_KEY` / `HERMES_API_KEY` | fallback | WS-token fallback chain |
| `HOME` / `HERMES_HOME` / `HERMES_VOICE_CACHE` | add-on | Set to `/data/hermes`; cache under `/data/hermes/voice_cache` |

Config:

| File | Keys | Values |
|---|---|---|
| `~/.hermes/config.yaml` | `plugins.enabled` | `home_assistant`, `voice_stack`; disable one to resolve tool-name overlap |
| HA setup form | shared WS string | Must equal `HERMES_HA_WS_TOKEN` when set |

## 9. Extensibility Points

- New HA capability → extend `plugins/home_assistant/` (entity search, state, service-call, bulk/compound helpers live there) (01-overview.md:22-26; 01-overview.md:79-88).
- New voice engine or pipeline step → extend `plugins/voice_stack/` (wake-word/STT/TTS/playback helpers; receiver starts on plugin load, no standalone server) (01-overview.md:22-26; 01-overview.md:241-269).
- New HA service, sensor, or config-flow option → extend `custom_components/hermes/` (01-overview.md:22-26).
- Dashboard action → extend the Lovelace `custom:hermes-action-bar` card (01-overview.md:63-75).
- Protocol change → update `docs/ws-protocol.md` and both ends (HA sender, voice-stack receiver) together (01-overview.md:42-48).
- Safety policy → adjust blocked service domains, optional allow-list, and JSON-line audit logging around `ha_call_service` / `ha_bulk_control` (01-overview.md:42-48).
- Packaging → `MANIFEST.in` (`recursive-include` directives) controls what ships in source distributions; `hacs.json` controls HACS presentation and minimum HA version (02-top-level-files.md:75-98; 02-top-level-files.md:56-72).

## 10. Limitations and Gotchas

- **Defaults are not cloud-free.** Local-only operation requires choosing a local model plus Piper and OpenWakeWord; stock paths use remote providers, network-backed Edge TTS, and keyed Porcupine (01-overview.md:52-57).
- **`media_player` playback may need a bridge.** Generated local audio files are not always HA-reachable; complex deployments need an HTTP/media bridge (01-overview.md:57).
- **Wheel ≠ full bundle.** The Python wheel ships plugins only; HACS integration and add-on require the GitHub tag/source distribution (01-overview.md:34; `MANIFEST.in:1-8` coverage in 02-top-level-files.md:75-98).
- **`HASS_URL` shape is strict.** It must include scheme (`http://`/`https://`) plus host/IP; `homeassistant.local` may not resolve — use a literal IP such as `http://192.168.1.50:8123` as fallback (01-overview.md:214-226).
- **WS auth mismatch fails silently-ish.** `HERMES_HA_WS_TOKEN` must match the HA setup-form string or be left empty; fallback chain (`API_SERVER_KEY`, `HERMES_API_KEY`) complicates debugging (01-overview.md:216-220).
- **Version coupling is real.** `v0.0.14` exists partly to fix config-entry reloads on HA 2026.9+, and HACS floor is HA `2024.8.0`; upgrades on either side can break the bridge (01-overview.md:36; `hacs.json:3`).
- **Coverage caveat.** The available wiki snapshot covers README overview through Step 4 and top-level packaging files only; it truncates mid-sentence at 01-overview.md:297 with an unexpanded `top-level-files/` macro pointer (01-overview.md:299-301), so service-test, protocol-detail, and later-step claims are not grounded here.

## 11. How It Compares to Alternatives

- **NousResearch Hermes Agent built-in HA integration:** lets Hermes operate HA as a tool provider from chats/skills; this repo is complementary — it adds the HA→Hermes direction (Assist agent, sensors, WebSocket lifecycle, voice helpers) under separate plugin directories without replacing bundled tools (01-overview.md:103-110).
- **Home Assistant Assist (built-in conversation agent):** HA-native intent handling with no extra bridge; this repo instead plugs Hermes in as the Assist brain and adds safety-gated bulk/compound tools plus an external voice stack, at the cost of running a second runtime.
- **Wyoming-protocol / OpenWakeWord + Piper satellite stacks:** fully local wake/STT/TTS plumbing; this repo can consume the same engines (Piper, OpenWakeWord cited at 01-overview.md:55-56) but frames them inside Hermes tool calls and HA sensors rather than as standalone satellites.
- **Cloud assistants (Alexa / Google Assistant + HA Cloud):** zero-self-hosting voice control with cloud dependence; this repo's positioning is the inverse — self-hosted, auditable, optionally fully local when local engines and models are selected (01-overview.md:52-57).

Positioning: use this repo when Home Assistant should use Hermes as its voice/chat brain with guarded, auditable device control; keep the bundled Hermes HA integration (or stock Assist) when Hermes merely needs HA as one tool provider among many.

## Appendix: Selected Code Snippets

1. Bundle definition (`01-overview.md:20-26`):

```text
| Piece | Path | What it does |
|---|---|---|
| Home Assistant custom integration | `custom_components/hermes/` | Adds the `hermes` integration, HA services, status sensors, and the Lovelace action bar. |
| Hermes Home Assistant plugin | `plugins/home_assistant/` | Gives Hermes tools for entity search, state lookup, service calls, bulk control, scene/script discovery, and HA context. |
| Hermes voice-stack plugin | `plugins/voice_stack/` | Adds wake-word, speech-to-text, text-to-speech, and voice pipeline helpers. |
```

2. Distribution constraint (`01-overview.md:34`):

```text
The Python wheel is intentionally plugin-focused. Use the GitHub tag or source distribution for the full HACS/custom-component/add-on bundle.
```

3. Connection variables (`01-overview.md:203-211`):

```bash
HASS_URL=http://homeassistant.local:8123
HASS_TOKEN=replace-with-your-long-lived-access-token
HERMES_HA_WS_TOKEN=
```

4. Source-distribution rules (`MANIFEST.in:1-8` via 02-top-level-files.md:77-87):

```text
include README.md LICENSE CHANGELOG.md hacs.json logo.png icon.png
recursive-include docs *.png *.md *.html
recursive-include custom_components *
recursive-include addon *
recursive-include plugins *.py *.yaml *.md
recursive-include skills *
recursive-include tests *.py
global-exclude __pycache__ *.py[cod] .DS_Store
```
