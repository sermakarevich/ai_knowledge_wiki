# Technical Analysis: vedantnimbarte/IRA

**Repository:** https://github.com/vedantnimbarte/IRA
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Speech-to-text has been usable for years; the failure mode IRA targets is turn-taking: assistants talk over the user during thinking pauses and force the user to listen through wrong answers (README.md:22). The primary user is a desktop operator who wants a hands-free, interruptible voice assistant for controlling local tools and services.

IRA addresses this with a single-process voice loop: wake word → endpointing → speech-to-text → streaming model → streaming speech, with barge-in armed through the whole speaking phase, tool calls, spoken confirmation before state-changing actions, and an on-screen display of what the agent is doing (README.md:18). The design bet is explicit: a slower model that yields the floor correctly is preferable to a smarter one that talks over the user (README.md:22). Everything runs in one process sharing a single cancellation token across transcription, generation, and playback, so one `cancel()` drops the HTTP stream and clears the audio queue in the same frame (README.md:143).

## 2. High-Level Architecture

```
  microphone (cpal capture, downmix, 16 kHz resample)
         │
         ▼
  wake.rs ──► openWakeWord 3-stage ONNX ──► chirp
         │
         ▼
  vad.rs ──► Silero VAD, 32 ms chunks ──► endpointing (200 ms pause starts STT, 700 ms silence ends turn)
         │
         ▼
  stt.rs ──► whisper (Groq cloud, or local) ──► transcript
         │
         ▼
  llm.rs ──► streaming generation ──► sentence split ──► Piper ──► rodio playback
         │         │                                            ▲
         │         ▼                                            │ duck-then-cut
         │   tool.rs registry + confirmation gate               │
         │         │                                            │
         │         ├──► mcp.rs (MCP servers as Tools)            │
         │         └──► wingman.rs (Wingman HTTP API as Tool) ───┘
         │
         ▼
  ui.rs / orb.rs ◄── GET /events stream ◄── main.rs state machine
         │
         ▼
  db.rs (ira.local.db) + transcript.jsonl + OS keyring + skills/*.md
```

Data flow:

1. **Idle / wake.** `wake.rs` runs openWakeWord (mel → embedding → classifier) continuously; a wake word ("hey Jarvis") or `POST /talk` moves the machine to Listening (README.md:117).
2. **Listening / endpointing.** `vad.rs` (Silero v5, 32 ms chunks) watches the stream; a 200 ms pause starts STT while the user is still finishing, and 700 ms of silence ends the turn (README.md:117). Transcription overlaps the wait.
3. **Transcription.** `stt.rs` transcribes over HTTP via Groq cloud or a local engine; the completed transcript is handed to the model stage (README.md:155).
4. **Holding / speaking.** `llm.rs` streams generation, splits into sentences, and feeds Piper → rodio as one thinking-and-speaking phase; barge-in stays armed and ducks at a hint, cutting when confirmed (README.md:117).
5. **Side effects / confirmation.** A tool that wants to change state diverts to a Confirming sub-state: spoken yes runs it, anything else (silence, ambiguity, interruption) is a refusal (README.md:117, README.md:186). The reply path then holds the floor open 2 s for a follow-up before returning to Idle (README.md:117).
6. **Observation.** `ui.rs` (screen) and `orb.rs` (overlay globe) render the same `GET /events` stream; `GET /state` polls status and `POST /say` injects speech that waits for a free floor (README.md:238, README.md:240).

Persistent state lives outside the process in four places: `ira.local.db` (settings, servers, tool policy, skill index) (README.md:166); `transcript.jsonl` (conversation record, ignored as runtime output) (`.gitignore:33`); the OS keyring (API keys, per-server credentials, OAuth tokens — never files) (README.md:59, README.md:200); and the models directory (`models/`, `piper/`, `whisper/`, fetched artifacts ~85 MB plus STT/Kokoro weights) (README.md:45, `.gitignore:29`). Per-platform app directory: `%LOCALAPPDATA%\IRA` on Windows (README.md:65), `~/.local/share/ira` on Linux (README.md:66), `~/Library/Application Support/IRA` on macOS (README.md:67). A source checkout keeps its own `models/`, `ira.local.db`, and transcript beside it, distinguished by a `Cargo.toml` in the working directory (README.md:87).

