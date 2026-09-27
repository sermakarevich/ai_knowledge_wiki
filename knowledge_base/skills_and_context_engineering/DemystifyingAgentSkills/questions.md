---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Demystifying Agent Skills: Why They Work-Until They Don't

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What is the central gap the paper claims existing skill evaluation leaves open, and how does the paper's contrastive design address it?

> [!tip]- Answer
> Existing work only measures aggregate task success — if a skill-augmented agent solves more tasks, the skill is called useful, but nothing is learned about *why*. The paper addresses this by comparing matched executions (Raw / Workflow Memory / Skill) built from the *same* prior trajectories, so any behavioral difference must come from how the experience is represented rather than from having more information. See [[wiki/01-introduction-and-related-work|Introduction and Related Work]].

### Q2. Why is "Skill vs Workflow Memory" the load-bearing comparison in the paper, rather than "Skill vs Raw"?

> [!tip]- Answer
> Workflow Memory and Skill are constructed from the exact same source trajectories — only the representation differs. The Skill-vs-Workflow-Memory delta (+6.06 pp, 95% CI [+0.76, +11.36]) is therefore attributable specifically to *how* the experience is packaged, whereas Skill-vs-Raw (+2.84 pp, CI crossing zero) conflates "having any prior experience" with "having it in skill form." See [[wiki/04-findings|Findings, Conclusion, and Limitations]].

### Q3. What are the four research questions (RQ1–RQ4), and what does each isolate?

> [!tip]- Answer
> RQ1: whether representation (skill vs. direct workflow memory) shapes experience reuse when trajectories are fixed. RQ2: whether the benefit comes from procedural content or from explicit success/failure outcome labels (standard vs. no-hint). RQ3: whether distilled guidance transfers across agent frameworks (source in Codex, evaluated in Gemini CLI). RQ4: how skill-pool size and distractor confusability affect retrieval and downstream execution. See [[wiki/02-study-design|Study Design]].

### Q4. What does "procedural anchoring" mean, and how much of the skill mechanism does it account for versus "knowledge injection"?

> [!tip]- Answer
> Procedural anchoring means the skill supplies a usable procedure — ordering, checklist, tool sequence, or verification plan — stabilizing *actions* rather than supplying new facts. It accounts for 65.7% of skill mechanism labels, versus only 4.5% for knowledge_injection (concrete domain knowledge the agent otherwise lacked). This is the paper's central mechanistic claim: skills work mainly by stabilizing behavior, not by teaching. See [[wiki/04-findings|Findings, Conclusion, and Limitations]].

### Q5. Describe the three Skill-use Categories (SC1, SC2, SC3) and how their counts shift between the Raw, Workflow Memory, and Skill arms.

> [!tip]- Answer
> SC1 (successful procedural anchoring) rises for skill (326/528) over workflow memory (294/528). SC2 (execution/verification-layer failures) drops for skill (124/528) versus raw (197/528) and workflow memory (176/528). SC3 (invocation/applicability/boundary failures) *increases* for skill (78/528) versus raw (19/528) — skills reduce execution-layer breakage but introduce a new misapplication failure surface. See [[wiki/03-skill-use-mechanisms|Skill-Use Mechanisms]].

### Q6. Why does the paper interpret RQ4's results only as "within-pairing" comparisons, not against RQ1–RQ3?

> [!tip]- Answer
> GPT-5.3-Codex (used for the Codex pairing in RQ1–RQ3) was no longer available under the same evaluation access when RQ4 was run, so RQ4's Codex experiments substitute GPT-5.4. Because the model changed, RQ4's absolute numbers cannot be validly compared model-to-model against RQ1–RQ3's Codex results — only the three RQ4 arms can be compared against each other. See [[wiki/02-study-design|Study Design]].

### Q7. What is the retrieval-precision collapse finding, and why doesn't it translate into a comparable collapse in task success?

