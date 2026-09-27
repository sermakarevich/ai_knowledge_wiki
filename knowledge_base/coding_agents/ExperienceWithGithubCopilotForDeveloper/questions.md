---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Experience with GitHub Copilot for Developer

### Q1. What are the five research questions the Zoominfo study set out to answer about GitHub Copilot?

> [!tip]- Answer
> The study asks how Copilot should be evaluated to reach a production deployment decision, what acceptance rates look like per language, what drives developer satisfaction, how effective Copilot is at improving productivity, and what its observed and potential limitations are. These questions frame the paper as a medium-scale enterprise evaluation rather than a lab benchmark. See [[wiki/01-github-copilot-developer-experience|Experience with GitHub Copilot for Developer — Paper Overview]].

### Q2. What was Zoominfo's engineering context and scale at the time of the Copilot deployment?

> [!tip]- Answer
> Zoominfo had close to 4,000 employees with about a quarter in engineering and 400 active developers across the US, Europe, India, and Israel, working in microservices plus a few monoliths on two public clouds. Its platform served 100s of millions of contact and company profiles, billions of daily events, and 10s of millions of queries per day across 1000s of repos. See [[wiki/01-github-copilot-developer-experience|Experience with GitHub Copilot for Developer — Paper Overview]].

### Q3. What projected benefits did Zoominfo expect from Copilot for day-to-day development?

> [!tip]- Answer
> Expected benefits were automated generation of snippets and whole functions, pseudo-code-review that spots bugs and aligns code with best practices, documentation and commenting assistance, and a reduced learning curve on new languages and frameworks. Together these were claimed to save time for architecture work, improve quality, speed onboarding, and accelerate development cycles. See [[wiki/02-projected-benefits-and-rollout|Projected Benefits and Rollout Methodology]].

### Q4. How did Zoominfo's four-phase evaluation-to-rollout methodology work in July–September 2023?

> [!tip]- Answer
> Phase 1 was a July 10–17 pilot with 5 engineers scoring ~8.8/10 experience and ~8.6/10 productivity; Phase 2 recruited 126 engineers (~32%) via stratified voluntary sampling with security training and compliance acknowledgments. Phase 3 ran a two-week trial (August 15–29) with 72 survey respondents reporting ~8.0 satisfaction and ~7.6 productivity with no PR quality decline, and Phase 4 began full rollout on September 7 via a paced ServiceNow license workflow. See [[wiki/02-projected-benefits-and-rollout|Projected Benefits and Rollout Methodology]].

### Q5. How is acceptance rate defined, and why did the authors adopt it as their success metric?

> [!tip]- Answer
> For each developer it is accepted suggestions divided by shown suggestions, computed separately for suggestions and for lines, with partial acceptances given full credit and the team rate averaged over developers. The authors adopted it because GitHub's own research found it a better predictor of perceived productivity than alternative measures, while also tracking DORA metrics and satisfaction for the longer term. See [[wiki/02-projected-benefits-and-rollout|Projected Benefits and Rollout Methodology]].

### Q6. What were the headline production acceptance results over the 26-day measurement window?

> [!tip]- Answer
> Over November 11–December 9, 2024, developers accepted about 33% of suggestions and 20% of suggested lines, with the suggestion rate roughly 1.5x the line rate and slight upward trend lines. Daily volume averaged close to 6,500 suggestions and 15,000 lines suggested (~2.8 lines per suggestion), totalling ~75,000 accepted lines in the window and 100s of 1000s in the codebase. See [[wiki/03-acceptance-rate-results|Acceptance Rate Results: Overall, Per-Language, Per-Editor]].

### Q7. How did acceptance rates vary by programming language and by editor?

> [!tip]- Answer
> The top four languages (TypeScript, Java, Python, JavaScript) covered ~80% of suggestions and ~85% of acceptances at rates near 30%, while HTML, CSS, JSON, and SQL were notably lower for unknown reasons; Go was highest but on far smaller volume with 6+ lines per suggestion. JetBrains had larger usage than VS Code with similar ~30% suggestion acceptance, but VS Code's line acceptance rate was ~50% higher with fewer lines per suggestion. See [[wiki/03-acceptance-rate-results|Acceptance Rate Results: Overall, Per-Language, Per-Editor]].

### Q8. What eight potential limitations did the authors envision even though they had not observed them?

> [!tip]- Answer
> They list sensitive-data exposure from public-repo training, IP infringement, security vulnerabilities in generated code, telemetry privacy risks, compliance violations, over-reliance on AI, reinforcement of insecure patterns, and eventual loss of creativity and productivity. The paper stresses these require thorough review, balanced use, and governance despite no observed incidents in the deployment. See [[wiki/04-satisfaction-and-limitations|Potential Limitations and Related Work]].

### Q9. How do the paper's findings relate to the broader related-work literature on Copilot?

> [!tip]- Answer
> The authors conclude their benefits-and-limitations findings are mostly in alignment with related work, with exact figures differing by task, language, and population. That literature is mixed: correctness ranges from ~29% to ~95% depending on the study, ~55–92% of generated tests fail, ~50% of suggestions change on paraphrased prompts, and project effects range from +6.5% productivity with +42% integration time to +40–50% task-time boosts. See [[wiki/04-satisfaction-and-limitations|Potential Limitations and Related Work]].

### Q10. Would you recommend Zoominfo's phased, security-trained Copilot rollout to a similar enterprise, and what caveats apply?

> [!tip]- Answer
> Yes, the evidence supports recommending it: consistent 33%/20% acceptance, ~20% time savings, 72% satisfaction, and no PR quality decline, with the phased pilot-to-trial-to-paced-rollout plus compliance training managing risk well. The key caveats are weaker results on markup/data languages, domain-logic gaps needing extra scrutiny, unresolved security and learning-effect questions, and the need for long-term DORA, quality, and maintenance tracking. See [[wiki/05-conclusions-and-related-work|Conclusions and Related Work]].
