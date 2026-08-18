# Sebastian Raschka on Kimi K3, GLM-5.2, DeepSeek V4 and the Open-Weight AI Explosion

**Video:** [Sebastian Raschka on Kimi K3, GLM-5.2, DeepSeek V4 and the Open-Weight AI Explosion](https://www.youtube.com/watch?v=pEf21w0r-vY) — Vanishing Gradients, ~79 min
**Wiki:** [[index]]

## Human Readable TL;DR

Sebastian Raschka (author of *Build a Large Language Model from Scratch* and the new *Build a Reasoning Model from Scratch*) joins the Vanishing Gradients podcast on the day Kimi K3's weights dropped, to make sense of three wild months of open-weight AI releases (DeepSeek V4, GLM-5.2, Qwen 3.5/3.6, and now Kimi K3). The big picture: open-weight models keep closing the gap on the proprietary frontier, but the "wins" are less about raw brains and more about product polish (computer use, image understanding, steering), targeted architecture tweaks (compressed attention, mixture-of-experts routing, extra residual paths), and how tightly a model is fitted to its own coding-agent harness. Raschka also talks through when it actually makes sense to run a model on your own hardware versus paying for a subscription, and closes with career advice: treat the field as a marathon, learn the building blocks in order, and don't chase every release.

## TL;DR

A wide-ranging interview tracing three months of open-weight LLM progress (DeepSeek V4 → GLM-5.2 → Qwen 3.5/3.6 → Kimi K3) through the lens of architecture, product, and workflow. Kimi K3 is dissected live as "Kimi Linear, but bigger, with a latent MoE and residual attention bolted on" — part of a broader shift from full quadratic attention toward hybrid/linear attention (Gated DeltaNet in Qwen3-Next, Kimi Delta Attention, Mamba-2 layers in Nemotron) and from dense MoE toward *latent* MoE (compressed expert routing, as in NVIDIA's Nemotron 3 Ultra). Raschka argues most of the apparent "smarter model" gains from frontier labs are actually product-layer improvements (computer use, steering, multimodal understanding) rather than new training math, and warns that models are increasingly RLVR-trained inside their *own* coding harness, making cross-harness performance an open question. On infrastructure, he contrasts a DGX Spark (great for maxing out big local MoE models at ~20-30 tok/s) against a Mac M4/M5 (faster per-token, less headroom) and argues privacy, not raw capability, is the main reason to go local today. On training trends: pre-training datasets have grown to roughly 30T tokens (2-3x last year), increasingly mixed with synthetic data to reach a usable baseline faster, while post-training has become a multi-stage SFT→RLVR→SFT→RLHF pipeline that also trains distinct "effort level" specialists (e.g. Kimi K3's reported light/medium/high-effort specialists per domain) which then get distilled into one model. He closes by suggesting the harness itself — not the user — should decide model size and effort level dynamically, an idea he has not seen implemented yet.

---

## Problem & Motivation

This is a conversation, not a research paper, so there is no single research problem — the motivating question is: *what actually changed in open-weight LLMs in the roughly three months between this and the previous Vanishing Gradients episode, and how should a practitioner make sense of it?* The releases in that window were DeepSeek V4, GLM-5.2, Qwen 3.5 and 3.6 (preview), and — hours before this recording — Kimi K3. The conversation's implicit thesis: open-weight/proprietary release cadence has compressed from 6-9 months to a few weeks, so keeping up model-by-model is no longer viable; the useful move is to track a small number of recurring architectural and workflow trends instead.

---

## Main Original Ideas

1. **Kimi K3 = Kimi Linear + latent MoE + residual attention.** Kimi K3 is architecturally almost a drop-in scale-up of the earlier Kimi Linear research prototype (27 → 93 layers), with a compressed ("latent") MoE routing layer analogous to NVIDIA Nemotron 3 Ultra's LatentMoE, plus a standalone "residual attention" trick borrowed from the Kimi Linear paper.
2. **The hybrid/linear-attention wave is the dominant architectural trend.** Qwen3-Next's Gated DeltaNet, Kimi's Kimi Delta Attention, and Nemotron's Mamba-2 layers are all variations on replacing full quadratic self-attention with a cheaper linear-attention mechanism in most layers — described as "swapping the engine, not reinventing the car."
3. **Model + harness co-evolution risks overfitting.** Models trained with RLVR largely inside their own native coding harness (Qwen Code, Kimi's CLI, Claude Code) appear to perform best in that harness and may be quietly overfitting to it — plausible symptoms are incorrect tool use and unnecessarily long reasoning/tool loops outside that harness.
4. **Most "the new model feels smarter" gains are product-layer, not training-layer.** Computer-use (mouse/screenshot automation in Codex), conversational steering mid-task, and harness-awareness (a model knowing about a UI's "right-hand panel") are framed as product engineering, not evidence of a new training procedure.
5. **Effort-level control is becoming a first-class, trainable axis.** Beyond choosing a model size, frontier and open-weight labs now train explicit "effort" specialists (light/medium/high) via RLVR with token-budget penalties, then distill them into one model selectable via system prompt — but no one has yet made the *harness* pick the effort level automatically based on context.
6. **Local inference is now mainly a privacy and hobby choice, not a capability necessity.** With subscriptions "relatively cheap," Raschka uses local models chiefly for sensitive/private queries and for the satisfaction of using owned hardware, not because local models outperform hosted ones.
7. **Learn architectures as a timeline, not in isolation.** Because modern architectures (K3-class models) would take "thousands of lines of code" to implement from scratch in one pass, Raschka argues understanding them requires tracing the lineage from GPT-2 forward, one added component at a time (attention → MoE → multi-head latent attention → hybrid/linear attention → residual/highway tricks).

---

## Key Findings

| Item                                                                            | Detail (as discussed in the conversation)                                                                                                                                                                                                |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Kimi K3 vs. Kimi Linear (research prototype)                                    | 93 transformer layers vs. 27; adds a latent MoE layer and a "residual attention" module not present in Kimi Linear                                                                                                                       |
| Residual attention overhead (per the Kimi Linear paper, as recalled by Raschka) | ~4-5% added training cost, ~2-3% added inference cost, described as a modeling-quality tweak rather than an efficiency tweak                                                                                                             |
| DeepSeek V4 "highway connections"                                               | Popularized (not invented) by DeepSeek V4: multiple (recalled as four) parallel residual paths instead of one                                                                                                                            |
| Model scale (as recalled live from the reports, approximate)                    | GLM-5.2 ≈ 2.7T total parameters; Kimi K3 ≈ 2.8T-class, i.e., roughly comparable in the "very large MoE" tier                                                                                                                             |
| Pre-training data volume                                                        | ≈30 trillion tokens is now roughly the norm for large frontier-class training runs — about 2-3x the typical size from a year earlier                                                                                                     |
| Local hardware: DGX Spark                                                       | ~120 GB unified RAM; a 35B-class MoE model uses ~80-90 GB even at long context; throughput ~20-30 tokens/sec, "usable" but not fast                                                                                                      |
| Local hardware: Mac (M4/M5)                                                     | Qwen3.6-35B-class MoE model: ~60-80 tok/s on M4, reported ~120 tok/s on M5 in a colleague's setup; substantial RAM headroom on 64GB+ machines                                                                                            |
| "1+1" efficiency probe                                                          | Early-2025-era reasoning models (e.g., DeepSeek-R1-class) could burn ~2,000 tokens answering "what is 1+1"; current-generation reasoning models answer efficiently, used informally as a sanity check for a model's reasoning-efficiency |
| Kimi K3 effort specialists (per the technical report, as recalled)              | Reportedly three effort-level specialists (light/medium/high) crossed with domains (math, coding, general knowledge) — roughly nine specialist variants distilled into the final release model                                           |

---

## Suggestions & Future Directions

1. **Build harness-level automatic model/effort routing.** Raschka explicitly flags this as an unsolved, valuable direction: the harness — informed by task, context, and conversation history — should choose model size and reasoning effort dynamically, rather than leaving it to the user's gut feeling (which tends to either over-spend compute on easy tasks or under-spend on hard ones).
2. **Learn new architectures incrementally, anchored to a timeline.** Rather than attempting to understand a current flagship model cold, start from GPT-2, then attention variants, then MoE, then multi-head latent attention (DeepSeek V3-era), then hybrid/linear attention — treating each new release as "one new component added to a known base."
3. **Use open-router/hosted inference to explore, then go local only if it sticks.** For quick evaluation of a new open-weight model, use a hosted endpoint (e.g., OpenRouter) rather than downloading (often 100+ GB, hours) — commit to local hosting only once a model proves worth keeping.
4. **A likely next book: "build a coding agent harness from scratch."** Raschka frames his book progression as engine (*LLMs from Scratch*) → tuned engine (*Build a Reasoning Model from Scratch*) → the vehicle the engine sits in (a coding-agent harness), and says this is the natural next topic, alongside multimodal LLMs as another candidate direction — pending a break after two intense one-year book projects.
5. **Treat the pace of releases as a marathon, not a sprint.** His closing advice to builders: you don't need to learn every new architecture in real time; focus on durable building blocks and accept that some releases can be skipped without real cost.

---

## Authors & Institutions

**Guest:** Sebastian Raschka — independent ML researcher and author (*Build a Large Language Model from Scratch*, *Build a Reasoning Model from Scratch*, Manning Publications); writes the *Ahead of AI* Substack.
**Host:** Hugo Bowne-Anderson — Vanishing Gradients podcast.
