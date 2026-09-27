> [[index|Wiki]] | [[summary|Summary]]
# Experience with GitHub Copilot for Developer — Digest

## 1. [[wiki/01-github-copilot-developer-experience|Experience with GitHub Copilot for Developer — Paper Overview]]
**In one sentence:** Zoominfo's case study of GitHub Copilot deployed to 400+ developers reports 33% suggestion acceptance, 20% line acceptance, ~20% time savings, and 72% satisfaction, with top-language rates near 30% but weaker results on HTML/CSS/JSON/SQL and limits from missing domain logic and inconsistent quality.
## Key points
- Systematic four-phase evaluation-to-deployment of GitHub Copilot across 400+ geographically dispersed developers with diverse disciplines and languages.
- Mixed method: quantitative acceptance rates of suggestions plus qualitative developer satisfaction surveys.
- Average acceptance rate of 33% for suggestions and 20% for lines of code, stated as in line with rates reported by GitHub and Google.
- Top four languages (TypeScript, Java, Python, JavaScript) sustained at about 30%; smaller acceptance rates observed for HTML, CSS, JSON, and SQL.
- Primary benefit is time savings around 20%; production contribution is on the order of hundreds of thousands of lines of code.
- Main limitations cited: lack of domain-specific logic and lack of consistency in code quality, requiring additional scrutiny when vetting generated code.
- Zoominfo context: ~4,000 employees (quarter in engineering, 400 active developers), 100s of millions of contacts/profiles, billions of daily events, 1000s of repos on GitHub Enterprise Server plus GitLab.

## 2. [[wiki/02-projected-benefits-and-rollout|Projected Benefits and Rollout Methodology]]
**In one sentence:** Copilot was expected to help with code review, documentation, learning new technologies, and overall productivity, and ZoomInfo validated this through a four-phase July–September 2023 evaluation (5-engineer pilot, 126-engineer trial, full rollout) before adopting acceptance rate as its success metric.
## Key points
- Copilot acts as a "pseudo-code-reviewer" trained on billions of lines of code to spot potential bugs, suggest improvements, and align code with best practices.
- Copilot assists documentation by explaining complex snippets and adding useful comments, making the codebase easier for teammates to understand and promoting collaboration.
- Copilot reduces the learning curve on new languages, libraries, and frameworks by suggesting code that adheres to the latest syntax and best practices.
- Overall productivity gains claimed are time efficiency (time freed for architecture and complex problems), quality improvement (fewer bugs and less rework), faster onboarding of new hires and juniors, and accelerated development cycles.
- Phase 1 initial assessment (July 10–17, 2023) with 5 engineers reported overall experience 8.8 out of 10, productivity improvement 8.6 out of 10, and good-to-excellent code-standards alignment from all five, with 3 out of 5 needing to modify suggested code.
- Phase 2 recruitment (July 17–August 14, 2023) enrolled 126 engineers (about 32% of developers) via stratified voluntary sampling, requiring security code review training, written compliance acknowledgments, and a commitment to a follow-up survey.
- Phase 3 two-week trial (August 15–29, 2023) with 72 respondents (about 57% response rate) reported mean satisfaction 8.0 out of 10, mean productivity improvement 7.6 out of 10, and security scores of 8.2, 8.2, and 8.6 out of 10, with no reported decline in pull-request code quality.
- Phase 4 full rollout began September 7th, 2023 via a ServiceNow Workflow for paced license provisioning and compliance tracking, after survey analysis found no outstanding blocking issues.

## 3. [[wiki/03-acceptance-rate-results|Acceptance Rate Results: Overall, Per-Language, Per-Editor]]
**In one sentence:** Over 26 days (Nov. 11–Dec. 9, 2024) developers accepted about one-third of Copilot suggestions (33%) and one-fifth of suggested lines (20%), with slight upward trends and variation by language and editor but similar headline rates.
## Key points
- Acceptance rate is defined per developer prompt as accepted/suggested, computed separately for suggestions and for lines.
- Daily averages are close to 6,500 suggestions and 15,000 lines suggested, with standard deviations near half those values driven by weekday/weekend differences, not day-to-day variation.
- Each suggestion averages 2.8 lines (range one to ten, median near the average); per developer this is a few tens of suggestions per day, totalling about 75,000 accepted lines in the Fig. 2 period and 100s of 1000s of Copilot-generated lines in the codebase.
- Overall acceptance rates average 33% for suggestions and 20% for lines (suggestion rate about 1.5x the line rate), in line with GitHub [34] and another company using a different AI pair programmer [18].
- Acceptance-rate trend lines slope slightly upward, and weekend acceptance rates usually increase rather than decrease for unknown reasons, against a wavy weekday-high/weekend-low volume pattern (Israel weekend Friday–Saturday; US/India Saturday–Sunday).
- By language (top dozen, Nov. 11–Dec. 9 data collected Jan. 9, 2025), acceptance varies about 14% to 32%; the top four languages (TypeScript, Java, Python, JavaScript) cover close to 80% of suggestions, 75% of lines suggested, and close to 85% of acceptances and lines accepted.
- By editor, JetBrains has larger usage/volume than VS Code; suggestion acceptance rates are close to each other and to 30%, while VS Code's lines acceptance rate is about 50% higher with a lower number of lines per suggestion (reason unknown).

