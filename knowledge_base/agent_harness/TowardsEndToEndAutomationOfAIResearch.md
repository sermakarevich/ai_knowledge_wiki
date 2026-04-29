# Towards End-to-End Automation of AI Research

**Paper:** [Towards end-to-end automation of AI research (Lu, Lu, Lange, Yamada et al., 2026)](https://doi.org/10.1038/s41586-026-10265-5)

## Human Readable TL;DR

Imagine a robot scientist that can come up with its own research ideas, run experiments, write up the results as a full paper, and even grade its own work -- all without human help. That is what this team built. They call it "The AI Scientist," and it managed to write a paper good enough to pass peer review at a respected machine learning workshop, the same process human researchers go through. It is like having a tireless lab assistant that can do the entire job from brainstorming to publication draft, though it still can not match the best human scientists on the hardest problems.

## TL;DR

This paper presents The AI Scientist, an end-to-end pipeline that autonomously performs ideation, literature search, experiment execution, result analysis, manuscript writing, and peer review using foundation models. Evaluated in template-based and template-free modes, the system produced a paper that passed peer review at an ICLR 2025 workshop (scores 6/7/6). An automated reviewer achieves human-level balanced accuracy (66--69%) on accept/reject decisions. Paper quality scales with both model capability and compute budget, suggesting continued improvement as models advance.

---

## Problem & Motivation

While AI has been applied to individual components of the scientific process -- hypothesis generation, literature review, coding experiments -- no system had autonomously navigated the entire research lifecycle from conception to a publication-ready manuscript. Closing this loop is critical because it could dramatically accelerate scientific discovery, reduce the cost of exploratory research, and enable continuous, open-ended scientific exploration without human bottlenecks.

---

## Main Original Ideas

1. **End-to-end scientific pipeline**: A fully integrated system covering ideation, novelty checking (via Semantic Scholar API), experiment execution, data visualization, manuscript generation in LaTeX, and automated peer review -- all without human modification.

2. **Template-free agentic tree search**: A parallelized tree search for experimentation with four structured stages (preliminary investigation, hyperparameter tuning, research agenda execution, ablation studies) and specialized node types (debug, hyperparameter, ablation, replication, aggregation). This enables open-ended discovery beyond fixed code templates.

3. **Automated Reviewer with ensemble meta-review**: An LLM-based reviewer using five independent reviews aggregated by a meta-review "area chair" agent, achieving performance comparable to human inter-reviewer agreement (balanced accuracy 66--69%, F1 0.62 vs human 0.49).

4. **Scaling laws for AI-generated research quality**: Demonstrated that paper quality improves with both the capability of the underlying foundation model (tracked across model release dates) and the amount of test-time compute allocated per paper, establishing predictable improvement trajectories.

5. **VLM-in-the-loop experimentation**: Integration of vision-language models (GPT-4o) to critique generated plots during experimentation and verify figure-caption alignment during manuscript preparation, improving research communication quality.

---

## Key Findings

| Metric | Result |
|--------|--------|
| Workshop peer review (best paper) | Scores: 6, 7, 6 (above acceptance threshold) |
| Workshop acceptance rate | 70% (ICLR 2025 ICBINB) |
| Automated Reviewer balanced accuracy (pre-cutoff) | **0.69 +/- 0.04** |
| Automated Reviewer balanced accuracy (post-cutoff) | **0.66 +/- 0.03** |
| Human reviewer balanced accuracy (NeurIPS 2021) | 0.66 |
| Automated Reviewer F1 (pre-cutoff) | **0.62** vs human 0.49 |
| Correlation: model release date vs paper quality | R = 0.517, P < 0.00001 |

- Paper quality consistently improves with newer foundation models across the timeline from GPT-4 through o3.
- Scaling the number of experimental tree-search nodes from 5 to 30 yields monotonic quality improvement.
- Data contamination analysis shows minimal effect: post-cutoff accuracy (66%) remains comparable to human reviewers.
- One of three submissions passed peer review; the other two did not, indicating the system is not yet consistent.
- Common failure modes: naive ideas, incorrect implementations, lack of methodological rigor, hallucinated citations, duplicated figures.
- The accepted paper notably reported a negative result, aligning well with the workshop's theme.

---

## Suggestions & Future Directions

1. **Extending beyond computational experiments**: Apply the same pipeline to domains with automated laboratories (e.g., chemistry, biology), where experiments can be conducted and data collected programmatically.
2. **Improving consistency and quality**: Current system passes workshop-level review but not main conference standards; improving idea depth, implementation correctness, and methodological rigor is essential.
3. **Addressing hallucinations and overconfidence**: LLM tendency to generate inaccurate citations and overconfident claims remains a key reliability barrier.
4. **Establishing community norms**: The scientific community needs clear standards for disclosure, evaluation, and ethical use of AI-generated research before such systems are deployed at scale.
5. **Safe open-ended exploration**: More research needed to ensure autonomous AI exploration aligns with human values and proceeds safely.
6. **Leveraging task-length scaling**: Recent evidence that AI task completion duration doubles every ~7 months suggests current implementation bottlenecks may resolve quickly.

---

## Authors & Institutions

Chris Lu (Sakana AI, FLAIR/University of Oxford), Cong Lu (Sakana AI, University of British Columbia, Vector Institute), Robert Tjarko Lange (Sakana AI), Yutaro Yamada (Sakana AI), Shengran Hu (Sakana AI, University of British Columbia, Vector Institute), Jakob Foerster (FLAIR/University of Oxford), David Ha (Sakana AI), Jeff Clune (University of British Columbia, Vector Institute)
