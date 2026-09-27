# Training stack research (2026-08-30, live web research by a research agent; condensed)

Read this together with `qwen38_family.md` and `datasets.md`. Where this report and the
pinned versions in `index.md` disagree, **`index.md` wins** — its numbers were checked on PyPI
and on `rtx` on 2026-08-30 (torch 2.13.0+cu130, transformers 5.16.1, trl 1.12.0, peft 0.20.0,
lm_eval 0.4.12, flash-linear-attention 0.5.2, bitsandbytes 0.50.2, liger-kernel 0.8.2).
The web sources below often still quote older versions (torch 2.11, TRL 0.26).

## 1. Pre-training a small model on one GPU

- Reference code: **nanochat** (karpathy, full pretrain→SFT→RL→inference pipeline) and
  **modded-nanogpt** (KellerJordan speed-runs) are the two designs to imitate for a plain
  PyTorch loop; **torchtitan** is multi-GPU only (skip); HF `Trainer` is the simplest fallback.
- Optimizer/schedule: AdamW + warmup + cosine is the safe baseline; **WSD** (warmup–stable–decay,
  used by MiniCPM, Llama-3.1, DeepSeek-V2) is preferred when the token budget is not fixed in
  advance, and linear decay to zero beats a partial cosine decay. **Muon** dominates the
  speed-run leaderboards at small scale → present as the optional "advanced" optimizer.
- Tokens per parameter: Chinchilla's ~20 is routinely exceeded (Llama-2-7B ≈ 290×,
  Gemma-7B ≈ 857×). Our 110M model on 1.5B tokens ≈ 14× → under-trained; say so in chapter 04
  and show the loss is still falling at the end.
- 4090 throughput (LLMQ paper, arXiv 2512.15306): 100M model ≈ 47k tok/s bf16, 500M ≈ 39k tok/s
  bf16 at a 500k-token batch. Rule of thumb: 500M model ≈ 7 h per 1B tokens. Chapter 03's
  benchmark must replace these with measured numbers.