## 3. The Turn State Machine

The central abstraction is the turn: a state machine in `main.rs` (README.md:162) that owns the microphone, the speaker, and one shared cancellation token (README.md:143). Representation is the four named states quoted verbatim from the state diagram (README.md:117):

- **Idle** — `openWakeWord: 3-stage ONNX` (README.md:117; component `wake.rs`, README.md:153). Entry via 2 s open floor expiring after a reply; exit via wake word or `POST /talk`.
- **Listening** — `Silero VAD, 32 ms chunks; pause 200 ms → start STT; silence 700 ms → turn is over` (README.md:117; component `vad.rs`, README.md:154). Transcription overlaps the endpointing wait.
- **Holding** — `model streams → sentences → Piper → rodio; barge-in armed the whole time; duck at a hint, cut when confirmed` (README.md:117; components `llm.rs`, README.md:156; audio path `audio.rs`, README.md:152). Thinking and speaking are one phase.
- **Confirming** — `spoken yes or no; anything else is no` (README.md:117; gate in `tool.rs`, README.md:157). Reached only when a tool wants to change something; reply completion returns through Holding.

Key queries against this abstraction are transitions, not data lookups. The two documented external ones:

- `GET /state` polls status; `GET /events` is the live stream read by screen and orb (README.md:240).
- Trigger speech from outside (README.md:234):

```bash
curl -X POST http://127.0.0.1:8180/say -H 'Content-Type: application/json' -d '{"text": "The build finished."}'
```

A pip sounds immediately and the words wait for the floor — the same path as finished background jobs, so a mid-sentence background completion never interrupts (README.md:238). Background-detached tools answer immediately, pip on completion, and speak when the floor is free (README.md:248).

## 4. LLM / External Service Integration

The available wiki pages name providers and engines but do not quote model IDs, endpoint URLs, or SDK call signatures; what follows is the provider/routing level documented in the overview page.

- **Generation (required):** Anthropic key configured via `ira set ANTHROPIC_API_KEY sk-ant-...` (README.md:51). Generation streams over HTTP; `llm.rs` owns streaming generation, sentence splitting, and the tool loop (README.md:156). A missing key is fatal at start-up: the fatal preflight subset runs on every start so a missing key stops the process instead of surfacing as mid-sentence silence (README.md:103).
- **Speech-to-text (required, two engines):** cloud via Groq (`ira set IRA_STT_ENGINE cloud` plus `ira set GROQ_API_KEY gsk_...`, README.md:55) or local whisper. First start downloads local STT (~80 MB, or ~900 MB with an NVIDIA-driver GPU build and bigger model) (README.md:45). `stt.rs` covers transcription over HTTP, cloud or local (README.md:155). On Linux/macOS whisper.cpp ships no prebuilt binary, so first start prints four build commands unless cloud STT is selected (README.md:55).
- **Speech synthesis (local models):** Piper voice (~85 MB bundle with wake models and piper, README.md:45) plus the Kokoro voice (330 MB) (README.md:45). Synthesis feeds rodio playback inside the Holding phase (README.md:117).
- **Wake / VAD (local models):** openWakeWord 3-stage ONNX (`wake.rs`, README.md:153) and Silero v5 (`vad.rs`, README.md:154), fetched on first start with progress shown (README.md:45).
- **Tool servers (optional, user-attached):** MCP servers (local stdio program or URL) attached from the settings window or orb, connected on save with no restart (README.md:175); Wingman (terminal coding agent) as the one non-MCP capability spoken to over its HTTP API directly, defaulting to port 8787 (README.md:253). Per-server credentials go to the keyring via `ira mcp env <server> <VAR> <value>`; OAuth servers get a Sign in button with self-refreshing keyring tokens (README.md:196, README.md:200).
- **Environment variables / secrets handling:** keys go to the OS keyring once and are read from there on every start, never from the environment (README.md:93). Named variables attested in the wiki: `ANTHROPIC_API_KEY`, `IRA_STT_ENGINE`, `GROQ_API_KEY`, `IRA_PTT` (press-to-talk, disarms voice barge-in, README.md:108), `IRA_WINGMAN_URL` (Wingman endpoint, README.md:258). Valueless per-server variables are omitted rather than passed empty (README.md:200).

