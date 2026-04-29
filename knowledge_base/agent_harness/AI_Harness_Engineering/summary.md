# AI Harness Engineering Interview Preparation Handbook

**Source:** AI Harness Engineering Interview Preparation Handbook (2026 Edition, AI Engineering Insider & Lankhot Sagian)  
**Type:** Professional reference guide for production AI agent engineering  
**Audience:** AI engineers, platform engineers, SDETs, DevOps/MLOps, security engineers, interview candidates

---

## Human Readable TL;DR

Think of an AI agent like a horse: the model is the horse, but the "harness" is everything that turns that horse into useful work. The harness includes all the infrastructure, safety rails, monitoring, and controls that let you run thousands of conversations reliably in production when things break, when inputs are adversarial, and when you need to audit exactly what happened. This handbook teaches the engineering discipline that sits between prompt engineering and application logic.

---

## TL;DR

AI Harness Engineering is the discipline of designing and operating the runtime, control layer, and infrastructure that wraps a language model so its outputs can be trusted, audited, and composed into production software. The core framework is the "seven-layer model": Instruction, Tools, Memory, Execution, Policy, Observability, and Evaluation. Production AI agents require the same rigor as distributed systems—queues, timeouts, retries, idempotency, circuit breakers, sandboxing, and comprehensive instrumentation.

---

## The Core Philosophy

**Model vs. Harness:**
- **The Model:** The commodity (weights, inference, token consumption)
- **The Harness:** The engineering—everything that makes the model's output trustworthy, auditable, and composable

In 2024-2025, the conversation shifted from "how do we prompt well?" to "how do we build production-grade agents?" This handbook codifies the engineering practices that best practitioners already use.

---

## The Seven-Layer Model

The harness consists of seven concentric layers around the language model:

| Layer | Purpose | Examples |
|-------|---------|----------|
| **1: Instruction** | System prompts, context tier definitions, failure-aware prompting | Three tiers: system context, domain context, request context |
| **2: Tools** | Safe action design, function schemas, input validation, error handling | Tool calling, MCP servers, result formatting |
| **3: Memory & Retrieval** | State persistence, episodic memory, semantic memory, RAG grounding | Scratch memory, long-context windows, vector stores |
| **4: Execution** | Sandboxing, isolation, resource limits, code execution safety | Docker, gVisor, Firecracker, per-task worktrees |
| **5: Policy** | Guardrails, content filtering, approval gates, refusal logic | Input/output filters, secret handling, governance |
| **6: Observability** | Tracing, cost tracking, anomaly detection, audit logs | Span tracing, prompt/completion capture, decision logs |
| **7: Evaluation** | Golden datasets, LLM-as-judge, statistical rigor, benchmark tracking | Regression suites, eval-as-a-service, failure analysis |

**Key Principle:** Each layer is independent but builds on the lower layers. You can swap models or tools without rearchitecting the whole system.

---

## Problem & Motivation

### The Gap

In 2023, the conversation was about prompts. In 2024, it shifted to agents. But agent design requires engineering discipline that most teams lack:

- **Reliability:** How do you handle edge cases, timeouts, and adversarial inputs?
- **Audit:** How do you prove what the agent did and why?
- **Composition:** How do you plug agents into larger systems without breaking them?
- **Cost:** How do you route requests to cheaper models without degrading quality?
- **Safety:** How do you prevent prompt injection, unintended actions, or policy violations?

Traditional software engineering solved these problems decades ago (SRE, DevOps, SecOps, platform engineering). But AI adds new dimensions: non-determinism, emergent behavior, and the fact that the model itself is a third-party black box.

### Why This Is a Discipline

A harness engineer is not a prompt whisperer. A prompt whisperer optimizes one conversation. A harness engineer builds the infrastructure that makes a hundred thousand conversations go well when nobody's watching, when the input is adversarial, when the model provider silently updates weights, and when the cost accountant wants a 5x reduction by Friday.

---

## Main Concepts & Layers (Expanded)

