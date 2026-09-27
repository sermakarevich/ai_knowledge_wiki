---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: renan-martini/saybench

### Q1. What problem does saybench solve, and what guardrails shape its design?

> [!tip]- Answer
> Saybench benchmarks your voice-AI pipeline on your own audio — accents, jargon, and failure modes — instead of trusting vendor lab numbers, reporting accuracy per failure mode plus live-call latencies and cost with a `compare` regression gate for CI. It ships as a single static Go binary installed via `go install github.com/renan-martini/saybench/cmd/saybench@latest` or `go build ./cmd/saybench`. Its principles are stdlib plus exactly one dependency (`coder/websocket`), env-only keys, deadlines plus size-bounded reads, deterministic fakes/ordering/schema, and `—` instead of flattering zeros. See [[wiki/01-overview|Overview]].

### Q2. What are the five benchmark modes, and what does each one measure?

> [!tip]- Answer
> Saybench exposes five modes, one per pipeline failure point: batch STT (corpus WER with sub/del/ins breakdown, per-failure-mode categories, keyterm recall, round-trip latency), streaming STT (time-to-first-partial, finalization lag, interim word survival fed at real-time pace), LLM turn (time-to-first-token, completion time, tok/s with SSE vs WebSocket as a dimension), speech-to-speech (voice-to-voice latency, echo comprehension scoring, barge-in stop time), and TTS (time-to-first-audio-byte, synthesis time, audio duration). Every mode ships an offline `fake` provider so it runs with zero keys, and the canonical `saybench stt -providers fake,deepgram,openai -manifest golden/manifest.jsonl -report today.json` run prints a per-provider table of clips, errors, WER, keyterm recall, and avg/p95 latency. See [[wiki/01-overview|Overview]].

### Q3. What cross-mode capabilities standardize trust and workflow in saybench?

> [!tip]- Answer
> Trust is standardized by an honest scoring doctrine: corpus-level WER, keyterm recall, opt-in digit normalization, opt-in LLM-judge placed beside WER rather than replacing it, and `—` where there is no data. Every run emits JSON reports reviewed with `show`, gated in CI by `compare -max-wer-regression`, warned by condition-aware checks, and rendered into a single-file HTML dashboard. Multi-vendor providers plus a two-method `custom` escape hatch cover Deepgram, OpenAI, AssemblyAI, ElevenLabs, Gemini Live, OpenRouter, and Groq, while `saybench mcp` exposes the whole tool to coding agents and the Pipecat guide maps each pipeline service to its saybench equivalent. See [[wiki/01-overview|Overview]].

### Q4. What did the golden-set findings reveal, and what is the fixed quickstart workflow?

> [!tip]- Answer
> The September 2026 golden-set runs showed aggregate rankings invert per failure mode: the 19%-WER vendor beat the 3.8% one on acronyms, names, and conversational speech, with a third of its errors from digit formatting rather than mishearing. Streaming gaps diverge from batch numbers: time-to-first-partial differs 5x between vendors only ~400ms apart in batch, cold TLS triples LLM time-to-first-token (1109ms cold down to 595ms warm) while warm WebSocket buys nothing at voice-turn sizes, and a speech-native model's 601ms first audio beats the composed pipeline's ~808ms pre-TTS floor even though it talks 12.4s per reply and sometimes performs an echo request instead of echoing it. The fixed workflow is a zero-key `fake` smoke test, env-only keys for real vendors, a JSONL manifest for your own clips, a `compare -max-wer-regression 2.0` CI gate, and `show`/`html` review. See [[wiki/01-overview|Overview]].

### Q5. What contribution and security guardrails bind work in the saybench repo?

> [!tip]- Answer
> AI sessions follow the same rules as humans: stdlib-only dependencies, no secrets in code/tests/fixtures/docs/examples, context deadline plus `io.LimitReader` on every HTTP call, a clean `gofmt -l .` / `go vet ./...` / `go test -race ./...` gate, pasted real output in docs, honest batch-vs-streaming and synthetic-vs-real metrics framing, original locally-synthesized golden audio, and a `SchemaVersion` bump on report schema changes. The security posture reads API keys from environment variables only — never flags, files, reports, logs, or error echoes — bounds inputs at 100 MiB audio and 1 MiB manifest lines, keeps zero runtime dependencies, and routes vulnerability reports to renan.martiniduarte@gmail.com with a one-week reply promise and no public issue for sensitive items. The build ignores the compiled binary, root-level JSON reports, dist output, audio artifacts, and macOS metadata. See [[wiki/02-top-level-files|Top-level files]].

### Q6. How did the saybench roadmap evolve, and what does the module depend on?

> [!tip]- Answer
> The roadmap is grounded in real voice-agent stacks (live phone calls, Pipecat plus LiveKit pipelines) where order signals intent rather than promise and every shipped item exists because a real system needed it. Shipped history runs from v0.1 STT benchmarking through v0.2 keyterms/dashboard, v0.4–v0.5 streaming plus interim survival, v0.6 LLM loop, v0.7–v0.9 transport/warmup and S2S phases with echo scoring, to the v1.0 close-out (TTS, cost columns, digit normalization, server VAD, MCP, Pipecat guide) and v1.1 judge, barge-in, and Gemini adapter, with every provider interface kept to two methods. The module pins exactly one dependency, `github.com/coder/websocket v1.8.15`, by hash in go.sum. See [[wiki/02-top-level-files|Top-level files]].

### Q7. Should a team running a production voice-AI stack adopt saybench as its benchmarking harness?

> [!tip]- Answer
> Recommend saybench for a team iterating on STT/LLM/TTS vendor choice or Pipecat pipelines, because the five zero-key-runnable modes, per-failure-mode honest scoring, live-call latency metrics, and CI regression gate directly catch degradations users would notice. Condition adoption on validating against the team's own accents, jargon, and phone-line audio first, since the published findings rest on one small bundled golden set whose per-mode rankings invert. See [[wiki/01-overview|Overview]].
