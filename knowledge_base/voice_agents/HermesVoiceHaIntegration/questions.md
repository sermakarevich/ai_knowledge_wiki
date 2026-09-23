---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: rusty4444/hermes-voice-ha-integration

### Q1. What is the one-sentence purpose of hermes-voice-ha-integration, and what capabilities does that include?

> [!tip]- Answer
> The project connects Hermes Agent to Home Assistant so Hermes can understand the home, call HA services, and optionally run a wake-word → STT → LLM → TTS voice loop. That spans natural-language smart-home questions, service calls across lights, switches, scenes, scripts, climate, and media players, plus safety controls, Hermes health sensors in HA, a WebSocket voice-lifecycle bridge, and a Lovelace action bar. See [[wiki/01-overview|Overview]].

### Q2. What three pieces does the integration bundle, and what is new in release v0.0.14?

> [!tip]- Answer
> The bundle holds `custom_components/hermes/` (HA integration, services, sensors, Lovelace bar), `plugins/home_assistant/` (entity search, state, service calls, bulk control, scene/script discovery), and `plugins/voice_stack/` (wake-word, STT, TTS, voice pipeline helpers). Release `v0.0.14` adds opt-in safety-filtered local HA intent handling, hardens reconnect cleanup, and fixes config-entry reloads on HA 2026.9+. See [[wiki/01-overview|Overview]].

### Q3. How do the install targets differ in maturity, and which artifact carries the full bundle?

> [!tip]- Answer
> The HA custom integration installs via HACS custom repository or manual copy and is Supported, the Hermes plugins install by copying into `~/.hermes/hermes-agent/plugins` or via the Python wheel and are Supported, and the Supervisor add-on scaffold in `addon/` is an Early scaffold. The Python wheel is intentionally plugin-focused, so the GitHub tag or source distribution must be used for the full HACS, custom-component, and add-on bundle. See [[wiki/01-overview|Overview]].

### Q4. Which Hermes tools does the project expose, and how does it coexist with Hermes' bundled HA integration?

> [!tip]- Answer
> It exposes 8 Hermes HA tools (`ha_search_entities`, `ha_get_state`, `ha_call_service`, `ha_get_overview`, `ha_list_services`, `control_light_and_set_scene`, `turn_off_all_except`, `ha_bulk_control`) and 6 voice tools (`voice_status`, `voice_enable`, `voice_disable`, `voice_speak`, `voice_listen`, `voice_prompt`). The bundled integration keeps handling Hermes→HA chats and skills while this project adds the HA→Hermes bridge (Assist agent, sensors, WebSocket lifecycle, voice helpers) under separate plugin directories. Existing skills referencing bundled tool names keep working, and overlap is resolved by keeping the familiar names or disabling one plugin in `~/.hermes/config.yaml`. See [[wiki/01-overview|Overview]].

### Q5. What is required for a fully local stack, and how is the Hermes→HA connection configured and smoke-tested?

> [!tip]- Answer
> Defaults are developer-friendly rather than cloud-free: a fully local stack needs a local model in Hermes config plus Piper instead of network-backed Edge TTS for offline speech, OpenWakeWord instead of key-gated Porcupine for wake-word, and possibly an HTTP/media bridge so `media_player` playback can reach generated audio files. Connection config sets `HASS_URL` with scheme plus host (e.g. `http://192.168.1.50:8123`), `HASS_TOKEN` to a long-lived access token, and `HERMES_HA_WS_TOKEN` empty or matching the HA setup-form string, with `home_assistant` and `voice_stack` enabled in `~/.hermes/config.yaml`. The pre-HA smoke test runs `hermes`, asks `Search my Home Assistant lights.` and `Is the living room light on?`, and expects `ha_search_entities` or `ha_get_state` to return live HA state. See [[wiki/01-overview|Overview]].

### Q6. What do the top-level files exclude from version control, declare to HACS, and ship in the source distribution?

> [!tip]- Answer
> `.gitignore` keeps Python build artifacts (`__pycache__/`, `*.py[cod]`, `*.egg-info/`, `dist/`, `build/`, `.eggs/`, `*.egg`, `*.whl`), virtual environments, IDE/OS files, test and coverage outputs, Hermes-local files (`*.hermes-home`, `local-config.yaml`), and build archives (`*.tar.gz`, `*.zip`) out of version control. `hacs.json` declares the HACS name `Hermes Voice Assistant`, minimum Home Assistant `2024.8.0`, and `render_readme: true`. `MANIFEST.in` ships top-level docs and assets (`README.md`, `LICENSE`, `CHANGELOG.md`, `hacs.json`, `logo.png`, `icon.png`), recursively includes `docs`, `custom_components`, `addon`, `plugins`, `skills`, and `tests`, and globally excludes `__pycache__`, `*.py[cod]`, and `.DS_Store`. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. Would you recommend this integration for a fully-offline, family-dependent voice setup, and why?

> [!tip]- Answer
> Not yet as the sole dependable layer: a fully-offline build is possible with a local model plus Piper and OpenWakeWord, but expect extra work on the HTTP/media bridge for `media_player` audio, an early-scaffold Supervisor add-on, and safety-filter tuning for local intents. Adopt it now to experiment with Hermes as the Assist chat/voice brain behind guarded service calls and audit logging, and keep a fallback control path until the voice pipeline and add-on mature. See [[wiki/01-overview|Overview]].
