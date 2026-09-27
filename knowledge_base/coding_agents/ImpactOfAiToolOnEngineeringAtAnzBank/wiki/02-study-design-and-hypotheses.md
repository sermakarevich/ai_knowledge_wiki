> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Study Design and Hypotheses
**In one sentence:** The ANZ experiment tests H0 (no significant Copilot effect on productivity or code quality) with a week-3/week-4 crossover A/B on Python challenges, collecting GitHub, survey, SonarQube and grading data and analysing 172 of 200 data points with the one-sided Wilcoxon signed-rank test at alpha 0.05.
## Key points
- Null hypothesis H0 is "There is no significant difference in productivity or code quality of engineers using Copilot"; alternative H1 is "there is a statistically significant difference in productivity and code quality of engineers using Copilot".
- Participants were randomised in half from baseline-survey submitters (minimum expectation 60 participants); the Control and Copilot groups of week 3 were reversed in week 4 so the groups stayed the same but Copilot-enable changed, with Control barred from Copilot but allowed internet/Stack Overflow.
- Each week had six algorithmic coding challenges (12 total over weeks 3-4), all in Python for uniformity of quality/correctness assessment; solutions were uploaded to repositories plus one survey per challenge.
- Per-challenge survey metrics: productivity as total self-reported minutes per problem; quality as unit-test success ratio; bugs; code smells; and security as code vulnerability; a briefing session on day one of Phase 2 plus reminder emails every two days supported collection.
- Data sources (Section 4): GitHub Copilot metrics (suggestions shown/accepted, fully-accepted lines, languages and acceptance rates, percentage acceptance, collected weekly); surveys (Baseline, Week 1-2 every second day, Week 3/4 per challenge up to 12 times); SonarQube static analysis; team grading of correctness; demographics of 100+ participants (mainly Software, Cloud, Data Engineers).
- Descriptive result (Table 1, n=200): mean Total_Time_Spent 30.98 min (Control) vs 17.86 min (Copilot), median 20 vs 10, 1st quartile 15 vs 5, 3rd quartile 35 vs 20, max 150 vs 150; debugging-time share 0-20% reported in 24 Control vs 48 Copilot data points; Python-proficiency and difficulty counts well distributed.
- Analysis pipeline: 6 duplicates plus 22 unsolved problems removed leaving 172 data points; boxplot shows lower Copilot median and smaller valid range (9 outliers retained); QQ-plot shows Total_Time_Spent non-normal/skewed, so non-parametric tests used; Wilcoxon signed-rank chosen over Mann-Whitney U because the same users appear in both groups (dependent samples), one-sided at alpha 0.05 (95% CI).
---
## Hypotheses
**Covers:** H0/H1 statement

- H0 = "There is no significant difference in productivity or code quality of engineers using Copilot"
- H1 = "there is a statistically significant difference in productivity and code quality of engineers using Copilot"

## Experiment design
**Covers:** Group randomisation, crossover, challenges, per-challenge metrics

- "Participants were divided randomly in half based on employees who had submitted the baseline survey in the preparation stage with an initial minimum expectation of 60 participants."
- "The Control and Copilot group in week 3 were reversed in week 4 so groups remained the same but their ability to enable the copilot extension was changed."
- "To note, the Control group were not permitted to use Copilot but other tools currently available to developers such as searching the internet or using Stack Overflow were allowed."
- "Six algorithmic coding challenges were provided to solve each week... 12 questions in total over week 3 and 4" with the constraint "all engineers were asked to use only Python to code, for uniformity in assessing code quality and interpretation of code correctness, ensuring rigor in statistical evaluation."
- On completion, participants "uploaded their solutions to their repositories, as well as submitted a survey for each challenge" collecting: Productivity — "Total time spent solving a problem (minutes, self-reported)"; Quality — "Unit test success ratio"; Bugs — "Code smells" (chunk lists "Code smells" under Bugs heading); Security — "Code vulnerability".
- "A briefing session was organised on the first day of Phase 2" plus "Emails were sent every two days to remind participants to submit surveys."

## Data collection approach
**Covers:** Section 4, 4.1 GitHub Copilot, 4.2 Surveys, 4.3 Static Code Analysis, 4.4 Grading of correctness, 4.5 Demographics

- Purpose per chunk: "To analyse data on developer productivity, quality of work performed and sentiment in using Copilot, we decided to use four sources to obtain metrics".
- 4.1 GitHub Copilot: "statistical information relating to usage of the tool and how useful Copilot was in terms of predicting code written", collected "at the end of each week", tracking: number of times a suggestion was provided; accepted; fully accepted as all suggested lines ("partial acceptance not included"); languages used and acceptance rates; percentage acceptance rate.
- 4.2 Surveys: "'Baseline Survey' was to be completed prior to initiation of phase 1, during the preparation stage"; "'Week 1-2 Survey' was to be completed every second day during phase 1"; "'Week 3 Survey' and 'Week 4 Survey' was to be completed each time a participant completed a challenge question (up to 12 times in total)".
- 4.3 Static code analysis: "performed using SonarQube to capture metrics related to code quality and security vulnerabilities".
- 4.4 Grading of correctness: "Solutions submitted by each participant were graded by the ANZ Copilot Experiment Team according to their correctness".
- 4.5 Demographics: "over 100 participants" with roles mainly "1. Software Engineers 2. Cloud Engineers 3. Data Engineers".

