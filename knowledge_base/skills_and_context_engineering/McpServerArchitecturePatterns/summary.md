# MCP Server Architecture Patterns for LLM-Integrated Applications

**Paper:** [MCP Server Architecture Patterns for LLM-Integrated Applications (Rodrigues & Vas, 2026)](https://arxiv.org/abs/2606.30317)

## Human Readable TL;DR

Anthropic's Model Context Protocol (MCP) lets an AI assistant plug into outside tools and data -- like a universal power adapter for connecting AI to databases, APIs, and apps. Since MCP launched, hundreds of these "servers" have been built, but nobody had written down what good ones actually look like. This paper is a field guide: the authors looked at fifteen real MCP servers (five running in production at a voice-AI company, ten popular public ones) and found the same five basic shapes kept showing up. They also measured a very practical limit: stuff an AI with more than about 10-15 tools at once and it starts picking the wrong one noticeably more often -- so a big part of good design is just not overwhelming the AI with choices.

## TL;DR

An industry-experience paper that catalogs five recurring MCP server architecture patterns -- Resource Gateway, Tool Orchestrator, Stateful Session Server, Proxy Aggregator, and Domain-Specific Adapter -- derived via two-cycle qualitative coding over an enumerated corpus of 15 servers (5 production servers from Celabe's ANSYR voice-AI platform, 10 public servers from the official MCP registry). Each pattern maps to a classical software-architecture ancestor (Repository, Facade, Session/Memento, Proxy, Adapter) with an "LLM-client delta" -- the twist introduced because the client selects operations by reading natural-language descriptions rather than consulting documentation. The paper backs the taxonomy with three measurements: substantial inter-rater reliability (Cohen's kappa = 0.76, N=54 held-out servers), transport latency showing protocol overhead is negligible next to network RTT, and observational production telemetry showing tool-selection accuracy drops below 90% between 10-15 tools for Claude Haiku 4.5 and between 20-30 tools for Claude Sonnet 4. It also documents four anti-patterns and cross-cutting concerns (auth, error handling, versioning, observability).

---

## Problem & Motivation

MCP (introduced by Anthropic, November 2024) standardizes how LLMs connect to external tools, resources, and prompts -- one server works with any compliant client (Claude, GPT-4, Gemini). Adoption was fast: hundreds of community servers appeared within months. What was missing was architectural guidance -- how to decompose tools, when server-side state is justified, how to aggregate many servers, when to wrap a complex API. These are ordinary API-design questions, but with an unusual constraint: LLM clients pick tools by reading natural-language descriptions, not by browsing docs or schemas, so they're sensitive to schema/description quality in ways human developers aren't. No prior software-maintenance literature described how the MCP ecosystem was structuring itself in production; prior MCP literature covers security threats (Hou et al.) and ecosystem-scale measurement (Guo et al., >8,000 servers) but not recurring server-side design structures.

---

## Main Original Ideas

1. **Five-pattern taxonomy grounded in a real, enumerated corpus.** Instead of inventing patterns abstractly, the authors derived them from 15 independently developed servers via a two-cycle qualitative coding procedure (open coding -> pattern coding), promoting a candidate only if it appeared independently in >=2 servers and solved a problem without an obvious prior solution.

2. **Resource Gateway** -- mediates all backend data access; exposes reads as Resources and unsafe-parameter queries as Tools; sanitizes backend content before it reaches the LLM (defends against prompt injection via untrusted data). Ancestor: Repository/REST.

3. **Tool Orchestrator** -- exposes composite tools that internally perform multi-system workflows (e.g., create ticket -> notify Slack -> send email) and return one summary, so the LLM reasons about one operation instead of an API graph. Ancestor: Facade/Mediator.

4. **Stateful Session Server** -- generates a session ID on connection; all tool calls carry it; server holds per-session context (in memory or Redis) since MCP tool calls are stateless by default. Ancestor: Session/Memento. Liability: the LLM must reliably pass the session ID, which isn't guaranteed.

5. **Proxy Aggregator** -- fronts N upstream MCP servers behind one endpoint, namespacing tool names (`server__tool`) to avoid collisions. Two variants: **static-merge** (unions all upstream tools -- simple but inflates visible tool count) vs. **scoped** (retrieves only the task-relevant subset per request, i.e. retrieval-over-tools). The paper explicitly recommends reaching for the scoped variant once aggregation would push a context past the tool-count accuracy budget.

6. **Domain-Specific Adapter** -- wraps an LLM-hostile API (cryptic IDs, complex auth, raw error codes) with human-readable descriptions, input normalization, output enrichment, and error translation, without reimplementing the underlying business logic. Ancestor: Adapter (GoF).

7. **Classical-pattern mapping (Table I).** Each MCP pattern is explicitly tied to a pre-LLM architectural ancestor; the paper's claimed contribution is only the "LLM-client delta" each pattern adds, not the underlying structural skeleton.

8. **Four anti-patterns** identified from code review and public issue/PR discussion, not from the derivation corpus itself: **The God Tool** (one `do_anything(action, params)` tool that collapses selection accuracy), **Unsanitized Resource Content** (prompt injection via unescaped backend data), **Synchronous Long-Running Operations** (no async callback in MCP -> client timeout; fix is job-ID + `poll_job`), and **Missing or Vague Tool Descriptions** (LLMs select by description text, not schema inspection).

---

## Key Findings

**Inter-rater reliability of the taxonomy** (N=54 held-out servers, architecture-neutral functional descriptions, two independent LLM raters -- Claude Haiku 4.5 and Claude Sonnet 4 at temperature 0):

| Metric | Value |
|---|---|
| Cohen's kappa (inter-rater) | 0.76 (95% CI [0.62, 0.88]), "substantial" |
| Raw inter-rater agreement | 81.5% |
| Agreement with author labels -- Haiku | 68.5% |
| Agreement with author labels -- Sonnet | 75.9% |
| Pilot on architecture-naming (non-neutral) descriptions | 97% |

Disagreements concentrate at three fuzzy boundaries: (1) statefulness is invisible from a function-only description (stateful servers like `git`/`puppeteer` get read as Tool Orchestrators), (2) domain/business logic is invisible (domain adapters like `kubernetes`/`salesforce`/`fhir` split between Tool Orchestrator and Resource Gateway), (3) read-heavy orchestrators (`sentry`, `notion`) get reclassified as Resource Gateways. Conclusion: statefulness and domain-logic should be treated as cross-cutting attributes layered on a primary pattern, not mutually exclusive categories.

**Transport latency** (stdio and loopback streamable-http measured end-to-end, N=100 calls + 10 warm-up; cross-host rows modeled as loopback overhead + documented same-region RTT calibration):

| Transport | Method | p50 | p95 | p99 |
|---|---|---|---|---|
| stdio (local) | measured | 0.01 ms | 0.02 ms | 0.02 ms |
| streamable-http (loopback) | measured | 0.39 ms | 0.45 ms | 0.48 ms |
| streamable-http (same-region remote) | modeled | 30.4 ms | 80.4 ms | 180.4 ms |
| Stateful Session Server (remote) | modeled | 38.4 ms | 100.4 ms | 216.4 ms |
| Proxy Aggregator (remote, single hop) | modeled | 62.4 ms | 160.4 ms | 308.4 ms |

Takeaway: protocol-layer overhead (stdio vs. streamable-http) is well under a millisecond and irrelevant once a network hop exists -- network RTT dominates by 2-3 orders of magnitude. The architecturally significant choices are co-location with the client, and whether aggregation fan-out adds another hop.

**Tool count vs. selection accuracy** (observational ANSYR production telemetry, Q1 2025, N=200 turns per bucket, buckets of {1,3,5,10,15,20,30,50} tools, Wilson 95% CI within +/-4pp):

- Claude Haiku 4.5: 91% accuracy at 10 tools (245 ms median), drops to 87% at 15 tools -- below the 90% threshold between 10-15 tools.
- Claude Sonnet 4: 95% accuracy at 10 tools (410 ms median), stays >=90% up to 20 tools, drops below 90% at 30 tools.
- Recommended budget: keep any single context under ~10-15 tools; use the scoped Proxy Aggregator (retrieval-over-tools) rather than static merging once a fleet would exceed this.
- Consistent with prior work at larger scale: Gan & Sun (RAG-MCP) report >90% success up to ~30 tools degrading sharply past ~100; Kate et al. measure a 7-85% accuracy drop as catalogs grow.

**Cross-cutting concerns:** authenticate at the transport layer (Bearer tokens, scoped to tool sets) not inside handlers; return structured tool errors rather than throwing exceptions; version via the `initialize` response and keep old schemas alive during migration; log tool name/input hash/latency/output size/error code per call as the primary LLM-debugging surface.

---

## Suggestions & Future Directions

1. Independent **human dual-coding** of the derivation corpus at ecosystem scale (current derivation used single-coder open coding with secondary verification, not independent dual coding).
2. A **multi-model rater panel** beyond two Claude models, to separate genuine taxonomy ambiguity from shared-LLM blind spots (both current raters are LLMs and may share blind spots -- a construct-validity threat the authors flag explicitly).
3. A **predictive study** linking pattern choice to measured latency and reliability, turning the catalog from descriptive vocabulary into an empirical instrument.
4. A **stratified replication at ecosystem scale** (>8,000 servers per Guo et al.) since the derivation corpus is only 15 servers from one organization plus the public registry.
5. **Security analysis of MCP attack surfaces**, particularly prompt injection via resources.
6. Acknowledged limitations: 3 of 5 transport-latency rows are modeled, not measured end-to-end; the tool-count study is observational (one organization's production tool surface, not a controlled experiment) and its raw session logs are not released; the reliability study's classification corpus uses descriptions, not running servers, so classifier accuracy on live production servers may differ.

---

## Authors & Institutions

Carson Rodrigues (Celabe, operator of the ANSYR voice AI platform), Oysturn Vas (University of Waterloo).
