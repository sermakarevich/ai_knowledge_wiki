# Towards Automating Scientific Review with Google's Paper Assistant Tool

**Paper:** [Towards Automating Scientific Review with Google's Paper Assistant Tool (Jayaram, Tyler, Woodruff, Cortes, Matias, Mirrokni, Cohen-Addad, 2026)](https://arxiv.org/pdf/2606.28277)

## Human Readable TL;DR

Too many science papers, not enough human reviewers to check them -- especially since AI now helps write the papers too. Google built an AI reviewer called PAT (Paper Assistant Tool) that reads a full paper, splits it into logical chunks (intro, theory, experiments), spends more "thinking effort" on the hard chunks like proofs, and then merges everything into one report and double-checks itself with a web search before handing it back. Authors at two big computer science conferences got to run their paper through PAT before submitting, and most said it caught real bugs -- one researcher rewrote 7-8 pages after PAT found a fatal flaw in their algorithm. The paper also sketches four possible futures for AI in peer review, from "just a spell-checker for authors" to "AI reviews everything and a human just rubber-stamps it."

## TL;DR

PAT is an agentic LLM pipeline (built on Gemini Deep Think) for reviewing full scientific manuscripts: a segmenter agent splits the paper into overlapping thematic segments, an adaptive budgeter assigns Light/Medium/High "thinking" compute per segment, parallel Deep Review agents verify each segment with full-paper context, and a synthesis agent deduplicates findings and grounds them via search before producing the final report. On a filtered subset of the SPOT benchmark (26 retracted math/CS papers, 29 equation/proof errors), PAT hits 89.7% error-detection recall vs. 55.2% for zero-shot Gemini 3.1 Pro and 21.1% for the original SPOT SOTA -- a 34-point improvement over single-call inference scaling. Pilot deployments at STOC 2026 (n=124 respondents) and ICML 2026 (n=733 respondents) reviewed 4,700+ submissions pre-submission, with 90%+ of authors finding feedback helpful and 31% of ICML authors running new experiments as a result.

---

## Problem & Motivation

Peer review capacity is not scaling with the growth in submissions. Table 1 in the paper shows combined ICLR+ICML+NeurIPS submissions growing from ~17k (2020) to an estimated ~74k (2026, +63% YoY), partly fueled by AI-assisted paper writing (17.5%+ of CS arXiv abstracts already showed AI-generation evidence in 2024). Rigorous review of dense math/CS proofs takes human reviewers days; that labor cannot scale to match AI-accelerated paper generation. The authors argue the only way to resolve the tension is to also use AI to accelerate verification/review itself -- but naive approaches (single model call, or Pass@k with independent samples) are limited by context-window constraints on deep proofs and by precision collapse (more passes = more hallucinated "issues" to sift through).

---

## Main Original Ideas

1. **PAT's four-stage inference-scaling pipeline.** (1) A *segmenter* agent divides the manuscript into thematic, possibly overlapping/non-contiguous segments (intro, theory, methodology, experiments). (2) An *adaptive budgeting* stage assigns Light/Medium/High thinking-compute tracks per segment based on estimated complexity/density (e.g., High for proofs, Light for intro/conclusion). (3) *Deep Review* agents (powered by an advanced Gemini Deep Think variant) verify each segment in parallel, each given the full paper as context but focused on its assigned segment. (4) A *global synthesis* agent deduplicates critiques across segments, checks severity, and grounds claims via Google Search to catch hallucinated references (e.g., citing non-existent theorems/papers).
2. **Explicit rejection of Pass@k as a scaling strategy.** The paper argues Pass@k (independent repeated single-shot calls) increases recall but destroys precision (10 passes x 10 issues/pass could mean ~100 candidate issues for 1 real one) and does not solve context-budget contention, since independent calls may redundantly spend budget on the same section while leaving others unchecked. PAT's segment-level orchestration is positioned as the fix.
3. **A four-level (plus 3.5) taxonomy of AI roles in peer review**, explicitly modeled on SAE vehicle-autonomy levels: Role 1 (AI as author-side tool, pre-submission -- what PAT currently does), Role 2 (AI as reviewer-side tool, drafting critiques for a human reviewer), Role 3 / 3.5 (AI as an independent supporting reviewer, optionally with a subjective rating, shifting the human's role toward Area Chair), and Role 4 (full AI automation of peer review, potentially enabling a new "AIrXiv"-style vetted-preprint tier).
4. **A logic-aware LLM grader** for benchmark evaluation that scores an error report as correct if it is *logically equivalent* to the ground-truth error, rather than requiring exact keyword overlap (as the original SPOT grader does) -- explicitly changing the metric, so results are not directly comparable to the original SPOT paper.

---

## Key Findings

**Table 2 -- Verification accuracy, Math/CS equation-and-proof error subset of SPOT (26 papers, 29 errors):**

| Verification Method | Detection Accuracy |
|---|---|
| Original SPOT SOTA | 21.1% |
| Gemini 3.1 Pro (zero-shot) | 55.2% |
| **PAT (Gemini 3.1 Pro)** | **89.7%** |

- PAT gives a 34-point recall improvement over zero-shot single-call inference on the same underlying model.
- Qualitative example: on a dual Banach spaces paper, the zero-shot baseline accepted a false complete-contractivity claim at face value; PAT instead constructed a concrete counterexample exposing a fatal gap in the main theorem.
- The authors extrapolate: if arXiv ran even a single zero-shot LLM review pass on submissions, more than half of retracted-paper errors in their sample would have been caught pre-submission; with PAT, nearly all would have.

**Table 3 -- STOC vs. ICML pilot survey results:**

| Survey Question | STOC (n=124) | ICML (n=733) |
|---|---|---|
| Would use PAT again | 97% | 92.1% |
| Improved paper clarity/readability | 85.1% | 87.0% |
| Believes PAT has education value | 75.2% | 83.9% |
| Very/Mostly helpful | 92.7% | 90.7% |
| Feedback mostly/all grounded (factual) | 55.8% | 64.8% |
| Identified substantive theory gaps | 11.6% | **35.4%** |
| Ran new experiments as a result | -- | 31% |

- Over 4,700 submissions were reviewed across both pilots (STOC Nov 2025, math-rigor-only pipeline; ICML Jan 2026, generalized pipeline also covering experimental-design critique). Both ran on an advanced Gemini 2.5 Deep Think variant.
- ICML authors reported theory-gap detection at 3x the STOC rate (35.4% vs 11.6%) -- attributed to ICML's lower baseline mathematical rigor vs. a dedicated TCS theory venue.
- Qualitative highlights: one team added 7-8 pages of new technical content after PAT found "an embarrassingly simple bug that evaded us for months"; a Vijay Vazirani (UC Irvine) and Hung Le (UMass Amherst) quote both cite PAT catching fatal/significant errors pre-submission.
- Reported failure modes: date hallucinations / stale knowledge cutoffs, PDF parsing issues (both since mitigated via better search tooling and parsing), and false-positive claims that a correct proof is wrong (an open, inherent LLM-reasoning limitation the authors say they are still addressing).
- Contextual stat: a Pangram study found 21% of ICLR 2026 reviews were fully AI-generated despite being against conference policy -- cited as evidence that AI is already informally entering Role 2/3 whether or not venues have a policy for it.

---

## Suggestions & Future Directions

1. Continue improving PAT's reasoning to reduce false "this proof is wrong" claims -- flagged as the hardest remaining failure mode since it stems from core LLM reasoning limits, not tooling.
2. Anticipate a gradual industry shift from Role 1/2 (author/reviewer tool) toward Role 3 (AI as an independent supporting reviewer under human Area Chair supervision) as agent reliability improves.
3. Long-term, consider Role 4 constructs such as an "AIrXiv" -- a repository tier where papers undergo multiple automated review/rebuttal rounds and earn a confidence rating, sitting between a raw preprint and a fully human-reviewed venue.
4. Explore an "AI for Students" role -- using PAT-like agents as technical mentors/tutors rather than only as reviewers.
5. Open challenges the authors explicitly flag: accountability (where does algorithmic assessment end and human judgment begin), guarding against reviewer deskilling/complacency, equitable compute access for review tools, adversarial gaming of review agents by authors, and reduced diversity of opinion if AI reviewers converge on centralized viewpoints (especially risky for humanities-style venues where debate itself is the point).
6. Note on baseline for Role 4 ambitions: the paper cites the NeurIPS 2021 consistency experiment (23% acceptance-decision inconsistency between independent committees, vs. ~35% expected from pure chance given the 22.7% acceptance rate) as evidence that human review noise is already closer to random than perfect -- used to argue AI review need not be perfect to be competitive, only reliable enough.

---

## Authors & Institutions

Rajesh Jayaram (Google Research, USA), Drew Tyler (Google Research, USA), David Woodruff (Google Research & Carnegie Mellon University, USA), Corinna Cortes (Google Research, USA), Yossi Matias (Google Research, USA), Vahab Mirrokni (Google Research, USA), Vincent Cohen-Addad (Google Research, USA).