### Layer 1: Instruction Engineering
- **Three tiers of context:** System prompt (unchanging, immutable instructions), domain context (docs, policies, domain knowledge), request context (user input, session state)
- **Structured outputs:** Constrain LLM output format with JSON schemas or other contracts
- **Failure-aware prompting:** Build in recovery logic; don't just ask the model to "do the right thing"
- **Prompt libraries:** Versioned, tested, composed from reusable pieces
- **Spotlight techniques:** Mark untrusted content so the model treats it with suspicion

### Layer 2: Tools & MCP
- **Trust ladder:** Input validation → schema enforcement → permission checks → sandboxing
- **Function schemas:** Explicit, machine-readable contracts for what a tool does
- **Input validation:** Validate at the API boundary; never trust the model's JSON parsing
- **Read vs. write separation:** Segregate read-only queries from actions with side effects
- **Retries & idempotency:** Design tools to handle `{retry, at-most-once, at-least-once}` semantics
- **Model Context Protocol (MCP):** Standard for composing tool servers; clients (agents), servers (tools), and transports (stdio, SSE)

### Layer 3: Memory & Retrieval
- **Three kinds of memory:**
  - **Scratch:** In-context surface (the token budget)
  - **Episodic:** Recent conversation history, learnings from this thread
  - **Semantic:** Domain knowledge, static facts, grounding for RAG
- **Memory decay:** Validate memory freshness; detect poisoning
- **Chunking & embedding choice:** Use domain-aware chunking, not just token windows
- **Hybrid retrieval:** Combine vector search (semantic) with BM25 (keyword) and structured queries
- **Citation & provenance:** Track where facts came from; support audit

### Layer 4: Execution
- **Sandboxing matters:** Default Docker is not enough; use gVisor (virtualized system calls) or Firecracker (lightweight VMs)
- **Trust boundaries:** Understand what you're trusting and isolate it
- **Per-task isolation:** Dedicated worktree per execution; clean up after failure
- **Network policies:** Explicit allowlists; block egress by default
- **Filesystem controls:** Credential scoping, secrets never logged

### Layer 5: Policy & Approval
- **Guardrails:** Input (reject bad requests), inline (correct mid-generation), output (filter results)
- **Content filtering:** Region/regulatory compliance, brand safety, secret handling
- **Policy engines:** Express rules as code (e.g., "if cost > $X, require approval")
- **Approval gates:** Human-in-the-loop for high-stakes decisions
- **Refusal & degradation:** Fail gracefully; don't just refuse

### Layer 6: Observability
- **Tracing:** Every decision point instrumented; connect trace IDs across services
- **Cost tracking:** Prompt caching savings, model routing decisions, token usage by dimension
- **Anomaly detection:** Statistical baselines for latency, error rate, cost per user
- **Audit logs:** Immutable record of what ran and why
- **Feedback signals:** Integration with monitoring systems (SIEM, incident response)

### Layer 7: Evaluation
- **Why evaluation is engineering, not QA:** Define success criteria before building; measure A/B, not subjective quality
- **What to evaluate:** Correctness (does it answer the question?), safety (does it refuse bad requests?), cost (does it route efficiently?), latency (does it return in time?)
- **Golden datasets:** Small, curated test sets for regression; updated quarterly
- **LLM-as-judge:** Use a different LLM to score outputs; validate the judge independently
- **Statistical rigor:** Report confidence intervals, not just point estimates
- **Eval-as-a-service:** External evaluation systems decouple iteration from feedback

---

## Key Findings & Patterns

### Agent Loop Architecture
```
Instruction (prompt) → Tools (act) → Memory (persist) → Execution (run)
  ↓
Policy (check) → Observability (log) → Evaluation (measure)
  ↓
[Feedback loop: update instruction, tools, or policy]
```

### The Trust Ladder
Before trusting the model's output to an action, it must pass:
1. **Input validation:** Is the request well-formed?
2. **Schema enforcement:** Does the parsed output match the contract?
3. **Permission checks:** Is this user allowed to do this?
4. **Sandboxing:** Can we safely execute this in isolation?

### Three Skills Interviewers Actually Test

