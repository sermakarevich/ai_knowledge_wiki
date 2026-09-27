# Task: chapter 08 — from logits to text: decoding strategies, perplexity, thinking tokens

Read `specs/COMMON.md`, `index.md`, `00_setup.md`, `02_*.md` (cwd `/Users/sergii/.ai/knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks`).

## Code — `src/llm_blocks/ch08_sampling.py`
- From scratch, each as a pure function on a logits vector: `greedy`, `temperature`, `top_k`, `top_p` (nucleus), `min_p`, `repetition_penalty(logits, prev_ids, penalty)`, `presence/frequency` optional. Tests vs `transformers.generation.logits_process` classes (`TemperatureLogitsWarper`, `TopKLogitsWarper`, `TopPLogitsWarper`, `MinPLogitsWarper`, `RepetitionPenaltyLogitsProcessor`) — find 5.16 names.
- `perplexity(logits, targets)` = `exp(mean NLL)`; test on a toy.
- `generate(model_fn, prompt_ids, strategy, max_new)` simple loop usable with a toy bigram "model" (a fixed transition table so tests are deterministic) and with SmolLM2 in `plots_real`.
- `plots`: `08_pipeline.png` (schematic: hidden → LM head → logits → warpers → probabilities → sample), `08_temperature.png` (one realistic 50-token distribution at T 0.2/0.7/1.0/1.5), `08_topk_topp_minp.png` (the same distribution truncated by top-k 10, top-p 0.9, min-p 0.1 — shaded kept mass), `08_repetition_penalty.png`, `08_perplexity_intuition.png` (perplexity as "effective number of choices": a few distributions and their perplexity values), `08_greedy_vs_sampling_tree.png` (a small tree showing why greedy can miss the highest-probability *sequence*).
- `plots_real` (SmolLM2-135M): `08_real_next_token.png` (top-15 next-token probabilities after "The capital of France is" and after a vaguer prompt; two panels), `08_real_entropy_over_text.png` (per-token entropy of the model's prediction along a 40-token sentence — which tokens are predictable); `demo-real` prints 3 completions each with greedy / T 0.7 top-p 0.9 / T 1.5 and the perplexity of one sentence.
- `demo`: numbers for the chapter.

## Chapter — `08_output_and_sampling.md`
The last step of the network (hidden → logits → probabilities, the pipeline figure, tied head recap); greedy decoding and why it is not the best sequence (tree figure); temperature (figure), top-k, top-p, min-p (figure), repetition penalty — what each knob does and typical values (Ollama parameter names `temperature`, `top_k`, `top_p`, `min_p`, `repeat_penalty`, `num_ctx` — map them to the code); the real next-token figure and entropy figure ("the model knows when it is sure"); perplexity as effective number of choices (figure) and as the metric used in `../llm_training/07_export_to_ollama.md` to compare quantised models; stop tokens and the chat template (`<|im_start|>`, `<|im_end|>`) in two paragraphs; "thinking" (`<think>` … `</think>`) is just more sampled tokens before the answer — the Qwen3.8 `enable_thinking` switch is a template change, not a different network; Troubleshooting (all-`<unk>` outputs from wrong template; repeating loops → penalty/temperature; `top_p` after temperature order); Exercises.

## Scope limits
No `index.md` edits.
