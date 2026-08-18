> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Prompt and Loop Layers

**In one sentence:** Prompt, loop, and graph engineering are not competing techniques but three nested levels of control, and the loop layer — which automates the agent's observe-act-verify cycle — fails not because of its machinery but because of the stop condition that separates "genuinely finished" from "stuck."

## Key points

- "Prompt engineering," "loop engineering," and "graph engineering" are three nested levels of control that stack: a prompt shapes one model call, a loop shapes one agent's repeated cycle built around that call, and a graph wires several such loops/agents together.
- Adding a layer does not retire the lower one: building a loop around a prompt leaves the prompt operating inside each cycle — it only changes who (or what) writes it on each pass.
- A supervised prompt-response cycle works while a human reads and judges every output; it breaks down once volume rises, tasks span multiple steps, no grader is available, or one step's output must feed the next without review — the prompt did not get worse, the deployment conditions outgrew manual review.
- Even inside multi-agent systems, sloppy prompting (not the agent topology) is often the root cause of coordination failures; the article cites Anthropic material on a bug where one simple query needlessly spawned 50 subagents, fixed by better prompting rather than architectural redesign.
- A production loop is built from: scheduled or event-triggered unsupervised automations, isolated worktrees so parallel agents don't collide on the same files, reusable written-down skills/conventions, connector-based access to external tools and data (issue trackers, databases, staging APIs), a separate checker pass so the producing model is not the sole grader (models grade their own work too generously), and externally persisted state (a markdown file or board) because the model retains no memory across runs.
- The loop layer's central thesis is that the repeat-and-check mechanism is easy to build, while the stop condition — a reliable, mechanical test distinguishing "genuinely finished" from "stuck" — is hard and where loops actually fail; without it, an unattended run fails silently by consuming tokens until an arbitrary budget cap ends it, rather than stopping because the work is correct or complete.

---

## Three nested levels of control

The article's core frame is that "prompt engineering," "loop engineering," and "graph engineering" are usually treated as rival techniques when they are in fact nested units of control:

- **Prompt layer** — shapes a single model call.
- **Loop layer** — shapes one agent's repeated cycle built around that call.
- **Graph layer** — shapes how several such loops/agents are wired together.

The nesting is not eliminative: lower layers keep operating inside higher ones. Building a loop around a prompt does not retire the prompt; it merely changes who (or what) writes it on each cycle.

## Why layers get added

A single supervised prompt-response cycle is sufficient as long as a human reads and judges every output. It stops being sufficient under any of these conditions:

- volume rises,
- tasks span multiple steps,
- no one is available to grade results,
- one step's output must feed straight into the next step without review.

The article's framing is that the prompt itself did not get worse — the deployment conditions moved past what manual review can keep up with. As evidence that lower-level discipline still dominates, it cites Anthropic material noting that even inside multi-agent systems, sloppy prompting (not the agent topology) was often the actual root cause of coordination failures; a bug that caused one simple query to needlessly spawn 50 subagents was fixed by better prompting, not by redesigning the architecture.

## The loop layer

A loop automates the **observe-act-verify-repeat** cycle so a coding/task agent can run without a human approving every single step. The building blocks commonly cited for a production loop:

- **Automations** — scheduled or event-triggered runs that operate unsupervised.
- **Worktrees** — isolated working copies so parallel agents cannot collide by editing the same files.
- **Skills** — reusable written-down conventions instead of re-explaining them every session.
- **Connectors** — access to external tools and data (issue trackers, databases, staging APIs).
- **Checker sub-agent** — a separate grading pass, because the same model that produced an answer is not the only one grading it: a model grades its own work too generously.
- **External state** — externally persisted state (a markdown file or board) since the model itself retains no memory across separate runs.

### The stop-condition thesis

The article's central thesis about the loop layer: the repeat-and-check mechanism itself is easy to build. What is hard — and where loops actually fail — is the **stop condition**: a reliable, mechanical test that can tell "genuinely finished" apart from "stuck." Without such a test, an unattended run does not fail loudly; it just keeps consuming tokens until an arbitrary budget cap ends it, rather than stopping because the work is actually correct or complete.

**Covers:** Gist of the three-layer stack; the prompt layer; the loop layer and its building blocks and stop-condition thesis (source chunk 01)
