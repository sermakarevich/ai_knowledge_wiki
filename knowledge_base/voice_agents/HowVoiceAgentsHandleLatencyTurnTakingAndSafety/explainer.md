> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# How Voice Agents Handle Latency, Turn-Taking, and Safety | Interview With Kræn Hansen — In Plain Language

## What is this about?

This is a plain-language guide to an interview about how voice agents work.

A voice agent is a machine you talk to out loud, like calling a helper on the phone.

Your speech is converted to text, a text-based AI thinks up a reply, and that reply is spoken back to you.

The special part is that the spoken reply can laugh, whisper, and sound expressive — so human-like that listeners sometimes cannot tell who is the person and who is the machine.

The interview focuses on three hard problems: delay before the agent answers, deciding whose turn it is to speak, and keeping the agent safe and honest.

## Why does it matter?

Delay is the biggest pain point in voice agents.

On a phone call, even a short silence feels broken — you wonder if the call dropped or if you should repeat yourself.

So builders cannot just make the AI smarter; they have to make waiting feel natural.

Turn-taking matters for the same reason: real conversations have nods, "yeah" and "okay" sounds, and polite interruptions.

A voice agent that cuts you off every time you say "yeah" feels rude and stupid.

Safety matters because a friendly human-like voice builds trust fast.

A banking helper must never give financial advice, and no agent should pretend to be human when asked directly.

## How does it work?

Think of the system as three steps in a chain.

First, speech-to-text turns your voice into written words.

Second, a text AI reads those words and writes a reply.

Third, text-to-speech speaks the reply out loud with expression.

The middle step — the text AI thinking — takes about 40 to 70 percent of the total waiting time.

Since that wait cannot be removed entirely, builders hide it the way good waiters do: they show something is happening.

The trick is called perceived latency, meaning how long the wait *feels*, not just how long it *is*.

The agent keeps background presence audible, like soft office noise or music, so you know the call is still alive.

When it needs time to look something up, it says so out loud — "I'm gonna look you up in the system" — and may play sounds like keyboard clicking while it works.

Turn-taking works on a simple rule: either you talk or the agent talks, but you are allowed to make small sounds without stealing the turn.

The speech-to-text layer tries to tell the difference between a backchannel ("yeah, yeah, okay" meaning "I'm listening") and a real interruption ("stop, I meant something else").

Only a real interruption cuts the agent off; a mere nod lets it keep talking.

Safety is handled by a second AI standing on the side like a supervisor with a kill switch.

If the main agent starts going off the rails, the supervisor cuts the conversation off.

There are two ways to run that supervisor: streaming or blocking.

In streaming mode, audio flows to you right away and gets cut only if something bad is heard — faster but riskier.

In blocking mode, every word is checked before any audio plays — safer but slower.

Everything is tunable under one general rule: the faster you make the stack, the less expressive or less correct it becomes.

Pushing expressiveness too far can even backfire, adding little hesitations that make the agent sound unsure.

To balance speed and smarts, a quick simple model can act as a receptionist and hand hard questions to a bigger, slower expert model.

The voice can stay the same across the handoff or change tone, for example sounding more serious when moving to loan advice.

Builders reach all of this through layered toolkits: a universal JavaScript library, a React package with hooks on top, and a React Native package that adds phone-microphone input.

You can bring your own screen design or use ready-made pieces like an agent view or an embeddable chat bubble.

## Where can this be used?

Customer support phone lines are the clearest fit: a fast receptionist model routes callers, and harder cases go to an expert sub-agent.

Banking and finance helpers can answer account questions while the safety supervisor blocks forbidden topics like financial advice.

Appointment booking and lookup tasks benefit from narrated waiting — "let me check the system" plus typing sounds — instead of dead silence.

Any existing text chatbot can gain a voice through the middle tier: you keep your own AI brain and the platform handles the speaking and listening parts.

Mobile apps can add voice with the React Native package, and websites can drop in a chat bubble without building a whole voice system from scratch.

## Conclusions & takeaways

A voice agent is a speech-to-text → text-AI → text-to-speech chain, and the text AI causes most of the delay.

Because delay cannot be fully removed, good design manages how the wait feels: background presence, honest narration, and work sounds.

Polite turn-taking means ignoring little "yeah" and "okay" sounds but yielding to real interruptions.

Safety comes from a supervisor AI plus a clear choice: streaming for speed, blocking for maximum caution.

The golden tradeoff to remember is simple: faster means less expressive or less correct, so tune each use case on purpose.

And because the voice can sound almost human, the agent should always admit it is a machine when asked.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Voice agent | A machine you talk to by voice that listens, thinks, and speaks back |
| Speech-to-text | The step that turns your spoken words into written text |
| Text-to-speech | The step that turns the AI's written reply into spoken audio |
| LLM (large language model) | The text AI in the middle that understands words and writes replies |
| Expressive TTS | A speaking voice that can laugh, whisper, and sound emotional instead of robotic |
| Latency | The delay between you finishing speaking and the agent starting to answer |
| Perceived latency | How long the wait *feels* to you, which good design can shorten even if the real wait stays the same |
| Turn-taking | The rules for who speaks when, and how interruptions are handled |
| Backchannel | A small listener sound like "yeah" or "okay" that means "I'm following you," not "stop talking" |
| Guardrail / sidecar LLM | A second supervisor AI that watches the main agent and cuts it off if it says something forbidden |
| Streaming vs blocking safety | Two supervisor styles: let audio play and cut on violation (faster) versus check everything first (safer, slower) |
| Router + sub-agent | A quick simple model that greets callers and passes hard questions to a bigger expert model |
