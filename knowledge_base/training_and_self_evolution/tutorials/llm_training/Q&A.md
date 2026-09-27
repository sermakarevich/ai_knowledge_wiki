# Questions & answers

Questions asked while reading this tutorial, with answers grounded in the chapters and the real run numbers (in `project/runs/*/metrics.json`). New entries are appended at the bottom as they come up.

---

## Q: Why not just train a 27B model from scratch?

Because the compute is off by ~7 orders of magnitude. Pre-training a 27B model on ~36 trillion tokens needs the 6·N·D ≈ 5.8e24 FLOPs (chapter 01 `budget` table). At a realistic 40% MFU on one RTX 4090 (~66 TFLOP/s sustained) that is ~24.5 million GPU-hours, i.e. **~2,800 years**. Our 110M model on 1.5B tokens is the *same* 6·N·D formula with a much smaller N and D — ~9.8e17 FLOPs, **~4 hours** on the same GPU. The procedure is identical; only the budget changes. Full-precision training memory is also a wall: ~16 bytes/param × 27B ≈ **401 GB** for weights + gradients + Adam states, which one 24 GB card cannot hold (chapter 01).

## Q: Why 3 linear-attention layers per 1 full-attention layer?

Full attention costs ∝ sequence-length² and its KV cache grows with every token; a linear-attention layer (Gated DeltaNet) keeps a *fixed-size* recurrent state instead, so it is equally cheap at token 10 or token 200,000 — that is what makes a 262k context affordable. But a fixed-size memory *must forget something*, whereas full attention retrieves any earlier token exactly. So the hybrid `linear, linear, linear, full` pattern (`full_attention_interval: 4`) keeps most layers cheap and constant-memory while every fourth layer does exact long-range lookup. In numbers: all 64 layers full attention would cost ~64 GB of KV cache at 262k tokens (≈ three 4090s) versus ~16 GB with the hybrid — that gap is the whole point (chapter 01 §2.5).

## Q: Why does DPO use a smaller learning rate than SFT?

SFT uses `lr: 1e-4`; DPO uses `lr: 5e-6`, 20× smaller (`configs/sft_smoltalk.yaml` vs `configs/dpo_ultrafeedback.yaml`, chapter 06). DPO starts from the already-good SFT model and its loss compares the model's probabilities to a *frozen reference copy* at every step, so it is far more sensitive to the model's starting point. A large step can push the log-ratio into a region where the sigmoid saturates and gradients vanish — or, worse, degrade the fluent SFT behaviour that reference represents. A small, careful step is standard practice for DPO (and GRPO goes lower still, `lr: 1e-6`).

## Q: Why can't lm_eval score MMLU through Ollama, but can score GSM8K the same way?

MMLU is a *loglikelihood* (multiple-choice) task: lm_eval scores it by running a forward pass for each of the 4 answer continuations and taking the one with the highest summed token log-probability. That needs direct access to the model's logits — i.e. `transformers` — not a chat endpoint. Ollama's OpenAI-compatible API only returns generated text and does not expose per-token logprobs, so there is nothing to compare. GSM8K and IFEval are *generative* tasks judged on the free-text output the API does provide, so they run fine through Ollama (`just eval-general-ollama name=qwen3.8:27b`). That is why chapter 08's Ollama baseline row shows MMLU/ARC/HellaSwag/WinoGrande/TruthfulQA as `skipped` and only GSM8K + IFEval as real numbers.

## Q: Which anti-forgetting recipe won, and by how much?

**Replay** — mixing general instruction data into the fine-tuning set — is the only recipe that cleanly works, and `replay_10000` is the model that ships (chapter 10, `runs/forget/summary.json`). Against the untouched base (domain 0.888 / general_mean 0.5781), `replay_2500` reaches domain **0.924** (+3.6 pts) at general 0.6259 (+4.8 pts), and `replay_10000` domain **0.912** (+2.4 pts) at general **0.6442** (+6.6 pts). The honest read: at a sensible learning rate fine-tuning did not really *forget* anything — the only row that lost ground is `naive_lr5e-4`, a too-high LR — so replay's value is buying the best general scores while keeping the domain high, mainly by acquiring *format* (IFEval 23.5 → 49.0). The cheaper tricks sit mid-table: self-distillation and lower LoRA rank barely move, and **merging** (TIES) is the surprise — it matches a ~95-minute replay with essentially no training time.
