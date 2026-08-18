> [[../index|Wiki]] | [[../summary|Summary]]

# Outlook: Building Blocks, Career Advice, and What's Next

This page collects the episode's reflective through-line: the occasion for the conversation (Raschka's new book, *Build a Reasoning Model from Scratch*), his standing advice for how a newcomer should learn transformer architecture without being overwhelmed by the current frontier, the book-progression analogy that points toward his likely next project (an agent-harness book), and his closing career advice to treat the field as "a marathon, not a sprint" [74:48]. It closes with the episode's own self-aware punchline: Kimi K3 dropped on the very day of recording, testing that advice in real time.

## The New Book: Build a Reasoning Model from Scratch

The episode is framed from the start as partly a celebration of Raschka's new Manning book, *Build a Reasoning Model from Scratch*, positioned as the sequel to his earlier *Build a Large Language Model from Scratch* [00:46]. Raschka shares physical details about the new book: he had just received hard copies "a few 2 weeks ago," and it is printed in color throughout — "it has color figures every everywhere" [01:32]. He notes this took real negotiation with the publisher: "This took me a lot of like effort like talking to the publisher" [01:32].

On format, he describes the new book as "almost twice as thick as the previous book, Build a Large Language Model from Scratch, but it's also almost the same number of pages, about 400. It's a much better paper quality and color" [01:32] — i.e., the added thickness comes from paper/print quality rather than substantially more pages. Manning offered the podcast audience 45% off the book and five giveaway copies for the best audience questions [01:32]-[02:18].

Later, discussing the effort behind the book, Raschka states plainly that "each of the two books it took me a year but also hard work... not just like a few hours" [69:22] — the same roughly one-year, concentrated-effort timeline applying to both the LLM book and the reasoning-model book.

## Learning Transformers as a Timeline

Prompted by Hugo's question about how someone who "hadn't really looked at a transformer before" should build up understanding all the way to a current model like Kimi K3 [15:22], Raschka lays out a recommended learning path that mirrors the historical order in which components were introduced.

**Why a timeline approach is needed at all:** earlier in the conversation he had already noted that recent flagship architectures are too complex to absorb in one pass. With GPT-2, "you could have everything in like 2 300 lines of code... and understand it at once," but something like Kimi K3 would take "thousands of lines of code," which he calls "very overwhelming" for a single person to take in at once [13:02]. Going "from one architecture to the next in chronological order," by contrast, means "you learn about one component or two components at a time, and then again, it does make sense. It's almost like a timeline. Like understanding transformers as a timeline" [14:35]. Without that grounding, "if you today start looking at Ki[mi] K3 and have never seen a transformer before, I think it would just — brain would explode" [14:35].

**The recommended sequence [16:08]-[16:54]:**

1. **Start at GPT-2.** Raschka picks this starting point partly because "luckily... it got rid of the rope, the rotational position embeddings" — GPT-2 uses learned/no positional-embedding handling of that type, "so you don't have to re-worry about that anymore" [16:08], simplifying one axis of the architecture for a beginner.
2. **Get the core concepts solid first:** "what is a transformer block? What is attention?" — understood "really like top to bottom" [16:08].
3. **Move to attention variants in the order they appeared:** if attention itself is new, start with regular attention, then move to multi-head latent attention as introduced in "DeepSeek version 3" [16:54] — the compressed-KV-cache technique described elsewhere in the episode as similar to a LoRA-style bottleneck [06:53].
4. **Then mixture-of-experts, and its later "latent" variant:** "if you see something like latent MoE and you have never heard about MoEs, I would start with MoEs" [16:54] before tackling the latent/compressed MoE variant seen in newer models.
5. **Leave cross-cutting tricks like residual/highway attention for last.** Raschka is explicit about sequencing this deliberately at the end: "the residual attention thing, uh, attention residual, they have a standalone paper on that. That's a tough one... it's a relatively straightforward concept... but I would probably leave that for the end. And then, because that is kind of like this cross connection" [16:08]-[16:54]. Unlike attention or MoE, which are self-contained modules you can swap in, residual/highway-style attention connects back across the whole stack, so it only makes sense once everything else is in place.

He summarizes the overall approach as going through the material "like really... top to bottom" the way his own architecture-diagram gallery is ordered [16:54].

## The Book-Progression Analogy: Engine, Race-Car Engine, and Where You Put It

Asked directly what a third book in the series would be, Raschka says "I think the answer is obvious in a sense... for myself. So, I'm not saying it should be obvious to you. It's obvious for me. I know what I should do, but I don't know when and if yet" [68:35].

The analogy he uses comes from a diagram in his own "components of coding agents" blog post: seeing that diagram is what made the three-book progression click for him — "I had this one figure in... the components of coding agents blog post... I just try to explain to people how things connect and then... I was saying oh this should be obvious to me because I saw okay this is actually three books here" [70:09].

The mapping:

