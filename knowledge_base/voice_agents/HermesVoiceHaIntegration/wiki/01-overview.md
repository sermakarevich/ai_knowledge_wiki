> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Connect Hermes Agent to Home Assistant so Hermes can understand the home, call HA services, and optionally run a wake-word → STT → LLM → TTS voice loop (01-overview.md:18).
## Key points
- Connects Hermes Agent to Home Assistant for home understanding, HA service calls, and an optional wake-word → STT → LLM → TTS voice loop (01-overview.md:18).
- Bundles three pieces: `custom_components/hermes/` (integration, services, sensors, Lovelace bar), `plugins/home_assistant/` (entity/service tools), and `plugins/voice_stack/` (wake-word/STT/TTS helpers) (01-overview.md:22-26).
- Ships via HACS/manual copy for HA, plugin copy or Python wheel for Hermes, and an early-scaffold Supervisor add-on; the wheel is plugin-focused while the tag/source bundle carries HACS/add-on (01-overview.md:28-34).
- Release `v0.0.14` adds opt-in safety-filtered local HA intent handling, hardens reconnect cleanup, and fixes config-entry reloads on HA 2026.9+ (01-overview.md:36).
- Exposes 8 Hermes HA tools (`ha_search_entities`, `ha_get_state`, `ha_call_service`, `ha_get_overview`, `ha_list_services`, `control_light_and_set_scene`, `turn_off_all_except`, `ha_bulk_control`) and 6 voice tools (`voice_status`, `voice_enable`, `voice_disable`, `voice_speak`, `voice_listen`, `voice_prompt`) (01-overview.md:79-99).
- Coexists with Hermes' bundled HA integration: bundled handles Hermes→HA chats/skills, this project adds HA→Hermes bridge (Assist agent, sensors, WebSocket lifecycle, voice helpers) under separate plugin directories (01-overview.md:103-110).
- Defaults are developer-friendly, not always cloud-free: local-only requires local model plus Piper for offline TTS and OpenWakeWord instead of Edge TTS / Porcupine key, and `media_player` playback may need an HTTP/media bridge (01-overview.md:52-57).
---
## Bundle pieces
Verbatim bundle definition (01-overview.md:20-26):

| Piece | Path | What it does |
|---|---|---|
| Home Assistant custom integration | `custom_components/hermes/` | Adds the `hermes` integration, HA services, status sensors, and the Lovelace action bar. |
| Hermes Home Assistant plugin | `plugins/home_assistant/` | Gives Hermes tools for entity search, state lookup, service calls, bulk control, scene/script discovery, and HA context. |
| Hermes voice-stack plugin | `plugins/voice_stack/` | Adds wake-word, speech-to-text, text-to-speech, and voice pipeline helpers. |

## Install targets and distribution
Verbatim install matrix (01-overview.md:28-32):

| Install target | Mechanism | Artifact/source | Current maturity |
|---|---|---|---|
| HA custom integration | HACS custom repository or manual copy | GitHub tag/source distribution, `custom_components/hermes/` | Supported |
| Hermes plugins | Copy into `~/.hermes/hermes-agent/plugins` or install the Python wheel | Wheel/source distribution, `plugins/*` | Supported |
| HA add-on | Home Assistant Supervisor add-on scaffold | GitHub tag/source distribution, `addon/` | Early scaffold |

Constraint (01-overview.md:34):

> The Python wheel is intentionally plugin-focused. Use the GitHub tag or source distribution for the full HACS/custom-component/add-on bundle.

## Capabilities
What you get (01-overview.md:42-48):

- Ask Hermes natural-language smart-home questions: “Is the kitchen light on?”
- Let Hermes call Home Assistant services: lights, switches, scenes, scripts, climate, media players, and more.
- Use safety controls: blocked service domains, optional allow-list, and JSON-line audit logging.
- Expose Hermes health into HA as status sensors.
- Bridge HA-originated voice lifecycle events over the documented WebSocket protocol (`docs/ws-protocol.md`).
- Add a small Lovelace action bar to dashboards.
- Build toward local voice control with configurable STT/TTS/wake-word engines.

## Locality reality check
Stack can be fully local **if you choose local engines and a local model**; defaults are developer-friendly, not always cloud-free (01-overview.md:52):

- Hermes can run local models or remote providers depending on your Hermes config (01-overview.md:54).
- Edge TTS is network-backed. Use Piper for offline TTS (01-overview.md:55).
- Porcupine requires a Picovoice access key. OpenWakeWord is the open-source option (01-overview.md:56).
- `media_player` playback needs audio that Home Assistant can access; generated local files may require an HTTP/media bridge in more complex deployments (01-overview.md:57).

## Architecture and tools
Flow (01-overview.md:63-75):

```text
Voice / Chat request
        │
        ▼
Hermes Agent
  ├─ plugins/home_assistant     → HA REST/WebSocket API
  └─ plugins/voice_stack        → wake word / STT / TTS / media playback
        │
        ▼
Home Assistant
  ├─ custom_components/hermes   → config flow, services, sensors
  └─ Lovelace dashboard card    → custom:hermes-action-bar
```

Hermes HA tools (01-overview.md:79-88):

