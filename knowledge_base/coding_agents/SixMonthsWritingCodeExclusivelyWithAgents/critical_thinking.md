> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: Six Months of Writing Code Exclusively With Agents - exe.dev blog

## Claims vs. evidence

- **Claim: a hard no-hand-code rule builds agent skill.** Evidence is anecdotal but concrete: one rule held six months, broken once for three minutes, with the stated mechanism of fixing prompts, tools, or environment whenever an agent stalled rather than finishing the code.
- **Claim: models crossed a usability threshold this year.** Supported only by author experience: Copilot and Cursor helped with drafts, while Claude Code plus GPT-5.3 and Opus 4.6 handled larger multi-file changes with less steering — no benchmarks or comparisons offered.
- **Claim: parallelism forces per-task VMs.** The isolation ladder is well-evidenced within the narrative: shared box collisions, worktrees fixing only Git, AGENTS.md patches burning context, containers leaking via laptop reachability and sleep, then one exe.dev VM per task with a validated startup script.
- **Claim: botd plus YOLO-in-VM is safe enough.** Partially evidenced: disposable VMs, proxied credentials, and write limits to test environments are described, but no incident data, injection attempts, or cost figures back the safety or economy claims.
- **Claim: non-coding agents carry the highest leverage.** Strongest evidence in the piece: verbatim-report investigators resolving issues with docs or emails, a red-team agent demonstrating reachable paths thought restricted, and Athena continuing a wave rollout after diagnosing infrastructure failure — each a specific outcome, not a generality.
- **Claim: validation scales but judgment does not.** Credible because the author admits the failure mode: agent-run tests, CI, screenshots, and peer-agent review still left self-graded work, unfamiliar whole diffs, abandoned VMs, and discarded green builds that were not worth shipping.

- **Claim: iteration moves from code to prompts, designs, and features.** Plausible given the Shelley example and SQLite conversation-querying, but supported by a single recalled design change rather than repeated measurement.
- **Claim: botd's collapse proves vibe coding fails where architecture matters.** Strongest self-indictment in the piece: an unread, unarchitected multi-harness core became a brand-new legacy codebase, though the data survived because history lived in SQLite.

## Genuinely new vs. repackaged

- **Genuinely new:** the isolation-to-VM-per-task progression with a learned startup-script loop, and botd's three rules (off-laptop, mobile-first, preserve every conversation) turning SQLite history into a queryable record of how decisions were made.
- **Genuinely new:** Athena-style deploy-watching as sustained attention work — diligent, undistracted wave-rollout triage — framed as a role humans perform worse, not just faster code output.
- **Repackaged:** "agent is a model in a loop with tools" and Willison's lethal trifecta (private data plus untrusted content plus external communication) are restated foundations, applied competently rather than invented.
- **Repackaged:** testing, migration, and hygiene lessons — behavior/contract/property tests over implementation-mirroring tests, state and migrations as the hard part, tolerated bad patterns becoming templates — are classic engineering truths amplified by agents copying whatever they find.
- **Repackaged:** the Shelley async-tools example (every command backgrounds after sixty seconds) is good simplification-by-design, but the move itself — deleting edge cases instead of handling them — predates agents.

- **Repackaged:** "shipping got easy, deciding what to ship got important" plus Hyrum's Law on unshipping restates product judgment as the bottleneck — true, but not agent-specific.
- **Repackaged:** fixing the environment instead of the code when an agent stalls is the familiar "fix the system, not the symptom" rule applied to prompts, tools, and sandboxes.

## Weaknesses and blind spots

- **Single-author, single-stack sample:** one expert with a strong prior mental model, one product family, ~20 VMs peak; no team, junior, regulated, or brownfield-legacy counterpoint.
- **No cost, latency, or quality numbers:** VM spend, model spend, idle/abandoned work rate, defect escape rate, and review time are all absent, so "failures were cheap" is asserted, not shown.
- **Security argument is thin:** YOLO mode plus credential proxying plus test-only writes is plausible for a dev-tool company, but there is no threat model test, no prompt-injection near-miss, and no discussion of customer-data exposure beyond ClickHouse log access.
- **Review bottleneck unresolved:** peer-agent review "worked surprisingly well" yet the author still had to load every diff into his head; "merge code we deem should be merged" and "peer review is dead" sit uneasily beside that admission.
- **Survivorship framing:** discarded work, dead-end designs, and the vibe-coded collapse of botd are presented as cheap tuition, but without a baseline it is unclear whether throughput gains outweigh rework and lost line-by-line familiarity.
- **Missing model-risk discussion:** no treatment of stale training data, hallucinated APIs, license hygiene in generated code, or how unfamiliar diffs affect debugging under incident pressure.
- **Missing human factors:** onboarding others onto agent-built systems, ownership handoff, on-call burden, and how conversation history substitutes for readable architecture are gestured at, not tested.

## Applicability

- Transfers best to greenfield or well-tested services with disposable environments, strong CI, and engineers who already hold the system model; transfers poorly where state, compliance, or blast radius forbids YOLO-style execution.
- The per-task VM plus startup-script plus conversation-preservation pattern is directly reusable for parallel agent fleets; the Athena deploy-watcher and verbatim-report investigator patterns are reusable without adopting the whole apparatus.
- Hygiene prerequisites are non-negotiable: contract/property tests, migration discipline, linter-encoded conventions, and isolated credentials must precede scale, or agents amplify existing mess.

- **Relevance to my work**
  - *AI/ML engineering:* adopt verbatim-report investigators over ClickHouse-style logs, behavior/contract/property tests for pipelines, and bespoke linters for data-schema conventions before scaling coding agents.
  - *Agentic systems:* copy the tools-not-loop framing, lethal-trifecta combination watch, disposable per-task environments, proxied secrets, and preserved queryable conversation history; add cost and escape-rate instrumentation the post omits.
  - *Elisity data platform:* highest value is investigator, red-team, and deploy-watcher roles around rollouts and incidents, plus migration-first planning for stateful changes; do not replicate YOLO writes against production-adjacent data.
  - *What to skip for now:* full YOLO execution, phone-first fleet ops, and declaring peer review dead until review-load and defect data from a bounded pilot justify it.

## What this changes

- Shifts the scarce skill from typing multi-layer edits to deciding what is worth shipping and engineering the system (architecture, interfaces, constraints, tradeoffs) before accepting code.
- Moves iteration up a level — from code to prompts, designs, and whole features — with rewrites costing a conversation and history queryable instead of memorized.
- Reframes review: the check that matters happens earlier in design discussion, contracts, and validation, with diffs arriving whole and unfamiliar rather than understood incrementally.
- Makes hygiene compounding: good patterns amplify, bad patterns amplify faster, and the marginal cost of encoding lessons as tools has collapsed.
- Makes environment investment the multiplier: startup scripts, ephemeral resources, and disposable machines decide whether parallel agents help or collide.

## Verdict

Useful as a field report, weak as a prescription: the VM-per-task ladder, non-coding agent roles, and agentic-engineering-before-code stance are worth borrowing, but the absent costs, single-expert sample, unresolved review bottleneck, and botd's own vibe-coded collapse argue against wholesale adoption. Run the investigator and deploy-watcher patterns and the disposable-environment plus conversation-history machinery as bounded pilots with measured rework and incident effects. Overall: **trial**.
