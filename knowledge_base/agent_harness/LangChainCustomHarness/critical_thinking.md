> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: How to Build a Custom Agent Harness

## Claims vs. evidence

(1) "An agent is only as good as the context it's given, so context delivery is the main lever of agent quality" — **asserted, not measured**. This is the article's foundational premise, stated as a design philosophy rather than backed by a benchmark or ablation. It's a plausible, widely-echoed claim in the agent-engineering community, but the post itself offers no data comparing a minimal-context agent against a well-fitted one.

(2) "`create_agent` matches production needs better than opinionated pre-assembled harnesses (Deep Agents, Claude Agent SDK)" — **vendor framing, unverified**. This is a first-party blog post from LangChain promoting its own `create_agent` API by contrasting it favorably with named competitor/sibling products. No benchmark, cost comparison, or user study is given; the comparison is architectural (minimal core vs. fixed stack) rather than empirical.

(3) "Middleware composes freely and is reusable across every agent in an organization" — **plausible but unsupported by evidence in-article**. This is a standard software-engineering argument for modularity (small units, single concern, composability), true in principle for well-designed plugin systems, but the post gives no example of actual reuse across LangChain's cited agents (GTM, async coding, no-code builder) — it asserts they share a base and differ in stack, without showing overlap or reuse metrics.

(4) "LangChain's own agents are built this way and it's the easiest path to a custom harness" — **anecdotal, self-referential**. The evidence is LangChain citing its own internal products as proof of its own framework's value — this is not independent validation.

## Genuinely new vs. repackaged

The `agent = model + harness` framing and the idea that harness quality (not model choice) drives outcomes are not new — this exact framing appears near-verbatim in other harness-engineering writeups already in this knowledge base (Osmani, amux.io). What's specific to this piece is `create_agent`'s particular minimalism claim and its four-lever middleware taxonomy (deterministic logic, tool lifecycle, custom state, stream handlers) — a concrete API-level contribution, not a conceptual one.

## Weaknesses and blind spots

- No benchmarks, cost figures, or failure-rate data anywhere in the post — every claim is qualitative and architectural, which is reasonable for a product-announcement blog post but means none of its comparative claims (vs. Deep Agents, vs. Claude Agent SDK) can be checked against evidence.
- The four customization levers and the eight-ish capability groups are presented as a clean taxonomy, but there's no discussion of what happens when middleware pieces conflict (e.g. two pieces both wanting to mutate custom state, or a retry middleware interacting badly with a call-limit middleware) — composability is asserted, not stress-tested.
- "Start minimal, add only what you need" offers no guidance on how a team would actually discover what they need before hitting a failure in production — the fit process itself is undertheorized.
- It's marketing content for a specific commercial product; the framing (minimal core = good, pre-assembled = less flexible) is the framing that favors LangChain's own API design choice.

## Applicability

Works: as an orientation piece for teams already committed to LangChain's ecosystem, explaining the mental model (`create_agent` + middleware) and giving a checklist of capability categories (context management, memory, action/delegation, reliability, policy, cost) to consider when scoping a new agent.
Fails or untested: any claim about which approach (minimal-core-plus-middleware vs. pre-assembled harness) actually performs better in practice — that comparison is architectural narrative, not measured. Teams evaluating harness frameworks should treat the competitive claims here as marketing, not benchmark evidence.
**Relevance to my work** — the capability checklist (context overflow, memory, action/delegation, reliability, policy/steering, cost) is a useful audit list when scoping any custom agent harness, independent of whether LangChain's specific API is used; the four-lever middleware taxonomy is a reasonable design vocabulary for describing customization points in any agent loop, not just `create_agent`'s.

## What this changes

Nothing empirically — no new results are reported. What it offers is a vocabulary (four levers, task-harness fit) and a capability checklist that's useful for structuring how to think about and communicate harness design decisions, regardless of which framework implements them.
