> [[../index|Wiki]] | [[../summary|Summary]]

# Local and Self-Hosted Inference: Hardware and Tradeoffs

"Open-weight" and "runs on your own hardware" are not the same thing, and most of this segment of the conversation is Raschka unpacking that gap: he walks through his actual local rig (a DGX Spark and a Mac Mini), contrasts it with a much faster Mac setup another guest uses, and then, prompted by a listener question, lays out why self-hosting a genuinely large open-weight model is hard in practice — leaving OpenRouter (or a hosting provider like Base10) as the pragmatic way to try a new model before committing to download and host it yourself.

## Open-Weight Does Not Mean Local

Discussing Kimi K3 (recalled as roughly 2.8T parameters) and GLM-5.2 (recalled as roughly 2.7T), Raschka flags that the newest large open-weight releases are increasingly not the kind of thing anyone runs on their own machine: "it is also the trend things are getting now to... models that are not super local anymore" [29:10]. Hugo confirms he tried both through Open Router or the vendor's own API rather than locally [29:10]. Raschka's framing: "it is also they are open weight models, but it's also open weight doesn't mean running things locally... that's yet another level for that" [29:10]. Open weights guarantee inspectability and, in principle, portability — not that a given model is a realistic target for self-hosting.

## Raschka's Local Setup: DGX Spark Running Ling S2.1

For an actual local run, Raschka describes trying "Ling S2.1" (transcribed in the source as "Laguna S2.1") over the preceding weekend [29:56]. His assessment on quality: "I don't think it's it doesn't feel much better than... Qwen 3.6 [35 billion MOE]... but I have not used it enough, so it might be better. So basically on benchmarks it suggests it's better, but it feels about the same" [29:56].

The interesting part is what it does to his hardware. His DGX Spark has "about 120 gigabyte RAM," and Ling S2.1 "uses about 80-90 gigabytes even in long contexts" [29:56] — a model that essentially maxes out the machine: "it's like a nice... where you feel like, 'Okay, this kind of maxes out my machine'" [30:42]. He contrasts this directly with running Qwen 3.6 35B MoE on the same box, where usage is only around 40 GB and there is comfortable headroom: "you have a lot of headroom... you feel like, 'Oh, I'm wasting. I could be running a bigger model here'" [30:42].

On throughput, Ling S2.1 is "two times slower" than Qwen 3.6, but still lands "like 20-30 tokens per second," which he judges "plenty fast... It's like using ChatGPT, basically. It's also 20-30 tokens per second" — "a comfortable speed" that is fine even for agent loops, though "of course faster is better" [30:42].

## Mac Setup and the Tunguz Comparison

Raschka also owns a Mac Mini with the maxed-out RAM configuration (64 GB), bought "like 1 and 1/2 years ago now before the RAM prices were high" [35:18]. He deliberately avoids running big local models on it: it is his main work machine, and running something like Qwen 3.6 on it "kind of slows down your computer" while he is "doing other things on that computer too" — he doesn't want it "to get too hot" [35:18]-[36:06]. So the DGX Spark, not the Mac, is his dedicated local-inference box.

Hugo brings in a data point from a different guest: Tomás Tunguz (VC), featured on Hugo's "Show Us Your Agent Skills" series, runs Qwen 3.5 locally with the "Pi" app and, per Hugo, "besides big code base changes, he can get away with using it for nearly everything," reportedly at "120 tokens per second," alongside his own custom WhisperFlow-style dictation tool with "300 ms dictation latency" [38:27]. Asked what hardware produces that speed, Hugo checks his notes: "a Mac M5" [39:13]. Raschka's own comparison point is his M4: "for the M4 I'm getting maybe 60-80... I think 80 around 80," using the MLX version of the model, and notes it makes sense that an M5 would be faster still — "that is... faster than like let's say GPT 5.6 or even 5.5" in token throughput terms [39:13]. Hugo separately mentions his own machine, a MacBook Pro M4 Max with "128 gigs of unified memory," though he finds he still prefers frontier proprietary models over Qwen 3.5 for open-ended reasoning tasks like synthesizing across multiple podcast transcripts [40:01].

## Why Run Local Models At All

Raschka is explicit that current local models are not winning on capability: "I use local models. I have to be honest here. I'm using them for just for fun because it kind of feels fun to use them. It feels kind of satisfying. It's like oh, it's on my computer... Kind of feels good. It's like people working on their car in the garage. You know, you don't have to, it's like a hobby, but it's kind of satisfying, it's fun" [36:06].

The other stated reasons are:
- **Privacy on sensitive queries.** "The only exception is if I want to do something where I feel like oh I don't want them to have my data... let's say medical... sometimes you want to know things and... you don't want them to have your whole medical history" [36:54].
- **A hedge against future pricing/access changes**, not a response to current necessity: "I think local models are important because we also want to be prepared for a case where... maybe we have to use them one day. It would be sad if they were not an option and there are only proprietary models and let's say the prices go up like crazy... you always have these local models then as a alternative. It's good to have alternatives... competition is good for business" [37:40].

