# DRBENCHER: Can Your Agent Identify the Entity, Retrieve Its Properties and Do the Math?

**Paper:** [DRBENCHER: Can Your Agent Identify the Entity, Retrieve Its Properties and Do the Math? (Young-Suk Lee, Ramón Fernandez Astudillo, Radu Florian, 2026)](https://arxiv.org/abs/2604.09251)

## Human Readable TL;DR

Imagine a quiz show where you're never told what the question is actually about. Instead, you get cryptic clues like "I am the highest peak in a country whose capital hosted the 1957 National Sports Festival" -- and only after you figure out the answer is Mount Fuji are you asked to compute the atmospheric pressure at its summit. DRBENCHER is a machine that automatically generates thousands of these puzzles across five areas of knowledge, including finance, science, history, and cybersecurity. It checks its own work by running computer code to verify the correct answer, and throws away any puzzle that's too easy. The best AI system tested (Claude Opus 4.6) can figure out the hidden subject 86% of the time, but correctly computes the final numerical answer only 20% of the time -- showing that retrieving and crunching the right numbers is much harder for today's AI than just knowing who or what is being described.

## TL;DR

DRBENCHER is a synthetic benchmark generator that enforces four jointly optimized criteria -- programmatic verifiability, compositional complexity (CCI = E + P), self-referential difficulty filtering (two-stage V1/V2), and graph-based diversity maximization -- to produce questions requiring multi-hop entity identification from Wikidata KG chains followed by domain-specific numerical computation. Gold answers are deterministically computed by code over KG-sourced values before question text is generated. The best frontier model (Claude Opus 4.6) achieves only 20.1% answer accuracy despite 86.1% entity identification accuracy on 268 human-validated questions, confirming that property retrieval and computation -- not entity identification -- are the binding constraints for current deep research agents.

---

## Problem & Motivation

Deep research agents increasingly interleave web browsing with multi-step computation, yet existing benchmarks evaluate these capabilities in isolation. Multi-hop retrieval datasets (HotpotQA, MuSiQue, BrowseComp) test only retrieval; mathematical benchmarks (MATH, GPQA) test only reasoning with fully specified inputs. Static benchmarks also face contamination risk: frontier models have been observed to autonomously identify which benchmark they are running and locate the answer key. There is no principled framework for generating fresh, verifiable benchmark instances on demand that force agents to chain entity identification, property retrieval, and quantitative computation in a single question.

---

## Main Original Ideas

1. **Multi-Skill Compositional Questions** -- The first benchmark generator that jointly requires agents to (a) identify an unnamed entity from indirect, multi-hop knowledge-graph clues and (b) compute a numerical answer using domain-specific formulas over that entity's retrieved properties. Neither skill alone is sufficient.

2. **Answer-First Pipeline with Programmatic Verifiability** -- Gold answers are computed deterministically by executing parameterized code over Wikidata/API values *before* the question is written. Verification is fully programmatic and immune to LLM hallucination in the ground truth.

3. **Compositional Complexity Index (CCI = E + P)** -- A model-independent complexity metric where E = number of entities to identify and P = number of distinct property lookups required per entity. CCI correlates strongly with empirical difficulty (Spearman ρ = -0.22, p < 0.001).

4. **Two-Stage Self-Referential Difficulty Filter (V1/V2)** -- Questions are discarded if the generating model can solve them either closed-book (V1) or with full agentic tool access including browser and Python interpreter (V2). This ensures every retained question is genuinely hard.

5. **Graph-Based Max-Min Diversity Filter** -- Candidate questions are embedded and placed in a near-duplicate graph; a greedy minimum vertex cover algorithm removes redundant questions, approximating a maximum independent set and maximizing semantic diversity.

6. **Contamination Resistance by Design** -- Questions are generated fresh from live Wikidata/API data with deterministically computed answers. No static answer key exists to leak, and new benchmark instances can be generated on demand.

---

## Key Findings

### Model Performance (268 Human-Validated Questions)

| Model | Entity ID (%) | Answer Acc (%) |
|---|---|---|
| **Claude Opus 4.6** | **86.1** | **20.1** |
| Gemini 2.5 Flash | 77.4 | 18.4 |
| Llama 4 Maverick | 75.5 | 17.9 |
| GPT-5.2 | 82.1 | 10.6 |
| Qwen3-30B-A3B-Thinking | 62.8 | 10.0 |
| Mistral-Small-3.2-24B | 70.6 | 6.8 |

- The gap between entity identification and answer accuracy confirms that property retrieval and computation are the primary bottlenecks
- Claude Opus 4.6 significantly outperforms GPT-5.2, Qwen3, and Mistral (all p < 0.001); differences vs. Gemini and Llama are not statistically significant

### Accuracy by Compositional Complexity Index

| CCI | n | Best Model (Opus) | Average (6 models) |
|---|---|---|---|
| 2 | 137 | 28.2% | 18.8% |
| 3 | 54 | 14.2% | 11.1% |
| ≥4 | 77 | 10.0% | 7.4% |

- Monotonic accuracy decline confirmed (Jonckheere-Terpstra Z = 6.75, p < 0.001)

### Human Validity

- 354 questions reviewed by 7 expert annotators: **75.7% valid** overall (**84.2%** excluding stale data errors)
- 35% of errors stem from stale/incorrect Wikidata entries -- an inherent limitation of systems reasoning over evolving data

### Semantic Diversity (vs. Curated Benchmarks)

| Benchmark | BGE dissim. ↑ | Granite dissim. ↑ | E5 dissim. ↑ |
|---|---|---|---|
| **DRBENCHER** | **.548** | **.295** | **.248** |
| BrowseComp+ | .498 | .275 | .229 |
| MATH-500 | .448 | .239 | .200 |
| GPQA | .446 | .261 | .206 |

- DRBENCHER achieves the highest semantic diversity across all three embedding models despite being fully synthetic

---

## Suggestions & Future Directions

1. **Multi-model pipelines** -- Using a different model family for V1/V2 filtering than for generation to reduce self-referential blind spots
2. **Expanding template library** -- Beyond the current 37 templates and two families (quantitative modeling, scientific inference)
3. **New domains** -- Any domain with a Wikidata type identifier or seed list can be onboarded without changing the pipeline
4. **Continuous generation** -- Fresh benchmark instances on demand to stay ahead of contamination as frontier models improve
5. **Acknowledged limitations** -- 35% of human-rated errors stem from stale KG data (especially quarterly-updated financial filings); the single-model pipeline may have systematic blind spots that a different model family could exploit

---

## Authors & Institutions

Young-Suk Lee (IBM), Ramón Fernandez Astudillo (IBM), Radu Florian (IBM)
