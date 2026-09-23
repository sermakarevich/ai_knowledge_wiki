> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# DeepL Voice: Real-Time Speech-to-Speech Translation | IJCAI — In Plain Language

## What is this about?

Imagine you are on a video call with colleagues in Tokyo, Berlin, and São Paulo.
Everyone speaks a different language, yet everyone needs to follow the
conversation as it happens — not five minutes later from meeting notes.

DeepL Voice is a system that tries to solve exactly that problem.
It listens to what people say in one language and translates it,
in near real time, so others can read or hear it in their own language.

The paper presents it as a working product, not a lab experiment.
It was launched in November 2024 and is aimed squarely at
global business communication: meetings, on-site conversations,
and software products that want to add live translation.

The core design choice is deliberately practical.
Instead of waiting for a futuristic all-in-one model,
the team shipped a step-by-step ("cascaded") system that works now,
while continuing to research more ambitious designs in parallel.

In short: this is a "translate speech as it happens" product,
built for reliability in everyday business settings.

## Why does it matter?

Anyone who has used live captions on a call knows the two big frustrations:
mistakes in hearing the words, and translations that jump around.

The second problem has its own nickname: "flickering."
You see a translated sentence appear, then change, then change again,
and you no longer know which version to trust.
For casual chatting that is annoying; for a business negotiation,
it can be genuinely confusing.

DeepL Voice matters because it tackles both problems at once.
It pairs its own speech-recognition models (described as competitive
in quality) with a translation stream designed to stay stable —
no flickering — while still keeping delays short.

It also matters because of scale and fit.
The system supports 18 input languages and more than 30 target languages,
and it adds business-specific controls: you can adjust formality
(say, formal "you" versus informal "you") and supply glossaries
so product names and company terms translate consistently.

That combination — live, stable, and business-appropriate —
is what turns translation from a demo trick into something
a company can rely on every day.

## How does it work?

Think of the system as a relay race with three runners,
each handing a baton to the next as fast as possible.

**Runner 1: Listen and write down.**
Specialized speech-recognition models listen to the incoming audio
and turn it into text, word by word, while the person is still speaking.
These are proprietary real-time models built by DeepL.

**Runner 2: Translate steadily.**
The transcribed text is translated into the target language
through a "stable text streaming" step.
The key idea: instead of showing you every rough guess and then
correcting it (which causes flickering), the system streams out
translations that stay put once shown, without adding much delay.

**Runner 3: Show or speak.**
The translated text appears as captions or subtitles in meetings
and conversations. Spoken output exists too, though the most
advanced version — a voice that clones the speaker's own voice —
is still under development and not yet released.

Behind the scenes, the team keeps two tracks going:
the cascaded step-by-step design described above (the shipped product),
and experimental end-to-end designs that would merge the steps,
researched in parallel for the future.

## Where can this be used?

The paper describes three ready-made ways to use the system.

**1. DeepL Voice for Meetings.**
Live translation inside video calls, integrated with
Microsoft Teams and Zoom. Participants follow along
with translated captions while the meeting runs.

**2. DeepL Voice for Conversations.**
Mobile apps for face-to-face situations: a factory visit,
a trade-show booth, a customer meeting where no shared
language exists and there is no time to set up equipment.

**3. DeepL API for Voice.**
A programming interface so other companies can build
live translation into their own apps and services.

Across all three, the same business controls apply:
tune the level of formality and enforce company vocabulary
through glossaries, so the output sounds appropriate
for professional use.

## Conclusions & takeaways

- DeepL Voice is a shipped, production-grade product (November 2024),
  not just a research prototype.
- Its philosophy is pragmatic: build a reliable step-by-step system now,
  research fancier unified models in parallel.
- The headline technical claim is stable, low-delay translation streaming:
  captions you can trust without distracting rewrites.
- Coverage is broad (18 input, 30+ target languages) with business polish
  via formality settings and glossary support.
- The boundary of what is done versus next: voice-cloning spoken output
  is explicitly still in development.
- Bottom line for a non-specialist: if your team works across languages,
  this is the kind of infrastructure that makes multilingual meetings
  feel almost like monolingual ones.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Speech-to-speech translation (S2ST) | Going from spoken words in one language to spoken (or captioned) words in another, automatically. |
| Cascaded system | A design built as a chain of separate steps (hear, then translate, then speak) rather than one giant step. |
| End-to-end system | An alternative design where a single model does the whole job at once, with no separate steps. |
| ASR (automatic speech recognition) | The "ears" of the system: software that turns audio of someone speaking into written text. |
| Proprietary model | A model built and owned by the company itself, rather than borrowed from public research. |
| Stable text streaming | Sending out translated words bit by bit in a way that avoids going back and rewriting them. |
| Flickering | When a live translation keeps changing on screen, so you cannot tell which version is final. |
| Latency | The delay between someone speaking and you seeing or hearing the translation. |
| Formality setting | A control that makes translations sound formal or casual, as business etiquette requires. |
| Glossary support | A custom word list (e.g., product names) that the system must translate in a fixed, approved way. |
| TTS (text-to-speech) | The "mouth" of the system: software that reads translated text aloud as synthetic speech. |
| Voice cloning | A TTS trick where the translated speech sounds like the original speaker's own voice. |
