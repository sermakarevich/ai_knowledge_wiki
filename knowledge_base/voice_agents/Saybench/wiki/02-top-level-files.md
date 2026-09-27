> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** Repo-root guardrails and history — AI-work rules, security posture, build ignores, the single dependency pin, and the shipped-version roadmap.
## Key points
- AI sessions are bound by the same contribution rules as humans, with stdlib-only, no-secrets, deadline-plus-bounded-read, clean-gate, real-output, honest-metrics, and original-audio constraints (CLAUDE.md:5-17).
- Security posture is env-only API keys never written to reports/logs or echoed in errors, per-item deadlines plus `io.LimitReader`, 100 MiB audio / 1 MiB manifest caps, and zero runtime dependencies (SECURITY.md:12-20).
- Vulnerability reports go to **renan.martiniduarte@gmail.com** with a one-week reply promise and no public issue for sensitive items (SECURITY.md:5-9).
- The build ignores the compiled binary, local JSON reports, distribution output, audio artifacts, and macOS metadata (`.gitignore:1-5`).
- The module pins exactly one dependency, `github.com/coder/websocket v1.8.15`, via hash and go.mod hash (go.sum:1-2).
- The roadmap is grounded in real voice-agent stacks (live phone calls, Pipecat + LiveKit pipelines) where order signals intent, not promise, and every shipped item exists because a real system needed it (ROADMAP.md:3-6).
- Shipped history spans v0.1 STT benchmarking through v1.0 TTS/cost/normalize/server-VAD/MCP/Pipecat close-out, with v0.2–v1.1 adding keyterms/dashboard, streaming, interim survival, LLM loop, S2S phases, transport/warmup, judge/barge-in/gemini (ROADMAP.md:8-62).
---
## .gitignore
Verbatim (`.gitignore:1-5`):

```
/saybench
/*.json
/dist/
*.aiff
.DS_Store
```

Ignores the built binary, root-level JSON reports, distribution builds, audio fixtures, and Finder metadata.
## CLAUDE.md
Verbatim rules (CLAUDE.md:1-17):

```
# CLAUDE.md — rules for AI-assisted work in this repo

This is a public repository and a professional work sample. Every commit is on
display. The rules in CONTRIBUTING.md are binding for AI sessions too; the ones
that matter most:

- **Stdlib only.** Do not add dependencies without an explicit human decision.
- **No secrets anywhere** — not in code, tests, fixtures, docs, or examples.
  Example keys in docs are `...`, never realistic-looking values.
- **Every HTTP call: context deadline + `io.LimitReader`.** No exceptions.
- **`gofmt -l .`, `go vet ./...`, `go test -race ./...` clean before any commit.**
- **README and docs/ examples must be real output**, pasted from an actual
  run — never hand-written or predicted.
- **Honest metrics framing** (batch vs streaming latency, synthetic vs real
  audio) is a product feature. Don't soften or blur it for marketing effect.
- Golden-set audio must be original: written for this repo and synthesized
  locally. Never copy audio or transcripts from other projects or datasets.
- Report schema changes bump `SchemaVersion` in `internal/report`.
```

| Rule | Exact requirement |
|---|---|
| Dependencies | Stdlib only without explicit human decision |
| Secrets | None in code/tests/fixtures/docs/examples; example keys are `...` |
| HTTP | Context deadline + `io.LimitReader`, no exceptions |
| Pre-commit gate | `gofmt -l .`, `go vet ./...`, `go test -race ./...` clean |
| Docs | README/docs examples are pasted real output only |
| Metrics | Honest batch-vs-streaming / synthetic-vs-real framing |
| Audio | Golden-set audio is repo-original, locally synthesized |
| Schema | Schema change bumps `SchemaVersion` in `internal/report` |
## go.sum
Verbatim (go.sum:1-2):

```
github.com/coder/websocket v1.8.15 h1:6B2JPeOGlpff2Uz6vOEH1Vzpi0iUz20A+lPVhPHtNUA=
github.com/coder/websocket v1.8.15/go.mod h1:NX3SzP+inril6yawo5CQXx8+fk145lPDC6pumgx0mVg=
```

