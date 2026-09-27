> PDF location: https://github.com/vedantnimbarte/IRA (no source.pdf fetched; see Source field below)
# vedantnimbarte/IRA
Source: https://github.com/vedantnimbarte/IRA
Kind: repo
Fetched: 2026-09-22T14:13:14.139543+00:00
Tool: git-clone

# vedantnimbarte/IRA

Commit: a3eb694a482c467df7870801fe86e00b085628f0

## README

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/ira-dark.svg">
    <img src="assets/ira-light.svg" alt="IRA" width="120">
  </picture>
</p>

<h1 align="center">IRA</h1>

<p align="center">A voice assistant you can interrupt.</p>

Wake word → endpointing → speech-to-text → streaming model → streaming speech,
with barge-in. It calls tools, asks before it changes anything, and shows you
what it is doing on a screen.

The bet is that **turn-taking is the feature**. Speech recognition has been good
enough for years; what stays broken is being cut off when you pause to think,
and having to wait out an answer you already know is wrong. A slower model that
yields the floor correctly beats a smarter one that talks over you.

## Install

Download an installer from [Releases](https://github.com/vedantnimbarte/IRA/releases),
or build her from source below.

| | | |
|---|---|---|
| **Windows** | `ira-<version>-x64.msi` | Installs for you only — no administrator rights, no UAC prompt. She lands in the Start menu, and `ira` works in any terminal. |
| **Linux** | `ira_<version>_amd64.deb` | `sudo apt install ./ira_*.deb`. No orb and no settings window here: `ira set` configures her, and the screen is at `http://127.0.0.1:8180`. |
| **macOS** | `ira-<version>-aarch64.dmg` | ⚠️ **Unverified.** It compiles, and that is the whole of what is known about it. See [what has not been verified](#what-has-not-been-verified). |

**Nothing is signed.** Windows will say "Windows protected your PC" — choose
**More info → Run anyway**. macOS will refuse outright: right-click the app and
choose **Open**. Both are what an unsigned installer looks like, and both stop
once there is a certificate to sign with.

### The first start

She downloads the wake models, the voice and piper — about 85 MB — the first
time she runs, and local speech-to-text with them: 80 MB on most machines, or
about 900 MB where an NVIDIA driver makes the GPU build and a bigger model
worth it. Her voice, Kokoro, is another 330 MB. She shows progress while she
does it. Then give her a key:

```
ira set ANTHROPIC_API_KEY sk-ant-...
```

On Linux and macOS whisper.cpp has no prebuilt binary, so the first start stops
and prints the four commands that build it — or `ira set IRA_STT_ENGINE cloud`
and `ira set GROQ_API_KEY gsk_...` to transcribe at Groq instead.

Keys go to the operating system's keyring. Everything else — the settings
database, the transcript, the skills you write and the models above — lives in
one directory:

| Platform | Directory |
|---|---|
| Windows | `%LOCALAPPDATA%\IRA` |
| Linux | `~/.local/share/ira` |
| macOS | `~/Library/Application Support/IRA` |

**Uninstalling does not remove it.** An upgrade uninstalls the old version
first, so deleting it there would throw away your conversations and 85 MB of
models on every update. Delete the directory yourself if you want her gone
completely; the keys are in the keyring, under `IRA`.

If a download stops part-way, `ira fetch` picks up where it left off, and
`ira doctor` says what is still missing.

## Run

From a checkout:

```powershell
.\scripts\fetch-models.ps1
cargo run --release -- set ANTHROPIC_API_KEY sk-ant-...
cargo run --release
```

A checkout keeps its own `models/`, `ira.local.db` and transcript beside it,
exactly as before — a `Cargo.toml` in the working directory is how she tells a
checkout from an install ([0019](docs/decisions/0019-installed-rather-than-cloned.md)),
so a clone and an installed copy on the same machine never touch each other's
settings.

Keys go to the operating system's keyring, once, and are read from there on
every start — not from the environment, which puts them in your shell history
and in `ps`. The settings window does the same job with a form.

On Linux or macOS, `./scripts/fetch-models.sh` does the same job — though see
[what has not been verified](#what-has-not-been-verified) before trusting it.

Say **"hey Jarvis"**, wait for the chirp, talk. Interrupt her any time. Answer a
follow-up without saying the wake word again.

`cargo run --release -- doctor` checks models, microphone, keys and local
engines before you talk to it. The fatal subset of those checks runs on every
start-up, so a missing key stops the process rather than surfacing as silence
three seconds into your first sentence.

> **Wear headphones, or use press-to-talk.** There is no acoustic echo
> cancellation, so on speakers the microphone hears IRA's own voice and she
> interrupts herself. `IRA_PTT=1` disarms voice barge-in and makes the talk
> control the way to interrupt — speakers work, at the cost of hands-free
> interruption. Why it is not solved properly:
> [decisions/0010](docs/decisions/0010-press-to-talk-before-echo-cancellation.md).

## How a turn works

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

Everything above happens in **one process**. Barge-in works because a single
process holds the microphone and the speaker at the same instant and shares one
cancellation token across transcription, generation and playback — interrupting
is one `cancel()` that drops the HTTP stream mid-flight and clears the audio
queue in the same frame. That is why IRA is not assembled out of separate
programs piped together, and it is the constraint every other decision bends
around: [decisions/0001](docs/decisions/0001-audio-path-stays-in-one-process.md).

| File | Job |
|---|---|
| `audio.rs` | cpal capture, downmix, 16 kHz resample; WAV replay for tests |
| `wake.rs` | openWakeWord: mel → embedding → classifier |
| `vad.rs` | Silero v5, endpointing and barge-in |
| `stt.rs` | Transcription over HTTP, cloud or local |
| `llm.rs` | Streaming generation, sentence splitting, tool loop |
| `tool.rs` | The `Tool` trait, the registry, the confirmation gate |
| `mcp.rs` | MCP servers adapted to that trait |
| `wingman.rs` | Wingman's own HTTP API adapted to that trait |
| `ui.rs` | The screen and its event stream |
| `orb.rs` | The overlay: a drawn globe on a layered window, same stream |
| `main.rs` | The state machine |
| `skills.rs` | `skills/*.md`: user-written instructions, loaded on demand |
| `cli.rs` · `oauth.rs` | The window from a terminal; signing in to a hosted server |
| `settings.rs` | Keys in the OS keyring, URLs and model ids in SQLite |
| `db.rs` | `ira.local.db`: settings, servers, tool policy, the skill index |
| `metrics.rs` · `doctor.rs` · `config.rs` · `transcript.rs` | Timing, preflight, the server list, the record |

## Tools

A tool is a Rust `impl Tool` or an MCP server you add in the settings window.
The registry cannot tell them apart and neither can the model.

Open the gear on the orb, or <http://127.0.0.1:8180/settings>, and add a server:
a program on this machine, or a URL. It connects when you save — no restart —
and its tools appear under it, each with a switch for whether IRA may use it and
a line saying what she will do before she does.

> **Adding a program is a spoken yes.** A `stdio` server is a command IRA runs
> at every start, so she reads it back to you and waits for an out-loud yes
> before storing it. Anything that is not a yes leaves nothing saved. The route
> behind that form is also stricter than `POST /talk`: a request that does not
> say where it came from is refused, so there is no `curl` equivalent.

Anything that changes state asks out loud first, and **only an explicit yes runs
it** — silence, ambiguity, and interrupting the question are all refusals. A
server's own description of a tool is never trusted for this, because a tool that
calls itself harmless and is not would otherwise walk straight through the gate.
Mark a tool read-only in the window and it stops asking; a tool nobody has
marked keeps asking, because *absent* and *safe* are not the same answer.

**Give a server what it needs.** Most want a credential of their own — a GitHub
token, a database URL. Add it under the server in the window, or:

```bash
ira mcp env github GITHUB_TOKEN ghp_...
```

Values go to the keyring, never to a file, and a variable with no value is not
passed at all rather than passed empty. A hosted server that wants OAuth instead
gets a **Sign in** button; the token lands in the keyring and refreshes itself.

**Try a tool before you talk to her.** Every connected tool has a *Try it* box
in the window — typed arguments, raw result. Finding out a server is
misconfigured mid-sentence is the worst time to find out.

Servers, their per-tool policy and which skills are on live in `ira.local.db`.
If you have an old `ira.toml`, it is imported once on the first start and then
never read again ([decisions/0017](docs/decisions/0017-servers-and-skills-are-configured-in-the-window.md)).

### From a terminal

Everything the window does, for provisioning a machine or reaching one over SSH:

```bash
ira mcp add github stdio npx -y @modelcontextprotocol/server-github
```

`ira mcp ls · add · env · rm` and `ira skill ls · add · on · off · rm`. These
write the database and connect nothing — a server added here comes up at the
next start. They do not ask before saving a command either, because a terminal
on this machine already is the authorisation.

`ira fetch` downloads the models, the voice and piper, and `ira fetch
--whisper` adds local speech-to-text on top. A first start runs both by itself
when the files are missing, so this is the way to retry after a download
stopped part-way.

## Talking to IRA from something else

She is not only a thing that calls tools; she is a thing your tools can call.

```bash
curl -X POST http://127.0.0.1:8180/say -H 'Content-Type: application/json' -d '{"text": "The build finished."}'
```

A pip sounds immediately and the words wait until she next has the floor — the
same path a finished background job takes, so a deploy that lands mid-sentence
never interrupts you. `GET /state` is a poll for what she is doing; `GET /events`
is the live stream and is what the screen and the orb both read.

Both are guarded like the talk button: a browser claiming to be elsewhere is
refused, a client that says nothing — curl, a CI job — is not. Neither can run
anything. The route that *can*, `POST /settings/admin`, is stricter. Full table:
[SPEC.md](docs/SPEC.md#the-http-surface).

Setting a tool to run in the background detaches the work: IRA answers immediately, a soft pip
sounds when it finishes, and the words wait until she next has the floor.

### Wingman

[Wingman](https://github.com/vedantnimbarte/wingman) is a terminal coding
agent, and the one capability that is not an MCP server you can add: it is an MCP
*client*, not a server, so IRA speaks its HTTP API directly
([decisions/0012](docs/decisions/0012-wingman-is-a-built-in-not-an-mcp-shim.md)).

```powershell
wingman serve                       # defaults to port 8787
$env:IRA_WINGMAN_URL = "http://127.0.0.1:8787

... (truncated, 16655 more characters)

## Cargo.toml

```
[package]
name = "ira"
version = "0.4.0"
edition = "2021"
license = "MIT"

# The icon, compiled into the executable. Windows asks the binary for it --
# the taskbar and alt-tab never see the installer's shortcut. Host-gated
# because it needs rc.exe, and because no other platform has resources.
[target.'cfg(windows)'.build-dependencies]
winresource = "0.1"

[dependencies]
anyhow = "1"
tokio = { version = "1", features = ["rt-multi-thread", "macros", "sync", "time", "io-util", "process", "signal"] }
tokio-util = "0.7"
cpal = "0.18"
rodio = "0.22"
ort = "=2.0.0-rc.13"
reqwest = { version = "0.13", features = ["json", "stream", "multipart"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
futures-util = "0.3"
# Object-safe async trait methods: `dyn Tool` needs a boxed future, and both
# Wingman and Echo already use this crate for the same reason.
async-trait = "0.1"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
toml = "0.8"
rmcp = { version = "3", default-features = false, features = ["client", "transport-child-process", "transport-streamable-http-client", "transport-streamable-http-client-reqwest", "auth"] }
keyring = { version = "4.2.0", features = ["apple-native-keyring-store"] }
rusqlite = { version = "0.40.2", features = ["bundled"] }
# Checking the whisper.cpp archives before running what is in them. Already in
# the tree through oauth2 and wry, so this adds no crate.
sha2 = "0.10"

# The orb, an always-on-top overlay. Windows-only on purpose: the event loop
# runs on a spawned thread, which is a Windows affordance, and a target-specific
# dependency also keeps webkit2gtk out of the Linux CI job for a feature that
# platform does not get. decisions/0013.
# espeak-ng is loaded from beside piper at run time; see kokoro.rs. Already in
# the tree.
[target.'cfg(unix)'.dependencies]
libc = "0.2"

[target.'cfg(windows)'.dependencies]
# The orb, an always-on-top overlay. Windows-only on purpose, and a
# target-specific dependency keeps all of it out of the Linux CI job for a
# feature that platform does not get. decisions/0013.
#
# The orb is drawn, not rendered: a webview window cannot be made transparent,
# and a transparent window is the whole point of an overlay. tiny-skia is a
# pure-Rust rasteriser with no C dependency and no build step, and between them
# these two are a far smaller tree than the webview stack they replace -- the
# window itself is ~120 lines of Win32 rather than a windowing crate.
tiny-skia = "0.11"
windows-sys = { version = "0.61", features = [
    "Win32_Foundation",
    "Win32_Graphics_Gdi",
    # Closing the console an installed IRA was given, and pointing what she
    # would have printed at a log file first. See console.rs.
    "Win32_Storage_FileSystem",
    "Win32_System_Console",
    # Tying whisper-server to IRA's lifetime however she exits. See whisper.rs.
    "Win32_System_JobObjects",
    "Win32_Security_Credentials",
    "Win32_System_LibraryLoader",
    # The local UTC offset, for reminders set "at 3pm" and the clock. See remind.rs.
    "Win32_System_Time",
    "Win32_UI_HiDpi",
    "Win32_UI_Controls",
    "Win32_UI_Input_KeyboardAndMouse",
    "Win32_UI_WindowsAndMessaging",
] }
# The settings window, and only that. The orb cannot be a webview because a
# webview window cannot be transparent (decisions/0013); a settings window has
# no such requirement, and hand-drawing text fields is building a GUI toolkit.
# No windowing crate with it: wry attaches to any `HasWindowHandle`, and the orb
# thread already owns a Win32 window and message loop to hang one on.
wry = "0.55"
raw-window-handle = "0.6"

```

## Top-level layout

- .gitattributes (~11 lines)
- .github/ (dir, 2 files, ~450 lines)
- .gitignore (~27 lines)
- assets/ (dir, 6 files, ~316 lines)
- build.rs (~27 lines)
- Cargo.lock (~5493 lines)
- Cargo.toml (~81 lines)
- corpus/ (dir, 1 files, ~0 lines)
- docs/ (dir, 28 files, ~3714 lines)
- LICENSE (~21 lines)
- packaging/ (dir, 3 files, ~177 lines)
- README.md (~593 lines)
- scripts/ (dir, 3 files, ~340 lines)
- src/ (dir, 30 files, ~17066 lines)
- tests/ (dir, 1 files, ~240 lines)

