# MEMENTO: Teaching LLMs to Manage Their Own Context

**Paper:** [MEMENTO: Teaching LLMs to Manage Their Own Context (Kontonis et al., 2025)](https://github.com/microsoft/memento/blob/main/docs/memento.pdf)

## Human Readable TL;DR

Imagine you're solving a long math problem on a whiteboard. Normally, you'd keep everything written out, filling board after board. MEMENTO teaches AI models to pause after each major step, write a compact sticky note summarizing what matters, then erase the whiteboard and keep going with just the sticky notes visible. The AI learns to write these summaries so well that it barely loses accuracy, but uses dramatically less memory -- like carrying a pocket notebook instead of dragging around filing cabinets.

## TL;DR

MEMENTO trains LLMs to segment their chain-of-thought reasoning into blocks, compress each block into a dense "memento" (a state summary targeting ~15--25% of original tokens), and reason forward by attending only to mementos via sparse block masking. Trained on OPENMEMENTOS (228K annotated traces), MEMENTO achieves 2--3x peak KV cache reduction across Qwen3, Phi-4, and Olmo-3 model families (8B--32B) while maintaining strong accuracy on math, science, and coding benchmarks. A dual information stream -- explicit memento text plus implicit KV representations -- carries block information across masked boundaries.

---

## Problem & Motivation

Reasoning models generate thousands of tokens of chain-of-thought before producing answers. This creates a flat, unstructured stream where every past token sits in the attention window at equal cost, and the model has no built-in mechanism to decide what to keep versus compress. A 32K-token CoT is a linear memory burden with no way to mark intermediate results as worth keeping or to compress long derivations into compact conclusions. This leads to growing KV cache requirements that bottleneck inference throughput and limit serving concurrency.

---

## Main Original Ideas

1. **Memento Compression** -- Each reasoning block is compressed into a "memento": a terse, lemma-like state summary preserving definitions, formulas, intermediate values, chosen strategies, and rejected approaches. Unlike traditional summarization, mementos target "lossless compression of reasoning state" at ~15--25% of original tokens while remaining purely extractive (no new derivations or error corrections).

2. **Block Masking via Sparse Attention** -- After a memento is generated, the preceding thinking block is masked from all subsequent attention. The model attends only to the prompt, past mementos, and the current block. This produces a sawtooth KV cache pattern that frees memory as blocks complete, enabling higher batch sizes and throughput.

3. **OPENMEMENTOS Dataset** -- A public dataset of 228K reasoning traces derived from OpenThoughts-v3, segmented and annotated with intermediate summaries via a 4-stage pipeline: sentence splitting, LLM boundary scoring, algorithmic segmentation optimization, and iterative memento generation with judge feedback (achieving 92% pass rate vs. 28% single-pass).

4. **Two-Stage SFT Curriculum** -- Stage 1 trains with full causal attention (learning the block-memento format), then Stage 2 introduces memento attention where preceding thinking blocks are masked after their memento is complete. This curriculum separates format learning from context management.

5. **Dual Information Stream Discovery** -- Mementos carry information through two complementary channels: the explicit summary text and the implicit KV representations computed while the block was still visible. Removing the KV channel (via restart ablation) drops AIME24 accuracy by 15 pp (66.1% to 50.8%), demonstrating that KV states function as compressed pointers into cached reasoning state.

6. **Native vLLM Block Masking** -- A custom vLLM fork that physically removes masked KV entries during generation, achieving 1.75x higher throughput and 1.58x faster batch completion on a single B200 GPU.

---

## Key Findings

| Model | Benchmark | Base | MEMENTO | Delta | Peak KV Reduction |
|-------|-----------|------|---------|-------|-------------------|
| Qwen3-8B | AIME'26 | 54.3 | 45.1 | -7.4 pp | 2.0--2.6x |
| Qwen3-8B | MATH-500 | 90.5 | 90.1 | -0.4 pp | 2.0--2.6x |
| Qwen3-8B | GPQA-D | 61.4 | 55.8 | -2.0 pp | 2.0--2.6x |
| Qwen3-8B | LCB v6 | 73.1 | 66.5 | -3.5 pp | 2.0--2.6x |
| Qwen3-32B | AIME'26 | 62.7 | 48.7 | -2.3 pp* | 1.4x |
| Qwen3-32B | MATH-500 | 91.9 | 91.1 | -0.7 pp | 1.4x |
| Phi-4-r (14B) | AIME'26 | 55.1 | 47.3 | -2.2 pp | 1.3x |
| Phi-4-r (14B) | MATH-500 | 87.3 | 89.7 | +0.9 pp | 1.3x |
| Olmo-3-7B | AIME'26 | 48.3 | 48.1 | -0.2 pp | 0.85--0.93x |

*Qwen3-32B + RL narrows AIME'26 gap further.

- **Accuracy gap shrinks with scale**: from -6.3 pp at 8B to -3.5 pp at 32B (averaged across 5 benchmark groups)
- **Iterative refinement is essential**: single-pass memento generation achieves only 28% judge pass rate; two iterations of feedback bring this to 92%
- **Compression is stable**: memento sizes converge to ~260--615 characters regardless of block length, confirming a learned skill rather than a fixed ratio
- **Majority voting recovers the gap**: at k=2--3 samples, MEMENTO models match or exceed base model pass@1, showing the accuracy drop is a consistency problem, not a capability problem
- **RL improves further**: CISPO on Qwen3-8B raises AIME'26 from 45.1 to 49.4 and Comp. Math from 55.8 to 62.9, while peak KV only rises from 1.08 to 1.48 GB (vs. 2.71 GB vanilla)
- **Serving throughput**: 1.75x higher token throughput at full concurrency (240 requests, 32K max tokens, single B200 GPU)
- **KV probing experiment**: memento KV states from masked positions recover injected 5-digit passcodes at 26.7% (8B) and 23.0% (32B) accuracy vs. 10% chance, confirming the implicit KV channel is architectural (residual stream), not learned

---

## Suggestions & Future Directions

1. **Scale RL to larger models** -- Initial CISPO results on Qwen3-8B are promising; applying RL to 32B+ models could further close the accuracy-compression gap.

2. **Long-horizon agent tasks** -- Extend MEMENTO to agent settings where steps form natural blocks and context windows are the primary bottleneck (e.g., multi-turn tool use, code generation with iterative debugging).

3. **Combine with sliding-window attention** -- The authors demonstrate compatibility with Olmo-3-7B-Think's hybrid architecture; deeper integration with sliding-window methods could yield compounding savings.

4. **Improve the implicit KV channel** -- The dual information stream is a novel finding; future work could explicitly optimize for KV-encoded information retention during training.

5. **Dataset scaling** -- Performance improves monotonically from 1K to 100K examples; the full 228K dataset is released for continued exploration.

---

## Authors & Institutions

Vasilis Kontonis, Yuchen Zeng, Shivam Garg, Lingjiao Chen, Hao Tang, Ziyan Wang, Ahmed Awadallah, Eric Horvitz, John Langford, Dimitris Papailiopoulos -- **Microsoft Research**
