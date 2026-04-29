# What 81,000 People Told Us About the Economics of AI

**Paper:** [What 81,000 People Told Us About the Economics of AI (Massenkoff & Huang, 2026)](https://www.anthropic.com/research/81k-economics)

## Human Readable TL;DR

Anthropic asked 81,000 people who use Claude what they think about AI and their jobs. About one in five said they worry about losing their job to AI -- and the more AI-like their job already is, the more scared they feel. Most people said AI made them much more productive, and most of that benefit stayed with the worker rather than going to their boss. But weirdly, the people whose work got faster the most were *also* the ones most worried -- like someone who can type 10x faster suddenly wondering if companies will need 10x fewer typists.

## TL;DR

This Anthropic report analyzes open-ended survey responses from 80,508 Claude users to connect self-reported economic concerns with the company's existing "Observed Exposure" metric (share of job tasks performed by Claude). Key results: (1) perceived job threat scales with observed AI exposure (+1.3 pp per 10 pp increase in exposure); (2) mean self-reported productivity gain is 5.1/7; (3) scope expansion (new capabilities) dominates speed gains 48% vs 40%; (4) a U-shaped relationship links speedup magnitude to job-threat anxiety. All variables are inferred from free-text using Claude-powered classifiers.

---

## Problem & Motivation

Prior Anthropic Economic Index work quantified *what* Claude does across occupations, but lacked workers' own perspectives. This study bridges that gap by pairing behavioral usage data with 81k qualitative survey responses, testing whether workers' subjective threat perceptions align with objectively measured AI exposure -- and surfacing where productivity gains actually flow.

---

## Main Original Ideas

1. **Observed Exposure as a Threat Predictor** -- Anthropic's existing metric (fraction of a job's tasks Claude performs) is shown to correlate with workers' self-reported displacement anxiety (r linear: +1.3 pp per 10 pp exposure), validating the metric as behaviorally meaningful from the workers' perspective.

2. **LLM-Powered Qualitative Coding at Scale** -- Rather than structured questionnaires, the study uses Claude itself as a classifier to extract occupation, career stage, productivity dimension (scope/speed/quality/cost), benefit recipient, and job-threat sentiment from free-form interview transcripts. Verbatim prompt templates are published in the appendix.

3. **U-Shaped Speedup--Anxiety Relationship** -- Job-threat concern is elevated both for workers AI *slows down* (creative workers frustrated by rigidity) and for those experiencing the *largest* speedups (who rationally infer their role may shrink). Workers with moderate speedups show the lowest anxiety.

4. **Scope Expansion as the Dominant Productivity Channel** -- 48% of users describing productivity effects cite scope (doing tasks previously out of reach), outpacing speed (40%), quality, and cost savings. This reframes AI productivity gains as capability extension, not just efficiency.

5. **Surplus Distribution Self-Report** -- In a quarter of interviews where recipients were named, most benefits were attributed to workers themselves (faster tasks, freed time), but 10% reported employers capturing gains via increased workload demands. This pattern is sharper for early-career workers (60% self-benefit) vs. senior workers (80%).

---

## Key Findings

| Metric | Value |
|--------|-------|
| Survey respondents | 80,508 |
| Respondents expressing job displacement concern | ~20% (1 in 5) |
| Increase in perceived threat per +10 pp exposure | +1.3 pp |
| Top-quartile vs. bottom-quartile exposure concern ratio | 3× |
| Mean productivity rating (1--7 scale) | 5.1 ("substantially more productive") |
| Respondents reporting negative/neutral impact | 3% |
| Respondents with unclear productivity indication | 42% |
| Scope as primary productivity type | 48% |
| Speed as primary productivity type | 40% |
| Early-career workers citing personal benefit | 60% |
| Senior workers citing personal benefit | 80% |
| Employers/clients capturing gains | 10% of those naming a recipient |

**By occupation (productivity, high → low):**
- Management (mostly solopreneurs/entrepreneurs)
- Computer & math (software developers)
- Legal & scientific (mildest improvements)

**By wage quartile:** Both highest- and lowest-paid quartiles report the largest productivity gains; the lowest-wage gains often come from AI enabling side projects (e-commerce, app development) rather than primary job tasks.

**Career stage:** Early-career workers are significantly more likely to express displacement anxiety than senior professionals; inferred from contextual clues (homework mentions, hiring involvement) for ~50% of respondents.

---

## Suggestions & Future Directions

1. **Replicate with structured surveys** -- Open-ended responses only capture voluntarily mentioned topics; findings should be confirmed with direct questions about occupation, career stage, and displacement concern.
2. **Include enterprise users** -- The sample is limited to personal Claude.ai accounts; enterprise users likely show different surplus-distribution patterns (more value accruing to employers).
3. **Track longitudinal change** -- A single cross-sectional snapshot cannot distinguish adaptation from sustained anxiety; repeated surveys over time would clarify whether concerns resolve as workers adjust.
4. **Validate classifier accuracy** -- The Claude-powered inference pipeline was applied at scale but only partially validated (robustness check on the 11% who explicitly stated their occupation); formal accuracy audits are needed.
5. **Extend to non-users** -- Survey respondents are active Claude users; understanding displaced or non-adopting workers requires different sampling strategies.

---

## Authors & Institutions

**Maxim Massenkoff** (Anthropic, led analysis), **Saffron Huang** (Anthropic, led interview project)

Additional contributors: Zoe Hitzig, Eva Lyubich (methodological guidance), Keir Bradwell, Rebecca Hiscott (editorial), Grace Yun, AJ Alt, Thomas Millar (Anthropic Interviewer implementation), Chelsea Larsson, Jane Leibrock, Matt Gallivan (survey design), Theodore Sumers (data infrastructure), Peter McCrory, Deep Ganguli, Jack Clark (direction).
