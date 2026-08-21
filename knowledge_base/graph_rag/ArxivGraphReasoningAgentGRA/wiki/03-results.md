[[../index|Wiki]] | [[../summary|Summary]]

# Results: accuracy, tool reliability, token usage, and tool-call budget (Sec. 6)

**In one sentence:** On the frozen xlarge benchmark (n = 258), GRA wins with the DeepSeek and GLM backbones while losing to SQA with Qwen3-Coder-Flash and GPT-5 Nano, and the pattern is explained not by extended reasoning but by tool-call reliability, low unique-input-token usage (GRA reads only ~29–33% of SQA's unique input), and a tool-call budget with a knee around B ≈ 30.

## Key points

- GRA outperforms SQA with DeepSeek V4-Flash (+17.9% relative error reduction), V4-Pro (+26.4%), V4-Pro-Think (+30.5%), and GLM-4.5-Air (+13.5%), but loses with Qwen3-Coder-Flash (−12.1%) and GPT-5 Nano (−22.9%).
- The best per-model accuracies are 87.6–88.4% for the DeepSeek configurations (GRA) versus 74.0–83.3% for SQA, with 95% paired-bootstrap intervals of ±3.9 to ±5.3 pp.
- Tool-call reliability is the dominant factor: under GRA, the three DeepSeek configurations fail under 1% of calls, GPT-5 Nano fails 10.2% of calls (51.6% of questions with ≥1 failure), and enabling reasoning on GPT-5 Nano roughly halves both failure measures (10.2% → 5.8% of calls, 51.6% → 34.9% of questions) for a +6.2 pp accuracy gain.
- Token usage: GRA reads 29–33% of SQA's unique input tokens and RSA 24–29% (measured per question as unique tokens, counting each token once per trajectory); for DeepSeek V4-Flash/V4-Pro SQA's 17.2 k unique input vs. GRA's ~5 k and RSA's 4–5 k.
- Output tokens reverse the pattern: SQA produces 0.5–1.3 k completion tokens per question (single SQL block; e.g. 0.56–0.82 k for V4-Flash/V4-Pro), while the multi-turn agents produce 1.0–2.0 k (e.g. 1.56–1.68 k).
- Billed vs. unique tokens diverge because GRA/RSA resend a growing context over 11–15 turns while SQA averages fewer than three; warm-cache batch eval favours SQA, cold-start single-question serving favours the agents (SQA re-pays its full 17 k-token prompt per question).
- Tool-call budget: accuracy rises sharply from B = 10 to B = 30 then plateaus on both the large (N = 148) and xlarge (N = 258) sets, with truncated questions dropping from 62 → 3 (large) and 118 → 11 (xlarge).
- At B = 10, xlarge accuracy is 63.6%; mean tool-calling turns stabilize at ~11 (large) and ~13 (xlarge) once truncation is rare; no measurable gain above B ≈ 30 calls.
- The budget-aware GRA agent receives the budget up front and a warning after roughly 80% of it is consumed.

## Detail

### 6.1 Accuracy across backbones (Table 3)

Results are reported on the frozen xlarge set (n = 258) with 95% paired-bootstrap intervals. ρ is the relative error reduction of GRA over SQA, defined as ρ = (e_SQA − e_GRA)/e_SQA with e = 100 − accuracy; positive values mean GRA removes a fraction of SQA's errors.

| Model | GRA | RSA | SQA | ρ (%) |
|---|---|---|---|---|
| DeepSeek V4-Flash | **87.6 ±3.9** | 86.1 ±4.2 | 84.9 ±4.5 | +17.9 |
| DeepSeek V4-Pro | **87.2 ±4.1** | 86.9 ±3.9 | 82.6 ±4.5 | +26.4 |
| DeepSeek V4-Pro-Think | **88.4 ±3.9** | 87.4 ±3.9 | 83.3 ±4.5 | +30.5 |
| GLM-4.5-Air | **77.5 ±5.1** | 75.6 ±5.2 | 74.0 ±5.3 | +13.5 |
| Qwen3-Coder-Flash | 78.7 ±4.9 | 78.3 ±5.0 | **81.0 ±4.9** | −12.1 |
| GPT-5 Nano | 70.5 ±5.9 | 70.2 ±5.5 | **76.0 ±5.3** | −22.9 |
| GPT-5 Nano (think) | **76.7 ±5.1** | — | — | — |

Bold indicates the best system for each model. Agentic methods (GRA/RSA) perform best with the DeepSeek and GLM models, whereas SQA performs best with Qwen3-Coder-Flash and GPT-5 Nano. GPT-5 Nano (think) was evaluated only under GRA.

### 6.2 Tool reliability matters more than extended reasoning

Extended reasoning changes little where tool use is already reliable: the three DeepSeek configurations (thinking vs. non-thinking, Flash vs. Pro) lie within 1.2 pp of one another with overlapping intervals. GPT-5 Nano is the exception — thinking adds +6.2 pp (70.5 → 76.7) — but its failure rates roughly halve at the same time: from 10.2% to 5.8% of failed calls, and from 51.6% to 34.9% of questions with at least one failure. The gain therefore looks mediated by reliability rather than by reasoning depth.

Accuracy tracks that failure measure across the whole grid: under GRA, the DeepSeek configurations fail under 1% of calls and take the top three accuracy places with the largest gains over SQA, while GPT-5 Nano fails 10.2% of calls and is both the least accurate configuration and the one for which GRA loses most to SQA. The paper's conclusion: on this task, reliable tool use is a stronger bottleneck than extended reasoning.

| Model (GRA) | Accuracy (%) | Mean tool calls | Failed calls (%) | Questions with ≥1 failure (%) |
|---|---|---|---|---|
| DeepSeek V4-Pro-Think | 88.4 | 12.1 | 0.5 | 5.4 |
| DeepSeek V4-Flash | 87.6 | 14.8 | 0.7 | 8.1 |
| DeepSeek V4-Pro | 87.2 | 13.4 | 0.6 | 7.0 |
| Qwen3-Coder-Flash | 78.7 | 12.2 | 2.0 | 15.9 |
| GLM-4.5-Air | 77.5 | 11.1 | 2.4 | 18.2 |
| GPT-5 Nano (think) | 76.7 | 11.6 | 5.8 | 34.9 |
| GPT-5 Nano | 70.5 | 11.1 | 10.2 | 51.6 |

The table is ordered by accuracy; the accuracy column repeats the GRA column of Table 3. Lower call-failure rates coincide with higher accuracy throughout: the three DeepSeek configurations fail well under 1% of calls, while GPT-5 Nano — the model for which SQA outperforms GRA — fails 10.2% and misses at least one call on more than half of all questions. Enabling reasoning on GPT-5 Nano roughly halves both failure measures.

### 6.3 Token usage (Figure 1)

Figure 1 reports unique input tokens per question for DeepSeek V4-Flash and V4-Pro (non-thinking) across the three systems, counting each token once per trajectory — a measure of corpus coverage rather than billed usage.

| System | V4-Flash unique input (k) | V4-Pro unique input (k) | Completion tokens V4-Flash (k) | Completion tokens V4-Pro (k) |
|---|---|---|---|---|
| GRA | ~5.6 | ~5 | ~1.68 | ~1.56 |
| RSA | 5 | 4.2 | — | — |
| SQA | 17.2 | 17.2 | 0.82 | 0.56 |

(Note: the chart's printed per-series labels are 5.6 / 17.2 / 17.2 for unique input and 1.68 / 1.56 / 1.62 / 1.59 for agent completion tokens and 0.82 / 0.56 for SQA; values above are as labeled in the figure.)

Across the five models, GRA reads 29–33% of SQA's unique input tokens while RSA reads 24–29%. Graph navigation therefore reads slightly more input than flat textual retrieval, but both agents stay well below the full-context baseline. The pattern reverses for output tokens: SQA produces 0.5–1.3 k completion tokens per question because it answers with a single SQL block, whereas the multi-turn agents produce 1.0–2.0 k during iterative search and planning — roughly two to three times as many.

Unique and billed input tokens differ: GRA and RSA resend a growing context over 11–15 turns, while SQA averages fewer than three turns. Under cache-aware pricing the relative cost depends on the workload — warm-cache batch evaluation favours SQA because its large fixed prefix can be reused across questions, whereas cold-start single-question serving favours GRA and RSA because SQA incurs its full 17 k-token prompt on every question.

### 6.4 Effect of the tool-call budget (Figure 2)

Each question is subject to a fixed tool-call budget B; if exhausted before the relevant data are found, the agent must answer before completing its search. B was varied over {10, 20, 30, 40, 50} on the large (N = 148) and xlarge (N = 258) sets, using the budget-aware GRA agent, which receives the budget at the start and a warning after approximately 80% has been consumed. Alongside accuracy, the truncation rate (proportion of questions exhausting the budget without a voluntary answer) and the mean number of tool-calling turns were measured.

Figure 2 (accuracy vs. B for GRA with DeepSeek V4-Flash, y-axis 10–90%): accuracy rises from the low 60s at B = 10 (63.6% on xlarge) up to the high 80s/low 90s by B = 30, with a marked knee at B ≈ 30, then plateaus on both datasets. Over the same 10 → 30 range, truncated questions fall from 62 to 3 on large and from 118 to 11 on xlarge. Once truncation becomes rare, the mean number of turns stabilizes at approximately 11 on large and 13 on xlarge, and additional budget has little effect. Budgets below 20 calls frequently truncate the search and reduce accuracy; no measurable gain is observed above 30 calls, making a budget of ~30 calls sufficient for these datasets.