- **Build a Large Language Model from Scratch** = the engine of a car — "just the engine" [70:09].
- **Build a Reasoning Model from Scratch** = the same engine, tuned and beefed up — "the reasoning model book which is like the beefed up engine. It's like Formula 1 race car engine." He's careful to keep the analogy honest to the underlying model: "the analogy is basically LLM — reasoning LLM is a more capable LLM. It's still an LLM" [70:09] — reasoning training makes the engine higher-performance, not a different kind of thing.
- **The natural next book** = where you put that engine, i.e., the vehicle it goes into: "where do you put this engine, right? And so that would be the agent harness essentially. So I think that that would be the most natural progression — like the next book probably something with agents" [70:09]-[70:55].

Hugo offers a parallel pop-culture framing of the same idea, from *Teenage Mutant Ninja Turtles*: "Krang is the brain, the LLM — tokens in, tokens out — but he needs a body in order to be the master criminal, and that's the harness" [72:29]. Both analogies make the same point: the model itself is necessary but not sufficient; it needs a surrounding structure (car body / Krang's body-suit) to actually act in the world.

**Caveats on the next-book idea:**

- Raschka has already experimented in this direction: he "started... writing my own harnesses" after the blog post, but is clear this was exploratory, not a competing product: "there are so many harnesses out there that... this article or my harness is more like a proof of concept [of] what are things to consider, but... it's not something you use — um it's not... Hermes... and it's also not Open Claw. It is a very simple harness. It's for education purposes" [70:55]-[71:41].
- He needs recovery time first, having just finished two consecutive roughly one-year book projects: "each of the two books it took me a year but also hard work... I do think I need a bit of a break after that... it was a big undertaking" [69:22].
- **Multimodal LLMs** are floated as a real alternative direction, based on audience demand rather than his own stated preference: "people ask me about multimodal LLMs, too... I have — too many things and not enough time... there are other interesting directions, too" [70:55]-[71:41].

Hugo closes the topic by naming the implied project explicitly: "It seems like at some point Sebastian may entertain the idea of writing a build... coding agent... from scratch" [72:29], inviting audience feedback on whether that's the book people want.

## Marathon, Not a Sprint: Closing Career Advice

Asked for one piece of advice for "builders, people working with LLMs and agents," Raschka gives what he calls "a mantra almost," while flagging its own corniness: "it's really cheesy, but it's a marathon not a race — not a sprint" [74:48].

The substance of the advice: there is no obligation to track every release or master every new architecture in real time. "There's no rush... I do think it's more like a long-term thing, because yeah, you may even skip certain things — architecture. You don't have to learn about each architecture because some are more important than others" [74:48]-[75:35]. The prescription is to anchor on durable fundamentals instead of chasing the news cycle: "what just makes sense is... focusing on the building blocks... and trying not to get overwhelmed" [75:35]. He frames this explicitly as a sustainability strategy rather than a purity test — "just to make it healthy and long-term successful... to not overdo it" [75:35].

Hugo extends the framing with his own ocean-swimming metaphor — that the volume of new releases is like wild waves that "just keep on coming," and that sometimes "you just got to let it wash over you" rather than chase every one [75:35]-[76:20].

## Coda: Kimi K3's Same-Day Release

Hugo immediately points out the tension: "Kim[i] K3 released it this week — today — and you've already published" a diagram and analysis of it [76:20]. Raschka takes this in stride and is self-deprecating about it: "that's — this is why I was saying I'm not always perfect with this" [76:20]. He admits the ideal version of the "marathon" philosophy would have meant not rushing — "ideally this would be something I would sit down and do in a few days" — but he wanted material ready for the podcast [76:20].

Crucially, he argues this doesn't actually contradict the building-blocks advice, because Kimi K3 wasn't a from-scratch undertaking: "it wasn't as hard because there was already Kimi Linear... things built on each other, and so if you kind of follow the more... building-block... [approach], it goes a long way. You are not starting from the ground up" [76:20]-[77:07]. He generalizes this to the technical report itself — dense as it is ("I think 50 pages of formulas and everything") — noting "that can be overwhelming, but if you get the big picture, the big picture itself is not overwhelming... it's building on other things you have already seen. For example, the multi-headed [latent] attention might be overwhelming, but it is essentially from DeepSeek version 3, long time ago, and then... it's not that overwhelming anymore because it's — oh, this is a component from back then" [77:07]-[77:53].

Hugo ties this back explicitly to the earlier timeline discussion: "if you really want to understand Ki[mi] K3... you can go and look at the most recent techniques... but if you want to go back and start with GPT-2 and then go through Sebastian's architectural diagrams and everything he's written to build these things out completely" [77:53] — the same closing point as the "learning transformers as a timeline" segment, and further confirmation of the building-blocks philosophy rather than a contradiction of "marathon, not sprint."

---

**Covers:** [00:46]-[03:03] and [14:35]-[17:39] and [67:50]-[78:39] segments of the transcript (topic: outlook and learning philosophy)
