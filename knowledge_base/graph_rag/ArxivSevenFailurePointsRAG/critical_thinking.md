> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Seven Failure Points When Engineering a Retrieval Augmented Generation System

## Claims vs. evidence

**Claim 1: RAG systems fail at exactly these seven identifiable points.** Evidence is *suggestive, not strong*: the seven points are derived by manual inspection of discrepancies across three case studies, one of which (BioASQ) had only 40 answers manually inspected out of 1,000 generated. There is no inter-rater reliability check, no claim about relative frequency of each failure point, and no argument that the taxonomy is exhaustive — it is presented as "what we observed," not "what is possible." As a starting checklist it is well-grounded; as a complete or ranked taxonomy it is not proven.

**Claim 2: automated evaluation (OpenEvals) is more pessimistic than human raters.** Evidence is *weak-to-suggestive*: based on a 40-answer manual review in one domain (biomedical), with an explicitly acknowledged confound — the human reviewers were not domain experts, so the LLM may simply have known more than the raters. This is a narrow, single-domain, small-sample observation presented with appropriate hedging by the authors themselves.

**Claim 3: larger context windows improve accuracy (8K vs 4K), contradicting prior "lost in the middle" findings.** Evidence is *weak*: this is reported as a lesson from AI Tutor with no numbers, no controlled comparison methodology described, and no discussion of why it differs from the GPT-3.5 "lost in the middle" literature it explicitly contradicts. It reads as an anecdotal field observation, not a validated result.

**Claim 4: open-source embedding models perform as well as closed-source alternatives (on small text).** Evidence is *weak*: reported as a case-study observation (BioASQ, AI Tutor) without a specific benchmark, models named, or metrics reported.

## Genuinely new vs. repackaged

The individual pipeline stages (chunking, embedding, retrieval, re-ranking, consolidation, reading) were already standard RAG architecture by early 2024, not new to this paper. The genuinely new contribution is the **failure taxonomy itself** — naming and localizing seven distinct failure modes to specific pipeline stages, from real deployments rather than from a benchmark leaderboard. Prior RAG evaluation work (e.g. benchmarking papers the authors cite) measured aggregate quality metrics; this paper instead asks "when it's wrong, which component broke," which is a genuinely different and complementary lens aimed at practitioners rather than at model comparison.

## Weaknesses and blind spots

- **No frequency or severity data.** The paper never reports how often each failure point occurs relative to the others, so a reader cannot prioritize which failure mode to guard against first for their own system.
- **No architectural comparisons.** All three case studies use broadly similar pipelines (chunk → embed → retrieve → consolidate → read); the paper doesn't compare against alternative architectures (e.g. graph-based retrieval, hybrid sparse+dense retrieval) that might avoid some of these failure points structurally rather than through calibration.
- **Confidentiality limits reproducibility.** Two of the three case studies (Cognitive Reviewer, AI Tutor) — the two "real" user-facing deployments the taxonomy leans on most — have no public data, scripts, or examples; only the BioASQ experiment is reproducible (figshare link provided).
- **The lessons (Table 2) mix strong and anecdotal claims without distinguishing them.** Nine lessons are presented at similar confidence levels in the same table, but they range from a structural observation (RAG needs continuous recalibration) to single-anecdote field notes (context-window size effect) — the paper does not flag this gradient itself.
- **Silent on cost.** No discussion of the compute/API cost implications of GPT-4-based pipelines at the scale used (15,000 documents, 1,000 questions), which practitioners considering the paper's approach would need.

## Applicability

This applies directly to teams building a document-Q&A or internal-knowledge chatbot with a standard chunk-embed-retrieve-generate pipeline, especially where: documents are heterogeneous (PDFs, video, HTML), questions are open-ended rather than from a fixed FAQ, and no pre-existing labelled Q&A data exists to validate against before launch — which describes most real internal-knowledge RAG deployments. It is less directly applicable to teams already using graph-based retrieval (GraphRAG-style systems), since the failure points are framed against a flat-chunk vector-retrieval pipeline and some (e.g. Missed Top Ranked, Not in Context) map differently onto a graph traversal design.

**Relevance to my work** — 2-4 bullets on what this means for Sergii's contexts (AI/ML engineering, agentic systems, Elisity data platform):
- **Trial**: use the seven-point taxonomy as a debugging/failure-triage checklist for any RAG feature built on top of Athena or internal documentation — when an answer is wrong, first localize which stage broke before tuning prompts blindly.
- **Adopt** the framing that RAG validation is only feasible during operation — bake monitoring/logging into any production RAG feature from day one rather than treating a pre-launch test pass as sufficient.
- **Watch**: the chunking/embedding and testing-and-monitoring research gaps this paper flags are still active areas (2024→2026); newer GraphRAG and evaluation-framework papers already in this KB partially address them — cross-reference before assuming this paper's open questions are still fully open.

## What this changes

If the claims hold as a practical checklist (which the qualitative but concrete case-study evidence supports for the failure taxonomy itself, even if the supporting lessons are weaker): teams get a shared vocabulary for RAG bugs ("this is a Missed-Top-Ranked issue, raise K" vs. "this is a Not-Extracted issue, reduce context noise") instead of generic "the AI is wrong" reports, which speeds up debugging and makes RAG quality issues addressable by the right specialist (retrieval engineer vs. prompt engineer vs. data engineer). It does not change the underlying hard problems — no-ground-truth testing and continuous calibration remain unsolved — it just names them clearly enough to plan around.

## Verdict

This is a well-scoped, honestly-framed practitioner report: it does not overclaim rigor it doesn't have, explicitly labels itself an experience report, and the central failure taxonomy is intuitive, pipeline-grounded, and immediately reusable even without frequency data. The supporting "lessons learned" (Table 2) are weaker anecdotal field notes that should not be treated as validated findings. Overall verdict: **trial** — adopt the seven-failure-point vocabulary and the "validation only during operation" framing for any RAG system being built or debugged, but do not cite this paper's specific numeric claims (context-window size, embedding comparisons) as benchmark evidence.
