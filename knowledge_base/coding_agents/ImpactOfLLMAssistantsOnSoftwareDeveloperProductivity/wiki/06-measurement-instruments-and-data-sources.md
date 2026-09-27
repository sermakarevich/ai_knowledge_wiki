> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Measurement Instruments and Data Sources (RQ1)
**In one sentence:** Self-reported methods (mostly author-designed surveys/interviews) predominate across the 39 empirical studies while only 15 use validated instruments and behavioral/performance metrics cluster in high-control experiments, with time-to-completion the top metric (31%), acceptance rate a common but cautioned-against metric, NASA-TLX cognitive-load findings mixed, and econometric studies reporting 24% throughput / 26% quality gains alongside a throughput–quality trade-off (r = −0.45).
## Key points
- Self-reported methods predominate and are often designed by study authors to capture user experience, perceived productivity, trust, or ease of use (e.g., post-task surveys, open-ended feedback).
- Only 15 out of 39 empirical studies incorporate validated instruments, including the SPACE framework, NASA-TLX for mental workload, TAM for technology acceptance, self-efficacy questionnaires, or emotional affect questionnaire.
- Behavioral and performance metrics focus on quantifiable outcomes — time to completion, acceptance rate of AI-generated suggestions, code quality metrics, and interaction patterns — and are mostly associated with high-control designs such as laboratory experiments, field experiments, or experimental simulation.
- Time to completion is the most frequently used performance metric at 31% (12 out of 39), mostly measured in laboratory experiments under controlled conditions, plus one field study comparing throughput/cycle time before/after Copilot, one experimental simulation using "person/days," and one study measuring issue-report-to-resolution time.
- Acceptance rate of LLM suggestions is a commonly used behavioral metric, with a Meta study of Code Compose counting accepted suggestions and proportion of LLM-authored code, while a GitHub study finds strong correlation between accepted-suggestion frequency and perceived productivity but cautions against using the metric in isolation.
- Six studies (6 out of 39) measure cognitive workload with NASA-TLX (mental demand, physical demand, temporal demand, performance, effort, frustration) in comparative experimental settings, with mixed findings: improvements in some, neutral effects in others, and one study reporting significantly worse frustration.
- Econometric studies using TCQ and RBV frameworks report that coding shows the highest GenAI gains (24% throughput, 26% quality on average across 1,000+ large firms, 2021–2023), while a survey of 70 large global companies confirms throughput gains but finds increased throughput negatively correlated with code quality (r = −0.45).
- Field studies and sample studies still employ diverse instruments but primarily rely on self-reported methods such as surveys, interviews, and users' open-ended feedback, whereas time-to-completion and code-quality metrics are mainly associated with laboratory experiments.
---
## Evaluation instruments (Table 7, §5.3)
| Data Source | Instrument Origin | Instrument and Primary Studies |
|---|---|---|
| Self-Reported | Designed by Authors | Surveys [50, 51, 56, 57, 58, 60, 63, 64, 67, 68, 69, 70, 72, 73, 78, 80, 85, 86, 88] |
| | | Interviews [52, 64, 70, 74, 75, 78, 80, 82, 83, 86] |
| | | Users open-ended feedback [54, 66, 74, 84] |
| | Validated Instruments and Frameworks | NASA-TLX (Mental Effort) [51, 57, 61, 62, 74, 87] |
| | | SPACE Framework-Based Surveys [65, 71, 73, 76] |
| | | Technology Acceptance Model (TAM) [58, 62, 88] |
| | | Self-Efficacy Questionnaires [52, 61] |
| | | After-Action Review for AI (AAR/AI) [61] |
| | | Emotion Affect Questionnaire [87] |
| Behavioral & Performance Metrics | Designed by Authors | Task Completion and Correctness [50, 53, 55, 61, 62, 70, 72, 78, 87] |
| | | Suggestions Acceptance Rate [54, 55, 59, 65, 66, 71, 73] |
| | | Interaction Patterns (Logs/Edits/Tracking) [50, 57, 62, 66, 72, 73, 74] |
| | | Time to Completion [50, 52, 53, 55, 57, 62, 67, 72, 73, 74, 76, 77] |
| | | Code Quality Metrics [50, 51, 61, 67, 73, 86] |
| | | Productivity Gain [77, 78] |
| | Validated Frameworks | Time Cost Quality (TCQ) Framework [81] |
| | | Resource-Based View (RBV) Framework [75, 81] |

