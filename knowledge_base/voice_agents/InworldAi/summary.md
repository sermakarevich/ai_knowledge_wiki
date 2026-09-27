# Technical Analysis: api-evangelist/inworld-ai

**Repository:** https://github.com/api-evangelist/inworld-ai
**Version analyzed:** unknown (provenance manifest `provenance: '0.1'` is a schema marker, not a repo version; 02-top-level-files.md:304-307)
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: developers integrating real-time voice AI must reconcile fragmented provider surfaces — separate text-to-speech, speech-to-text, voice management, and speech-to-speech session protocols, each with its own auth, billing, and client semantics. The profile covers Inworld AI as a real-time voice AI infrastructure provider delivering TTS, STT, speech-to-speech Realtime API, and an OpenAI/Anthropic-compatible LLM Router (01-overview.md:73).

How the repo addresses it: it does not ship software. The repository contains no software, build, release, or binary — only text and machine-readable API descriptions (01-overview.md:57-60). It catalogs the provider's TTS, Voice, STT, and Realtime APIs behind one API surface and billing relationship (01-overview.md:3), declaring five catalog entries — Realtime, Speech To Text, Text To Speech, Voices, Chat Completions — in `apis.yml` (02-top-level-files.md:24-30), each pointing at reconstructed OpenAPI specs plus a shared AsyncAPI/JSON-Schema/JSON-LD set (02-top-level-files.md:32-43), with an independent Tier-1 Consuming review (02-top-level-files.md:69-78). Primary user: an API consumer or agent-tooling author evaluating or integrating Inworld AI's voice platform, not a contributor building this repo.

## 2. High-Level Architecture

```
  provider docs/portal (docs.inworld.ai, API keys, billing, playground)
      │ harvested / reconstructed
      ▼
  openapi/_original/* (6 byte-identical harvested specs)
      │ split into path subsets
      ▼
  openapi/inworld-ai-*-openapi.yml (7 derived per-API specs)
      ├───► collections/*.postman_collection.json + *.opencollection.json (derived)
      └───► asyncapi/inworld-ai-asyncapi.yml, json-schema/*, json-ld/* (shared)
      │ documented by
      ▼
  apis.yml (catalog root) + provenance.yml (authorship) + review.yml (Tier-1 verdict)
```

Data-flow narrative: (1) provider material (docs, keys, billing, TTS playground) is observed from the public surface (02-top-level-files.md:80-88); (2) six original specs are fetched byte-identical as `harvested` evidence (02-top-level-files.md:58-60); (3) seven per-API OpenAPI files are split out as `derived` path subsets, e.g. the voices spec (02-top-level-files.md:61-62, 02-top-level-files.md:564-566); (4) Postman/OpenCollection artifacts are derived per API with `evidence: openapi/<api-name>` (02-top-level-files.md:61-62, 02-top-level-files.md:318-320); (5) `apis.yml` binds each API `aid` to its machine-readable properties and human URLs (02-top-level-files.md:13-15); (6) `review.yml` publishes the independent Tier-1 Consuming assessment with strengths, weaknesses, and sources (02-top-level-files.md:67-78, 02-top-level-files.md:91).

Persistent state lives in the YAML/JSON artifacts themselves: `apis.yml` (catalog root), `provenance.yml` (method/evidence per path), `review.yml` (verdict snapshot dated 2026-05-25), and the spec/collection files. There is no database, runtime store, or generated cache described in the wiki.

## 3. The Cataloged API Surface

The repo's central concept is the profiled third-party API entry: an `aid`-keyed catalog record binding a provider capability to human docs and machine-readable specs. Each entry carries `aid`, `name`, `description`, `humanURL`, `tags`, and `properties` (02-top-level-files.md:13-15). Named kinds (02-top-level-files.md:24-30):

- `inworld-ai:inworld-ai-realtime-api` — Inworld AI Realtime API — "Realtime speech-to-speech sessions." (02-top-level-files.md:26)
- `inworld-ai:inworld-ai-speech-to-text-api` — Inworld AI Speech To Text API — "Transcribe audio to text." (02-top-level-files.md:27)
- `inworld-ai:inworld-ai-text-to-speech-api` — Inworld AI Text To Speech API — "Synthesize speech from text using Inworld voice models." (02-top-level-files.md:28)
- `inworld-ai:inworld-ai-voices-api` — Inworld AI Voices API — "Voice cloning, design, and lifecycle." (02-top-level-files.md:29)
- `inworld-ai:inworld-ai-chat-completions-api` — Inworld AI Chat Completions API — "OpenAI-compatible chat completions through the LLM Router." (02-top-level-files.md:30)