Crucially, he is not being pushed toward local use by cost pressure today: subscriptions are "relatively [cheap], in quotation marks... where it's like you get a lot for the subscription where... until, you know, I reach the limits in terms of... subscription usage I'm not forced to use local models" [36:06]. He expects this to change "at some point where you will probably run into your limits sooner. And then that will be the point where you will automatically also use more local models" [34:32]-[35:18] — but that point hasn't arrived for him yet.

## Self-Hosting a Large Model: The Practical Obstacles

Responding to a listener question from Lak Veer — "With models reaching as large as [hundreds of billions/trillions of] parameters, what are the challenges to self-hosting? And how do we get around them?" plus the observation that "even renting GPUs doesn't always seem possible. They're always out" [50:01] — Raschka lays out several concrete obstacles:

- **Single-GPU hosting is impossible for the largest models.** "For the bigger models, you just can't host them on a single hardware. You need multiple" [50:49].
- **Consumer purchase of server GPUs isn't really an option.** "Even as a consumer, you can't just buy a server GPU... even if they would [be available]... out of stock, and even then they would be way too expensive. And even then if you could afford it, you probably don't want them at home" [50:49].
- **GPU rental (e.g., AWS) is often unavailable or expensive.** "You could technically just rent off an AWS instance... but then they're also out and expensive" [51:35].

He illustrates the "don't want them at home" point with an anecdote from his university days: "I had, when I was at the university in 2018, my office... the Lambda workstation. It's meant as a workstation... four GPUs and they were the... GTX 1080, ancient by now, but even those were so hot and so loud, I couldn't bear it. I had it in my office and... like a month we moved it to the server room because it was so loud and so hot, it was very uncomfortable... if I had office hours, I could barely hear... you go crazy" [50:49]-[51:35]. He half-jokes that a basement is a fallback for housing hardware like this, "but basements can flood" [51:35].

## OpenRouter as the Middle Ground

Raschka's practical answer to "how do you get around this" is OpenRouter: "you know, the difference is it's not fully local, there is still... it's going through something and you don't know exactly what happens to your data" [51:35]-[52:21]. He clarifies that OpenRouter itself is a layer on top of multiple inference providers: "there's Open Router itself and then they do partner with other inference providers and they pick the one that is currently... most available and cost efficient, so you have multiple... companies involved in that" [52:21]. His data-handling heuristic: "if it goes to the internet it's not fully safe and private, to me at least... a more like a common sense thing. So I think if you're a bank or like a very sensitive medical information, you probably can't or shouldn't use those models, but... for tinkering — let's say I fix a bug on my website, my website is public anyway — I think that's a good alternative to use open weight models" even though it isn't local [52:21]-[53:06].

## Download Economics as a Reason to Test Before Hosting

Even with local hardware available, Raschka doesn't download every new model to try it, because of storage and time cost: "I also don't want to... download and install each model because they are large. I mean the [DGX Spark], I think it has 4 terabytes, but... I also have a lot of data from experiments on there like checkpoints and stuff. So I'm not like unlimited in space there" [53:06]. His rule of thumb for sizing a download: "roughly the billions of parameters is roughly, I guess, the gigabytes in storage it takes. It's another 100 gigabytes and it takes 2 hours to download it" [53:06]-[53:53].

This leads to his stated workflow: test a new open-weight model via a hosted endpoint first, and only download it for local hosting once it has proven worthwhile. "In this case I downloaded it because I did know that I wanted to use it, but I wouldn't do it just for all the models because that would take a long time to download and you have to switch them. So it's just easier... to quickly check something, just use open router... to quickly try something out and if you find... this is worthwhile, then switching to it locally if you can run it locally" [53:53].

## Hugo's Closing Frame: "Explore the Art of the Possible"

Hugo generalizes this into an operating principle: "explore the art of the possible. Like when Frontier Labs release new models, go and see what you can do with them. Don't necessarily put them in every workflow you have, but similarly with stuff like [Kimi] K3, explore what is possible with an open router endpoint or Base 10... I've had a lot of fun with Base 10... and they're great. I'm not affiliated with them, by the way. They have sponsored some of my courses, but... if you feel like it could really work for you, think about if you want to host it yourself" [54:39]. Raschka's reply ties this back to the "hobby" framing from earlier in the segment: "it's just also the whole thing itself is somehow fun... it's fun and it's empowering" [54:39]-[55:25].

---

**Covers:** [29:10]-[38:27] and [38:27]-[43:05] and [49:15]-[54:39] segments of the transcript (topic: local/self-hosted inference)
