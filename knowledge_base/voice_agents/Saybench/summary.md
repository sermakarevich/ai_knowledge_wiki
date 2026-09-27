# Technical Analysis: renan-martini/saybench

**Repository:** https://github.com/renan-martini/saybench
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview

Problem space: voice-AI stacks fail on the deployer's own audio, accents, jargon, and network conditions, while vendor benchmarks report lab-audio accuracy and batch latency that do not transfer to live calls. Aggregate rankings hide per-failure-mode inversions and batch-vs-streaming latency gaps (README.md:44-52).

How the repo addresses it: saybench benchmarks the caller's own voice pipeline on the caller's own clips, reporting accuracy per failure mode, live-call latencies, and cost, plus a CI regression gate (README.md:9-11). It exposes five benchmark modes — `stt`, `stream`, `llm`, `s2s`, `tts` — each with an offline `fake` provider so every mode runs with zero keys (README.md:26-34). Cross-mode machinery standardizes scoring doctrine, JSON reports with `compare` gate and HTML dashboard, multi-vendor providers plus `custom` escape hatch, MCP server, and Pipecat mapping (README.md:36-42). Distribution is a single static Go binary via `go install github.com/renan-martini/saybench/cmd/saybench@latest` or `go build ./cmd/saybench` (README.md:55-59).

Primary user: an engineer operating a live voice agent (phone-call platform or Pipecat + LiveKit pipeline) who must select providers and block regressions on representative audio (ROADMAP.md:3-6, README.md:63-82).

## 2. High-Level Architecture

```
  local clips + manifest.jsonl
    │
    ▼
  saybench CLI (cmd/saybench) ─► mode runner (stt | stream | llm | s2s | tts)
    │                                │
    │                                ▼
    │                           provider adapter (deepgram | openai | assemblyai |
    │                            elevenlabs | gemini | openrouter | groq | custom | fake)
    │                                │
    │                                ▼
    │                           scorer (WER sub/del/ins, keyterm recall,
    │                            digit-normalize, LLM-judge, latency percentiles)
    │                                │
    ▼                                ▼
  baseline.json ─► compare (-max-wer-regression) ─► show / html dashboard
```

Data-flow narrative:

1. Operator assembles a corpus: audio files plus a JSONL manifest of `{"audio","reference","category"}` rows (README.md:73-75). The bundled golden set serves as the default corpus (README.md:63-66).
2. A mode runner replays the corpus against each selected provider adapter at the mode's pace (batch for `stt`, real-time pace for `stream`, turn loop for `llm`/`s2s`, synthesis for `tts`), enforcing per-item deadlines and size-bounded reads (README.md:26-34, SECURITY.md:12-20).
3. The scorer computes corpus WER with substitution/deletion/insertion breakdown, per-category failure-mode slices, keyterm recall, and mode-specific latency distributions (avg/p95, TTFP, TTFT, time-to-first-audio), emitting `—` where there is no data (README.md:28-33, README.md:103-109).
4. Each run persists a self-contained JSON report (`-report today.json`); reports carry reference transcripts, hypotheses, conditions (warm-vs-cold, echo-vs-conversational), and cost columns from a user-supplied pricing table (README.md:66-72, SECURITY.md:17-20, ROADMAP.md:91).
5. `compare baseline.json today.json -max-wer-regression 2.0` diffs two reports and fails CI on regression; it refuses cross-mode deltas and warns on condition mismatches (README.md:76-78, ROADMAP.md:82-89). `show` and `html -o dashboard.html` render reports for review (README.md:80-82).
6. The MCP server (`saybench mcp`) exposes the same tool surface to coding agents over stdio (README.md:41).

Persistent state lives outside the binary: the audio corpus and JSONL manifest on disk, JSON report files, and the generated single-file HTML dashboard. Reports contain reference transcripts and hypotheses and must be treated as sensitive if the corpus is (SECURITY.md:17-20). Ignored build artifacts are the compiled binary, root-level JSON reports, distribution output, audio fixtures, and Finder metadata (.gitignore:1-5).

