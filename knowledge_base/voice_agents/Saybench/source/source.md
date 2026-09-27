> PDF location (no bundled PDF): https://github.com/renan-martini/saybench

# renan-martini/saybench
Source: https://github.com/renan-martini/saybench
Kind: repo
Fetched: 2026-09-22T14:40:33.434809+00:00
Tool: git-clone

# renan-martini/saybench

Commit: 0d61233b21503c4024424f45d125ad29a09497cf

## README

# saybench

**Benchmark the voice-AI pipeline on *your* audio, not a vendor's lab.**

Every vendor publishes benchmarks showing they're the fastest and most accurate. None of them ran on your audio, your accents, your jargon, or your phone-line quality — and none of them will tell you when an API update quietly makes *your* pipeline worse. saybench does: point it at your providers and your clips, get the numbers that decide whether a voice agent feels good — accuracy per failure mode, the latencies a live call actually feels, cost — and wire the regression gate into CI so a degradation fails the build before your users notice.

```
$ saybench stt -providers fake,deepgram,openai -manifest golden/manifest.jsonl -report today.json

PROVIDER                       CLIPS  ERRORS  WER    KEYTERM RECALL  AVG LATENCY  P95 LATENCY
deepgram:nova-3                14     0       3.8%   93.5%           926ms        2139ms
fake                           14     0       16.5%  67.7%           47ms         73ms
openai:gpt-4o-mini-transcribe  14     0       19.0%  74.2%           1319ms       1930ms
```

*(Real output: the bundled golden set against live vendor APIs, September 2026 — plus the offline `fake` provider that runs with zero keys. Your audio will rank them differently; that is the point of the tool. The full run, per-category breakdown included, is in [docs/stt.md](docs/stt.md).)*

## What it measures

Five benchmark modes, one for each place a voice pipeline can be slow, wrong, or expensive — each with an offline `fake` provider so everything runs with zero keys:

| Mode | Command | The numbers that matter |
|---|---|---|
| [Batch STT](docs/stt.md) | `saybench stt` | corpus WER with sub/del/ins breakdown, per-failure-mode categories, keyterm recall, round-trip latency |
| [Streaming STT](docs/streaming.md) | `saybench stream` | time-to-first-partial, finalization lag, interim word survival — fed at real-time pace |
| [LLM turn](docs/llm.md) | `saybench llm` | time-to-first-token, completion time, tok/s — warm by default, SSE vs WebSocket as a dimension |
| [Speech-to-speech](docs/s2s.md) | `saybench s2s` | voice-to-voice latency, echo comprehension scoring, barge-in stop time |
| [TTS](docs/tts.md) | `saybench tts` | time-to-first-audio-byte, synthesis time, audio duration |

And across all of them:

- **[Scoring you can trust](docs/scoring.md)** — corpus-level WER, keyterm recall (did the customer's *name* survive?), opt-in digit normalization, opt-in LLM-judge scoring beside WER (never replacing it), and `—` where there's no data, never a flattering 0%.
- **[Reports, compare, dashboard](docs/reports.md)** — JSON everything, a CI regression gate (`compare -max-wer-regression`), condition-aware warnings (warm vs cold, echo vs conversational…), and a single-file HTML dashboard.
- **[Providers](docs/providers.md)** — Deepgram, OpenAI, AssemblyAI, ElevenLabs, Gemini Live, OpenRouter, Groq, and a `custom` escape hatch per mode for any compatible or self-hosted endpoint. Adding one is a two-method interface.
- **[MCP server](docs/mcp.md)** — `saybench mcp` exposes the whole tool to coding agents over stdio.
- **[Pipecat guide](docs/pipecat.md)** — map each service in your pipeline to its saybench equivalent.

## What real runs found

Published, reproducible findings from the bundled golden set against live APIs (each linked page has the full tables):

- Vendors **invert per failure mode**: the 19%-WER vendor beat the 3.8% one on acronyms, names, and conversational speech — and a third of its "errors" were digit formatting, not mishearing. → [stt](docs/stt.md)
- The **time-to-first-partial gap is 5×** between two vendors that were ~400ms apart in batch. → [streaming](docs/streaming.md)
- **Cold TLS is a ~3× TTFT effect** (1109ms → 595ms warm) — and warm, WebSocket transport buys nothing at voice-turn sizes. → [llm](docs/llm.md)
- A speech-native model's **first audio (601ms avg) beats the composed pipeline's floor** (~808ms before TTS even starts) — but it talks 12.4s per reply, and when told to echo a request it sometimes *performs* it instead. → [s2s](docs/s2s.md)

## Install

```
go install github.com/renan-martini/saybench/cmd/saybench@latest
```

Or clone and `go build ./cmd/saybench`. Single static binary.

## Quickstart

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

The other modes work the same way: `saybench stream|llm|s2s|tts -providers/-targets …` — each mode's page has its flags, its vendors, and its published results.

## Documentation

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

## Design principles

- **Standard library plus exactly one dependency** — [`coder/websocket`](https://github.com/coder/websocket) (itself dependency-free), because streaming vendors speak WebSocket and the stdlib doesn't. Anything else needs a reason the stdlib can't answer.
- **Keys from the environment only** — never flags, never config files, never logs. See [SECURITY.md](SECURITY.md).
- **Every network call has a deadline**; every response read is size-bounded.
- **Deterministic where possible** — the fake providers, result ordering, and report schema are all stable so diffs mean something.
- **Honest numbers** — real output only in the docs, `—` over fake zeros, conditions recorded and warned about. The full doctrine: [docs/scoring.md](docs/scoring.md).

## License

MIT — see [LICENSE](LICENSE).


## go.mod

```
module github.com/renan-martini/saybench

go 1.25

require github.com/coder/websocket v1.8.15

```

## Top-level layout

- .github/ (dir, 1 files, ~59 lines)
- .gitignore (~5 lines)
- CLAUDE.md (~18 lines)
- cmd/ (dir, 1 files, ~810 lines)
- CONTRIBUTING.md (~38 lines)
- docs/ (dir, 25 files, ~784 lines)
- go.mod (~5 lines)
- go.sum (~2 lines)
- golden/ (dir, 18 files, ~31 lines)
- internal/ (dir, 43 files, ~7104 lines)
- LICENSE (~21 lines)
- llm/ (dir, 1 files, ~8 lines)
- README.md (~107 lines)
- ROADMAP.md (~71 lines)
- SECURITY.md (~20 lines)

