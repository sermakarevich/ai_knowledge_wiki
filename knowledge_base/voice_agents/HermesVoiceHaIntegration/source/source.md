# rusty4444/hermes-voice-ha-integration
PDF: https://github.com/rusty4444/hermes-voice-ha-integration
Source: https://github.com/rusty4444/hermes-voice-ha-integration
Kind: repo
Fetched: 2026-09-22T14:11:14.313194+00:00
Tool: git-clone

# rusty4444/hermes-voice-ha-integration

Commit: a1a854690a9f82f1d2862c01fe9fc80217f708e7

## README

# Hermes × Home Assistant Voice Integration
<p align="center">
  <a href="https://buymeacoffee.com/rusty4" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50">
  </a>
</p>



![Hermes + Home Assistant Logo](logo.png)

Connect **Hermes Agent** to **Home Assistant** so Hermes can understand your home, call HA services, and optionally run a wake-word → STT → LLM → TTS voice loop.

This repository is a bundle of three pieces:

| Piece | Path | What it does |
|---|---|---|
| Home Assistant custom integration | `custom_components/hermes/` | Adds the `hermes` integration, HA services, status sensors, and the Lovelace action bar. |
| Hermes Home Assistant plugin | `plugins/home_assistant/` | Gives Hermes tools for entity search, state lookup, service calls, bulk control, scene/script discovery, and HA context. |
| Hermes voice-stack plugin | `plugins/voice_stack/` | Adds wake-word, speech-to-text, text-to-speech, and voice pipeline helpers. |

| Install target | Mechanism | Artifact/source | Current maturity |
|---|---|---|---|
| HA custom integration | HACS custom repository or manual copy | GitHub tag/source distribution, `custom_components/hermes/` | Supported |
| Hermes plugins | Copy into `~/.hermes/hermes-agent/plugins` or install the Python wheel | Wheel/source distribution, `plugins/*` | Supported |
| HA add-on | Home Assistant Supervisor add-on scaffold | GitHub tag/source distribution, `addon/` | Early scaffold |

The Python wheel is intentionally plugin-focused. Use the GitHub tag or source distribution for the full HACS/custom-component/add-on bundle.

> **Release:** `v0.0.14` — adds opt-in, safety-filtered local HA intent handling, hardens reconnect cleanup, and fixes config-entry reloads on Home Assistant 2026.9+.

---

## What you get

- Ask Hermes natural-language smart-home questions: “Is the kitchen light on?”
- Let Hermes call Home Assistant services: lights, switches, scenes, scripts, climate, media players, and more.
- Use safety controls: blocked service domains, optional allow-list, and JSON-line audit logging.
- Expose Hermes health into HA as status sensors.
- Bridge HA-originated voice lifecycle events over the documented WebSocket protocol (`docs/ws-protocol.md`).
- Add a small Lovelace action bar to dashboards.
- Build toward local voice control with configurable STT/TTS/wake-word engines.

## Important reality check

The stack can be fully local **if you choose local engines and a local model**. The defaults are developer-friendly, not always cloud-free:

- Hermes can run local models or remote providers depending on your Hermes config.
- Edge TTS is network-backed. Use Piper for offline TTS.
- Porcupine requires a Picovoice access key. OpenWakeWord is the open-source option.
- `media_player` playback needs audio that Home Assistant can access; generated local files may require an HTTP/media bridge in more complex deployments.

---

## Architecture

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

### Hermes tools provided by the HA plugin

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

### Voice tools provided by the voice plugin

| Tool | Purpose |
|---|---|
| `voice_status` | Show engine availability and pipeline state. |
| `voice_enable` | Enable continuous wake-word listening. |
| `voice_disable` | Disable continuous voice mode. |
| `voice_speak` | Speak text through the configured TTS engine. |
| `voice_listen` | One-shot record + transcription. |
| `voice_prompt` | Build the voice-optimised prompt with HA context. |

### If you already use Hermes' bundled Home Assistant integration

This project and Hermes' bundled Home Assistant integration can run side by side:

