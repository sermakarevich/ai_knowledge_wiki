> [[index|Wiki]] | [[summary|Summary]]
# renan-martini/saybench — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** saybench benchmarks the voice-AI pipeline on your own audio, accents, jargon, and providers to produce accuracy, latency, and cost numbers plus a CI regression gate (README.md:9-11).
- Benchmarks your voice-AI pipeline on your audio rather than vendor lab audio, reporting accuracy per failure mode, live-call latencies, and cost (README.md:9-11).
- Exposes five benchmark modes — `stt`, `stream`, `llm`, `s2s`, `tts` — each with an offline `fake` provider so every mode runs with zero keys (README.md:26-34).
- Standardizes cross-mode trust and workflow: honest scoring doctrine, JSON reports with `compare` regression gate and HTML dashboard, multi-vendor providers plus `custom` escape hatch, MCP server, and Pipecat mapping (README.md:36-42).
- Publishes reproducible golden-set findings where aggregate rankings invert per failure mode and batch vs streaming latency gaps diverge (README.md:44-52).
- Ships as a single static Go binary via `go install github.com/renan-martini/saybench/cmd/saybench@latest` or `go build ./cmd/saybench` (README.md:55-59).
- Runs a fixed workflow: zero-key `fake` smoke test, env-only keys for real vendors, JSONL manifest for own clips, `compare -max-wer-regression` CI gate, `show`/`html` for review (README.md:63-82).
- Enforces design principles: stdlib plus exactly one dependency (`coder/websocket`), env-only keys, deadlines plus size-bounded reads, deterministic fakes/ordering/schema, and `—` instead of flattering zeros (README.md:103-109).

## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** Repo-root guardrails and history — AI-work rules, security posture, build ignores, the single dependency pin, and the shipped-version roadmap.
- AI sessions are bound by the same contribution rules as humans, with stdlib-only, no-secrets, deadline-plus-bounded-read, clean-gate, real-output, honest-metrics, and original-audio constraints (CLAUDE.md:5-17).
- Security posture is env-only API keys never written to reports/logs or echoed in errors, per-item deadlines plus `io.LimitReader`, 100 MiB audio / 1 MiB manifest caps, and zero runtime dependencies (SECURITY.md:12-20).
- Vulnerability reports go to **renan.martiniduarte@gmail.com** with a one-week reply promise and no public issue for sensitive items (SECURITY.md:5-9).
- The build ignores the compiled binary, local JSON reports, distribution output, audio artifacts, and macOS metadata (`.gitignore:1-5`).
- The module pins exactly one dependency, `github.com/coder/websocket v1.8.15`, via hash and go.mod hash (go.sum:1-2).
- The roadmap is grounded in real voice-agent stacks (live phone calls, Pipecat + LiveKit pipelines) where order signals intent, not promise, and every shipped item exists because a real system needed it (ROADMAP.md:3-6).
- Shipped history spans v0.1 STT benchmarking through v1.0 TTS/cost/normalize/server-VAD/MCP/Pipecat close-out, with v0.2–v1.1 adding keyterms/dashboard, streaming, interim survival, LLM loop, S2S phases, transport/warmup, judge/barge-in/gemini (ROADMAP.md:8-62).

## The system in five moves
1. Benchmark your own voice-AI pipeline on your own audio — accents, jargon, failure modes — instead of trusting vendor lab numbers.
2. Cover all five pipeline failure points (batch STT, streaming STT, LLM turn, speech-to-speech, TTS), each runnable offline with zero keys via the fake provider.
3. Standardize trust across modes with honest scoring, JSON reports, a compare regression gate, and an HTML dashboard.
4. Ship it as a single static Go binary with env-only keys, deadline-plus-bounded reads, and deterministic fakes, ordering, and schema.
5. Hold the whole effort inside repo-root guardrails — AI-work rules, env-only security posture, one pinned dependency, and a roadmap grounded in real voice-agent stacks.
