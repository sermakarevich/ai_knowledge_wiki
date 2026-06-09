# Models

Specific **LLM and multimodal model releases** — flagship and frontier model cards, technical reports, and architectural release notes (e.g. MoE, Mamba-Transformer hybrids, omnimodal stacks). Architecture-only and theory papers live in `llm_theory_and_multimodal`; Anthropic-specific cards live in `claude_ecosystem`.

## Papers

- [[AnImageIsWorth16x16Words/summary]] — Vision Transformer (ViT): 16x16 patches + standard Transformer; matches/beats CNNs at scale.
- [[HyperloopTransformers/summary]] — Combines looped (recurrent-depth) Transformers with hyper-connections (loop-boundary matrix residuals) for ~50% parameter reduction with competitive or better performance; diagonal transition matrices and loop position embeddings improve quantization robustness at scales up to 2B.
- [[IntroducingMuseSpark]] — Meta's natively multimodal reasoning model with Contemplating Mode; 58% on HLE, >10x compute efficiency vs Llama 4.
- [[LanguageModelsAreFewShotLearners]] — GPT-3 (175B): scaling enables strong few-shot in-context learning across NLP tasks without fine-tuning.
- [[Nemotron3Super/summary]] — 120B/12B active MoE hybrid Mamba-Transformer achieving 7.5x higher throughput via LatentMoE routing, MTP speculative decoding, and NVFP4 end-to-end 4-bit pre-training on 25T tokens.
- [[Qwen35Omni/summary]] — Fully omnimodal (text/image/audio/video in, text+speech out) with Thinker-Talker + ARIA streaming.
- [[Qwen36-35B-A3B/summary]] — Open-weight sparse 35B-total/3B-active MoE multimodal model with novel Gated DeltaNet hybrid attention and MTP training; 73.4% SWE-bench Verified, runs on single RTX 4090.
