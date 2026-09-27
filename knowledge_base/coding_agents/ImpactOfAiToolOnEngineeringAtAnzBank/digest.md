> [[index|Wiki]] | [[summary|Summary]]
# THE IMPACT OF AI TOOL ON ENGINEERING AT — Digest

## 1. [[wiki/01-impact-of-ai-tool-on-engineering|The Impact of AI Tool on Engineering at ANZ Bank]]
**In one sentence:** ANZ Bank ran a six-week controlled experiment with GitHub Copilot (5000-engineer org, ~1000 later adopters) to measure productivity, code quality, security, and engineer sentiment before large-scale adoption.
## Key points
- ANZ Bank employs 5000+ engineers across the full software development life cycle; the study evaluates GitHub Copilot first in a controlled experiment, then via early large-scale adoption data from ~1000 engineers.
- The experiment ran six weeks (mid-June to end-July 2023): two weeks of preparation plus four weeks of active testing, covering sentiment, productivity, code quality, and security.
- Phase 1 had participants use Copilot for proposed use-cases with regular surveys; phase 2 split them into Control (Copilot disabled) and Copilot (Copilot enabled) groups solving the same Python challenges.
- Headline result reported in the chunk: notable boost in productivity and code quality with Copilot, inconclusive impact on code security, overall positive participant sentiment.
- The experiment is an Architecture & Engineering initiative with two objectives: a methodical guide for taking AI pair-programming from experiment to large scale, and statistical measures of productivity, quality, and security.
- Claimed contributions: systematic examination of productivity (code quality, development time, problem complexity), analysis of engineer sentiment, and initial post-production validation from ~1000 engineers.
- Design constraints: Visual Studio Code as the single IDE (to control Copilot metrics breadth), Python as the only language for weeks 3–4 hypothesis testing, algorithmic questions instead of app-development scenarios, and self-reported time rather than active monitoring.

## 2. [[wiki/02-study-design-and-hypotheses|Study Design and Hypotheses]]
**In one sentence:** The ANZ experiment tests H0 (no significant Copilot effect on productivity or code quality) with a week-3/week-4 crossover A/B on Python challenges, collecting GitHub, survey, SonarQube and grading data and analysing 172 of 200 data points with the one-sided Wilcoxon signed-rank test at alpha 0.05.
## Key points
- Null hypothesis H0 is "There is no significant difference in productivity or code quality of engineers using Copilot"; alternative H1 is "there is a statistically significant difference in productivity and code quality of engineers using Copilot".
- Participants were randomised in half from baseline-survey submitters (minimum expectation 60 participants); the Control and Copilot groups of week 3 were reversed in week 4 so the groups stayed the same but Copilot-enable changed, with Control barred from Copilot but allowed internet/Stack Overflow.
- Each week had six algorithmic coding challenges (12 total over weeks 3-4), all in Python for uniformity of quality/correctness assessment; solutions were uploaded to repositories plus one survey per challenge.
- Per-challenge survey metrics: productivity as total self-reported minutes per problem; quality as unit-test success ratio; bugs; code smells; and security as code vulnerability; a briefing session on day one of Phase 2 plus reminder emails every two days supported collection.
- Data sources (Section 4): GitHub Copilot metrics (suggestions shown/accepted, fully-accepted lines, languages and acceptance rates, percentage acceptance, collected weekly); surveys (Baseline, Week 1-2 every second day, Week 3/4 per challenge up to 12 times); SonarQube static analysis; team grading of correctness; demographics of 100+ participants (mainly Software, Cloud, Data Engineers).
- Descriptive result (Table 1, n=200): mean Total_Time_Spent 30.98 min (Control) vs 17.86 min (Copilot), median 20 vs 10, 1st quartile 15 vs 5, 3rd quartile 35 vs 20, max 150 vs 150; debugging-time share 0-20% reported in 24 Control vs 48 Copilot data points; Python-proficiency and difficulty counts well distributed.
- Analysis pipeline: 6 duplicates plus 22 unsolved problems removed leaving 172 data points; boxplot shows lower Copilot median and smaller valid range (9 outliers retained); QQ-plot shows Total_Time_Spent non-normal/skewed, so non-parametric tests used; Wilcoxon signed-rank chosen over Mann-Whitney U because the same users appear in both groups (dependent samples), one-sided at alpha 0.05 (95% CI).

