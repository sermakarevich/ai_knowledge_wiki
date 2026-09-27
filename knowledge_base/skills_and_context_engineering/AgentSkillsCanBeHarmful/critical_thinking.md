> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Agent Skills Can Be Harmful

## Claims vs. evidence

**Claim 1: "On-topic skills, not off-topic ones, cause most functional failures."**
Suggestive, not strong. The headline number (Applicability Mismatch = 2/125 = 1.6%) is a single-digit count in a taxonomy the authors themselves built and then hand-labeled.
With n=2, one relabeled case would double the percentage.
The finding is directionally plausible — most retrieved skills passed a cosine-similarity ≥0.7 filter, so of course few are wildly off-topic; the filter itself partly manufactures the low APM rate — but the precision implied by "1.6%" overstates what 2 data points can support.

**Claim 2: "Efficiency regressions are dominated by Excessive Procedure (62.6%, 114/182), not prompt length."**
This is the paper's best-supported claim. n=114 is a reasonable sample, and the CO vs. EP split has a clear operational definition (per-call cost vs. trajectory-length cost).
Still weak at the subcategory level: Supplementary-Material Bloat = 3/182 (1.6%) is too thin to support the stated implication ("gate supplementary material behind lazy-loading triggers") as a general design principle — it's an anecdote dressed as a category.

**Claim 3: "SkillTriage can automate attribution at useful accuracy."**
Weak, and the paper's own evaluation design has a circularity problem the wiki pages don't resolve.
SkillTriage is scored against the same manually-assigned labels that a human team produced through "group consensus" — there is no independent, blinded ground truth; the humans built the taxonomy, labeled the 307 cases with it, and then the tool is graded on reproducing those same labels. That's an internal-consistency check, not external validation.
It's also evaluated on the exact 307 cases used to iteratively define the taxonomy's category boundaries in the first place (no held-out taxonomy-development split is mentioned), so there's a real risk the categories were shaped to be the ones an LLM classifier finds easy to hit.
The 2-of-3 majority vote over 3 GPT-5.5 runs is a thin ensemble — it reduces sampling variance but not systematic bias shared across all 3 runs (e.g., GPT-5.5 having the same blind spot on the IRF/RRO boundary in every run, which is exactly where the paper reports errors concentrating: 14/125 errors at the IRF/RRO and EM/WAL boundaries).
Reporting "88.4% subcategory accuracy within TIF" while TIF is 68.8% of the dataset also means the achievable accuracy is heavily determined by getting the largest, easiest bucket right.

**Claim 4 (implicit): "Findings generalize across agents/models."**
Unsupported by the evidence presented in these five pages. Every one of the 307 cases was produced by one agent framework (OpenCode 1.15.1) and one model (Claude Opus 4.6).
There is no cross-model or cross-framework replication anywhere in the described methodology.
The "seven domains" breadth (from SkillsBench/SWE-Skills-Bench) says nothing about robustness to a different model or harness, and the two threats-to-validity dimensions (task distribution and skill ecosystem) are conflated with the harness/model dimension, which the authors flag but do not empirically probe.

## Genuinely new vs. repackaged

Novel: applying a differential/contrastive-testing design (target run vs. paired reference run, varying only the skill) specifically to attribute causal responsibility for agent failures to a *loaded skill artifact* rather than to the base model or scaffold.
The functional-failure taxonomy (APM/EM/TIF/AM) and efficiency taxonomy (CO/EP/DO) are also a genuine contribution as a named vocabulary for this failure mode.

Repackaged / built directly on prior work: the underlying benchmarks (SkillsBench, SWE-Skills-Bench) already showed pass-rate drops and >400% token overhead — this paper's "discovery" that skills can hurt is not new, only the attribution mechanism is.
The differential-testing idea itself is decades old in software engineering (mutation testing, A/B regression testing), applied here to LLM agent trajectories.
The failure taxonomy structurally mirrors MAST (multi-agent failure taxonomy) and classic software bug taxonomies (performance-bug, config-bug, DL-fault studies) — the paper explicitly says it "adapts" these.
The long-context/distraction motivation (Lost in the Middle, RAG document-count degradation) is cited as background, not as this paper's own contribution.

## Weaknesses and blind spots

Acknowledged by the authors (Threats to Validity): internal validity (subjective labeling, mitigated by consensus + exclusion of ambiguous cases + SkillTriage cross-check); external validity (single harness, single model, single pair of skill-sharing sites, task-distribution dependence) — flagged but not measured.

Not addressed, or addressed only in passing:

1. Only two marketplaces (smithery.ai, skillsmp.com) were searched, with an embedding-similarity ≥0.7 cutoff and top-5-candidates cap. This could both miss genuinely relevant skills below the threshold and admit false "semantic matches" that are topically similar-sounding but operationally unrelated, inflating or deflating APM counts in an unmeasured direction.
2. No discussion of how a skill author would practically implement "budget-aware execution policies" — the future-work section names the idea but gives no mechanism, cost model, or worked example of what a compliant SKILL.md would look like.
3. No test with smaller/weaker models. The entire failure mode (agent "over-trusting" a topically matched skill and treating examples as requirements) plausibly gets *worse*, not better, with weaker models that have less capacity to independently verify skill guidance against task text, yet the paper's evidence base can't speak to this because Opus 4.6 is the only model used.
4. Possible selection bias in benchmark choice: SkillsBench and SWE-Skills-Bench were both already known (per the paper's own related-work section) to show skill-induced regressions before this study began. Choosing benchmarks already known to contain the phenomenon under study is reasonable for mining failure mechanisms, but it means the 307-case dataset cannot support any claim about the *base rate* of skill-induced harm in typical skill usage.

## Applicability

Applies well to: teams building coding agents with a skill/plugin/instruction-file ecosystem (exactly the fleet/CLAUDE.md/SKILL.md pattern), skill-marketplace curators who need a triage signal for submitted skills, and anyone authoring SKILL.md-style files who wants a checklist of failure modes to self-audit against (mandatory-sounding examples, unscoped verification steps, path assumptions).

Would not transfer well to: non-coding agent domains where there's no deterministic verifier (both benchmarks here rely on programmatic pass/fail — the whole contrastive-attribution machinery depends on having a verifier at all; it wouldn't work for open-ended writing, conversation, or subjective-quality agent tasks). Also unlikely to transfer cleanly to smaller/open models, since the taxonomy and its "on-topic skill causes implementation fault" finding was built entirely on Opus-tier frontier-model trajectories.

**Relevance to my work** —
- Sergii's fleet orchestrator and CLAUDE.md/SKILL.md files are structurally identical to the artifact under study here — the paper's dominant failure mode (Incorrect Required-Element Fill + Required-Element Omission = 65.6% of all functional failures) is a direct warning: any of his own skill files (e.g., the `ai` CLI skill, `ai_knowledge_base` skill) that bundle examples or templates risk being treated by a coder-worker agent as literal requirements rather than illustrations.
- The Excessive Verification finding (67/182 cases, the single largest efficiency subcategory) is directly actionable for his fleet task specs: any bd task or CLAUDE.md instruction that says "always run full test suite" or "always verify with checklist X" risks inducing the same 2x+ token/time blowups this paper measures, especially when farmed out to cheaper coder models (sonnet, qwen3.6) that may follow such instructions more literally/rigidly than Opus did in this study.
- The Artifact Misplacement failure mode (19.2%, agent follows package conventions over task-specified paths) maps onto multi-repo/worktree fleet workflows — worth a spot-check that skill/instruction files specify absolute target paths rather than relying on "standard" conventions.
- Caution: don't over-index on the specific percentages (they come from one model/one harness) when deciding how much to trust this as a design checklist — use it as a hypothesis list to test against his own fleet logs, not as calibrated base rates.

## What this changes

If the claims hold, skill authors and platform builders get a concrete, ranked punch-list instead of vague "skills can be risky" folklore: separate mandatory requirements from examples/templates (addresses ~66% of functional failures), scope verification/exploration to task uncertainty rather than prescribing exhaustive workflows (addresses ~63% of efficiency regressions), and treat environment/path assumptions as guarded constraints (addresses ~30% of functional failures). This mainly benefits skill-marketplace operators (a triage signal for vetting submissions), agent-framework maintainers (a rationale for building compatibility-check and budget-aware loading features), and any team with a growing library of instruction/skill files who currently treats "add more guidance" as costless.

## Verdict

The contrastive-attribution method is a genuinely useful methodological contribution and the top-line category splits (TIF 68.8%, EP 62.6%) are large enough samples to trust directionally. But several load-bearing numbers rest on single-digit subcategory counts (APM=2, SMB=3, OWG=4), the entire dataset comes from one model/one harness with no replication, and the SkillTriage validation is scored against the same labels its own designers hand-assigned rather than an independent ground truth — so "automated attribution works" is asserted more confidently than the evidence (72.5-93.6% against self-produced labels, with errors clustering exactly at the fuzziest boundaries) supports. The failure taxonomy is a good checklist to borrow for auditing one's own skill files even if the precise percentages don't generalize. **trial** — the taxonomy and checklist are worth applying to your own SKILL.md/CLAUDE.md files as a self-audit tool, but don't treat the quantitative breakdown or SkillTriage's accuracy numbers as calibrated for a different model or framework.
