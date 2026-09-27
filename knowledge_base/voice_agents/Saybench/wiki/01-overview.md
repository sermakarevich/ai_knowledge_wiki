> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** saybench benchmarks the voice-AI pipeline on your own audio, accents, jargon, and providers to produce accuracy, latency, and cost numbers plus a CI regression gate (README.md:9-11).
## Key points
- Benchmarks your voice-AI pipeline on your audio rather than vendor lab audio, reporting accuracy per failure mode, live-call latencies, and cost (README.md:9-11).
- Exposes five benchmark modes — `stt`, `stream`, `llm`, `s2s`, `tts` — each with an offline `fake` provider so every mode runs with zero keys (README.md:26-34).
- Standardizes cross-mode trust and workflow: honest scoring doctrine, JSON reports with `compare` regression gate and HTML dashboard, multi-vendor providers plus `custom` escape hatch, MCP server, and Pipecat mapping (README.md:36-42).
- Publishes reproducible golden-set findings where aggregate rankings invert per failure mode and batch vs streaming latency gaps diverge (README.md:44-52).
- Ships as a single static Go binary via `go install github.com/renan-martini/saybench/cmd/saybench@latest` or `go build ./cmd/saybench` (README.md:55-59).
- Runs a fixed workflow: zero-key `fake` smoke test, env-only keys for real vendors, JSONL manifest for own clips, `compare -max-wer-regression` CI gate, `show`/`html` for review (README.md:63-82).
- Enforces design principles: stdlib plus exactly one dependency (`coder/websocket`), env-only keys, deadlines plus size-bounded reads, deterministic fakes/ordering/schema, and `—` instead of flattering zeros (README.md:103-109).
---
## Benchmark modes
Five modes, one per voice-pipeline failure point, each with an offline `fake` provider (README.md:26-27):

| Mode | Command | The numbers that matter |
|---|---|---|
| [Batch STT](docs/stt.md) | `saybench stt` | corpus WER with sub/del/ins breakdown, per-failure-mode categories, keyterm recall, round-trip latency |
| [Streaming STT](docs/streaming.md) | `saybench stream` | time-to-first-partial, finalization lag, interim word survival — fed at real-time pace |
| [LLM turn](docs/llm.md) | `saybench llm` | time-to-first-token, completion time, tok/s — warm by default, SSE vs WebSocket as a dimension |
| [Speech-to-speech](docs/s2s.md) | `saybench s2s` | voice-to-voice latency, echo comprehension scoring, barge-in stop time |
| [TTS](docs/tts.md) | `saybench tts` | time-to-first-audio-byte, synthesis time, audio duration |

Example invocation and real output shape (README.md:13-22):

```
$saybench stt -providers fake,deepgram,openai -manifest golden/manifest.jsonl -report today.json

PROVIDER                       CLIPS  ERRORS  WER    KEYTERM RECALL  AVG LATENCY  P95 LATENCY
deepgram:nova-3                14     0       3.8%   93.5%           926ms        2139ms
fake                           14     0       16.5%  67.7%           47ms         73ms
openai:gpt-4o-mini-transcribe  14     0       19.0%  74.2%           1319ms       1930ms
```

## Cross-cutting capabilities
Across all modes (README.md:36-42):

- **[Scoring you can trust](docs/scoring.md)** — corpus-level WER, keyterm recall, opt-in digit normalization, opt-in LLM-judge beside WER, and `—` where there is no data.
- **[Reports, compare, dashboard](docs/reports.md)** — JSON everything, CI gate (`compare -max-wer-regression`), condition-aware warnings, single-file HTML dashboard.
- **[Providers](docs/providers.md)** — Deepgram, OpenAI, AssemblyAI, ElevenLabs, Gemini Live, OpenRouter, Groq, plus a `custom` escape hatch per mode; adding one is a two-method interface.
- **[MCP server](docs/mcp.md)** — `saybench mcp` exposes the whole tool to coding agents over stdio.
- **[Pipecat guide](docs/pipecat.md)** — map each pipeline service to its saybench equivalent.

## Published findings
Reproducible results from the bundled golden set against live APIs, September 2026 (README.md:22-22, README.md:44-52):

