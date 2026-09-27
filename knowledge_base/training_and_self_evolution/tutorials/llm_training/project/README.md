# llm_training — runnable project

The code behind the [../index.md](../index.md) tutorial. It trains a ~110M-parameter model with the *exact* Qwen3.5/3.8 architecture (hybrid Gated DeltaNet + Gated Attention) from scratch — tokenizer → pre-train → SFT → DPO → GRPO → GGUF/Ollama — and then fine-tunes real Qwen models (4B LoRA, 27B QLoRA) onto a cybersecurity domain, measuring domain accuracy vs general capability and testing the recipes that stop one from collapsing.

Layout: one Python module per stage under `src/llm_tutorial/`, one YAML config per run in `configs/`, one CPU-only test file per chapter in `tests/`, real run artifacts in `runs/`.

## The two machines
| | Mac (this repo) | `rtx` GPU box |
|---|---|---|
| role | edit, tests, git | all GPU work |
| torch | CPU | CUDA, RTX 4090 24 GB (GPU 0) |
| project dir | here | `~/projects/llm_training` (synced by `just push`) |
| artifacts | `runs/` = metrics, plots, samples only | `runs/` **and** `~/.cache/huggingface` = checkpoints, datasets, GGUFs (never synced back) |
| Ollama | over SSH tunnel at `:11435` | systemd service pinned to GPU 0 |

## Quick start
```sh
cd project
just sync          # uv sync — CPU deps on the Mac
just remote-sync   # push code + build rtx's GPU venv (first run downloads ~3 GB)
just check         # rtx GPU visible & bf16 fast; proves there is no GPU on the Mac
just test          # CPU-only suite (2-layer/64-hidden models — no GPU, no network)
```
GPU recipes call `just gpu-free` first (stops idle Ollama models, never busy ones). Long jobs run detached in `tmux` on `rtx` — start with `just remote-bg <name> "<cmd>"`, block with `just remote-wait <name>`, tail with `just remote-log <name>`.

## Stage → recipe → output
| stage | recipe | what it writes (on rtx) |
|---|---|---|
| tokenizer | `just tok-train`, `just tok-compare` | `runs/tokenizer_32k/` (ch 02) |
| sanity | `just sanity-init`, `just sanity-overfit` | loss ≈ ln(vocab), one batch to ~0 loss (ch 03) |
| pretrain | `just pretrain`, `just pretrain-smoke` | `runs/pretrain_110m_fineweb/` → `log.jsonl`, `loss.png` (ch 04) |
| SFT | `just sft`, `just sft-compare` | `runs/sft_110m_smoltalk/` + `runs/models/tiny-qwen35-110m-sft` (ch 05) |
| DPO | `just dpo` | `runs/dpo_110m_uf/` + `runs/models/tiny-qwen35-110m-dpo` (ch 06) |
| GRPO | `just grpo config=…`, `just gsm8k-eval model=…` | `runs/grpo_110m_gsm8k/` (ch 06) |
| export | `just llamacpp-build`, `just export model=… quant=Q8_0`, `just ollama-create name=… gguf=…` | `runs/export/*.gguf` + Ollama model (ch 07) |
| eval | `just eval-general model=…`, `just eval-domain model split`, `just eval-baselines` | `runs/eval_baselines/<model>/metrics.json` (ch 08) |
| fine-tune | `just ft config=…`, `just ft-eval run splits=2000`, `just ablate` | `runs/ft_qwen35_4b_lora/`, `runs/ft_qwen38_27b_qlora/`, `runs/ablation_4b/` (ch 09) |
| forget | `just forget-run config=…`, `just forget-report config=…` | `runs/forget/summary.json`, `tradeoff.png` (ch 10) |

## Where the numbers live
Every run writes `runs/<run>/metrics.json` (plus `loss.png`, `samples.md`, `log.jsonl`). The chapters quote **only** these real numbers, never invented ones. Pull the artifacts back to the Mac with `just pull` — it copies metrics/plots/samples/logs only and `--prune-empty-dirs`, never checkpoints.

## Disk footprint on `rtx` (≈197 GB in `runs/`)
| path | size | what it is |
|---|---|---|
| `runs/models/` | ~132 GB | HF + LoRA checkpoints: tiny base/sft/dpo, 4B & 27B fine-tunes, all forget-grid variants |
| `runs/export/` | ~46 GB | GGUF files (bf16, Q8_0, Q4_K_M) and the Ollama Modelfiles |
| `runs/data/` | ~3.1 GB | tokenized FineWeb-Edu / CyberMetric uint16 shards |
| everything else | <1 GB | metrics, curves, sample generations, logs |

The Mac's `runs/` is small because it holds pulled artifacts only. Checkpoints, datasets and the HF cache never leave `rtx`.
