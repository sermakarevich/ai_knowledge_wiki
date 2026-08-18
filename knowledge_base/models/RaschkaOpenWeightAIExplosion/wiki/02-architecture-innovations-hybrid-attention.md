> [[../index|Wiki]] | [[../summary|Summary]]

# Hybrid Attention and Targeted Architecture Innovations

Raschka frames the current wave of open-weight architecture work not as a series of fundamental reinventions but as a set of narrow, targeted component swaps layered onto a still-recognizable transformer skeleton. The dominant swap is the move from standard (quadratic) self-attention toward linear-attention-like mechanisms in most layers — a trend he illustrates with named implementations in Qwen3-Next, Kimi K3, and Nemotron — alongside smaller, more surgical tweaks like DeepSeek V4's "highway connections" and a "looped transformer" design he happened to look at the same weekend. His overall verdict, given directly in response to a listener question about what's architecturally next, is that hybrid/linear attention is currently where "most of the bang for the buck" comes from, while everything else is incremental tuning of individual knobs.

## The trend: from quadratic attention toward linear attention

Raschka introduces this as the most important recent architectural trend when walking through his architecture-comparison gallery: "in the lower right side here you see... hybrid architectures and that is I think that is... the most recent trend if we look at architectures" [10:44]. He describes it as a shift where models are "going from the standard attention to like a linear more linear type of attention that is... kind of faster" [10:44]. Crucially, he stresses this is not about brute-force scaling alone: "it is all about making models bigger, but then also kind of like keeping in mind it's not all brute force anymore. It's kind of really sophisticated now" [11:29].

The framing he returns to later, when directly asked what's next architecturally, is the car analogy: these are "very targeted... replacements. Like if you have a car, you don't reinvent the car that has four wheels, but you swap out the engine, you know, like now you have electric motors instead of gasoline motors" [61:36]. Hybrid/linear-attention components — replacing full attention with a cheaper mechanism in most layers while typically retaining some full-attention layers — are, in his words, the engine swap of this current generation of models.

## Named examples: Gated DeltaNet, Kimi Delta Attention, Mamba-2

Three concrete implementations are named as instances of this same underlying pattern:

- **Qwen3-Next's Gated DeltaNet** — referenced as one of the models embodying the shift "from the standard attention to like a linear more linear type of attention" [10:44], and again later as one of the "some flavor" hybrid-attention implementations: "the Gated DeltaNet in Qwen 3" [60:50].
- **Kimi's "Kimi Delta Attention"** — explicitly said to be closely related to the Qwen3-Next mechanism: "this model has the Kimmy Delta attention, which is very similar to gated Delta net, which we've just seen there" [11:29], repeated again near the end of the conversation: "in Kimi, the Kimi Delta attention, which is very similar to Gated DeltaNet" [60:50].
- **Nemotron's Mamba-2 layers** — cited as another flavor of the same trend: "Nemotron has... more like Mamba 2 layers" [60:50].

Raschka's summary judgment across all three: "These are kind of complicated components if you look at them compared to the normal attention, but they're not super complicated. It's almost like swapping out that module" [60:50].

He also notes, when talking about Kimi K3 specifically, that it should not be read as a minor variant despite its architectural closeness to Kimi Linear: "Kimmy linear was like a research prototype. Now, this is a production model" [11:29], meaning the same Kimi Delta Attention mechanism has now moved from research prototype into a shipped, production-scale model.

## DeepSeek V4's highway connections

Asked what's next architecturally, Raschka brings up residual/highway connections as an example of tweaking a component that "has [not] changed in a long time" [57:44]. He is careful to attribute credit correctly: "it was not invented, I would say, by Deep Seek version four, but they popularized it. I think they had another paper on that before, like a prototype. They always have like a prototype paper and then the production model" [58:29]. The mechanism itself: "instead of one residual path, you have multiple. I think in that case they were four. And... that was one way to improve residual connections" [58:29]. This mirrors the pattern he also describes for Kimi K3's overall design — take an existing prototype paper's idea, then popularize/scale it into a production release [13:49].

## Kimi K3's residual attention (cross-reference)

Raschka mentions Kimi K3's "residual attention" as another example of this same "targeted tweak" pattern, alongside the highway-connections discussion: "right now, Kimmy K3 from Kimmy Linear, the... residual attention... They also had a stand-alone paper" [58:29]. Earlier in the conversation he described it in more detail — computing softmax attention over previous blocks and adding it as a residual rather than a simple additive connection [11:29]-[12:17], noting it is a modeling-quality tweak (not an efficiency tweak) that reportedly added "4 or 5% training cost and like 2 or 3% inference cost" [11:29]. Full detail on this mechanism lives on the dedicated Kimi K3 architecture page; here it is noted simply as one more instance of labs tuning "little knobs" on top of the base transformer [11:29].

## The looped transformer

Raschka recalls looking at six architectures over the preceding weekend and singles out one using a "looped transformer" design, though he could not recall which specific model it was: "there was uh, one architecture that used the looped transformer... they had 22 transformer blocks... and they... looped back to them... So, they had two times 22. So, you have twice the compute because you go now through 44 layers, but you only have the same [size]... for the 22 layers, you use the same set of weights for the second time when you loop through the 22 layers" [59:16]-[60:02]. In other words: 44 layers of effective compute depth, but no increase in parameter count, since the second pass through the 22 blocks reuses the same weights.

He flags a methodological gap in how this was reported: "I don't think they did a nice ablation study in the paper or technical report, unfortunately, so I don't know how much that actually improved, but it was worth it to actually do it" [60:02] — i.e., the technique was apparently judged worth shipping, but the paper did not clearly quantify the benefit of looping versus not looping.

## Overall framing: targeted swaps, not reinvention

Raschka's closing synthesis on this question is explicit: none of these changes — highway connections, residual attention, the looped transformer, or the various hybrid-attention variants — amount to a fundamental architectural reinvention. They are incremental, targeted swaps of individual components within an otherwise stable transformer scaffold: "It's not really... throwing everything out there like what we already have and it's not replacing everything. It's just very targeted... replacements" [61:36]. Among all of these, he singles out hybrid/linear attention as the highest-leverage lever currently available: "I do think most of the bang for the buck comes from the hybrid attention" [60:02]-[60:50]. This matches his broader point made earlier in the conversation that modern flagship architectures (like Kimi K3) are now too complex to write from scratch as a single file of a few hundred lines — instead, teams "take an existing one and then just add that one thing to it" [13:49], one targeted component at a time.

---

**Covers:** [10:44]-[13:49] and [57:44]-[63:10] segments of the transcript (topic: hybrid attention and architecture innovations)