Researchers employ instruments "from self-reported surveys and interviews including validated questionnaires to behavioral & performance metrics as shown in Table 7." Figure 5 maps empirical strategies to instruments: behavioral and performance metrics cluster with laboratory experiments, field experiments, and experimental simulation.

## Time to completion (§5.3.1)
The most frequently used performance metric: 31% (12 out of 39) of empirical primary studies. Breakdown from the chunk:
- Laboratory experiments [50, 52, 55, 57, 62, 67, 72, 73, 74] assess time to complete specific programming tasks under controlled conditions (majority of users of this metric).
- One field study within a software company [76] measures time-related performance by comparing throughput and cycle time before and after Copilot integration.
- One experimental simulation [77] estimates total effort using a "person/days" metric to compare durations with and without LLM-assistants.
- One study [53] measures completion time as duration from issue report to resolved/closed.

## LLM suggestions acceptance rate (§5.3.2)
Used in [54, 55, 59, 65, 66, 71, 73]. Meta study [54] of internal Code Compose "quantifies the LLM-assistant's utility by measuring both the number of LLM-generated suggestions accepted by developers and the proportion of code authored by the LLM-assistants," then compares against reported acceptance rates of competing assistants. GitHub study [65] "statistically analyzes the relationship between several interaction metrics related to code completion and developers' self-reported productivity" and finds "a strong correlation between the frequency of accepted suggestions and perceived productivity." Verbatim cautions: "optimizing for acceptance rate may bias LLM-assistants toward well-represented languages or routine tasks, potentially disadvantaging less-represented workflows" and "'blind' reliance on acceptance rate can lead to superficial improvements that inflate perceived usefulness without meaningfully enhancing developer outcomes."

## Mental effort and cognitive load (§5.3.3)
"Studies often use the terms mental effort or cognitive load interchangeably." Traditionally measured via EEG or ECG, but "[n]one of the identified studies leverages any biomedical measures or sensors"; only one experimental study uses eye-tracking [55] for time spent reading code documentation. Six studies [51, 57, 61, 62, 74, 87] use NASA-TLX, capturing "mental demand, physical demand, temporal demand, performance, effort, and frustration," all in comparative experimental settings. Mixed findings:
- Improvements: [62, 72, 87] — e.g., "[87] reports that Copilot reduces both perceived effort and mental demand for novice programmers"; "[72] develops a custom questionnaire" for programming exam tasks and finds "students using Google Bard report lower mental effort compared to those relying on conventional search engines."
- Neutral: [51, 57] — "[51] finds that participants rate LLM-assisted tasks as equally demanding and effortful"; "[57] finds no statistically significant differences across all NASA-TLX dimensions when comparing coding with and without ChatGPT (GPT-3.5)."
- Worse: [61] — "no significant difference in overall cognitive load between students using ChatGPT (GPT-4) and those using a traditional web browser, but does report a statistically significant increase in frustration for the ChatGPT group."
The chunk attributes variability to "diverse operationalizations of cognitive load, differences in participants' expertise, task design, and the capabilities of LLM-assistants," calling for "more standardized methodologies and multi-modal assessment strategies."

## Econometric analysis (§5.3.4)
Two complementary studies [75, 81]. Study [81] uses the Time-Cost-Quality (TCQ) framework for "a comparative survey of over 1,000 large firms from 2021 to 2023, examining the effect of GenAI on labor productivity across different domains, including coding and content production," assessing throughput (time efficiency) and quality (correctness): "coding exhibits the highest reported gains, with an average 24% improvement in throughput and 26% in quality." Complementary study [75] surveys 70 large global companies on LLM-based pair programming: confirms throughput gains but "increased throughput is negatively correlated with code quality (r = −0.45)," with effectiveness depending "heavily on organizational readiness and the ability to balance speed with software quality."

## RQ1 summary (as given in chunk)
Verbatim: "Among all primary studies, laboratory experiments are the most common strategy (38%, 15 out of 39). Mixed-methods designs are prevalent (69%, 27 out of 39) among empirical methods, often combining user experiments with surveys. Time to completion is the most frequently used performance metric (31%, 12 out of 39). Acceptance rate is a frequently used behavioral metric, though some studies caution against its overuse. Cognitive load findings are mixed: 6 studies use NASA-TLX, but results vary from reduced effort to increased frustration."

**Covers:** RQ1 instruments, data sources, procedures and metrics for evaluating productivity (§5.3–5.3.4 plus RQ1 summary box; Table 7; Figure 5 mapping)
