> [[../index|Wiki]] | [[../summary|Summary]]

# The Shrinking Open-Weight vs. Frontier Gap

A central theme of this conversation is that the gap between open-weight model releases (DeepSeek, GLM, Kimi, Qwen) and proprietary frontier releases (ChatGPT, Claude, Grok, Gemini) is visibly compressing — both in release cadence and in perceived capability — and that Raschka is skeptical that most of what looks like frontier "improvement" is actually new training-time math rather than product-layer polish. He illustrates the closing gap concretely with GLM-5.2, DeepSeek V4, and Kimi K3, tracing a specific multimodal affordance (drag-and-drop image support) across the three releases, and separately marvels at how well attention-based image *understanding* works even though generation remains weak.

## Compressed Release Cadence and "Leapfrogging"

Hugo frames the shift directly: historically, open-weight models trailed frontier releases by roughly 6 to 9 months, but that gap "is really shrinking" [18:25]. Raschka agrees, describing the current dynamic among proprietary frontier labs (ChatGPT, Claude, Grok, Gemini) as one where "the latest model is always the best model for like a few weeks and then it's like leapfrogging almost" [18:25]. Hugo characterizes this as happening in "rounds or waves" — clusters of releases within a span of a few weeks.

Raschka adds a strategic-timing observation: labs likely "have some models ready that are still they could stop training and release them," but hold back and wait, so that if a competitor releases first, they can respond within about two weeks rather than releasing immediately [19:12]. This suggests the cadence compression is partly a competitive-timing artifact, not purely a reflection of how fast the underlying research is progressing.

## Genuine Training Improvement vs. "Polishing"

Raschka is explicit that he can't cleanly separate real capability gains from surface-level polish: "I can't know how much the models improve really versus like they all improve on the benchmarks and everything and everyday usage, but I don't know how much of that is because they are like smarter in that sense or whether they just have better like how to use tools to get their job done or like how to interpret the harness constraints" [19:12].

He frames this as a distinction between pre-training/fine-tuning improvements and fine-tuning to the deployment environment: "more like the fine-tuning in the environment it's going to get used" [19:57]. His example is web search — a model that is "better at doing web search" will give better results "without hallucination," but the underlying question is how much of that is "almost like polishing versus training" the rough edges that real users hit, as opposed to deeper pretraining/fine-tuning/RLHF work [19:57]. He is careful to note labs are "still training models from scratch and fine-tuning and RLHF and extending everything," but his instinct is that a lot of the visible improvement "is almost more like on a product level" [19:57].

## Codex-Style Computer Use as Product, Not New Math

Asked what impresses him most in recent releases, Raschka pointedly does not point to raw model quality jumps ("5.6 is better than 5.5, but you know what 5.5 was already very good") [20:42]. Instead he singles out product-level capabilities such as Codex being able to operate a computer directly — "it can use your computer now... in Codex you can say, well, I don't know, use my email client and do something there... it would physically use the mouse, take screenshots of your screen" and "actually navigate things on your computer and automate workflows" [20:42].

His interpretation is explicit: this is "an impressive product feature," "a next step for LLMs" in terms of what they can *do*, "but not really because they are smarter. It's more about, I guess, the product like how that's implemented" [20:42]. He extends this to multimodal image handling in this context too: extracting information from screenshots is "more like a product implementation rather than um mathematical training procedure that is different from the previous one" [21:28]. Hugo agrees and adds a related product-layer observation about "steering" — the ergonomics of interjecting new instructions mid-task in harnesses like Codex and Amp without the agent stopping or stuttering — as another example of harness/UX-level rather than model-level progress [21:28]-[22:59].

## GLM-5.2, DeepSeek V4, Kimi K3: Vibes and Affordances Closing the Gap

Hugo identifies GLM-5.2 as a turning point: "the GLM 5.2 was really the first model that when it came out, the first open-weight one where I was like, 'Oh, this is really close to... This feels really close to frontier lab stuff, based on vibes'" [27:36]. He ties this impression partly to concrete multimodal affordances in his own workflow (voice input, dragging and dropping images, generating HTML/markdown output): he "couldn't drag and drop images in... into" GLM-5.2, "could with Deep Seek V4 before that," and then "with Kimi K3, I can drag and drop images to it" [27:36]. He reads this progression as evidence that "with those types of affordances... the open weight models are getting even closer as well" to frontier-lab product experience [28:24].

Raschka immediately tempers the comparison with a scale caveat: "Kimiko 3 is 2.8, I think, and GLM 5 is like 2,700 billion, so it is it is magnitudes bigger, too. So, four times as big also... it's 2.8, right? 2.8, I think so. I mean, just my brain is also from looking at numbers today" [28:24]-[29:10]. In other words, he explicitly flags this as a rough, in-the-moment recollection (approximately 2.7 trillion parameters for GLM-5.2 versus approximately 2.8 for Kimi K3, i.e. roughly comparable trillion-class scale despite the "four times as big" remark, which he himself hedges as uncertain), not a precise, verified citation.

He also notes a related trend: some of these open-weight models are "not super local anymore" — they are open-weight in the licensing sense but practically consumed via API-like services such as OpenRouter rather than run on personal hardware, which is itself part of how the frontier/open-weight product experience is converging [29:10]-[29:56].

## Attention-Based Image Understanding vs. Image Generation

Later, discussing product-harness awareness more broadly, Raschka returns to multimodality with a point of genuine fascination: "what it is not good at is making images... but how good it is at understanding images... even like subtleties" [48:29]. His framing is architectural: in a multimodal LLM the image is "chopped up... into smaller patches," and what strikes him is "how well attention works" to reconstruct "the big picture" from those patches [48:29].

His concrete example is diagram interpretation — he describes throwing in something like the "Kimi K3 diagram" and asking the model to check "if I do something wrong there... you forgot that arrow there or... I don't have a wrong connection there," noting the model "can't draw for you, but it can point out" such errors, though "it's not always right" and needs to be checked [48:29]-[49:15]. He emphasizes that this requires the model to "reconcile" information spread across "multiple patches" and that watching this actually work — for pixels, not just "tokens and words and code" — remains fascinating to him: "it is actually working. So that's kind of still fascinating to me how well it works" [49:15].

---

**Covers:** [17:39]-[22:59] and [27:36]-[29:56] and [48:29]-[50:01] segments of the transcript (topic: open-weight vs frontier gap)
