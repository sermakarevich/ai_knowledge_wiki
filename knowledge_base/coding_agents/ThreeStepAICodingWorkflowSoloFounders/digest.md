> [[index|Wiki]] | [[summary|Summary]]
# A 3-step AI coding workflow for solo founders | Ryan Carson (5x founder) — Digest

## 1. [[wiki/01-three-step-ai-coding-workflow|Three-step AI coding workflow for solo founders]]
**In one sentence:** The biggest mistake with AI coding is rushing context, so slow down and run a PRD → task list → one-subtask-at-a-time execution loop in Cursor to reliably build large features solo.
## Key points
- The core failure mode is impatience with context: not telling the AI what it needs to know to solve the problem.
- The fix is a three-file Cursor-rules loop: a PRD generator rule, a task-list generator rule, and a task-list manager rule for iterative execution.
- The PRD prompt is framed as "suitable for a junior developer to understand and implement," which keeps the AI concrete instead of assuming obvious details.
- PRD clarifying questions use dot notation (e.g. 2.1, 2.2) so answers stay addressable; unanswered questions get "make your best judgment / you pick."
- Generated PRDs go into a `tasks/` folder and task lists use markdown checkboxes with tasks, subtasks, and sub-subtasks plus a "relevant files" section.
- Execution does one subtask at a time, marks it complete immediately, then stops and waits for user go-ahead (often just "y") before continuing.
- Ryan reports building features of ~10,000 lines of code reliably with this loop plus human-in-the-loop checks and commits after workable parent tasks.

## The argument in five moves
1. The bottleneck in AI coding is not the model but rushed context, so slowing down to specify what the AI needs to know speeds everything up.
2. That patience is operationalized as three Cursor rules — PRD generation, task-list generation, and task-list management — demonstrated on a yacht-club CRM feature.
3. Step one produces a junior-developer-grade PRD via clarifying questions in dot notation, defaulting open questions to the AI's best judgment.
4. Step two turns the PRD into an explicit checkboxed task list with relevant files, and step three executes it one subtask at a time with human go-ahead, commits at workable states, and fixes for the small errors the AI introduces.
5. Context tooling (Postgres/Browserbase MCPs, Repo Prompt token-shrinking, hand-cranked markdown over PM tools) and coaching-style prompting extend the loop.
6. The payoff is solo-founder leverage: not a replacement for a PM or CTO's depth, but enough to build the company alone where a 110-person team with PMs once stood.
