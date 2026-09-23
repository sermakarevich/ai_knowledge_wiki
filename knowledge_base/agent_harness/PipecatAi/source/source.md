PDF: https://github.com/api-evangelist/pipecat-ai
# api-evangelist/pipecat-ai
Source: https://github.com/api-evangelist/pipecat-ai
Kind: repo
Fetched: 2026-09-22T14:32:36.255485+00:00
Tool: git-clone

# api-evangelist/pipecat-ai

Commit: 8de17346c379261fcf028f274533a85b2044b188

## README

# Pipecat (pipecat-ai)

<!-- API-EVANGELIST-PROVENANCE:BEGIN -->
> ### About this repository
>
> **This is not our API.** This repository is an independent, third-party profile of a company's
> **publicly available** API surface, maintained by [API Evangelist](https://apievangelist.com).
> API Evangelist does not operate, host, resell, or support this company's APIs, and is not
> affiliated with or endorsed by the company unless stated on the profile.
>
> **Where the information came from.** Everything here is assembled from material a member of the
> public can reach with a browser and no credentials — the company's own website, developer portal
> and documentation, the specifications it publishes for public use (OpenAPI, AsyncAPI, JSON Schema,
> `apis.json`, `llms.txt` and similar), its public repositories, and its public status, pricing and
> changelog pages. **Nothing here is obtained by breaching a system, defeating an access control, or
> using credentials of any kind.**
>
> **The rating is an independent assessment.** The Kin Score and Agent Readiness rating are
> independently calculated scores of a company's *public* API artifacts, produced by API Evangelist
> against a published rubric. They are not certifications, endorsements, security assessments, or
> audits, and they score published artifacts — not the quality, safety, or security of the software.
>
> **Corrections, re-scores, and removal are free.** No partnership, contract, or purchase is
> required, and you do not need to justify the request.
>
> - **Something wrong?** Open an issue on this repository, or email
>   [info@apievangelist.com](mailto:info@apievangelist.com).
> - **Published something new?** Ask for a re-score and we will re-run the rating.
> - **Want the listing taken down?** Say so and we will honor it. The profile is reduced to your
>   company name, a factual description, and a link to your own site, and the company is recorded as
>   **unrated** — never scored zero for having asked.
>
> **Response times.** Acknowledgement within **one business day**; removal or restriction within
> **two business days**; corrections and re-scores within **five business days**.
>
> **Not from the company, and here with a question?** You are welcome here — we would rather be the
> front line and point you the right way than have a good report go nowhere. What this repository
> can answer is narrow, though, so it is worth knowing who you are actually looking for:
>
> - **A question about how the API works, an account, billing, or a bug in the service** — that is
>   the company's own support, not us. We profile this API; we do not operate it and cannot see
>   your account.
> - **A bug in an open-source project we only catalog** — file it on that project's own repository.
>   This has happened with a real and correct bug report that reached us instead of the people who
>   could fix it, which helped nobody.
> - **Anything about this listing itself** — the description, the tags, the rating, a missing or
>   wrong artifact — is ours. Open an issue here.
> - **Not sure, or something general about API Evangelist or APIs.io** — open an issue on the
>   [APIs.io Inbox](https://github.com/api-search/inbox) and we will route it.
>
> **This repository contains no software, and we will never ask you to download anything.** There is
> no build, release, installer, or binary here — only text and machine-readable API descriptions, so
> there is nothing here that can be "corrupt" or need "repairing". Any issue, comment, or email
> claiming otherwise and offering a download link is not from us and is hostile. Do not follow the
> link; it is a lure. Report it to GitHub and, if you like, tell us at
> [info@apievangelist.com](mailto:info@apievangelist.com) so we can take it down.
>
> **On a security or compliance team?** Email
> [info@apievangelist.com](mailto:info@apievangelist.com) with *security* in the subject line and
> you will get a person, not a form. We will tell you exactly which public URLs this profile was
> built from so your team can see the same surface we did, and we will take the listing down on
> request while you work through it.
>
> Full detail: **[Where this data comes from](https://apievangelist.com/about/where-our-data-comes-from)**
<!-- API-EVANGELIST-PROVENANCE:END -->

Pipecat is an open-source Python framework (created by Daily) for building realtime voice and multimodal AI agents. It orchestrates pipelines of frames through pluggable services (STT, LLM, TTS, vision) and transports (Daily WebRTC, WebSocket, SmallWebRTC, telephony). Pipecat Cloud adds a hosted platform with a REST control API for deploying agents and starting/stopping agent sessions at scale.

**APIs.json:** [https://raw.githubusercontent.com/api-evangelist/pipecat-ai/refs/heads/main/apis.yml](https://raw.githubusercontent.com/api-evangelist/pipecat-ai/refs/heads/main/apis.yml)

## Tags

- AI
- Voice
- Multimodal
- Agents
- Realtime
- Framework

## Timestamps

- **Created:** 2026-06-21
- **Modified:** 2026-06-21

## APIs

### Pipecat Framework (Python SDK)

Open-source (BSD 2-Clause) Python framework whose interface is the pipecat-ai library, not a REST API. Applications wire FrameProcessors into a Pipeline, where Frames carry audio, text, images, and control signals between pluggable AI Services (STT, LLM, TTS, vision) and client Transports.

- **Human URL:** [https://docs.pipecat.ai/overview/introduction](https://docs.pipecat.ai/overview/introduction)

#### Tags

- Framework
- Python
- SDK
- Pipelines
- Frames

#### Properties

- [Documentation](https://docs.pipecat.ai/overview/introduction)
- [API Reference](https://docs.pipecat.ai/server/introduction)
- [GitHub](https://github.com/pipecat-ai/pipecat)

### Pipecat Cloud (Agents/Sessions API)

Hosted REST control API (Bearer-token authenticated) for deploying and operating Pipecat agents on Pipecat Cloud - create/list/update/delete agents, start and stop agent sessions, manage builds, secrets, and organization properties.

- **Human URL:** [https://docs.pipecat.ai/api-reference/pipecat-cloud/rest-reference](https://docs.pipecat.ai/api-reference/pipecat-cloud/rest-reference)
- **Base URL:** `https://api.pipecat.daily.co/v1`

#### Tags

- Cloud
- Agents
- Sessions
- REST
- Deployment

#### Properties

- [Documentation](https://docs.pipecat.ai/overview/cloud)
- [API Reference](https://docs.pipecat.ai/api-reference/pipecat-cloud/rest-reference)
- [OpenAPI](openapi/pipecat-ai-openapi.yml) — [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Postman Collection](collections/pipecat-ai.postman_collection.json) — [Postman Collection 2.1](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [Open Collection](collections/pipecat-ai.opencollection.json) — [Open Collection 1.0](https://schema.opencollection.com/opencollection/v1.0.0.json)

### Transports (WebRTC/WebSocket)

Realtime media transport layer of the framework. Bidirectional audio, video, and data flow over Daily WebRTC, SmallWebRTC, LiveKit, FastAPI WebSocket server, and telephony serializers (Twilio, Telnyx, Plivo, Exotel). These are SDK transport classes, not a hosted public REST/WebSocket control API.

- **Human URL:** [https://docs.pipecat.ai/server/services/supported-services](https://docs.pipecat.ai/server/services/supported-services)

#### Tags

- Transports
- WebRTC
- WebSocket
- Telephony
- Realtime

#### Properties

- [Documentation](https://docs.pipecat.ai/server/services/supported-services)
- [GitHub](https://github.com/pipecat-ai/pipecat)

## Common Properties

- [GitHub Organization](https://github.com/pipecat-ai)
- [LinkedIn](https://www.linkedin.com/company/daily-co)
- [Website](https://www.pipecat.ai)
- [Documentation](https://docs.pipecat.ai)
- [Plans](plans/pipecat-ai-plans-pricing.yml)
- [Rate Limits](rate-limits/pipecat-ai-rate-limits.yml)
- [Fin Ops](finops/pipecat-ai-finops.yml)

## Maintainers

**FN:** Kin Lane
**Email:** kin@apievangelist.com


## Top-level layout

- agentic-access/ (dir, 1 files, ~323 lines)
- apis.yml (~199 lines)
- authentication/ (dir, 1 files, ~13 lines)
- capabilities/ (dir, 1 files, ~37 lines)
- collections/ (dir, 13 files, ~3419 lines)
- finops/ (dir, 1 files, ~127 lines)
- kin/ (dir, 65 files, ~3298 lines)
- openapi/ (dir, 7 files, ~855 lines)
- plans/ (dir, 1 files, ~187 lines)
- provenance.yml (~224 lines)
- rate-limits/ (dir, 1 files, ~66 lines)
- README.md (~162 lines)
- review.yml (~114 lines)
- security/ (dir, 1 files, ~39 lines)

