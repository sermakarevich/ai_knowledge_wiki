> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: Rethinking Code Review Workflows with LLM

## Claims vs. evidence

- Claim: developers prefer AI-led (Mode A) summaries for unfamiliar, large, or low-risk PRs. Evidence: moderate — consistent quotes across P3/P7/P11/P12, but from only 10 Phase 2 participants in one company with rotated but unblinded exposure.
- Claim: the assistant catches defects humans miss (race conditions, deadlocks) and confirms reviewer judgment. Evidence: weak-to-moderate — supported by session notes ("caught exactly what he was looking for") yet purely self-reported, with no defect-injection ground truth or before/after miss-rate measurement.
- Claim: the assistant speeds reviews and cuts search effort (codebase, docs, Jira). Evidence: moderate for perceived effort, weak for actual time — Phase 2 deliberately avoided performance metrics, so no timing or thoroughness numbers back the efficiency theme.
- Claim: trust is achievable if use stays optional ("no real harm" with opt-out). Evidence: weak — contradicted in the same data by reports of strange findings (wrong missing-import flag), noisy low-priority output, and hours wasted chasing impossible suggestions.
- Claim: RAG with Jira context plus a full-context `start_review` sub-agent is sufficient context grounding. Evidence: weak — participants still cited missing architecture docs, conventions, READMEs, and connected repos as the main limitation.
- Claim: Mode B (on-demand) suits familiar codebases and control-sensitive reviewers. Evidence: moderate — a minority but consistent position (P8), fitting the situational-preference synthesis ("50/50, both are useful" [P1]).
- Overall: the direction of each claim is plausible and triangulated across interviews and observation, but every effect size is qualitative and single-site.

## Genuinely new vs. repackaged

- Genuinely new: the head-to-head contrast of proactive co-reviewer (Mode A) vs. passive on-demand assistant (Mode B) on real WirelessCar PRs, with familiarity split (4 familiar, 6 unfamiliar) — prior work compared tools or accuracy, not preferred interaction.
- Genuinely new: the implementation detail that Mode A injects full PR data into a `start_review` sub-agent instead of retrieving via query engine, explicitly to guarantee per-file coverage — a concrete agentic-review pattern worth reusing.
- Genuinely new: emergent usage patterns from participants — author-side pre-review aid (P10) and human-first-then-AI-validates — which reframe the assistant as upstream quality gate, not just reviewer sidekick.
- Repackaged: Phase 1 pain points (delayed reviews, big PRs nobody picks up, context-switch cost, missing rationale) are textbook modern-code-review findings, not LLM-era discoveries.
- Repackaged: design implications (embed in GitHub/Slack/IDE, be concise with file/line refs, be fast, be context-aware, offer dual modes) are sensible but generic — any code-assistant study since Copilot lands in the same place.

## Weaknesses and blind spots

- Small, single-company, convenience sample: 7 Phase 1 and 10 Phase 2 developers at WirelessCar Sweden AB, recruited via Slack; saturation-after-7 claim is thin and cancels the scheduled eighth interview rather than testing it.
- No quantitative backbone: no detection precision/recall, no review-time delta, no control arm without AI; ordering/mode-to-PR rotation mitigates but cannot replace a baseline.
- Prototype confounds preference: the tested UI is a separate chat tool, yet the headline recommendation is "embed in existing tools" — dislike of context-switching may inflate Mode B's penalty and latency complaints.
- Prompting skill is an uncontrolled variable: P10 admits poor prompting degraded answers, so "accuracy" partly measures participant skill, not model capability; model identity, version, and temperature are absent from the wiki extract.
- Trust dynamics are snapshot, not longitudinal: no data on whether over-reliance (P3's "colored by the LLM" worry, worst in Mode A) grows as familiarity grows, nor on alert-fatigue decay from false positives.
- Thin treatment of security, privacy, and cost: enterprise-subscription-only Copilot/ChatGPT use is noted, but data-flow, secrets leakage, GPLv3 artifact licensing consequences, and agentic-review latency/cost trade-offs are unexamined.
- Missing criticality analysis: no stratification by safety/security-critical vs. routine code, even though participants say preference flips with criticality.
- No author-perspective or team-level outcomes: knowledge sharing, review turnaround, and comment quality — the stated goals of review — are never measured beyond individual perception.

## Applicability

- Transfers best to teams doing async PR review on large or unfamiliar diffs, with Jira-linked requirements and GitHub/Slack-centric workflows — i.e., standard enterprise product teams.
- Transfers poorly as a turnkey recipe: the RAG setup (LlamaIndex, `search_requirements`, full-context injection) will not scale unchanged to very large monorepos or cross-service changes (P1's bottleneck warning).
- Transfers poorly as a trust model: newcomer-heavy and low-standard teams gain most, while expert reviewers of critical code gain least — rollout should segment by audience.
- The dual-mode + pre-review + validate-after-human patterns are portable to any LLM review bot; the specific latency, verbosity, and trust numbers are not.

**Relevance to my work**

- AI/ML engineering: adopt the human-first-then-AI-validates pattern for model and pipeline PRs — keeps expert judgment primary while using the LLM as a second reader for shape mismatches, leakage, and config drift.
- Agentic systems: reuse the full-context `start_review` sub-agent over per-file retrieval for bounded diffs, but add file/line-anchored, severity-ranked output and a fast on-demand path alongside the slower agentic pass.
- Elisity data platform: pilot Jira/requirements-linked summaries on large or cross-team PRs and newcomer onboarding, embedded as expandable in-line GitHub comments rather than a separate chat UI, with opt-out and prompt coaching.

## What this changes

- Default to dual-mode assistants: proactive summary on open, on-demand Q&A after — and let familiarity, PR size, and risk select the mode rather than fixing one globally.
- Add an author-side pre-review step before PR submission; several reviewer-load problems are cheaper to fix upstream than in review.
- Require concise, actionable output discipline (file + line, severity, one-line why) and measure false-positive rate explicitly — verbosity and noise are the documented adoption killers.
- Treat requirements context (Jira/ticket injection) as table stakes, and plan the deeper context layer (arch docs, conventions, linked repos) as the real work.
- Coach prompting and keep use optional: perceived accuracy currently depends on asking skill, and opt-out is what makes experimentation low-stakes.
- Instrument the pilot from day one: log mode chosen, override rate, false-positive reports, and time-to-first-meaningful-comment, so the next review of this paper has numbers.

## Verdict

- Useful as interaction-design evidence, not as efficacy proof: it tells us which assistant shape developers reach for and why, not whether reviews get measurably better or faster.
- The honest contribution is narrow but real — situational mode preference plus two extra usage patterns — wrapped in otherwise familiar review-pain and assistant-design findings from a small single-site qualitative study.
- For our context, the cost of a scoped pilot (embedded, dual-mode, requirements-aware, with false-positive and latency tracking) is low and the upside on large/unfamiliar PRs and onboarding is concrete enough to test rather than admire from afar: **trial**.