## 5. The Voice Turn Pipeline

The primary workflow is one interruptible voice turn from wake to reply, executed by the `main.rs` state machine (README.md:162) across the component files in the README component map (README.md:151). Per-function `file.py:line` step detail is not quoted in the available wiki pages; steps below are grounded at the file level the wiki attests.

1. **Capture and resample** — `audio.rs`: cpal capture, downmix, 16 kHz resample; WAV replay for tests (README.md:152). Single process holds microphone and speaker simultaneously (README.md:143).
2. **Wake detection** — `wake.rs`: openWakeWord mel → embedding → classifier (README.md:153). Say "hey Jarvis", wait for the chirp; follow-ups need no second wake word within the open floor (README.md:100).
3. **Endpointing and barge-in sensing** — `vad.rs`: Silero v5, endpointing and barge-in (README.md:154). 200 ms pause starts STT overlapping the wait; 700 ms silence ends the turn; during Holding the same detector ducks at a hint and cuts when barge-in is confirmed (README.md:117).
4. **Transcription** — `stt.rs`: transcription over HTTP, cloud or local (README.md:155). Produces the transcript handed to generation.
5. **Streaming generation and tool loop** — `llm.rs`: streaming generation, sentence splitting, tool loop (README.md:156). Sentences stream to Piper → rodio as a single thinking-and-speaking phase (README.md:117).
6. **Tool gating** — `tool.rs`: the `Tool` trait, the registry, the confirmation gate (README.md:157). State-changing tools require an explicit spoken yes; silence, ambiguity, and interrupting the question all refuse; a tool's self-description is never trusted for the read-only gate (README.md:186). Unmarked tools keep asking; marking a tool read-only stops the prompts (README.md:186).
7. **Server adaptation** — `mcp.rs`: MCP servers adapted to the `Tool` trait (README.md:158); `wingman.rs`: Wingman's HTTP API adapted to that trait (README.md:159). Rust `impl Tool` and MCP-added tools are indistinguishable to registry and model (README.md:172).
8. **Rendering and record** — `ui.rs`: screen and event stream (README.md:160); `orb.rs`: overlay globe on a layered window, same stream (README.md:161); `skills.rs`: `skills/*.md` user instructions loaded on demand (README.md:163); `transcript.rs` with `metrics.rs`/`doctor.rs`/`config.rs`: timing, preflight, server list, the record (README.md:168).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `src/main.rs` | whole file | Turn state machine (Idle → Listening → Holding → Confirming) (README.md:162) |
| `src/audio.rs` | whole file | cpal capture, downmix, 16 kHz resample; WAV replay for tests (README.md:152) |
| `src/wake.rs` | whole file | openWakeWord wake-word detection: mel → embedding → classifier (README.md:153) |
| `src/vad.rs` | whole file | Silero v5 endpointing and barge-in sensing (README.md:154) |
| `src/stt.rs` | whole file | Transcription over HTTP, cloud (Groq) or local whisper (README.md:155) |
| `src/llm.rs` | whole file | Streaming generation, sentence splitting, tool loop (README.md:156) |
| `src/tool.rs` | whole file | `Tool` trait, registry, spoken confirmation gate (README.md:157) |
| `src/mcp.rs` | whole file | MCP servers (stdio/URL) adapted to the `Tool` trait (README.md:158) |
| `src/wingman.rs` | whole file | Wingman HTTP API adapted to the `Tool` trait; non-MCP exception (README.md:159) |
| `src/ui.rs` | whole file | Screen and its `GET /events` event stream (README.md:160) |
| `src/orb.rs` | whole file | Overlay globe on layered window consuming the same stream; icon source via ignored render test (README.md:161, `.gitattributes:16`) |
| `src/skills.rs` | whole file | `skills/*.md` user-written instructions, loaded on demand (README.md:163) |
| `src/cli.rs`, `src/oauth.rs` | whole files | Terminal window (`ira set/mcp/skill/fetch/doctor`); hosted-server sign-in (README.md:164) |
| `src/settings.rs` | whole file | Keys in OS keyring, URLs and model IDs in SQLite (README.md:165) |
| `src/db.rs` | whole file | `ira.local.db`: settings, servers, tool policy, skill index (README.md:166) |
| `src/metrics.rs`, `src/doctor.rs`, `src/config.rs`, `src/transcript.rs` | whole files | Timing, preflight checks, server list, conversation record (README.md:168) |
| `build.rs` | 67–65 | Windows-only icon embed: re-run on `assets/ira.ico` change, `winresource::WindowsResource::set_icon`; missing `rc.exe` degrades to warning (build.rs:71, build.rs:75, build.rs:79) |
| `.gitignore` | 25–47 | Ignores `/target`, fetched `/models/*.onnx{,.json,.bin}` + `/piper/` + `/whisper/`, runtime `/transcript.jsonl` + `/ira.log` + `/ira.local.db{,-journal}`, `.wingman/`, release `*.msi/*.deb/*.dmg` outputs (.gitignore:25–47) |
| `.gitattributes` | 9–18 | `* text=auto` LF enforcement plus `*.ico/*.png/*.icns binary` guards for rendered icons (.gitattributes:12, .gitattributes:18) |