Representation: the first four entries each repeat the same machine-readable property set (per-API OpenAPI plus shared AsyncAPI, JSON Schema, JSON-LD) alongside Documentation and GettingStarted URLs (02-top-level-files.md:32-43); the Chat Completions entry points at `https://docs.inworld.ai/router/introduction` with Documentation, GettingStarted, and OpenAI-compatibility URLs (02-top-level-files.md:45). Key query — catalog root identity, verbatim:

```
aid: inworld-ai
url: https://raw.githubusercontent.com/api-evangelist/inworld-ai/refs/heads/main/apis.yml
name: Inworld AI
```

(02-top-level-files.md:16-22)

## 4. LLM / External Service Integration

The repository itself calls no LLM and no external API: it is static catalog text plus spec artifacts, with no runtime, credentials, or env vars described in either wiki page. All provider/service interaction described below belongs to the profiled Inworld AI platform, consumed by downstream users — not executed by this repo.

- Providers routed through: multi-provider STT routing, currently Whisper variants via Groq, 99+ languages (01-overview.md:10, 01-overview.md:44); OpenAI/Anthropic-compatible LLM Router with chat-completions endpoint and Models APIs (01-overview.md:5, 02-top-level-files.md:30, 02-top-level-files.md:80-88); Twilio media-stream integration and MCP server tunneling on the Realtime API (01-overview.md:12, 01-overview.md:52).
- Required vs optional calls (downstream consumer view): TTS synthesis (sync, server-streamed, WebSocket), Voice CRUD plus workspace publish, STT transcribe plus streaming WebSocket, Realtime session events (`session.update`, `input_audio_buffer.append`, `response.create`), Chat Completions via the router (01-overview.md:8-12, 01-overview.md:31, 01-overview.md:38, 01-overview.md:51).
- Env vars: none documented in the wiki for this repo. The review notes the provider portal exposes API keys, billing, usage, and a TTS playground (02-top-level-files.md:80-88), implying downstream callers hold an Inworld API key, but no variable name or required/optional split is given in the wiki and none is asserted here.

## 5. The Artifact Derivation Pipeline

The repo's primary workflow is catalog construction: harvest provider specs, split derived per-API subsets, generate collections, bind them in `apis.yml`, and record verdict in `review.yml`. Step by step (no functions exist; every step cites its artifact record):

