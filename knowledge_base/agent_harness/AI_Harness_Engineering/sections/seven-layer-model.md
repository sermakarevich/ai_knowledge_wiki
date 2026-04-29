> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## The Seven-Layer Model

The AI Harness is organized as seven concentric layers around the language model. Each layer is independent; you can upgrade or swap components within a layer without rearchitecting the others.

### Overview Diagram

```
┌─────────────────────────────────────────┐
│       Layer 1: Instruction              │
│  (Prompts, context, structured output)  │
├─────────────────────────────────────────┤
│         Layer 2: Tools                  │
│   (Safe actions, schemas, validation)   │
├─────────────────────────────────────────┤
│      Layer 3: Memory & Retrieval        │
│  (State, RAG grounding, context)        │
├─────────────────────────────────────────┤
│        Layer 4: Execution               │
│  (Sandboxing, isolation, limits)        │
├─────────────────────────────────────────┤
│      Layer 5: Policy & Approval         │
│  (Guardrails, filters, gates)           │
├─────────────────────────────────────────┤
│      Layer 6: Observability             │
│  (Tracing, logging, audit)              │
├─────────────────────────────────────────┤
│      Layer 7: Evaluation                │
│  (Metrics, datasets, assessment)        │
├─────────────────────────────────────────┤
│     LANGUAGE MODEL (Center)             │
│  (The weights, the inference engine)    │
└─────────────────────────────────────────┘
```

---

## Layer 1: Instruction

**Purpose:** Encode what the agent should do, what constraints apply, and how to behave when things go wrong.

**Core Components:**

1. **Three-tier context hierarchy:**
   - **System context:** Immutable instructions that never change (e.g., "You are a customer support agent"; "Never make up information")
   - **Domain context:** Domain-specific knowledge, policies, reference data (e.g., API docs, compliance rules, product FAQs)
   - **Request context:** The specific user input, session state, and immediate context for this interaction

2. **Structured outputs:** Use JSON schemas or other machine-readable contracts to constrain the model's output format.

3. **Failure-aware prompting:** Don't just ask the model to "do the right thing." Instead, tell it:
   - What to do if it's uncertain
   - How to ask for clarification
   - When to refuse an action
   - What recovery looks like

4. **Prompt versioning:** Treat prompts like code. Version them, test them against golden datasets, and roll them out incrementally.

5. **Spotlight techniques:** Mark untrusted external data with special tokens (e.g., `<UNTRUSTED>...</UNTRUSTED>`) so the model treats it with suspicion.

**Key Questions for Interviews:**
- How do you version and test prompts?
- How would you detect a prompt injection attack?
- What belongs in system vs. domain vs. request context?

---

## Layer 2: Tools

**Purpose:** Give the agent safe actions it can perform, with explicit contracts and validation at every step.

**Core Concept: The Trust Ladder**

Before the model's request reaches an action, it must pass:

1. **Input validation:** Parse the request; check types, sizes, formats
2. **Schema enforcement:** Does the parsed output match the declared contract?
3. **Permission checks:** Is this user/org allowed to do this?
4. **Sandboxing:** Can we safely execute this in isolation?

Each rung filters out a class of failures.

**Key Components:**

1. **Function schemas:** Machine-readable contracts defining what a tool does, what inputs it accepts, and what it returns.

2. **Input validation:** Never trust the model's JSON parsing. Validate at the API boundary using strict parsers and type checkers.

3. **Read vs. write separation:** Segregate read-only queries (which can be cached, retried, optimized) from actions with side effects (which require idempotency, approval, audit).

4. **Idempotency & retries:** Design tools so that retrying the same request N times has the same effect as running it once. Use idempotency keys.

5. **Error messages for LLM consumption:** Error messages for the model should guide it to recovery, not just report the failure (e.g., "User ID not found. Try a different ID." instead of "404").

6. **Tool result formatting:** Return structured data, not raw text, so the model can parse reliably.

**The Model Context Protocol (MCP):**

MCP is a standard for composing tool servers (the agent) with tool implementations (servers). It defines:
- **Clients:** Agents that invoke tools
- **Servers:** Tool implementations
- **Transports:** How they communicate (stdio, HTTP, SSE)
- **Capability discovery:** The agent queries the server for what tools are available

MCP enables:
- Decoupled tool development (teams build servers independently)
- Composition (one agent can orchestrate multiple tool servers)
- Versioning (servers can be updated without updating the agent)
- Security (explicit capability boundaries)

**Key Questions for Interviews:**
- Design a tool for "transfer funds." What goes in the schema? How do you validate inputs? What about idempotency?
- A tool call returns a 500 error. What does the agent see? How should it recover?
- Why separate read and write operations?

---

## Layer 3: Memory & Retrieval

**Purpose:** Ground the agent in relevant information and maintain state across interactions.

**Three Kinds of Memory:**