## 7. Dependencies

The two available wiki pages do not quote `Cargo.toml` (or any manifest) and therefore attest no package version-constraint strings; fabricating them would be unverified. The table below lists the runtime/engine dependencies the overview page names, with the constraint column marked accordingly.

| Package | Version constraint | Purpose |
|---|---|---|
| openWakeWord (ONNX models) | not quoted in available wiki pages | 3-stage wake-word detection in `wake.rs` (README.md:153); fetched on first start (README.md:45) |
| Silero VAD v5 | not quoted in available wiki pages | Endpointing and barge-in sensing in `vad.rs` (README.md:154) |
| whisper (Groq cloud or local whisper.cpp) | not quoted in available wiki pages | Speech-to-text in `stt.rs` (README.md:155); local build ~80 MB / ~900 MB GPU option (README.md:45) |
| Piper + Kokoro voice | not quoted in available wiki pages | Streaming speech synthesis feeding rodio (README.md:117); ~85 MB bundle and 330 MB Kokoro voice (README.md:45) |
| rodio / cpal (audio I/O) | not quoted in available wiki pages | Speaker playback and microphone capture/downmix/16 kHz resample in `audio.rs` (README.md:152) |
| MCP servers (user-attached, e.g. GitHub MCP server) | not quoted in available wiki pages | External tools adapted via `mcp.rs` (README.md:158); e.g. `npx -y @modelcontextprotocol/server-github` (README.md:216) |
| Wingman agent | not quoted in available wiki pages | Non-MCP coding capability via its HTTP API in `wingman.rs`, default port 8787 (README.md:253) |
| winresource (Windows build only) | not quoted in available wiki pages | Embeds `assets/ira.ico` into the binary; warning-only fallback without `rc.exe` (build.rs:75, build.rs:79) |

## 8. CLI / Usage Surface

Entry points: installed binary `ira` (Start menu entry and PATH on Windows, README.md:34; `apt`-installed on Linux, README.md:35; DMG on macOS, README.md:36), source equivalent `cargo run --release -- <args>` (README.md:81), settings window / orb gear or `http://127.0.0.1:8180/settings` for interactive configuration (README.md:175), and the HTTP surface (`POST /say`, `GET /state`, `GET /events`, `POST /settings/admin`, `POST /talk`-family) for external control (README.md:234, README.md:240, README.md:243).