- the bundled integration lets Hermes talk to Home Assistant from inside Hermes chats and skills
- this project lets Home Assistant talk back to Hermes, including the Assist conversation-agent bridge, status sensors, WebSocket lifecycle, and optional voice-stack helpers
- existing skills that call the bundled `ha_get_state`, `ha_call_service`, or other built-in HA tools should keep working because this package installs separate plugin directories and does not replace the bundled integration
- if both integrations expose similarly named tools in your Hermes profile, keep using the tool names your existing skills already reference, or disable one plugin explicitly in `~/.hermes/config.yaml` if you want to avoid overlap

In short: install this when you want Home Assistant to use Hermes as a voice/chat brain. Keep the bundled integration when you want Hermes to operate Home Assistant as a tool provider.

---

## Prerequisites

You need:

1. **Home Assistant** with network access from the machine running Hermes.
2. **Hermes Agent** installed and working.
3. A **Home Assistant Long-Lived Access Token** for Hermes.
4. Python 3.11+ for local development/plugin execution.
5. Optional audio dependencies if you want voice input/output on the Hermes machine.

---

## Step 1 — Install Hermes Agent

Install Hermes using the official installer:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Restart your shell, then verify:

```bash
hermes --version
hermes doctor
```

Run the setup wizard if this is your first Hermes install:

```bash
hermes setup
```

Choose a model/provider. For a local-first HA assistant, configure Hermes to use your local model endpoint (for example Ollama, vLLM, or llama.cpp). Remote providers also work.

---

## Step 2 — Create a Home Assistant token

1. Open Home Assistant.
2. Click your user profile/avatar.
3. Scroll to **Security**.
4. Under **Long-Lived Access Tokens**, click **Create Token**.
5. Name it something clear, for example `Hermes Agent`.
6. Copy the token now. Home Assistant only shows it once.

Keep this token private. It can control your Home Assistant instance with your account permissions.

---

## Step 3 — Install the Hermes plugins

### Recommended: install from the Python package

Install or upgrade the package directly from GitHub, then run the bundled plugin installer:

```bash
python3 -m pip install --upgrade "hermes-voice-ha-integration @ git+https://github.com/rusty4444/hermes-voice-ha-integration.git@v0.0.14"
hermes-ha-install-plugins
```

The installer copies the packaged `home_assistant` and `voice_stack` plugin directories into `~/.hermes/hermes-agent/plugins`. On upgrade it replaces the existing plugin directories first, so files removed from newer releases do not remain behind from older manual copies.

If your Hermes Agent profile lives somewhere else, pass it explicitly:

```bash
hermes-ha-install-plugins --profile /path/to/hermes-agent-profile
```

### Manual source install

If you prefer to inspect or edit the source locally, clone the repository and copy the plugins yourself:

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

The `rm -rf` lines are intentional during manual upgrades: they avoid leaving stale files behind if a release removes or renames plugin files.

Configure Home Assistant connection details for Hermes. The plugin reads standard environment variables:

```bash
cat >> ~/.hermes/.env <<'EOF'
# URL to your Home Assistant instance (not the Hermes URL)
HASS_URL=http://homeassistant.local:8123
# Long-lived access token from HA user profile → Security → Long-Lived Access Tokens
HASS_TOKEN=replace-with-your-long-lived-access-token
# Optional: bearer token for the HA-to-Hermes WebSocket connection. Leave empty if no auth is needed.
HERMES_HA_WS_TOKEN=
EOF
```

**About the `HASS_URL` format:** The URL must include a scheme (`http://` or `https://`) and a hostname or IP address. For example `http://192.168.1.50:8123`. If you see `"No host part in the URL"`, the URL is missing the `http://` prefix or the hostname.

**About `HERMES_HA_WS_TOKEN`:** This is optional and used to secure the connection **from Home Assistant to Hermes**. Most users do not need it:

- **Leave empty** (or omit) for unauthenticated WebSocket connections.
- **Set to any string** (e.g. `my-hermes-token`) if you want to require a matching token on the HA side. If you set this, enter the same value in the HA custom integration setup form field "Hermes API / WebSocket token".
- If unset, the system falls back to `API_SERVER_KEY` or `HERMES_API_KEY` if either is configured.

If your HA URL is different, use that instead, for example:

```bash
HASS_URL=http://192.168.1.50:8123
```

Enable the plugins in `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - home_assistant
    - voice_stack
```

