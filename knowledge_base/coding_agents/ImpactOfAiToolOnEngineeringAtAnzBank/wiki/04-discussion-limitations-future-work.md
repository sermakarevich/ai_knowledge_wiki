[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Discussion, Recommendation and Future Work
**In one sentence:** The paper concludes Copilot had a statistically and practically significant positive impact on productivity and quality with no major security issues found, reports moderately positive user sentiment, and recommends productionising Copilot at ANZ Bank.
## Key points
- The Copilot group completed tasks 42.36% faster than the control group, a statistically significant productivity gain.
- Copilot-produced code contained fewer code smells and bugs on average, implying better maintainability and lower production-breakage risk, both statistically significant.
- The experiment could not generate meaningful code-security data, but the available data suggest Copilot did not introduce any major security issues.
- Median survey responses were uniformly positive but moderate: never the maximum positivity level in any surveyed area.
- Participants reported a "positive effect" on reviewing/understanding code, documenting code, and creating unit tests, plus "a bit less time" debugging and "a bit more time" needed without Copilot.
- Suggestions were rated "somewhat helpful" and aligned with coding standards "well", with qualitative feedback pointing to areas for improvement.
- Subject to further security analysis, the authors recommend productionising GitHub Copilot at ANZ Bank, noting 1,000+ users already adopted it and a detailed productivity study is underway.
---
## Overall findings
**Covers:** conclusion section, overall evidence summary

The chunk states: "This paper presents evidence on the impacts that GitHub Copilot may have on productivity, code quality and code security in ANZ Engineering." Key reported outcomes:

| Outcome | Result stated in chunk |
|---|---|
| Productivity | Copilot group completed tasks 42.36% faster than control; statistically significant; described as statistically and practically significant |
| Code quality | Fewer code smells and bugs on average in Copilot code; more maintainable and less likely to break in production; statistically significant |
| Code security | Experiment could not generate meaningful data to measure security; data suggest Copilot did not introduce any major security issues |

## User sentiment
**Covers:** conclusion section, sentiment survey results

- Participants felt Copilot had a "positive effect" on ability to review and understand existing code, create documentation, and create unit tests.
- They felt it helped them spend "a bit less time" debugging and that they would have spent "a bit more time" producing the same code without Copilot.
- Suggestions were "somewhat helpful" and aligned with coding standards "well".
- Sentiments were "uniformly positive in valence" but "all moderate; in none of the surveyed areas did the median participant respond with the maximum degree of positivity."
- Qualitative feedback "suggests that there are areas of improvement for Copilot to be more effective in improving the developer's experience."

## Recommendation and future work
**Covers:** conclusion section, recommendation and adoption status

- "However, considering the quantitative and qualitative analysis of the data generated in this experiment and subject to further analysis on security of the code suggested by Copilot, it is recommended to productionise GitHub Copilot at ANZ Bank."
- "In conclusion, this research provides compelling evidence of the transformative impact of GitHub Copilot on engineering practices at ANZ Bank."
- Adoption framing: shift empowering engineers to focus more on creative and design tasks while reducing time spent on repetitive coding.
- Status at writing: "over 1,000 users using it into their workflows" and "a detailed investigation into the productivity improvements attributable to GitHub Copilot is underway" to quantify impact on operational efficiency and overall performance.