| Command | Effect |
|---|---|
| `ira set ANTHROPIC_API_KEY sk-ant-...` | Store generation key in OS keyring (README.md:51) |
| `ira set IRA_STT_ENGINE cloud` + `ira set GROQ_API_KEY gsk_...` | Select cloud STT and store its key (README.md:55) |
| `ira fetch` / `ira fetch --whisper` | Download models/voice/piper; add local STT (README.md:225) |
| `ira doctor` | Report missing models, microphone, keys, local engines (README.md:74, README.md:103) |
| `ira mcp ls · add · env · rm` | Provision/list/remove MCP servers; writes DB, connects nothing until next start; terminal use needs no spoken confirmation (README.md:220) |
| `ira mcp add github stdio npx -y @modelcontextprotocol/server-github` | Concrete server-add example (README.md:216) |
| `ira mcp env github GITHUB_TOKEN ghp_...` | Store per-server credential in keyring (README.md:196) |
| `ira skill ls · add · on · off · rm` | Manage `skills/*.md` instruction packs in the DB (README.md:220) |
| `POST /say` (`curl -X POST http://127.0.0.1:8180/say ...`) | Inject speech that pips and waits for a free floor (README.md:234, README.md:238) |

| Env var | Required? | Effect |
|---|---|---|
| `ANTHROPIC_API_KEY` (via `ira set`) | yes, for generation | Generation credential; missing key fails start-up preflight (README.md:51, README.md:103) |
| `GROQ_API_KEY` (via `ira set`) | only with cloud STT | Cloud transcription credential (README.md:55) |
| `IRA_STT_ENGINE` | no (default local) | `cloud` selects Groq over local whisper (README.md:55) |
| `IRA_PTT` | no | `=1` disarms voice barge-in; talk control becomes the interrupt path (README.md:108) |
| `IRA_WINGMAN_URL` | only with Wingman | Wingman HTTP endpoint, default port 8787 (README.md:258) |

| Config store | Contents |
|---|---|
| OS keyring (`IRA` entries) | All keys and per-server secrets/OAuth tokens; never files (README.md:59, README.md:200) |
| `ira.local.db` (+`-journal`) | URLs, model IDs, servers, per-tool policy, skill toggles (README.md:208, `.gitignore:40`) |
| Legacy `ira.toml` | Imported once on first start, never read again (README.md:208) |
| Screen at `http://127.0.0.1:8180` (Linux, no orb/settings window) | `ira set` configures; screen served over HTTP (README.md:35) |

## 9. Extensibility Points

- **New built-in tool:** implement the Rust `Tool` trait and register it in `src/tool.rs`, which owns the trait, the registry, and the confirmation gate (README.md:157). Rust tools and MCP tools are indistinguishable downstream (README.md:172).
- **New external capability:** add an MCP server (local stdio program or URL) from the orb gear / `http://127.0.0.1:8180/settings`; it connects on save with per-tool enable switches and announcement lines (README.md:175). `stdio` additions require a spoken yes because they run at every start (README.md:180). Headless/SSH equivalent is `ira mcp add` plus `ira mcp env` (README.md:196, README.md:216).
- **Non-MCP agent integration:** follow `src/wingman.rs`, which adapts Wingman's own HTTP API to the `Tool` trait because Wingman is an MCP client rather than a server (README.md:159, README.md:253).
- **User instructions:** add `skills/*.md` packs via `ira skill add` / `on` / `off`, loaded on demand by `src/skills.rs` (README.md:163); per-tool Try-it boxes test tools outside a conversation (README.md:204).
- **Read-only vs gated tools:** mark a tool read-only to stop confirmation prompts; leave it unmarked and every invocation keeps asking, since absent and safe are not the same answer (README.md:186).
- **UI/event consumers:** consume `GET /events` (same stream as screen and orb) and `GET /state`; full HTTP auth matrix is in `docs/SPEC.md#the-http-surface` (README.md:240, README.md:243). `src/ui.rs` and `src/orb.rs` are the in-repo consumers to copy (README.md:160, README.md:161).
- **Windows packaging:** icon handling only — `assets/ira.ico` is rendered by the ignored `render_the_icon` test in `src/orb.rs` and embedded by `build.rs` via `winresource` (build.rs:64, `.gitattributes:16`).