1. Harvest originals — six `openapi/_original/` specs fetched provider-side byte-identical, `method: harvested` (02-top-level-files.md:58-60, 02-top-level-files.md:546-548).
2. Split derived subsets — seven `openapi/inworld-ai-*-openapi.yml` specs produced as path subsets of the harvested specs, `method: derived`, e.g. the voices spec (02-top-level-files.md:61-62, 02-top-level-files.md:582-584).
3. Derive collections — `collections/*.postman_collection.json` and `*.opencollection.json` built from OpenAPI with `evidence: openapi/<api-name>`, `method: derived` (02-top-level-files.md:61-62, 02-top-level-files.md:318-320).
4. Bind the catalog — `apis.yml` declares root `aid: inworld-ai` / `name: Inworld AI` (02-top-level-files.md:16-22) and the five API entries with descriptions and property URLs (02-top-level-files.md:24-30, 02-top-level-files.md:32-45).
5. Record authorship — `provenance.yml` maps each path to `generated` / `derived` / `harvested` / `unknown` with evidence; `unknown` means no authorship record, not provider authorship (02-top-level-files.md:49-63).
6. Publish verdict — `review.yml` stamps `reviewedBy: API Evangelist`, `reviewedAt: '2026-05-25'`, `position: Consuming`, `tier: 1` with summary, strengths, weaknesses, sources (02-top-level-files.md:67-78, 02-top-level-files.md:91).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `apis.yml` | catalog root + 5 API entries (02-top-level-files.md:13-45) | Declares `aid: inworld-ai`, per-API names/descriptions, human and machine-readable property URLs |
| `provenance.yml` | header at 02-top-level-files.md:304-307, entries truncated at 02-top-level-files.md:603-605 | Maps every artifact path to `generated`/`derived`/`harvested`/`unknown` with evidence |
| `review.yml` | header 02-top-level-files.md:611-616, body 02-top-level-files.md:617-646 | Independent Tier-1 Consuming verdict: summary, strengths, weaknesses, sources |
| `openapi/_original/` (6 specs) | harvested evidence 02-top-level-files.md:558-560 | Byte-identical provider-fetched sources, e.g. `openapi/_original/inworld-tts-api-openapi.yml` |
| `openapi/inworld-ai-realtime-api-openapi.yml` | derived subset 02-top-level-files.md:564-566 | Realtime API path subset referenced from `apis.yml` properties |
| `openapi/inworld-ai-voices-api-openapi.yml` | derived subset 02-top-level-files.md:582-584 | Voices API path subset; see also 01-overview.md:40 |
| `openapi/inworld-tts-api-openapi.yml` | spec artifact 01-overview.md:34 | TTS OpenAPI description |
| `openapi/inworld-voice-api-openapi.yml` | spec artifact 01-overview.md:40 | Voice API OpenAPI description |
| `openapi/inworld-stt-api-openapi.yml` | spec artifact 01-overview.md:47 | STT OpenAPI description |
| `openapi/inworld-ai-chat-completions-api` (spec) | derived evidence 02-top-level-files.md:318-320 | Basis for the chat-completions collection |
| `collections/inworld-tts-api.postman_collection.json` | collection artifact 01-overview.md:34 | TTS Postman collection |
| `collections/inworld-tts-api.opencollection.json` | collection artifact 01-overview.md:34 | TTS OpenCollection |
| `collections/inworld-voice-api.postman_collection.json` | collection artifact 01-overview.md:40 | Voice Postman collection |
| `collections/inworld-stt-api.postman_collection.json` | collection artifact 01-overview.md:47 | STT Postman collection |
| `collections/inworld-ai-chat-completions-api.opencollection.json` | derived, evidence `openapi/inworld-ai-chat-completions-api` 02-top-level-files.md:318-320 | Chat-completions OpenCollection |
| `asyncapi/inworld-ai-asyncapi.yml` | shared property 02-top-level-files.md:32-43; also 01-overview.md:34, 01-overview.md:47 | AsyncAPI description shared across TTS/STT/Realtime entries |
| `json-schema/inworld-tts-synthesis-schema.json` | shared property 02-top-level-files.md:32-43; 01-overview.md:34 | JSON Schema for TTS synthesis |
| `json-ld/inworld-ai-context.jsonld` | shared property 02-top-level-files.md:32-43; 01-overview.md:34 | JSON-LD context for the catalog |
| `agentic-access/inworld-ai-agentic-access.yml` | generated record 02-top-level-files.md:60 | Tooling-declared agentic-access artifact (method `generated`) |
| `kin/score-*.yml` | generated snapshots 02-top-level-files.md:60 | Kin Score snapshots written by `score.rb` (method `generated`) |

## 7. Dependencies

The repo has no software package manifest and no runtime dependencies; the wiki names no packages with version constraints. Its functional dependencies are spec-artifact formats and the profiled provider surface. Required first:

| Package | Version constraint | Purpose |
|---|---|---|
| OpenAPI (per-API YAML specs) | unknown (no constraint stated in wiki) | Machine-readable REST descriptions bound in `apis.yml` properties (02-top-level-files.md:32-43) |
| AsyncAPI (`asyncapi/inworld-ai-asyncapi.yml`) | unknown (no constraint stated in wiki) | Event/ streaming description shared by TTS, STT, Realtime entries (02-top-level-files.md:32-43) |
| JSON Schema (`json-schema/inworld-tts-synthesis-schema.json`) | unknown (no constraint stated in wiki) | TTS synthesis shape validation (01-overview.md:34) |
| JSON-LD (`json-ld/inworld-ai-context.jsonld`) | unknown (no constraint stated in wiki) | Linked-data context for the catalog (01-overview.md:34) |
| Postman / OpenCollection (collections JSON) | unknown (no constraint stated in wiki) | Importable request collections derived from OpenAPI (02-top-level-files.md:318-320) |
| Inworld AI hosted platform (TTS / Voice / STT / Realtime / LLM Router) | unknown (no constraint stated in wiki) | Profiled third-party service the catalog describes; one base URL and billing surface (02-top-level-files.md:80-88) |