Single pinned dependency and its go.mod hash; consistent with the stdlib-only posture (CLAUDE.md:7) and zero-runtime-dependencies claim (SECURITY.md:17).
## ROADMAP.md
Positioning verbatim (ROADMAP.md:3-6):

```
Grounded in real voice-agent stacks: platforms running live AI phone calls, and
meeting/conversation pipelines built on frameworks like Pipecat + LiveKit. Each
item exists because a real system needed it, not because a benchmark could
measure it. Order is intent, not promise.
```

Shipped log (ROADMAP.md:8-62):

| Version | Shipped |
|---|---|
| v0.1 | STT benchmarking: corpus WER with sub/del/ins, batch avg/p95, failure-mode categories, JSON reports, `compare` CI gate, offline `fake`, clean-room golden set |
| v0.2 | Keyterm recall, `-format json` on every command, self-contained HTML dashboard (A/B compare, WER trends, category/latency charts, worst-clips table) |
| v0.4 | Streaming STT: `saybench stream` at real-time pace over Deepgram live / OpenAI Realtime / AssemblyAI Universal-Streaming; time-to-first-partial, finalization lag, interim count; mode-tagged reports; `compare` refuses cross-mode deltas |
| v0.5 | Interim word survival (fraction of final distinct words previewed by any interim), word-weighted per provider |
| v0.6 | LLM loop: `saybench llm` vs any OpenAI-compatible endpoint (openai / openrouter / groq / custom base URL); TTFT, completion time, decode tok/s |
| v0.9 | S2S phase 2: `-score echo` repeat-back task scored with WER + keyterm recall; echo-vs-conversational is a compare-warned condition |
| v0.8 | S2S phase 1: `saybench s2s` voice-to-voice latency, response-done time, speech-out duration; OpenAI Realtime plus `custom` dialect; deterministic turn ending; per-turn reply transcript |
| v0.7 | Transport dimension (`openai-ws:model` Responses-API WebSocket mode) + `-warmup` default-on unmeasured first request recorded in report, compare-warned warm-vs-cold |
| v1.1 | Deferred items: `-judge` LLM-rated semantic preservation beside WER, s2s `-barge-in` stop-time (implies server_vad), `gemini` S2S adapter (Google Live API / BidiGenerateContent, auto-VAD, refuses `-turn-ending commit`, mock-tested) |
| v1.0 | Close-out: TTS mode (time-to-first-audio, 24 kHz PCM: openai, elevenlabs, custom, fake-tts), user-supplied pricing-table cost columns, `-normalize digits`, s2s `-turn-ending server_vad`, `saybench mcp`, Pipecat guide |

Next-section contributor note verbatim (ROADMAP.md:66-67):

```
### More providers everywhere
Every provider interface in this repo is two methods. PRs welcome.
```

No truncated files were noted in the chunk.
## SECURITY.md
Verbatim (SECURITY.md:1-20):

```
# Security

## Reporting

Found a vulnerability? Email **renan.martiniduarte@gmail.com** — please don't
open a public issue for anything sensitive. You'll get a reply within a week.

## Posture

- **API keys are read from environment variables only** and are never accepted
  via flags or config files, never written to reports or logs, and never echoed
  in error messages.
- **All network calls have deadlines** (per-item context timeout plus an HTTP
  client backstop); response bodies are read through `io.LimitReader`.
- **Input bounds:** audio files are capped at 100 MiB; manifest lines at 1 MiB.
- **Zero runtime dependencies** — the supply-chain surface is the Go standard
  library.
- Reports contain your reference transcripts and hypotheses. If your corpus is
  sensitive, treat report files accordingly — saybench never uploads anything
  anywhere except the audio you explicitly send to the provider you selected.
```

| Control | Exact bound |
|---|---|
| Keys | Env vars only; never flags/files/reports/logs/error echoes |
| Network | Per-item context timeout + HTTP client backstop; `io.LimitReader` bodies |
| Input | Audio ≤ 100 MiB; manifest lines ≤ 1 MiB |
| Supply chain | Zero runtime dependencies (stdlib surface) |
| Data | Reports hold references/hypotheses; uploads only the audio sent to the selected provider |

**Covers:** .gitignore, CLAUDE.md, go.sum, ROADMAP.md, SECURITY.md
