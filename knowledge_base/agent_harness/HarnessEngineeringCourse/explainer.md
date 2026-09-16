> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# HarnessEngineeringCourse — In Plain Language

## What is this about?

Think of a careful assistant working at a desk. You give it a task, and instead of just talking, it can also pick up tools: read a file, run a command, check the result, and then decide what to do next. That loop — think a little, act a little, look at what happened, repeat — is what this course is about.

In plain terms, the course builds a small working example of that loop. A central piece (called the Agent) holds a conversation with a language model, lets the model request tool actions, runs those actions itself, and feeds the results back. Around that loop it adds the supporting pieces: instructions that tell the model how to behave, file context pulled in on demand, memory that survives restarts, safe places to run code, and a visible record of everything that happened.

The overall claim is simple: the model only ever asks, while the surrounding program (sometimes called the harness) does. The harness decides what the model may touch, runs each step, checks the outcome, and keeps going until the task is done or needs a human decision.

## Why does it matter?

A language model on its own can only produce text. Connected to tools, it can read project files, run tests, and change code — which is far more useful but also riskier. Without structure, that setup is fragile: the model may see too much text, forget earlier work, run something dangerous, or leave no trace of what it did.

This course matters because it shows each safeguard as a separate, understandable piece. Confined file access keeps edits inside one folder. Memory plus summarising (compaction) keeps long work inside the model's limited view. Sandboxed execution plus a human approval step keeps runs safer. A visible trace plus a terminal display (TUI) makes every step checkable. And two separate quality gates keep "the code passes tests" distinct from "it actually works with a real model".

## How does it work?

1. **Start the loop.** The Agent combines the base instructions, the project rules file, and a short menu of available skills into one set of directions for the model.
2. **Bring context on demand.** When you mention a file with a marker, the harness reads that file and pastes its content into the conversation in a clearly labelled block.
3. **Let the model ask, then execute.** The model replies with either text or tool requests. The harness runs each requested tool — reading files, editing within the confined folder, or running shell commands — and returns the results.
4. **Route every model call through one door.** All model requests pass through a single function, which either talks to a compatible model server or uses a built-in fake responder for offline testing. Costs are estimated by matching parts of the model name to a price list.
5. **Remember across runs.** Messages and trace events are saved as line-by-line JSON files, written safely so an interruption does not corrupt them. A simple keyword search can find relevant past messages.
6. **Keep long work fitting.** The middle of a long conversation is condensed into one short summary note while the start and end are kept whole, with cuts placed so tool requests are never separated from their answers. Oversized items are shortened with an explicit marker.
7. **Load extra knowledge lazily.** Extra abilities (skills) are stored as files with a short name and description; only that short entry is shown upfront, and the full instructions are read only when needed.
8. **Plan, approve, and split work.** Bigger tasks are split into a short list of steps, each step runs only after approval, failures can retry, and independent subtasks can fan out to parallel helpers that return just their answers.
9. **Run code safely and check it.** Commands run in an isolated container when available, otherwise in a scoped local process. Candidate code is re-run in a fresh process with a check, and success is signalled by a random code printed only after the check passes.
10. **Show everything.** Each model call, tool call, and check is recorded both as a simple event and as a structured span, viewable in a two-pane terminal display or as plain printed output, and exportable as line-by-line JSON.
11. **Pass two gates.** Every chapter must clear an offline deterministic check (formatting, types, unit tests) and a separate live-model check, with each chapter adding one piece and tagged so any chapter's state can be revisited.

## Where can this be used?

- **Coding helpers that edit real projects:** reading files, making confined edits, and running the project's own test command before claiming success.
- **Offline development and tests:** the fake responder and deterministic checks let most work happen without network access or model cost.
- **Long-running tasks:** saved sessions plus middle-summarising let work survive restarts and stay within the model's text limits.
- **Supervised automation:** planned steps with per-step approval, plus parallel helpers for independent subtasks, fit tasks that need a human in the loop.
- **Debugging and demos:** the visible event trace, replayable records, and per-chapter demos make it easy to see what the agent did and show each capability working.

## Conclusions & takeaways

- The core pattern is a loop: the model reasons and requests, the harness acts and verifies. Keeping those roles separate is what makes the system understandable and testable.
- Each supporting piece solves one concrete problem: context delivery for file awareness, memory plus summarising for long runs, sandbox plus approval for safety, tracing plus display for visibility, fake plus pricing for cheap offline work.
- The honest limits, as stated in the digest: keyword-only recall has no semantic search; the local execution fallback is teaching-grade rather than a real security boundary; size estimates are rough; skill loading and step planning can fail back to simple defaults; and passing offline tests alone does not prove the agent works — only the live-model check does that.

## Jargon decoder

| Term | What it means here |
|------|--------------------|
| Agent loop | The repeating cycle: ask the model, run its requested tools, feed results back, repeat |
| Harness | The surrounding program that runs tools, enforces limits, and checks results |
| Context window | How much text the model can see at once; the reason for summarising and clamps |
| `@path` injection | Typing a file marker so the harness pastes that file's content into the conversation |
| JSON-L | A save format with one JSON object per line, easy to append and resume |
| Compaction | Condensing the middle of a long conversation into one short summary note |
| Skill | An extra ability stored as a file; only its name and description are shown until needed |
| Sandbox | An isolated place to run commands, ideally a container with no network |
| Approval gate | A pause where a human must allow the next step before it runs |
| Trace / span | Two views of the same record: a simple event list and a structured nested timing tree |
| TUI | A terminal display with two panes: conversation plus live record of steps |
| Verify vs accept | Two checks: offline deterministic tests versus a live run against a real model |
