# Q&A

Questions that came up while writing (and reading) this tutorial — the things that were not
obvious from the spec, or that changed while the code was being built against a moving
`transformers` version. Chapter Troubleshooting sections cover single-bug fixes; this file is for
questions with a longer answer or that span chapters.

**Q: Is our from-scratch `GatedDeltaNetBlock` really the same computation as `transformers`'
`Qwen3_5GatedDeltaNet`, or just "close enough"?**
A: Numerically the same to `rtol=1e-4`, given the same weights and the same pre-processing.
Chapter 07's test copies all nine weight tensors from a real `Qwen3_5GatedDeltaNet` (built from
`Qwen3_5TextConfig`) into our module and compares outputs directly. The catch is that
`transformers` applies two steps *before* the recurrence when `use_qk_l2norm_in_kernel=True`
(always true for Qwen3.5): L2-normalising `q` and `k`, and scaling `q` by `1/sqrt(d_k)`. Our
`gated_delta_rule_recurrent` does neither on its own — the caller applies them — so a naive
side-by-side comparison without replicating both steps will disagree by a lot. See chapter 07's
Troubleshooting, "Our delta rule and `transformers`' disagree by a lot."

**Q: Chapter 10 claims we "did not approximate anything" loading real Qwen3 weights into our
own blocks — is that really exact, or rounded to some tolerance?**
A: Exact in float32 with `torch.testing.assert_close(rtol=1e-4, atol=1e-5)`, which is tight
enough to catch real bugs (wrong RoPE convention, wrong attention scaling, mismatched norm
convention) but not so tight that it fails on associativity-order floating point noise. In bf16
the same port disagrees by ~1e-2 in the third decimal place — that's bf16's 8-bit mantissa, not
a bug (chapter 10 Troubleshooting, "Off by ~1e-2 instead of ~1e-5").

**Q: Where do `Qwen3RotaryEmbedding` and `apply_rotary_pos_emb` live in `transformers` 5.16?
Older tutorials reference different paths.**
A: `transformers.models.qwen3.modeling_qwen3` for the dense Qwen3 line (chapter 04, chapter 06).
The RoPE base (`rope_theta`) also moved: in 5.16 it lives in `config.rope_parameters["rope_theta"]`
instead of a bare `config.rope_theta` attribute. Code that assumes the old flat attribute raises
`AttributeError: 'Qwen3Config' object has no attribute 'rope_theta'` — read the dict first and
fall back to the old attribute for older configs (chapter 10 Troubleshooting; `decoder_config_from_hf`
in `project/src/llm_blocks/ch10_transformer.py` does this).

**Q: Where does the Gated DeltaNet reference class live, and does the module path match the
dense Qwen3 one?**
A: No — `transformers.models.qwen3_5.modeling_qwen3_5.Qwen3_5GatedDeltaNet`, under `qwen3_5`, not
`qwen3`. Qwen3.5's attention, norm, and RoPE reference classes (`Qwen3_5Attention`,
`Qwen3_5RMSNorm`, `Qwen3_5RMSNormGated`) live there too, separate from the Qwen3 (dense-only)
module used by chapters 03–06 for the plain-attention checks.

**Q: `Qwen/Qwen3.5-0.8B` is documented as a vision-language checkpoint. How does chapter 00's
"text-only real model" load it with `AutoModelForCausalLM`?**
A: `transformers` registers `qwen3_5` model type to a config class that serves both the
vision-language checkpoint and plain text ones. `AutoModelForCausalLM.from_pretrained` maps it to
`Qwen3_5ForCausalLM`, which wraps only the text tower (`Qwen3_5TextModel` + `lm_head`) and lists
`^model.visual.*` in `_keys_to_ignore_on_load_unexpected`. Since the `Qwen/Qwen3.5-0.8B` repo on
the Hub only ships text-tower weights (no vision tower to ignore), loading it this way just works
— no vision weights are expected or downloaded. See `project/src/llm_blocks/reference.py`,
`load_qwen35_08b()`.

