> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Acceptance Rate Results: Overall, Per-Language, Per-Editor
**In one sentence:** Over 26 days (Nov. 11–Dec. 9, 2024) developers accepted about one-third of Copilot suggestions (33%) and one-fifth of suggested lines (20%), with slight upward trends and variation by language and editor but similar headline rates.
## Key points
- Acceptance rate is defined per developer prompt as accepted/suggested, computed separately for suggestions and for lines.
- Daily averages are close to 6,500 suggestions and 15,000 lines suggested, with standard deviations near half those values driven by weekday/weekend differences, not day-to-day variation.
- Each suggestion averages 2.8 lines (range one to ten, median near the average); per developer this is a few tens of suggestions per day, totalling about 75,000 accepted lines in the Fig. 2 period and 100s of 1000s of Copilot-generated lines in the codebase.
- Overall acceptance rates average 33% for suggestions and 20% for lines (suggestion rate about 1.5x the line rate), in line with GitHub [34] and another company using a different AI pair programmer [18].
- Acceptance-rate trend lines slope slightly upward, and weekend acceptance rates usually increase rather than decrease for unknown reasons, against a wavy weekday-high/weekend-low volume pattern (Israel weekend Friday–Saturday; US/India Saturday–Sunday).
- By language (top dozen, Nov. 11–Dec. 9 data collected Jan. 9, 2025), acceptance varies about 14% to 32%; the top four languages (TypeScript, Java, Python, JavaScript) cover close to 80% of suggestions, 75% of lines suggested, and close to 85% of acceptances and lines accepted.
- By editor, JetBrains has larger usage/volume than VS Code; suggestion acceptance rates are close to each other and to 30%, while VS Code's lines acceptance rate is about 50% higher with a lower number of lines per suggestion (reason unknown).
---
## Success measure and overall volume
**Covers:** Section 7, Fig. 2 (Nov. 11–Dec. 9, 2024, 26 days)

For each prompt from a developer, GitHub Copilot makes a suggestion with one or more lines of code or comments, and the developer accepts or declines it; the ratio is the acceptance rate, reported for both suggestions and lines. Fig. 2 tables suggestions, acceptances, lines suggested, and lines accepted plus both rates.

| Measure | Value |
|---|---|
| Period | 26 days, Nov. 11–Dec. 9, 2024 |
| Avg. suggestions per day | close to 6,500 |
| Avg. lines suggested per day | close to 15,000 |
| Std. deviations | close to half of each average, due to weekday vs. weekend rather than day-to-day variation |
| Weekday averages | about 20% (suggestions) and 35% (lines) larger than overall averages |
| Weekend averages | about 60% (suggestions) and 75% (lines) smaller than overall averages |
| Weekend definition | Israel Friday–Saturday; US and India Saturday–Sunday |
| Lines per suggestion | average 2.8, range one to ten, median close to average |

## Overall acceptance rates and trends
**Covers:** Section 7, Figs. 3–4 (Fig. 3 bars: Nov. 14–Dec. 9, 2024)

| Measure | Value |
|---|---|
| Avg. suggestion acceptance rate | 33% (about one third of suggestions accepted) |
| Avg. line acceptance rate | 20% (about one fifth of suggested lines accepted) |
| Suggestion vs. line rate | former about 1.5 times larger than latter |
| Trend | slight upward trend in each acceptance-rate trend line (Figs. 3–4) |
| Weekend effect | acceptance rates during weekends usually increase rather than decrease; reason unknown |
| Volume pattern | wavy pattern due to weekdays (high) and weekends (low) |
| External comparison | numbers in line with GitHub [34] and other companies, e.g. [18] with a different AI pair programmer; future work: why this cross-company/tool alignment occurs |
| Scale impact | a few 10s of suggestions per day per developer; about 75,000 lines accepted during the Fig. 2 period alone; total Copilot-generated lines in codebase has reached 100s of 1000s |

## Per-language acceptance rates
**Covers:** Section 8, Figs. 5–7 (Fig. 5 data for ~month Nov. 11–Dec. 9, 2024, collected Jan. 9, 2025)

Fig. 5 tables per-language suggestions, acceptances, lines suggested, lines accepted, acceptance rate, and lines acceptance rate for only the top dozen languages sorted by total suggestions; Groovy, Shell (e.g. zsh/bash), Scala, Ruby and the like excluded as too small. Largest counts are for TypeScript, Java, Python, and JavaScript, unsurprising given most of the codebase is in these four.

| Measure | Value |
|---|---|
| Top-four share | close to 80% of suggestions, 75% of lines suggested, close to 85% of acceptances and lines accepted |
| Per-language suggestion acceptance | varies between about 14% to 32% |
| Highest | Go, but with far smaller suggestion count; Go lines per suggestion over 6 vs. 2–3 for other languages |
| Top three languages | acceptance rates over 30%, agreeing with overall rate |
| HTML, CSS, JSON, SQL | interestingly smaller acceptance than general-purpose languages; reason unknown |
| Fig. 6–7 notes | same table as bar charts/line plots; suggestion rate 1.5 to over 2 times larger than line rate; slight upward trend lines |

## Per-editor acceptance rates
**Covers:** Section 9, Fig. 8 (top two IDEs: JetBrains and VS Code)

| Measure | Value |
|---|---|
| Usage | JetBrains more widespread, hence larger suggestions and lines suggested |
| Suggestion acceptance | close to each other and close to the 30% overall figure |
| Lines acceptance | differ, with VS Code about 50% higher |
| Lines per suggestion | lower for VS Code; reason for the difference unknown |
