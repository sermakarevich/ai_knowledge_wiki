# Language Models are Few-Shot Learners

**Paper:** [Language Models are Few-Shot Learners (Brown et al., 2020)](https://arxiv.org/abs/2005.14165)

## Human Readable TL;DR

Imagine you show a child one example of a new card game and they immediately start playing it well -- that is what this paper achieves with a computer program. The researchers built the largest language AI of its time (GPT-3, 175 billion parameters) and showed that simply making it bigger lets it pick up new tasks from just a handful of examples typed into a prompt, no special re-training needed. This was a breakthrough because previous systems needed thousands of labeled examples to learn each new task, much like needing a whole textbook instead of a single flash card.

## TL;DR

This paper introduces GPT-3, a 175B-parameter autoregressive language model that achieves strong performance on a wide range of NLP benchmarks through in-context few-shot learning -- conditioning on a natural language task description and a few demonstrations at inference time, with no gradient updates. Across dozens of tasks, GPT-3 matches or approaches fine-tuned state-of-the-art results, demonstrating that scaling model size dramatically improves task-agnostic meta-learning capabilities. The work also reveals emergent abilities such as multi-digit arithmetic and word manipulation from minimal examples.

---

## Problem & Motivation

The dominant NLP paradigm at the time was pre-train then fine-tune: train a large language model on general text, then retrain it on thousands of task-specific labeled examples. This created three problems:

1. **Data bottleneck** -- collecting large labeled datasets for every new task is expensive and impractical for the long tail of possible language tasks.
2. **Spurious correlations** -- fine-tuning on narrow distributions causes models to exploit artifacts rather than learn genuine task understanding, leading to poor out-of-distribution generalization.
3. **Lack of human-like adaptability** -- humans learn new language tasks from a few examples or brief instructions; NLP systems could not.

The authors hypothesized that scaling model size could unlock strong in-context learning, removing the need for task-specific fine-tuning altogether.

---

## Main Original Ideas

1. **Extreme-scale in-context learning** -- Training a single 175B-parameter autoregressive model and evaluating it purely through zero-shot, one-shot, and few-shot prompting (no gradient updates), demonstrating that scale is the primary driver of few-shot capability.

2. **Systematic scaling study across eight model sizes** -- Training models from 125M to 175B parameters on the same data and evaluating all on identical benchmarks, providing clear empirical evidence that few-shot performance scales more steeply with model size than zero-shot performance.

3. **High-quality filtered training corpus** -- Constructing a 410B-token dataset by applying classifier-based quality filtering to Common Crawl, fuzzy deduplication, and mixing in curated corpora (WebText2, Books, Wikipedia) with non-proportional sampling favoring quality.

4. **Emergent reasoning on synthetic tasks** -- Demonstrating that GPT-3 can perform multi-digit arithmetic, word unscrambling, and novel-word usage from a few examples -- tasks unlikely to be memorized -- suggesting genuine on-the-fly pattern learning.

5. **Comprehensive data contamination analysis** -- Introducing a systematic N-gram overlap study between training data and evaluation benchmarks, with "clean" subset re-evaluations, setting a precedent for transparency in large-model evaluation.

6. **Broad societal impact analysis** -- Including an extensive section on misuse potential (misinformation, spam), bias (gender, race, religion), and energy consumption, establishing a template for responsible reporting of large model capabilities.

---

## Key Findings

### Benchmark Results (Few-Shot, No Fine-Tuning)

| Task | Metric | GPT-3 (FS) | Previous SOTA | Notes |
|------|--------|-------------|---------------|-------|
| LAMBADA | Accuracy | **86.4%** | 68.0% | +18pp over prior SOTA |
| TriviaQA (closed-book) | Accuracy | **71.2%** | 50.1% (T5-11B) | Matched open-domain fine-tuned SOTA |
| CoQA | F1 | **85.0** | ~90 (fine-tuned) | Within a few points of human performance |
| PIQA | Accuracy | **82.8%** | 79.4% | New SOTA (some contamination noted) |
| SAT Analogies | Accuracy | **65.2%** | 57% (avg. applicant) | Exceeds average college applicant |
| SuperGLUE (avg) | Score | Competitive | BERT-Large | Beat fine-tuned BERT-Large on 4/8 tasks |

### Additional Findings

- **Scaling law extends** -- cross-entropy loss follows a smooth power law across two additional orders of magnitude of compute.
- **Few-shot gap narrows with scale** -- the performance gap between few-shot prompting and fine-tuning shrinks as model size increases, with few-shot scaling more steeply.
- **Arithmetic emergence** -- 100% accuracy on 2-digit addition (few-shot), 80.4% on 3-digit addition, with some generalization to 4-5 digits.
- **News article generation** -- human evaluators could only distinguish GPT-3-generated ~500-word news articles from real ones 52% of the time (near chance).
- **Weaknesses persist** -- poor performance on natural language inference (ANLI, RTE), some reading comprehension tasks (RACE, QuAC), and long-form coherence issues (repetition, self-contradiction).

---

## Suggestions & Future Directions

1. **Bidirectional and denoising objectives** -- Explore architectures beyond autoregressive left-to-right generation (e.g., bidirectional models, fill-in-the-blank training) to improve performance on comparison and inference tasks where GPT-3 struggles.

2. **Multimodal grounding** -- Integrate vision, audio, or physical-world interaction into pre-training to provide richer world knowledge and commonsense understanding.

3. **Pre-training sample efficiency** -- Investigate methods to achieve comparable performance with less training data, reducing both computational cost and environmental impact.

4. **Understanding in-context learning mechanisms** -- Determine whether few-shot performance reflects genuine task learning at inference time or retrieval of patterns absorbed during pre-training.

5. **Model distillation** -- Develop techniques to compress 175B-parameter models into smaller, deployable versions while preserving few-shot capabilities.

6. **Bias and fairness mitigation** -- Address gender, racial, and religious biases inherited from internet-scale training data through improved data curation, debiasing techniques, and evaluation frameworks.

7. **Fine-tuning exploration** -- While this paper focuses on in-context learning, the authors note that fine-tuning GPT-3 could yield further gains and is left for future work.

---

## Authors & Institutions

Tom B. Brown (OpenAI), Benjamin Mann (OpenAI), Nick Ryder (OpenAI), Melanie Subbiah (OpenAI), Jared Kaplan (Johns Hopkins University / OpenAI), Prafulla Dhariwal (OpenAI), Arvind Neelakantan (OpenAI), Pranav Shyam (OpenAI), Girish Sastry (OpenAI), Amanda Askell (OpenAI), Sandhini Agarwal (OpenAI), Ariel Herbert-Voss (OpenAI), Gretchen Krueger (OpenAI), Tom Henighan (OpenAI), Rewon Child (OpenAI), Aditya Ramesh (OpenAI), Daniel M. Ziegler (OpenAI), Jeffrey Wu (OpenAI), Clemens Winter (OpenAI), Christopher Hesse (OpenAI), Mark Chen (OpenAI), Eric Sigler (OpenAI), Mateusz Litwin (OpenAI), Scott Gray (OpenAI), Benjamin Chess (OpenAI), Jack Clark (OpenAI), Christopher Berner (OpenAI), Sam McCandlish (OpenAI), Alec Radford (OpenAI), Ilya Sutskever (OpenAI), Dario Amodei (OpenAI)
