> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: Rules | Cursor DocsCursor LogoCursor Logo

## Claims vs. evidence

- Claim: rules give "persistent, reusable" agent context because LLMs keep no memory between completions. Evidence in digest: plausible mechanism (prepend to context), but no measurement of retention, recall rate, or conflict resolution — mechanism asserted, not demonstrated.
- Claim: four application modes (Always, Intelligent, glob-scoped, Manual) route the right rule at the right time. Evidence: frontmatter truth table and glob examples are concrete, yet "Apply Intelligently" rests on the Agent judging a short description — no precision/recall data or failure examples given.
- Claim: Team Rules with enforce-toggle guarantee org-wide standards. Evidence: dashboard controls and precedence order are documented, but enforcement is inclusion in prompt context, not a hard guardrail — the doc itself concedes AI guidance is not a security control.
- Claim: best practices (under 500 lines, composable, `@`-reference instead of copy) keep rules fresh and effective. Evidence: sensible engineering advice, but presented as maxims; no before/after token counts, staleness cases, or retrieval-latency numbers.
- Claim: `AGENTS.md` nesting and plugin import cover simple and shared cases. Evidence: directory-combination rule and marketplace flow are specified, yet migration guidance (`.mdc` vs `AGENTS.md` vs both) and dedup behavior are absent.
- Claim: rules can be created from chat (`/create-rule`, "ask the agent to create a rule"). Evidence: creation path is described, but there is no review/validation step documented — a generated rule with wrong globs fails silently per the FAQ.
- Claim: "start simple, add rules only when Agent repeats a mistake" prevents bloat. Evidence: reasonable heuristics ("Start simple"), but no signal for when a rule should be deleted or demoted from Always to glob-scoped.
- Claim: file references via `@template` stay fresher than pasted contents. Evidence: directionally sound (single source of truth), though no detail on how referenced files are resolved, versioned, or budgeted in context.

## Genuinely new vs. repackaged

- Genuinely useful: the explicit `alwaysApply`/`description`/`globs` decision matrix — a compact routing contract many agent-config docs leave implicit.
- Genuinely useful: glob-scoped Team Rules plus Team → Project → User precedence with "earlier wins" — a clear multi-layer merge semantic.
- Genuinely useful: the "rule that writes rules" loop (`/create-rule`, `@cursor` on GitHub issues to update rules) — codified self-maintenance rather than one-off setup.
- Repackaged: "prepend instructions to context" is standard system-prompt layering, not a Cursor invention; the novelty is packaging and UI.
- Repackaged: `/create-rule`, Customize sidebar, `@`-references, and template pointers restate familiar IDE-snippet plus prompt-include patterns.
- Repackaged: `AGENTS.md` support follows the emerging cross-tool `AGENTS.md` convention; Cursor documents compatibility rather than originating it.
- Repackaged: "don't paste the style guide, use a linter" and "don't document npm/git" restate general prompt-hygiene advice found in every agent-framework guide.

## Weaknesses and blind spots

- Silent-failure surface: a plain `.md` in `.cursor/rules` is ignored; a missing description or non-matching glob means a rule never fires — the FAQ names this, but there is no lint, dry-run, or "which rules applied" inspector described.
- "Intelligent" retrieval is a black box: no scoring, threshold, tie-breaking, or debugging story when two descriptions both match.
- Conflict semantics are thin: "earlier sources win" says nothing about intra-file contradictions, rule ordering within one layer, or size-budget eviction when many Always rules pile up.
- Context economics ignored: no token budget, truncation policy, dedup of overlapping Team/Project/User rules, or performance guidance beyond "under 500 lines".
- Scope gaps are explicit but consequential: rules do not affect Cursor Tab or Inline Edit (`Cmd/Ctrl+K`), so style/standards coverage is Agent-Chat-only — easy to misread as global.
- Security posture is honest yet weak: enforced rules aid compliance workflows but are prompt-level hints an agent can misinterpret; no mention of evaluation, audit logs, or rollback.
- Plugin distribution friction: rules cannot be imported standalone and require a marketplace plugin with `.cursor-plugin/marketplace.json` — heavyweight for sharing a single convention file.
- No lifecycle story: nothing on rule ownership, deprecation, per-rule analytics (fire rate, acceptance), or testing a rule change before enforcing it team-wide.
- User Rules are global-but-partial (Agent Chat only, styled as "concise replies" examples), which invites overloading personal preferences with project facts that belong in version control.
- Examples skew to greenfield web stacks (Tailwind, Framer Motion, zod, Express/React templates); data-pipeline, notebook, IaC, and monorepo-scale rule organization get little attention.
- Nested `AGENTS.md` "more specific wins" is stated without a worked merge example against `.mdc` precedence, leaving the interaction of the two systems ambiguous.

## Applicability

- Directly applicable anywhere a team repeats the same agent corrections: encode the correction once as a scoped rule, `@`-reference the canonical template, and review when the agent errs.
- Team-first precedence fits org standards (lint configs, API error shapes, copyright headers) while leaving project-level exceptions in `.cursor/rules`.
- Glob scoping plus nested `AGENTS.md` maps well to monorepos: directory-local conventions without one giant always-on prompt.
- Manual `@`-mention rules suit rare-but-critical procedures (migrations with `up`/`down`, release checklists) that must not consume context daily.
- The 500-line/composable guidance is a usable review bar in PRs: reject pasted style guides, require `@`-links to canonical files.
- **Relevance to my work**
  - AI/ML engineering: glob-scoped rules for training vs. serving code, zod/pydantic validation conventions, eval-harness commands the agent should not re-invent.
  - Agentic systems: description-gated workflow rules (analyze app, draft docs, run `npm run dev` + read logs) as reusable agent playbooks with explicit triggers.
  - Elisity data platform: project rules pinning schema-validation, error-envelope, logging, and storage-flag patterns; enforced Team Rules for compliance-relevant headers and review checklists (as hints, not sole controls).

## What this changes

- Treats agent guidance as versioned config: check `.cursor/rules/*.mdc` into git, keep each rule focused and `@`-linked, split on the third repeated correction.
- Shifts rule-writing from style-guide dumps to retrieval design: short descriptions for intelligent recall, tight globs for precision, manual `@`-mention for rare migrations.
- Downgrades "enforced" expectations: useful for consistency nudges and onboarding, insufficient as a compliance or security boundary — pair with linters, tests, and CI checks.
- Suggests a dual-track default: `.mdc` rules where routing matters, plain nested `AGENTS.md` where simplicity and cross-tool portability matter.
- Adds a maintenance habit the doc hints at but underplays: assign each rule an owner, re-check fire-rate quarterly, and delete rules the agent has internalized or stopped needing.
- Reframes sharing: prefer `@`-referenced in-repo templates over plugin packaging unless the rule truly spans many repos.

## Verdict

- Useful conventions layer with a crisp routing model, undermined by silent failures, opaque intelligent recall, and prompt-level (not hard) enforcement.
- Net: worth a bounded pilot with fire-rate checks and linter/CI backing, not a blind org-wide mandate.
- On balance the pragmatic move is a scoped rollout on one repo plus one enforced team rule, then review hit-rate before wider rollout: **trial**.
