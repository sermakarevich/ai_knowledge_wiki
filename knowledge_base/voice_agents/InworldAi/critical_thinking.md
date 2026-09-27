> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: api-evangelist/inworld-ai

## Claims vs. evidence
- Claim: Inworld AI is a real-time voice-AI infrastructure provider (TTS, STT, speech-to-speech Realtime, LLM Router) behind one API surface and billing relationship. Evidence: digest frames exactly this (digest.md:4), with five `apis.yml` entries sharing portal properties (02-top-level-files.md:24-30).
- Claim: TTS spans Realtime TTS-2 (100+ languages), TTS 1.5 Max (15 languages), TTS 1.5 Mini (sub-120 ms first-token) with sync, streamed, and WebSocket synthesis. Evidence: feature-list level only (01-overview.md:30-31); no benchmark method, test set, or latency distribution reproduced.
- Claim: Voice API does instant cloning from audio plus natural-language voice design with list/get/update/delete and workspace publish. Evidence: operation list only (01-overview.md:38); no audio requirements, consent flow, or quality metric given.
- Claim: STT routes multi-provider (currently Whisper variants via Groq), 99+ languages, word timestamps, voice profiling, prompt biasing. Evidence: capability list only (01-overview.md:44-45); no WER numbers, language list, or routing policy reproduced.
- Claim: Realtime API is an end-to-end STT+LLM+TTS pipeline over WebSocket/WebRTC with an OpenAI-Realtime-compatible event protocol (`session.update`, `input_audio_buffer.append`, `response.create`), VAD, tool calling, MCP tunneling, Twilio integration. Evidence: strongest signal — named events and named integrations are specific and falsifiable (01-overview.md:51-52).
- Claim: Everything comes from public, browser-reachable material; Kin Score / Agent Readiness rate public artifacts only. Evidence: explicit provenance statement quoted in wiki (01-overview.md:14-16); honest scoping, but also a ceiling on what the profile proves.
- Claim: Tier-1 Consuming provider with coherent OpenAPI-shaped REST surface plus compat endpoints. Evidence: `review.yml` header and summary verbatim (02-top-level-files.md:70-78, 02-top-level-files.md:80-88); it is one reviewer's judgment dated 2026-05-25, not an audit.
- Claim: Chat Completions API offers OpenAI-compatible chat through the LLM Router. Evidence: catalog entry with Router documentation and quickstart URLs — but its property block ends in an empty `url:` value and the chunk truncates there (02-top-level-files.md:45), so the claim is cataloged, not confirmed.
- Overall: strong on catalog shape (what the surface contains), weak on performance, cost, and reliability (what it delivers in production).

## Genuinely new vs. repackaged
- Genuinely useful: one machine-readable inventory across voice+LLM APIs — per-API OpenAPI plus shared AsyncAPI, JSON Schema, and JSON-LD (02-top-level-files.md:32-43) — which Inworld itself does not package this way per the review (02-top-level-files.md:91).
- Genuinely useful: explicit derivation chain in `provenance.yml` — six harvested byte-identical provider specs split into seven derived path-subset OpenAPIs that generate collections/Postman artifacts (02-top-level-files.md:58-63).
- Genuinely useful: the compatibility-mapping move — OpenAI Realtime event parity plus OpenAI Chat Completions / Anthropic Messages compat on the Router (01-overview.md:51, 02-top-level-files.md:91) — which directly lowers switching-cost analysis.
- Repackaged: model variant names, language counts, cloning/design features, and latency figures restated from provider docs without independent measurement.
- Repackaged: standard API-Evangelist scaffolding (catalog root, per-API properties, collections, review rubric) applied to Inworld; the value is the template, not Inworld-specific depth.
- Neither vendor docs nor SDK: the repo holds no software, build, release, or binary — only text and descriptions (digest.md:7) — so engineering value is descriptive, never executable.

