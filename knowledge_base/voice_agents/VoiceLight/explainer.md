> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Voice-Light: A Full-Duplex Cascaded Voice Agent with Causal Turn-Taking and Speculative Generation — In Plain Language

Think of Voice-Light as a phone-call assistant that can listen and talk at the same time,
instead of waiting rigidly for its turn like most voice bots do today.

## What is this about?

Voice-Light is a voice assistant built as a chain of three familiar parts:
it hears speech and turns it into text, a language model decides what to say,
and a voice synthesizer speaks the answer out loud.

The new part is how it handles live conversation.
The microphone stays open even while the assistant is speaking,
so it can notice interruptions, short pauses, and background remarks.

Its central rule is simple: the system may start work early when it is unsure,
but nothing becomes audible or permanent until an explicit check approves it.
Only speech the listener's browser confirms was actually played
counts as part of the conversation history.

In plain terms, it prepares answers quietly in the background
and only speaks them once it is fairly confident the user has finished.

## Why does it matter?

Talking to a machine feels awkward when it keeps cutting you off
or waits too long before answering.
The hard problem is telling a real "I finished" silence
apart from a short "let me think" pause.

Most systems solve this with a simple silence timer.
Voice-Light tried to do better with a small learned detector
that reads the speech recognizer's internal signals
and predicts whether the user is done.

That attempt is the honest headline of the paper: it did not win.
On 1,673 real-conversation pauses, the learned detector cut people off
rarely (2.70% false cutoffs) but caught only 12.53% of finished turns,
while a plain Silero timing policy caught 95.60% at the same cutoff rate.
So the team kept a hybrid controller where the timer stays in charge
and the learned signal is only an advisor.

The value is therefore the plumbing and the candor:
a reproducible way to mix uncertain AI guesses into a safe live controller,
plus published data, code, and clearly stated limits.

## How does it work?

Sound flows from the browser microphone to the server over one connection.
A fast acoustic detector reacts the instant speech starts,
while a persistent streaming recognizer produces running transcripts.

A tiny turn-taking adapter — about 183,000 trainable parameters —
sits on top of the frozen 0.6-billion-parameter Nemotron speech encoder.
It reuses the recognizer's own internal layers instead of loading
a second large speech model, and it only ever looks at past sound,
never the future.

A typed controller combines these signals with transcript revisions,
playback state, and conservative deadlines.
Reactions are staged by confidence: speech onset may quietly lower
the assistant's volume, but only stronger word-level, learned,
or timeout evidence commits to cancelling playback.

Meanwhile the language model (Qwen) drafts replies and typed tool calls
such as search, calculate, and get-time, while Kyutai voice synthesis
prepares sound only for text the controller has released.
This "speculative generation" stays private until transcript
and turn checks promote it — failed guesses are thrown away silently.

Training mixed synthetic and real material.
Roughly 3,999 scripted tool-use conversations taught the spoken protocol,
about 1,092–1,097 synthetic timelines per release (~21.8 hours each)
taught turn-taking patterns, and a locked set of 107 real conversations
(36.30 hours) provided the human check.
The deployed adapter (step 750) was picked on human validation
because synthetic-only scores transferred poorly to real speech.

In a small live test — three unscripted sessions, 36 answer turns —
the median delay from the final speech boundary to the first reply audio
was 758 ms, with 21 of 36 turns under 800 ms.
Turns that reused speculative work tended to be faster,
though that comparison is observational, not a proven speedup.

## Where can this be used?

Anywhere people talk to machines and interruptions are normal:
customer-service phone lines, hands-free car or kitchen assistants,
live translation or meeting helpers, and accessibility tools
for people who need patient, barge-in-friendly conversation.

The design fits teams that want inspectable pieces —
transcripts, tool calls, playback state, cancellation —
rather than one opaque end-to-end speech model.
Because canceled audio never enters the durable history,
it also suits settings where records must reflect
what the caller actually heard.

It is not a drop-in product: the live evidence is one operator,
three sessions, English-first, and the learned detector
still defers to the timer.

## Conclusions & takeaways

Voice-Light shows how to build a full-duplex voice agent
from ordinary parts plus careful control logic:
react fast but reversibly, prepare early but publish late,
and trust only acknowledged audio.

Its main lesson is a negative result stated openly:
strong synthetic-data scores (near 0.93 ranking quality)
fell to roughly 0.56–0.60 on real human pauses,
and no tested detector passed the joint cutoff/recall/latency gate,
so the follow-up test split stayed sealed.

Take away three things: start uncertain work early but commit late;
measure learned components where they will actually run;
and keep a boring, reliable fallback — here, the silence timer —
when the clever model is late or wrong.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Full duplex | Listening and speaking at the same time, like a phone call, not walkie-talkie turns. |
| Cascaded agent | A voice bot built as a chain: speech-to-text, then language model, then text-to-speech. |
| Turn-taking / endpointer | Deciding when the speaker finished so the assistant may reply. |
| False cutoff | Mistaking a mid-thought pause for a finished turn and jumping in too early. |
| EOT recall | Share of genuinely finished turns the system correctly detects in time. |
| Causal adapter | A small add-on model that judges turn state using only past audio, never future audio. |
| Speculative generation | Quietly drafting an answer before the turn is certain; discarded if the guess was wrong. |
| Acknowledged audio | Reply sound the browser confirms was actually played; the only history the system trusts. |
| HOLD pause | A silence where the same speaker keeps going afterward — exactly what must not trigger a reply. |
| Hybrid controller | The referee combining timer, transcript, and learned signals, with the timer as backstop. |