1. **Scratch memory:** The in-context token budget. It's fast (no latency), but limited. Use for the current task and recent history.

2. **Episodic memory:** Recent learnings from this conversation thread. What did we discover? What failed? Where are we in the task? Typically stored in a vector DB or structured key-value store.

3. **Semantic memory:** Static facts, domain knowledge, reference docs. Accessed via RAG. This is the long-term knowledge base.

**Key Components:**

1. **Memory decay:** Don't trust memory indefinitely. Re-validate facts before using them; detect if old memory has been invalidated by subsequent events.

2. **Memory poisoning:** Assume external data sources may be adversarial. Don't let a poisoned document change the agent's behavior.

3. **Chunking strategy:** How you break up documents matters. Token-based chunking ignores semantic boundaries. Semantic chunking (breaking at section headers, natural sentence boundaries) works better. Domain-specific chunking (e.g., breaking on code blocks, function definitions) works best.

4. **Embedding models:** Different models have different strengths. Some are good at semantic search; others at dense retrieval. Test and measure.

5. **Hybrid retrieval:** Combine vector search (semantic similarity) with BM25 (keyword matching) and structured queries. Each catches different relevance patterns.

6. **Citation & provenance:** Always include where the retrieved fact came from. Support audit trails.

7. **Context windows:** Longer context windows (4K → 100K → 200K tokens) change the game. You can include entire documents instead of snippets. But cost scales linearly, so route carefully.

**Key Questions for Interviews:**
- A user asks a question; the agent retrieves 3 documents. One is relevant but outdated. How do you detect that?
- Design a RAG system for a product with 100K technical docs. What's your chunking strategy?
- How would you prevent prompt injection through a retrieved document?

---

## Layer 4: Execution

**Purpose:** Safely run arbitrary code (or model-generated code) in isolation with bounded resources.

**Core Concept: Trust Boundaries**

Understand what you're trusting and isolate it:
- Trust the model's intent, not its code
- Trust your sandbox, not the executed code
- Trust audit logs, not operator memory

**Isolation Techniques (in order of strength):**

1. **Docker:** Process isolation. Lightweight, widely used. Not truly secure against privileged container escape.

2. **gVisor:** Virtualized system calls. The sandbox reimplements Linux syscalls in userspace, preventing direct kernel access. Good security/performance trade-off.

3. **Firecracker:** Lightweight VMs (microVMs). True hardware isolation. Startup latency ~100ms. Good for functions that need strict isolation.

4. **Kubernetes jobs:** Orchestrated container execution. Good for multi-container workloads.

**Per-Task Isolation:**

