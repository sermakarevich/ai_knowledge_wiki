---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: THE IMPACT OF AI TOOL ON ENGINEERING AT

### Q1. What organisation, tool, timeframe, and four research aims defined the ANZ Bank experiment?

> [!tip]- Answer
> ANZ Bank (5000+ engineers) ran a six-week experiment (mid-June to end-July 2023: two weeks preparation plus four weeks active testing) on GitHub Copilot, followed by early adoption data from ~1000 engineers. The four aims asked whether developers feel positive/empowered, how much faster they work, whether output is better, and whether suggested code is secure. See [[wiki/01-impact-of-ai-tool-on-engineering|The Impact of AI Tool on Engineering at ANZ Bank]].

### Q2. What design constraints did the experiment impose, and what did related work suggest about Copilot?

> [!tip]- Answer
> The study restricted weeks 3–4 hypothesis testing to VS Code and Python, used short algorithmic questions rather than app-development scenarios, and relied on self-reported time instead of active monitoring. Related work reported a 55.8% speedup (Microsoft, 95 engineers), noted Copilot generates the most lines but also the most deletions, and warned its errors are easier to fix for experts but risky for novices. See [[wiki/01-impact-of-ai-tool-on-engineering|The Impact of AI Tool on Engineering at ANZ Bank]].

### Q3. What were H0/H1, and how did the week-3/week-4 crossover A/B test work?

> [!tip]- Answer
> H0 stated no significant difference in productivity or code quality with Copilot; H1 stated a statistically significant difference. Participants were randomised in half from baseline-survey submitters, then the Control and Copilot groups of week 3 were reversed in week 4 so the same users experienced both conditions across 12 Python algorithmic challenges. See [[wiki/02-study-design-and-hypotheses|Study Design and Hypotheses]].

### Q4. Which four data sources fed the analysis, and why was the one-sided Wilcoxon signed-rank test chosen?

> [!tip]- Answer
> The four sources were weekly GitHub Copilot metrics (suggestions shown/accepted, acceptance rates), surveys (baseline, every-second-day in weeks 1–2, per-challenge in weeks 3–4), SonarQube static analysis, and team grading of correctness. After removing 6 duplicates and 22 unsolved problems (200 → 172 points), the skewed non-normal timing data required a non-parametric test, and Wilcoxon signed-rank was chosen over Mann-Whitney U because the same users appeared in both groups. See [[wiki/02-study-design-and-hypotheses|Study Design and Hypotheses]].

### Q5. What productivity and code-quality results did the Wilcoxon test support?

> [!tip]- Answer
> The Copilot group completed tasks ~42.36% faster on average (mean 30.98 → 17.86 min, median 20 → 10), a statistically significant gain largest for Beginners (52.27%) and on Hard tasks, with H0 rejected for total time, bugs, and code smells. Unit-test success was 12.86% higher for Copilot code but not statistically significant (p = 0.060). See [[wiki/03-results-productivity-quality-security|Results: Productivity, Quality, Security and Sentiment]].

### Q6. What did the study find on code security and engineer sentiment?

> [!tip]- Answer
> SonarQube produced only one non-zero vulnerability data point, so the security hypothesis could not be tested despite the two inserted probes (pbkdf2_hmac password hashing and the FastAPI '/execute' injection check). Phase 1 median sentiment was positive but never maximally so: a bit less debugging time, somewhat helpful suggestions aligning well with standards, and positive effects on reviewing code, unit tests, and documentation. See [[wiki/03-results-productivity-quality-security|Results: Productivity, Quality, Security and Sentiment]].

### Q7. Given significant productivity and quality gains but inconclusive security evidence, should ANZ Bank productionise Copilot?

> [!tip]- Answer
> Yes, with a caveat: the authors recommend productionising Copilot subject to further security analysis, judging the ~42% speedup and significant bug/smell reductions statistically and practically significant with no major security signal observed. This balances the moderate-but-uniform positive sentiment and 1000+ existing adopters against limits like atomic tasks, fluctuating participation, and self-report biases. See [[wiki/04-discussion-limitations-future-work|Discussion, Recommendation and Future Work]].
