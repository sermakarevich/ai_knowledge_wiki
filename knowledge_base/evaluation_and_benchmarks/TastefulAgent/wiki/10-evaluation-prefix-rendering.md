> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluation Prefix Rendering
**In one sentence:** Evaluation prefixes are rendered one line per trajectory step before the fork (with truncation rules for long outputs and a 65,536-token cap), answers are parsed from a final ANSWER line, and accuracy requires both seeded and reversed presentations to be correct.
## Key points
- Agent messages render as `[i] AGENT:` plus text, commands as `[i] $` plus command, exit code, and indented output, and file edits as `[i] EDIT:` plus edited paths.
- Command outputs longer than 700 characters keep head and tail with the omitted character count marked in between.
- Complete prompts are limited to 65,536 tokens; over-limit prompts keep the first 25 prefix lines (task setup) plus the longest fitting tail, marking omitted steps.
- In the main evaluation the token limit is reached by one question for two models (Claude Opus 5 and Claude Sonnet 5) and by no question for the other models.
- Responses are parsed from the final `ANSWER: X` line, with a single-letter response also accepted; unparseable responses score as incorrect and Table 4 reports counts per model.
- Each question is presented twice (seeded candidate order, fixed per question and shared by all models, and reversed); cell accuracy is the fraction correct in both presentations, mean accuracy is the fraction of correct presentations.
- Engineering accuracy pools the two engineering cells, research accuracy pools the two research cells, and Average is the mean of the two; Figure 3 95% intervals are percentile intervals from 4,000 bootstrap resamples drawn within each domain.
- Every model gets the same prompt and the same 65,536-token output budget with default sampling unless stated; Table 3 lists per-model reasoning settings.
---
## Prefix rendering
The prefix is rendered from the recorded trajectory steps before the fork, one line per step. An agent message is rendered as `[i] AGENT:` followed by its text, a command as `[i] $` followed by the command, its exit code, and its indented output, and a file edit as `[i] EDIT:` followed by the edited paths. When a command output is longer than 700 characters, the rendering keeps its head and its tail and marks the number of omitted characters in between. The complete prompt is limited to 65,536 tokens. When a prompt exceeds this limit, the rendering keeps the first 25 lines of the prefix, which contain the task setup, and the longest tail that fits, and it marks the omitted steps between them. In the main evaluation this limit is reached by one question for two models, Claude Opus 5 and Claude Sonnet 5, and by no question for the other models.
## Answer parsing
The response is parsed from its final `ANSWER: X` line, and a response that consists of a single letter is also accepted. A response without a parseable answer is scored as incorrect, and Table 4 reports the number of such responses per model.
## Scoring
Each question is presented twice, once in a seeded order of the two candidates and once in the reverse order, where the seeded order is fixed per question and shared by all models. The accuracy of a model on a cell is the fraction of questions answered correctly in both presentations, and the mean accuracy is the fraction of correct presentations. The engineering accuracy pools the two engineering cells and the research accuracy pools the two research cells, and the Average is the mean of the two. The 95% intervals of Figure 3 are percentile intervals from 4,000 bootstrap resamples of the questions, drawn within each domain.
## Model settings
Table 3 lists the reasoning setting of each model. Every model receives the same prompt and the same output budget of 65,536 tokens, with default sampling parameters unless stated.

Table 3 Settings of the evaluated models.

| Model | Reasoning setting |
|---|---|
| GPT-5.6 Sol | reasoning effort xhigh |
| GPT-5.5 | reasoning effort xhigh |
| GPT-5.6 Luna, GPT-5.6 Terra | default |
| GPT-5.4 Mini, GPT-5.4 Nano | reasoning effort high |
| Claude Opus 5 | default |
| Claude Sonnet 5 | adaptive thinking |
| Grok 4.5 | reasoning effort high |
| Grok 4.20 Reasoning | default |
| DeepSeek V4 Flash | reasoning effort max |
| GLM-5.2 | reasoning effort max, temperature 1.0 |
| MiniMax M3 | default |
| Mistral Medium 3.5 | reasoning effort high |
## Full results per model and per cell
Table 4 reports the accuracy of every model on the four cells, together with the mean accuracy over the two presentations and the joint outcomes of the two presentations. The columns CC, CW, WC, and WW count the questions answered correctly in both presentations, only in the seeded presentation, only in the reverse presentation, and in neither.

