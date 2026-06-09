# Software Engineering Fundamentals for AI Coding

**Source:** [AI Coding Workshop -- Software Engineering Fundamentals for Working with LLMs (Matt Pocock, 2025)](https://www.youtube.com/watch?v=-QFHIoCo-Ko)

## Human Readable TL;DR

Think of building software with AI like planning a renovation project. Before your contractor (the AI) starts demolishing walls, you need to agree on a blueprint -- otherwise they'll tear down load-bearing things or build you a room you didn't want. Matt shows a step-by-step process: first have a deep conversation with the AI to reach a shared vision, then write that vision down, then break the work into small testable chunks the AI can tackle without losing track, and finally let the AI work through those chunks mostly unsupervised while you check the results. The big insight is that old-fashioned software wisdom -- keep things small, test as you go, design clean building blocks -- turns out to be exactly what makes AI assistants perform well too.

## TL;DR

Matt Pocock argues that LLM coding agents have two fundamental constraints: a "smart zone" (roughly the first ~100K tokens of context) where attention quality is high, and a "dumb zone" where performance degrades as context grows; plus a "Memento problem" where clearing context resets all memory. His workflow counters these by using structured alignment sessions ("grill me"), PRD generation, and vertical-slice Kanban issue decomposition to pre-queue well-scoped tasks for AFK (away-from-keyboard) agent loops. TDD with red-green-refactor is essential because feedback loops are the ceiling for agent code quality. Deep modules (large interfaces, small API surface) make codebases more testable and therefore more AI-friendly.

---

## Problem & Motivation

Developers using LLMs for coding consistently hit two walls: (1) output quality degrades as context grows, and (2) clearing context loses all accumulated alignment. The dominant response -- ever-larger context windows and "compact" summaries -- doesn't fix either problem and often makes them worse. Matt's thesis: the same software engineering fundamentals that make human teams effective (planning, modular design, feedback loops, TDD) directly solve the AI collaboration problem, and most developers are skipping them.

---

## Main Original Ideas

1. **Smart Zone / Dumb Zone** -- LLM attention scales quadratically with token count. Past roughly 100K tokens in a single session, quality degrades meaningfully regardless of the model's advertised context length. Sizing each task to fit comfortably within the smart zone is the primary lever on output quality.

2. **The Memento Principle -- Embrace Statelessness** -- Rather than fighting forgetfulness via compacting (which introduces "sediment"), design workflows around clearing and restarting from a predictable base state. Every clear drops back to a known system prompt; that predictability is a feature. Keep CLAUDE.md minimal so work starts in the smart zone.

3. **The Grill Me Skill -- Alignment Before Artifacts** -- Before writing any spec, run a structured interviewing session where the AI asks questions one at a time (with recommended answers) until both parties share the same mental model of the feature. Inspired by Frederick P. Brooks' "design concept" -- the shared internal picture that all participants must hold. The conversation history is the valuable asset, not the output document.

4. **Human-in-the-Loop vs. AFK Tasks** -- Planning and alignment always require a human present. Implementation can run unattended ("AFK"). Explicitly tagging tasks with this distinction determines when you engage vs. step away.

5. **Vertical Slices Over Horizontal Layers** -- AI naturally codes horizontally (schema first, then API, then UI), which delays feedback until the last phase. The correct structure is vertical slices / tracer bullets -- each task cuts through all layers to produce something testable end-to-end immediately.

6. **Deep Modules (Ousterhout's Principle)** -- A deep module has a small, simple interface but rich internal functionality. Unguided AI produces shallow module codebases (many tiny files, many exports) that are hard to test and hard to reason about. Explicitly designing deep modules with clean interfaces lets developers retain architectural ownership while delegating implementation details.

7. **Push vs. Pull for Coding Standards** -- Implementer agents should pull standards on demand; reviewer agents should have standards pushed into their context so they can compare written code against norms without a separate retrieval step.

---

## Key Findings

| Practice | Mechanism | Outcome |
|---|---|---|
| Grill Me before PRD | AI interviews human, resolves decision tree | Shared design concept, 40-100 alignment questions surfaced |
| Token counter always visible | Status line shows live token count | Know when you're approaching dumb zone |
| Vertical-slice issues | Each issue touches all layers | Testable after every issue, not after phase 3 |
| TDD red-green-refactor | Failing test first, then implement | Prevents AI cheating tests; feedback loop is the ceiling |
| PRD out-of-scope section | Explicit definition of done | Prevents feature creep during AFK loops |
| Ralph loop (`ralph-once.sh`) | Cat all issues + last 5 commits → inject into `claude --permission-mode accept-edits` | AFK implementation loop |
| Automated reviewer agent | Clear context, push standards, review commits | Catches issues without contaminating implementer context |
| Sandcastle parallelization | DAG-scheduled worktrees in Docker, planner → implementers → reviewer → merger | Multi-agent parallel implementation |

**Specific tools / workflows mentioned:**
- `claude --permission-mode accept-edits` with `--print` for non-interactive loops
- Claude Code skills: `/grill-me`, `/write-prd`, `/prd-to-issues`, `/ralph-once`, `/improve-code-base-architecture`
- Sandcastle TypeScript library (Matt's own) for multi-agent DAG orchestration
- Gemini Meetings → transcript → grill me session as external input pipeline
- Playwright MCP for browser automation (noted as immature for production front-end)

---

## Suggestions & Future Directions

1. Smart zone will expand as models improve -- the core architecture remains valid but the practical token budget grows.
2. Front-end AI tooling is not yet reliable for production; current best practice is generating multiple throwaway prototype routes and making aesthetic decisions as a human.
3. Code review volume increases with delegation -- there is no clean solution yet; teams should prepare for higher review load.
4. Teams should involve domain experts and multiple developers in the grill me / PRD phase, not just solo developers.
5. QA should feed new issues back into the Kanban board continuously rather than as a final phase gate.
6. Parallelization with Sandcastle-style DAG loops is the next step after mastering sequential Ralph loops.

---

## Authors & Institutions

**Matt Pocock** -- independent educator, founder of AI Hero (aihero.dev), creator of the Cadence course video management platform. Previously known for TypeScript education content.