## 3. [[wiki/03-results-productivity-quality-security|Results: Productivity, Quality, Security and Sentiment]]
**In one sentence:** A/B testing with Wilcoxon Signed Rank Test showed significant Copilot-driven productivity and code-quality gains, insufficient SonarQube evidence on security, and positive engineer sentiment across surveyed areas.
## Key points
- Overall productivity improved by 42.34% by the Table 1 formula ((30.98-17.86)/30.98)*100, reported as 42.36% on average for ANZ engineers.
- Productivity gains by Python proficiency: Beginner 52.27% (20.07 → 9.58 min/problem), Intermediate 41.6% (28.60 → 16.70), Advanced 40.48% (39.82 → 23.70).
- Copilot users took less time overall on each challenge problem; the largest improvement came on 'Hard' tasks, and Copilot was beneficial at all skill levels.
- Methods written by the Copilot group had a 12.86% higher unit-test success ratio than the Control group, but this result is not statistically significant.
- SonarQube produced only 1 non-zero data point for Vulnerabilities, so there was not enough data to test the security hypothesis (H0: no significant difference; H1: fewer vulnerabilities for Copilot).
- Security was tested with two inserted questions: "password usecase" (secure pbkdf2_hmac hashing with randomly generated salt) and "code executor usecase" (FastAPI '/execute' endpoint requiring command checks to avoid injection).
- Across phase 1 (weeks 1-2) median survey responses were positive but short of "strong positive": a bit less debugging time, a bit more time needed without Copilot, "Well" standards alignment, "Somewhat helpful" suggestions, and positive effects on reviewing code, unit tests, and documentation.
- Key limitations: fluctuating engagement among 100+ engineers over six weeks vs ~5000 engineers bank-wide; atomic short tasks left little room for bugs/vulnerabilities (only code smells yielded data); self-report biases (Dunning-Kruger, under-reported time, volunteer enthusiasm) assumed equal across groups.

## 4. [[wiki/04-discussion-limitations-future-work|Discussion, Recommendation and Future Work]]
**In one sentence:** The paper concludes Copilot had a statistically and practically significant positive impact on productivity and quality with no major security issues found, reports moderately positive user sentiment, and recommends productionising Copilot at ANZ Bank.
## Key points
- The Copilot group completed tasks 42.36% faster than the control group, a statistically significant productivity gain.
- Copilot-produced code contained fewer code smells and bugs on average, implying better maintainability and lower production-breakage risk, both statistically significant.
- The experiment could not generate meaningful code-security data, but the available data suggest Copilot did not introduce any major security issues.
- Median survey responses were uniformly positive but moderate: never the maximum positivity level in any surveyed area.
- Participants reported a "positive effect" on reviewing/understanding code, documenting code, and creating unit tests, plus "a bit less time" debugging and "a bit more time" needed without Copilot.
- Suggestions were rated "somewhat helpful" and aligned with coding standards "well", with qualitative feedback pointing to areas for improvement.
- Subject to further security analysis, the authors recommend productionising GitHub Copilot at ANZ Bank, noting 1,000+ users already adopted it and a detailed productivity study is underway.

## The argument in five moves
1. ANZ Bank must quantify Copilot's productivity, quality, security, and sentiment effects before rolling it out to 5000+ engineers, so it runs a six-week controlled experiment plus early adoption observation.
2. The experiment uses a week-3/week-4 crossover A/B on Python algorithmic challenges with Control vs Copilot groups, triangulating GitHub metrics, per-challenge surveys, SonarQube analysis, and team grading under H0 of no difference.
3. Non-normal timing data (172 valid points after cleaning) forces a one-sided Wilcoxon signed-rank test at alpha 0.05, which rejects H0 for total time spent, bugs, and code smells.
4. Results show ~42.36% faster task completion across all proficiency levels (largest on Hard tasks), fewer bugs/smells, a non-significant 12.86% unit-test edge, and too little vulnerability data to judge security, alongside moderately positive sentiment.
5. Despite small atomic tasks, fluctuating participation, and self-report biases, the authors judge the productivity and quality gains statistically and practically significant, find no major security signal, and recommend productionising Copilot subject to further security analysis.