- Vendors invert per failure mode: the 19%-WER vendor beat the 3.8% one on acronyms, names, and conversational speech; a third of its errors were digit formatting.
- Time-to-first-partial gap is 5× between two vendors ~400ms apart in batch.
- Cold TLS is a ~3× TTFT effect (1109ms → 595ms warm); warm WebSocket transport buys nothing at voice-turn sizes.
- Speech-native model first audio (601ms avg) beats the composed pipeline floor (~808ms before TTS); it talks 12.4s per reply and sometimes performs an echo request instead of echoing it.

## Install
Verbatim (README.md:55-59):

```
go install github.com/renan-martini/saybench/cmd/saybench@latest
```

Or clone and `go build ./cmd/saybench`. Single static binary.

## Quickstart workflow
Verbatim workflow (README.md:63-82):

```bash
# 1. Zero-key smoke test with the offline fake provider and bundled corpus:
saybench stt -providers fake

# 2. Real vendors — keys come from the environment, never from files or flags:
export DEEPGRAM_API_KEY=...
export OPENAI_API_KEY=...
saybench stt -providers deepgram,openai -report baseline.json

# 3. Your own audio: write a JSONL manifest next to your clips…
#    {"audio":"clips/refund-call.wav","reference":"I want a refund for order four two nine","category":"numbers"}
saybench stt -providers deepgram -manifest my-corpus/manifest.jsonl -report today.json

# 4. Catch regressions — in CI, fail if any provider got >2 points worse:
saybench compare baseline.json today.json -max-wer-regression 2.0

# 5. Revisit any saved report, or render a set of them into a dashboard:
saybench show today.json
saybench html -o dashboard.html baseline.json today.json
```

Exact flag/parameter names used here are `-providers`, `-manifest`, `-report`, `-max-wer-regression`, `-o`; other modes follow the same pattern as `saybench stream|llm|s2s|tts -providers/-targets …` (README.md:76-84).

## Documentation map
Verbatim index (README.md:88-101):

| Page | What's in it |
|---|---|
| [docs/stt.md](docs/stt.md) | Batch STT, the manifest format, the golden set, what one real run teaches |
| [docs/streaming.md](docs/streaming.md) | Streaming STT: TTFP, finalization lag, interim word survival |
| [docs/llm.md](docs/llm.md) | LLM TTFT, warmup, SSE-vs-WebSocket transport |
| [docs/s2s.md](docs/s2s.md) | Speech-to-speech: voice-to-voice latency, echo comprehension, barge-in |
| [docs/tts.md](docs/tts.md) | TTS time-to-first-audio |
| [docs/scoring.md](docs/scoring.md) | The scoring doctrine: WER, keyterms, normalization, judge, conditions |
| [docs/providers.md](docs/providers.md) | Every provider spec, key, and override; the verification ladder; adding your own |
| [docs/reports.md](docs/reports.md) | JSON reports, `show`, `compare` + CI gate, the dashboard, cost columns |
| [docs/mcp.md](docs/mcp.md) | The MCP server for coding agents |
| [docs/pipecat.md](docs/pipecat.md) | Benchmarking a Pipecat stack |
| [ROADMAP.md](ROADMAP.md) | The shipped log — what each version added and why |
| [CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) | Contribution rules · key handling |

## Design principles and license
Principles (README.md:103-109):

- Standard library plus exactly one dependency — `coder/websocket` (itself dependency-free).
- Keys from the environment only — never flags, never config files, never logs.
- Every network call has a deadline; every response read is size-bounded.
- Deterministic where possible — fake providers, result ordering, and report schema are stable.
- Honest numbers — real output only, `—` over fake zeros, conditions recorded and warned about.

License is MIT (README.md:111-113). No truncated files were noted in the chunk.

**Covers:** README.md (repo root overview, modes, findings, install, quickstart, principles); referenced docs index docs/stt.md, docs/streaming.md, docs/llm.md, docs/s2s.md, docs/tts.md, docs/scoring.md, docs/providers.md, docs/reports.md, docs/mcp.md, docs/pipecat.md; ROADMAP.md, CONTRIBUTING.md, SECURITY.md, LICENSE