Create a fresh, isolated environment for each execution:
- Dedicated filesystem (never shared state)
- Isolated network (allowlist only necessary IPs)
- Bounded resource limits (CPU, memory, disk I/O, execution time)
- Credential scoping (inject secrets only for what the task needs)
- Cleanup after failure (don't leave artifacts)

**Filesystem Controls:**

- **Credential scoping:** If a task only needs S3 access, give it a temporary STS token scoped to one bucket, not an AWS account key.
- **Secrets never logged:** Strip secrets from output before logging. Use a secrets manager with audit trails.
- **Immutable logs:** Once written, don't modify. Use append-only log stores.

**Key Questions for Interviews:**
- I give the agent code to execute. How do you prevent it from exfiltrating secrets?
- A container execution times out. What's your recovery? How do you clean up?
- Design a system where agents can run user-uploaded Python code safely.

---

## Layer 5: Policy & Approval

**Purpose:** Enforce rules about what the agent can do, when it needs human approval, and how to refuse unsafe requests.

**Core Components:**

1. **Input guardrails:** Reject obviously bad requests before they reach the model. This saves cost and prevents abuse.

2. **Inline guardrails:** During generation, detect if the model is heading toward a policy violation (e.g., generating PII) and steer it away.

3. **Output guardrails:** Filter final output for policy violations, sensitive data, etc.

4. **Policy engines:** Express rules as code. Examples:
   - "If cost > $100, require human approval"
   - "If user is new, require additional verification"
   - "If request involves deletes, log decision immutably"

5. **Approval gates:** For high-stakes actions (delete, refund, message send), pause and ask a human before proceeding. Design approval workflows that don't create bottlenecks.

6. **Refusal & degradation:** When you can't fulfill a request, don't just refuse. Suggest an alternative:
   - Can't delete? Offer archive instead.
   - Can't answer? Offer to escalate to support.
   - Can't fulfill due to policy? Explain why.

**Content Filtering:**

- Regional/regulatory compliance (GDPR, CCPA, etc.)
- Brand safety (don't generate content that violates brand guidelines)
- Secret handling (detect and redact API keys, passwords, PII)
- Prompt injection detection (distinguish legitimate colons from injection attempts)

**Key Questions for Interviews:**
- Design an approval workflow for "transfer funds > $10K" that doesn't make humans a bottleneck.
- A user asks for PII about another user. How do you prevent the agent from answering?
- How do you detect a prompt injection attack in real time?

---

## Layer 6: Observability

**Purpose:** Instrument every decision point so you can understand what happened, why, and whether it was correct.

**Core Instrumentation Points:**

1. **Decision logs:** Record:
   - Which instruction version ran?
   - Which tools were invoked and with what args?
   - What was the model's output?
   - Which policy rules were evaluated?
   - What was the decision (approve/reject/escalate)?

2. **Trace spans:** Distributed tracing (e.g., OpenTelemetry):
   - Connect related operations with trace IDs
   - Record latency, errors, and dependencies
   - Propagate trace context across service boundaries

3. **Cost tracking:**
   - Prompt tokens, completion tokens, by model
   - Cost per user, per tenant, per feature
   - Cost attribution (which feature used most tokens today?)
   - Cache hit rates (prompt caching savings)

4. **Anomaly detection:**
   - Baselines: latency, error rate, cost per interaction, success rate
   - Alerts when behavior deviates (e.g., "success rate dropped from 95% to 60%")
   - Root cause support ("What changed at 2pm?")

5. **Audit logs:** Immutable records of who did what when and why. Used for:
   - Compliance (regulatory audits)
   - Incident response ("Show me all requests from this user")
   - Debugging ("What happened at this exact time?")

6. **Prompt & completion capture:** Log the full prompt and completion for every request (respecting privacy/security). This is critical for debugging misbehavior.

**Key Questions for Interviews:**
- Your eval says 85% success; production shows 60%. How do you debug?
- Design the observability for an agent that can approve refunds. What must you log?
- How do you detect a data poisoning attack through a retrieved document?

---

## Layer 7: Evaluation

**Purpose:** Define what "good" means, measure whether you're achieving it, and catch regressions early.

**Core Components:**

1. **Golden datasets:** Small, curated test sets (100-1000 examples) that cover happy paths, edge cases, and known failure modes. Update quarterly.

2. **What to measure:**
   - **Correctness:** Does the agent answer the question accurately?
   - **Safety:** Does it refuse bad requests? Does it avoid generating PII or secrets?
   - **Cost:** Does it route to cheaper models when appropriate?
   - **Latency:** Does it return in expected time?
   - **Composition:** Can the agent's output feed into downstream systems?

3. **LLM-as-judge:** Use a different LLM to score outputs (e.g., "Is this answer correct? Rate 1-5"). Validate the judge independently (it can be biased).

4. **Statistical rigor:** Don't report point estimates. Report confidence intervals, sample sizes, and effect sizes.

5. **Regression testing:** Before deploying, run against golden datasets. Catch breaking changes early.

6. **Eval-as-a-service:** External evaluation systems decouple iteration from feedback. You develop locally, commit to a branch, and an external service runs evals automatically.

**Key Questions for Interviews:**
- Design a golden dataset for a customer support agent. What edge cases?
- How do you measure whether guardrails are working without causing false negatives?
- Your new prompt improves correctness by 2% but increases cost by 20%. What do you do?

---

## Why Seven Layers?

Each layer solves a class of problems:
1. **Instruction** → "What should the agent do?"
2. **Tools** → "What can it safely do?"
3. **Memory** → "What does it know?"
4. **Execution** → "How does it run safely?"
5. **Policy** → "What are we comfortable with?"
6. **Observability** → "What happened?"
7. **Evaluation** → "Did it work?"

Independence matters: You can redesign Layer 1 (prompts) without touching Layers 4-7 (execution, policy, observability). You can add a new tool (Layer 2) without updating evaluation metrics (Layer 7).

This independence makes the harness composable and upgradeable.

---

## Layer Dependencies

| Layer | Depends On | Notes |
|-------|-----------|-------|
| 1: Instruction | None | Foundational; defines behavior |
| 2: Tools | 1 | Agent must know how to invoke tools |
| 3: Memory | 1, 2 | Instruction and tools determine what to remember |
| 4: Execution | 2, 3 | Tools and memory determine what needs isolation |
| 5: Policy | 1, 2, 4 | Based on what agent should/can do and how it runs |
| 6: Observability | 1-5 | Observes all upstream layers |
| 7: Evaluation | 1-6 | Measures outcomes across all layers |

---

## Key Interview Questions (Across All Layers)

1. **Design question:** "Build an agent that can answer questions about a company's internal docs. Design the harness." (Answer should touch all 7 layers.)

2. **Operational question:** "Your eval shows 85% success, but production shows 60%. Debug it." (Tests understanding of what can go wrong between eval and production.)

3. **Failure fluency:** "What are the ways this agent can fail? How would you detect each? How would you recover?" (Tests failure taxonomy.)

4. **Trade-off question:** "Cost or correctness? Latency or safety? Defend your choice." (Tests design judgment.)
