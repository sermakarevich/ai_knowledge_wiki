> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# stimm-ai/stimm — In Plain Language

## What is this about?

Stimm is a toolkit for building voice assistants
that feel fast and natural to talk to.

Think of a normal voice assistant: you speak,
then it goes quiet while it "thinks,"
and only then answers. That pause feels awkward.
Stimm fixes this by splitting the job
between two helpers working side by side.

One helper is the talker. It listens to you,
understands your words quickly,
and starts answering almost right away.
The other helper is the thinker.
It watches the conversation in the background,
does the harder work like looking things up
or making plans, and quietly passes
better instructions to the talker.

Under the hood, Stimm is built on top of LiveKit,
a popular system for real-time audio and video calls.
It adds the voice-assistant logic on top: hearing,
quick answering, speaking, plus the background thinking.

## Why does it matter?

Talking feels very different from typing.
When you chat by text, a short delay is fine.
When you talk by voice, even a one-second silence
feels broken, like the other person stopped listening.

Stimm matters because it removes that awkward waiting
without giving up smart answers. Most systems force
a trade-off: either answer fast but simply,
or answer smartly but slowly. Stimm tries to give you both.

It does this with a simple idea borrowed from websites:
respond optimistically. A website might show your "like"
immediately and sort out the details in the background.
Stimm does the same for voice: acknowledge you right away,
start speaking early, and keep the deeper thinking
running in parallel.

This is especially important for phone assistants,
customer support lines, kiosk helpers, and any hands-free
helper where people expect a snappy,
human-like back-and-forth.

## How does it work?

A conversation in Stimm flows through a short chain of steps.

First, the system detects when you start and stop speaking.
Then it turns your speech into text.
Then a small, fast language model drafts a quick reply.
Finally, a speech voice reads that reply out loud.

A useful detail sits between drafting and speaking:
a small waiting buffer. Instead of reading out every
half-word the moment it appears, Stimm can wait
for a whole word, a few words, or a punctuation mark.
You can tune this from "say everything instantly"
to "wait a bit for smoother speech."
The default waits for about four words or a punctuation mark.

Meanwhile, the second helper — the supervisor — watches
a live copy of the conversation. It can run bigger models,
use tools, or do planning. When it has something better
to say, it sends a short instruction to the talker
over a structured message channel. The talker stays
in charge of the live turn, so the first reply is never
blocked waiting for the thinker.

You can run this in three styles: a fully independent talker,
a talker that only says what the supervisor tells it,
or a mix of both. The mix is the default:
answer fast on your own,
but accept steering from the supervisor.

Setting it up is meant to be simple. You install
the small core package, then add only the speech
and AI providers you actually picked, such as one service
for hearing and another for speaking. A built-in catalog
and setup wizard help you choose, and your app only saves
your choices — never secret keys or internal wiring.

## Where can this be used?

Stimm fits anywhere a voice needs to feel instant
but still stay smart.

Good examples include customer support phone lines
that should greet you immediately while looking up
your order in the background, phone and internet-call
assistants that need to sound responsive before all
the business logic finishes, and live copilots
that start explaining early while a supervisor checks
facts or corrects course.

It also suits physical places like stores,
reception desks, or kiosks, where a slow or silent machine
feels broken and people judge mostly by how quickly it reacts.

For builders, it fits apps that already use LiveKit
for calls and want to add a voice agent,
in either Python or TypeScript, without rebuilding
the whole hearing-thinking-speaking pipeline from scratch.

## Conclusions & takeaways

The big idea is simple: one helper talks fast,
one helper thinks deep, and they collaborate in real time.

The practical result is a voice assistant
that acknowledges you immediately, stays interruptible,
and still benefits from deeper reasoning and tools
running alongside. Tunable speech buffering
and three running styles let builders pick their own
balance between speed and polish.

The project also keeps integration tidy:
pick providers through a catalog, install only what you chose,
keep secrets out of logs and saved settings,
and use public building blocks only.
That makes Stimm less of a demo and more of a runtime
you can actually ship inside a product.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Optimistic voice interface | Answering early with your best guess instead of making the caller wait for the full answer. |
| Voice agent (the talker) | The part that handles the live conversation: hearing you and speaking back quickly. |
| Supervisor (the thinker) | The background helper that watches the chat, reasons harder, and steers the talker. |
| Speech-to-text | Turning your spoken words into written text the computer can work with. |
| Text-to-speech | Turning the computer's written reply into a spoken voice you hear. |
| Voice activity detection | Noticing when someone starts and stops talking, so the system knows when to listen and when to reply. |
| Pre-speech buffering | Briefly holding back words before speaking so the voice sounds smooth instead of choppy. |
| Runtime mode | A setting that decides who is in charge: the talker alone, the supervisor alone, or both together. |
| Provider | An outside service that does one job, such as hearing, speaking, or thinking — you pick one for each job. |
| Setup wizard | A step-by-step chooser that helps you pick providers and installs only the pieces you selected. |
