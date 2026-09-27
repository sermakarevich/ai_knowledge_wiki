> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: Workers Delos — Autonomous AI Workers, 24/7

## Claims vs. evidence

- **Claim: "Hire autonomous AI workers that work like real teammates, 24/7."** Evidence: none beyond marketing copy. No task-success rates, uptime numbers, or comparisons against human or baseline-agent performance across the 35 pages.
- **Claim: "Over 10,000 workers deployed; 15 profiles; 200+ use cases with time savings."** Evidence: vendor-supplied counts only. Worker pages (Laura, James, Nova, Henry, Arjun…) cite self-reported figures (e.g. 2.8M visits, 99.98% uptime) with no method, baseline, or third-party check; per-worker pricing even renders as "0", a scrape gap the digest flags.
- **Claim: "Teams of 1–15 with shared memory and coordination; personal clone that reasons like you."** Evidence: mechanism described (shared context, style learning, approval scopes), but no data on coordination failures, memory limits, or how much is reusable template versus customer configuration.
- **Claim: "Secure RAG (Retrieval-Augmented Generation) grounding, per-tenant memory, logged permissioned actions with human approval."** Evidence: this is the strongest part — the tech page names models (GPT, Claude, Gemini), RAG sources, isolated memory, MCP (Model Context Protocol) orchestration, and audit logs. Still no retrieval accuracy, benchmark scores, or failure examples.
- **Claim: "Enterprise-grade security: encryption, isolation, no training on your data, GDPR, SOC 2."** Evidence: badges plus FAQ confirmation only. No audit reports, data-residency regions, subprocessor list, or incident history.
- **Claim: "3000+ no-code integrations in under 5 minutes."** Evidence: plausible via an aggregator plus OAuth (standard password-free login), but depth per tool (read vs. write, webhook vs. polling) is undisclosed.
- **Net judgment:** the digest supports existence and breadth of the offer, not effectiveness; every load-bearing claim (autonomy quality, scale, security depth) is asserted, not evidenced.

## Genuinely new vs. repackaged

- **Genuinely new (packaging, not science):** "hire a worker, not a chatbot" — durable identity, role-calibrated personality, memory, mission handoff inside Slack/Teams, plus team assembly and self-cloning — is a real product choice competitors rarely bundle this completely.
- **Genuinely useful:** five-minute no-code onboarding, 200+ filterable use cases with ROI (Return on Investment), and a Companion browser extension lower adoption friction versus standalone AI apps.
- **Repackaged:** the engine — role prompts, tool-calling agents, RAG over docs, chat memory, multi-agent chains — is standard 2024–2026 agent-stack practice; model auto-switching and MCP use are table stakes.
- **Repackaged:** "3000+ integrations" is almost certainly an aggregator, and the named tools (Gmail, Notion, HubSpot, Salesforce, Jira, GitHub, Figma) are the usual suspects; personalities read as prompt-level persona plus stored preferences, not a research advance.
- **Blurred line:** worker pages mix role titles with mismatched voices (e.g. designer Sophie described with prospecting copy), suggesting templated catalog generation — which undercuts the "each worker is unique" story.
- **Honest credit:** if 10,000 workers are truly active, the team solved unglamorous hard problems — onboarding, connector maintenance, channel ops — that the site undersells.

## Weaknesses and blind spots

- **No evaluation story:** no benchmarks, pass/fail rates, hallucination (confident falsehood) numbers, override rates, or before/after productivity data — despite the blog promising "frameworks and numbers".
- **Autonomy risk under-addressed:** workers running "end to end, 24/7" can compound mistakes 24/7; approvals and logging are named but approval granularity, rollback, and blast-radius limits are never specified.
- **Memory/RAG failure modes ignored:** stale docs, conflicting sources, over-remembering, cross-mission leakage — the top failure modes of exactly this architecture — go unmentioned.
- **Vague security depth:** permission granularity, secret handling, tenant (one customer's isolated share) separation, and offboarding (what happens to memory/access when a worker is removed) are missing.
- **Scale ambiguity:** 10,000 workers could be active teammates or one-click trials; 15 profiles is thin across seven-plus functions, and catalog copy-paste errors hint at quantity over depth.
- **Missing operational facts:** no real per-worker price, no SLA (Service-Level Agreement — guaranteed uptime/support promise), no latency, no residency regions.
- **No multi-worker coordination story:** overlapping workers editing the same CRM, docs, or code with shared memory is a conflict-resolution problem the site never discusses.
- **Thin company page:** the About page is mostly navigation plus a LinkedIn pointer — team size, funding, and history are absent, so vendor longevity cannot be judged.
- **Blog authorship loop:** articles "written by AI Workers, reviewed by editors" showcase the product but are also self-graded homework; customer stories (startup support, SMB marketing, 8-worker finance team) give steps without verifiable numbers.

## Applicability

- **Where it could fit:** well-scoped, reversible, high-volume chores in Slack/Teams — ticket triage, status rollups, CRM hygiene, meeting follow-ups, first-draft content — with human review before anything external or irreversible.
- **Where it does not fit:** autonomous code merges, finance postings, HR decisions, customer-facing sends, or production-data writes without approvals and full audit trails.
- **What to demand before any pilot:** per-worker permission scopes, read-only-first mode, approval gates on writes, full action logs, memory inspection/deletion, crisp offboarding.
- **Suggested pilot shape:** one worker, one team, one reversible workflow (e.g. weekly reports), 2–4 weeks, predefined metrics (time saved, error and override rates) plus a kill switch.

- **Relevance to my work**
  - **AI/ML engineering:** useful reference design for packaging agents as hireable teammates with memory and channel-native UX (user experience); not a component to build on until evals, logs, and permission controls are proven.
  - **Agentic systems:** the mission-handoff pattern (explicit mission spec, tool scopes, review gate, memory with expiry) plus use-case catalog discipline is worth copying into own agents; the missing measurable autonomy guardrails are what own stack should add first.
  - **Elisity data platform:** never grant a third-party worker broad lake or pipeline access on badges alone; if trialed, sandbox on mirrored non-sensitive data, read-only scopes, human approval on every write, and measure retrieval grounding before expanding.

## What this changes

- **It changes buying, not building:** confirms the market shift from "chat with AI" to "staff AI teammates inside existing workflows" — onboarding speed and channel presence now matter as much as model quality.
- **It does not change the engineering checklist:** RAG grounding, memory governance, least-privilege scopes, approvals, and evals remain the real work; Delos names them without evidencing them.
- **Practical takeaway:** treat the site as a packaging benchmark for own agent UX — five-minute setup, visible worker identity, in-channel progress, 200-use-case catalog — while keeping own reliability and security bar unchanged.
- **What would upgrade pitch to proof:** one public eval (task set, pass rate, override rate), one named customer story with numbers, one security whitepaper (scopes, logging, retention, subprocessors).

## Verdict

- A competent, broad product pitch — catalog, teams, clone, Companion, integrations, plausible security labels — with zero verifiable evidence on quality, autonomy safety, or operational depth, plus catalog-quality red flags.
- Pricing opacity is a minor flag: the Office Suite bands (€10–€80) are clear, but per-worker pricing is unscrapeable, so total cost of a 15-worker team cannot be estimated from the site.
- For low-risk internal chores a fenced, read-heavy experiment may be justified; for anything touching production data, customers, money, or hiring, the blind spots disqualify it today.
- Track for real case studies, evals, and a disclosed permission/audit model; allow only a fenced trial if a concrete low-risk use case appears — verdict: **watch**.