## Statistical inference and data summary
**Covers:** Sections 4.6-4.7, Table 1, Figures 1-2

- 4.6: "From Phase 2 surveys (A/B Testing), total 200 data points were collected"; "Data were also collected by running unit test scripts and SonarQube code review against the code submitted by participants to ANZ GitHub repositories."

| Metric | Level | Control | Copilot |
|---|---|---|---|
| Total_Time_Spent (minutes) | Min. | 4 | 2 |
| | 1st Quartile | 15 | 5 |
| | Median | 20 | 10 |
| | Mean | 30.98 | 17.86 |
| | 3rd Quartile | 35 | 20 |
| | Max. | 150 | 150 |
| Python_Proficiency | Beginner | 10 | 9 |
| | Novice | 4 | 3 |
| | Intermediate | 40 | 51 |
| | Advanced | 22 | 22 |
| | Expert | 6 | 5 |
| Debugging_Time_Ratio | 0-20% | 24 | 48 |
| | 21-40% | 26 | 19 |
| | 41-60% | 19 | 13 |
| | 61-80% | 13 | 8 |
| | 81-100% | 0 | 2 |
| Difficulty_Level | Very Easy | 11 | 11 |
| | Easy | 52 | 59 |
| | Medium | 15 | 14 |
| | Hard | 4 | 6 |

- Chunk's Table 1 observations, verbatim: "Both Control Group and Copilot Group have almost equal proportion data points."; "Both mean, median, 1st Quartile and 3rd Quartile values of total time taken to solve a problem (Total_Time_Spent) are significantly less for Copilot Group than Control group."; "Number of data points across Python Proficiencies and Difficulty Levels are well distributed across both Control Group and Copilot Group."; "Debug Percentage is less for Copilot Group compared to Control group".
- 4.7 Data Summary: "There were 6 duplicate data points" (same participant, two surveys for same problem); "There were 22 data points where participants could not solve the problems. Remaining 172 data points were used for all the statistical analysis"; the split-group summary "only includes numeric columns from Phase 2 surveys".
- Figure 1 (boxplot): "the median value for time to solve the problem for Copilot Group is less than Control Group. Also, the range of valid Copilot data is much smaller than Control Group. According to this diagram, there are 9 outliers. However, in the analysis these data points were not excluded".
- Figure 2 (QQ-plot): "it is evident that for both Control Group and Copilot Group, Total Time Spent does not follow normal distribution. Since the data does not follow normal distribution, data is skewed, and the number of data points is insufficient, non-parametric tests were performed".

## Non-parametric test method and results (partial — chunk truncated)
**Covers:** Section 4.8, Wilcoxon Signed Rank Test, Table 2 (truncated mid-table in chunk)

- Test choice: "Mann-Whitney U-test and Wilcoxon Signed Rank Test were considered. Finally, Wilcoxon Signed Rank Test were selected because Mann-Whitney U-test tests two independent samples, whereas the Wilcox sign test tests two dependent samples... In the case of Copilot experiment, Copilot Group and Control group consists same set of users."
- Setup: "The tests were one sided and Alpha value selected for this experiment is 0.05 (Confidence Interval 95%)", testing "whether there is any significant difference between the Control Group and Copilot Group participants in terms of average time spent to solve a problem."

| Category | Metric | Hypothesis (verbatim) | Sample size | W | p-value | Decision |
|---|---|---|---|---|---|---|
| Productivity | Total_Time_Spent | H0: no significant difference in Total_Time_Spent; H1: Total_Time_Spent is less for Copilot Group | 22 | 26 | 0.001 | H0 rejected |
| Code Quality | Unit_Test_Success_Ratio | H0: no significant difference in Unit_Test_Success_Ratio; H1: ratio is higher for Copilot Group | 17 | 98 | 0.060 | H1 rejected (per chunk wording) |
| Code Quality | Bugs | H0: no significant difference in Bugs; H1: fewer Bugs for Copilot Group | 17 | 0 | 0.033 | H0 rejected |
| Code Quality | Code_Smells | H0 (verbatim): no significant difference in Code_Smells | 17 | 10 | 0.007 | H0 rejected |

- Note: the chunk ends mid-Table-2 at the Code_Smells row header line, so H1 wording, any Security/Vulnerabilities rows, and further sections are absent from this page's source.
