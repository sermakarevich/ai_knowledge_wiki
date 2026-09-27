# Towards Automating Scientific Review with Google's Paper Assistant Tool

**Paper:** [Towards Automating Scientific Review with Google's Paper Assistant Tool (Jayaram et al., 2026)](https://arxiv.org/abs/2606.28277)

## Human Readable TL;DR

Science is producing research papers faster than expert humans can review them -- AI is actually making the problem worse by accelerating output. This paper describes a tool Google built to act like a very thorough reviewer: it reads your paper, checks your math, looks for logical holes, and suggests improvements. They tested it at two major computer science conferences and the vast majority of authors found it genuinely useful -- some even caught serious bugs they'd missed for months.

## TL;DR

PAT (Paper Assistant Tool) is an agentic inference-scaling framework that performs comprehensive scientific review of manuscripts, specializing in detecting mathematical and logical errors. A four-stage pipeline (segmentation → adaptive budgeting → deep review → synthesis) achieves 89.7% recall on the SPOT benchmark vs. 55.2% for zero-shot Gemini -- a 34% improvement. Pilot programs across STOC 2026 (124 respondents) and ICML 2026 (733 respondents) showed 90%+ satisfaction, with 31% of ICML respondents running new experiments based on PAT feedback.

---

## Problem & Motivation

Peer review capacity has not scaled with submission volume. Combined ICLR/ICML/NeurIPS submissions grew from 17,051 in 2020 to an estimated 73,883 in 2026 (+62.9% YoY). AI-accelerated research output is the primary driver -- the same technology that needs reviewing is also producing more work to review. The result is reviewer overload, declining review quality, and critical errors slipping through. A scalable AI-assisted review layer is needed to maintain scientific rigor without requiring proportional growth in expert human labor.

---

## Main Original Ideas

1. **Four-Stage Inference-Scaling Pipeline** -- PAT segments manuscripts into logical components, assigns computational budgets per section based on complexity (light/medium/high thinking), runs specialized deep-review agents with full paper context, then synthesizes findings with deduplication and hallucination-checking via Google Search. This outperforms both zero-shot and Pass@k scaling strategies for error detection.

2. **Taxonomy of AI Roles in Peer Review** -- A principled four-level framework: Role 1 (AI as author tool, current pilots), Role 2 (AI as reviewer aid), Role 3 (AI as supporting reviewer producing full assessments, humans as area chairs), Role 3.5 (Role 3 + subjective ratings), and Role 4 (full automation). Each level transfers increasing decision authority from humans to AI with distinct accountability and bias risks.

3. **Adaptive Computational Budgeting** -- Rather than uniform inference effort across a paper, PAT dynamically allocates more compute to theoretically dense sections and less to introductory material. This addresses the fundamental mismatch between where errors concentrate and where uniform sampling wastes compute.

4. **AIrXiv Concept** -- Proposed automated preprint repository with interactive rebuttals and staged evaluation as a lower-stakes environment for transitioning toward Role 4 automation, enabling confidence calibration before deploying in high-stakes conference review.

---

## Key Findings

| Metric | STOC (n=124) | ICML (n=733) |
|--------|-------------|-------------|
| Would use PAT again | **97.0%** | **92.1%** |
| Very/mostly helpful | 92.7% | 90.7% |
| Improved clarity/readability | 85.1% | 87.0% |
| Educational value | 75.2% | 83.9% |
| Feedback grounded | 55.8% | 64.8% |
| Identified theory gaps | 11.6% | **35.4%** |
| Ran new experiments based on feedback | -- | **31.0%** |

**SPOT Benchmark (math/CS equation-proof errors, 26 papers):**

| System | Recall |
|--------|--------|
| Original SOTA | 21.1% |
| Gemini 3.1 Pro zero-shot | 55.2% |
| **PAT** | **89.7%** |

- Detected invalid proof in dual Banach spaces paper via counterexample construction
- Caught "critical bug in a way we were applying a tool...evaded us for months" (ICML author quote)
- Distinguished professor Vijay Vazirani: "pointed out a subtle though fatal bug in my algorithm -- simply mind-blowing"
- Mathematical error types detected: missing absolute values, reversed inequalities, overloaded notation, invalid proof steps

---

## Suggestions & Future Directions

1. Improve reasoning to reduce false positives (claiming correct proofs are wrong) -- a persistent LLM failure mode
2. Improve PDF parsing and date/citation grounding to reduce hallucinations
3. Gradual transition from Role 1 toward Role 3 with validation against human reviewer baselines
4. Deploy AIrXiv as a testbed for Role 3.5/4 systems before high-stakes conference use
5. Expand beyond mathematics/computer science to other scientific domains
6. Develop clear algorithmic accountability frameworks distinguishing AI assessment from human judgment
7. Address cognitive complacency risk: human reviewers relying on PAT without verification
8. Ensure equitable infrastructure access so large institutions don't gain unfair review advantages
9. Apply PAT capabilities to scientific education as an "AI for Students" mentorship system

---

## Authors & Institutions

Rajesh Jayaram (Google Research), Drew Tyler (Google Research), David Woodruff (Google Research / Carnegie Mellon University), Corinna Cortes (Google Research), Yossi Matias (Google Research), Vahab Mirrokni (Google Research), Vincent Cohen-Addad (Google Research)