- Kernels: FlashAttention-2 supports Ada (SM89); FA3 is Hopper-only → on the 4090 use PyTorch
  SDPA (which uses FA2-class kernels). `torch.compile` + bf16 + grad accumulation + packing are
  standard. **Liger kernels** (`liger-kernel`, `TrainingArguments(use_liger_kernel=True)` or
  `apply_liger_kernel_to_qwen3()`-style patching) fuse RMSNorm/RoPE/SwiGLU/cross-entropy and cut
  peak memory 40–60 % — the win is largest with a big vocabulary (Qwen's 248k), i.e. for the
  4B/27B fine-tunes, not for the 32k-vocab tiny model.
- Qwen3.5 hybrid layers (Gated DeltaNet) need `flash-linear-attention` (`fla`) and
  `causal_conv1d` for fast kernels; without them transformers silently uses a slow pure-PyTorch
  path (documented, not an error). `fla 0.5.2` installed on rtx (verified); speed is measured in
  chapter 03 and decides hybrid vs the dense `Qwen3` fallback.

## 2. Tokenizer

- `tokenizers.BpeTrainer` trains a byte-level BPE in minutes; known gotcha: the final vocab can
  be slightly smaller than `vocab_size` on large corpora (tokenizers issue #1514) → read the real
  size back and put it into the model config.
- Reusing Qwen's 248k vocabulary on a 100M model would make the embedding table alone
  ≈ 190M parameters (248,320 × 768) — larger than the rest of the network. Hence the 32k custom
  tokenizer in chapter 02; the Qwen tokenizer is only used when fine-tuning Qwen checkpoints.

## 3. Post-training

- TRL: `SFTTrainer`, `DPOTrainer`, `KTOTrainer`, `GRPOTrainer` all current.
- GRPO on one 24 GB card works for 0.5B–4B models. `vllm_mode="colocate"` runs vLLM inside the
  trainer process (fast generation); caveats: hard-coded `MASTER_PORT=12345` (trl #3979) so only
  one colocate job per box, and vLLM's transformers pin can conflict with transformers 5 → the
  tutorial uses plain HF `generate` (slower, zero extra dependencies).
- RLVR algorithm family: GRPO (baseline, critic-free, group-relative advantage), **DAPO**
  (clip-higher + dynamic sampling against entropy collapse), **GSPO** (Qwen; sequence-level
  importance ratios), **Dr. GRPO** (removes length/std normalisation bias — read arXiv paper
  before quoting details). Chapter 06 explains these as "what changes vs GRPO", no implementation.
- Frameworks (single 24 GB GPU): Unsloth fastest / lowest VRAM (custom Triton kernels, ~2× speed,
  ~70 % less VRAM vs HF+FA2); Axolotl most config-driven; LLaMA-Factory most features. The
  tutorial uses TRL + PEFT directly so every step is visible; Unsloth's published 24 GB recipe for
  Qwen3.8-27B (QLoRA, bs 1, ga 4, seq 2048, lr 2e-4) is the reference point for chapter 09.
- Memory: QLoRA (NF4) fine-tunes 33B on 24 GB in the original paper at short sequences; full
  fine-tuning fits ≤ 1–3B; activations dominate at long context → chapter 09's 27B run uses
  `max_len 1024` first.

## 4. Evaluation

- lm-evaluation-harness (`lm_eval` 0.4.12): `--model hf --model_args pretrained=<dir>,dtype=bfloat16`
  for local checkpoints; `--model local-chat-completions --model_args model=<name>,base_url=http://127.0.0.1:11434/v1/chat/completions`
  for Ollama (generative tasks only — no log-probabilities). Gotcha: evaluating a GGUF through
  the `hf` backend without `tokenizer=<hf id>` makes HF rebuild a tokenizer from the GGUF, which
  "can take hours or hang" → always pass the tokenizer. `--limit N` for subsets.
- **lighteval** (HF) is the maintained alternative if a task definition in lm_eval looks stale.
- LLM-as-judge and held-out perplexity (`exp(mean NLL)`) are standard complements — chapter 08.

## 5. Catastrophic forgetting

- *LoRA Learns Less and Forgets Less* (Biderman et al., TMLR 2024, arXiv 2405.09673): LoRA
  under-performs full fine-tuning on the target domain but forgets less out of domain; full FT
  perturbations have 10–100× higher rank than typical LoRA.
- *LoRA Without Regret* (Thinking Machines 2025): LoRA matches full FT when applied to **all**
  linear layers (especially MLP), with lr ≈ 10× the full-FT lr and moderate batch sizes; for RL
  even rank 1 suffices. → chapter 09 default `all-linear`, ablation over targets.
- **mergekit** (Arcee, Apache-2.0): TIES / DARE / SLERP / task arithmetic via YAML; used to merge
  a fine-tuned model back toward its base to undo forgetting. PEFT's `add_weighted_adapter(...,
  combination_type="ties")` covers the adapter-level case without extra packages.
- **Self-Distillation Fine-Tuning** (SDFT, arXiv 2601.19897, Jan 2026): the model teaches itself
  with demonstration-conditioned outputs → much less forgetting than SFT at extra generation cost.
- Replay ratio: 10–30 % general data mixed into the domain set is the commonly cited range;
  **no primary source found** — chapter 10 measures 25 % and 100 % and reports what it sees.

## 6. Export

- llama.cpp `convert_hf_to_gguf.py` lists `qwen35` (hybrid) → build recent `master` with
  `-DGGML_CUDA=ON`; flow: merge LoRA → convert (f16/bf16) → `llama-quantize` Q8_0 (near-lossless)
  or Q4_K_M (best size/quality default), Q5_K_M in between. The `gguf` pip package only
  reads/writes the container.
- Ollama: `ollama create <name> -f Modelfile` with `FROM <gguf>`, `TEMPLATE`, `PARAMETER stop /
  num_ctx`. Do not rely on the converter's embedded chat template — set `TEMPLATE` explicitly and
  verify (chapter 07 `check_template`).

## Flagged as unverified by the researcher

fla/causal_conv1d speed on torch 2.13+cu130 (installed OK; speed measured in ch. 03); the
471M/100 h/25k tok/s blog figure (fp32, source blocked); exact llama.cpp commit adding `qwen35`;
Dr. GRPO details; the replay-ratio percentage.

## Sources

https://github.com/karpathy/nanochat · https://github.com/KellerJordan/modded-nanogpt ·
https://arxiv.org/pdf/2410.06511 · https://github.com/fla-org/flash-linear-attention ·
https://huggingface.co/docs/transformers/model_doc/qwen3_5 · https://arxiv.org/pdf/2512.15306 ·
https://github.com/dao-ailab/flash-attention · https://linkedin.github.io/Liger-Kernel/ ·
https://arxiv.org/pdf/2410.10989 · https://zeroentropy.dev/concepts/learning-rate-scheduler/ ·
https://arxiv.org/pdf/2507.17634 · https://lifearchitect.ai/chinchilla/ ·
https://github.com/huggingface/tokenizers/issues/1514 · https://github.com/huggingface/trl/releases ·
https://huggingface.co/learn/cookbook/grpo_vllm_online_training ·
https://huggingface.co/docs/trl/vllm_integration · https://github.com/huggingface/trl/issues/3979 ·
https://github.com/unslothai/unsloth/issues/4920 ·
https://www.marktechpost.com/2026/07/22/unsloth-vs-axolotl-vs-trl-vs-llama-factory-a-fine-tuning-framework-comparison-on-speed-vram-and-multi-gpu/ ·
https://github.com/EleutherAI/lm-evaluation-harness · https://github.com/huggingface/lighteval ·
https://arxiv.org/abs/2405.09673 · https://thinkingmachines.ai/blog/lora/ ·
https://arxiv.org/pdf/2403.13257 · https://arxiv.org/abs/2601.19897 · https://docs.ollama.com/modelfile ·
https://llm-stats.com/blog/research/post-training-techniques-2026
