> **Guide:** [[summary]]

# AI Harness Engineering -- Deep Dive

Comprehensive exploration of production AI agent engineering principles, organized by engineering domain.

## Sections

| Section | Focus |
|---------|-------|
| [[sections/seven-layer-model\|The Seven-Layer Model]] | Core architectural framework: Instruction, Tools, Memory, Execution, Policy, Observability, Evaluation |
| [[sections/instruction-engineering\|Instruction Engineering]] | Prompt hierarchy, structured outputs, failure-aware design, prompt libraries, context management |
| [[sections/tool-calling-and-mcp\|Tool Calling & MCP]] | Safe action design, function schemas, trust ladder, Model Context Protocol as composition standard |
| [[sections/memory-and-retrieval\|Memory, State & Retrieval]] | Scratch/episodic/semantic memory, RAG architecture, chunking strategies, retrieval grounding |
| [[sections/sandboxing-and-execution\|Sandboxing & Execution]] | Trust boundaries, isolation techniques (Docker, gVisor, Firecracker), credential scoping, filesystem controls |
| [[sections/policy-and-guardrails\|Policy & Guardrails]] | Input/output filtering, content policy, approval gates, refusal design, governance layers |
| [[sections/observability-and-instrumentation\|Observability & Instrumentation]] | Tracing, cost tracking, anomaly detection, audit logs, decision point instrumentation |
| [[sections/evaluation-and-testing\|Evaluation & Testing]] | Golden datasets, LLM-as-judge, statistical rigor, regression suites, eval-as-a-service |
| [[sections/failure-modes-and-reliability\|Failure Modes & Reliability]] | Taxonomy of failures, recovery strategies, partial state, chaos engineering for agents |
| [[sections/multi-agent-orchestration\|Multi-Agent Orchestration]] | Composition patterns, durable orchestration, handoff protocols, failure handling across agents |

---

## Core Concept: Model vs. Harness

The handbook's central insight separates the **model** (the commodity—weights, inference, tokens) from the **harness** (the engineering). This distinction is critical:

- **Model engineers** optimize: inference speed, model size, training data quality, fine-tuning
- **Harness engineers** optimize: reliability, auditability, composability, cost, safety, compliance

A production AI agent requires both. Most failures in production are harness failures, not model failures.

---

## The Trust Ladder

Before the model's output reaches production, it must pass (in order):

1. **Input validation:** Well-formed request? Size checks? Type checks?
2. **Schema enforcement:** Does the parsed output match the declared contract?
3. **Permission checks:** Is this user/org allowed to do this action?
4. **Sandboxing:** Can we safely execute this in isolation? Are resources bounded?
5. **Audit & reversal:** Can we undo this? Is it logged immutably?

Each rung prevents classes of failures upstream.

---

## Key Principles Across All Layers

### 1. Observability is Non-Negotiable
Every significant decision point must be instrumented. You cannot optimize what you cannot measure. This includes:
- Instruction selection (which prompt version ran?)
- Tool invocation (which tool was called and with what args?)
- Policy decisions (why was this request rejected?)
- Evaluation signals (what made this run succeed or fail?)

### 2. Composition Over Monolith
The seven layers are independent. You should be able to:
- Swap models without rearchitecting instruction or tools
- Add new tools without retraining
- Change evaluation metrics without touching the agent loop
- Route requests to different harness configurations (cost vs. latency)

### 3. Fail-Safe Defaults
In ambiguous cases, the agent should:
- Refuse the action
- Escalate to a human
- Degrade gracefully
- Log the decision for audit

It should never silently succeed in an unsafe state.

### 4. Irreversibility Matters
Some actions are reversible (read queries, logging); others are not (delete, refund, message send). Design the harness differently for each:
- **Reversible:** Can retry, can batch, can optimize
- **Irreversible:** Require approval gates, explicit confirmation, audit logging, rollback capability

### 5. Adversarial Inputs Are Normal
Assume:
- Users will try to prompt-inject
- External data may be poisoned
- The model's output may be untrustworthy
- Attackers will find creative ways to misuse the agent

Design the harness to survive these; don't just ask the model to "be careful."

---

## The Three Skills Interviewers Test

Real harness engineering interviews assess:

1. **Design Judgment:** Can you choose reasonable trade-offs? Do you understand the cost/latency/reliability/safety pentagon? Can you defend a choice?
2. **Operational Instinct:** What happens when this runs at 10k QPS? What breaks first? How do you debug "eval says 85%, prod shows 60%"?
3. **Failure Fluency:** Can you name failure modes before they happen? Can you design recovery? Do you understand irreversibility?

Surface knowledge (knowing what MCP is, what gVisor does) predicts nothing. These three skills predict everything.

---

## Study Guide by Role

**AI Engineers** building agentic products: Master all sections. You own the full stack.

**Platform/Infrastructure Engineers** integrating AI into existing systems: Focus on [[sections/tool-calling-and-mcp\|Tool Calling & MCP]], [[sections/sandboxing-and-execution\|Sandboxing & Execution]], [[sections/observability-and-instrumentation\|Observability]], and [[sections/multi-agent-orchestration\|Multi-Agent Orchestration]].

**SDETs & Evaluation Specialists:** Deep-dive on [[sections/evaluation-and-testing\|Evaluation & Testing]], [[sections/failure-modes-and-reliability\|Failure Modes]], and instrumentation.

**Security & Safety Engineers:** Prioritize [[sections/policy-and-guardrails\|Policy & Guardrails]], [[sections/sandboxing-and-execution\|Sandboxing]], and [[sections/failure-modes-and-reliability\|Failure Modes]].

**DevOps/MLOps Engineers** running agents at scale: Focus on [[sections/observability-and-instrumentation\|Observability]], [[sections/multi-agent-orchestration\|Multi-Agent Orchestration]], and cost optimization patterns.

**Interview Candidates:** Read all sections. Practice system design prompts. Internalize failure modes. Be able to articulate the one-sentence definition without referencing a tool.

---

## Recommended Reading Order

1. Start with [[sections/seven-layer-model\|The Seven-Layer Model]] to understand the architecture
2. Read [[sections/instruction-engineering\|Instruction Engineering]] and [[sections/tool-calling-and-mcp\|Tool Calling & MCP]] to understand the control surface
3. Deep-dive [[sections/memory-and-retrieval\|Memory & Retrieval]] and [[sections/sandboxing-and-execution\|Sandboxing]] for grounding and safety
4. Master [[sections/observability-and-instrumentation\|Observability]] (non-negotiable for production)
5. Study [[sections/failure-modes-and-reliability\|Failure Modes]] and [[sections/policy-and-guardrails\|Policy & Guardrails]] for resilience
6. Finish with [[sections/evaluation-and-testing\|Evaluation]] and [[sections/multi-agent-orchestration\|Multi-Agent Orchestration]] for scale

On a second pass (or if short on time), focus on:
- The failure modes section (this is where senior engineers listen)
- The policy and guardrails section (this is where safety lives)
- The observability section (you cannot run production without this)

---

## The Field's Evolution

**2023:** "How do we prompt well?"  
**2024:** "How do we build production agents?"  
**2025-2026:** "How do we operate agents at scale across multiple teams?"

This handbook reflects the 2024-2026 conversation. The shape of the problems (isolation, composition, observability, audit) is stable. The tools (specific LLM providers, frameworks, MCP servers) will change—learn the principles, not the specifics.