## 8. CLI / Usage Surface

There is no CLI, entry-point script, or config file in this repo per the wiki. Usage is read-only: browse the catalog, follow human doc URLs, import the machine-readable specs. Entry points:

| Entry point | Target user | Action |
|---|---|---|
| `apis.yml` (root `aid: inworld-ai`) | catalog consumer / agent tooling | Resolve the five API entries and their property URLs (02-top-level-files.md:16-30) |
| `review.yml` | evaluator | Read the Tier-1 Consuming verdict, strengths/weaknesses, sources (02-top-level-files.md:67-91) |
| `provenance.yml` | maintainer | Check method/evidence per artifact; drift checked by `check-provenance-manifest.py` (02-top-level-files.md:49-56) |
| Provider portal (API keys, billing, usage, TTS playground) | integrator | Obtain key, test synthesis, monitor usage (02-top-level-files.md:80-88) |

Human documentation URLs (from wiki):

| API | Human URL |
|---|---|
| TTS | `https://docs.inworld.ai/tts/tts` (01-overview.md:28-34) |
| Voice | `https://docs.inworld.ai/api-reference/voiceAPI/voiceservice/list-voices` (01-overview.md:35-40) |
| STT | `https://docs.inworld.ai/stt/overview` (01-overview.md:41-47) |
| Realtime | `https://docs.inworld.ai/realtime/overview` (01-overview.md:48-54) |
| Chat Completions / Router | `https://docs.inworld.ai/router/introduction`, quickstart, OpenAI-compatibility page (02-top-level-files.md:45) |

Env vars: none defined by this repo (see section 4). Config table: not applicable — no config schema is described in the wiki; consumer authentication (provider API key, Realtime JWT sessions per 01-overview.md:52) lives on the Inworld platform side, outside this repo.

## 9. Extensibility Points

- New profiled capability (e.g. Router/Models APIs, which the overview notes are listed in the plan cover line but undescribed, 01-overview.md:54): add an `apis.yml` entry with `aid`/`name`/`description`/`humanURL`/properties following the existing five-entry pattern (02-top-level-files.md:24-45).
- New or refreshed REST surface: harvest into `openapi/_original/` as byte-identical source (`method: harvested`, 02-top-level-files.md:58-60), then split the derived per-API subset (`method: derived`, 02-top-level-files.md:61-62).
- New client collection: add `collections/<api>.postman_collection.json` / `.opencollection.json` with `evidence: openapi/<api-name>` (02-top-level-files.md:61-62, 02-top-level-files.md:318-320).
- New streaming/event shape: extend the shared `asyncapi/inworld-ai-asyncapi.yml`, currently `unknown` authorship (02-top-level-files.md:62-63); record the change in `provenance.yml` (generated by `build-provenance-manifest.py`, drift-checked by `check-provenance-manifest.py`, 02-top-level-files.md:49-56).
- New verdict dimension: extend `review.yml` strengths/weaknesses/sources lists (02-top-level-files.md:80-91); new tooling snapshots go to `agentic-access/` and `kin/` as `generated` artifacts (02-top-level-files.md:60).

## 10. Limitations and Gotchas

