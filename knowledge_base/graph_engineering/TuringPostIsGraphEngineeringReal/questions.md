---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: FOD#159: Is Graph Engineering Real?

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What three primitives does the article use to formally describe a graph, and what does each one mean?

> [!tip]- Answer
> Nodes (units of work — an agent call, tool call, router, or human checkpoint), edges (routing/transition decisions — which node runs next and under what condition), and state (the information that flows between nodes, what gets carried forward or discarded). See [[wiki/01-core-argument-and-definitions|Core Argument and Definitions]].

### Q2. How long did it take "graph engineering" to displace "loop engineering" as the trending buzzword, and why does the article treat this speed as significant?

> [!tip]- Answer
> About six weeks. The article treats the speed as a signal that the term is riding hype rather than a slowly validated engineering consensus, which motivates its fact-check of the claims attached to the new buzzword. See [[wiki/01-core-argument-and-definitions|Core Argument and Definitions]].

### Q3. Name the four types of "graph" the article distinguishes, with one example of each.

> [!tip]- Answer
> Control graph (workflow routing — LangGraph, Google's ADK), knowledge graph (entity-relationship retrieval — GraphRAG), execution trace (post-hoc debugging record — agent execution logs), and improvement graph (self-checking/self-optimizing loop — an optimizer paired with audit/verification steps). See [[wiki/02-four-graph-types-and-fact-check|Four Graph Types and Fact-Check]].

### Q4. Why does the article conclude the "Microsoft, Stanford, and Anthropic adopted graph engineering" claim is false?

> [!tip]- Answer
> Because each institution's cited evidence doesn't actually support the claim: GraphRAG (Microsoft) is a retrieval-augmented-generation/knowledge-graph technique, not a general graph-engineering methodology; DSPy (Stanford) optimizes language-model programs/prompts, a different problem from designing agent topologies; and Anthropic never announced any such named discipline at all. See [[wiki/02-four-graph-types-and-fact-check|Four Graph Types and Fact-Check]].

### Q5. The 18%/85% performance figures circulated as evidence that graphs are universally better. What is the actual source of those numbers, and why does that matter?

> [!tip]- Answer
> They trace back to a single industrial-diagram-processing case study, which was never shown to generalize to arbitrary agent workloads. It matters because presenting a narrow case study's numbers as a universal "switch to graphs and get this result" claim overstates what the evidence actually supports. See [[wiki/02-four-graph-types-and-fact-check|Four Graph Types and Fact-Check]].

### Q6. Why does the article insist that a genuinely linear workflow should be kept linear rather than converted to a graph?

> [!tip]- Answer
> Because graphs bring real, non-trivial costs — state management across branches, routing/transition logic, and harder debugging of a branching (rather than single-trace) execution path — that are only worth paying when the task genuinely needs parallel branches, independent verification, or different tools per step; absent those needs, the extra complexity is premature and unearned. See [[wiki/03-practical-guidance-and-industry-shift|Practical Guidance and the Industry Shift]].

### Q7. A team is building an agent that classifies a support ticket, looks up one knowledge-base article, and drafts a reply — always in that fixed order, with no need for a second opinion. Should they reach for a graph? Why or why not?

> [!tip]- Answer
> No — this is a genuinely linear task with no parallel branches, no need for independent verification, and no per-step tool variation, so per the article's decision rule a simple loop is the right architecture; adding graph topology here would only add state-management and debugging overhead without a matching benefit. See [[wiki/03-practical-guidance-and-industry-shift|Practical Guidance and the Industry Shift]].

### Q8. The article frames the "graph vs. loop" naming debate as a proxy fight over something bigger. What is that bigger shift, and what does it mean for where engineering effort should go?

> [!tip]- Answer
> The shift is from prompt-centric development (getting a single model call right) to system-centric development (treating reliability as a property of the surrounding architecture — how work is routed, how state is preserved or discarded, how outputs are checked, how failures are handled). It means engineering effort should increasingly go into the system's structure and checks, not just into refining individual prompts. See [[wiki/03-practical-guidance-and-industry-shift|Practical Guidance and the Industry Shift]] and [[critical_thinking|Critical Analysis]].
