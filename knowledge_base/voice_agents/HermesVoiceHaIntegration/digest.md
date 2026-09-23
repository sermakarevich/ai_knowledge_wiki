> [[index|Wiki]] | [[summary|Summary]]

# rusty4444/hermes-voice-ha-integration — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** Connect Hermes Agent to Home Assistant so Hermes can understand the home, call HA services, and optionally run a wake-word → STT → LLM → TTS voice loop (01-overview.md:18).

## Key points

- Connects Hermes Agent to Home Assistant for home understanding, HA service calls, and an optional wake-word → STT → LLM → TTS voice loop (01-overview.md:18).
- Bundles three pieces: `custom_components/hermes/` (integration, services, sensors, Lovelace bar), `plugins/home_assistant/` (entity/service tools), and `plugins/voice_stack/` (wake-word/STT/TTS helpers) (01-overview.md:22-26).
- Ships via HACS/manual copy for HA, plugin copy or Python wheel for Hermes, and an early-scaffold Supervisor add-on; the wheel is plugin-focused while the tag/source bundle carries HACS/add-on (01-overview.md:28-34).
- Release `v0.0.14` adds opt-in safety-filtered local HA intent handling, hardens reconnect cleanup, and fixes config-entry reloads on HA 2026.9+ (01-overview.md:36).
- Exposes 8 Hermes HA tools (`ha_search_entities`, `ha_get_state`, `ha_call_service`, `ha_get_overview`, `ha_list_services`, `control_light_and_set_scene`, `turn_off_all_except`, `ha_bulk_control`) and 6 voice tools (`voice_status`, `voice_enable`, `voice_disable`, `voice_speak`, `voice_listen`, `voice_prompt`) (01-overview.md:79-99).
- Coexists with Hermes' bundled HA integration: bundled handles Hermes→HA chats/skills, this project adds HA→Hermes bridge (Assist agent, sensors, WebSocket lifecycle, voice helpers) under separate plugin directories (01-overview.md:103-110).
- Defaults are developer-friendly, not always cloud-free: local-only requires local model plus Piper for offline TTS and OpenWakeWord instead of Edge TTS / Porcupine key, and `media_player` playback may need an HTTP/media bridge (01-overview.md:52-57).

## 2. [[wiki/02-top-level-files|Top-Level Files]]

**In one sentence:** The top-level files define what stays out of version control, how HACS presents the integration, and what ships in the source distribution.

## Key points

- `.gitignore` excludes Python build artifacts (`__pycache__/`, `*.py[cod]`, `*.egg-info/`, `dist/`, `build/`, `.eggs/`, `*.egg`, `*.whl`) from version control (`.gitignore:1-9`).
- `.gitignore` excludes virtual environments (`venv/`, `.venv/`, `env/`, `.env`) from version control (`.gitignore:11-15`).
- `.gitignore` excludes IDE and OS files (`.idea/`, `.vscode/`, `*.swp`, `*.swo`, `*~`, `.DS_Store`, `Thumbs.db`) from version control (`.gitignore:17-26`).
- `.gitignore` excludes test and coverage outputs (`.coverage`, `htmlcov/`, `.pytest_cache/`, `coverage/`) from version control (`.gitignore:28-32`).
- `.gitignore` excludes Hermes-local files (`*.hermes-home`, `local-config.yaml`) and build archives (`*.tar.gz`, `*.zip`) from version control (`.gitignore:34-40`).
- `hacs.json` declares the HACS integration name as `Hermes Voice Assistant`, the minimum Home Assistant version as `2024.8.0`, and enables README rendering via `render_readme` (`hacs.json:2-4`).
- `MANIFEST.in` ships top-level docs and assets (`README.md`, `LICENSE`, `CHANGELOG.md`, `hacs.json`, `logo.png`, `icon.png`) and recursively includes `docs`, `custom_components`, `addon`, `plugins`, `skills`, and `tests` while globally excluding `__pycache__`, `*.py[cod]`, and `.DS_Store` (`MANIFEST.in:1-8`).

## The system in five moves

1. The project connects Hermes Agent to Home Assistant for home understanding, service calls, and an optional wake-word → STT → LLM → TTS voice loop.
2. That capability is bundled as three pieces: the `custom_components/hermes/` HA integration, the `plugins/home_assistant/` Hermes tools, and the `plugins/voice_stack/` voice helpers.
3. The bundle ships through HACS/manual copy, plugin copy or plugin-focused wheel, and an early-scaffold Supervisor add-on, with v0.0.14 hardening safety-filtered local intents and reconnect/config reloads.
4. Coexistence is kept clean by leaving the bundled Hermes→HA integration in place while this project adds the HA→Hermes bridge, sensors, WebSocket lifecycle, and voice tools behind safety and locality choices.
5. The top-level files enforce that distribution boundary: `.gitignore` keeps build, env, IDE, test, and local artifacts out, `hacs.json` presents the integration to HACS, and `MANIFEST.in` carries the docs, components, add-on, plugins, skills, and tests into the source bundle.
