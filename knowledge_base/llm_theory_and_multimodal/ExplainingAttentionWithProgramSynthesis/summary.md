# Explaining Attention with Program Synthesis

**Paper:** [Explaining Attention with Program Synthesis (Amiri Hayes, Belinda Z Li, Jacob Andreas, 2026)](https://arxiv.org/abs/2606.19317)

## Human Readable TL;DR

Imagine a translator who can somehow understand a foreign language perfectly, but can't explain their reasoning -- they just "feel" the right answer. That's how attention heads inside large language models work: they decide which words to focus on, but nobody can read out *why*. This paper builds a system that watches an attention head's behavior and then asks another AI to write a short, plain Python program that mimics it -- essentially reverse-engineering the "black box" into readable code. Surprisingly, for a large chunk of attention heads, these short programs work almost as well as the original neural computation, and you can literally swap the program in for the real thing without breaking the model much.

## TL;DR

The authors propose an LM-guided program-synthesis pipeline that generates Python programs approximating individual attention head behavior from observed attention matrices, ranks candidates by Jensen-Shannon Distance and Intersection-over-Union (IoU) on held-out data, and validates them causally by substituting programs for real attention heads during inference. Across GPT-2, TinyLlama-1.1B, and Llama-3B, fewer than ~1,000-4,000 synthesized programs achieve IoU similarity often exceeding 70-79%, and replacing up to 25% of attention heads with their programmatic equivalents increases perplexity by only ~16% while leaving downstream QA benchmark accuracy largely stable. BERT-base (bidirectional) is markedly harder to characterize than the causal/autoregressive models.

---

## Problem & Motivation

Understanding what a trained deep network is actually *computing* remains unsolved. Existing interpretability approaches are either top-down (probing for human-defined concepts) or bottom-up (summarizing activations in natural language), but neither yields "a full, formal description of neural computation." Natural-language explanations in particular cannot be substituted back into the model to causally test whether the explanation is correct.

The authors argue that executable programs occupy a useful middle ground: they are human-readable like natural language, but formally verifiable and directly substitutable into the model like the original weights -- enabling causal validation of an explanation, not just a correlational one. They apply this idea specifically to attention heads in transformer language models, since attention balances "interpretability and simplicity" better than single neurons or whole-model analyses.

---

## Main Original Ideas

1. **LM-guided attention synthesis pipeline.** A four-stage pipeline: (1) extract ground-truth attention matrices from a text corpus, (2) prompt an auxiliary LM (Claude Sonnet 4) to write Python programs that reproduce the top 2.5% of attention weights given only the input text, (3) rank candidate programs by Jensen-Shannon Distance and IoU on held-out data, (4) validate causally by swapping the program's output in for the real attention matrix during a forward pass.
2. **Jensen-Shannon Distance as a synthesis-ranking signal.** JSD(A,Â) = ½KL(A‖(A+Â)/2) + ½KL(Â‖(A+Â)/2) is used to score and select among generated program candidates before the more expensive causal evaluation.
3. **IoU as an attention-alignment metric.** IoU(A,Â) = Σmin(A_ij,Â_ij) / Σmax(A_ij,Â_ij) quantifies how closely a synthesized program's attention pattern overlaps with the real head's pattern.
4. **Causal head-replacement evaluation.** Rather than stopping at correlational similarity, the authors perform interchange interventions -- literally replacing a neural attention head's output with the synthesized program's output during inference -- and measure the effect on perplexity and downstream task accuracy. This is the paper's central methodological contribution: programs are validated as functional surrogates, not just descriptive summaries.
5. **"Best program" vs. "intended program" distinction.** A globally selected best-fit program (searched across the whole synthesized library) consistently outperforms the program that was specifically synthesized and intended for that particular head, suggesting a shared library of program "primitives" recurs across heads.

---

## Key Findings

| Model | Heads | Mean best-program IoU |
|---|---|---|
| GPT-2-small | 144 | ~69% |
| TinyLlama-1.1B | 704 | ~74% |
| Llama-3B | 672 (28 layers) | ~79% |
| BERT-base | 144 (bidirectional) | Significantly lower |

- Fewer than ~1,000-4,000 generated programs (1,664 total across four models) can reproduce attention patterns across GPT-2, TinyLlama-1.1B, and Llama-3B, at ~$150 total API cost using Claude Sonnet 4.
- Fit quality increases with model scale, and autoregressive (causal) models are easier to characterize than bidirectional BERT -- attributed to bidirectional attention's added complexity.
- Replacing up to 25% of attention heads with programmatic equivalents causes only a ~16% average perplexity increase; downstream QA benchmark performance (HellaSwag, PIQA, SciQ, ARC-Easy, Social IQa, COPA) remains stable up to 30-40% head replacement.
- A structural (non-learned) baseline program collapses badly -- perplexity increase exceeds 1000% after just 5% replacement in TinyLlama -- showing the synthesized programs are doing real, non-trivial work.
- Strong negative correlation (Spearman r > 0.9) between IoU and perplexity increase across all models: better-fitting programs cause less behavioral disruption when substituted in.
- Qualitative clustering of GPT-2 head programs shows early layers dominated by "first-token" attention programs, middle layers by syntactic-relationship programs, and later layers by more diverse assignments -- consistent with known hierarchical feature organization in transformers.

---

## Suggestions & Future Directions

1. Pursue a complete symbolic characterization of language models, extending beyond attention heads to other model components.
2. Expand synthesis-strategy diversity and program complexity -- many current high-scoring programs are "not particularly complex," implying shallow characterization rather than a ceiling on what's expressible.
3. Move beyond the current single-round program refinement toward multi-round refinement with richer feedback signals.
4. A substantial fraction of heads (especially in BERT-base) still score below 40% IoU -- closing this coverage gap is an open problem, and the authors attribute most causal degradation at high replacement rates to these poorly-fit heads.
5. Long-term goal: let researchers "reason about model behavior the way they reason about algorithms: by reading, modifying, and testing the underlying logic directly."

---

## Authors & Institutions

Amiri Hayes, Belinda Z Li, Jacob Andreas. (Affiliations not stated in retrieved source; code and data released at https://github.com/AmiriHayes/explaining_attention_heads.)
