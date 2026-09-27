# Common rules for every `llm_blocks` task

Tutorial folder: `/Users/sergii/.ai/knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks/` (git repo root `/Users/sergii/.ai`).
Read `index.md` first — it is the contract (chapter list, libraries, models, figure rules). Do not change
`index.md` except where a task explicitly allows it.

## Machine
Everything runs on this Mac on CPU. Do not ssh anywhere. Do not use a GPU. Keep every `plots`
command under ~3 minutes on CPU (tiny tensors: hidden ≤ 256, seq ≤ 512 unless the point of the plot is length).

## Chapter style (`NN_name.md`)
- Audience: an ML engineer who has used LLMs but never looked inside. Simple language; explain each
  abbreviation the first time it appears in the chapter (LLM, MLP, GQA, RoPE, KV cache, MoE …).
- Sections: `## What you will learn` (bullets) → numbered sections → `## Troubleshooting` → `## Exercises` (3–5).
- 250–450 lines. Each block: (a) the intuition in 1–2 paragraphs with an everyday analogy, (b) the maths
  in one or two formulas each followed by a plain sentence, (c) the from-scratch code (copied from
  `project/src/llm_blocks/`, ≤ 40 lines per snippet), (d) the figure(s) with a caption that says what to
  look at, (e) "in Qwen3.5/3.8 this is …" with the real config values (hidden 5120, 64 layers,
  24 Q heads / 4 KV heads, head dim 256, DeltaNet 48 V heads / 16 QK heads / head dim 128, SwiGLU
  17408, vocab 248320, partial RoPE 0.25 of head dim, RMSNorm eps 1e-6, context 262144). Verify config
  values with `transformers` (`Qwen3_5TextConfig` defaults or `AutoConfig.from_pretrained("Qwen/Qwen3.5-0.8B")`)
  before quoting them; if unsure, say "for the 0.8B: …" using the value you loaded.
- Figures: `![caption](assets/NN_name.png)`; the file must exist and be produced by the chapter's
  `plots` command. Use `llm_blocks.plotting.save(fig, "NN_name")` (writes `../assets/NN_name.png`
  at 130 dpi, tight bbox, closes the figure). Aim for 3–6 figures per chapter; each one must teach
  one idea (axis labels, title, legend, annotated arrows/text where useful).
- Numbers quoted in the text (timings, parameter counts, losses) must come from actually running the code.

## Code conventions (`project/`)
- One module per chapter: `src/llm_blocks/chNN_<name>.py` with a Typer app exposing `plots`
  (generates all figures for the chapter) and, where meaningful, `demo` (prints the numbers quoted
  in the chapter). Shared helpers: `plotting.py` (`save`, `style()` = consistent colours/figsize),
  `reference.py` (loaders for the two small real models, `load_smollm()`, `load_qwen35_08b()`,
  both lazy, CPU, `dtype=torch.float32`).
- From-scratch implementations are plain `torch.nn.Module`s with type hints and docstrings; no
  clever tricks — readability wins.
- Tests in `tests/test_NN_<name>.py`: CPU-only, no network, < 30 s per file; compare each block to its
  reference with `torch.testing.assert_close(..., rtol=1e-4, atol=1e-5)`. Anything that downloads a
  model is `@pytest.mark.slow` (excluded by default). `plots-real` recipes are allowed to download.
- `justfile` recipes: `test`, `plots` (loop over all `chNN_*` modules), `plots-real`, `lint` (`ruff check`), `clean-assets`.

## Definition of done (every task)
1. `cd project && uv run pytest tests/ -q -m "not slow"` passes; `uv run python -m llm_blocks.chNN_<name> plots` runs and the PNGs exist in `../assets/`.
2. `cd /Users/sergii/.ai && git add knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks/<chapter>.md knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks/assets/NN_*.png knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks/project/<changed files>` (named paths only — never `git add -A`; the repo has an auto-sync job committing other folders) and `git commit -m "llm_blocks: NN_<name> — <one line>"`.
3. Verify: `git show HEAD --stat | grep llm_blocks` lists the chapter, the PNGs and the code; `grep -c "What you will learn" <chapter>.md` = 1.
4. `fleet bd close <this task id>`.
If something in the spec is impossible (API changed, model not loadable), implement the closest thing that works, say so in the chapter's Troubleshooting, and add a line to `Q&A.md` (create it if missing).
