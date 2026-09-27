> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# What's Next After RLHF — Talk Opening and Speaker Intro

**In one sentence:** The speaker reframes the talk as what's next after the ChatGPT / assistance era, arguing today's RLHF-built AI is excellent at pleasing a human in the loop but not at autonomous automation, so what comes next must be real automation and smarter software.

## Key points

- The talk is titled "what's next after RLHF" but reframed as "what's next after the ChatGPT era," with the claim that the Claude Code era is not next because Claude Code belongs to the same assistance era.
- The speaker introduces himself in the chunk as "Tiago Almeida," claiming co-authorship of GPT-4, ChatGPT, and RLHF / instruct GPT, and that his team "basically invented post-training as a concept."
- He states he is one of the few OpenAI people who "hates on" ChatGPT — clarifying he loves it as a world-changing product, but blames minor decisions in the ChatGPT algorithms for much of the field's current state.
- He maps two extreme camps: cult one says AI is going "insanely well" with every NLP benchmark crushed and autonomous operation time growing exponentially, while cult two says AI is going "insanely poorly" as a bubble of circular financing deals producing only chat apps.
- His proposed sane explanation is the assistance-vs-automation divide: left-side successes are intrinsically human-in-the-loop tasks whose goal is to please the human, while right-side failures are tasks whose goal is to remove the human loop entirely.
- Lesson one stated in the chunk: everything inherited from RLHF is incredible at human-in-the-loop stuff but not automation, so businesses learn "do not use AI for decisions with stakes to your business" and push costs onto the user.
- RLHF is described as the algorithm behind roughly "100% of LLMs" by usage — "just collect human preferences, optimize for human preferences" — which is why every LLM requires a human in the loop, why "overpromising is a feature," and why the end game is optimizing for engagement, illustrated by the fart-sound-effects "eerie vibe atmosphere piece" anecdote.
- Lesson two and three stated in the chunk: today's AI was designed for assistance through human-preference optimization, while tomorrow's AI will be for automation with "smarter software" rather than unchanged-since-2019 SaaS plus a latched-on chatbot or just "just-in-time software"; his company TypeSafe is redesigning the AI stack for reliability and automation via a third post-training approach beyond RLHF and RLVR, optimized for calibrated decision-making.

---

## Opening and speaker credibility

The speaker opens interactively ("Feel free if you don't disag- agree with something to yell out"), polls the audience on who knows RLHF, and introduces the topic as "what's next after RLHF," immediately correcting it to "what's next after the chat GPT era that I think we're all in." Verbatim hint: "it is not the Claude code era. I will justify this later on, but I actually believe them to be part of the same era." Credibility claims, verbatim in substance: "co-authored to GPT-4, chat GPT, RLHF {slash} instruct GPT" and "the team I was part of basically invented post-training as a concept."

**Covers:** talk opening, audience poll on RLHF, title reframing, speaker introduction and credentials

## The two cults and the sane-view question

| Camp | Claim as stated in chunk |
|---|---|
| Cult one: AI insanely well | Every benchmark surpasses human level, continuously and accelerating; basically every NLP benchmark "getting crushed"; time LLMs can operate autonomously growing exponentially |
| Cult two: AI insanely poorly | AI is a bubble generating no value, just circular financing deals; if AI is so great, why is everything just a chat app or Claude-like thing; retreat from transformative-AI talk to "massively valuable B2B SaaS" talk |

The speaker says the only agreement is that "everyone basically thinks AI is insane, but like for different reasons," and asks for the simplest explanation of how unsolved math problems get solved while customer service still needs humans in the loop for "dumb tasks."

**Covers:** spectrum of opinions, cult-one vs cult-two evidence, puzzle of hard tasks solved vs easy tasks failing

## Assistance vs automation as the explanation

His answer: left-side tasks have the goal of pleasing the human in the loop ("Claude code's job is not to just make code work"), while right-side basic tasks have the goal of removing the human loop — ideally running unseen on a server until it becomes legacy software. This is labeled "the divide between assistance and automation." Business consequence stated: "do not use AI for decisions with stakes to your business," with the pattern "make sure that all of the costs are to the user and not to your business" — e.g., fine to flood the user with docs in customer service, not fine to let AI make expensive decisions.

**Covers:** assistance-vs-automation thesis, lesson one, business pattern of avoiding high-stakes AI decisions

## What RLHF is and why it forces human-in-the-loop

Summary given in the chunk: "it is just collect human preferences, optimize for human preferences," referencing the OpenAI team's blog post with annotated preference-collection vs optimization parts. Claims: roughly "100% of LLMs are trained with RLHF" by usage; therefore "we literally put them in the loop." Consequences: "overpromising is a feature... by design," with a persistent gap between human preference and good results even when results are good; models err toward what pleases the human when uncertain. Example quoted: sending ChatGPT an audio file of fart sound effects asking for "a straight honest reaction" to self-made music, getting back "It's a very eerie vibe atmosphere piece." Stated end game: "optimizing for engagement," whereas automation wants the model to "not give a[ ] about the humans and just do the task correctly in a calibrated way." Labeled lesson two: "today's AI was designed for assistance through optimizing for human preference."

**Covers:** RLHF definition, 100% claim, preference vs results gap, fart-audio anecdote, engagement vs calibration

## Why Claude Code is still the old era, and what automation means

The speaker returns to the opening clue: "it's not Claude code because Claude code is still part of that assistance era. Claude code is still RLHF," adding that a purely RLVR version "would look very very different," and that the agentic-capability vs following-what-you-want trade-off in optimization space still does not add automation. Logical answer: "what's next after assistance is real automation." On software: "all of the SaaS basically has not changed since 2019... except sometimes a chatbot is like latched on," which he calls predictable because AI is "assistance native." Contrasts early OpenAI charter language about doing tons of work with today's direction of cheaper-to-write code; quotes Garry Tan's "golden age of just-in-time software" as a double-edged compliment because he wants "smarter software" with more expressive building blocks, not just automated writing of same-expressibility software.

**Covers:** Claude Code still RLHF / assistance era, RLVR contrast, SaaS-unchanged-since-2019 claim, just-in-time vs smarter software

## TypeSafe pitch and Q&A fragments

Lesson three as stated: the field took "a weird detour," and "Tomorrow's AI... will be for automation" with "actual work that is automated," which is currently "a rounding error despite LLM's intelligence." TypeSafe's core question, quoted in substance: "what if the AI stack was redesigned for reliability and automation?" plus a call to join the mailing list / careers page and follow him on Twitter for a spicy post claiming "the original scaling laws were incorrect." Q&A fragments in the chunk: pre-training is "phenomenal" and not the problem — the problem is "how we unearth it"; hallucination is "intrinsic to optimizing for human preference" via reward-model asymmetry "like what GANs have" encouraging confident mode-dropping; the new approach "is definitely not RLVR... it is a new thing"; stack view: "data matters more than compute and doing the right task matters way more than data," with RLHF optimizing human preference, RLVR optimizing log error rates of pure correctness, and their third thing optimizing "calibrated decision-making" by "mainlining the intelligence of pre-trained models into like being actually useful for software," including a differently shaped API.

**Covers:** lesson three, TypeSafe automation thesis, scaling-laws teaser, pre-training vs hallucination Q&A, RLHF / RLVR / third-way distinction
