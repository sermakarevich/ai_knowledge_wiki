# Open questions — ai_coding_best_practices (coding_agents)

Focus: What are the evidence-backed best practices for using AI coding assistants for writing, debugging, and refactoring code?

> Seed for the next run: each question below names the sub-topic it belongs to; a re-run may add one sub-topic per question. No question here is answered by the current sources.

## 01 — code-generation

### 1. What verification workflow minimizes the review/rework tax while preserving generation speedups?
- **Sub-topic:** 01-code-generation
- **Why it matters:** Generation speeds up routine drafting ~40–55%, but reviewing, refining, and reworking output can consume up to half of assisted time and makes acceptance/merge rates misleading. Without an evidence-backed verify-first workflow, best-practice guidance cannot tell practitioners where the net win actually is.

### 2. Which prompt and repair patterns reliably reduce security weaknesses across models and tasks?
- **Sub-topic:** 01-code-generation
- **Why it matters:** About a quarter of committed Copilot snippets carry confirmed weaknesses, while mitigations (security persona prefix, self-critique-and-fix, warning-fed repair) work unevenly and even backfire on some models; coercive framing hurts. Best practices for writing secure code with assistants depend on knowing which patterns generalize rather than being model- or setup-specific.

### 3. Do multi-agent / TDD-governed generation pipelines scale beyond small pilots, and is their overhead justified?
- **Sub-topic:** 01-code-generation
- **Why it matters:** Engineered context plus enforced process (multi-agent pipeline, test-first gating, bounded repair) shows large single-shot gains on a handful of tasks at 3–5× token cost, but evidence is preliminary and small-scale. Scaling evidence decides whether this is a recommended practice for repository-level work or an expensive exception.

### 4. How should novice versus expert usage differ to keep speed gains without over-trust or skill erosion?
- **Sub-topic:** 01-code-generation
- **Why it matters:** Beginners gain the most speed but verify the worst; experts gain less but verify better. Role-specific practices (what novices must check, where experts add value) determine whether assistant use builds capability or degrades it.

### 5. When does AI assistance improve versus degrade code quality (defects, maintainability, security)?
- **Sub-topic:** 01-code-generation
- **Why it matters:** Sources disagree on quality direction — some report fewer defects, others subtle errors and harder-to-maintain code. Best practices cannot recommend "generate more" versus "generate narrowly" until the conditions separating these outcomes are pinned down.

## 02 — debugging

### 6. Does the human-like repair pipeline (on-demand static+dynamic context, typed diagnosis, trace-diff refinement) generalize beyond Java benchmark bugs?
- **Sub-topic:** 02-debugging
- **Why it matters:** The strongest debugging evidence is Java-only (Defects4J/RWB) with fixed budgets; the broader survey stays at taxonomy level. Generalization evidence decides whether this pipeline is a general debugging best practice or a Java-benchmark result.

### 7. What are the cost, latency, and stopping budgets for iterative debug/repair loops in practice?
- **Sub-topic:** 02-debugging
- **Why it matters:** Iterative feedback loops clearly beat one-shot patching, but current budgets (e.g. bounded diagnosis/refinement rounds, validation caps) come from benchmark settings. Practitioners need evidence-backed stopping rules that trade fix rate against per-bug cost and waiting time.

### 8. Do self-directed debugging and test-free IDE-integrated repair generalize beyond benchmark Java bugs? (supersedes the filled gap below)
- **Sub-topic:** 02-debugging
- **Why it matters:** The former gap — two of four debugging sources unreachable — is now closed: DebugRepair (224 Defects4J fixes on GPT-3.5, 295 on DeepSeek-V3, all QuixBugs Java/Python, $0.036/bug) and the PracAPR vision (ROSE prototype, +44% task success) both corroborate the runtime-evidence-plus-iteration thesis. What remains open is generalization: DebugRepair still assumes perfect fault localization and explicit test cases (SWE-bench issue-only settings are out of scope), ROSE's user study is single-setting, and multi-location repair has a taxonomy but no evaluated fix rate. Evidence on issue-only debugging, imperfect localization, and multi-location strategies decides whether these pipelines are general practices or benchmark results.

## 03 — refactoring

### 9. Do iterative readability-refactoring dynamics hold beyond clean Java snippets and a single model, and what stopping rule prevents over-refactoring?
- **Sub-topic:** 03-refactoring
- **Why it matters:** Restructure-then-stabilize convergence with structural drift (line growth, comment loss, rare functionality breaks) is shown on one educational Java repo with one main model and anecdotal readability judgment. Verified stopping criteria decide when to let the assistant iterate versus stop.

### 10. Which review-assistant mode (proactive co-reviewer vs. on-demand assistant) fits which situation, and how is the false-positive trap avoided?
- **Sub-topic:** 03-refactoring
- **Why it matters:** Preference is situational (unfamiliar/complex/large/low-risk vs. familiar/codebase-owned work), and noisy suggestions can flood reviewers into missing real issues. Evidence on mode selection plus noise control turns review assistance from a demo into a dependable refactoring/review practice.

### 11. How can refactoring and review assistants preserve valuable documentation while using deeper project context?
- **Sub-topic:** 03-refactoring
- **Why it matters:** Both sub-topic sources flag the same gap: inline comments get stripped by repeated refactoring, and reviewers blame missing architecture docs, conventions, and connected-repo context for superficial feedback. Comment-preservation mechanisms plus context design are the precondition for safe, useful AI-assisted refactoring.

### 12. Where should the model/human refactoring boundary sit across languages, models, and change types?
- **Sub-topic:** 03-refactoring
- **Why it matters:** The StarCoder2-vs-developer split (model wins surface/syntactic, humans win structural/dependency-heavy) comes from one open model on Java with tool-dependent measurement. Best practices need the boundary re-checked per language, per model generation, and per refactoring type before teams can safely route clean-ups to the model and design work to humans.
