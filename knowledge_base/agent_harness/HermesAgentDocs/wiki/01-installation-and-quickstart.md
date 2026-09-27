> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Installation and Quickstart
**In one sentence:** Install Hermes Agent with the Desktop installer or one curl/PowerShell command, configure a provider with `hermes setup --portal` or `hermes model`, then verify with `hermes` and `hermes --continue` before adding gateway, tools, skills, MCP, or ACP layers.
## Key points
- Install on Linux, macOS, WSL2 (Windows Subsystem for Linux 2), or Termux (Android terminal app) with `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` and reload the shell with `source ~/.bashrc` or `source ~/.zshrc`.
- Install on native Windows 10/11 in PowerShell (command-line shell for Windows) with `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`, or use the Hermes Desktop installer on macOS or Windows for CLI (Command Line Interface) plus desktop app together.
- Prerequisites are Git on all non-Windows platforms plus `curl` and `xz-utils` on Linux (for example `sudo apt install curl xz-utils` on Debian/Ubuntu), with `build-essential` or `g++` additionally required for the desktop app.
- Per-user installs put code at `~/.hermes/hermes-agent/`, the launcher at `~/.local/bin/hermes`, and data at `~/.hermes/`, while root-mode installs use `/usr/local/lib/hermes-agent/`, `/usr/local/bin/hermes`, and `/root/.hermes/` or `$HERMES_HOME`.
- Fastest provider setup is `hermes setup --portal` for Nous Portal OAuth (login in browser, no API key) login covering 300+ models plus Tool Gateway, otherwise run `hermes model` and switch providers any time with the same command.
- Hermes Agent requires a model with at least 64,000 tokens of context (64K context minimum), so local models must be started with at least `--ctx-size 65536` or `-c 65536`.
- Secrets and tokens live in `~/.hermes/.env` while non-secret settings live in `~/.hermes/config.yaml`, best edited with `hermes config set <KEY> <value>`, and failures are diagnosed in order with `hermes doctor`, `hermes model`, `hermes setup`, `hermes sessions list`, `hermes --continue`, `hermes gateway status`.
---
## Install methods
### Desktop installer
On macOS or Windows, download the Hermes Desktop installer from https://hermes-agent.nousresearch.com/ and run it to get both the command-line (`hermes` command) and desktop applications together. After a command-line-only install, you can add the desktop app later with `hermes desktop`.
### curl script for Linux, macOS, WSL2, and Termux
For a command-line-only install without Hermes Desktop, run:
```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```
This covers Linux, macOS, WSL2, and Android Termux. On phones, see the dedicated Termux guide for the tested manual path and Android limitations. After it finishes, reload the shell:
```
source ~/.bashrc   # or source ~/.zshrc
```
Then start chatting with `hermes`.
### Windows PowerShell
On native Windows, run in PowerShell:
```
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```
 Herm es Desktop is the recommended path on Windows 10/11 when you also want the graphical app.
