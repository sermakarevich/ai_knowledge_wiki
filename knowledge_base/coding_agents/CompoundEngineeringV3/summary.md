# Compound Engineering v3

**Source:** [Compound Engineering v3 (Trevin Chow, 2026)](https://x.com/trevin/status/2047066108763770998)

## Human Readable TL;DR

Think of Compound Engineering as a smart assistant that helps software teams build better software. In v3, they gave every tool a consistent label so nothing gets confused, added a "paper trail" system so you can always trace a bug back to the original idea that caused it, made the assistant work equally well on every coding platform, and upgraded the code review process so you actually have to think about each problem individually instead of clicking "approve all".

## TL;DR

Compound Engineering 3.0.0 ships four major improvements: a unified `ce-` namespace eliminating skill name collisions across harnesses; structured artifact IDs threading from `ce-brainstorm` through `ce-plan` to `ce-work`, giving agents and humans a traceable provenance chain; first-class install and runtime support on Codex, Pi, and Copilot alongside Claude Code; and per-finding interactive review flows replacing bucket-level policies that enabled rubber-stamping.

---

## Problem & Motivation

CE's prior releases accumulated naming inconsistencies (`ce:work`, `git-commit`, `setup` mixing three conventions), lacked stable artifact IDs across the brainstorm-to-commit pipeline (requirements existed only as prose and "vibes"), treated Claude Code as the primary harness while others were second-class ports, and allowed reviewers to approve entire batches of findings with a single decision -- degrading review quality.

---

## Main Original Ideas

1. **Unified `ce-` Namespace** -- Every skill and agent now lives under a single `ce-` hyphen prefix. `ce:work` → `ce-work`, `git-commit` → `ce-commit`, `setup` → `ce-setup`. This eliminates collision with other plugins across harnesses and resolves Windows filesystem issues from the colon syntax. Breaking change.

2. **Structured Artifact Paper Trail** -- `ce-brainstorm` now produces docs with first-class sections: Actors, Key Flows, Acceptance Examples, and Requirements -- each with stable IDs. `ce-plan` pulls those IDs into a Requirements Trace section and assigns plan-local unit IDs. `ce-work` references unit IDs in blockers and task labels. This allows agents and humans to trace failing tests → acceptance examples → flows → brainstorm entries.

3. **Cross-Harness Parity** -- Codex gets native marketplace install (`codex plugin marketplace add`) with a converter writing CE agents as TOML under `~/.codex/agents/`. Pi drops CE's own compatibility layer in favor of @nicopreme's `pi-subagents` (real parallelism) and @edlzsh's `pi-ask-user` (blocking questions). Copilot (CLI + VSCode) gets native plugin install support.

4. **Per-Finding Review Engagement** -- `ce-code-review` now walks findings one at a time with Apply/Defer/Skip/"LFG the rest" options. `ce-doc-review` adds three-tier autofix classification and premise-dependency chain grouping -- collapsing related findings into one decision, dropping typical engagement from 14+ findings to 4-6 real decisions. A new `ce-swift-ios-reviewer` persona joins for Swift/iOS stacks.

5. **Tightened Debug Methodology** -- `ce-debug` gains an early environment sanity check (branch, deps, runtime, env vars, stale artifacts), an assumption audit at hypothesis time, parallel read-only subagent dispatch for broad searches, and a technique reference covering heisenbugs, boundary instrumentation, repro minimization, and a bug-class checklist.

---

## Key Findings

- Old colon-syntax skill names (`ce:work`) collided with other plugins on multi-plugin setups and caused Windows filesystem errors
- Requirements written in `ce-brainstorm` had no stable identity by the time they reached `ce-plan` -- the agent had no way to recover original intent when a test failed
- Pi's previous compatibility layer competed with the most popular community subagent extension and serialized parallel dispatch
- Bucket-level review questions (one decision per policy area) enabled rubber-stamping; per-finding engagement significantly raises review quality
- `ce-debug` previously defaulted to print-debugging and skipped environment sanity, sometimes declaring heisenbugs "fixed" when instrumentation merely suppressed them

| Area | Before v3 | After v3 |
|------|-----------|----------|
| Skill naming | Mixed prefixes (`ce:`, `git-`, none) | Uniform `ce-` prefix |
| Requirement traceability | Prose only, no stable IDs | Stable IDs from brainstorm → plan → work |
| Pi parallelism | Serialized (CE's own layer) | Real parallel via community extension |
| Review engagement | Bucket decisions, rubber-stamp risk | Per-finding: Apply / Defer / Skip |
| Doc review decisions | ~14+ findings per run | ~4-6 real decisions |

---

## Suggestions & Future Directions

1. **More product and strategy skills** -- Greenfield product-tier support expanded in v3 but more depth is planned
2. **Sharper verification and shipping support** -- Continued investment in the commit-to-ship pipeline
3. **Configurable preferences** -- Hardcoded paths like `docs/solutions` for compounded-docs output will become user-configurable; nearly ready for v3 but held back to bake longer
4. **Codex custom agents** -- Plugin spec doesn't cover custom agents yet; current workaround is TOML converter under `~/.codex/agents/`, likely to be replaced when the spec matures

---

## Authors & Institutions

Trevin Chow (@trevin) -- Ex: Big Cartel, Sketchylearning, Axon Technology, Nike, Microsoft. Contributors: @jcjvm (ce-swift-ios-reviewer), Lucas Henn (ce-demo-reel local save), @andrewlook (ce-update safety fix), @nicopreme (pi-subagents), @edlzsh (pi-ask-user).