If your config already has a `plugins.enabled` list, add the two entries instead of replacing the whole section.

Restart Hermes after changing plugins or `.env`.

**How the WebSocket receiver starts:** The WebSocket receiver does not require a standalone `server.py` file. It starts automatically when the `voice_stack` plugin loads. After restarting Hermes, check that the WebSocket is active:

```bash
# Confirm the plugin is loaded: run `hermes plugins` and check that
# voice_stack appears in the list (it's an interactive prompt, so piping
# through grep won't work).
hermes plugins

# Test the WebSocket endpoint (replace with your Hermes host/port).
# If HERMES_HA_WS_TOKEN, API_SERVER_KEY, or HERMES_API_KEY is set in your
# ~/.hermes/.env, include it as a bearer token or you'll see
# "Invalid bearer token":
curl -N --no-buffer \
  -H "Accept: text/event-stream" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  http://localhost:7860/api/hermes/ws
```

The `voice_stack` plugin starts a small HA-facing WebSocket receiver at:

```text
ws://<hermes-host>:7860/api/hermes/ws
```

Home Assistant connects to this endpoint through the **Hermes URL** you enter below. If `HERMES_HA_WS_TOKEN`, `API_SERVER_KEY`, or `HERMES_API_KEY` is set, the HA custom integration token must match it.

When running the Home Assistant add-on, expose/map TCP port `7860` so Home Assistant can reach the HA-facing receiver. The bundled add-on config maps `7860/tcp` by default.

The add-on also sets `HOME`, `HERMES_HOME`, and `HERMES_VOICE_CACHE` to `/data/hermes` so voice engines that call `Path.home()` write their cache under `/data/hermes/voice_cache` instead of `/root/.hermes/voice_cache`.

---

## Step 4 — Test Hermes ↔ Home Assistant before installing anything in HA

Start Hermes:

```bash
hermes
```

Ask:

```text
Search my Home Assistant lights.
```

Then try a read-only state check:

```text
Is the living room light on?
```

Expected result:

- Hermes should use `ha_search_entities` or `ha_get_state`.
- The response should include the current state from Home Assistant.
- If Home Assistant is unreachable, Hermes sh

... (truncated, 21886 more characters)

## pyproject.toml

```
[project]
name = "hermes-voice-ha-integration"
version = "0.0.14"
description = "Home Assistant voice stack integration for Hermes Agent"
authors = [{name = "Sam Russell", email = "rusty4444@users.noreply.github.com"}]
license = "MIT"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "aiohttp>=3.9",
    "pydantic>=2.0",
]

[project.scripts]
hermes-ha-install-plugins = "plugins.install_hermes_ha_plugins:main"

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5",
    "PyYAML>=6.0",
    "build>=1.2",
]

voice = [
    "edge-tts>=6.1",
    "sounddevice>=0.4",
    "numpy>=1.26",
]

voice-stt = [
    "faster-whisper>=1.0",
]

voice-wake = [
    "pvporcupine>=3.0",
    "pyaudio>=0.2",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
pythonpath = ["."]

[build-system]
requires = ["setuptools>=77", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
include = ["plugins*"]
exclude = ["addon*", "custom_components*", "skills*", "tests*"]

[tool.setuptools.package-data]
"plugins.home_assistant" = ["plugin.yaml", "README.md"]
"plugins.voice_stack" = ["plugin.yaml", "README.md"]

```

## Top-level layout

- .github/ (dir, 2 files, ~68 lines)
- .gitignore (~40 lines)
- addon/ (dir, 6 files, ~207 lines)
- CHANGELOG.md (~90 lines)
- custom_components/ (dir, 18 files, ~2135 lines)
- docs/ (dir, 6 files, ~518 lines)
- hacs.json (~5 lines)
- icon.png (~0 lines)
- LICENSE (~21 lines)
- logo.png (~0 lines)
- MANIFEST.in (~8 lines)
- plugins/ (dir, 21 files, ~4556 lines)
- pyproject.toml (~56 lines)
- README.md (~889 lines)
- scripts/ (dir, 1 files, ~218 lines)
- skills/ (dir, 1 files, ~45 lines)
- tests/ (dir, 7 files, ~2564 lines)

