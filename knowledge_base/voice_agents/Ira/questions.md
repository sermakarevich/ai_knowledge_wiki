---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: vedantnimbarte/IRA

### Q1. What is IRA's end-to-end voice pipeline, and what is its core design bet?

> [!tip]- Answer
> IRA pipes wake word → endpointing → speech-to-text → streaming model → streaming speech, with barge-in, tool calls, spoken confirmation before state changes, and an on-screen display in a single process. Its design bet is that turn-taking is the feature: a slower model that yields the floor correctly beats a smarter one that talks over you. Speech recognition is treated as solved; being interruptible is what stays broken. See [[wiki/01-overview|Overview]].

### Q2. How does a single turn move through IRA's state machine?

> [!tip]- Answer
> A turn runs Idle (openWakeWord 3-stage ONNX) → Listening (Silero VAD on 32 ms chunks; a 200 ms pause starts STT, 700 ms of silence ends the turn) → Holding (model streams sentences into Piper and rodio playback with barge-in armed) → optional Confirming → a 2 s open floor → Idle. Transcription overlaps the silence wait, and thinking and speaking are one streaming path in Holding. A spoken yes or no resolves Confirming, with anything else counting as no. See [[wiki/01-overview|Overview]].

### Q3. How does IRA implement barge-in, and why must it be a single process?

> [!tip]- Answer
> Everything runs in one process sharing a single cancellation token across transcription, generation, and playback, so interrupting is one `cancel()` that drops the HTTP stream and clears the audio queue in the same frame. Holding arms barge-in the whole time, ducking audio at a hint of speech and cutting when confirmed. The single process exists because one process must hold the microphone and speaker simultaneously for this to work. See [[wiki/01-overview|Overview]].

### Q4. What is IRA's confirmation gate for tools, and how do tools get added?

> [!tip]- Answer
> Anything that changes state asks out loud first and only an explicit yes runs it; silence, ambiguity, and interrupting the question all count as refusals, and a tool's own self-description is never trusted for the read-only gate. Tools are a Rust `impl Tool` or an MCP server added in the settings window or orb, indistinguishable to the registry and the model. Wingman is the one exception, spoken over its HTTP API directly because it is an MCP client rather than a server. See [[wiki/01-overview|Overview]].

### Q5. What does IRA ignore at the repo top level, and why?

> [!tip]- Answer
> `.gitignore` excludes Rust build output (`/target`), fetched model weights (`/models/*.onnx`, `/piper/`, `/whisper/`), and runtime-written files such as `/transcript.jsonl`, `/ira.log`, and `/ira.local.db`, plus release-packaging outputs like `*.msi` and `*.deb`. The rule is that the repo keeps only source: builds, fetched weights, per-machine state, and release artifacts are never committed. Keys additionally stay out of files entirely, living in the OS keyring instead. See [[wiki/02-top-level-files|Top-level files]].

### Q6. What do `.gitattributes` and `build.rs` do at the repo top level?

> [!tip]- Answer
> `.gitattributes` pins every text file to LF via `* text=auto` and marks `*.ico`, `*.png`, and `*.icns` as binary so line-ending normalization cannot corrupt rendered icons. `build.rs` acts only on Windows, embedding `assets/ira.ico` into the binary because Windows reads taskbar and Explorer icons from the executable itself. A missing resource compiler is only a warning, so the build still succeeds with a plain icon. See [[wiki/02-top-level-files|Top-level files]].

### Q7. Would you recommend IRA's interruptible single-process architecture for a new voice assistant, and why?

> [!tip]- Answer
> Yes, where natural turn-taking matters more than raw model intelligence, because one shared cancellation token makes barge-in structural instead of bolted on. The trade-off is platform complexity: no echo cancellation means headphones or press-to-talk, and the single-process constraint shapes every other decision. Recommend it for conversational control tasks, not for settings where maximal model quality outweighs interruption handling. See [[wiki/01-overview|Overview]].
