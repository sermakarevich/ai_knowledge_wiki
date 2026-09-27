# A Technical Taxonomy of LLM Agent Communication Protocols

**Paper:** [A Technical Taxonomy of LLM Agent Communication Protocols (Sander, Gidey, Lenz, Knoll, 2026)](https://arxiv.org/abs/2606.19135)

## Human Readable TL;DR

Imagine you have a team of AI assistants that need to talk to each other and to different software tools. Right now, each team uses a different "language" to communicate -- some are better for quick tool lookups, others for long back-and-forth conversations. This paper creates a map (taxonomy) that sorts all these communication languages into five key questions: Who are you talking to? What data do you send? Does the conversation have memory? How do you find other agents? And how rigid are the rules? Using this map, the researchers found that most AI agent "languages" are still centralized and lack privacy safeguards -- and that no single standard will win; instead, a layered system like the internet's own protocol stack will likely emerge.

## TL;DR

The paper proposes a five-dimension taxonomy -- counterparty, payload, interaction state, discovery mechanism, and schema flexibility -- to classify nine open-source LLM agent communication protocols (MCP, A2A, LAP, agents.json, Agora, ANP, LMOS, ACP, agntcy). All agent-to-agent protocols converge on session-state with hybrid payloads; decentralized discovery remains rare; and the authors predict a federated, OSI-like layered protocol stack rather than a single dominant standard.

---

## Problem & Motivation

Multi-agent LLM systems are proliferating -- AutoGen, CrewAI, CAMEL, and others -- but the protocols they use to communicate lack systematic classification. Without a shared vocabulary, practitioners cannot compare or select protocols, and researchers cannot identify gaps. Classical agent communication frameworks (FIPA, KQML) predate LLMs and don't capture modern concerns like schema negotiation or tool-use payloads. The paper addresses this gap with a design-science taxonomy built from analyzing nine real open-source protocols.

---

## Main Original Ideas

1. **Five-dimension taxonomy** -- A structured framework that characterizes any LLM agent communication protocol across: (1) *Counterparty* (agent vs. context vs. hybrid), (2) *Payload* (structured/conversation/hybrid), (3) *Interaction State* (stateless vs. session), (4) *Discovery Mechanism* (static/centralized/partially centralized/decentralized/hybrid), and (5) *Schema Flexibility* (single/multiple/evolving).

2. **Communication Trilemma** -- Protocols face a fundamental trade-off between three properties: *versatility* (ability to express rich, open-ended tasks), *efficiency* (low token and compute overhead), and *portability* (interoperability across different agent stacks). Context-focused protocols like MCP maximize efficiency and portability by using rigid schemas; agent-to-agent protocols that achieve versatility pay a token overhead cost.

3. **Federated layered stack prediction** -- Rather than convergence on a single protocol, the authors project emergence of an OSI-style layered architecture: a lightweight discovery layer, a structured context protocol layer (tool execution), and a session-aware schema-evolving layer (multi-turn deliberation).

4. **Empirical protocol classification** -- Systematic mapping of nine concrete protocols onto the taxonomy, producing a reference classification table that reveals structural patterns invisible from individual protocol documentation.

---

## Key Findings

| Protocol | Counterparty | Interaction State | Discovery | Payload | Schema |
|----------|-------------|------------------|-----------|---------|--------|
| MCP (Anthropic) | Context | Stateless | Static | Structured | Multiple |
| A2A (Google) | Agent | Session | Centralized | Hybrid | Multiple |
| LAP (LangChain) | Agent | Session | Static | Hybrid | Single |
| agents.json | Context | Stateless | Static | Structured | Single |
| Agora | Agent | Session | Static | Hybrid | Evolving |
| ANP | Agent | Session | Centralized | Hybrid | Evolving |
| LMOS | Hybrid | Session | Hybrid | Hybrid | Multiple |
| ACP (IBM/BeeAI) | Agent | Session | Centralized | Hybrid | Multiple |
| agntcy | Agent | Session | Centralized | Hybrid | Multiple |

- **Session-state universal for A2A**: All seven agent-to-agent protocols implement session state -- multi-turn interaction requires memory.
- **Hybrid payload dominates A2A**: Every agent-to-agent protocol uses hybrid payloads (text + structured data); pure structured payloads only appear in context protocols.
- **Schema negotiation is rare**: Only Agora and ANP support runtime schema evolution; the other seven rely on static schemas defined before runtime.
- **Decentralized discovery nearly absent**: Only LMOS implements decentralized discovery; most protocols require static endpoint configuration or centralized registries.
- **Critical safety gap**: Privacy safeguards, compliance mechanisms, and policy enforcement are widely absent -- a major concern for safety-critical domains.

---

## Suggestions & Future Directions

1. **Formal verification** -- Apply protocol verification methods to prove correctness properties of agent communication schemas.
2. **Efficiency benchmarking** -- Measure token overhead and latency across protocols to quantify the trilemma trade-offs empirically.
3. **Standardized specifications** -- Develop formal protocol standards to reduce fragmentation, particularly for discovery mechanisms.
4. **Resilience evaluation** -- Test protocol behavior under model errors and hallucinations to understand failure modes.
5. **Security and privacy** -- Investigate security implications of different communication schemes; design protocols with built-in compliance and policy enforcement for healthcare, finance, and other regulated domains.
6. **Taxonomy evolution** -- Update the taxonomy continuously as LLM capabilities and new protocols emerge (the field moves fast).

---

## Authors & Institutions

Linus Sander, Habtom Kahsay Gidey, Alexander Lenz, Alois Knoll -- Technische Universität München, Munich, Germany
