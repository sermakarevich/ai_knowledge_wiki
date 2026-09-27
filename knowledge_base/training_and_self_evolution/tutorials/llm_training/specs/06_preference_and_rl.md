# Task: chapter 06 — Preference optimisation and RL: DPO on UltraFeedback, GRPO on GSM8K with a verifiable reward

Read `specs/COMMON.md`, `index.md`, chapters 00–05 first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
After SFT the model imitates examples. The last two stages of modern post-training make it
*prefer* better answers (DPO — Direct Preference Optimization, from pairs chosen/rejected) and
*optimise a reward* it can verify (GRPO — Group Relative Policy Optimization: sample a group of
answers per prompt, reward each, push probability toward above-average ones). We run both with
TRL 1.12 (`DPOTrainer`, `GRPOTrainer` — inspect the installed `DPOConfig`/`GRPOConfig` signatures
first; APIs moved between TRL versions). Our 110M model will show little GRPO signal, so GRPO is
also run on `Qwen/Qwen3.5-0.8B` where the reward curve visibly rises. Honest numbers matter more
than good numbers.

## Fix

### `project/src/llm_tutorial/dpo.py` (Typer CLI)
Config `configs/dpo_ultrafeedback.yaml`: `run_name: dpo_110m_uf`, `base: runs/models/tiny-qwen35-110m-sft`, `dataset: HuggingFaceH4/ultrafeedback_binarized`, `train_split: train_prefs`, `eval_split: test_prefs`, `n_train: 10000`, `n_eval: 500`, `max_len: 1024`, `max_prompt_len: 512`, `beta: 0.1`, `loss_type: sigmoid`, `lr: 5e-6` (explain: DPO uses much smaller lr than SFT), `epochs: 1`, `per_device_batch: 8`, `grad_accum: 4`, `bf16: true`.
- `prepare_pairs(cfg) -> DatasetDict` with columns `prompt`, `chosen`, `rejected` in the conversational format TRL expects (lists of messages), filtered by length; `to_pairs(row) -> dict` pure and tested.
- `train(config)`: `DPOTrainer(model, ref_model=None (TRL makes a frozen copy), args=DPOConfig(...), …)`; save `runs/models/tiny-qwen35-110m-dpo`; metrics: `rewards/chosen`, `rewards/rejected`, `rewards/margins`, `rewards/accuracies` from `log_history` → `metrics.json` + `dpo.png` (margin and accuracy vs step). Runtime ≈ 20–30 min.
- Also implement `loss_type: ipo` and `orpo`-style option only if TRL exposes them trivially (a config string); otherwise just describe ORPO/SimPO/KTO in the chapter.

### `project/src/llm_tutorial/grpo.py` (Typer CLI)
Configs `configs/grpo_gsm8k_110m.yaml` (`base: runs/models/tiny-qwen35-110m-dpo`) and `configs/grpo_gsm8k_qwen35_0.8b.yaml` (`base: Qwen/Qwen3.5-0.8B`, load with `AutoModelForCausalLM` — the checkpoint is the multimodal `Qwen3_5ForConditionalGeneration`; if `AutoModelForCausalLM` cannot load text-only, load the full model and use its language model, or use the `-Base`/text variant if one exists; document what worked). Common keys: `dataset: openai/gsm8k` (`main`, split train; eval on 300 test problems), `system_prompt` asking for reasoning then a final line `Answer: <number>`, `max_prompt_len: 512`, `max_completion_len: 256`, `num_generations: 8`, `per_device_batch: 8`, `grad_accum: 2`, `lr: 1e-6` (0.8B: use LoRA r=32 on all linear layers so it fits and trains quickly; 110M: full), `beta: 0.0` (no KL) — mention `beta 0.04` as classic, `steps: 300` (110M) / `400` (0.8B), `bf16`, `temperature 1.0`, generation with plain HF `generate` (no vLLM; note vLLM colocate mode exists in TRL and why we skip it on one 24 GB card).
- Reward functions (pure, tested): `extract_answer(text) -> str|None` (last `Answer:` line or last number), `correctness_reward(completions, answer) -> list[float]` (1.0 exact numeric match after stripping commas/`$`, else 0.0), `format_reward` (0.2 if the `Answer:` line exists). Pass both to `GRPOTrainer(reward_funcs=[...])`.
- `evaluate(model_dir, n=300) -> accuracy` greedy on GSM8K test with the same prompt (used before and after; also used by chapter 08).
- Metrics: reward mean/std, `frac_reward_zero_std` (groups with identical rewards give no gradient — explain), completion length, KL if any, eval accuracy before/after → `metrics.json`, `reward.png`.
- Runtime: 110M ≈ 20–30 min, 0.8B LoRA ≈ 60–90 min. Use `just gpu-free` + `remote-bg`, poll every 20 min.

### `project/tests/test_06_rl.py`
`to_pairs` on a synthetic UltraFeedback-shaped row; `extract_answer` on 6 formats (`Answer: 42`, `#### 42`, `$1,234`, trailing text, none); `correctness_reward` and `format_reward` values; a 3-step `DPOTrainer` and a 2-step `GRPOTrainer` run on the 2-layer test model with 4 synthetic rows each (CPU, `num_generations 2`, `max_completion_len 8`) finishing without error and producing `log_history` (mark these two tests `slow` ONLY if they take > 40 s on the Mac; try to keep them fast).

### `justfile`: `dpo`, `grpo config=…`, `gsm8k-eval model=…`.

### `06_preference_and_rl.md` (chapter)
Why imitation is not enough; preference data (a real chosen/rejected pair, shortened); the DPO loss in one formula and one sentence per symbol (β, reference model, log-ratio), what `rewards/accuracies` means; real DPO curves and a before/after generation; the RL stage: reward model vs verifiable reward, GRPO algorithm as a mermaid flow (prompt → G samples → rewards → group-normalised advantages → policy update), the 110M result (probably ~0–3 % GSM8K, flat or noisy reward — say so) vs the 0.8B result (reward and accuracy before/after with numbers), completion length dynamics; refinements in 2025–26: DAPO (clip-higher, dynamic sampling, token-level loss, overlong shaping), Dr. GRPO (remove length/std bias), GSPO (sequence-level ratios, Qwen's choice for Qwen3), and how Qwen3 was post-trained (long-CoT cold start → reasoning RL → thinking-mode fusion → general RL); Troubleshooting (all rewards equal → increase temperature/num_generations; OOM → `max_completion_len`; reward hacking on format; loading the multimodal 0.8B checkpoint); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/{dpo,grpo}.py`, `project/configs/{dpo_ultrafeedback,grpo_gsm8k_110m,grpo_gsm8k_qwen35_0.8b}.yaml`, `project/tests/test_06_rl.py`, `project/justfile`, `project/runs/{dpo_*,grpo_*}/{metrics.json,*.png,samples.md}`, `06_preference_and_rl.md`. Verify token `"What you will learn"`.

## Scope & constraints
No vLLM, no multi-GPU, no reward-model training. Do not change `index.md`, `sft.py`, `pretrain.py`. The `Qwen/Qwen3.5-0.8B` download (~1.6 GB) goes to `~/.cache/huggingface` on rtx only.
