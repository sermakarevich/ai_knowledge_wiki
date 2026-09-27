> [[index|Wiki]] | [[summary|Summary]]

# vedantnimbarte/IRA — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** IRA is a voice assistant you can interrupt, piping wake word → endpointing → speech-to-text → streaming model → streaming speech with barge-in, tool calls, and an on-screen display in a single process.

- IRA's whole pipeline is wake word → endpointing → speech-to-text → streaming model → streaming speech with barge-in, tool use, spoken confirmation before state changes, and a screen showing what it is doing (README.md:18).
- The design bet is that turn-taking is the feature: a slower model that yields the floor correctly beats a smarter one that talks over you (README.md:22).
- Everything runs in one process sharing a single cancellation token across transcription, generation, and playback, so interrupting is one `cancel()` that drops the HTTP stream and clears the audio queue in the same frame (README.md:143).
- A turn is a state machine — Idle (openWakeWord 3-stage ONNX) → Listening (Silero VAD, 32 ms chunks; 200 ms pause starts STT, 700 ms silence ends the turn) → Holding (model streams → sentences → Piper → rodio, barge-in armed, duck-then-cut) → optional Confirming (spoken yes/no, anything else is no) → 2 s open floor → Idle (README.md:117).
- Anything that changes state asks out loud first and only an explicit yes runs it; silence, ambiguity, and interrupting the question are all refusals, and a tool's own self-description is never trusted for the read-only gate (README.md:186).
- Tools are a Rust `impl Tool` or an MCP server added in the settings window/orb, indistinguishable to the registry and the model; Wingman is the one exception, spoken over its HTTP API directly because it is an MCP client rather than a server (README.md:172).

## 2. [[wiki/02-top-level-files|Top-level files]]

**In one sentence:** Repo-level hygiene plus Windows packaging: line-ending and binary rules, ignores for build/model/runtime artifacts, and a Windows-only build script that embeds the orb-rendered icon into the executable.

- `.gitattributes` forces every text file to LF in the repo via `* text=auto`, so a clone on another OS or in CI cannot rewrite line endings and turn a one-line change into a whole-file diff (.gitattributes:12).
- `.gitattributes` marks `*.ico`, `*.png`, and `*.icns` as `binary` because `text=auto` would otherwise guess "text" and corrupt the rendered icons by rewriting line endings inside the image data (.gitattributes:18).
- `.gitignore` excludes the Rust build output (`/target`) and wingman's own state directory (`.wingman/`, holding its index, sessions, and memory) (.gitignore:25, .gitignore:44).
- Model weights fetched by `scripts/fetch-models.ps1` — `/models/*.onnx`, `/models/*.onnx.json`, `/models/*.bin`, plus `/piper/` and `/whisper/` (~6 MB of weights) — are ignored as fetched artifacts, not source (.gitignore:29).
- Files IRA writes at runtime are ignored: `/transcript.jsonl` (the record of conversations), `/ira.log` (written when she starts from a shortcut and closes her own console; see `src/console.rs`), and `/ira.local.db` plus its `-journal` (this machine's URLs and model ids written by the settings window — not keys, which go to the OS keyring) (.gitignore:33, .gitignore:36, .gitignore:41).
- Release-packaging outputs built by `.github/workflows/release.yml` into the working directory (`/*.msi`, `/*.deb`, `/*.dmg`, `/IRA.app/`, `/*.iconset/`) are ignored (.gitignore:47).
- `build.rs` does nothing except on Windows (`#[cfg(windows)]`): it re-runs when `assets/ira.ico` changes and embeds that icon via `winresource::WindowsResource::set_icon`, because Windows reads taskbar/alt-tab/Explorer/Start-menu icons out of the binary itself, so a shortcut-level icon would still leave a generic gear everywhere else (build.rs:71, build.rs:75).
- A missing resource compiler is a warning, not a fatal error: if `res.compile()` fails (needs `rc.exe` from the Windows SDK), the build emits `cargo:warning=no icon embedded` and still produces an IRA with a plain icon (build.rs:79).

## The system in five moves

1. The repo keeps only source: line endings are pinned to LF, rendered icons are guarded as binary, and builds, fetched weights, runtime state, and release packages are all ignored rather than committed.
2. A first start fetches wake, voice, and speech models, stores keys in the OS keyring and machine settings in SQLite, and preflights models, microphone, and keys before ever opening the mic.
3. Each turn is a state machine — wake word idles, VAD-gated listening endpoints the utterance, transcription overlaps the silence wait, and the model streams sentences straight into speech synthesis and playback.
4. Interruption is structural, not bolted on: one process shares one cancellation token across transcription, generation, and playback, so barge-in is a single cancel that drops the stream and clears the audio queue in the same frame.
5. Capability arrives through one tool registry — a Rust impl, an MCP server, or Wingman's HTTP API — with every state-changing call gated behind an explicit spoken yes.
6. Everything stays visible and reachable: the screen and orb read one event stream, the HTTP surface exposes speech triggers and state, and the orb-rendered icon is embedded into the Windows binary so packaging matches what is on screen.
