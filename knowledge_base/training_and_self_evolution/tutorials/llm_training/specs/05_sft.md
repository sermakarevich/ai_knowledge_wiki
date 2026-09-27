# Task: chapter 05 — SFT (Supervised Fine-Tuning): chat template, SmolTalk, TRL SFTTrainer, before/after

Read `specs/COMMON.md`, `index.md`, chapters 00–04 first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
`tiny-qwen35-110m-base` (04) completes text; it does not follow instructions. SFT teaches the
chat format and instruction following from example conversations. This chapter introduces the
chat template, the SmolTalk data, TRL's `SFTTrainer` (trl 1.12 — check the installed API with
`uv run python -c "import trl,inspect;print(trl.__version__);print(inspect.signature(trl.SFTConfig))"`
before writing code; do not trust memory of older TRL versions), assistant-only loss masking, and
shows real before/after generations plus evaluation loss.

## Fix

### `project/src/llm_tutorial/chat.py`
- `CHAT_TEMPLATE`: a ChatML template (Qwen style) using our reserved tokens: `<|im_start|>role\n…<|im_end|>\n`, with `{% generation %}` markers around assistant content so TRL's `assistant_only_loss` can mask prompts; `add_generation_prompt` support; a `system` default ("You are a helpful assistant.").
- `attach_chat_template(tokenizer) -> tokenizer` (sets `tokenizer.chat_template`, adds `<|im_start|>`/`<|im_end|>` as special tokens if missing — they already exist from 02 — and sets `eos_token` to `<|im_end|>` for chat models; explain the eos choice in the chapter).
- `render(messages, tokenizer, add_generation_prompt=True) -> str` and `chat(model, tokenizer, messages, max_new_tokens=128, temperature=0.7) -> str` (stops at `<|im_end|>`).
- Chapter explains how the real Qwen3.5 template differs (7.7k-character Jinja with `<think>` handling, `enable_thinking`, tool calls) and shows a rendered example from `Qwen/Qwen3.5-0.8B`'s tokenizer (network on Mac is fine for the tokenizer files; not in tests).

### `project/src/llm_tutorial/sft.py` (Typer CLI)
Config `configs/sft_smoltalk.yaml`: `run_name: sft_110m_smoltalk`, `base: runs/models/tiny-qwen35-110m-base`, `dataset: HuggingFaceTB/smoltalk`, `subsets: [smol-magpie-ultra, smol-constraints, smol-summarize]`, `n_train: 50000`, `n_eval: 1000`, `max_len: 2048`, `packing: false`, `assistant_only_loss: true`, `epochs: 2`, `lr: 1e-4` (full fine-tuning; explain why higher than typical 7B SFT lr 1e-5: tiny model), `warmup_ratio: 0.03`, `schedule: cosine`, `per_device_batch: 16`, `grad_accum: 2`, `bf16: true`, `eval_steps: 200`, `logging_steps: 10`, `seed: 1337`.
- `prepare_dataset(cfg) -> DatasetDict`: load the subsets (`load_dataset("HuggingFaceTB/smoltalk", subset, split="train")`), keep only the `messages` column, filter conversations whose rendered length ≤ `max_len` tokens, shuffle, take `n_train`/`n_eval`. Expose `filter_by_length(ds, tokenizer, max_len)` for tests.
- `train(config)`: `SFTTrainer(model, args=SFTConfig(...), train_dataset, eval_dataset, processing_class=tokenizer)` with `assistant_only_loss=True` (requires the `{% generation %}` markers) — if the installed TRL exposes a different flag name, use it and document; save to `runs/<run>/final` and `runs/models/tiny-qwen35-110m-sft`; write `metrics.json` (train/eval loss curve from `trainer.state.log_history`, wall time, tokens, peak memory) and `loss.png`.
- `compare(base, sft, prompts_file=configs/eval_prompts.yaml)`: 8 fixed prompts (a question, an instruction with a constraint, a summarisation of a short paragraph, a list request, a short arithmetic question, a "who are you", a request for a Python function, a follow-up turn); generate with both models; write `runs/<run>/samples.md` as a two-column comparison. Quote 4 of them verbatim in the chapter.
- Time budget: 50k conversations × 2 epochs on a 110M model ≈ 20–40 min on the 4090; run via `just gpu-free` + `just remote-bg sft …`.

### `project/tests/test_05_sft.py`
`attach_chat_template` + `render` produce the expected ChatML string for a 2-turn conversation; `apply_chat_template(..., return_assistant_tokens_mask=True)` marks only assistant tokens (TRL relies on this); `filter_by_length` drops the long conversation in a 3-row synthetic dataset; `chat()` on the 2-layer test model returns a string and terminates (max_new_tokens 8). No downloads.

### `justfile`: `sft`, `sft-compare`, `chat model=… prompt=…` (remote).

### `05_sft.md` (chapter)
What SFT is and what it is not (it teaches format and behaviour, adds little knowledge); the chat template as a plain string with tokens highlighted, mermaid of the loss mask (prompt tokens masked, assistant tokens trained); SmolTalk (what, licence, why built for small models; one real example conversation); the TRL trainer and the handful of arguments that matter; real loss curve + eval loss; before/after generations (verbatim); an honest note on quality at 110M (it will follow the format and give short plausible answers; facts will often be wrong) and what changes at 4B/27B; how Qwen does SFT (thinking + non-thinking data mixed, "≥75 % reasoning examples to keep thinking mode", from Unsloth's Qwen3.8 notes); Troubleshooting (`assistant_only_loss` errors when the template lacks generation markers; eos never emitted → check `eos_token`; OOM → `max_len`, batch; slow tokenisation → `num_proc`); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/{chat,sft}.py`, `project/configs/{sft_smoltalk,eval_prompts}.yaml`, `project/tests/test_05_sft.py`, `project/justfile`, `project/runs/sft_110m_smoltalk/{metrics.json,samples.md,loss.png}`, `05_sft.md`. Verify token `"What you will learn"`.

## Scope & constraints
Full fine-tuning of the tiny model only (no LoRA yet — that is chapter 09). Do not modify `pretrain.py` or `index.md`.
