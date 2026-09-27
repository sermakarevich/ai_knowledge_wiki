> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[Orkes/summary|Orkes -- Operating System for AI Agents and Workflows]] — Same vendor and platform (Orkes Conductor built on Conductor OSS); the Orkes entry is the marketing homepage (scale, SLA, positioning) while this entry distills the technical docs (engine semantics, operators, agent primitives).
- [[ApacheBurr/summary|Apache Burr: Build Reliable AI Agents and Applications]] — Same-problem-different-method: both tackle durable, observable agents with state persistence and human-in-the-loop; Burr does it as a lightweight Python action/state-machine library, Conductor as a centralized server with polyglot workers and enterprise governance.
- [[CompilingAgenticWorkflowsIntoLLMWeights/summary|Compiling Agentic Workflows into LLM Weights]] — Contradicts: the paper argues persistent procedures belong compiled into model weights to eliminate the runtime orchestration layer, while Conductor argues procedures belong in an external durable workflow engine with per-step persistence and retry.
- [[OrchestratingAICodeReviewAtScale/summary|Orchestrating AI Code Review at Scale]] — Applies-in-practice: Cloudflare's coordinator-led multi-agent review with tiered models, circuit-breakers, and human override is a production instance of the patterns Conductor provides natively (fan-out via FORK_JOIN, HUMAN approval gates, failure workflows, bounded retries).
- [[AgentEvalsTCO/summary|Total Cost of Ownership for Evaluating Agents]] — Shares-technique: Conductor evaluates agents by asserting on the durable execution trace (tools, handoffs, guardrail events) rather than final text alone, and this entry addresses the cost/coverage problem of running such evaluations at scale (full-trace scoring vs. sampled LLM-as-judge).