## 3. The Benchmark Mode

The central concept is the benchmark mode: one CLI subcommand per voice-pipeline failure point, each parameterized by a provider list and sharing scoring, reporting, and `fake`-provider conventions (README.md:26-34).

Representation: a mode is invoked as `saybench <mode> -providers <list> [-manifest ...] [-report ...]`; other modes follow the same pattern as `saybench stream|llm|s2s|tts -providers/-targets …` (README.md:76-84). Exact flag names attested in the wiki slice are `-providers`, `-manifest`, `-report`, `-max-wer-regression`, `-o` (README.md:85).

Named kinds/types with file:line:

- Batch STT — `saybench stt`, corpus WER with sub/del/ins breakdown, per-failure-mode categories, keyterm recall, round-trip latency (README.md:28).
- Streaming STT — `saybench stream`, time-to-first-partial, finalization lag, interim word survival, fed at real-time pace (README.md:29).
- LLM turn — `saybench llm`, time-to-first-token, completion time, tok/s, warm by default, SSE vs WebSocket as a dimension (README.md:30).
- Speech-to-speech — `saybench s2s`, voice-to-voice latency, echo comprehension scoring, barge-in stop time (README.md:31).
- TTS — `saybench tts`, time-to-first-audio-byte, synthesis time, audio duration (README.md:32).

Key queries: select a mode by failure point, then sweep providers against the same manifest. Verbatim invocation and output shape (README.md:13-22):

```
$saybench stt -providers fake,deepgram,openai -manifest golden/manifest.jsonl -report today.json

PROVIDER                       CLIPS  ERRORS  WER    KEYTERM RECALL  AVG LATENCY  P95 LATENCY
deepgram:nova-3                14     0       3.8%   93.5%           926ms        2139ms
fake                           14     0       16.5%  67.7%           47ms         73ms
openai:gpt-4o-mini-transcribe  14     0       19.0%  74.2%           1319ms       1930ms
```

## 4. LLM / External Service Integration

Providers (README.md:40, ROADMAP.md:82-91): Deepgram, OpenAI, AssemblyAI, ElevenLabs, Gemini Live, OpenRouter, Groq, plus a `custom` per-mode escape hatch. Transports include Deepgram live / OpenAI Realtime / AssemblyAI Universal-Streaming for streaming STT, OpenAI-compatible endpoints (openai / openrouter / groq / custom base URL) for the LLM loop, OpenAI Realtime plus `custom` dialect and Gemini Live (BidiGenerateContent) for S2S, and openai / elevenlabs / custom / fake-tts for TTS (ROADMAP.md:82-91).

Required vs optional calls: no network call is required to exercise the tool — every mode has an offline `fake` provider and the documented smoke test is zero-key against the bundled corpus (README.md:26-27, README.md:63-66). Live-vendor calls are optional and occur only against explicitly selected providers with keys present.

Env vars: keys come from the environment only, never from flags, files, or logs, and are never written to reports or echoed in errors (README.md:67-71, SECURITY.md:12-20). Attested names in the wiki slice are `DEEPGRAM_API_KEY` and `OPENAI_API_KEY` (README.md:67-71); the providers page (docs/providers.md, indexed at README.md:98) holds the full key-to-provider map but is outside the ingested slice. Every network call carries a deadline (per-item context timeout plus HTTP client backstop) and size-bounded reads via `io.LimitReader`; audio inputs are capped at 100 MiB and manifest lines at 1 MiB (SECURITY.md:12-20, CLAUDE.md:11).

## 5. The Measure-Compare-Gate Pipeline

Primary workflow: measure own audio, persist a JSON baseline, compare each subsequent run, fail CI on regression, review via `show`/`html` (README.md:63-82).

