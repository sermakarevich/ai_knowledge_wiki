> [[../index|Wiki]] | [[../summary|Summary]]

# Kimi K3's Architecture

On the day Kimi K3's weights were released, Sebastian Raschka spent the afternoon speed-reading its technical report and sketching its architecture diagram, and his headline finding was reassuring: "it was not that much different from Kimi Linear" [04:35] — the earlier Kimi Linear research prototype. Kimi K3 is best understood as Kimi Linear scaled up and combined with a "latent MoE" layer borrowed from the same design space as NVIDIA's Nemotron 3 Ultra, plus a separate "residual attention" component that Kimi Linear's own paper had already introduced. Raschka frames the whole exercise as evidence of a broader shift in how frontier architectures are now built: not from scratch, but by taking a known base model and bolting on one new component at a time [13:49].

## Kimi Linear, Scaled Up

Raschka's diagram of Kimi K3 could "almost... copy paste the architecture" of Kimi Linear [04:35], because the two share the same overall structure. The one difference visible in the base diagram is depth: Kimi Linear had 27 layers, while Kimi K3 has 93 layers [04:35]. Everything else that changed is not depth but composition — Kimi K3 swaps in a latent MoE where Kimi Linear had a regular MoE, a change too "crowded" to show cleanly on the same diagram [05:20]. He summarizes the relationship plainly: "it's basically Kimi linear bigger with latent MoE" [05:20].

He's careful to frame the relationship as a research-prototype-to-production jump rather than a trivial rename: "Kimi linear was like a research prototype. Now, this is a production model" [11:29]. Kimi K3 also uses Kimi Delta Attention, which Raschka describes as "very similar to gated Delta net" [11:29] — i.e., part of the same wider move (seen also in Qwen3-Next and Nemotron) from full quadratic self-attention toward linear/hybrid attention variants. That attention-mechanism swap is treated elsewhere in the transcript as its own trend; this page focuses on the latent-MoE and residual-attention additions layered on top of it.

## Latent MoE (the Nemotron 3 Ultra Analogy)

Instead of a standard MoE layer, Kimi K3 uses a "latent MoE" [05:20]. Raschka draws the direct comparison to NVIDIA's Nemotron architecture: "I think it's the Nemotron 3 ultra architecture has that as well... it's basically kind of like multi-head latent attention" [05:20]–[06:53]. To explain what "latent" means here, he gives a compression/bottleneck analogy:

> "A multi-head latent attention is... like attention, but you have a latent vector that is like a compressed state. It's almost like Laura, where you go from a big like a matmul like from a bigger vector to a smaller vector like the bottleneck basically." [06:53]

The point of the compression is specifically about what gets cached: "the idea here in... latent attention is to [get] the KV cache to store smaller K and V's. So, you compress the K and V's into a smaller shared form. And then you store that in the KV cache instead of the full-size KV." [06:53]–[07:40] He characterizes this as "more like an efficiency tweak" [07:40] — i.e., aimed at reducing memory/compute cost, not at changing what the model can represent.

The latent MoE applies the same compression idea to experts rather than to K/V vectors: "the MoE... latent MoE is kind of similar, where you have like latent experts... they're smaller essentially" [07:40]. In short, both the attention side and the expert-routing side of Kimi K3 use the same underlying trick — project down into a smaller shared/compressed representation before doing the expensive part (caching K/V, or running an expert), then expand back out.

## Residual Attention

Separate from the latent MoE, Kimi K3 carries over a component Raschka says was "glanced over" the first time but shouldn't be underrated: "residual attention" [11:29]. He describes the mechanism as computing an extra attention pass over earlier layers and folding it in as a residual, rather than as a normal skip connection:

> "It's yet another trick where you... add — it's like kind of like a computing softmax and attention over previous blocks and you add that as a residual instead of just the addition." [11:29]–[12:17]

He's explicit that this is a modeling-quality lever, not an efficiency one: "it's not like a huge improvement in terms of modeling quality. This is not a efficiency tweak. It's a modeling quality tweak." [12:17] He attributes the idea to the Kimi Linear paper and gives a specific cost figure from (his recollection of) that paper: it "added like 4 or 5% training cost and like 2 or 3% inference cost" [12:17]. The component has its own standalone paper — a point he repeats later in the conversation when contrasting it with DeepSeek V4's "highway connections" (multiple parallel residual paths): "right now, Kimi K3['s]... residual attention... they also had a standalone paper" [58:29]–[59:16].

Residual attention is also the component Raschka singles out as hardest to slot into a learning sequence, because it is a cross-cutting connection rather than a self-contained module — see the learning-path note below.

## Growing Implementation Complexity

Raschka uses Kimi K3 as the example for a broader claim about where architecture design is heading. GPT-2, he notes, could be implemented and understood as a single file: "with GPT-2, you could have everything in like 2 [to] 300 lines of code... and understand it at once" [13:02]. Kimi K3 is past that point: "if you look at something like Kimi[]... 3, I think it would be thousands of lines of code unless you have modules in different files... all the modules like residual attention, latent MoE, and everything in one file, it would be thousands of lines of code, and I think it would be very overwhelming." [13:02] His conclusion is blunt: "I don't think a single person can really do that anymore." [13:02]–[13:49]

His explanation for how such models still get built is incremental composition rather than ground-up design: "no one starts this from scratch. What you would do is you would take an existing one and then just add that one thing to it... for Kimi[]... K3, they started with Kimi linear and added latent MoE. They already had the other things. So you do one thing at a time, and then it's doable." [13:49] He illustrates the trajectory with an inverted-SpaceX analogy — rocket engines historically went from a tangle of wires to something visually simpler over successive generations, whereas transformers are going the other direction, starting simple (the original attention-is-all-you-need block) and accumulating more and more attached components over time [13:49]–[14:35].

The corollary for a newcomer: approaching a model like Kimi K3 cold, with no prior transformer background, is overwhelming — "if you today start looking at Kimi[]... 3 and have never seen a transformer before, I think it would just [your] brain would explode" [14:35]. Going through architectures "in chronological order," by contrast, means "you learn about one component or two components at a time" [14:35], which is tractable.

## Recommended Learning Path (Brief)

Asked how a newcomer should build up to being able to read something like Kimi K3, Raschka's answer follows directly from the "one component at a time" point above: start with GPT-2 as the base — transformer block, attention — then work through each subsequent addition in turn: multi-head latent attention (introduced with DeepSeek V3 [16:54]), MoE and then latent MoE, hybrid/linear attention variants, and only at the end the residual-attention cross-connection, since it doesn't sit inside a single block the way the other components do: "that is kind of like this cross connection... I would probably leave that for the end" [16:08]–[16:54]. This progression — and the broader "timeline" framing of transformer history — is covered in more depth on the outlook/building-blocks page of this wiki; the point relevant here is simply that Kimi K3's own construction (Kimi Linear + latent MoE) is a direct instance of the same incremental pattern he recommends for learning.

For scale context: Raschka separately notes Kimi K3 is in the roughly 2.8 (trillion-parameter-class) range, comparable in scale to GLM-5.2's ~2.7T [28:24]–[29:10] — underscoring that the architectural additions discussed above (latent MoE, residual attention) are layered onto an already very large base model, not a small one.

---

**Covers:** [03:03]-[16:54] segment of the transcript (topic: Kimi K3 architecture), with brief supporting references to [28:24]-[29:10] and [58:29]-[59:16].
