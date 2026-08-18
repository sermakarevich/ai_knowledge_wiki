---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Sebastian Raschka on Kimi K3, GLM-5.2, DeepSeek V4 and the Open-Weight AI Explosion

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. Kimi K3 is described as essentially "Kimi Linear, but bigger, with a latent MoE and residual attention bolted on." What concretely changed between the Kimi Linear research prototype and the production Kimi K3 model?

> [!tip]- Answer
> Kimi K3 keeps the same overall architecture as Kimi Linear but scales depth from 27 to 93 transformer layers, and adds two components not present in Kimi Linear: a latent MoE layer that routes to compressed ("latent") experts instead of full-size ones, and a standalone residual-attention module that folds an extra attention pass over earlier blocks into the residual stream. See [[wiki/01-kimi-k3-architecture|Kimi K3's Architecture]].

### Q2. Raschka's "you swap the engine, not reinvent the car" analogy describes the dominant trend in recent open-weight architectures. What is the trend, and which three named implementations does he cite as examples?

> [!tip]- Answer
> The trend is replacing full quadratic self-attention with a cheaper linear/hybrid attention mechanism in most layers while keeping the rest of the transformer skeleton intact. He cites Qwen3-Next's Gated DeltaNet, Kimi's Kimi Delta Attention (which he calls very similar to Gated DeltaNet), and Nemotron's Mamba-2 layers as three implementations of this same underlying swap. See [[wiki/02-architecture-innovations-hybrid-attention|Hybrid Attention and Targeted Architecture Innovations]].

### Q3. Both Kimi K3's latent attention and its latent MoE routing use the same underlying trick. What is that trick, and specifically what does it reduce the cost of in each case?

> [!tip]- Answer
> Both project a larger representation down into a smaller, compressed ("latent") shared form before doing the expensive operation, then expand back out — Raschka compares it to a LoRA-style bottleneck. In latent attention this shrinks the K and V vectors that get stored in the KV cache; in latent MoE the same compression is applied to experts, making them smaller so routing and computation are cheaper. See [[wiki/01-kimi-k3-architecture|Kimi K3's Architecture]].

### Q4. Raschka repeatedly says he can't tell how much of a new model's "feels smarter" improvement is training-layer versus product-layer. What two concrete examples does he give of capabilities he attributes to product engineering rather than new training math?

> [!tip]- Answer
> He points to Codex's computer-use feature (physically controlling the mouse and taking screenshots to operate a computer) and to extracting information from screenshots and other multimodal inputs, both of which he calls "product implementation" rather than a different mathematical training procedure. He also mentions mid-task "steering" as a harness/UX-level improvement in the same category. See [[wiki/03-open-weight-vs-frontier-gap|The Shrinking Open-Weight vs. Frontier Gap]].

### Q5. Why might training a model with RLVR mostly inside its own native coding harness lead to worse performance in other harnesses, and what two symptoms would suggest this is happening rather than just a difference in context management?

> [!tip]- Answer
> If most of RLVR happens in one harness, the model has seen that harness's tool conventions and context structure far more than any other, so it may implicitly specialize in ways that don't transfer even after a brief cross-harness SFT pass at the very end. The two candidate symptoms are using the wrong tool for a given harness, and looping longer than necessary (burning excess tokens) even when it eventually uses the correct tool — though Raschka cautions that higher token usage alone could just reflect a harness's context/compaction engineering rather than true overfitting. See [[wiki/04-harness-model-coupling-and-overfitting|Harness-Model Coupling and the Overfitting Question]].

### Q6. Comparing his DGX Spark and Mac setups for local inference, what tradeoff does Raschka describe, and what throughput/memory figures does he give?

> [!tip]- Answer
> The DGX Spark has about 120GB of unified RAM and can run large MoE models (e.g., Ling S2.1 at roughly 80-90GB) at only 20-30 tokens/sec — usable but not fast, and it essentially maxes out the machine. His Mac M4 runs a smaller MoE model (Qwen3.6-35B-class) much faster, around 60-80 tokens/sec, trading memory capacity/headroom for per-token speed. See [[wiki/05-local-and-self-hosted-inference|Local and Self-Hosted Inference: Hardware and Tradeoffs]].

### Q7. Raschka argues effort-level and model-size selection should be pushed from the user into the harness, and that under-provisioning is the more forgivable mistake. Suppose you were designing an automatic router for a new agentic coding tool: how should this asymmetry between under- and over-provisioning shape its default behavior, and what signals besides the immediate task should it use to decide?

> [!tip]- Answer
> Because starting with a smaller or lower-effort model and escalating if it fails is cheap and natural, while defaulting to the most expensive model wastes money and latency on easy problems, a router should default low and escalate dynamically within a session rather than defaulting high "just in case." It should also draw on more than the current prompt alone — conversation history and accumulated context, not just the task in isolation — since a single message may not reveal how hard the underlying problem really is. See [[wiki/06-inference-time-effort-levels-and-routing|Inference-Time Effort Levels and the Case for Automatic Routing]].

### Q8. What two changes to pre-training does Raschka describe, and what is the actual payoff he says comes from mixing in synthetic data — is it a way to beat larger models, or something else?

> [!tip]- Answer
> He describes dataset scale roughly doubling or tripling to about 30 trillion tokens, alongside a growing proportion of synthetic (model-generated) data, including chain-of-thought-style examples that were rare a few years earlier. The payoff of synthetic data is not that it lets a model beat bigger competitors — trained purely on synthetic data a model "goes in circles" — but that a good mix reaches a usable baseline with fewer iterations, freeing up compute to spend on post-training instead. See [[wiki/07-pretraining-post-training-trends|Pre-Training and Post-Training Trends]].

### Q9. In his recommended learning path for a newcomer working up to reading a model like Kimi K3, Raschka deliberately leaves residual/highway-style attention for last, after attention variants and MoE. Why does this component need to come last rather than being learned alongside the others?

> [!tip]- Answer
> Attention variants and MoE (including their latent versions) are self-contained modules that slot into a single transformer block, so they can be learned and swapped in on their own. Residual/highway attention is instead a cross-cutting connection that reaches back across the whole stack, so it only makes sense once the reader already understands the rest of the architecture it is threading through. See [[wiki/08-outlook-building-blocks-and-next-book|Outlook: Building Blocks, Career Advice, and What's Next]].

### Q10. This entire source is a live, unscripted podcast conversation in which Raschka repeatedly recalls technical-report details (parameter counts, training-cost percentages, specialist counts) from memory of a same-day skim rather than a re-checked citation. How reliable should a reader treat the specific numbers in this source, and what does Raschka's own commentary suggest about how to use them?

> [!tip]- Answer
> Raschka himself repeatedly flags his numbers as uncertain — hedging the Kimi K3/GLM-5.2 parameter counts on air ("I mean, just my brain is also from looking at numbers today"), and explicitly stating that training details in technical reports are often ambiguous, so breakdowns like "nine specialists" are partly "speculation" on his part. A careful reader should treat this source as reliable for the architectural concepts, trends, and reasoning it conveys, but should verify any specific figure (percentages, token counts, parameter counts) against the primary technical reports before citing it as fact. See [[wiki/03-open-weight-vs-frontier-gap|The Shrinking Open-Weight vs. Frontier Gap]] and [[wiki/07-pretraining-post-training-trends|Pre-Training and Post-Training Trends]].
