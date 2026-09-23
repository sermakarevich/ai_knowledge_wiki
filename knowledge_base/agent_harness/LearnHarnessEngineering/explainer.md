> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Welcome to Learn Harness Engineering | Learn Harness Engineering — In Plain Language
## What is this about?
Learn Harness Engineering is a course about making AI coding helpers
reliable enough to trust with real work.
Think of tools like Codex (an AI coding tool from OpenAI) and
Claude Code (an AI coding tool from Anthropic).
Out of the box they are smart but flaky: they write code fast,
then get lost, forget things, or claim a job is done when it is not.
This course says: do not just wait for a smarter model.
Instead, build a better workshop around the model.
That workshop is called a harness — the setup around the AI:
rules, note files, tests, and controls that keep it on track.
The course pulls together the best ideas from the industry,
including guides from OpenAI and Anthropic (two leading AI labs),
plus a community collection called Awesome Harness Engineering.
It turns those ideas into lessons to study, small projects to build,
and ready-to-copy templates.
## Why does it matter?
A strong AI model alone is not enough. Anyone who has used an AI coding
assistant knows the pattern: it starts brilliantly, then drifts.
It edits the wrong file. It forgets what it did yesterday.
It says "all done!" while the tests still fail.
It cannot explain what it changed or why.
That hurts when you want real development work: building a feature,
fixing a bug, or automating a boring chore. You need the AI to behave
like a careful junior engineer, not an overconfident intern.
Harness engineering is the difference between a cool demo and
a dependable worker. It gives you fewer surprises (the agent — the AI
doing the task — works inside clear boundaries), memory across sessions
(notes and state, i.e. saved progress, survive between runs), honest
results (tests catch unfinished work), and less debugging pain
(you can see what the agent did). In short: the model provides
the brains, the harness provides the discipline.
## How does it work?
The course teaches one big idea: a harness is a closed-loop working system.
"Closed-loop" (a process that checks its own results and corrects itself)
means the AI does not answer once and stop. It works in a circle:
try something, check the result, fix mistakes, repeat until it passes.
That circle rests on four supports.
1. **Environment design.** Set up the workspace before the AI starts:
which folders it may touch, which commands it may run, what "done" looks like.
Like child-proofing a room before letting a toddler play in it.
2. **State management.** Give the AI a memory outside its own head.
`feature_list.json` (a simple task list) and `claude-progress.md`
(a running diary) store what is finished and what is next, so a new
session picks up where the last one left off.
3. **Verification.** Do not trust the agent's word — test its work,
with full-pipeline tests (checks running the whole workflow end to end)
plus self-reflection (the AI reviewing its own output critically).
4. **Control systems.** Add guardrails (automatic limits and rules).
Explicit rules in `AGENTS.md` (a rulebook the agent reads) say what it may
and may not do. Other controls stop it declaring victory too early and make
its actions observable (visible, traceable) and debuggable (easy to inspect).
To teach this, the course offers three paths: **lectures** explain theory,
starting with "Why Capable Agents Still Fail"; **projects** let you build
a minimal harness, starting with "Baseline vs Minimal Harness" — first watch
the raw agent fail, then watch it improve with rules, memory, and tests;
a **resource library** gives copy-ready templates (`AGENTS.md`,
`feature_list.json`, `claude-progress.md`) for your own projects.
There are also breakdowns of real tools — Pi, Claude Code, Codex,
and DeepSeek (four AI coding products) — showing how each designs its harness.
## Where can this be used?
Anywhere you want an AI to do multi-step coding work without babysitting:
**building features** (task list plus rules, then code, tests, report);
**fixing bugs** (reproduce the bug — make the error happen again — patch it,
prove it with tests); **automating chores** like migrations (moving code
or data to a new setup), upgrades, and repetitive edits; **long-running
projects** spanning hours or days, where memory files keep the thread alive;
**team setups**, where shared rulebooks keep every developer and agent
on the same standards. Rule of thumb: one prompt and ten seconds needs
no harness; ten steps and two days does.
## Conclusions & takeaways
- Smart models still fail without structure; reliability comes from engineering around the model.
- A harness is no magic brain upgrade — it is rules, memory, checks, and controls.
- Start small: watch the bare agent stumble, then add one guardrail (limit) at a time.
- Write things down: task lists and progress notes are the cheapest long-term memory.
- Never accept "done" on faith: tests and self-review turn claims into confirmed results.
- Steal the starter pack: `AGENTS.md`, `feature_list.json`, `claude-progress.md`.
- Next: Lecture 01 for the "why", Project 01 for the "how", templates for practice.
## Jargon decoder
| Term | What it really means |
|------|----------------------|
| Harness | Support system around the AI: rules, memory files, tests, controls. |
| Agent | AI program doing a task step by step, like a junior engineer. |
| Closed-loop system | Workflow where the AI tries, checks, fixes, and repeats until it passes. |
| Environment design | Setting up folders, permissions, and "done" before work starts. |
| State management | Saving progress in files so the AI remembers context (background details) across sessions. |
| Verification | Proving work correct with tests and reviews, not trusting claims. |
| Full-pipeline test | Check running the whole workflow end to end, not one piece. |
| Self-reflection | The AI re-reading and criticizing its own work before finishing. |
| Observable / debuggable | Every step visible and easy to inspect when things break. |
| Guardrails | Automatic rules and limits stopping unsafe or sloppy actions. |
| AGENTS.md | Rulebook file in the project telling the AI how to behave. |
| feature_list.json | Simple machine-readable task list the agent checks off. |
