> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Why OpenAI and Codex?
**In one sentence:** The author sticks with OpenAI/ChatGPT and Codex because his prompt libraries are tuned for them and they run the way he wants, rejecting Gemini, Anthropic, and Copilot on workflow and operational grounds while deferring open-source/local models to later, and values Codex mainly as scaffolding that breaks writer's block even though he threw away about half the code it gave him.
## Key points
- OpenAI was the author's first LLM, initially little-used because ungrounded generated text without RAG could not reference or source its information, but later useful, with ChatGPT replacing Google as a search tool.
- Code from more than roughly 6–12 months ago is described as "not worth much," implying model quality only recently became practically useful for his work.
- Gemini is rejected on working-relationship grounds after Verizon-era use under a Google contract ("every chat ... broke down into arguments"), rated decent only for image generation.
- Anthropic is rejected on operational grounds (API availability, confusing credits, arbitrary limits and waits, possible model downgrades) plus distrust of its leadership, marketing, and security claims, keeping only a free account for AEO queries.
- Copilot is dismissed with "Which one?", and open-source models are deferred as a future API-key swap, blocked by missing image generation and weaker RAG/search.
- The stated end state is staying on ChatGPT/Codex now, with a possible later move of tedious private work such as GTM automation to a local model that "won't leave the premises."
- Personal gain is framed as momentum and labour saved: about half the bot code was discarded, yet it still replaced code he would otherwise have written himself and broke through writer's block by giving him "a framework I could hammer into shape."
- Ownership is selective: lightly-reviewed frontend output stays if it looks good enough, while Go, Ansible/automation, and build tools get strict scrutiny because that is "the stuff that will actually wake me up at 3 a.m."
---
## Why OpenAI and Codex?
OpenAI was "the first LLM I used." For the first year or two he did not use it much because he had "no need for randomly generated text that was not implemented or integrated with RAG, and therefore could not reference or source its own information." Since then it has been useful, and by the time recent code improved he was already using ChatGPT "as a replacement for Google." Verbatim: "Some of the code it generated before the last six to twelve months was not worth much."

## Gemini
Used at Verizon under their Google contract. Verdict: "every chat I had with Gemini broke down into arguments and me berating the bot. This wasn't a healthy working relationship." Only concession: "Decent for generating images though."

## Anthropic
Has only "a free account with Anthropic, which I only have for AEO queries," adding "frankly, Anthropic is full of nonsense." Operational objections are listed as open questions: "Will their APIs actually be online? Which credits are going to be used? If I say "openclaw" will it nuke my usage for no reason? Will I hit some fairly arbitrary credit limit and then be told to wait five hours? Will I select one model and then have them decide to downgrade my requests to a different model, or however that system works?" Conclusion: "There is just too much operationally awkward evidence around Anthropic for me to want to depend on them."

He adds a values-based objection: "Hacker News and the usual crowd are big on Anthropic, but these are the same people who have spent years picking up every JavaScript framework that wandered past them," contrasting his values of "efficiency, clarity and simplicity," noting he avoided "react, angular and next.js instead landing on SolidJS."

On leadership and marketing: "I don't think Sam Altman is a saint, but Dario Amodei is out to claim my income for himself using lies and other people's cash," plus the claims that Anthropic "released its own client source code to the world by accident and had its Mythos model available if you just guessed what the endpoint was. Don't piss on my leg and tell me it's raining." He also criticises "the strategy of marketing yourself as an arms manufacturer and then being surprised" at government treatment, contrasting it with "Philip Zimmermann ... put the full source code for PGP in a fucking book ... 30 years ago," and dismisses Anthropic's security-model claims with "Yeah, ok." Summary line: "Anthropic is a massive drama bomb."

## Copilot
The whole subsection is one line: "Which one?"

## Open source models
"Yes. I'll do this at some point. They're basically just swapping out an API key so no rush currently. But they don't have image generation and they often don't RAG so search takes a hit. Otherwise sure."

## The result
"I am sticking with ChatGPT for now. My prompt libraries are tuned to do what I want with these models. Codex is perfectly fine and runnable the way I want it." Future direction: "Ideally, at some point, I would switch parts of my business process to a local model for tedious things like GTM automation. That'll be fine because it's private, can handle emails and simple text and won't leave the premises. That would be the next step for me."

## What have I personally gained from this?
The headline number is a ~50% discard rate: "even though I threw away about half the code the bot gave me, it still gave me code I would otherwise have had to write myself," which "reduced the massive, daunting task of doing all of this, especially at the beginning." The biggest benefit is framed as momentum: "breaking through that writer's block. It gave me a framework I could hammer into shape, rather than having to go out and build everything from nothing."

Selectivity is explicit: "certain parts of the code are the sort of work I don't like doing, and that is the code that has mostly been left in. Front end is a good example. If it looks good enough to me, that is just fine, I don't care that much about the implementation flavour," adding "I prefer classList but whatever" on JSX classList versus string interpolation. By contrast: "When it comes to the Go code though, the actual engineering, well that's the stuff that will actually wake me up at 3 a.m. I am on that with no remorse. Same deal with the Ansible and other automation." Build tools get the same treatment after "years of dealing with Java nonsense in Gradle and Maven": "I hate trying to fix tools that should just fucking work. Here is the input, there is the output, go." Hence: "the stuff I care about most is the stuff I touch the most."

Small projects are the best fit: "when I am doing small projects like browser extensions and things like that, I actually do not need to touch the code it spits out too much. For those smaller pieces, it is fantastic." Closing verdict: "I know where I can fit the botto in without remorse, I'm comfortable with it's shortcomings and I'm happy knowing the numbers."

**Covers:** Vendor-choice rationale (OpenAI vs others), analysis motivation, personal productivity gains
