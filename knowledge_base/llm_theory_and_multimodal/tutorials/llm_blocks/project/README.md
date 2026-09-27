# llm_blocks

The runnable code behind the [`llm_blocks`](../index.md) tutorial: from-scratch PyTorch
implementations of the building blocks inside a modern LLM (large language model), each one
checked numerically against `torch` / `transformers`, and each figure in the tutorial generated
from this code so every plot is reproducible.

Everything here runs on a Mac CPU in minutes — no GPU needed.

## Install

```
uv sync
```

Requires Python 3.12 and [`uv`](https://docs.astral.sh/uv/getting-started/installation/). Also
uses [`just`](https://just.systems) to run the recipes below
(`curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin`).

## Commands

| Command | What it does |
|---|---|
| `just test` | CPU-only test suite (< 2 min, no network, no downloads); every from-scratch block is compared to its reference with `torch.testing.assert_close` |
| `just test-all` | Same, plus tests marked `slow` (may download a model) |
| `just plots` | Regenerates every chapter's figures into `../assets/` (CPU, no downloads) |
| `just plots-real` | Regenerates the handful of figures that need a small real model (`HuggingFaceTB/SmolLM2-135M`, `Qwen/Qwen3.5-0.8B`); downloads once, then cached in `~/.cache/huggingface` |
| `just clean-assets` | Removes every generated figure from `../assets/` |
| `just lint` | `ruff check src tests` |

## Layout

- `src/llm_blocks/ch<NN>_<name>.py` — one module per chapter, each a Typer app with a `plots`
  command (and `plots-real` / `demo` where relevant).
- `src/llm_blocks/plotting.py` — shared `save()` / `style()` helpers so every figure has the same
  look (130 dpi, consistent colours, tight bbox).
- `src/llm_blocks/reference.py` — lazy CPU loaders for the two real models used across chapters:
  `load_smollm()` (`HuggingFaceTB/SmolLM2-135M`) and `load_qwen35_08b()` (`Qwen/Qwen3.5-0.8B`).
- `tests/test_<NN>_<name>.py` — one test file per chapter.

## Chapter ↔ module table

| Chapter | Module | Test file |
|---|---|---|
| [00_setup.md](../00_setup.md) | `ch00_setup.py` | `test_00_setup.py` |
| [01_neural_networks_in_one_page.md](../01_neural_networks_in_one_page.md) | `ch01_neural_networks.py` | `test_01_neural_networks.py` |
| [02_tokens_embeddings_softmax.md](../02_tokens_embeddings_softmax.md) | `ch02_tokens_embeddings.py` | `test_02_tokens_embeddings.py` |
| [03_attention.md](../03_attention.md) | `ch03_attention.py` | `test_03_attention.py` |
| [04_positional_encoding.md](../04_positional_encoding.md) | `ch04_positional_encoding.py` | `test_04_positional_encoding.py` |
| [05_normalization_and_residuals.md](../05_normalization_and_residuals.md) | `ch05_norm_residual.py` | `test_05_norm_residual.py` |
| [06_mlp_and_moe.md](../06_mlp_and_moe.md) | `ch06_mlp_moe.py` | `test_06_mlp_moe.py` |
| [07_linear_attention_and_deltanet.md](../07_linear_attention_and_deltanet.md) | `ch07_linear_attention.py` | `test_07_linear_attention.py` |
| [08_output_and_sampling.md](../08_output_and_sampling.md) | `ch08_sampling.py` | `test_08_sampling.py` |
| [09_training_dynamics.md](../09_training_dynamics.md) | `ch09_training_dynamics.py` | `test_09_training_dynamics.py` |
| [10_assembling_a_transformer.md](../10_assembling_a_transformer.md) | `ch10_transformer.py` | `test_10_transformer.py` |

See [../Q&A.md](../Q&A.md) for questions that came up while building this (API changes across
`transformers` versions, exact-equivalence caveats, etc.).