## Weaknesses and blind spots
- No public OpenAPI download: the specs are reconstructed from documented JSON shapes, so drift from the live provider surface is always possible (02-top-level-files.md:91).
- Realtime protocol documented narratively, not as machine-readable AsyncAPI — the highest-risk surface (streaming, VAD, tool calls) is the least specified (02-top-level-files.md:91).
- Status page exists at `status.inworld.ai` but is not surfaced from the landing page — operational transparency gap (02-top-level-files.md:91).
- Truncated evidence: the Realtime properties list cuts off mid-entry (01-overview.md:54) and `apis.yml` truncates after Chat Completions (02-top-level-files.md:45), so Router/Models entries are named but undescribed here.
- Single snapshot dated 2026-05-25 (01-overview.md:22-23, 02-top-level-files.md:70-78); realtime voice APIs churn fast, so model IDs, pricing, and compat claims may be stale.
- Scoring opacity: Kin Score / Agent Readiness method and actual Inworld scores are referenced but not reproduced in digest or wiki, so ratings cannot be audited from these files.
- Missing operational essentials: JWT session auth, MCP tunneling scope, Twilio media-stream wiring, end-of-turn tuning, and fallback behavior are named (01-overview.md:52, 01-overview.md:45) but never specified.
- Missing trust essentials: zero-data-retention mechanics, on-premise deployment model, and cloning consent/provenance are asserted at feature level (01-overview.md:32) with no contract or flow excerpt.
- STT forwarding caveat: "currently Whisper variants via Groq" (01-overview.md:44) implies resold capacity with data-flow and retention implications the profile does not explore.
- Authorship gaps: the shared `asyncapi/inworld-ai-asyncapi.yml` and `json-schema/inworld-tts-synthesis-schema.json` are `method: unknown` — no authorship record at all (02-top-level-files.md:63) — so the streaming contract's origin is unclear.
- No cost or failure lens in these files: no per-minute/per-token numbers, quota semantics, reconnect/partial-transcript handling, or Router fallback behavior reproduced.
- Voice-lifecycle gaps: list/get/update/delete plus workspace publish are named (01-overview.md:38) with no versioning, rollback, or sharing-permission semantics described.

## Applicability
- Use as a vendor-shortlist pointer for realtime voice (TTS/STT/speech-to-speech) and compat-routed chat completions — not as integration ground truth.
- Use the artifact inventory (OpenAPI/AsyncAPI/collections) to bootstrap contract checks and mock harnesses, then re-validate every endpoint against live Inworld docs.
- Use the compat claims to scope a thin-adapter spike (swap base URL, replay Realtime events, route chat completions) before any native-SDK commitment.
- Do not use for compliance, security, or cost decisions: retention, on-premise, and unified-billing claims need vendor contracts and live pricing, none present here.
- Do not cite arena rank, sub-120 ms, or language counts externally from this profile alone; each needs a dated primary source.
- **Relevance to my work**
  - AI/ML engineering: candidate speech layer (streaming TTS/STT, phoneme/viseme alignment, cloning, prompt biasing, VAD options) for voice-agent evals; requires live latency/quality benchmarking first.
  - Agentic systems: Router pattern (OpenAI/Anthropic-compat routing) plus Realtime tool calling and MCP tunneling is the most transferable idea — worth mirroring in our own gateway abstractions.
  - Elisity data platform: zero-retention and on-premise TTS options map to regulated-workload requirements, but the profile gives no deployable detail — treat as vendor-diligence questions, and flag the Groq-forwarded STT path as a data-lineage item.

## What this changes
- Changes vendor scouting, not architecture: Inworld enters the shortlist as a voice-quality plus compat-routing option alongside pure-play TTS/STT vendors.
- Changes adapter strategy: compat-first trial (OpenAI/Anthropic/Realtime protocols) looks cheaper than native lock-in — conditional on live docs confirming parity.
- Changes nothing about trust: artifact hygiene scores describe public docs, not model quality, safety, security, or uptime; independent testing still required.
- Changes process thinking: the profile format itself (`apis.yml` + provenance chain + correction-friendly third-party review) is a reusable template for our own API inventories.
- Changes evaluation checklists: any voice-vendor trial must now demand latency distributions, language proofs, cloning-consent handling, retention contracts, and Router fallback tests.
- Does not change build priorities: nothing here justifies displacing current TTS/STT/LLM choices without a live side-by-side trial.

## Verdict
- A transparent, well-structured, but thin third-party directory entry: good for discovery, insufficient for build-or-buy decisions.
- Value concentrates in the machine-readable inventory, the provenance chain, and the compat mapping; performance and cost claims are unverified here.
- Next step if interested: verify live docs, pull real specs, run latency/quality/cost spikes on TTS, STT, Realtime, and Router before any roadmap commitment.
- **watch**
