# Task: chapter 07 — Export to Ollama: safetensors → GGUF (llama.cpp), quantisation, Modelfile, `ollama create`, chat, template check

Read `specs/COMMON.md`, `index.md`, chapters 00–06 first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
Our models live as Hugging Face safetensors folders on `rtx`. Ollama runs **GGUF** files (the
llama.cpp single-file format with weights + tokenizer + chat template metadata). We need a
repeatable path: build llama.cpp, convert, quantise, write a `Modelfile`, `ollama create`, chat,
and check that the chat template and stop tokens really work. Then measure what quantisation costs.

## Fix

### llama.cpp on `rtx`
Add `just llamacpp-build`: `git clone https://github.com/ggml-org/llama.cpp ~/projects/llama.cpp` (or `git pull`), `cmake -B build -DGGML_CUDA=ON && cmake --build build --config Release -j 24 --target llama-quantize llama-perplexity llama-cli` (CUDA toolkit: the box has nvcc 12.0 at `/usr/local/cuda`; if CUDA build fails, build CPU-only — quantisation and perplexity are fine on CPU for a 110M model — and document it). Install the converter's Python deps into our venv: `uv pip install -r ~/projects/llama.cpp/requirements/requirements-convert_hf_to_gguf.txt` (or `gguf` + `sentencepiece`; record what worked). Record the llama.cpp commit hash in the chapter. **Check support for our architecture**: `grep -n "Qwen3_5\|qwen35\|Qwen3Next" ~/projects/llama.cpp/convert_hf_to_gguf.py`; the Qwen3.5 hybrid (`Qwen3_5ForCausalLM`, `model_type qwen3_5_text`) must be listed. If conversion of the hybrid model fails, convert the dense-fallback model instead if chapter 03 chose it, or document precisely what fails; do not fake a success.

### `project/src/llm_tutorial/export.py` (Typer CLI, runs on rtx)
- `to_gguf(model_dir, out_dir, dtype="bf16")` → runs `python ~/projects/llama.cpp/convert_hf_to_gguf.py <model_dir> --outfile <out>/<name>-bf16.gguf --outtype bf16`; before that, `ensure_chat_template(model_dir)` (the converter embeds `tokenizer.chat_template` into GGUF metadata; our SFT/DPO tokenizers have it from chapter 05; the base model has none — export it without a template).
- `quantize(gguf_in, type="Q8_0"|"Q4_K_M"|"Q5_K_M")` → `llama-quantize`.
- `modelfile(gguf, out_path, system=None, num_ctx=2048, stop=["<|im_end|>", "<|endoftext|>"], temperature=0.7)` writes:
  ```
  FROM ./tiny-qwen35-110m-dpo-Q8_0.gguf
  TEMPLATE """{{ if .System }}<|im_start|>system
  {{ .System }}<|im_end|>
  {{ end }}{{ range .Messages }}<|im_start|>{{ .Role }}
  {{ .Content }}<|im_end|>
  {{ end }}<|im_start|>assistant
  """
  PARAMETER stop <|im_end|>
  PARAMETER num_ctx 2048
  ```
  Explain in the chapter that Ollama can also read the template embedded in the GGUF, but an explicit `TEMPLATE` in Go-template syntax makes the contract visible (show both routes).
- `create(name, modelfile)` → `ollama create <name> -f <modelfile>`; `chat(name, prompt)` → `ollama run <name> "<prompt>"` and/or the HTTP API (`/api/chat`, `stream:false`) via httpx — use the API for the reproducible checks.
- `check_template(name)`: send `[{"role":"user","content":"Reply with exactly the word PONG."}]` and check the response ends without leaking `<|im_start|>`/`<|im_end|>` text and stops; compare the tokens Ollama sends by rendering the same conversation with our HF template (`/api/generate` with `raw:true` shows what raw prompts look like) — the point is proving the two templates agree.
- `perplexity(gguf, text_file)` → `llama-perplexity -m <gguf> -f <file> -c 1024` on 200 kB of `val` text (write it with the tokenizer's decode from `val.bin`, or use a raw text sample saved in chapter 02 — add `data.export_val_text` if needed); also compute HF bf16 perplexity on the same text for the table.
- Names to create in Ollama: `tiny-qwen35-110m-base`, `tiny-qwen35-110m-sft`, `tiny-qwen35-110m-dpo` (each `Q8_0`; plus `Q4_K_M` for the dpo model to compare). Ollama models are stored under `/usr/share/ollama` or `~/.ollama` by the systemd service — `ollama create` handles that; never touch the folders directly.
- These models are tiny; running them in Ollama does not need `gpu-free` (a few hundred MB). Do not unload `qwen3.8:27b` for this chapter.

### `project/tests/test_07_export.py`
`modelfile()` output contains `FROM`, `TEMPLATE`, `stop <|im_end|>` and the given `num_ctx`; `ensure_chat_template` detects presence/absence in a tmp tokenizer dir; `parse_perplexity_output(text)` extracts the number from a canned `llama-perplexity` log; `build_ollama_chat_payload(messages, model)` shape. No subprocess calls in tests.

### `justfile`: `llamacpp-build`, `export model=… quant=…`, `ollama-create name=… gguf=…`, `ollama-chat name=… prompt=…`, `export-check name=…`, `gguf-ppl gguf=…` (all remote).

### `07_export_to_ollama.md` (chapter)
What GGUF is and what is inside (metadata keys incl. `tokenizer.chat_template`; show `gguf-dump` head); llama.cpp build (real commit, time); conversion output (real); quantisation types explained simply (Q8_0, Q5_K_M, Q4_K_M, what "K" and "M" mean, bytes/param) with the real file sizes for our model; the Modelfile line by line; `ollama create`/`ollama list`/`ollama show --modelfile`; a real chat transcript with our model in Ollama; the template check and why a wrong template silently ruins a model (show an intentionally broken template producing garbage — one example); the perplexity table bf16 vs Q8_0 vs Q4_K_M on our 110M model (expect Q8 ≈ lossless, Q4 noticeably worse on a tiny model — explain why small models suffer more); how this maps to how `qwen3.8:27b` in Ollama is packaged (Q4_K_M, ~17 GB, vision projector); the LoRA case (merge first, `ADAPTER` is whitelisted for few architectures) — pointer to chapter 09; Troubleshooting (unsupported architecture in converter; `bos`/`eos` mismatch; endless generation → stop tokens; Ollama pulling the wrong template; `num_ctx`); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/export.py`, `project/tests/test_07_export.py`, `project/justfile`, `project/runs/export/{metrics.json,Modelfile*,chat_samples.md}`, `07_export_to_ollama.md`. Verify token `"What you will learn"`.

## Scope & constraints
Never modify the Ollama service or existing models (`qwen3.8:27b`, `gemma4`, `nomic-embed-text`). GGUF files stay on rtx (`runs/export/*.gguf`, gitignored). Do not change `index.md`.
