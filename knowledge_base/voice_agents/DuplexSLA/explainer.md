> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# hyzhang24/DuplexSLA — In Plain Language

Think of DuplexSLA as a voice assistant that can listen, talk,
think, and use tools — all at the same time, like a person does.

Most voice bots work in turns: you talk, then they think, then they
answer. DuplexSLA removes those rigid turns so conversation and
action flow together without awkward pauses.

## What is this about?

DuplexSLA is a speech model designed for natural, full-duplex voice
conversation — meaning both sides can speak, interrupt, and respond
at any moment.

Its core idea is simple: put listening, speaking, planning, and tool
calling on one shared clock, so nothing has to stop for anything else.

Concretely, the model runs on a repeating 160-millisecond heartbeat.
Every heartbeat it processes three things at once:

- What the user is saying right now (the listening channel).
- What the assistant should sound like next (the speaking channel).
- What the assistant is thinking or doing behind the scenes,
  such as planning words or calling a tool (the action channel).

One model decodes all three channels together, starting from an
existing ~7B-parameter audio model and refined with extra training
on duplex dialogue, turn-taking, and tool-call examples.

## Why does it matter?

Normal voice assistants have a hidden weakness: they can talk or
listen, but they struggle to think and act *while* talking.

Typical problems this causes:

- The assistant cannot gracefully handle interruptions ("wait, stop").
- It goes silent while it looks something up or runs a tool.
- It needs a separate helper just to decide when to pause or respond.
- Planning what to say and doing something useful feel like two
  disconnected steps.

DuplexSLA matters because it gives the model a built-in channel for
thinking and doing during the conversation itself.

That means fewer freezes, fewer missed interruptions, and an
assistant that can keep talking while it quietly gets work done —
much closer to how a human receptionist talks while typing.

## How does it work?

Imagine a conductor keeping three musicians in time with one baton.
The baton taps every 160 milliseconds, and each musician plays their
part on every tap.

1. **Listen.** The user-audio channel continuously absorbs what you
   say, sampled in small slices about 80 milliseconds apart. This is
   the model's ears — always open, never switched off.

2. **Speak.** The assistant-audio channel produces the assistant's
   voice in small speech pieces. Each heartbeat carries one short
   text anchor plus four audio pieces, keeping speech smooth and
   aligned with the shared clock.

3. **Think and act.** The action channel is a short text side-stream,
   limited to about 10 tokens per heartbeat. It carries things like
   delayed transcripts, private planning notes, labels such as
   "pause" or "interrupt," and structured tool calls.

4. **Decide turn-taking from meaning, not just volume.** Instead of
   relying on an external voice detector, the model itself decides
   when to pause, interrupt, or give a small acknowledgement like
   "mm-hmm," based on what is actually being said.

5. **Use tools without stopping the voice.** When it needs to call a
   tool, it writes that call into the action channel at its own
   heartbeat slot. The voice keeps flowing, and tool calls can run
   in the order the conversation requires — including several in a
   row, or one triggered by a quick acknowledgement.

Under the hood, a single backbone model produces all of this jointly,
so speech and actions stay synchronized instead of drifting apart.

## Where can this be used?

Anywhere a voice assistant should feel present and capable while it
works:

- Customer-support phone bots that keep talking while checking an
  order, booking, or account status.
- In-car or on-device assistants that must react to interruptions
  ("no, turn left instead") without freezing.
- Live receptionist or scheduling agents that acknowledge you ("got
  it, one moment") while firing off calendar or search tools.
- Accessibility helpers and companions where natural back-and-forth
  matters more than rigid question-and-answer.
- Research on duplex benchmarks: the project includes DuplexSLA-Bench
  for testing pause, interrupt, acknowledgement behavior, plus single,
  multi-step, and acknowledgement-triggered tool calls.

Note: inference code, model weights, and the benchmark were still
marked coming-soon at the time of the digest — the technical report
is the released artefact so far.

## Conclusions & takeaways

- DuplexSLA treats conversation as one clock, not a sequence of
  take-turns-and-wait steps.
- Three synchronized channels — hear, speak, think-and-act — let the
  assistant stay responsive while getting things done.
- Turn-taking becomes a language decision ("the user means stop"),
  not just an audio-volume decision.
- Tool use becomes part of talking, not a pause from talking.
- The practical payoff is voice agents that interrupt cleanly,
  acknowledge naturally, and act without going silent.

In one line: talk, listen, think, and do — together, on every beat.

## Jargon decoder

| Term | What it really means |
|---|---|
| Full-duplex | Both sides can speak and hear at the same time, like a phone call, not walkie-talkie turns. |
| Shared chunk timeline (160 ms) | A repeating 160-millisecond heartbeat that keeps listening, speaking, and acting in step. |
| User audio channel | The model's ears: a stream of what the user sounds like, sampled every ~80 ms. |
| Assistant audio channel (TA4) | The model's voice: each heartbeat emits 1 text anchor plus 4 small speech pieces. |
| Action channel | A short side-stream for thinking and doing: notes, labels, and tool calls, capped per heartbeat. |
| Text anchor | A tiny text hint attached to each speech chunk to keep the voice on-message. |
| Turn-taking (pause / interrupt / backchannel) | Deciding when to stop, cut in, or murmur "uh-huh" — here decided by the model from meaning. |
| Semantic VAD | An external loudness/voice detector; DuplexSLA replaces it with the model's own judgement. |
| In-conversation tool calling | Looking something up or triggering an action mid-sentence without halting speech. |
| Backbone (~7B, CPT + post-training) | The base ~7-billion-parameter audio model, further trained on duplex and tool-use dialogues. |
| DuplexSLA-Bench | The project's test suite for interruptions, acknowledgements, and mid-talk tool use. |
