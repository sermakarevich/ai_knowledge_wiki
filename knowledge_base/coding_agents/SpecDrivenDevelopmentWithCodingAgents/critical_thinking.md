> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: Spec-Driven Development with Coding Agents - DeepLearning.AI

## Claims vs. evidence
- Claim: detailed markdown specs produce better, more maintainable software than vibe coding. Evidence in digest/wiki: assertion only, no metrics, comparisons, or code-review data.
- Claim: specs preserve context across agent sessions and improve intent fidelity. Evidence: plausible mechanism (persistent constitution + feature spec), but no failure cases or session-window measurements shown.
- Claim: the workflow reduces "cognitive debt." Evidence: term is used, never defined or operationalized; no before/after illustration in the material summarized.
- Claim: "many of the best developers already work this way." Evidence: authority statement from course copy, not a survey or citation.
- Claim: the same plan-implement-verify loop works on greenfield and legacy code. Evidence: lesson titles cover both, including bootstrapping specs from existing docs, but depth is thin (legacy = one 4m video).
- Structural fact that weakens all claims: Beginner level, 1h16m total, 15 videos, 0 code examples, 1 graded assignment. This is an orientation, not an empirical study.
- Claim: replanning between features compounds into an MVP. Evidence: course outline shows two feature phases plus an MVP lesson, but no definition of MVP scope or when to stop replanning.
- Claim: agent skills make the workflow reusable and portable. Evidence: a single 6m "build your own workflow" video plus a 3m "agent replaceability" video; no cross-IDE demonstration captured in the digest.

## Genuinely new vs. repackaged
- Genuinely useful packaging: constitution (mission, tech stack, roadmap) + per-feature spec + replan-between-features as one named loop is a compact, teachable scaffold for agent work.
- Repackaged: plan-implement-verify is classic design-build-test / TDD-at-feature-granularity with "verify" relabeled for agents.
- Repackaged: the project constitution is AGENTS.md / CLAUDE.md / repo memory conventions under a grander name, plus a roadmap doc.
- Repackaged: "package your workflow into a portable agent skill" restates Claude Skills, Cursor rules, Copilot instructions, and JetBrains Junie guidelines; portability across agents/IDEs is asserted, not demonstrated in the digest.
- Genuinely timely (not new): framing specs as the anti-drift device for stateless agents names a real failure mode — agents forget intent between sessions — even if the fix is old documentation discipline.
- Useful emphasis: iterative planning loops before implementation, rather than one-shot prompting, matches how agent output quality actually scales with upfront structure.
- Missing novelty check: nothing in the digest distinguishes the constitution from lightweight RFCs or architecture decision records, which already solve context preservation for humans.
- Net: maybe 20% new framing, 80% disciplined-docs-plus-agile relabeled for the agent era.

## Weaknesses and blind spots
- No treatment of spec drift: who updates the constitution when code and spec diverge, and how is divergence detected?
- No treatment of spec quality: what makes a spec good, testable, or appropriately sized? A bad spec faithfully implemented is still a bad feature.
- Verification is under-specified: "validate human-in-the-loop" gets a 4m video and a 1m implementation video — the hardest step (tests, acceptance criteria, evals) gets the least time.
- No cost/benefit analysis: spec-writing overhead vs. vibe-coding speed is never quantified; no guidance on when a lightweight prompt beats a full spec.
- No failure taxonomy: hallucinated APIs, over-scoped features, legacy docs that lie, conflicting instructions between constitution and feature spec — none surfaced in the digest.
- Vendor framing risk: built with JetBrains, taught by a JetBrains advocate; "agent replaceability" and portability claims deserve skepticism until tested outside the demo IDE.
- Environment setup gets more time (5m reading + 1m video) than implementation (1m), which signals a tool-onboarding course rather than an engineering-methods course.
- No security or review posture: agent-written code merged under a spec still needs threat review, dependency checks, and data-access scrutiny — none mentioned.
- Prerequisite ("basic familiarity with a language and LLM coding tools") confirms the audience is new agent users, so advanced practitioners should calibrate expectations down.
- Assessment is thin: one graded assignment plus a 10m quiz cannot verify the workflow transfers to real codebases.

## Applicability
- Good fit: greenfield MVPs with 2–5 features where intent clarity matters more than iteration speed; onboarding agents onto a legacy repo with decent existing docs.
- Partial fit: large refactors and long-lived services, where the missing spec-maintenance story becomes the dominant cost.
- Poor fit: spikes, exploratory data work, and hotfixes, where spec ceremony costs more than agent drift.
- **Relevance to my work**
  - AI/ML engineering: adopt the constitution-plus-feature-spec skeleton for experiment repos — dataset, metrics, and acceptance thresholds belong in the spec, since "done" is otherwise undefined.
  - Agentic systems: plan-implement-verify maps directly onto agent harness design (planner, executor, verifier roles); the course's weakest step, verification, is where agentic evaluation and regression prompts should be invested.
  - Elisity data platform: trial SDD for agent-assisted pipeline and schema changes, where intent fidelity and auditability matter; require each feature spec to state data contracts, backfill rules, and rollback criteria before the agent writes code.
- Process suggestion: make the constitution a versioned repo file with an owner and a changelog, so "living context" does not silently rot.
- Process suggestion: pair every feature spec with executable acceptance checks (tests, eval queries, pipeline dry-runs) to close the verification gap the course leaves open.

## What this changes
- Changes little technically, but usefully reframes the agent from "pair programmer you chat with" to "contractor you brief in writing" — the artifact (spec), not the chat, is the unit of work.
- If taken seriously, it shifts agent effort left: more time writing constitutions and acceptance criteria, less time re-prompting a drifting agent.
- It normalizes portable workflow skills as team assets, which — if the portability claim holds — turns personal prompting habits into reviewable, versioned process.
- It does not change the fundamental bottleneck: judgment about what to build and how to verify it still sits with the human, and the course gives that step the least instruction.
- It raises the status of written intent as a durable team artifact: specs outlive any single agent session and become reviewable history, unlike chat transcripts.
- It implies a new code-review surface: reviewers should diff the spec against the implementation, not just review the code — a habit most teams have not built yet.

## Verdict
- Worth one focused hour for the vocabulary (constitution, intent fidelity, plan-implement-verify) and the MVP/replan cadence, but do not mistake it for evidence or depth.
- Borrow the scaffold, discard the hype: require written specs with acceptance criteria for agent work, but supply your own standards for spec quality, verification, and drift control.
- Concretely: run the pilot with a frozen constitution for one milestone, measure rework rate and reviewer time versus a vibe-coded baseline, then keep or drop the ceremony.
- Skip a full team rollout until spec maintenance, verification standards, and cross-IDE portability are proven on that pilot.
- **trial**: pilot the constitution-plus-spec workflow on one Elisity feature slice before deciding anything broader.
