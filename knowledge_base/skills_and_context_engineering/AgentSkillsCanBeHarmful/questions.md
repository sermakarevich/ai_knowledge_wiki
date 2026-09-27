---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Agent Skills Can Be Harmful

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. In this paper's contrastive design, what is a "reference run," and why does the paper insist it is a "pseudo-oracle" rather than a ground-truth solution?

> [!tip]- Answer
> A reference run is another execution of the *same* task (same verifier, agent framework, model, and repo/container state) under a different skill setup — either no skill or a semantically matched alternative skill. It's a pseudo-oracle, not ground truth, because passing or being cheaper only shows the task *can* be solved (or solved more cheaply) under otherwise identical conditions — it doesn't certify that its own trajectory is optimal or the only correct approach, just that the target run's failure/cost can be attributed to the skill rather than to task difficulty or base-model limits. See [[wiki/01-problem-and-methodology|Methodology]].

### Q2. Write out the formal condition used to classify a PASS/PASS pair as an efficiency regression at threshold T, and explain in plain terms why both a minimum and a maximum condition are required (rather than just one ratio exceeding T).

> [!tip]- Answer
> The condition is: min(rtok, rtime) > 1.0 AND max(rtok, rtime) > T, where rtok and rtime are target-to-reference token and time ratios (primary T = 2.0). The min>1.0 part requires *both* metrics to worsen, which rules out ordinary token/time tradeoffs (e.g., a run that uses fewer tokens but takes longer). The max>T part requires at least one metric to worsen substantially, which filters out small, likely-noise fluctuations. Together they isolate large, genuine two-sided cost regressions. See [[wiki/01-problem-and-methodology|Methodology]].

### Q3. Among the 125 confirmed functional failures, Applicability Mismatch (skill picked for the wrong topic) is only 1.6% of cases, while Task-Implementation Fault is 68.8%. What does this imbalance demonstrate about where skill-induced failures actually originate?

> [!tip]- Answer
> It shows failures almost never come from bad skill *selection/routing* (the skill being topically wrong for the task) — they come from an on-topic, correctly-selected skill causing the agent to fill in or omit a required implementation element incorrectly, often because the agent over-trusts the skill's reusable defaults, examples, or templates as if they were task-specific requirements. The practical implication is that better skill-matching alone would not fix most failures; skill *content* design (separating mandatory requirements from optional examples) is the real lever. See [[wiki/02-functional-failure-taxonomy|Functional Failure Taxonomy]].

### Q4. What is the operational difference between "Incorrect Required-Element Fill" (IRF) and "Required-Element Omission" (RRO), and why does this distinction matter for how a skill author would fix each one?

> [!tip]- Answer
> IRF means the target artifact *does* contain an implementation of the required element, but it's wrong (e.g., computing a ratio without the required percentage scaling). RRO means the required element is absent entirely, with no concrete substitute provided (e.g., a configurable-parameter requirement that the skill's example never demonstrated, so the agent never added it). Fixing IRF requires correcting the skill's guidance/examples so agents implement the element the right way; fixing RRO requires expanding the skill's examples/checklists to cover elements they currently omit, since agents tend to faithfully copy only what's shown. See [[wiki/02-functional-failure-taxonomy|Functional Failure Taxonomy]].

### Q5. If Excessive Verification (EV) and Heavy Implementation Pipeline (HIP) were entirely removed from the Excessive Procedure category (leaving only Excessive Exploration), would Excessive Procedure still be the single largest root-cause category of efficiency regressions? Justify with the numbers.

> [!tip]- Answer
> No. EP totals 114/182 (62.6%) cases, made up of EE (17), HIP (30), and EV (67). Removing HIP and EV would leave only EE's 17 cases, far below Context Bloat's 46 cases and even below Dependency Resolution's 22 cases. This shows the "Excessive Procedure dominates" finding is driven almost entirely by EV and HIP (97 of 114 cases), not by exploration overhead — the dominant mechanism is the agent doing unnecessary extra verification and heavier construction work, not wandering the repo more. See [[wiki/03-efficiency-regression-taxonomy|Efficiency Regression Taxonomy]].

