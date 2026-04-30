# LLMs Corrupt Your Documents When You Delegate

**Paper:** [LLMs Corrupt Your Documents When You Delegate (Philippe Laban, Tobias Schnabel, Jennifer Neville, 2026)](https://arxiv.org/abs/2604.15597)

## Human Readable TL;DR

Imagine hiring an assistant to update your files over time -- rewriting a recipe, editing a legal contract, tweaking a spreadsheet -- and later discovering they silently garbled the content across dozens of sessions. This paper is the first large-scale study of that exact problem: AI assistants that make changes to your documents introduce errors that accumulate, often catastrophically, the longer you let them work. They tested 19 top AI models across 52 professions and found that even the best models had corrupted roughly a quarter of document content after just 20 back-and-forth edits. The lesson: don't blindly trust an AI to keep your documents intact over repeated editing sessions.

## TL;DR

This paper introduces DELEGATE-52, a benchmark of 310 work environments across 52 professional domains, to evaluate LLMs at long-horizon delegated document editing. Using a novel Round-Trip Relay Simulation -- where an LLM applies a forward edit then reverses it, and this is chained across 20 interactions -- the authors show that all 19 tested LLMs degrade documents over time: average corruption reaches ~50% after 20 interactions, even frontier models corrupt ~25%, and agentic tool use fails to help.

---

## Problem & Motivation

Modern knowledge workers increasingly delegate complex editing tasks to LLMs ("vibe coding" is one example). But if the LLM silently corrupts the document -- deleting content, hallucinating facts, distorting structure -- the user may not catch it, especially when they lack domain expertise or time to review every change. Existing benchmarks focus on single-turn tasks or single domains, failing to capture the iterative, multi-session reality of delegated work. There is no standardized way to measure whether an LLM can be trusted to faithfully edit professional documents over extended workflows.

---

## Main Original Ideas

1. **DELEGATE-52 Benchmark** -- 310 work environments across 52 professional domains (Science & Engineering, Code & Configuration, Creative & Media, Structured Records, Everyday). Each environment has a real-world seed document (2k--5k tokens), 5--10 pairs of invertible forward/backward editing instructions, and distractor documents (8k--12k tokens) to mimic imperfect retrieval in real settings.

2. **Round-Trip Relay Simulation** -- A reference-free evaluation method: the LLM applies a forward instruction (e.g., "sort ingredients alphabetically") and then immediately reverses it ("restore original ingredient order"). Perfect execution returns the document unchanged. Chaining multiple round-trips (a "relay") simulates long-horizon workflows without needing human-annotated ground truth.

3. **Domain-Specific Similarity Functions** -- Instead of generic metrics (ROUGE, Levenshtein, embeddings), each of the 52 domains has a custom parser + similarity function that evaluates structured semantic content (e.g., ingredient lists, chess moves, molecule bonds). These were validated to outperform all generic baselines including GPT-as-judge.

4. **Large-Scale Multi-Model Evaluation** -- 19 diverse frontier and mid-tier LLMs from OpenAI, Anthropic, Google, Mistral, xAI, and Moonshot, spanning a wide range of scales, architectures, and families.

5. **Agentic Harness Ablation** -- A controlled comparison where models operate through file tools (read_file, write_file, run_python) instead of direct text generation, testing whether tool use mitigates degradation.

---

## Key Findings

| Model Tier | Avg. Reconstruction Score @ 20 interactions | Domains "Ready" (≥98%) |
|---|---|---|
| Frontier (Gemini 3.1 Pro, Claude Opus 4.6, GPT 5.4) | ~75% | 11/52 (best model) |
| All 19 models averaged | ~50% | Very few |
| Image generation models (best) | ~28--30% | 0 |

- **Python is the only outlier**: 17 of 19 models achieved near-lossless manipulation. All other domains showed severe degradation for the majority of models.
- **80%+ of model-domain combinations** exhibit catastrophic corruption (reconstruction score < 80%).
- **Degradation is not gradual** -- it is dominated by sparse, severe "critical failures" (single-round-trip drops ≥10%), which account for 80--98% of total observed degradation.
- **Weaker models delete content; stronger models corrupt it.** Frontier models preserve more text but distort/hallucinate its content.
- **Document size compounds degradation**: each additional 1k tokens causes ~0.7% loss after 2 interactions, growing to ~3.6% after 20.
- **Agentic tool use made things worse** (avg. +6% additional degradation), because models preferred manual file rewriting over precise code execution.
- **Distractor documents widen the gap** over time: initial 0.4--4% harm grows to 2--8% by interaction 20.
- **Hardest task types**: global restructuring (split/merge, classification). Easiest: local string manipulation.
- **No plateau in degradation** even at 100 interactions -- models continue introducing novel errors on repeated tasks.

---

## Suggestions & Future Directions

1. **Use DELEGATE-52 as a training environment** -- repurpose the benchmark as an RL "mini-gym" where models are rewarded for achieving lossless round-trips across all 52 domains; cycle-consistency training (inspired by image-to-image translation) is the suggested mechanism.
2. **Design reward functions carefully** to balance instruction-following with content preservation, avoiding reward hacking where a model ignores edits entirely to preserve the document.
3. **Push beyond short-horizon benchmarks** -- the paper argues that 2-interaction performance does not predict 20-interaction performance, so the field needs more long-horizon evaluation standards.
4. **Broaden research beyond math and code** -- the vast majority of knowledge work professions are underserved by current LLM benchmarks; DELEGATE-52 provides a framework to close this gap.
5. **Revisit the "agents always help" assumption** -- basic tool-use harnesses do not solve document integrity issues; stronger architectures (e.g., those that favor code execution over manual rewrites) may be needed.
6. **Extend to multimodal settings** -- the image editing experiments confirm the same degradation dynamics in visual domains, suggesting artifact corruption is a general problem across modalities.

---

## Authors & Institutions

Philippe Laban (Microsoft Research), Tobias Schnabel (Microsoft Research), Jennifer Neville (Microsoft Research)
