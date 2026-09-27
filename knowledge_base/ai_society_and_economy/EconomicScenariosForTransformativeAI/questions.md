---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Economic Scenarios for Transformative AI

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What does the paper promise: prediction, probability, or comparable scenarios -- and what four inputs map to GDP, wages, labor share, and unemployment?

> [!tip]- Answer
> It promises comparable scenarios with no probabilities attached, not predictions. The four inputs are share of tasks affected, diffusion of use, productivity gain per task, and automation-versus-augmentation share. See [[wiki/01-introduction-and-framework|Introduction and Framework]].

### Q2. Define each of m, d, a, and psi in one phrase, and state what the products m*d and m*d*a mean.

> [!tip]- Answer
> Mass m is the fraction of tasks AI affects, diffusion d is the share of those instances actually done with AI, gain a is the log unit-cost decline per AI instance, and psi is the automated share of AI-performed instances. Then m*d is the fraction of economy instances AI performs and m*d*a is that fraction times the per-instance gain. See [[wiki/02-model-production-and-factor-shares|Production and Factor Shares]].

### Q3. Why do wages at fixed rents track productivity m*d*a rather than net displacement (1-rho)*psi*m*d, and when can wages still fall below the no-AI path?

> [!tip]- Answer
> At fixed rents the whole TFP gain m*d*a passes to wages, while displacement only moves task counts, labor share, and capital demand, reaching wages indirectly through rents. Wages fall below no-AI when small per-task savings pair with large task transfers and scarce capital, so rents rise enough to absorb more than the saving -- so-so automation. See [[wiki/02-model-production-and-factor-shares|Production and Factor Shares]].

### Q4. Why does AI-accelerated idea growth add so little to output by 2030 even on the extreme path?

> [!tip]- Answer
> Research input rises only with the GDP level gap, and that level gain applies to a baseline idea growth rate near 1% per year, so a 5% GDP gap lifts TFP growth only from about 1.00% to 1.05%. Realized ideas sit just 0.6% above no-AI in 2030 though the long-run level heads about 10% higher, because cumulation takes decades plus fishing-out drag. See [[wiki/03-model-innovation-and-unemployment|Innovation and Unemployment]].

### Q5. How do sticky cognitive wages plus slow cross-occupation matching turn a wage cut into unemployment?

> [!tip]- Answer
> The cognitive wage closes only part of its gap to the market-clearing level each period, so firms facing an above-clearing wage ration jobs and lay off the excess instead of cutting pay to keep everyone employed. Displaced workers then search across occupations at a discount mu, and with postings closing only a fraction theta_H of the shortfall per month, re-employment lags and unemployment pools up. See [[wiki/03-model-innovation-and-unemployment|Innovation and Unemployment]].

### Q6. State the mid-2026 anchors for m, d, and a, plus the 2030 modest/substantial/extreme values for m, d, a, psi, rho, mu, and theta_H.

> [!tip]- Answer
> Mid-2026 anchors are m = 0.14, d = 0.10, and a = 0.30/0.35/0.45. For 2030, m = 0.2/0.3/0.5, d = 0.2/0.4/0.6, a = 0.30/0.45/0.80, psi = 0.50/0.75/0.90, rho = 0.50/0.25/0, mu = 0.17/0.08/0.04, and theta_H = 0.10/0.25/0.50 per month with rigidity xi = 0.50 in all scenarios. See [[wiki/04-calibration-parameters-and-ai-pace|Calibration and AI Pace]].

### Q7. What did the median of 10,980 US adults expect for 2030 capability, adoption, automation, gain, and re-employment time -- and which scenario do those medians sit near?

> [!tip]- Answer
> The median expects 6 of 8 tasks by 2030 (m = 0.44), adoption d = 0.40, automation psi = 0.47, log gain a = 0.44, and re-employment in about 8 months (mu = 0.064). Fed through the model that lands near substantial change: GDP about 8.6% above no-AI with cognitive employment down about 4.2%. See [[wiki/05-survey-of-us-expectations|Survey of US Expectations]].

### Q8. State the 2030 GDP level gaps, growth rates, and labor-share values for the modest, substantial, and extreme scenarios.

> [!tip]- Answer
> GDP above no-AI is 1.6%, 8.3%, and 32.4%, with growth at 2.4%, 5.4%, and 15.4% per year against 2.0% without AI. Labor share falls from 60% to 59.4%, 56.1%, and 45.2% respectively. See [[wiki/06-results-three-scenarios|Three Scenarios Results]].

### Q9. Contrast the labor-market pain across scenarios: cognitive employment, cognitive unemployment, and the cognitive-versus-other wage split.

> [!tip]- Answer
> Cognitive employment change since mid-2026 is -0.5%, -3.9%, and -21.5%, with cognitive unemployment at 2.9%, 4.5%, and 17.9%. Cognitive wages sit 0.4%, -0.3%, and -11.5% versus no-AI while other-occupation wages run 1.1%, 5.9%, and 33.6% above it. See [[wiki/06-results-three-scenarios|Three Scenarios Results]].

### Q10. How does wage rigidity xi trade wages against unemployment in the extreme scenario, using xi = 0, 0.5, and 0.9?

> [!tip]- Answer
> At baseline xi = 0.5 the extreme cognitive wage is -11.5% with 17.9% cognitive unemployment. At very rigid xi = 0.9 the wage is +2.8% but unemployment climbs to 24.0%, while at fully flexible xi = 0 the wage collapses -42.2% with only 2.6% unemployment. See [[wiki/07-robustness-conclusions-appendix|Robustness and Conclusions]].

### Q11. A city expects AI to displace 10% of its paralegals within a year while electrician and nursing aide openings grow slowly. Using the framework, which three parameters decide whether this becomes a wage dip or an unemployment spike, and what retraining policy follows from the trade-off?

> [!tip]- Answer
> The outcome hinges on psi and rho (how much work is automated outright versus augmented or replaced by new tasks), mu and theta_H (how fast displaced workers cross occupations and how fast receiving occupations post openings), and xi (whether pay adjusts fast or rationing creates layoffs). Policy should therefore raise mu and theta_H with targeted cross-occupation retraining plus hiring capacity in receiving occupations, paired with temporary income support when rigid wages push the cost into unemployment. See [[wiki/07-robustness-conclusions-appendix|Robustness and Conclusions]].

### Q12. What is the weakest link in the paper's evidence chain for its 2030 unemployment claims, and what single check would most change your trust?

> [!tip]- Answer
> The weakest link is that re-employment frictions mu and theta_H plus rigidity xi are scenario assumptions rather than measured AI-displacement flows, since large-scale AI displacement has not yet happened. The check that matters most is incoming data on how long actually displaced cognitive workers take to land new-occupation jobs and at what wage loss, which would pin down the unemployment versus wage-cut split. See [[critical_thinking|Critical Analysis]].