1. **Design judgment:** Choosing reasonable trade-offs among architecture, cost, latency, and failure modes. (This measures real experience.)
2. **Operational instinct:** Understanding what happens minute-to-minute under load, adversarial input, and model provider outages. (Deep-dive round.)
3. **Failure fluency:** Naming failure modes, recovery paths, and design for recoverability. (What senior engineers listen for.)

---

## Typical Structure & Topics Covered

### Foundations (Chapters 1-3)
- What is AI harness engineering? (One-sentence definition + mental models)
- The seven-layer model (visualization, dependencies, why this shape)
- Core concepts: agent loop, state and continuation, tools, schemas, handlers, specialist sub-agents

### System Design & Tools (Chapters 4-8)
- Instruction engineering: prompt hierarchy, structured output, failure-aware design
- Skills and reusable behaviors: taxonomy, testing, versioning, tool discovery
- Tool calling: trust ladder, function schema design, input validation, error handling
- **MCP (Model Context Protocol):** Why protocols matter; clients, servers, capability discovery, composition
- Harness MCP server: Exposing platform resources; audit trails; governed workflows

### Data & Execution (Chapters 9-11)
- Memory and state: scratch, episodic, semantic; memory decay and poisoning
- Retrieval and grounding: RAG architecture, chunking, embedding choice, hybrid search, citation
- Sandboxed execution: trust boundaries, isolation (Docker, gVisor, Firecracker), filesystem controls, credential scoping

### Quality & Verification (Chapters 12-14)
- Guides, sensors, and self-correction: computational vs. inferential controls, recursive correction loops
- Evaluation as engineering: golden datasets, LLM-as-judge, statistical rigor, benchmarks
- Failure modes and reliability: taxonomy of failures, recovery strategies, chaos engineering, partial state

### Safety & Governance (Chapters 15-16)
- Guardrails: input filtering, prompt injection, content policies, refusal design
- Governance: identity and authentication, RBAC, audit integration, incident response, vendor risk, regulatory compliance

### Operations (Chapters 17-19)
- Tracing and observability: GenAI-specific instrumentation (prompt/completion capture, cost tracking, decision logs)
- Runtime engineering: model routing, batching, caching, concurrency control, latency optimization
- Multi-agent systems: composition patterns, handoff protocols, durability, failure handling across agents

---

## Suggestions & Future Directions

### Acknowledged Limitations
- The field moves faster than any printed material
- Specific tools will be replaced; the *shape* of the problem will not
- Code examples are illustrative, not production-ready

### Author Guidance
- Learn the **shape** of the problem (the seven layers, the trust ladder, failure modes)
- Understand the **why** (why sandboxing matters, why observability is not optional)
- Implement the **tooling** (start with what exists; the problem is not novel, the harness is)
- Do the exercises: Each chapter has system design prompts (45-minute scope problems) and interview focus boxes

### For the Field
- This is a discipline in its infancy; practitioners are still figuring out best practices
- The harness principles (isolation, observability, composition, audit) are borrowed from distributed systems and will endure
- Model specifics will change; engineering principles will not

---

## Authors & Context

**Primary Author:** AI Engineering Insider (with Lankhot Sagian)  
**Edition:** 1.0, 2026  
**Published by:** AI Engineering Insider (Premier Technical Series)

This handbook distills patterns from interviews, on-call incidents, and production deployments across dozens of AI-first companies as of 2026. The preface emphasizes that the *shape* of the harness (its seven layers, its failure modes) is more durable than any specific tool or model.

---

## How to Use This Guide

**For interview candidates:**
- Read Parts I–II and VII for foundations and safety
- Work through the system design prompts at the end of each part
- Practice articulating design trade-offs out loud
- If time is short, focus on the "Key Insight" boxes and failure-fluency chapters (14, 15)

**For engineers building agents:**
- Skim all parts once to understand the landscape
- Deep-dive into the parts relevant to your role (tooling, data, observability, safety, operations)
- Use the production readiness checklist in the appendices before shipping

**For interviews:**
- Interviewers open with the one-sentence definition (Section 1.1) to separate framework-absorbed candidates from those who understand the concept
- Focus on operational instinct: "Your eval says 85% success, but production shows 60%; debug it"
- Listen for failure fluency: naming failure modes, recovery paths, and irreversibility of actions