> [!tip]- Answer
> As candidate pool size grows from 5 to 100, averaged actual-use precision (Arm 3, real execution) falls from 29.6% to 3.3%, while downstream task success changes only from 36.4% to 39.3%. This gap exists because exact ground-truth-skill invocation is neither necessary nor sufficient for success — agents often inspect multiple candidates (Arm 3 recall stays 54.3–73.6% at k=100) and can complete tasks using partial procedural support from related, non-ground-truth skills. See [[wiki/04-findings|Findings, Conclusion, and Limitations]].

### Q8. Between raw pool size and distractor type, which is the dominant stressor for correctly identifying the right skill, and what is the evidence?

> [!tip]- Answer
> Semantic confusability (similar distractors) is the dominant stressor, not raw pool size. In Arm 1 (embedding retrieval), top-1 precision on *similar* pools falls from 70.5% at k=5 to 53.4% at k=100, compared with only 97.7%→84.1% for random pools and 96.6%→93.2% for dissimilar pools — a much steeper drop for similar distractors than pool size alone would predict. See [[wiki/04-findings|Findings, Conclusion, and Limitations]] and [[wiki/05-implementation-details-and-prompts|Implementation Details and Prompts]].

### Q9. How were the paper's taxonomy labels validated, and why does that validation matter for trusting the findings?

> [!tip]- Answer
> An independent human annotator performed 714 trajectory–label checks (238 open-coded labels × 3 supporting trajectories each), confirming all of them, and then independently remapped the 238 raw labels to the 12 canonical modes, achieving 95.8% exact agreement with the LLM aggregation and Cohen's κ = 0.952. This matters because the entire taxonomy — and therefore the SC1/SC2/SC3 breakdown driving the paper's central claims — is LLM-assisted; without this validation step, the categories could just reflect LLM judgment quirks rather than genuine behavioral patterns. See [[wiki/03-skill-use-mechanisms|Skill-Use Mechanisms]].

### Q10. The paper shows an "effectiveness–efficiency trade-off" on the matched 83-task token analysis. What is it, and what would you expect if you needed to optimize purely for token cost rather than success rate?

> [!tip]- Answer
> On the matched intersection, Skill achieves the highest success (69.6%, +5.5 pp vs Raw) but uses more tokens than Workflow Memory (521.5K vs 426.2K total per task, though fewer than Raw's 555.7K); Workflow Memory is the most token-efficient representation (+0.7 pp success at the lowest token cost). If optimizing purely for token cost with only a marginal success requirement, Workflow Memory would be the better choice; if optimizing for success rate, Skill's extra ~95K tokens per task over Workflow Memory buys +4.8 pp success. See [[wiki/05-implementation-details-and-prompts|Implementation Details and Prompts]].

### Q11. How would you apply this paper's contrastive-triple methodology to evaluate a new procedural-memory feature in an internal coding-agent system?

> [!tip]- Answer
> Build matched triples for the same tasks under (a) no memory, (b) raw retrieved logs/traces as context, and (c) a distilled skill/playbook built from the same traces — holding the underlying experience fixed. Then have a judge (human or LLM, ideally validated against human labels) classify each run into failure/success modes rather than only recording pass/fail, so gains and regressions can be attributed to specific behavioral changes (e.g., fewer environment-setup failures vs. new misapplication failures) instead of an opaque aggregate score. Also separately test retrieval-in-isolation (can the right playbook be found?) against downstream success, since the paper shows these can diverge sharply as the playbook library grows.

### Q12. What is the single weakest link in this paper's evidence base, and why?

> [!tip]- Answer
> The mechanism taxonomy — which underlies essentially every headline claim (procedural anchoring vs. knowledge injection, SC1/SC2/SC3 shifts) — is induced from an open-coding sample covering only ~3% of the normalized 8,135-record manifest (240 trajectories), then applied via LLM judging across the full 528-triple paired sample. While the taxonomy construction is independently human-validated (95.8% agreement, κ = 0.952), the full paired-triple labeling itself remains LLM-assisted rather than exhaustively human-coded, so rare or subtly-different behavioral modes could be misclassified or underrepresented at scale even though the taxonomy's category definitions are sound. See [[critical_thinking|Critical Analysis]].