- **No public OpenAPI download; specs are reconstructed from documented JSON shapes.** The review's weaknesses state exactly this (02-top-level-files.md:80-91), so derived specs can lag or misstate provider behavior — verify against live docs before generating clients.
- **Realtime WebSocket protocol is narratively documented, not machine-readable AsyncAPI.** Same weakness list (02-top-level-files.md:80-91): event names like `session.update` / `input_audio_buffer.append` / `response.create` (01-overview.md:51) lack a formal contract, raising interop risk for drop-in OpenAI Realtime clients.
- **Status page exists but is unsurfaced from the landing page** (`status.inworld.ai`, 02-top-level-files.md:80-91) — operational visibility requires knowing the direct URL.
- **Wiki source itself is truncated in two places.** The Realtime Properties list cuts off mid-entry (01-overview.md:54), the Chat Completions `apis.yml` entry truncates with 14,524 more characters withheld (02-top-level-files.md:45), and `provenance.yml` truncates mid-entry at the rate-limits line (02-top-level-files.md:65) — Router/Models detail and later provenance rows are simply absent.
- **Third-party profile, not provider documentation.** Everything is assembled from public browser-reachable material with no credentials (01-overview.md:13-16), and the Kin Score / Agent Readiness rating is an independent assessment of public artifacts (01-overview.md:16); staleness is bounded by the 2026-05-25 review date (02-top-level-files.md:67-78).

## 11. How It Compares to Alternatives

This repo is a catalog profile, not a runnable platform, so comparison is on integration surface as recorded in the wiki — primarily its OpenAI/Anthropic-compatible endpoints and routed providers.

- **OpenAI Realtime API:** the explicit interop target — Inworld's Realtime API uses an OpenAI-Realtime-API-compatible event protocol so existing OpenAI Realtime clients can swap base URLs (01-overview.md:51); the review claims drop-in OpenAI Realtime compatibility as a strength (02-top-level-files.md:80-88).
- **OpenAI Chat Completions:** the router exposes an OpenAI-compatible chat-completions endpoint (`inworld-ai-chat-completions-api`, 02-top-level-files.md:30) with an OpenAI-compatibility doc page (02-top-level-files.md:45) — positioning Inworld as a routing layer rather than a competing foundation model.
- **Anthropic Messages API:** likewise surfaced as a compatibility target in the review summary and strengths (02-top-level-files.md:80-88) — same routing-layer positioning for Anthropic-shaped workloads.
- **Groq-served Whisper variants / Twilio Media Streams:** named as the current STT routing backend (01-overview.md:44) and the Realtime telephony integration (01-overview.md:52) — Inworld composes third-party transcription and telephony primitives behind its single billing surface instead of owning that layer.

Positioning sentence: per the review, the profiled platform competes as a unified multi-product voice layer — one base URL and billing surface with drop-in OpenAI/Anthropic compatibility, first-class cloning plus phoneme/viseme alignment, and an open-source TTS model with on-prem support — against point providers, with spec-reconstruction and narrative-protocol documentation as its assessed costs (02-top-level-files.md:80-91).

## Appendix: Selected Code Snippets

Catalog root identity (`apis.yml` excerpt, 02-top-level-files.md:16-22):

```
aid: inworld-ai
url: https://raw.githubusercontent.com/api-evangelist/inworld-ai/refs/heads/main/apis.yml
name: Inworld AI
```

Per-API machine-readable property set (Realtime entry, 02-top-level-files.md:32-43):

```
  - type: OpenAPI
    url: openapi/inworld-ai-realtime-api-openapi.yml
  - type: AsyncAPI
    url: asyncapi/inworld-ai-asyncapi.yml
  - type: JSONSchema
    url: json-schema/inworld-tts-synthesis-schema.json
  - type: JSONLD
    url: json-ld/inworld-ai-context.jsonld
```

Provenance header (`provenance.yml` excerpt, 02-top-level-files.md:49-56):

```
provenance: '0.1'
note: Who wrote each artifact in this repository. `unknown` means we have no record — not that the provider
  did not write it. Generated by all/0-working/build-provenance-manifest.py; drift from disk is checked
  by check-provenance-manifest.py.
```

Review verdict (`review.yml` excerpts, 02-top-level-files.md:69-88):

```
aid: inworld-ai
name: Inworld AI
reviewedBy: API Evangelist
reviewedAt: '2026-05-25'
position: Consuming
tier: 1
```

```
summary: >
  Tier-1 provider. Inworld AI publishes a coherent, OpenAPI-shaped REST surface
  (TTS, Voice, STT, Realtime, LLM Router, Models) plus an OpenAI-Realtime-API-
  compatible WebSocket event protocol and an OpenAI-and-Anthropic-compatible chat
  completions endpoint. The portal exposes API keys, billing, usage, and a TTS
  playground; the docs publish an `llms.txt` index and a `llms-full.txt` archive.
```
