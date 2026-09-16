> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Natural-Language Agent Harnesses — In Plain Language

> Plain-language guide to Natural-Language Agent Harnesses (NLAHs) and the shared runtime that executes them. Written from the digest only.

## What is this about?

Think of a talented cook working in a restaurant kitchen. The cook is the AI model — smart, but it needs recipes, kitchen rules, and someone deciding who chops, who tastes, and when a dish is done. That surrounding system is called the harness: everything outside the model that decides its inputs, tools, notes, checks, retries, and when to stop.

Normally that "kitchen rulebook" is buried inside complicated program code that is hard to read, compare, move to another kitchen, or test piece by piece. This paper proposes writing the rulebook as an ordinary readable document instead — a Natural-Language Agent Harness (NLAH). A shared kitchen manager, called the Intelligent Harness Runtime (IHR), reads that document and runs the show: calling agents, handing work between them, updating notes, running checks, and enforcing hand-in rules.

Even a seemingly solo job is run as a small team: a parent organizer plus one worker child, so the line between "the plan" and "the doing" stays visible.

## Why does it matter?

Three reasons, in plain terms:

- **Hidden rules become visible.** Today harness logic is tangled in controller code. A readable document makes the policy inspectable: you can read what stages exist, who is responsible, what evidence is required, and when to retry or stop.
- **Rules become portable and testable.** Because the policy is a short text document plus a shared runtime, you can move it between setups and switch individual modules on and off to see what actually helps. The digest reports big compression: for example, one coding setup shrank from about 60,000 code tokens across 68 files to a roughly 3,000-token, 3-file document.
- **Performance is preserved.** Across coding, terminal-use, and computer-use benchmarks, the runtime-executed documents scored competitively with native code harnesses, while leaving measurable traces of the intended workflow, contracts, tool use, and recovery behavior.

In short: same kitchen output, but the recipe is now something a human can read, carry elsewhere, and edit with confidence.

## How does it work?

1. **Start with a minimal worker.** The base agent is a simple loop whose only tool is a terminal: it reads and writes files, runs processes, logs events, and can launch child agents as fresh copies of itself using small task packets.
2. **Add a fixed manager instruction.** A fixed runtime policy turns that minimal worker into the IHR — the shared interpreter that knows how to read any NLAH document and turn it into calls, handoffs, state updates, and checks.
3. **Write the readable rulebook.** For each task family you write one NLAH document: the task contract first, then stages, roles, shared state, verification steps, recovery rules, and stopping rules.
4. **Keep exact machinery in code.** Deterministic pieces stay as code: test runners, parsers, sandboxing, benchmark tools, validators, and logging. Natural language carries the policy; code carries the exact mechanisms.
5. **Run as parent plus child.** A parent organizer reads the NLAH, splits the work, and hands task packets to child executors. Children do the work and return evidence; the parent checks it against the contract.
6. **Enforce evidence and gates.** The document demands explicit state and evidence: what was tried, what the tools returned, what the verification signals say, and whether the completion gates pass before stopping.
7. **Recover and stop cleanly.** If a tool fails or a check fails, the policy says what to retry, what to hand off, and when to quit — instead of looping forever or quitting too early.
8. **Follow five writing principles.** State the contract first; separate stages from mechanisms; make state and evidence explicit; draw module boundaries so each piece (verifier, self-evolution, multi-candidate search, context compression, markdown memory) can be removed and tested; and prefer simple enforceable wording over vague advice like "be careful."

There are three styles of control: hard-coded harnesses (rules in program logic), document-plus-runtime (this paper's approach), and a future idea with no external harness at all, where one controller model directly manages the others.

## Where can this be used?

- **Software repair tasks.** Coding benchmarks such as SWE-bench Verified and Live-SWE, where an agent must read code, edit files, run tests, and produce a fix that passes hidden checks.
- **Terminal and system tasks.** Benchmarks such as Terminal-Bench 2.0, where an agent works through a command line: installing, configuring, scripting, and leaving behind a required artifact such as a solve script.
- **Computer-use tasks.** Benchmarks such as OSWorld with setups like SeeAct, where an agent must operate a computer interface step by step toward a task goal.
- **Teams that compare harnesses.** Any group that today maintains several hard-to-compare controller codebases and wants one shared runtime plus short readable policies they can diff, share, and ablate.
- **Module-by-module improvement.** Groups wanting to test one idea at a time — for example, adding file-backed notes, a separate verifier, or an evidence rule — and measure whether scores, workflow preservation, and tool success actually move.

## Conclusions & takeaways

- Readable rulebooks can match code rulebooks on task scores while being far shorter and easier to inspect — but the language model, runtime version, and machine setup still matter, and every number comes from one shared instantiation described in the digest.
- The split of labor is deliberate: words carry roles, contracts, evidence discipline, retry, handoff, validation strategy, and stopping rules; code keeps execution, parsing, sandboxing, adapters, logging, safety, permissions, and evaluation.
- The clearest wins came from discipline about state and acceptance: file-backed state and evidence-backed answering helped, and self-evolution helped on the reported benchmarks, because they shorten the path from intermediate work to checkable evidence.
- Honest limits: passing work between parent and child loses information. Reported handoff recall is low (about 0.32 on one coding setup, 0.55 on a terminal setup) and orchestration reliability trails plain prompting (about 0.83–0.85 versus near 1.00), because work is spread across separate contexts.
- More machinery is not always better: trying many candidate solutions at once multiplied agent calls (about 1.1 to 5.7) while slightly lowering one score, and compressing context hurt results (notably about −8 points on one computer-use setup). A separate verifier helped mostly near the final acceptance gate.
- A cautionary tale from the appendices: a code harness tuned for one model family ported poorly to another (only 32 of 89 terminal tasks solved, many stuck in timeout loops even after earning a passing verifier signal), which is exactly the kind of brittle, hard-to-move logic the document approach tries to avoid.

## Jargon decoder

| Term | What it means in plain language |
| --- | --- |
| Harness | The system around the AI model that decides inputs, tools, notes, checks, retries, and stopping. |
| NLAH | Natural-Language Agent Harness: the readable document carrying one task family's rules. |
| IHR | Intelligent Harness Runtime: the shared interpreter that reads an NLAH and runs the calls and checks. |
| Base agent | The minimal worker loop whose only tool is a terminal for files, processes, and launching children. |
| Task packet | A small handoff note a parent sends a child to start one chunk of work as a fresh instance. |
| Artifact contract | The agreed hand-in rule: exactly what file or proof must exist at the end, and how it is checked. |
| Verifier | A separate checking step or module that judges whether the work passes before accepting it. |
| File-backed state | Shared notes saved to files so parent and child do not lose track across steps. |
| Self-evolution | A module where the agent revises its own approach or notes based on feedback during the run. |
| Multi-candidate search | Trying several candidate solutions in parallel instead of one straight attempt. |
| Context compression | Shrinking the accumulated notes and history into a shorter summary to save space. |
| Handoff recall | How much of the important information survives when work passes from parent to child. |