## 4. [[wiki/04-satisfaction-and-limitations|Potential Limitations and Related Work]]
**In one sentence:** The authors list eight envisioned but unobserved limitations of GitHub Copilot (data exposure, IP, vulnerabilities, privacy, compliance, over-reliance, bad patterns, lost creativity) and survey related work showing mixed productivity and correctness results, concluding their own benefits-and-limitations findings are mostly in alignment with that literature.
## Key points
- Eight potential limitations are envisioned despite not being observed: sensitive-data exposure, IP infringement, security vulnerabilities, telemetry privacy, compliance violations, over-reliance, reinforcement of insecure patterns, and reduced creativity/productivity.
- GitHub's own report [34] finds acceptance rate of shown suggestions is a better predictor of perceived productivity than alternative measures, and the authors adopt the same measure in §6.
- Reported correctness varies widely by study: ~60% Java / ~30% JavaScript on LeetCode [15], 70–95% by human graders on intro assignments [19], ~29% correct / ~20% incorrect / rest partially correct with ~92% valid code [30].
- Test-generation and robustness results are weak: ~55% of generated tests fail inside an existing suite and ~92% outside it [11]; ~50% of suggestions differ on semantically equivalent prompts with correctness affected in ~30% of cases [14].
- Project-level effects are mixed: +6.5% productivity from individual output plus participation but +42% integration time [20], versus +40–50% task-time boost growing with difficulty in a ~1,000-engineer, four-week corporate deployment [2].
- Prompt language and privacy matter: worst Copilot performance in Chinese among Chinese/English/Japanese with all degrading as difficulty rises [12], and ~8% of test cases leak sensitive personal information from the Codex model [16].
- Usage patterns: JavaScript/Python, VS Code, and data processing dominate discussions [33]; Copilot ranks second to ChatGPT on HumanEval [29]; generated code is mostly small, low-complexity, sparsely commented functions with fewer modifications than human code [32].

## 5. [[wiki/05-conclusions-and-related-work|Conclusions and Related Work]]
**In one sentence:** GitHub Copilot showed consistent acceptance rates (33% suggestions, 20% lines) and 72% developer satisfaction with an effective phased deployment, but has domain-logic and security limitations requiring long-term study of DORA metrics, quality, maintenance, and learning effects.
## Key points
- Suggestion acceptance rate of 33% and line acceptance rate of 20% held consistent across different programming languages.
- Consistency across languages indicates reliable utility across diverse development contexts.
- Developer satisfaction reached 72%, with positive feedback on support for daily development tasks.
- Copilot was particularly effective for boilerplate code generation and unit testing.
- A phased deployment approach including security training and policy alignment proved effective for managing the transition to AI-assisted development.
- The tool shows limitations in understanding domain-specific logic.
- Security implications require careful consideration despite overall success.
- Future work should assess long-term impact on DORA metrics, code quality, and maintenance, plus effects on developer learning and skill development for enterprise adoption.

## The argument in five moves
1. Zoominfo frames developer productivity as competitive advantage and treats Copilot tooling for writing, testing, and reviewing code as a fundamental lever worth a systematic enterprise evaluation.
2. Projected benefits (generation, pseudo-review, documentation, learning-curve reduction) justify a governed four-phase July–September 2023 path from 5-engineer pilot to 126-engineer trial to paced full rollout, with acceptance rate adopted as the productivity proxy.
3. Production measurement over 26 days then quantifies the payoff at 33% suggestion and 20% line acceptance (~6,500 suggestions and ~15,000 lines per day), concentrated in TypeScript/Java/Python/JavaScript and consistent with external GitHub and industry figures.
4. Qualitative and related-work evidence bounds the claim: strong satisfaction and boilerplate/test utility alongside weaker HTML/CSS/JSON/SQL rates, domain-logic gaps, inconsistent quality needing scrutiny, and literature showing mixed correctness, test-failure, robustness, and privacy results.
5. The conclusion therefore endorses phased, security-trained deployment as effective and successful at ~20% time savings and 72% satisfaction, while calling for long-term study of DORA metrics, quality, maintenance, and learning effects before enterprise adoption is fully understood.
