> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Realtime-Venus: A full-duplex interaction system with asynchronous delegation — In Plain Language

## What is this about?

Realtime-Venus is a voice-and-video AI assistant that can listen, watch, and speak at the same time.

Most assistants work in strict turns: you finish talking, then they think, then they answer.
Realtime-Venus works more like a person: it keeps listening while it talks, notices small sounds like "uh-huh" or background chatter, and decides whether to keep going, pause, or stop.

It comes in two versions, both with about 9 billion parameters and built on MiniCPM-o 4.5:

- **Realtime-Venus-Omni:** hears audio and sees video.
- **Realtime-Venus-Audio:** hears audio only, for spoken conversation.

Both versions can quietly hand off hard work to a background helper called **Realtime-Venus-Harness**, then keep talking while that work finishes and weave the answer back into the conversation.

A concrete example: you ask in Chinese which car tail numbers are restricted in Beijing today. The assistant says "let me check," sends a private background request, keeps listening, and later speaks the result: tails 2 and 7 are restricted from 7am to 8pm inside the 5th Ring Road.

## Why does it matter?

Normal conversation and computer work run at very different speeds.

Chatting needs an answer in a fraction of a second. Looking something up, reasoning, or calling a tool can take much longer. If the assistant freezes while it "thinks," the conversation feels broken.

Realtime-Venus separates those two jobs:

- The **foreground** keeps the conversation alive: listening, speaking, reacting.
- The **background** does the slow work: searching, reasoning, calling tools.

This matters because real life is messy. People hesitate, interrupt, correct themselves, talk to someone else nearby, or have noisy rooms. A useful assistant must tell "keep going, that was just a backchannel" from "stop, I changed my mind."

The reported results suggest the idea works without losing basic understanding:

- Omni led compared online models on six of eight video benchmarks, including
  StreamingBench at 70.2%, OVO-Bench at 64.7%, and Daily-Omni at 81.3%.
- Audio led on MMAU at 78.0%, MMAU-Pro at 63.2%, Llama Questions at 83.8%,
  and Speech CMMLU at 67.8%, with a tied-best AlpacaEval score of 4.81.
- Audio continued correctly 97% of the time after backchannels, 88% after
  speech directed at someone else, and 86% after background speech.

## How does it work?

Think of it as two loops sharing one clock.

**1. One shared timeline, cut into one-second pieces.**

Everything — what you say, what the assistant says, and what the background helper returns — is lined up on the same timeline. The system processes the conversation second by second, so a late background answer still matches the right moment.

**2. Each second, a simple decision: listen or speak.**

Every chunk, the model predicts a control signal:

- `<|listen|>`: stay quiet and keep perceiving.
- `<|speak|>`: produce the next bit of speech.
- `<|turn_eos|>`: end the turn.

Speech is scheduled to match playback, so text is emitted faster or slower depending on whether the spoken audio is lagging or has spare capacity.

**3. Interruptions are interpreted, not just detected.**

Any overlap does not automatically mean "stop." The rule is based on meaning:

- Pause or noise: keep listening.
- Short "yes" or "right": keep speaking.
- Real interruption where you take the floor: stop, then repair, update,
  redirect, or follow up. Already-played audio cannot be undone.

**4. Hard questions are delegated privately.**

If a request needs outside information, broader context, or replanning, the assistant writes a hidden delegation note. That note fixes what evidence the background task should use, so later conversation changes do not corrupt it.

The harness runs the task, checks whether the result is still fresh, waits for a good moment, and hands it back as private context. The frontend then decides how to say it given what you want now — which may have changed.

Simple or urgent replies stay local and are answered immediately.

**5. Long videos get an extra memory.**

The Omni version adds a training-free memory. It saves only frames with meaningful visual change, finds relevant old frames by matching the question, prefers diverse scenes, then reassembles those frames plus nearby audio in time order. This helped hour-long video scores, e.g. about +5.88 points on a 60–90 minute split.

**6. Training ties it all together.**

One post-training pass mixes offline understanding, live proactive conversation, and delegation examples — over 2.8 million samples, about 72,200 sessions, 1,600 hours of audio. Only response parts are supervised; only the language-thinking part is updated and the voice synthesizer stays fixed.

## Where can this be used?

- **Live voice assistants:** ask, interrupt, or correct yourself without restarting the conversation.
- **Video-aware helpers:** watch a match or meeting and speak up when something happens, e.g. a wicket reaction.
- **Driving or hands-busy use:** check rules, news, or schedules while background lookup runs and listening continues.
- **Meetings and multi-person rooms:** ignore side talk and background noise but respond when actually addressed.
- **Customer service:** acknowledge immediately ("checking that now"), look things up in the background, then deliver naturally.
- **Long video review:** search across tens of minutes or hours without keeping every frame in working memory.

The limits are honest too: interrupting behavior still trails some stronger
interrupters, tool arguments and full task success lag GPT-Realtime, and the two
frontends fail differently — Audio tends to delegate too often, Omni too rarely.

## Conclusions & takeaways

Realtime-Venus shows that liveness and usefulness do not have to conflict.

Keep a fast loop for talking and listening, run a slower loop for thinking and
tools, and connect them with a shared timeline plus careful handoff rules.

Three ideas carry over beyond this system:

1. Treat turn-taking as meaning, not volume: continue through backchannels,
   yield to real interruptions.
2. Freeze the evidence when background work starts, but reinterpret the result
   when it returns, because intent may have moved on.
3. Train conversation control and delegation together, so "when to speak" and
   "when to look something up" are one decision, not two systems bolted together.

In short: talk now, think in the background, and rejoin the conversation gracefully.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Full-duplex | Listening and speaking at the same time, like a phone call, not walkie-talkie turns. |
| Frontend | The part you interact with: it listens, decides, and speaks. |
| Realtime-Venus-Harness | The background worker that runs slow tasks and returns answers to the conversation. |
| Asynchronous delegation | Quietly handing work to the background while the chat continues, instead of freezing. |
| Backchannel | A short listener sound like "uh-huh" that means "keep going," not "stop." |
| Interruption | When the speaker is cut off and the floor changes; may need stop, repair, or redirect. |
| Evidence snapshot | A frozen copy of what the request meant at the time, used for background work. |
| Freshness check | A test of whether a late background answer is still relevant before speaking it. |
| Thinker–Talker | Two-part voice design: one part plans words, the other turns them into speech sounds. |
| Long-video memory | An external notebook that saves and retrieves important old video moments. |
