# AI Demands More Engineering Discipline. Not Less

**Article:** [AI Demands More Engineering Discipline. Not Less (Charity Majors, 2026)](https://charitydotwtf.substack.com/p/ai-demands-more-engineering-discipline)

## Human Readable TL;DR

Imagine your team used to build custom furniture by hand -- every piece took weeks and was treated like a treasure. Now you have a machine that can produce furniture in minutes. You wouldn't throw away all the rules about what makes good furniture; you'd actually need *more* precise blueprints and quality checks, because bad designs now get built at scale instantly. That's what's happening with AI and software: code just got cheap and fast to produce, so the bottleneck shifted from writing code to knowing what to build -- and whether it actually works.

## TL;DR

Charity Majors argues that the 2025 milestone -- where AI-generated code reached median-engineer quality -- inverted code economics from scarce to abundant. This shifts the bottleneck from production to evaluation: teams must now encode knowledge in specifications, architecture, and behavioral tests rather than implicit code. Rather than eliminating engineering discipline, nondeterministic AI systems demand more of it.

---

## Problem & Motivation

A previous Majors piece on AI was misread as advocating for scrapping code review and testing. This article is a technical rebuttal. The deeper problem it addresses: the software industry has not updated its engineering practices to reflect a world where code generation is cheap and fast. Teams still treat code as the primary repository of knowledge and the primary artifact under review -- practices that made sense when writing code was the bottleneck, but are now misaligned.

---

## Main Original Ideas

1. **Code as Cache, Not Asset** -- Borrowing Chad Fowler's framing, Majors argues code is "a materialized view of understanding that is useful while current, disposable when stale." Once code regeneration is easy and cheap, code stops being a durable asset and behaves like a cache: valuable when current, discardable when stale.

2. **The Evaluation Problem, Not the Code Problem** -- Engineers cannot delete code not because the code is irreplaceable, but because (a) they don't know what behavior is required and (b) they lack mechanisms to verify correctness of a replacement. These are evaluation infrastructure gaps, not code quality gaps.

3. **Discipline Intensifies Under Nondeterminism** -- The common assumption is that AI doing the coding means less rigor is needed. Majors inverts this: nondeterministic systems require *stronger* engineering practices -- specifications, behavioral tests, observability, characterization tests, capture/replay -- because you cannot assume outputs are stable.

4. **Review Architecture, Not Code** -- Code itself was never the ideal review artifact. Majors proposes reviewing architecture artifacts, specifications, and design decisions. Code can then be regenerated from architectural changes rather than inferred from code.

5. **Operations/QA Tooling as the Template** -- Behavioral tests, characterization tests, capture/replay, and production observability -- historically undervalued by software engineering and native to operations and QA -- are the exact evaluation tools the new paradigm requires.

6. **Historical Parallel: Infrastructure Revolution** -- The shift from handcrafted servers to immutable/Phoenix infrastructure (Chad Fowler, 2013) is the model. "Mutability is the sworn enemy of understanding." Code is about to undergo the same transition from precious hand-crafted artifact to replaceable, regenerable unit.

---

## Key Findings

- By November 2025 (Opus 4.5 release), AI-generated code reached approximately median software engineer quality -- the threshold Majors treats as the practical turning point.
- Teams with short, fast feedback loops and strong engineering discipline remain rare (estimated 5--10% of organizations), meaning most teams have not yet invested in the practices that will compound under AI assistance.
- The returns on encoding organizational knowledge into specifications and tests are described as "massive and nonlinear" -- the investment cost is front-loaded but the compounding is discontinuous.
- Determinism remains a hard requirement from users: consistent interfaces, reliable financial transactions. "Determinism is not going anywhere" -- AI tooling does not change this expectation.

---

## Suggestions & Future Directions

1. Invest now in encoding organizational knowledge into specifications, tests, and architecture artifacts -- not leaving it implicit in code or developer minds.
2. Treat 2026 as a "return to discipline": tighten feedback loops, build out observability, and systematize behavioral testing.
3. Redirect code review effort toward architecture artifacts and design decisions, with code treated as a downstream regenerable artifact.
4. Draw on operations and QA tooling (characterization tests, capture/replay, production observability) as the template for AI-era evaluation practices.
5. Resist the CEO-level impulse to use AI as a cost-cutting shortcut; use it instead to accelerate adoption of rigorous engineering practices that have historically been too labor-intensive to sustain.

---

## Authors & Institutions

Charity Majors -- Substack (charitydotwtf.substack.com); formerly CTO of Honeycomb.io. References: Chad Fowler (Phoenix Architectures / immutable infrastructure, 2013).