## 10. Limitations and Gotchas

- **No acoustic echo cancellation.** On speakers the microphone hears IRA's own voice and she interrupts herself; wear headphones or set `IRA_PTT=1` for press-to-talk (README.md:108).
- **Unsigned installers.** Windows shows "Windows protected your PC" (More info → Run anyway); macOS refuses outright (right-click → Open) (README.md:38). macOS status is "it compiles and that is all that is known" (README.md:36).
- **Linux has no orb or settings window.** Configuration is `ira set` and the screen is served at `http://127.0.0.1:8180` (README.md:35).
- **Linux/macOS local STT needs a manual build.** whisper.cpp ships no prebuilt binary there, so first start prints four build commands; the alternative is cloud STT (README.md:55).
- **Uninstall and upgrade do not remove state.** The per-platform app directory (conversations, models, settings DB) survives uninstall — deliberately, because an upgrade uninstalls first — and must be deleted manually plus the `IRA` keyring entries for full removal (README.md:69).
- **Fail-fast preflight, not graceful degradation.** The fatal `doctor` subset runs on every start, so a missing key or model stops the process rather than failing mid-sentence (README.md:103).
- **Confirmation defaults to no.** Only an explicit spoken yes runs a state-changing tool; unmarked tools prompt every time, and interrupting the confirmation question itself counts as refusal (README.md:186).
- **Windows icon build is SDK-dependent.** Without `rc.exe` from the Windows SDK the icon embed degrades to a `cargo:warning=no icon embedded` and a plain icon (build.rs:79).

## 11. How It Compares to Alternatives

- **OpenVoiceOS / Mycroft AI:** full voice-assistant platforms with skills ecosystems and multi-device support; IRA is narrower — a single-process desktop loop whose differentiator is endpointing/barge-in discipline rather than skill breadth (README.md:22, README.md:143).
- **Rhasspy / Home Assistant voice:** offline-first, pipeline-of-separate-services architectures (wake → STT → intent → TTS as distinct components); IRA inverts this by fusing the loop into one process with a shared cancellation token so interruption is atomic (README.md:143).
- **Vapi / LiveKit Agents (hosted voice-agent stacks):** managed telephony/WebRTC pipelines with server-side orchestration; IRA is local-first with keys in the OS keyring and models/DB on disk, trading managed scale for local control and no-per-minute inference path beyond the named providers (README.md:45, README.md:59).
- **Raw whisper.cpp + Piper + LLM wiring:** the same building blocks as DIY setups, but DIY leaves turn-taking, confirmation gating, and the MCP/Wingman tool registry to the builder; IRA's contribution is exactly that integration (state machine, duck-then-cut barge-in, spoken confirm gate, Try-it test boxes) (README.md:117, README.md:186, README.md:204).

Positioning: IRA competes on turn-taking correctness and single-process interruption atomicity for a desktop operator, not on model quality, skill count, or multi-device reach.

## Appendix: Selected Code Snippets

Windows icon embedding, verbatim (build.rs:67):

```rust
fn main() {
    #[cfg(windows)]
    {
        println!("cargo:rerun-if-changed=assets/ira.ico");
        let mut res = winresource::WindowsResource::new();
        res.set_icon("assets/ira.ico");
        if let Err(e) = res.compile() {
            println!("cargo:warning=no icon embedded ({e})");
        }
    }
}
```

Turn state diagram, verbatim (README.md:117):

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

Line-ending and binary guards, verbatim (`.gitattributes:9`, `.gitattributes:17`):

```
* text=auto
```

```
*.ico binary
*.png binary
*.icns binary
```

Per-server credential storage, verbatim (README.md:196):

```bash
ira mcp env github GITHUB_TOKEN ghp_...
```
