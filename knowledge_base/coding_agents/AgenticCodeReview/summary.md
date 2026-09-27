# Agentic Code Review

**Source:** [Addy Osmani (@addyosmani) on X (Jun 15, 2026)](https://x.com/addyosmani/status/2066595308629594363)
**Author:** Addy Osmani (Google Chrome)
**Published:** June 15, 2026

---

## Human Readable TL;DR

Imagine a factory that suddenly produces 4x the goods per worker -- but quality control didn't scale up at all. That's software development with AI coding agents. The code is being written faster than any team can check it, so unreviewed code is quietly slipping through. Addy Osmani's argument: the most valuable skill in software right now isn't writing code, it's knowing how to confidently decide if code is correct. And the trick is using AI to help you review AI code -- not instead of you, but alongside you -- while saving your real attention for the decisions only a human should make.

## TL;DR

AI agents produce code at machine speed while human reading speed is unchanged, creating a structural review bottleneck. Multiple large-scale datasets (Faros AI: 22K devs; CodeRabbit: 470 OSS PRs; GitClear: production telemetry) converge: 4x the code output yields ~12% more delivered value, while defect rates, churn, and zero-review merges all spike. The prescriptions: tier review depth by blast radius, require intent artifacts before review, run heterogeneous multi-model AI review (93.4% of bugs are caught by exactly one tool -- diversity beats redundancy), and move the human "up a level" to own accountability and high-stakes gates rather than reading every diff.

---

## Problem & Motivation

Code review was built around a happy accident: senior engineers could read code faster than juniors could write it. AI agents shattered that assumption -- they produce thousands of lines in seconds while human reading speed is unchanged. The consequence is a measurable, multi-dataset crisis: code churn +861%, defect rates jumping from 9% to 54%, review time up 441%, and 31% more PRs merging with zero review. Crucially, mature and disciplined teams were hit just as hard as undisciplined ones -- good process didn't protect against the volume increase. On top of that, agent PRs carry a known quality deficit (1.7x more issues per CodeRabbit) and strip the intent/reasoning from the diff, forcing reviewers to reconstruct a rationale that was never written down.

---

## Main Original Ideas

1. **The Constraint Moved Downstream** -- Writing code is no longer the bottleneck; being confident a change is correct is. This is not a loss -- it is the highest-leverage place in software right now. The same tools generating all that extra code are the best tools for triaging the review queue.

2. **Blast Radius Determines Review Rules** -- Three variables set the correct review depth: blast radius (what happens when it breaks), code longevity (prototype vs. 10-year system), and team size (just you vs. shared ownership). Most advice in circulation is one position on this spectrum telling the other how to live. Solo/no-users and enterprise/old-codebase share almost no constraints worth naming.

3. **The Missing Intent Problem** -- Agent PRs discard the agent's reasoning the moment the diff is produced. The reviewer becomes "the first human to ever lay eyes on this code," forced to reconstruct intent that was never written down. This is why review time is up 441%. The fix is a tooling problem: require the agent to produce a decision log (what it was trying to do, what it ruled out) attached to the PR. Recoverable, but currently neglected.

4. **Heterogeneous Multi-Model Review** -- In a 4-tool parallel experiment across 146 real PRs and 679 findings, 93.4% of flagged locations were caught by exactly one tool; none caught by all four. Tool strengths: Greptile (near-zero false positives, correctness/architecture), CodeRabbit (widest net, one-click fixes, Martian F1 winner at ~49% precision), Sentry Seer (production-failure severity), Cursor BugBot. Running two with different architectures beats running four copies of the same model.

5. **Human Moves "Up a Level"** -- The human doesn't leave the loop; they shift from reading every diff to owning what doesn't transfer to a model: (a) accountability -- a model cannot be paged, (b) judgment of whether this is the right change to build, and (c) requirements nobody specified, because a model reviews the code that exists, not the behavior nobody thought to write down.

6. **Plan-First Architecture (Kun Chen Pattern)** -- Ex-Meta L8 shipping ~40 PRs/day solo: writes detailed plans up front, runs 20-30 agents for hours against them, uses an automated review gate ("No Mistakes") before merge. The "first human to read this" problem is half-solved when intent is written up front. Rational for a solo builder with no blast radius; dangerous to copy onto a team.

7. **Agents Will Weaken CI** -- Not maliciously -- via gradient descent finding the cheapest path to green. Watch for: removed tests, lowered coverage thresholds, skipped lint, duplicated helpers, and user-controlled text piped into LLM calls without sanitization (prompt injection). Deterministic gates are the one part of the pipeline that cannot be talked out of their verdict by a confident paragraph.

---

## Key Findings

| Source | Method | Key Numbers |
|--------|--------|------------|
| Faros AI (Mar 2026) | 22K devs, 4K teams | Code churn **+861%**, defect rate **9% → 54%**, review duration **+441.5%**, zero-review merges **+31.3%**, incidents/PR **+242.7%** |
| CodeRabbit (Dec 2025) | 470 OSS PRs (320 AI / 150 human) | AI PRs carry **~1.7x more issues**: logic +75%, security +1.5-2x, readability 3x+ |
| GitClear (2025) | Production telemetry | **4x raw output**, **~12% more delivered value** (possibly selection bias) |
| GitHub | Platform-wide | **60M Copilot reviews** (10x in under a year), **>1 in 5** reviews involves an agent |
| Anthropic Code Review | Internal PRs | PRs receiving substantive review: **16% → 54%**; **<1%** findings marked incorrect |
| Martian benchmark (Jan-Feb 2026) | Tool comparison | CodeRabbit: 49% precision, best recall; Greptile: 82% bug-catch rate, more false positives |
| 4-tool parallel experiment | 146 PRs, 679 findings | **93.4%** caught by exactly **one** tool; **0%** caught by all four |
| Early-Stage Prediction (Jan 2026) | 33,707 agent PRs | 28% merge near-instantly; **38%** of rejections = reviewer abandonment on subjective feedback |

- Agent PRs run **51% larger on average** (Faros); reviewer engagement is strongest predictor a PR merges at all
- *AI Slop and the Software Commons* (2026, 1,154 posts): developer quote -- "the first human being to ever lay eyes on this code"

---

## Suggestions & Future Directions

1. **Tier review by risk, not author** -- config change: linter + glance; core business logic: types + tests + two AI reviewers + human owner + security pass
2. **Raise intake bar** -- require before review: statement of intent, readable diff size, test output, proof it ran; push intent-reconstruction cost back to submitter
3. **Fast-fail high-maintenance PRs** -- use cheap signals (file types, patch size) as circuit-breaker before humans invest time (Early-Stage Prediction paper pattern)
4. **Instruct agents to produce small commits** -- reviewable diff as explicit design constraint, not a courtesy
5. **Read test changes first** -- canonical agent failure: change behavior + rewrite assertion to match; mutation testing over coverage alone to verify tests would actually catch regressions
6. **Keep CI as the immovable wall** -- watch specifically for prompt injection surfaces (user-controlled text → LLM calls)
7. **Capture agent reasoning as decision logs on PRs** -- the single highest-leverage fix for the 441% review time increase; the reasoning existed, it was just discarded
8. **Measure review capacity as a real resource** -- QA and review work rises even as output rises; cutting senior reviewers because "AI made us faster" converts the saving into future incidents

---

## Authors & Institutions

Addy Osmani -- Engineering Director, Chrome (Google); data cited from: Faros AI, CodeRabbit, GitClear, GitHub, Martian benchmark, anonymous 4-tool experiment (146 PRs), *AI Slop and the Software Commons* (2026), *Early-Stage Prediction of Review Effort* (Jan 2026)
