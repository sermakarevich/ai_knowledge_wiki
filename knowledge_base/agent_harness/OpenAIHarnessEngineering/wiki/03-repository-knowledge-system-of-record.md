> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Repository Knowledge as the System of Record

**In one sentence:** The team replaced a monolithic AGENTS.md with a short map file (~100 lines) pointing into a structured, CI-validated docs/ directory treated as the single system of record, and optimized the whole repository for agent legibility on the principle that anything Codex cannot reach in-context effectively does not exist.

## Key points

- The "one big AGENTS.md" approach failed in four predictable ways: context is scarce so a giant manual crowds out task and code context; too much guidance becomes non-guidance as agents pattern-match locally; the file rots instantly into stale rules nobody maintains; and a single blob resists mechanical checks for coverage, freshness, ownership, and cross-links.
- The replacement treats AGENTS.md as the table of contents: roughly 100 injected lines that map to deeper sources of truth, with the knowledge base living in a structured docs/ directory.
- The docs/ layout includes design-docs/ (with index, core beliefs, verification status), exec-plans/ (active/, completed/, tech-debt-tracker.md), generated/ (e.g. db-schema.md), product-specs/, references/ (*-llms.txt adapter files), and top-level DESIGN.md, ARCHITECTURE.md, FRONTEND.md, PLANS.md, PRODUCT_SENSE.md, QUALITY_SCORE.md, RELIABILITY.md, SECURITY.md.
- Plans are first-class versioned artifacts: lightweight ephemeral plans for small changes, full execution plans with progress and decision logs for complex work, all checked in and co-located so agents never depend on external context.
- The structure is enforced mechanically: dedicated linters and CI jobs validate that the knowledge base is current, cross-linked, and correctly structured, and a recurring doc-gardening agent scans for stale docs and opens fix-up pull requests.
- Agent legibility is the explicit optimization target: repository-local versioned artifacts (code, markdown, schemas, executable plans) are all Codex can see, so Slack threads, Google Docs, and tacit knowledge must be encoded into the repo or they are invisible, exactly as they would be to a new hire three months later.
- Dependency choices follow the same rule: boring, composable, API-stable technologies are preferred because agents can model them, and the team sometimes reimplemented small subsets (e.g. their own OTel-integrated map-with-concurrency helper with 100% test coverage instead of a generic p-limit-style package) rather than depend on opaque upstream behavior.

---

## Why the big manual failed

Context management is named as one of the biggest challenges in the whole experiment. The team tried stuffing everything into AGENTS.md and documents four failure modes worth quoting in full because they generalize: (1) context scarcity, the manual crowds out the task, the code, and the relevant docs, so the agent misses key constraints or optimizes the wrong ones; (2) saturation, when everything is important nothing is, and agents navigate by local pattern-matching instead of intent; (3) rot, a monolith becomes a graveyard of stale rules that agents cannot distinguish from live ones and humans stop maintaining; (4) unverifiability, a blob cannot be mechanically checked for coverage, freshness, ownership, or cross-links, so drift is inevitable.

## The map-and-records design

### AGENTS.md as table of contents

The short AGENTS.md (about 100 lines, injected into context) serves primarily as a map with pointers to deeper sources. Agents start from a small stable entry point and are taught where to look next rather than being flooded up front. This is progressive disclosure applied to repository knowledge.

### The docs/ tree

The in-repository knowledge store is catalogued and indexed. Design documentation carries verification status plus a set of core beliefs defining agent-first operating principles. Architecture documentation maps domains and package layering. A quality document grades each product domain and architectural layer and tracks gaps over time. Product specs, reference adapters for external systems (*-llms.txt), and domain guides (frontend, reliability, security, product sense) each live at fixed, discoverable paths.

### Plans as artifacts

Ephemeral lightweight plans cover small changes; complex work gets execution plans with progress tracking and decision logs checked into the repository. Active plans, completed plans, and known technical debt are versioned side by side, so an agent picking up work needs no chat history or meeting notes.

## Mechanical enforcement

Linters and CI jobs validate the knowledge base itself: freshness, cross-links, structure. A recurring doc-gardening agent scans for documentation that no longer matches code behavior and opens fix-up PRs. Knowledge hygiene is thus itself an agent-driven loop, not a human chore queue.

## Agent legibility as the design goal

Because the repository is entirely agent-generated, it is optimized first for Codex's legibility. From the agent's point of view, anything unreachable in-context while running effectively does not exist. The team therefore pushed ever more context into the repo over time: a Slack decision on an architectural pattern gets encoded or it stays illegible. The onboarding analogy is explicit: treat the agent like a new teammate and write down product principles, engineering norms, and team culture.

That framing drove dependency decisions. Boring technologies win because of composability, API stability, and representation in the training set. Where an upstream library was opaque, reimplementation was sometimes cheaper: the cited example replaces a generic p-limit-style package with an in-house map-with-concurrency helper tightly integrated with OpenTelemetry instrumentation, carrying 100% test coverage and exactly the runtime's expected behavior. Pulling more of the system into inspectable, validatable, modifiable form increases leverage for Codex and for other agents (e.g. Aardvark) working in the same codebase.

**Covers:** article sections "We made repository knowledge the system of record" (four failure modes, docs/ layout, plans, linters, doc-gardening) and "Agent legibility is the goal" (in-context existence rule, onboarding framing, boring dependencies, map-with-concurrency example).