**Q: Config numbers (hidden size, layers, heads) differ across the chapters — which ones are
"the" Qwen3.8-27B numbers and which are the small real model's?**
A: Two different models are quoted throughout, and every chapter tries to label which is which:
Qwen3.8-27B-class (hidden 5120, 64 layers, 24 query / 4 KV heads, head dim 256, Gated DeltaNet 48
value heads / 16 QK heads / head dim 128, SwiGLU intermediate 17408, vocab 248320, RMSNorm eps
1e-6, context 262144, partial RoPE = 0.25 × head dim) is the target architecture the tutorial
explains. `Qwen/Qwen3.5-0.8B`, the actually-downloaded real model, has the same block types at
smaller sizes (e.g. 8 query / 2 KV heads). If a number in a chapter looks off from the list above,
check whether it is labelled "for the 0.8B" first — the two are not supposed to match.

**Q: Do all cross-links to `../llm_training/` chapters resolve?**
A: Two do not yet, and that's expected — `llm_training`'s own chapter numbering doesn't fully
line up with `llm_blocks`' cross-references at the time this wrap-up ran: `08_output_and_sampling.md`
links to `../llm_training/07_export_to_ollama.md`, which currently only exists under
`../llm_training/specs/07_export_to_ollama.md` (the spec, not the published chapter — that
chapter has not been promoted out of `specs/` yet). Once `llm_training` publishes that chapter at
the top level, the link will resolve without any change needed on this side.

**Q: Why does `just plots` for chapters 06 and 10 print an "unauthenticated requests to the HF
Hub" warning?**
A: Those two modules call `AutoConfig.from_pretrained("Qwen/Qwen3.5-...")` to read the *real*
config shapes (hidden size, head counts, etc.) so the figures' numbers are never hand-typed. That
downloads a small `config.json` (no model weights) over the network; without an `HF_TOKEN` it
just uses the public unauthenticated rate limit, which is fine for a `config.json`-sized request.
If the network is unavailable, `load_text_config` falls back to `Qwen/Qwen3.5-0.8B`'s cached
config and the figures' numbers refer to that model instead (chapter 10 Troubleshooting).

**Q: Attention output doesn't match `transformers` and `output_attentions=True` returns `None`
— is our attention wrong?**
A: Probably not — check which attention kernel the reference model is using first. Fused kernels
(`sdpa`, `flash_attention_2`) never materialize the full `T × T` attention-weight matrix, so
there is nothing to return for `output_attentions=True`. Load the reference model with
`attn_implementation="eager"` (as `reference.load_smollm()` does) to get real weights back, and
expect it to run slower and use more memory than the fused path (chapter 03 Troubleshooting).

**Q: A from-scratch MoE (Mixture of Experts) trains fine but ends up using only 1-2 experts out
of many — is the routing code broken?**
A: Almost certainly not a bug — this is "expert collapse," the expected default behaviour of
top-k routing without any balancing signal (chapter 06, section 7). Before debugging the router's
forward pass, check whether a load-balancing auxiliary loss is present at all; adding one is a
faster fix than reading through the routing code. Note separately that `torch.topk` is only
differentiable through the *values* it selects, not *which* indices get picked — gradients reach
an expert's weights only when that expert is actually selected, and reach the router's weights
only through the combining weight of already-selected experts.

**Q: I loaded a Qwen3.5 checkpoint's RMSNorm weight into code written for the Qwen3/Llama
convention and nothing crashed, but the model is subtly wrong from the first layer on. Why no
error?**
A: The two conventions parameterise the same idea differently and both produce shape-valid,
plausible-looking tensors: Qwen3/Llama compute `weight * normalize(x)`, Qwen3.5 computes
`(1 + weight) * normalize(x)`. Mixing them up is an "off by one" scale on every channel with no
shape mismatch and no exception — the only symptom is activations that look scaled wrong right
after loading (chapter 05 Troubleshooting, chapter 10's `RMSNorm` also differs cosmetically for
this reason).

**Q: Why do RoPE angles computed directly in bf16 (16-bit floating point) come out wrong, even
though the model itself trains and runs in bf16?**
A: `theta ** (arange(...) / dim)` — the frequency computation behind RoPE — loses precision badly
in low precision, especially for the fastest-varying dimension pairs. `Qwen3RotaryEmbedding.forward`
deliberately computes `cos`/`sin` in float32 and casts down to the model's working dtype only
after `.cos()`/`.sin()`. Computing the whole thing in bf16 up front silently produces inaccurate
angles with no error (chapter 04 Troubleshooting).
