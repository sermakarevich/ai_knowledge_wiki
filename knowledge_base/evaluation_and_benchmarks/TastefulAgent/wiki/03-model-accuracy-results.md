> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Accuracy of Current Models on Taste-Bench
**In one sentence:** Frontier models score poorly on Taste-Bench (best 59.7% on binary choices), errors concentrate on forks whose deciding evidence appears late, and extra reasoning budget does not fix this.
## Key points
- Best model GPT-5.6 Sol reaches only 59.7% Average accuracy, with GPT-5.5 close behind at 59.5%, and all remaining models dispersed below them — none close to solving Taste-Bench despite every question being a binary choice.
- Research and engineering subsets diverge per model: e.g. Claude Opus 5 scores 64.3% on research but 46.7% on engineering, while GPT-5.6 Sol scores 62.5% research / 56.9% engineering.
- Mean accuracy over 14 models falls from 62.3% at the in-prefix horizon to 21.0% at the more-work horizon, near the 25% score of random guessing on the both-orders-correct metric.
- Detour forks are harder than parallel forks in both domains, and this gap exceeds the gap between the two domains (Appendix D.1).
- Moving from lowest to highest reasoning-effort setting changes accuracy by −0.2 points (GPT-5.6 Sol) and +2.2 points (GPT-5.6 Luna), with settings overlapping at every time horizon — larger reasoning budget does not improve taste.
- Models produce the most reasoning tokens at the more-work level, the level with the lowest accuracy, suggesting they recognize the hard forks but the deciding evidence appears only in the later work.
- Solid bars report accuracy when both candidate orders are answered correctly; dotted extension shows mean over the two orders; whiskers show 95% item-bootstrap intervals; unparseable responses count as incorrect.
---
## 4.2 Accuracy results (Figure 3)
Figure 3 reports Average (R:E = 1:1) plus research (112 forks) and engineering (390 forks) subsets, each column sorted independently highest to lowest. Printed values are the solid-bar endpoint (both orders correct).

| Average | % | Research | % | Engineering | % |
|---|---|---|---|---|---|
| GPT-5.6 Sol | 59.7 | Claude Opus 5 | 64.3 | GPT-5.6 Sol | 56.9 |
| GPT-5.5 | 59.5 | GPT-5.5 | 63.4 | GPT-5.5 | 55.6 |
| Claude Opus 5 | 55.5 | GPT-5.6 Sol | 62.5 | Grok 4.5 | 52.1 |
| Grok 4.5 | 54.6 | GLM-5.2 | 59.8 | GPT-5.6 Terra | 50.0 |
| GPT-5.6 Terra | 54.0 | Claude Sonnet 5 | 58.9 | GLM-5.2 | 47.9 |
| GLM-5.2 | 53.9 | GPT-5.6 Terra | 58.0 | Claude Opus 5 | 46.7 |
| Claude Sonnet 5 | 51.6 | Grok 4.5 | 57.1 | Claude Sonnet 5 | 44.4 |
| GPT-5.6 Luna | 49.0 | GPT-5.4 Mini | 54.5 | MiniMax M3 | 44.1 |
| MiniMax M3 | 45.3 | GPT-5.6 Luna | 54.5 | GPT-5.6 Luna | 43.6 |
| DeepSeek V4 Flash | 43.3 | DeepSeek V4 Flash | 48.2 | Mistral Medium 3.5 | 41.5 |
| GPT-5.4 Mini | 40.1 | MiniMax M3 | 46.4 | DeepSeek V4 Flash | 38.5 |
| Mistral Medium 3.5 | 37.7 | GPT-5.4 Nano | 41.1 | GPT-5.4 Nano | 32.1 |
| GPT-5.4 Nano | 36.6 | Mistral Medium 3.5 | 33.9 | GPT-5.4 Mini | 25.6 |
| Grok 4.20 Reasoning | 15.7 | Grok 4.20 Reasoning | 8.9 | Grok 4.20 Reasoning | 22.6 |

> "Finding 1 — Current frontier models show limited taste. Even the strongest models cannot reliably identify the better direction at decision time, although every question is a binary choice."

> "Across the four cells of the release, detour forks are harder than parallel forks in both domains, and this gap exceeds the gap between the two domains (Appendix D.1)."

## Time-horizon effect (Figure 4 left; §4.3 spillover in chunk)
Every fork is annotated with how far past the fork an observer must see before the supported candidate is clearly justified: in prefix (decisive fact already visible), inferable (hints together justify), next step (first observation after fork justifies), more work (requires completed local check or substantial later work). A judge model assigns the level; Appendix D.3 gives prompt and counts per level. Mean over 14 models falls 62.3% (in-prefix) → 42.9% → 31.5% → 21.0% (more-work).

> "Finding 2 — Model errors concentrate on forks with a long time horizon. Accuracy falls on average as the horizon increases, so answering the questions requires predicting the later work."

## Reasoning-budget effect (Figure 4 right; §4.4 spillover in chunk)
Two models (GPT-5.6 Sol at LOW/XHIGH/MAX; GPT-5.6 Luna at NONE/HIGH/MAX) rerun under three reasoning-effort settings with questions, prompt, token limit, and §3.4 protocol unchanged: six conditions, 6,024 responses total. Accuracy change lowest→highest: Sol −0.2 points, Luna +2.2 points; settings overlap at every horizon.

> "Finding 3 — A larger reasoning budget does not improve taste. The accuracy is unchanged at every time horizon, and the models reason longest at the level where their accuracy is lowest, which suggests that the deciding evidence at these forks appears only in the later work."

## End-to-end comparison (§4.5 fragment in chunk)
Chunk ends mid-sentence comparing the Figure 3 ranking against an end-to-end agent benchmark ("because the taste measurement…", "4.0 PP", axis labels GPT-5.5 / GPT-5.6 SOL); no complete claim is present in this chunk.

**Covers:** Sections 4.2 (full) plus 4.3–4.5 spillover present in chunk 03-4-2-accuracy-of-current-models-as.md (Figures 3–4, Findings 1–3).
