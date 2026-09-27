> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Overview

**In one sentence:** IRA is a voice assistant you can interrupt, piping wake word → endpointing → speech-to-text → streaming model → streaming speech with barge-in, tool calls, and an on-screen display in a single process.

## Key points

- IRA's whole pipeline is wake word → endpointing → speech-to-text → streaming model → streaming speech with barge-in, tool use, spoken confirmation before state changes, and a screen showing what it is doing (README.md:18).
- The design bet is that turn-taking is the feature: a slower model that yields the floor correctly beats a smarter one that talks over you (README.md:22).
- Everything runs in one process sharing a single cancellation token across transcription, generation, and playback, so interrupting is one `cancel()` that drops the HTTP stream and clears the audio queue in the same frame (README.md:143).
- A turn is a state machine — Idle (openWakeWord 3-stage ONNX) → Listening (Silero VAD, 32 ms chunks; 200 ms pause starts STT, 700 ms silence ends the turn) → Holding (model streams → sentences → Piper → rodio, barge-in armed, duck-then-cut) → optional Confirming (spoken yes/no, anything else is no) → 2 s open floor → Idle (README.md:117).
- Anything that changes state asks out loud first and only an explicit yes runs it; silence, ambiguity, and interrupting the question are all refusals, and a tool's own self-description is never trusted for the read-only gate (README.md:186).
- Tools are a Rust `impl Tool` or an MCP server added in the settings window/orb, indistinguishable to the registry and the model; Wingman is the one exception, spoken over its HTTP API directly because it is an MCP client rather than a server (README.md:172).

---

## The bet

Speech recognition has been good enough for years; what stays broken is being cut off when you pause to think, and having to wait out an answer you already know is wrong (README.md:22).

## Install

Download an installer from Releases, or build from source (README.md:29):

| OS | Artifact | Notes |
|---|---|---|
| Windows | `ira-<version>-x64.msi` | Per-user install, no admin/UAC; Start menu entry, `ira` on PATH (README.md:34) |
| Linux | `ira_<version>_amd64.deb` | `sudo apt install ./ira_*.deb`; no orb/settings window — `ira set` configures, screen at `http://127.0.0.1:8180` (README.md:35) |
| macOS | `ira-<version>-aarch64.dmg` | Unverified — it compiles and that is all that is known (README.md:36) |

Nothing is signed: Windows shows "Windows protected your PC" (More info → Run anyway); macOS refuses outright (right-click → Open) (README.md:38).

### First start

First run downloads wake models, voice, and piper (~85 MB), plus local speech-to-text (80 MB, or ~900 MB with an NVIDIA-driver GPU build and bigger model) and the Kokoro voice (330 MB), with progress shown (README.md:45). Then:

```
ira set ANTHROPIC_API_KEY sk-ant-...
```

verbatim (README.md:51). On Linux/macOS whisper.cpp has no prebuilt binary, so first start prints four build commands — or use cloud STT instead (README.md:55):

```
ira set IRA_STT_ENGINE cloud
ira set GROQ_API_KEY gsk_...
```

Keys go to the OS keyring; everything else (settings DB, transcript, skills, models) lives in one directory (README.md:59):

| Platform | Directory |
|---|---|
| Windows | `%LOCALAPPDATA%\IRA` (README.md:65) |
| Linux | `~/.local/share/ira` (README.md:66) |
| macOS | `~/Library/Application Support/IRA` (README.md:67) |

Uninstalling does not remove that directory (an upgrade uninstalls first, so deleting it would discard conversations and models on every update); delete it manually plus the `IRA` keyring entries for full removal (README.md:69). Interrupted downloads resume with `ira fetch`; `ira doctor` reports what is still missing (README.md:74).

## Run from a checkout

```powershell
.\scripts\fetch-models.ps1
cargo run --release -- set ANTHROPIC_API_KEY sk-ant-...
cargo run --release
```

verbatim (README.md:81). A checkout keeps its own `models/`, `ira.local.db`, and transcript beside it; a `Cargo.toml` in the working directory distinguishes checkout from install so a clone and an installed copy never share settings (README.md:87). Keys go to the keyring once and are read from there on every start, never from the environment (README.md:93); the settings window does the same job with a form (README.md:95). Linux/macOS equivalent is `./scripts/fetch-models.sh` (README.md:97).

Say **"hey Jarvis"**, wait for the chirp, talk; interrupt any time; follow-ups need no second wake word (README.md:100). `cargo run --release -- doctor` checks models, microphone, keys, and local engines; the fatal subset runs on every start-up so a missing key stops the process instead of surfacing as silence mid-sentence (README.md:103).

> **Wear headphones, or use press-to-talk.** No acoustic echo cancellation: on speakers the microphone hears IRA's own voice and she interrupts herself. `IRA_PTT=1` disarms voice barge-in and makes the talk control the way to interrupt (README.md:108).

## How a turn works

State diagram, verbatim (README.md:117):

```
        ┌──────────── Idle ─────────────┐
        │   openWakeWord: 3-stage ONNX  │
        └───────────────┬───────────────┘
                        │ wake word, or POST /talk
        ┌───────────────▼───────────────┐
        │          Listening            │   Silero VAD, 32 ms chunks
        │  pause 200 ms → start STT ────┼──► whisper (Groq, or local)
        │  silence 700 ms → turn is over│    transcription overlaps the wait
        └───────────────┬───────────────┘
                        │ transcript in hand
        ┌───────────────▼───────────────┐
        │           Holding             │   thinking and speaking are one
        │  model streams ──► sentences ─┼──► Piper ──► rodio
        │  barge-in armed the whole time│    duck at a hint, cut when confirmed
        └───────┬───────────────┬───────┘
                │               │ a tool wants to change something
                │               ▼
                │        ┌─────────────┐
                │        │ Confirming  │  spoken yes or no; anything else is no
                │        └─────────────┘
                │ reply done
                ▼
        floor stays open 2 s for a follow-up, then Idle
```

