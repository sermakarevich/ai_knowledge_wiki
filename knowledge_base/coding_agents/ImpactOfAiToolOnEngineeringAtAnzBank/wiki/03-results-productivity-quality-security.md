> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Results: Productivity, Quality, Security and Sentiment
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
---
## Wilcoxon A/B result
Results of Wilcoxon Signed Rank Test in Table 2 suggests that, because of using Copilot there are significant improvements on productivity and code quality related metrics. However, "The SonarQube code review did not produce sufficient evidence to make any conclusion on Security aspect of the code submitted by the participants."
**Covers:** Table 2 summary bridging hypotheses H0/H1 on Code_Smells and Vulnerabilities

## 4.9.1. Productivity
Table 3 describes productivity increase by Python proficiency (Novice merged into Beginner; Expert merged into Advanced due to few participants):

| Python proficiency | Mean Total_Time_Spent (Control)/problem (min) | Mean Total_Time_Spent (Copilot)/problem (min) | Productivity Improvement |
|---|---|---|---|
| Beginner | 20.07 | 9.58 | 52.27% |
| Intermediate | 28.60 | 16.70 | 41.6% |
| Advanced | 39.82 | 23.70 | 40.48% |

Overall Productivity Improvement = ((Mean Total_Time_Spent(Control Group) - Mean Total_Time_Spent(Copilot Group)) / Mean Total_Time_Spent(Control Group))*100 = ((30.98-17.86)/30.98)*100 = 42.34%. "This study shows that Copilot improves the productivity of ANZ engineers by 42.36% on an average." Copilot users took less time overall on each challenge problem; the assessment found Copilot "was most helpful for those who were 'Expert' python programmers" (Figure 3), helped at all code-challenge levels from 'Very Easy' to 'Hard' (Figure 4), with the largest improvement on 'Hard' tasks.
**Covers:** Section 4.9.1, Table 3, Figures 3–4

## 4.9.2. Quality
"According to the unit test results, methods written by Copilot Group participants had 12.86% more success ratio than methods written by Control group users. However, this result is not statistically significant." Table 3 suggests participants with "Beginner" Python proficiency received the highest benefit from using Copilot.
**Covers:** Section 4.9.2

## 4.9.3. Security
"This section covers how engineers - with and without Copilot - performed from a security standpoint, providing insight into both the introduction of security risks as well as minimisation of existing ones." One security-related question was inserted per week: "password usecase" prompted a function securely hashing an inputted password using pbkdf2_hmac from 'hashlib', keyed on a randomly generated cryptographic salt ("if salts aren't randomly generated, hackers are better able to match the inputs and outputs of a hash function"); "code executor usecase" prompted a basic FastAPI app accepting a 'command' parameter at POST '/execute', requiring checks on command parameters before running functions, otherwise "susceptible to injection attacks." SonarQube static analysis checked both via Sonar Way definitions; SonarQube defines a vulnerability as "a security-related issue that represents a backdoor for attackers." The scan "generated only 1 non-zero data point against Vulnerabilities. There is not enough data available to test this metric."
**Covers:** Section 4.9.3

## 4.9.4. Sentiment Around Copilot
All table values are medians (50th percentile), colour-coded by favourability. Aggregation of phase 1 (weeks 1-2) responses: "Across all areas, participants responded positively regarding GitHub Copilot," but "the magnitude of each area's sentiment fell short of the 'strong positive'":

| Area | Aggregate Perceived Effect |
|---|---|
| Time spent debugging code using Copilot | A bit less time |
| Time needed to produce the same code without Copilot | A bit more time |
| Suggestions' alignment with project's coding standards | Well |
| Quality of suggestions received | Somewhat helpful |
| Impact on ability to review and understand existing code | Positive effect |
| Impact on ability to create unit tests for code | Positive effect |
| Impact on ability to create documentation of the code | Positive effect |

They "felt it helped them review and understand existing code, create documentation, and test their code; they felt it allowed them to spend less time debugging their code and reduced their overall development time; and they felt the suggestions it provided were somewhat helpful, and aligned well with their project's coding standards."
**Covers:** Section 4.9.4, Table 4

## 5.1. Limitations
Sample size: "over 100 engineers participated over a six-week period" but "participation rates fluctuated significantly"; vs "around 5000 engineers in diverse roles," the sample "represents only a fraction of this population." Programming questions: "password usecase" was seen by some as difficult, receiving fewer attempts; lightweight atomic questions left "little room for bugs and vulnerabilities to exist," so "the other two categories could not be reasonably measured" and only some code-smell data was obtained — a repeat should use a "project-style task." Biases: Dunning-Kruger effects on self-reported proficiency and possible under-reporting of time, both assumed equal across randomly composed groups so "relative comparisons between experience levels remain valid"; sentiment may reflect positive volunteer predisposition outweighing any negative bias.
**Covers:** Section 5.1