| Tool | Purpose |
|---|---|
| `ha_search_entities` | Search entities by name, domain, area-like metadata, or entity ID. |
| `ha_get_state` | Fetch current state and attributes for one entity. |
| `ha_call_service` | Call a Home Assistant service with safety checks. |
| `ha_get_overview` | Build a compact overview of the home. |
| `ha_list_services` | Discover service domains and service names. |
| `control_light_and_set_scene` | Compound helper for common light + scene actions. |
| `turn_off_all_except` | Turn off a domain while preserving chosen entities. |
| `ha_bulk_control` | Run multiple service calls and summarise results. |

Voice tools (01-overview.md:92-99):

| Tool | Purpose |
|---|---|
| `voice_status` | Show engine availability and pipeline state. |
| `voice_enable` | Enable continuous wake-word listening. |
| `voice_disable` | Disable continuous voice mode. |
| `voice_speak` | Speak text through the configured TTS engine. |
| `voice_listen` | One-shot record + transcription. |
| `voice_prompt` | Build the voice-optimised prompt with HA context. |

Bundled-integration coexistence (01-overview.md:103-110):

- the bundled integration lets Hermes talk to Home Assistant from inside Hermes chats and skills
- this project lets Home Assistant talk back to Hermes, including the Assist conversation-agent bridge, status sensors, WebSocket lifecycle, and optional voice-stack helpers
- existing skills that call the bundled `ha_get_state`, `ha_call_service`, or other built-in HA tools should keep working because this package installs separate plugin directories and does not replace the bundled integration
- if both integrations expose similarly named tools in your Hermes profile, keep using the tool names your existing skills already reference, or disable one plugin explicitly in `~/.hermes/config.yaml` if you want to avoid overlap

> In short: install this when you want Home Assistant to use Hermes as a voice/chat brain. Keep the bundled integration when you want Hermes to operate Home Assistant as a tool provider.

## Prerequisites and setup
Prerequisites (01-overview.md:116-122): Home Assistant reachable from Hermes machine; working Hermes Agent; HA Long-Lived Access Token; Python 3.11+; optional audio deps for voice I/O.

Step 1 — Hermes install (01-overview.md:130-147):

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes --version
hermes doctor
hermes setup
```

Step 2 — HA token via profile → Security → Long-Lived Access Tokens → Create Token, e.g. `Hermes Agent`; HA shows it once (01-overview.md:151-158).

Step 3 — plugin install, recommended (01-overview.md:170-175):

```bash
python3 -m pip install --upgrade "hermes-voice-ha-integration @ git+https://github.com/rusty4444/hermes-voice-ha-integration.git@v0.0.14"
hermes-ha-install-plugins
```

Manual source alternative (01-overview.md:188-196):

```bash
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/rusty4444/hermes-voice-ha-integration.git
cd hermes-voice-ha-integration
mkdir -p ~/.hermes/hermes-agent/plugins
rm -rf ~/.hermes/hermes-agent/plugins/home_assistant ~/.hermes/hermes-agent/plugins/voice_stack
cp -R plugins/home_assistant ~/.hermes/hermes-agent/plugins/home_assistant
cp -R plugins/voice_stack ~/.hermes/hermes-agent/plugins/voice_stack
```

Connection config, exact variable names (01-overview.md:203-211):

```bash
HASS_URL=http://homeassistant.local:8123
HASS_TOKEN=replace-with-your-long-lived-access-token
HERMES_HA_WS_TOKEN=
```

Rules: `HASS_URL` must include scheme (`http://`/`https://`) plus host/IP, e.g. `http://192.168.1.50:8123` (01-overview.md:214,222-226); `HERMES_HA_WS_TOKEN` empty/omitted for unauthenticated WS, or set to a shared string matching the HA setup-form field; fallback is `API_SERVER_KEY` or `HERMES_API_KEY` (01-overview.md:216-220).

Enable plugins (01-overview.md:228-235):

```yaml
plugins:
  enabled:
    - home_assistant
    - voice_stack
```

WebSocket receiver: no standalone `server.py`; starts when `voice_stack` loads at `ws://<hermes-host>:7860/api/hermes/ws`; verify with `hermes plugins` and `curl -N --no-buffer -H "Accept: text/event-stream" -H "Authorization: Bearer <YOUR_TOKEN>" http://localhost:7860/api/hermes/ws`; add-on maps `7860/tcp` and sets `HOME`, `HERMES_HOME`, `HERMES_VOICE_CACHE` to `/data/hermes` so cache lands under `/data/hermes/voice_cache` (01-overview.md:241-269).

Step 4 — pre-HA smoke test: run `hermes`, ask `Search my Home Assistant lights.` then `Is the living room light on?`; expect `ha_search_entities` or `ha_get_state` with live HA state (01-overview.md:273-296).

Truncation note: the chunk cuts off mid-sentence at 01-overview.md:297 (`If Home Assistant is unreachable, Hermes sh`) and ends with an unexpanded `Macro components: top-level-files/` pointer (01-overview.md:299-301); no claims beyond that point are covered here.

**Covers:** `README` repo overview (bundle, install matrix, `v0.0.14` note, capabilities, architecture diagram, HA/voice tool tables, prerequisites and Steps 1–4) as given in `chunks/01-overview.md`; referenced paths `custom_components/hermes/`, `plugins/home_assistant/`, `plugins/voice_stack/`, `addon/`, `docs/ws-protocol.md`, `~/.hermes/hermes-agent/plugins`, `~/.hermes/.env`, `~/.hermes/config.yaml`.