### Q6. The paper distinguishes Context Bloat from Excessive Procedure as root causes of efficiency regressions. Explain the mechanism-level difference between them, and give an example of how the *same* extra content in a skill could, in principle, cause one or the other.

> [!tip]- Answer
> Context Bloat means each individual model call becomes more expensive (bigger prompts/context) while the *sequence* of task-solving steps stays similar to the reference run — the cost driver is content size. Excessive Procedure means the skill changes the trajectory itself, adding extra exploration, implementation, or verification steps — the cost driver is more steps, not bigger calls. The same skill content (e.g., a long checklist) could cause Context Bloat if it's just always loaded into every prompt without changing behavior, or cause Excessive Procedure if the agent actually acts on the checklist by running extra verification/rebuild steps. When both effects appear together, the paper assigns the label to whichever is the larger observed cost driver. See [[wiki/03-efficiency-regression-taxonomy|Efficiency Regression Taxonomy]].

### Q7. Suppose you run SkillTriage on a new confirmed case where the target run wrote a fully correct helper module, but at `src/utils/helpers.py` instead of the task-specified `lib/core/helpers.py`, while the reference run wrote it to the correct path. Which functional-failure category and evidence signal (DS1–DS5) should drive the attribution, and why would it NOT be classified as an Environment Mismatch or Incorrect Required-Element Fill?

> [!tip]- Answer
> This should be attributed to Artifact Misplacement, driven by DS3 (which tests task-required paths against target write paths). It's not Environment Mismatch because the runtime/dependency/environment state isn't what diverges — the code content and execution environment are fine. It's not IRF because the artifact's *content* is correct; the divergence is purely about *where* it was written, matching the paper's stated principle that the decisive failure is location, not artifact quality. See [[wiki/04-skilltriage-tool-and-evaluation|SkillTriage]].

### Q8. SkillTriage reaches 93.6% category accuracy on functional failures but only 79.7% on efficiency regressions, and within-category subcategory accuracy drops further for efficiency regressions (68.4% for Excessive Procedure) than for functional failures (88.4% for Task-Implementation Fault). What does the paper attribute this accuracy gap to, and what does it imply about deploying automated attribution tools in practice?

> [!tip]- Answer
> The gap is attributed to boundary errors: efficiency-regression subcategories (Excessive Exploration, Heavy Implementation Pipeline, Excessive Verification) often overlap in the same trajectory — e.g., dependency repair happening inside a verification loop, or a build command that could plausibly be tagged as either implementation or verification — making the correct single label genuinely ambiguous even for humans. This implies automated triage tools should not be trusted as opaque single-label oracles; they should expose the underlying evidence (cited skill section, trajectory step, cost-heavy step) alongside the label, so a human can adjudicate boundary cases, which is exactly the design choice the paper makes for SkillTriage's output. See [[wiki/04-skilltriage-tool-and-evaluation|SkillTriage]].

### Q9. This paper's evidence rests on one agent runtime (OpenCode 1.15.1), one model (Claude Opus 4.6), and two skill-sharing sites for augmentation. If you had to name the single weakest link in the paper's evidence chain, what would it be, and why?

> [!tip]- Answer
> Arguably the weakest link is generalizability across agent harness and model: all 307 confirmed cases and the entire taxonomy were produced by one specific agent runtime paired with one specific frontier model, so findings like "skills rarely fail via applicability mismatch" or "efficiency regressions are dominated by Excessive Procedure" could partly reflect how *this* runtime/model combination happens to use skills (e.g., how aggressively it treats checklists as mandatory) rather than a universal property of agent skills. The authors acknowledge this threat but mitigate it only by avoiding claims tied to the two specific benchmarks — they do not re-run the study on a second harness or model to confirm the taxonomy transfers. A secondary weak link is the reliance on human judgment for root-cause labeling, mitigated by consensus and cross-checking with SkillTriage, but SkillTriage itself was built and evaluated using GPT-5.5 against the same human labels, which is a fairly tight validation loop rather than fully independent confirmation. See [[wiki/01-problem-and-methodology|Methodology]].