### Non-sudo and system service-user installs
Running Hermes as a dedicated unprivileged user (for example a `hermes` systemd service account, a background service manager on Linux) is supported. Only the Playwright `--with-deps` step (browser automation libraries such as `libnss3` and `libxkbcommon`) genuinely needs root (administrator) access, and the installer skips it when sudo is unavailable.
Recommended split on Debian/Ubuntu:
1. One time, as an admin user with sudo, install Chromium system libraries:
```
sudo npx playwright install-deps chromium
```
2. As the unprivileged service user, run the regular installer:
```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```
3. To skip browser automation entirely on headless (no screen) servers, pass `--skip-browser`:
```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-browser
```
Pass `--skip-computer-use` to skip pre-installing `cua-driver` (helper for the Computer Use toolset); it then installs on demand when the tool is enabled.
4. Make `hermes` visible to the service user by adding `~/.local/bin` to PATH (list of directories the shell searches for commands) or symlinking system-wide as admin:
```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
sudo ln -s /home/hermes/.hermes/hermes-agent/venv/bin/hermes /usr/local/bin/hermes
```
5. Verify with `hermes doctor`. A `ModuleNotFoundError: No module named 'dotenv'` means you invoked the repo source file with system Python instead of the venv (isolated Python environment) launcher. For an always-on messaging gateway on this account, enable lingering (keep user services running after logout and start them at boot) with `sudo loginctl enable-linger <service-user>`.
### Platform support tiers
Tier 1 (first priority, tested, must not break): macOS on Apple Silicon via Desktop or `install.sh`; Windows 10/11 x86_64 and aarch64 via Desktop or `install.ps1` with a few unavailable features; Linux and WSL2 x86_64 and aarch64 via `install.sh` tested on latest Ubuntu and WSL2; Docker (container platform) x86_64 and aarch64 via `docker pull`, where `hermes update` is not supported and updates use a new image.
Tier 2 (best effort, may break): Android Termux aarch64 via `install.sh` with phone limitations; Nix (reproducible package manager) on macOS, Linux, and NixOS (Linux distribution built on Nix) via a dedicated Nix setup path.
Unsupported (do not use, fixes not accepted): installs via AUR (Arch User Repository), macOS on Intel x86 processors, installs via PyPI (Python Package Index, for example `pip install hermes-agent`), and installs via Homebrew (`brew install hermes-agent`).
## What the installer does
The installer handles dependencies, repo clone, virtual environment, global `hermes` command setup, and LLM (Large Language Model) provider configuration automatically. You do not need to install Python, Node.js, ripgrep, or ffmpeg manually.
Automatically provided:
- uv (fast Python package manager)
- Python 3.11 via uv, no sudo needed
- Node.js v26 for browser automation and WhatsApp bridge; an existing system Node 22.22+, 24.11+, or 26+ is reused as-is
- ripgrep (fast file search tool)
- ffmpeg (audio format conversion for TTS, Text-to-Speech)
Layout depends on install user:
| Installer mode | Code lives at | `hermes` binary | Data directory |
|---|---|---|---|
| Per-user (git installer) | `~/.hermes/hermes-agent/` | `~/.local/bin/hermes` (symlink) | `~/.hermes/` |
| Root-mode (`sudo curl ... \| sudo bash`) | `/usr/local/lib/hermes-agent/` | `/usr/local/bin/hermes` | `/root/.hermes/` or `$HERMES_HOME` |
The root-mode FHS (Filesystem Hierarchy Standard) layout matches other system-wide developer tools on Linux and suits shared machines where one install serves every user; per-user auth (login credentials), skills, and sessions still live under each user's `~/.hermes/` or explicit `HERMES_HOME`. Hermes auto-detects git-installer, Docker, or NixOS layout for `hermes update` and shows it in `hermes doctor`.
Manual or developer installs from source (for contributing, specific branches, or full virtual-environment control) follow the Development Setup in the Contributing guide. Nix is no longer an explicitly supported general install path and has its own Nix and NixOS Setup guide.
## Provider choice and settings storage
Provider selection is the most important setup step. Run `hermes` once, then choose a path by goal: `hermes setup` for guided setup on your machine, `hermes model` when you already know the provider, `hermes gateway setup` after CLI works for a bot or always-on setup, `hermes model` plus custom endpoint for local or self-hosted models, and add routing or fallback only after base chat works.
Easiest path is Nous Portal:
```
hermes setup --portal
```
This logs you in, sets Nous as provider, and turns on the Tool Gateway (hosted web search, image generation, TTS, and cloud browser) in one command. On a fresh install, `hermes setup` offers Quick Setup with Nous Portal (free OAuth login), Full Setup (bring your own keys for every provider and tool), and Blank Slate (minimal agent with only provider and model plus File Operations and Terminal toolsets, everything else off and explicitly listed so updates do not re-enable it).
Useful defaults include Nous Portal via OAuth login in `hermes model`, OpenAI Codex via ChatGPT or Codex subscription device auth, Anthropic Claude via OAuth on Max plan plus extra credits or API key, OpenRouter via API key for multi-provider routing, and Custom Endpoint with base URL plus API key for Ollama (local model runner), LM Studio (local desktop app with OpenAI-compatible API), vLLM, or SGLang. The full catalog lives on the Providers page. You can switch any time with `hermes model`.
Minimum context is 64,000 tokens. Models with smaller windows cannot maintain working memory for multi-step tool-calling workflows and are rejected at startup. Most hosted Claude, GPT, Gemini, Qwen, and DeepSeek models meet this; local models need at least 64K configured.
Settings are split by type:
- Secrets and tokens go to `~/.hermes/.env`
- Non-secret settings go to `~/.hermes/config.yaml`
Edit them through the CLI so values land in the right file:
```
hermes config set model anthropic/claude-opus-4-6
hermes config set terminal.backend docker
hermes config set OPENROUTER_API_KEY sk-or-...
hermes model          # choose provider and model
hermes tools          # configure enabled tools
hermes gateway setup  # set up messaging platforms
hermes config set     # set one value
hermes config get     # inspect one value
hermes setup          # full setup wizard
```
## First chat and verify sessions
Start the classic CLI (Command Line Interface) or the newer TUI (Terminal User Interface, with modal overlays, mouse selection, and non-blocking input):
```
hermes          # classic CLI
hermes --tui    # modern TUI, recommended
```
Both share sessions, slash commands, and config. Use a specific, verifiable first prompt such as `Summarize this repo in 5 bullets and tell me what the main entrypoint is`, `Check my current directory and tell me what looks like the main project file`, or `Help me set up a clean GitHub PR workflow for this codebase`. Success means the banner shows your model and provider, Hermes replies without error, it can use a tool when needed, and conversation continues past one turn. Rule of thumb: if normal chat fails, do not add gateway, cron (scheduled jobs), skills, voice, or routing yet.
Verify session resume before moving on:
```
hermes --continue    # resume most recent session
hermes -c            # short form
```
This should return to the session just held. If not, check `hermes sessions list` and confirm the profile is the same and the session actually saved. For migration, use `hermes import` for a full backup restore or `hermes profile import` for one agent; profile exports exclude credentials by design, so they are not full backups.
Useful CLI basics: `/help` lists commands, `/tools` lists tools, `/model` switches models, `/personality pirate` tries a personality, `/save` saves the conversation; `Alt+Enter`, `Ctrl+J`, or `Shift+Enter` gives multi-line input depending on terminal support; typing a new message or pressing `Ctrl+C` interrupts a long-running agent task.
## Next-layer additions
Add these only after base chat works.
### Messaging gateway and bots
```
hermes gateway setup
```
Connects Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant, or Microsoft Teams through interactive platform configuration.
### Tools and sandboxed terminal
Tune tool access per platform with `hermes tools`. For safety, isolate terminal commands with `hermes config set terminal.backend docker` for Docker isolation or `hermes config set terminal.backend ssh` for a remote server. Docker users can add the egress credential-injection proxy (a local filter that keeps real API keys out of the sandbox) with `hermes egress setup && hermes egress start`; `hermes setup terminal` also points Docker users at it.
### Skills
Skills are on-demand `SKILL.md` instruction documents (for example deploy to Kubernetes, open a GitHub PR) that the agent loads only when a task matches, so they do not bloat every request. Bundled skills live in `~/.hermes/skills/`. Browse and install more with:
```
hermes skills browse
hermes skills search kubernetes
hermes skills install openai/skills/k8s
hermes skills opt-in --sync
```
Every installed skill becomes a slash command such as `/k8s deploy the staging manifest`.
### MCP servers
MCP (Model Context Protocol, a standard for connecting agents to external tools and data) servers are added in `~/.hermes/config.yaml`, for example:
```
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"
```
### ACP editor integration
ACP (Agent Client Protocol, a standard for connecting editors to agents) ships with the standard install extras. Run:
```
hermes acp
```
If installed without those extras, first run `cd ~/.hermes/hermes-agent && uv pip install -e ".[acp]"`.
### Voice mode
Install voice extras from the install directory, then use `/voice on` and `Ctrl+B` to record:
```
cd ~/.hermes/hermes-agent
uv pip install --python ./venv/bin/python -e ".[voice]"
```
## Common failure modes and recovery toolkit
| Symptom | Likely cause | Fix |
|---|---|---|
| `hermes: command not found` | Shell PATH not reloaded or missing `~/.local/bin` | Run `source ~/.bashrc`, check PATH, or symlink launcher to `/usr/local/bin/hermes` |
| `API key not set`, empty or broken replies | Wrong provider auth or model selection | Run `hermes model` again and confirm provider, model, and auth |
| Custom endpoint returns garbage | Wrong base URL, model name, or non-OpenAI-compatible endpoint | Verify endpoint in a separate client first, then check context length is at least 64K |
| Gateway starts but nobody can message it | Incomplete bot token, allowlist (list of permitted users), or platform setup | Re-run `hermes gateway setup` and check `hermes gateway status` |
| `hermes --continue` cannot find old session | Switched profiles or session never saved | Check `hermes sessions list` and confirm the right profile |
| Model unavailable or odd fallback | Aggressive provider routing or fallback settings | Keep routing off until base provider is stable |
| `hermes doctor` flags config problems, missing config after update | Missing or stale config values | Run `hermes config check` then `hermes config migrate`, retest plain chat before adding features |
| Symlinked `HERMES_HOME` storage error naming a path and link target | Missing, inaccessible, or non-directory link target, possibly unmounted external or NAS (Network Attached Storage) volume | Restore mount, fix target, verify permissions, and retry; do not run `hermes setup` as repair and do not let Hermes replace the link |
Recovery order when something feels off:
1. `hermes doctor`
2. `hermes model`
3. `hermes setup`
4. `hermes sessions list`
5. `hermes --continue`
6. `hermes gateway status`
**Covers:** getting-started/installation, getting-started/quickstart, getting-started/platform-support (docs site, retrieved 2026-09-08)
