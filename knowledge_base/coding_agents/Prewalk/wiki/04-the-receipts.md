> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Receipts

**In one sentence:** Across two frontier/cheap model families, `/prewalk` recovers 92–97% of the frontier model's own solo pass rate while cutting cost 39–53% and cutting wall-clock time 34–47%, consistently beating the paired "cheap model working alone" baseline it hands off to.

## Key points

- **GPT-5.6 family (executor: GPT-5.6 Luna):**
  - Luna oneshot (cheap model alone): 77% pass, $0.60, 570s.
  - `/prewalk` (Sol plans, Luna executes): 85% pass (**+10 points** over Luna alone), $1.04 (**−39%** vs. Sol oneshot), 300s (**−47%** vs. Sol oneshot).
  - Sol oneshot (frontier model alone): 88% pass, $1.71, 372s.
  - Framed by the author: `/prewalk` reaches **97% of Sol's pass rate at 61% of the cost**, and is the fastest of the three arms, "because Sol stops burning slow frontier tokens after the opening and Luna doesn't waste turns lost in the woods."
- **Opus 4.8 family (executor: Gemini Flash 3.5):**
  - Flash oneshot (cheap model alone): 60% pass, $1.16, 360s.
  - `/prewalk` (Opus plans, Flash executes): 78% pass (**+30 points** over Flash alone), $1.46 (**−47%** vs. Opus oneshot), 402s (**−34%** vs. Opus oneshot).
  - Opus oneshot (frontier model alone): 85% pass, $2.78, 606s.
  - Framed by the author: `/prewalk` reaches **92% of Opus's pass rate at 53% of the cost**, at **1.5×** the speed, and **+18 points** over oneshot Flash.
- The pattern is symmetric across both families: the cheap executor alone is the weakest arm on pass rate; the frontier model alone is the strongest but most expensive/slowest; `/prewalk` sits close to frontier pass rate while undercutting frontier cost and duration by roughly a third to a half.
- These numbers should be read alongside [[01-the-plan-paradox|The /plan Paradox]]'s finding that `/plan` (the plan-document handoff) is not merely worse than `/prewalk` — for Opus, it was *worse than not splitting the task at all* (higher cost than Opus oneshot, at the same 84.6% pass rate).
- The headline aggregate stats quoted at the top of the article — 97% of frontier performance, 41% cheaper, 1.9× faster completion, ~3× less likely to cheat — are the article's own summary framing of the same underlying SWE-Bench Pro results across these arms (cheating numbers are covered separately in [[05-cheating-and-prefill|Cheating and the Prefill Connection]]).
- Both test rides use real historical SWE-Bench Pro tasks (Django issues `django-13279` and `django-12325`) as the worked examples behind the summary tables, not synthetic benchmarks.

---

## Reading the two tables together

| Arm | Pass | Cost | Duration |
|---|---|---|---|
| GPT-5.6 Luna oneshot | 77% | $0.60 | 570s |
| GPT-5.6 `/prewalk` (Sol→Luna) | 85% | $1.04 | 300s |
| GPT-5.6 Sol oneshot | 88% | $1.71 | 372s |
| Gemini Flash 3.5 oneshot | 60% | $1.16 | 360s |
| Opus 4.8 `/prewalk` (Opus→Flash) | 78% | $1.46 | 402s |
| Opus 4.8 oneshot | 85% | $2.78 | 606s |

The GPT-5.6 family shows a smaller gap between frontier and cheap oneshot pass rates (88% vs. 77%) than the Opus/Flash family (85% vs. 60%) — yet `/prewalk` still adds double-digit points over the cheap baseline and beats the frontier model's own cost and duration in both families, suggesting the technique's benefit does not depend on a large capability gap between the two models.

## Covers

The "The receipts" section of the article, including both result tables (GPT-5.6 Sol and Opus 4.8) and the two percentage/cost/speed framing lines that follow each.
