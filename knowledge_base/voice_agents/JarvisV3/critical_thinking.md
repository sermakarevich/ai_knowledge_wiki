> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: CarverXx/jarvis-v3

## Claims vs. evidence
- Claim: fully local voice loop (LLM, ASR, TTS on-host; only Tavily web search leaves the box).
- Evidence: strong. Service table names SGLang :8000, Qwen3-ASR :8002, VoxCPM2 :8003,
  Hermes shim :8004, MCP tools :8005, and `requirements.txt` pins the matching stack.
- Claim: one LLM cannot be both fast and smart, so cognition splits into a fast
  Subconscious speaker and a Hermes tool executor.
- Evidence: moderate. Two worked turns ground it: "你好" answers directly (~300 ms,
  no tool call); "今天天气" escalates via `invoke_hermes(task=...)` → `web.search`
  → 2-sentence spoken reply. Latency targets (TTFB < 1 s vs. 5–30 s) are stated,
  but no histograms, benchmarks, or ablations are captured.
- Claim: end-to-end pipeline works with autoresume and studio-grade cloning
  (SIGKILL + autoresume tested; VoxCPM2 RMS stddev < 1 dB).
- Evidence: weak. These are status-list assertions; the status list itself ends in a
  truncated empty bullet, and no test log or measurement method is recorded.
- Claim: personalisation without code edits (4–8 s voice clip, 20-sample wake
  verifier, two prompt env vars).
- Evidence: moderate. Exact scripts and artefacts are named (`trim_voice_ref.py`,
  `split_wake_recording.py`, `train_wake_verifier.py`, `hey_jarvis_verifier.pkl`),
  but no recall/precision numbers are given.
- Claim: echo-safe turn-taking (mic mute during TTS, queue flush, cooldowns).
- Evidence: moderate. The `config.py` comment recording the 2026-04-19 fix
  (`POST_TTS_GRACE_MS` 500→800 after TTS-echo "在 spam" retrigger) reads as genuine
  field-hardening rather than designed proof.
- Docs drift flag: "5 systemd services" stated, 6 rows listed including the daemon;
  `docs/customize.md` is a TODO and several paths are referenced-only.

## Genuinely new vs. repackaged
- Genuinely useful: the Subconscious-as-router pattern — a fast LLM whose only tool
  is `invoke_hermes(task=...)` — cleanly separates sub-second chatter from 40–90 s
  agent loops hidden behind a 2 s heartbeat beep.
- Genuinely practical: voice-loop tuning written down as numbers with reasons —
  32 ms chunks matching the Silero frame size, `MIC_INPUT_GAIN=2.5` with soft-clip,
  VAD gates 0.5/0.7, `EOS_SILENCE_S=0.5`, `MIN_UTTERANCE_S=0.3`,
  `FOLLOWUP_WINDOW_S=15.0`, 1.5 s wake cooldown.
- Genuinely operable: a 6-panel `rich.Live` TUI tailing a JSONL event stream
  (state, mic/wake sparkline, ASR, Subconscious tokens, Hermes pulse, TTS bar).
- Repackaged: per-model FastAPI shims on adjacent ports, systemd units,
  `.gitignore` hygiene, and env-driven `config.py` explicitly copied from jarvis-v2.
- Repackaged: MCP namespaces (`fs`/`rag`/`web`/`cf`/`system`), keyword
  `rag.search` + `fs.read` over a Markdown vault, and commodity ASR/LLM/TTS models.
- Net: a well-documented hobbyist build log with production-flavoured operability,
  not novel models or measured research.

## Weaknesses and blind spots
- Hardware moat: ~50 GB VRAM minimum, 96 GB tested (RTX PRO 6000 Blackwell),
  8–16 cores, 32–96 GB RAM, Linux + PulseAudio/PipeWire only. No small-GPU story;
  14B fallbacks are admitted with a quality hit.
- Single-box brittleness: fixed ports, `~/models` paths, and device-name hints
  (`MIC_DEVICE_HINT="Poly Sync"`) make every new machine a hand-editing exercise.
  No container, health-check, or failover topology is described.
- Narrow envelope: the system prompt explicitly refuses calendar, mail,
  iMessage/WeChat, smart-home, music, calls, meetings, and booking — the tasks
  that would justify an always-on assistant.
- Thin retrieval: keyword `rag.search`, `SUBCONSCIOUS_HISTORY_N=6`,
  `HERMES_MAX_REPLY_CHARS=500` — adequate for wiki Q&A, inadequate for large,
  versioned, or permissioned corpora.
- Fragile failure protocol: only three parenthesised prefixes count as tool
  failure; all other tool output is "trusted fact". Injection, mis-summary, and
  fabricated-realtime risks are unaddressed.
- Manual safety: secrets protection is a `.gitignore` plus a "run the audit script
  before pushing" comment — no hook, no scan gate, no test suite mentioned.

## Applicability
- Direct reuse fits only a Linux workstation with a large GPU and tolerance for a
  Chinese-first persona and 5–120 s tool turns (`HERMES_TIMEOUT_S=120`).
- Transferable value is the pattern catalogue: router-plus-executor, echo-safe
  audio state machine, verifier-based wake personalisation, JSONL-event dashboard.
- **Relevance to my work**
  - AI/ML engineering: adopt the env-centralised config contract, the pin-rationale
    comments (e.g. `openwakeword==0.4.0` avoiding missing `tflite-runtime` wheels),
    and the "one tunable per incident" documentation habit.
  - Agentic systems: trial the single-escalation-tool router, heartbeat-during-tools
    UX, 1–2 sentence spoken-summary cap, and explicit refuse-lists over silent
    hallucination.
  - Elisity data platform: do not port the voice stack; do port the operability
    shape — JSONL event stream with live panels, session-id resume mapping,
    per-component error tags, and runbook-RAG as a stepping stone to vector search.

## What this changes
- Reframes local assistants as a latency-routing problem, not a bigger-model
  problem: keep a fast speaker in front, hide the slow agent behind one tool call.
- Raises the bar for build logs: every magic number ships with the failure
  (noise triggers at v2's 0.40 threshold, TTS-echo spam) that motivated it.
- Does not change the economics: 50 GB+ VRAM, single-user, single-box, and a
  refuse-list over mainstream tasks keep this a reference design, not a platform.

## Verdict
- A sharp field manual for dual-brain routing and voice-loop hardening, but not
  adoptable as a system given hardware, OS, language, and capability constraints.
- Trial the router, echo-discipline, and TUI patterns in isolation on real tasks;
  leave the full six-service stack alone until a lighter, tested revision appears.
- Call: **watch**