Table 4 Full results of the 14 models on Taste-Bench. P and D denote the parallel and detour constructions, and Eng and Res denote the engineering and research domains. Accuracies are percentages. Unparsed is the number of responses without a parseable answer over the 1,004 presentations.

| Model | Average | Eng. | Res. | P-Eng | P-Res | D-Eng | D-Res | Mean acc. | CC | CW | WC | WW | Unparsed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GPT-5.6 Sol | 59.7 | 56.9 | 62.5 | 75.8 | 56.2 | 48.1 | 67.2 | 65.2 | 292 | 25 | 29 | 156 | 0 |
| GPT-5.5 | 59.5 | 55.6 | 63.4 | 73.4 | 56.2 | 47.4 | 68.8 | 64.6 | 288 | 26 | 24 | 164 | 0 |
| Claude Opus 5 | 55.5 | 46.7 | 64.3 | 71.0 | 64.6 | 35.3 | 64.1 | 60.3 | 254 | 26 | 25 | 197 | 0 |
| Grok 4.5 | 54.6 | 52.1 | 57.1 | 61.3 | 56.2 | 47.7 | 57.8 | 62.0 | 267 | 40 | 43 | 152 | 10 |
| GPT-5.6 Terra | 54.0 | 50.0 | 58.0 | 70.2 | 58.3 | 40.6 | 57.8 | 62.2 | 260 | 40 | 46 | 156 | 0 |
| GLM-5.2 | 53.9 | 47.9 | 59.8 | 64.5 | 60.4 | 40.2 | 59.4 | 64.0 | 254 | 52 | 49 | 147 | 17 |
| Claude Sonnet 5 | 51.6 | 44.4 | 58.9 | 62.1 | 56.2 | 36.1 | 60.9 | 60.7 | 239 | 37 | 52 | 174 | 0 |
| GPT-5.6 Luna | 49.0 | 43.6 | 54.5 | 67.7 | 50.0 | 32.3 | 57.8 | 58.9 | 231 | 48 | 51 | 172 | 0 |
| MiniMax M3 | 45.3 | 44.1 | 46.4 | 64.5 | 56.2 | 34.6 | 39.1 | 57.2 | 224 | 61 | 51 | 166 | 3 |
| DeepSeek V4 Flash | 43.3 | 38.5 | 48.2 | 58.1 | 50.0 | 29.3 | 46.9 | 54.9 | 204 | 59 | 55 | 184 | 2 |
| GPT-5.4 Mini | 40.1 | 25.6 | 54.5 | 26.6 | 54.2 | 25.2 | 54.7 | 49.5 | 161 | 46 | 59 | 236 | 112 |
| Mistral Medium 3.5 | 37.7 | 41.5 | 33.9 | 43.5 | 41.7 | 40.6 | 28.1 | 51.8 | 200 | 70 | 67 | 165 | 24 |
| GPT-5.4 Nano | 36.6 | 32.1 | 41.1 | 46.0 | 43.8 | 25.6 | 39.1 | 48.8 | 171 | 65 | 61 | 205 | 93 |
| Grok 4.20 Reasoning | 15.7 | 22.6 | 8.9 | 28.2 | 8.3 | 19.9 | 9.4 | 29.0 | 98 | 78 | 72 | 254 | 459 |
## Effect of construction and domain
The mean over the 14 models is 58.1% on parallel engineering, 50.9% on parallel research, 50.8% on detour research, and 35.9% on detour engineering. Research forks are therefore not uniformly harder than engineering forks. Moreover, the gap between the two constructions is larger than the gap between the two domains. The pattern is clearest in the two extreme cells. Parallel engineering compares two branches whose recorded outcomes are clearly separated, and it is the easiest cell. In contrast, detour engineering requires the evaluated model to recognize a mistake before the acting agent did, and it is the hardest cell. For this reason, we report the four cells separately and keep both constructions in the benchmark.
## Comparison with SWE-bench Verified
Section 4.5 compares the Average of each model with its public SWE-bench Verified score from the Vals AI leaderboard, and it excludes three models whose responses are unparsable on more than 9% of the presentations. Two models change places between the two benchmarks. Specifically, DeepSeek V4 Flash is 5th of the 11 models on SWE-bench Verified and 10th on Taste-Bench, and only 2 of its 1,004 responses are unparsable, while GPT-5.5 is 8th on SWE-bench Verified and 2nd on Taste-Bench, ahead of Claude Opus 5 on the engineering subset. It is worth noting that the SWE-bench Verified scores are public numbers from a single harness, that the reasoning-effort setting is not matched between the two evaluations for every model, and that the 95% interval of the correlation is wide at this sample size, `[+0.04, +0.89]` for the Average (p = 0.04) and `[−0.30, +0.79]` for the engineering subset.
## Time horizon annotation: judge and prompt
One judge model, GPT-5.5, annotates the time horizon of every question. The judge reads the task, the prefix, the two candidates, and the supported candidate, and it returns one sentence of justification followed by a score. The prompt is shown below.
> Time horizon annotation
>
> # Task
> {query}
>
> # Trajectory before the decision
> {prefix}
>
> # Candidate next steps
> Option A:
> {candidate text}
>
> Option B:
> {candidate text}
>
> # Correct answer
> {letter} (established in hindsight from the completed run)
>
> How far into the future would an observer at this decision point need to see before the correct choice becomes clearly justified? Use this scale:
>
> 0 - Explicit evidence in the prefix: a specific decisive fact is already visible before the decision (an error message, a stated constraint, a visible fix or diff) that directly rules out one option.
> 1 - Inferable from the prefix: no single decisive fact is visible, but weighing the hints already present in the prefix (domain judgment, combining observations) is enough to justify the correct option; no future observation is needed.
> 2 - Next observation settles it: the first direct observation after the decision (the output of one command or probe, the content of one opened file) would clearly justify the correct option.
> 3 - Quick local check needed: a completed, self-contained local verification is needed (running one unit test, a small script, a quick smoke experiment) before the correct option is clearly justified.
> 4 - Substantial future work needed: more than a quick local check is required - meaningful further implementation or investigation, results appearing across later stages of downstream work, or only the terminal outcome (final test suite, external grader, complete branch comparison).
>
> Give a one-sentence justification, then end with exactly: SCORE: N
## Time horizon annotation: levels
The prompt defines five scores, and the four levels of Section 4 are these scores with the two highest merged. This is because only 13 questions receive the highest score, which is too few for a per-model comparison, so we merge them with the 56 questions at the quick-local-check score into the more-work level. The four levels contain 158, 219, 56, and 69 questions. Table 5 reports the distribution per cell, and Table 6 reports the accuracy of every model per level.

Table 5 Number of questions per time horizon level and cell.

| Cell | In prefix | Inferable | Next step | More work |
|---|---|---|---|---|
| Parallel engineering | 72 | 45 | 4 | 3 |
| Parallel research | 11 | 13 | 3 | 21 |
| Detour engineering | 69 | 128 | 36 | 33 |
| Detour research | 6 | 33 | 13 | 12 |
| All | 158 | 219 | 56 | 69 |

**Covers:** chunk 10-prefix-rendering-the-prefix-is-rendered (prefix rendering, answer parsing, scoring, model settings Table 3, full results Table 4, construction/domain effect, SWE-bench Verified comparison, time-horizon judge prompt and level merging/Table 5)