1. Zero-key smoke test with the offline fake provider and bundled corpus — `saybench stt -providers fake` (README.md:65-66). Validates installation and report path without credentials.
2. Baseline against real vendors — `export DEEPGRAM_API_KEY=...`, `export OPENAI_API_KEY=...`, then `saybench stt -providers deepgram,openai -report baseline.json` (README.md:68-71). Keys are env-only by construction (SECURITY.md:12-20).
3. Own-audio measurement — write a JSONL manifest next to the clips, e.g. `{"audio":"clips/refund-call.wav","reference":"I want a refund for order four two nine","category":"numbers"}`, then `saybench stt -providers deepgram -manifest my-corpus/manifest.jsonl -report today.json` (README.md:73-75). Scoring applies corpus WER, keyterm recall, opt-in digit normalization and opt-in LLM-judge beside WER (README.md:38).
4. Regression gate — `saybench compare baseline.json today.json -max-wer-regression 2.0`, intended for CI to fail when any provider regresses more than 2 points (README.md:77-78). `compare` refuses cross-mode deltas and warns on warm-vs-cold and echo-vs-conversational condition mismatches (ROADMAP.md:82-89).
5. Review — `saybench show today.json` for terminal review; `saybench html -o dashboard.html baseline.json today.json` for a self-contained A/B dashboard with WER trends, category/latency charts, and worst-clips table (README.md:80-82, ROADMAP.md:82).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| README.md | 113 (cited 1-113) | Root overview: modes, cross-cutting capabilities, findings, install, quickstart, doc index, principles, license |
| docs/stt.md | unknown (indexed README.md:92) | Batch STT, manifest format, golden set, lessons from one real run |
| docs/streaming.md | unknown (indexed README.md:93) | Streaming STT: TTFP, finalization lag, interim word survival |
| docs/llm.md | unknown (indexed README.md:94) | LLM TTFT, warmup, SSE-vs-WebSocket transport |
| docs/s2s.md | unknown (indexed README.md:95) | S2S: voice-to-voice latency, echo comprehension, barge-in |
| docs/tts.md | unknown (indexed README.md:96) | TTS time-to-first-audio |
| docs/scoring.md | unknown (indexed README.md:97) | Scoring doctrine: WER, keyterms, normalization, judge, conditions |
| docs/providers.md | unknown (indexed README.md:98) | Provider specs, keys, overrides, verification ladder, adding providers |
| docs/reports.md | unknown (indexed README.md:99) | JSON reports, show, compare + CI gate, dashboard, cost columns |
| docs/mcp.md | unknown (indexed README.md:100) | MCP server for coding agents |
| docs/pipecat.md | unknown (indexed README.md:101) | Mapping a Pipecat stack to saybench equivalents |
| ROADMAP.md | 67+ (cited 3-67) | Shipped log v0.1–v1.1 and design intent grounded in live voice stacks |
| CLAUDE.md | 17 (cited 1-17) | Binding AI-work rules: stdlib-only, no secrets, HTTP discipline, clean gate |
| SECURITY.md | 20 (cited 1-20) | Key handling, network/input bounds, disclosure contact |
| CONTRIBUTING.md | unknown (indexed README.md:102) | Contribution rules, binding on AI sessions (CLAUDE.md:3-5) |
| LICENSE | unknown (cited README.md:111-113) | MIT license |
| go.sum | 2 (cited 1-2) | Sole dependency pin and go.mod hash |
| .gitignore | 5 (cited 1-5) | Ignores binary, root JSON reports, dist, audio, .DS_Store |
| cmd/saybench | unknown (install ref README.md:55-59) | Binary entry point built by `go build ./cmd/saybench` |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| github.com/coder/websocket | `v1.8.15` (exact pin, `h1:6B2JPeOGlpff2Uz6vOEH1Vzpi0iUz20A+lPVhPHtNUA=`) | Sole non-stdlib dependency; WebSocket transport (streaming STT, Realtime/S2S, LLM WS mode) |
| Go standard library | unknown (no constraint string in wiki slice) | Everything else; stdlib-only posture forbids new dependencies without explicit human decision (CLAUDE.md:7) |