Single-process rationale: one process holds microphone and speaker simultaneously and shares one cancellation token, which is why IRA is not separate piped programs; it is the constraint other decisions bend around (README.md:143).

Component map, verbatim (README.md:151):

| File | Job |
|---|---|
| `audio.rs` | cpal capture, downmix, 16 kHz resample; WAV replay for tests (README.md:152) |
| `wake.rs` | openWakeWord: mel → embedding → classifier (README.md:153) |
| `vad.rs` | Silero v5, endpointing and barge-in (README.md:154) |
| `stt.rs` | Transcription over HTTP, cloud or local (README.md:155) |
| `llm.rs` | Streaming generation, sentence splitting, tool loop (README.md:156) |
| `tool.rs` | The `Tool` trait, the registry, the confirmation gate (README.md:157) |
| `mcp.rs` | MCP servers adapted to that trait (README.md:158) |
| `wingman.rs` | Wingman's own HTTP API adapted to that trait (README.md:159) |
| `ui.rs` | The screen and its event stream (README.md:160) |
| `orb.rs` | The overlay: a drawn globe on a layered window, same stream (README.md:161) |
| `main.rs` | The state machine (README.md:162) |
| `skills.rs` | `skills/*.md`: user-written instructions, loaded on demand (README.md:163) |
| `cli.rs` · `oauth.rs` | The window from a terminal; signing in to a hosted server (README.md:164) |
| `settings.rs` | Keys in the OS keyring, URLs and model ids in SQLite (README.md:165) |
| `db.rs` | `ira.local.db`: settings, servers, tool policy, the skill index (README.md:166) |
| `metrics.rs` · `doctor.rs` · `config.rs` · `transcript.rs` | Timing, preflight, the server list, the record (README.md:168) |

## Tools

Open the gear on the orb or `http://127.0.0.1:8180/settings` and add a server (a local program or a URL); it connects on save with no restart, and its tools appear with a per-tool enable switch and a pre-action announcement line (README.md:175). Adding a `stdio` program is a spoken yes: it runs at every start, so IRA reads it back and waits for an out-loud yes; anything else leaves nothing saved, and the backing route is stricter than `POST /talk` (no `curl` equivalent without an origin) (README.md:180).

Confirmation gate: only an explicit yes runs a state-changing tool; unmarked tools keep asking because absent and safe are not the same answer; mark a tool read-only to stop the prompts (README.md:186).

Credentials per server (verbatim, README.md:196):

```bash
ira mcp env github GITHUB_TOKEN ghp_...
```

Values go to the keyring, never a file; valueless variables are omitted rather than passed empty; OAuth servers get a Sign in button with self-refreshing keyring tokens (README.md:200). Every connected tool has a Try-it box (typed args, raw result) for testing outside a conversation (README.md:204). Servers, per-tool policy, and skill toggles live in `ira.local.db`; a legacy `ira.toml` is imported once on first start and never read again (README.md:208).

Terminal equivalents for provisioning/SSH (verbatim, README.md:216):

```bash
ira mcp add github stdio npx -y @modelcontextprotocol/server-github
```

`ira mcp ls · add · env · rm` and `ira skill ls · add · on · off · rm` write the database and connect nothing (servers come up at next start), with no spoken confirmation since a local terminal already is the authorisation (README.md:220). `ira fetch` downloads models/voice/piper; `ira fetch --whisper` adds local STT; first start runs both when files are missing (README.md:225).

## Talking to IRA from something else

Trigger speech from outside (verbatim, README.md:234):

```bash
curl -X POST http://127.0.0.1:8180/say -H 'Content-Type: application/json' -d '{"text": "The build finished."}'
```

A pip sounds immediately and the words wait for the floor (the same path as finished background jobs, so a mid-sentence deploy never interrupts) (README.md:238). `GET /state` polls status; `GET /events` is the live stream read by screen and orb (README.md:240). Both are guarded like the talk button (foreign-origin browsers refused; originless clients such as curl/CI allowed); neither can run anything, while `POST /settings/admin` is stricter — full table in `docs/SPEC.md#the-http-surface` (README.md:243). Background-detached tools answer immediately, pip on completion, and speak when the floor is free (README.md:248).

### Wingman

Wingman (terminal coding agent) is the one non-MCP capability: it is an MCP client, not a server, so IRA speaks its HTTP API directly (README.md:253). Setup fragment, verbatim as far as the chunk carries it (README.md:258):

```powershell
wingman serve                       # defaults to port 8787
$env:IRA_WINGMAN_URL = "http://127.0.0.1:8787
```

Note: the chunk ends mid-block here — the closing quote and any further Wingman configuration lines are cut off, so they are not documented (README.md:258).

## Truncation note

The chunk ends abruptly inside the Wingman setup block (unclosed code fence at chunk line 261) and then lists `top-level-files/` as the next macro component; per the task contract, the cut Wingman remainder and the `top-level-files/` material are not guessed at here — they belong to the follow-up page (chunk lines 258-265).

**Covers:** README (product pitch, install/run, turn state machine, tool model, HTTP surface, Wingman) and the `audio.rs`/`wake.rs`/`vad.rs`/`stt.rs`/`llm.rs`/`tool.rs`/`mcp.rs`/`wingman.rs`/`ui.rs`/`orb.rs`/`main.rs`/`skills.rs`/`cli.rs`/`oauth.rs`/`settings.rs`/`db.rs`/`metrics.rs`/`doctor.rs`/`config.rs`/`transcript.rs` component map; grounded in chunk `01-overview.md` lines 1-265.
