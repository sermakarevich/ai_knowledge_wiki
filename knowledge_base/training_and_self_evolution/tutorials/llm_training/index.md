# LLM training and fine-tuning tutorial — from a random model to a domain expert served by Ollama

A from-zero, hands-on tutorial on how a modern **LLM** (Large Language Model — a neural network that predicts the next token of text) is built and trained, and how a finished model is fine-tuned to a topic without forgetting what it knew. The reference model family is **Qwen3.8 / Qwen3.5** (Alibaba's open-weight models; `qwen3.8:27b` is the model this knowledge base already runs in Ollama). Everything is done for real on one **NVIDIA RTX 4090 (24 GB)**:

1. **Part A — training from scratch.** We build a small (~110M parameter) model with the *exact* Qwen3.5/3.8 architecture (hybrid Gated DeltaNet + Gated Attention layers, SwiGLU, RMSNorm, RoPE), train a tokenizer, pre-train it on real web text, then run the modern post-training pipeline — SFT (Supervised Fine-Tuning) → DPO (Direct Preference Optimization) → GRPO (Group Relative Policy Optimization, reinforcement learning with a verifiable reward) — and finally export it to **GGUF** and chat with it in **Ollama**.
2. **Part B — fine-tuning a real model to a domain.** We take pretrained Qwen3.5-4B (fast loop) and Qwen3.8-27B (QLoRA capstone), fine-tune them on a cybersecurity question set, and measure what matters: **domain accuracy** vs **general-capability benchmarks before and after**, and the techniques that keep the second one from collapsing (catastrophic forgetting).

Why not train a 27B model from scratch? Qwen3 was pre-trained on ~36 *trillion* tokens; a 27B model needs roughly 6·N·D ≈ 6 × 27e9 × 36e12 ≈ 5.8e24 FLOPs. One RTX 4090 sustains ≈ 1.5e14 FLOP/s in bf16 with good utilisation, i.e. ≈ 1,200 years. Chapter 01 walks through this arithmetic; the point of Part A is that the *procedure* is identical at 120M and at 27B — only the budget changes.

Retrieve chapters with `ai show research_topics/training_and_self_evolution/tutorials/llm_training/<chapter>`.

## Chapters (read in order)
- [00_setup.md](00_setup.md) — the two machines (Mac + `rtx` GPU box), `uv`, `just`, project layout, `.env`, syncing code to the GPU with `just push` and running there with `just remote`, sharing the GPU with Ollama, `just check` (GPU visible, bf16 speed).
- [01_concepts.md](01_concepts.md) — what an LLM computes; every component of the Qwen3.5/3.8 architecture explained (tokens → embeddings → [RMSNorm → Gated DeltaNet or Gated Attention → SwiGLU MLP] × N → LM head); parameter and FLOP counting; the full modern training pipeline (pre-training stages → SFT → preference optimisation → RL) and what each stage adds; why full-precision training of 27B is impossible on one GPU and what LoRA/QLoRA change.
- [02_tokenizer_and_data.md](02_tokenizer_and_data.md) — tokenizers (BPE, vocabulary size vs embedding parameters), training our own 32k tokenizer vs reusing Qwen's 248k one, streaming FineWeb-Edu, tokenising and packing into fixed-length training blocks, token budgets (Chinchilla).
- [03_model_from_scratch.md](03_model_from_scratch.md) — instantiating the tiny Qwen3.5-architecture model from a config, reading its module tree, forward pass and cross-entropy loss, the sanity checks every training run needs (initial loss ≈ ln(vocab), overfit one batch).
- [04_pretraining.md](04_pretraining.md) — the training loop: AdamW, warmup + cosine (and WSD) schedules, gradient clipping, bf16 autocast, `torch.compile`, gradient accumulation, checkpoints; tokens/second and memory on the 4090; loss/perplexity curves from the real ~2-hour run; sample generations as training progresses.
- [05_sft.md](05_sft.md) — turning a text-completer into an assistant: the chat template, SmolTalk, TRL `SFTTrainer` with assistant-only loss, before/after generations and evaluation loss.
- [06_preference_and_rl.md](06_preference_and_rl.md) — DPO on UltraFeedback (TRL `DPOTrainer`), then GRPO on GSM8K with a verifiable reward (TRL `GRPOTrainer`) — run on our tiny model (little signal, honest numbers) and on Qwen3.5-0.8B (visible reward curve); what DAPO/GSPO change and why RL is the last stage.
- [07_export_to_ollama.md](07_export_to_ollama.md) — HF safetensors → GGUF with llama.cpp (`convert_hf_to_gguf.py`, `llama-quantize` Q8_0/Q4_K_M), the Ollama `Modelfile` (TEMPLATE, stop tokens, num_ctx), `ollama create`, chatting with our own model, checking the chat template is right, perplexity cost of quantisation.
- [08_evaluation.md](08_evaluation.md) — how models are measured: `lm-evaluation-harness` (MMLU, ARC, HellaSwag, WinoGrande, TruthfulQA, GSM8K, IFEval) with `--limit` for speed, evaluating an HF checkpoint and an Ollama model through its OpenAI-compatible API, our domain harness (CyberMetric multiple-choice exact match), LLM-as-judge with the local `qwen3.8:27b` judge, the `metrics.json` every later run writes.
- [09_domain_finetuning.md](09_domain_finetuning.md) — fine-tuning a real model to a topic: Qwen3.5-4B LoRA on CyberMetric (baseline → fine-tuned → domain accuracy + general benchmarks), then the same with Qwen3.8-27B QLoRA inside 24 GB; a small ablation table (learning rate, LoRA rank, epochs, target modules).
- [10_forgetting_and_merging.md](10_forgetting_and_merging.md) — catastrophic forgetting measured, then mitigated: replay/mixing general instruction data, lower learning rate and fewer epochs, LoRA rank, self-distillation, model merging (TIES/DARE with `mergekit`); the domain-vs-general trade-off table; exporting the final domain model to Ollama; production checklist.
- [Q&A.md](Q&A.md) — questions asked while reading, with answers (appended over time).

## Runnable project
`project/` — `pyproject.toml` (uv, Python 3.12, package `llm_tutorial` under `src/`), `justfile`, `.env.template`, `configs/*.yaml` (one per model/run), `src/llm_tutorial/` (one module per stage), `tests/` (CPU-only, tiny configs, no GPU/network), `runs/` (metrics, curves and sample generations pulled back from the GPU box — checkpoints stay on `rtx`). Start with `cd project && just sync && just check`.

`specs/` holds the build instructions and research notes used by the fleet workers that wrote this tutorial (one spec per chapter, `COMMON.md` shared rules, `research/` sources with links). It is not part of the reading path.

## The two machines (shared by all chapters — never change these)
| setting | value |
|---|---|
| Mac (where you edit, run tests, keep git) | this repository, `~/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training/project` |
| GPU box | ssh alias `rtx` (`~/.ssh/config`), Ubuntu 24.04, **RTX 4090 24 GB** (GPU 0; a GTX 1080 Ti 11 GB is GPU 1 and is not used), 62 GB RAM, 32 cores, CUDA driver 580 |
| project directory on `rtx` | `~/projects/llm_training` (mirror of `project/`, kept in sync with `just push`) |
| checkpoints / datasets / HF cache on `rtx` | `~/projects/llm_training/runs/` and `~/.cache/huggingface` (never synced back) |
| Ollama on `rtx` | systemd service, pinned to the 4090, `OLLAMA_CONTEXT_LENGTH=98304`; `qwen3.8:27b` takes ~17 GB of VRAM while loaded → `just gpu-free` (`ollama stop qwen3.8:27b`) before any training |
| Ollama from the Mac | `http://127.0.0.1:11435` through the SSH tunnel (`fleet tunnel`), same as the graph_rag tutorial |
| Python | 3.12 via `uv` on both machines; `torch` 2.13 (CUDA 13 wheels on `rtx`, CPU wheels on the Mac), `transformers` 5.16, `trl` 1.12, `peft` 0.20, `datasets` 5.0, `lm_eval` 0.4.12, `bitsandbytes` 0.50 (Linux only) |
| llama.cpp on `rtx` | built from source in `~/projects/llama.cpp` (chapter 07) |

All `.env` values are read from `project/.env` (copy `project/.env.template`); `.env` is gitignored.

## Models (shared by all chapters)
| name | what | used in |
|---|---|---|
| `tiny-qwen35-110m` | our own model, Qwen3.5 text architecture (`Qwen3_5TextConfig`: 12 layers in 3 linear-attention : 1 full-attention pattern, hidden 768, SwiGLU 2048, 12 heads / 2 KV heads, tied embeddings, own 32k tokenizer), ≈110M parameters (84M non-embedding + 24.6M tied embedding), trained from random init | 03–08 |
| `Qwen/Qwen3.5-0.8B` | smallest pretrained Qwen3.5 (Apache-2.0) — GRPO with visible signal | 06 |
| `Qwen/Qwen3.5-4B` | pretrained, LoRA fine-tuning fits comfortably in 24 GB | 08–10 |
| `Qwen/Qwen3.8-27B` | the target-class model (Apache-2.0, dense, 64 layers, 262k context); QLoRA only — 4-bit weights ≈ 15–19 GB, 16-bit LoRA needs > 36 GB | 09–10 |
| `qwen3.8:27b` (Ollama) | LLM-as-judge and reference answers | 08–10 |

## Datasets (shared by all chapters)
| stage | dataset | licence | how much we use |
|---|---|---|---|
| pre-training | `HuggingFaceFW/fineweb-edu`, config `sample-10BT` (streamed) | ODC-BY | ≈1.5B tokens (≈14 tokens per parameter; Chinchilla-optimal is ≈20) |
| smoke pre-training | `roneneldan/TinyStories` | CDLA-Sharing-1.0 | a 10-minute run to test the loop |
| SFT | `HuggingFaceTB/smoltalk` (`smol-magpie-ultra` + `smol-constraints` + `smol-summarize`) | Apache-2.0 | ≈50k conversations |
| DPO | `HuggingFaceH4/ultrafeedback_binarized` | MIT | ≈10k pairs |
| GRPO | `openai/gsm8k` | MIT | train split (7.5k), reward = exact numeric answer |
| domain fine-tuning | `tihanyin/CyberMetric` (cybersecurity 4-option multiple choice, 9 sub-domains) | Apache-2.0 | train on `CyberMetric-10000` minus any question that also appears in `CyberMetric-2000`; evaluate on `CyberMetric-2000` (and `-500` for quick runs) |
| general capability | `lm_eval` tasks `mmlu`, `arc_challenge`, `hellaswag`, `winogrande`, `truthfulqa_mc2`, `gsm8k`, `ifeval` | various | `--limit` per task, fixed in `configs/eval_general.yaml` |

Alternative domain to try afterwards (exercise, not run in the chapters): `neo4j/text2cypher-2025v1` (Apache-2.0, natural-language question + graph schema → Cypher), evaluated by normalised exact match and by `EXPLAIN` against the Neo4j instance of the `neo4j` tutorial.

## Conventions
- Every run has a YAML config in `configs/` and writes `runs/<run_name>/metrics.json` (+ `loss.png`, `samples.md`) — chapters quote these real numbers, never invented ones.
- Long GPU jobs run detached on `rtx` in `tmux` (`just remote-bg <name> "<cmd>"`, `just remote-log <name>`) so an SSH drop never kills training.
- `uv run pytest tests/ -q` must pass on the Mac with no GPU and no network: tests use 2-layer/64-hidden configs and tiny synthetic data. GPU tests are `@pytest.mark.slow`.

Related reading in this knowledge base: `ai show research_topics/graph_rag/tutorials/graph_rag` (uses `qwen3.8:27b` through Ollama), `ai show research_topics/graph_rag/tutorials/neo4j`.

Verified on: RTX 4090, driver 580.173, Ubuntu 24.04, Ollama 0.32.12, transformers 5.16.1, trl 1.12.0, 2026-08-30.

Verified on: RTX 4090, driver 580.173, Ubuntu 24.04, Ollama 0.32.12, transformers 5.16.1, trl 1.12.0, 2026-09-07 — chapter 10 exported `cyber-qwen35-4b` and `cyber-qwen38-27b` to Ollama.
