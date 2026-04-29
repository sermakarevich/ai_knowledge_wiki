> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## Observability & Instrumentation

Observability is non-negotiable for production agents. You cannot optimize what you cannot measure, and you cannot debug what you have not logged. This section covers instrumentation patterns, tracing, cost tracking, and audit logging.

### Core Instrumentation Points

**Every agent system must instrument:**

1. **Instruction selection:** Which prompt version ran? Why this version over others?
2. **Model invocation:** How many tokens? Which model? How long did generation take?
3. **Tool calls:** What tool was called with what args? What was the result?
4. **Policy decisions:** Was this request approved, rejected, or escalated? Why?
5. **Evaluation signals:** What made this run succeed or fail? Did it meet acceptance criteria?

### The Three Levels of Visibility

| Level | What | When |
|-------|------|------|
| **Metrics** | Aggregates (success rate, latency, cost per user) | Always; sampled |
| **Logs** | Individual events (one request) | Always; full details |
| **Traces** | Request flow across services | Sampled; 10-100% |

### Key Questions for Interviews

- "Your eval says 85% success but production shows 60%. Debug it."
- "Design observability for an agent that approves refunds. What must you log?"
- "How do you detect data poisoning in a RAG system?"

### Future Sections (To be expanded)

- Tracing with OpenTelemetry
- Cost tracking and optimization
- Anomaly detection baselines
- Audit log immutability
- Prompt/completion capture for debugging
