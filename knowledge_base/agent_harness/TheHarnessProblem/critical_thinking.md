> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: We improved 15 LLMs at coding in one afternoon. Only the harness changed. — Stencil

## Claims vs. evidence
- Headline claim: changing only the edit tool improved ~15 models by ~15 points on average with zero training compute.
- Support: 16-model × 180-task × 3-run table with fresh agent session per run and four tools (read, edit, write); hashline beats patch in 14/16.
- "Weakest gain most" claim: Grok Code Fast 1 went 6.7% → 68.3%, "a tenfold improvement."
- Mechanism offered: catastrophic patch failures hid real coding ability (Grok 4 patch failure 50.7%, GLM-4.7 46.2%).
- Caveat: the tenfold figure depends on a near-zero patch baseline, so it measures format mismatch more than reasoning gains.
- Token claim: best-case output tokens fell 61% (Grok 4 Fast) because models "stopped burning tokens on retry loops."
- Gap: only output-token deltas reported (TOK column); input-token cost of hash tags on every read/grep is unreported.
- Counterevidence in-table: GPT-5.2 Codex +26% and DeepSeek V3.2 +20% token increases; DeepSeek regresses −5 vs patch and −8.3 vs replace.
- "Bigger than most model upgrades" (Gemini +8% for ~$300 benchmarking): rhetorical comparison, no upgrade baseline measured, no significance tests.
- "Patch is worst for nearly every model": holds 14/16, but the DeepSeek exception is unexplained and breaks universality.

## Genuinely new vs. repackaged
- Genuinely new: hashline — every line returned with a 2–3 char content hash (e.g. `2:f1`), model edits by anchor ("replace range 1:a3 through 3:0e").
- New property: stale reads rejected before corruption, since hashes "optimistically won't match" after file changes.
- New rationale: recalling a pseudo-random tag proves the model knows what it edits, removing the need to reproduce whitespace exactly.
- New framing: "the model isn't flaky at understanding, it's flaky at expressing itself — blaming the pilot for the landing gear."
- New method stance: model-agnostic open harness where "the model is but a parameter" and the harness is the controlled variable.
- Repackaged: "format matters as much as the model" — Aider already showed GPT-4 Turbo swinging 26% → 59% on format alone.
- Repackaged: JetBrains Diff-XYZ ("no single edit format dominates") and EDIT-Bench ("only one model over 60% pass@1") are cited in the piece itself.
- Repackaged pain points: apply_patch blob strictness, str_replace exact-match fragility ("String to replace not found" megathread +27 issues).
- Repackaged: Cursor's 70B merger model still losing to full rewrites under 400 lines; Gemini's fuzzy-whitespace variant of str_replace.
- Advocacy, not finding: "the model is the moat, the harness is the bridge," plus single-sided Anthropic/OpenCode and Google-ban anecdotes.

## Weaknesses and blind spots
- Synthetic fixtures: random React file + mechanical mutations (operator swaps, boolean flips, off-by-ones, removed guard clauses, renames).
- Scoring bias: success means reverting the mutation after formatting; valid alternative fixes count as failures, understating true capability.
- Narrow scope: single-file bug fixes with read/edit/write only — no multi-file refactors, large repos, terminal/test loops, or human UX.
- Statistics missing: 180 tasks × 3 runs is modest; no error bars, no per-task variance, no v1-vs-v2 ablation beyond headline deltas.
- Best v2 data point (GPT-5.1 Codex Mini 60.0% → 77.5%) is reported without distribution or significance.
- Cost accounting one-sided: output tokens down, but per-line hash tags inflate input tokens and possibly latency — neither measured.
- Failure modes unexamined: hash collisions, tag hallucination, anchor recall errors, human readability of tagged file views.
- Confounder: gateway-level token bias toward patch for Codex variants is asserted ("almost certainly"), not tested.
- Prompt and schema tuning per format unclear; per-model prompt sensitivity could explain part of the DeepSeek regression.
- Source bias: Stencil sells an open harness, so "don't block open harnesses" serves its positioning; per-run reports promised but not evaluable here.

## Applicability
- Direct lesson: before swapping models, profile harness failures — patch errors, retry loops, token burn — and A/B the edit tool per model.
- Generalizes to any agent replaying seen content: file edits, SQL rewrites, config patches, notebook cell updates.
- Stale-hash rejection is a cheap concurrency guard wherever agents act on previously read state.
- Scrolling/UX and JSONL-leak examples (Claude Code subagents) remind that harness polish is user-visible quality, not plumbing.
- **Relevance to my work**
  - AI/ML engineering: track edit-format as an eval hyperparameter; report patch-failure and retry rates beside pass rates.
  - AI/ML engineering: re-run model comparisons under at least two harnesses before concluding which model is "best."
  - Agentic systems: instrument tool schemas, error messages, and state staleness; prefer verifiable anchors over exact-string replay.
  - Agentic systems: measure input+output tokens and latency, and add a stale-edit stress test to the agent eval suite.
  - Elisity data platform: pilot hash-anchored edits for agent-managed pipelines, queries, and configs with reject-on-stale-read.
  - Elisity data platform: quantify reliability and cost wins on platform tasks before standardizing any new edit format.

## What this changes
- Leaderboards without a pinned harness are misleading; every "best coding model" claim should name edit format and harness version.
- Harness work (schemas, error messages, state management) can beat a model upgrade on ROI for edit-heavy agents.
- A ~$300 afternoon experiment legitimately competes with waiting for the next model drop — at least directionally.
- Weak-model failures deserve re-diagnosis: format mismatch can masquerade as poor reasoning.
- Small/cheap models become viable again once catastrophic patch failures are removed from their scores.
- Open model-agnostic harnesses are where cross-model tuning happens, since no vendor tunes for competitors.

## Verdict
- A strong, well-scoped demonstration of one mechanism with striking breadth (16 models), weakened by synthetic tasks and missing statistics.
- Input-cost blindness and one unexplained regression mean the universality claim overreaches; vendor anecdotes add heat, not evidence.
- Still, the fix is cheap, reversible, and directly testable on our own edit workloads with full token accounting.
- Replicate hashline vs str_replace internally, including stale-edit and multi-file stress tests, before any platform-wide adoption.
- **trial**
