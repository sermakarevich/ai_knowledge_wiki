> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Reducing Voice Agent Latency with Forced End-of-Utterance — In Plain Language

Think of a voice assistant as a person on the other end of a phone call.
You finish your sentence — and then there is an awkward pause.
Nobody likes that pause. This explainer is about how to get rid of it.

## What is this about?

Imagine you ask a voice agent to book a restaurant table.
You say: "Hi there. Could you book me a table for two tonight at 7 p.m., please?"
Then you stop talking — and nothing happens for a couple of seconds.

That silence is not the assistant "thinking."
It is the speech system waiting to be sure you are really done speaking
before it hands your words over to the part that forms an answer.

This video is about a simple fix from Speechmatics called
"force end-of-utterance." Instead of passively waiting for silence,
you actively tell the system: "The person is done talking.
Give me the final transcript now."

The result: the final, cleaned-up transcript arrives in under 250 milliseconds —
roughly the blink of an eye — instead of after a multi-second wait.

## Why does it matter?

Human conversation runs on fast turn-taking.
When you talk to a friend, you reply within a fraction of a second.
Even a one- or two-second delay feels strange and broken.

For a voice agent, that delay "can kill the flow of conversation
and make it feel weird." People start to wonder:
Did it hear me? Should I repeat myself? Is it frozen?

The old approach — waiting for a stretch of silence plus an extra
safety buffer — is perfectly fine for some jobs.
If you are taking meeting notes or writing captions for a video,
nobody minds a short delay, because nobody is waiting for a reply.

But a conversational agent is different.
Everything downstream depends on the finished transcript:
understanding the request, asking the language model for an answer,
and speaking that answer out loud.
Nothing can start until the transcript is finalized,
so every extra moment of waiting stacks up into a sluggish experience.

Cutting that wait down to under 250 milliseconds is what makes
talking to a machine start to feel like talking to a person.

## How does it work?

Here is the process in plain steps.

**Step 1: You speak, and the system drafts what it hears.**
While you are talking, the recognizer shows "partial transcripts" —
rough, still-changing guesses at your words.
Think of these as pencil sketches: useful, but not finished.

**Step 2: Normally, the system waits for silence.**
The traditional method, called "endpointing," works like this:
hear silence for a while, add an extra safety buffer of silence,
and only then declare the transcript final.
It is cautious, but slow.

**Step 3: Forced end-of-utterance skips the waiting.**
With the new feature, your app sends a short message to the server
that means: "I'm done talking. Give me the finalized transcript."
The server immediately returns the polished, final version —
no silence-watching required.

**Step 4: Any signal can pull the trigger.**
The clever part is that *you* decide what "done talking" means.
It could be a voice-activity detector (software that notices speech stopping),
a push-to-talk button the user holds down, or any custom turn-taking logic.
In the demo, the presenter presses a 3D-printed big red button,
and the finalized transcript appears at the bottom of the screen almost instantly.

**Step 5: The answer pipeline starts sooner.**
Because the final transcript arrives in under 250 milliseconds,
the language model and voice output can get going right away.
The demo shows two everyday requests — booking a table for two
and setting an oven reminder — flowing through with no awkward gap.

In short: drafts on top while you speak, a decisive "we're done" signal,
and a final transcript at the bottom in a flash.

## Where can this be used?

Anywhere a person talks to a machine and expects a quick reply:

- **Customer-service phone agents** that answer questions and book appointments.
- **Smart speakers and in-car assistants** where a pause feels especially unnatural.
- **Hands-busy helpers** — kitchen, workshop, or accessibility settings —
  where push-to-talk or a physical button marks the end of a request.
- **Live translation and receptionist bots** that must keep a natural rhythm.
- **Developer platforms:** the feature ships in the Speechmatics voice SDK
  (the high-level toolkit), the real-time API, and the real-time SDK
  (the lower-level building blocks), with support for popular agent
  frameworks like Pipecat and LiveKit on the way.

The common thread: if silence-waiting is what slows you down,
a decisive end-of-turn signal speeds you back up.

## Conclusions & takeaways

- The "couple of seconds" of dead air after you speak comes mostly
  from waiting on silence, not from the AI thinking.
- Silence-based finishing is fine for notes and captions,
  but conversational agents "need something faster and more decisive."
- Forced end-of-utterance hands control back to you:
  one simple call tells the server to finalize the transcript now.
- Pair it with whatever turn signal fits — voice-activity detection,
  push-to-talk, a button, or your own logic.
- The payoff is concrete: a final transcript in under 250 milliseconds
  and a conversation that keeps its flow.
- If you are building a voice agent, this is one of the cheapest,
  highest-impact latency wins available.

## Jargon decoder

| Term | What it really means |
|---|---|
| Voice agent | A program you talk to out loud that talks back, like a phone bot or smart speaker |
| Latency | The delay between you finishing and the system responding |
| Utterance | One chunk of speech — a sentence or request you say in one go |
| End-of-utterance | The moment the system decides you have finished your chunk of speech |
| Endpointing | The job of detecting that finishing moment, traditionally by watching for silence |
| Silence buffer | An extra safety pause the system adds after silence before trusting you are done |
| Partial transcript | A rough, still-changing draft of your words shown while you are speaking |
| Finalized transcript | The polished, locked-in version of your words that the answer is built on |
| Voice activity detection (VAD) | Software that simply notices whether someone is speaking or quiet right now |
| Push-to-talk | A button you hold while speaking and release when done, like a walkie-talkie |
