---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: KetsuiLabs/MichiAI

### Q1. What is MichiAI and how does full-duplex interaction differ from a serial ASR → LLM → TTS pipeline?
> [!tip]- Answer
> MichiAI is a lightweight multimodal speech LLM designed for full-duplex interaction, meaning it listens and speaks simultaneously like natural human conversation. A serial pipeline transcribes, reasons, then synthesizes in separate stages, while MichiAI hears while it talks, handling interjections and backchanneling implicitly. See [[wiki/01-overview|Overview]].

### Q2. What are MichiAI's headline specs and base backbone?
> [!tip]- Answer
> The advertised spec is 530M parameters with ~80ms time-to-first-audio tested on an RTX 4090, built on a SmolLM-360m backbone. Its architecture is described as continuous embeddings plus rectified flow matching, with single-step decoding and no coherence loss as the key innovation. See [[wiki/01-overview|Overview]].

### Q3. Why does MichiAI use continuous audio latents instead of RVQ decoding?
> [!tip]- Answer
> Traditional RVQ (Residual Vector Quantization) models need slow multi-step token decoding, costing latency and forward passes. MichiAI bypasses RVQ with continuous audio latents plus rectified flow matching, enabling high-fidelity audio with far fewer forward passes and ~80ms time-to-first-audio. See [[wiki/01-overview|Overview]].

### Q4. How do the Listening Head and Speaking Head divide the work?
> [!tip]- Answer
> The Listening Head is a multimodal encoder that maps raw audio into continuous embeddings while simultaneously generating text tokens, covering semantic meaning and emotional context. The Speaking Head predicts audio embeddings with rectified flow matching for fast, diverse speech, then renders them through a lightweight causal HiFi-GAN vocoder for real-time streaming. See [[wiki/01-overview|Overview]].

### Q5. What does the performance table claim against Hertz-dev, Moshi, and Qwen-Omni?
> [!tip]- Answer
> MichiAI at 530M parameters and ~5,000 hours of audio with a continuous approach is contrasted with Hertz-dev (8.5B, 20,000,000 hours), Moshi (7B, 7,000,000 hours), and Qwen-Omni (7B+, 8,000,000+ hours), all listed as quantized. The claim is that it retains text-LLM reasoning without coherence-loss degradation by reusing pretrained text knowledge despite far less size and data. See [[wiki/01-overview|Overview]].

### Q6. What do the two top-level files configure, and what latency figure does the site description state?
> [!tip]- Answer
> The component covers exactly two files: `.gitignore`, which excludes the `dist` build-output directory from version control, and `_config.yml`, which selects the `jekyll-theme-minimal` theme with title `MichiAI`. The site description reads `Full-duplex speech LLM with ~75ms latency.`, which differs slightly from the ~80ms README headline. See [[wiki/02-top-level-files|top-level-files]].

### Q7. Given the roadmap and the repo surface, would you recommend adopting MichiAI for a production voice agent today?
> [!tip]- Answer
> I would not recommend it for production yet, only for prototyping, because scaling to a larger backbone, multilingual support, a live Hugging Face demo, and an API client are all still unchecked on the roadmap. The repo surface is also just a minimal Jekyll docs site with build output excluded, so the claims (reasoning retention, 5,000-hour training, TTFA) need independent verification before any deployment commitment. See [[wiki/01-overview|Overview]].