Required first: `coder/websocket v1.8.15` is the only pinned dependency (go.sum:1-2), consistent with the stdlib-plus-one-dependency principle (README.md:103-109) and the zero-runtime-dependencies posture (SECURITY.md:17). No transitive runtime surface beyond the standard library is claimed.

## 8. CLI / Usage Surface

Entry points: single static binary `saybench`, installed via `go install github.com/renan-martini/saybench/cmd/saybench@latest` or built from clone via `go build ./cmd/saybench` (README.md:55-59).

Commands (README.md:26-34, README.md:76-84, README.md:36-42):

| Command | Purpose |
|---|---|
| `saybench stt -providers ...` | Batch STT benchmark (WER, keyterms, latency) |
| `saybench stream -providers ...` | Streaming STT at real-time pace (TTFP, finalization lag, survival) |
| `saybench llm -providers/-targets ...` | LLM turn benchmark (TTFT, completion, tok/s; warmup; transport dimension) |
| `saybench s2s -providers ...` | Speech-to-speech benchmark (voice-to-voice latency, echo score, barge-in) |
| `saybench tts -providers ...` | TTS benchmark (time-to-first-audio-byte, synthesis time, duration) |
| `saybench compare base.json new.json -max-wer-regression 2.0` | CI regression gate |
| `saybench show report.json` | Terminal review of a saved report |
| `saybench html -o dashboard.html base.json new.json` | Single-file HTML dashboard |
| `saybench mcp` | MCP server over stdio for coding agents |

Env-var table (attested names; full map lives in docs/providers.md):

| Variable | Purpose |
|---|---|
| `DEEPGRAM_API_KEY` | Authenticate Deepgram provider (README.md:68) |
| `OPENAI_API_KEY` | Authenticate OpenAI provider (README.md:69) |

Config: no config files and no key flags by design — keys from environment only, never flags, files, or logs (SECURITY.md:12-20, README.md:103-109). Corpus configuration is the JSONL manifest beside the clips with `audio`, `reference`, `category` fields (README.md:73-75). Cost columns use a user-supplied pricing table (ROADMAP.md:91). S2S turn control includes `-turn-ending server_vad` vs deterministic commit and `-score echo` / `-barge-in` options; LLM loop includes `-warmup` (default on) and `-judge` / `-normalize digits` scoring toggles (ROADMAP.md:88-91).

## 9. Extensibility Points

- New provider: implement the two-method provider interface; contribution note states every provider interface in the repo is two methods and PRs are welcome (ROADMAP.md:93-98). Spec, key, and override conventions live in docs/providers.md (README.md:98); the `custom` per-mode escape hatch (base-URL/dialect) covers one-off endpoints without a new adapter (README.md:40).
- New scoring dimension: extend the scoring doctrine in docs/scoring.md (WER, keyterms, normalization, judge, conditions) following the honest-metrics rule — batch-vs-streaming and synthetic-vs-real framing must not be blurred (README.md:97, CLAUDE.md:12-13).
- New report field or condition: add it to the JSON schema and bump `SchemaVersion` in `internal/report` (CLAUDE.md:16); keep `compare` condition warnings and cross-mode refusal consistent (ROADMAP.md:82-89, README.md:39).
- New corpus or failure mode: add manifest rows with a `category` label and document the mode page under docs/stt.md, docs/streaming.md, docs/llm.md, docs/s2s.md, or docs/tts.md (README.md:92-96).
- Agent integration: extend `saybench mcp` surface per docs/mcp.md rather than adding ad-hoc CLI output; every command already supports `-format json` for machine consumption (README.md:100, ROADMAP.md:82).

## 10. Limitations and Gotchas

