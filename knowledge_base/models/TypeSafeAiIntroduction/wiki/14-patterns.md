> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Patterns

**In one sentence:** TypeSafe is designed to sit inside a larger system powering decisions with AI, and getting the most out of it means thinking in discrete atomic decisions composed in code, using four documented patterns that trade off cost, speed, reliability, and safety.

## Key points

- TypeSafe powers decisions with AI from within a larger system; the key skill is thinking in discrete, atomic decisions that compose into complex system behavior.
- The patterns section assumes knowledge of the TypeSafe primitives and how confidence works, and says to read those first if not.
- Speculative Fan-Out sends many questions in a single call, including speculative ones, and lets code decide what's relevant; benefits are cost and speed.
- Confidence-Gated Routing uses confidence as a second decision axis to build safer systems; benefits are reliability and safety.
- Composite Scoring combines several dimensions of analysis into a single score; benefits are cost, reliability, and speed.
- Intent Routing classifies a user's intent and routes to the appropriate handler; benefits are cost and speed.
- The page invites readers to share killer use cases they think should be mentioned.

---

## The patterns

| Pattern | What it does | Benefits |
|---|---|---|
| Speculative Fan-Out | Send many questions in a single call, including speculative ones, and let your code decide what's relevant | Cost, Speed |
| Confidence-Gated Routing | Utilize confidence as a second decision axis to build safer systems | Reliability, Safety |
| Composite Scoring | Combine several dimensions of analysis into a single score | Cost, Reliability, Speed |
| Intent Routing | Classify a user's intent and route to the appropriate handler | Cost, Speed |

Each pattern has its own detail page: Speculative Fan-Out, Confidence-Gated Routing, Composite Scoring, and Intent Routing (wiki pages 15–18).

**Covers:** https://docs.typesafe.ai/patterns
