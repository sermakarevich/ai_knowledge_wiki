> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: Spec-driven development with AI: Get started with a new open source toolkit - The GitHub BlogLinkedIn iconInstagram iconYouTube iconX iconTikTok iconTwitch icon

## Claims vs. evidence

- **Claim: specs become "living, executable" shared truth.** Evidence offered: none beyond assertion. The digest describes the spec driving checklists and task breakdowns, but no example of a spec catching a real defect, resolving ambiguity, or surviving a mid-project pivot.
- **Claim: four gated phases (Specify → Plan → Tasks → Implement) beat one-shot code dumps.** Plausible mechanism — smaller reviewable diffs, TDD-like isolation — but no comparative data: no defect rates, review times, or before/after measurements versus direct prompting.
- **Claim: developer "steer + verify" checkpoints catch gaps and edge cases.** The checkpoint questions (does the spec capture intent, does the plan handle constraints) are sensible, but the digest gives no evidence reviewers actually catch more with this ritual than with normal code review, nor how long verification takes.
- **Claim: tool-agnostic workflow (Copilot, Claude Code, Gemini CLI).** Supported only by naming the agents; no interop detail, no note on which slash-command hosts work where, no failure matrix.
- **Claim: parallel per-task implementation stays safe.** The digest says tasks run "one by one or in parallel" because order is known upfront — but offers no dependency analysis, no conflict story, and no rollback guidance when parallel tasks collide.
- **Net:** the digest's argument is a coherent how-to narrative, not an evaluated result. Treat every benefit as hypothesis, not finding.

## Genuinely new vs. repackaged

- **Genuinely new (packaging, not theory):** the opinionated CLI loop — `specify init`, `/specify`, `/plan`, `/tasks` — that scaffolds agent-compatible artifacts in one place. Prior spec tooling rarely shipped slash-command ergonomics aimed directly at coding agents.
- **Repackaged:** almost everything else. Specify-what-before-how is classic requirements engineering; Plan-with-constraints is architecture decision records plus standards docs; Tasks-as-small-testable-chunks is WBS / issue decomposition / TDD rhetoric; Implement-per-task is incremental delivery.
- **Repackaged:** "AI generates, human verifies" is the standard human-in-the-loop slogan, restated as "steer, don't just write." The digest adds checkpoint language but no novel verification technique (no formal checks, property tests, or spec-execution semantics).
- **Verdict on novelty:** workflow glue is new; underlying ideas are decades old, now rebranded for the agent era.
- **"Executable" is doing heavy lifting:** nothing in the digest shows specs that run, test themselves, or enforce conformance — "executable" reads as aspirational metaphor for "consulted often," not a technical property.
- **What the CLI actually adds:** artifact scaffolding plus phase ordering. That is real ergonomic value for agent workflows, but it is scaffolding innovation, not methodological invention.

## Weaknesses and blind spots

- **No failure modes:** what happens when the spec is wrong, contradictory, or stale? No guidance on spec drift, merge conflicts between plan variations, or cost of re-specifying mid-implementation.
- **Verification is hand-waved:** "critique gaps before advancing" assumes the developer can spot what the agent missed — the hardest part. No checklists, no acceptance-test generation discipline, no definition of "validated."
- **Scale and legacy gaps:** Plan claims to absorb legacy/compliance/performance constraints, but there is no worked example — no brownfield repo, no monorepo, no regulated-environment walkthrough.
- **Thin source base:** per the digest, the second chunk is pure related-posts/newsletter boilerplate. The entire substantive argument rests on a single how-to section; there is no counterargument, limitation, or user report in the material.
- **Vendor framing risk:** a GitHub-published piece promoting a GitHub toolkit invites optimism bias — costs (spec authoring time, review overhead, agent token spend on artifacts) are never quantified.
- **Missing maintenance story:** living artifacts need gardeners. No ownership model, no review cadence, no rule for when a code change must propagate back into spec/plan/tasks.
- **No human-factors account:** the process assumes developers enjoy and excel at spec critique, yet spec review is a known weak muscle on teams that adopted agile precisely to escape big-upfront-spec fatigue.

## Applicability

- **Where it fits:** greenfield features with fuzzy requirements, agent-assisted teams drowning in unreviewable thousand-line diffs, and shops that already value written specs but let them rot.
- **Where it strains:** hotfixes, exploratory spikes, and tightly-coupled legacy changes where writing a full spec costs more than the fix; also teams without review discipline — gates only work if someone enforces them.
- **Adoption cost:** low to try (open-source CLI, markdown artifacts), medium to sustain — value depends entirely on reviewers doing real verification at each gate rather than rubber-stamping agent output.
- **First-trial shape:** one bounded feature, one reviewer empowered to reject at each gate, with review time and rework logged — otherwise the trial proves nothing.

**Relevance to my work**

- **AI/ML engineering:** directly usable as a prompt-structuring discipline — force what/why (data, metrics, success criteria) before stack choices; plan variations map well to experiment configs and eval harnesses.
- **Agentic systems:** the Specify → Plan → Tasks → Implement loop is a template for agent orchestration itself — decomposing agent work into isolated, testable tasks with explicit human checkpoints mirrors safe agent deployment patterns.
- **Elisity data platform:** highest leverage in data-pipeline and API work where contracts matter — spec-first endpoint/pipeline definitions (schemas, validation rules like the email-format example, compliance constraints) could cut integration churn if reviewers treat specs as living contracts.

## What this changes

- **If taken seriously:** shifts agent effort from "generate code fast" to "generate reviewable artifacts in order" — code becomes a downstream rendering of spec + plan + tasks rather than the primary medium.
- **For team process:** makes the review surface earlier and smaller — critique a spec paragraph instead of a 1,000-line diff — but only if gates are real stops, not ceremonial clicks.
- **For tooling:** normalizes slash-command-driven SDLC scaffolding inside the editor; expect copycat kits embedding org standards directly into `/plan` templates.
- **For agent-economics framing:** reframes token spend from "more code per prompt" to "more intermediate artifacts per feature" — cheaper to evaluate only if reviewers actually read them instead of skimming to the final diff.
- **What it does not change:** the fundamental need for someone who understands the domain to say "this spec is wrong." The toolkit moves the judgment earlier; it does not automate it.

## Verdict

- Useful process discipline with near-zero trial cost, but sold on assertion rather than evidence — worth testing on one real feature with measured review effort before standardizing.
- The repackaging is honest enough to be actionable: even skeptics of "spec-driven" branding can steal the gated artifact flow and per-task implementation rule.
- Big open question the material never answers: does spec authoring + gate review actually cost less than fixing agent-generated code after the fact? Only a trial resolves that.
- Watch item: whether the "living spec" survives contact with week-three scope cuts — if teams stop updating artifacts, the process degrades into waterfall with slash commands.

**trial**