- **Aggregate WER misleads; slice by failure mode.** The published golden-set run shows the 19%-WER vendor beating the 3.8% vendor on acronyms, names, and conversational speech, with a third of its errors from digit formatting (README.md:44-52). Comparing only the headline number inverts the buy decision.
- **Batch latency does not predict streaming behavior.** Two vendors ~400ms apart in batch diverged 5x in time-to-first-partial (README.md:44-52). Quoting batch avg/p95 for a live barge-in path overstates responsiveness.
- **Cold start dominates small-turn measurements.** Cold TLS showed a ~3x TTFT effect (1109ms → 595ms warm); warmup is default-on and recorded in the report, and warm-vs-cold is a compare-warned condition (README.md:44-52, ROADMAP.md:88). Disabling `-warmup` without noting it invalidates trend comparisons.
- **Reports embed corpus text — handle them as sensitive data.** Reports contain reference transcripts and hypotheses and the tool uploads audio only to the explicitly selected provider, so redaction and access control are the operator's job (SECURITY.md:17-20). Root-level `/*.json` reports are git-ignored, not encrypted (.gitignore:1-5).
- **Input and network bounds can truncate large corpora.** Audio files cap at 100 MiB, manifest lines at 1 MiB, all network calls have deadlines, and bodies pass through `io.LimitReader` (SECURITY.md:12-20, CLAUDE.md:11). Oversized clips or slow endpoints surface as per-item errors, not retries.
- **Wiki slice is partial — internals unverified.** The ingested slice covers README.md plus root guardrail files only; `internal/*`, `cmd/*`, and all docs/*.md bodies beyond their index blurbs were not in the slice, so adapter internals, scorer formulas, and schema fields below are not independently grounded here.

## 11. How It Compares to Alternatives

- **Pipecat (Daily)**: a production voice-pipeline framework (STT/LLM/TTS orchestration with LiveKit transport), not a benchmark. Saybench's Pipecat guide maps each pipeline service to its saybench equivalent so a Pipecat stack can be measured externally (README.md:42, README.md:101, ROADMAP.md:3-6).
- **LiveKit Agents**: a real-time media framework for conversational agents; the roadmap cites LiveKit-based meeting/conversation pipelines as the grounding workload (ROADMAP.md:3-6). Saybench does not transport live traffic — it replays corpora and scores providers.
- **Vendor dashboards and playgrounds (Deepgram / OpenAI / AssemblyAI / ElevenLabs consoles)**: single-vendor accuracy and latency views on vendor-selected audio. Saybench's position is cross-vendor comparison on the operator's own clips with per-failure-mode WER, streaming latency dimensions, cost columns, and a CI gate (README.md:9-11, README.md:36-42).
- **Generic text/LLM harnesses and WER scripts (e.g., OpenAI evals-style prompt harnesses, `jiwer`-style scoring snippets)**: cover text quality or raw WER math only. Saybench's position is voice-turn measurement end to end — word-survival and finalization lag for streaming, TTFT/tok/s with transport and warmup dimensions for the LLM turn, echo comprehension and barge-in stop time for S2S, time-to-first-audio-byte for TTS — with deterministic fakes, stable ordering/schema, and honest `—`-for-missing-data reporting (ROADMAP.md:82-91, README.md:103-109).

Positioning sentence: saybench is the operator-owned, multi-vendor voice-pipeline benchmark with a CI gate, where frameworks ship the pipeline and vendor consoles score one vendor, saybench scores all of them on your audio.

## Appendix: Selected Code Snippets

1. Quickstart workflow, `README.md:63-82`:

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

2. AI-work rules, `CLAUDE.md:1-17`:

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

3. Security posture, `SECURITY.md:1-20`:

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

4. Roadmap positioning, `ROADMAP.md:3-6`:

```
Grounded in real voice-agent stacks: platforms running live AI phone calls, and
meeting/conversation pipelines built on frameworks like Pipecat + LiveKit. Each
item exists because a real system needed it, not because a benchmark could
measure it. Order is intent, not promise.
```
