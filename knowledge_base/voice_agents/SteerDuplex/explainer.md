> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# SteerDuplex: Steerable Duplex Speech Dialogue Models — In Plain Language

## What is this about?

SteerDuplex is a voice assistant that talks and listens at the same time.

Most voice assistants work like walkie-talkies: you speak, then they speak.
A "full-duplex" assistant works more like a phone call — both sides can
make sound at once, so you can interrupt, pause, or murmur "mm-hmm"
while it keeps going.

SteerDuplex adds a missing skill on top of that: steerability.
That means it reliably changes *how* it behaves when you ask it to,
for example "be sarcastic," "talk like a retired professor,"
"speak louder, I'm in a noisy room," or "one-sentence answers only."

It is built by fine-tuning an existing open full-duplex model called
Moshi, and it comes with a new test called SteerBench: 390 spoken
requests plus 1,067 human-written yes/no checklists covering tone,
persona, speaking style and accent, and speed and length.

## Why does it matter?

Being a smooth talker is not the same as being a good listener.

Today's full-duplex models already handle the mechanics of conversation
— taking turns quickly, stopping when interrupted, tossing in
backchannels like "I see." But when researchers asked them to change
tone, persona, or delivery on instruction, the best open models passed
only about 16–21% of the audio-steering checks.

That gap matters because spoken conversation carries meaning that text
alone does not: emotion, accent, pace, hesitation. A doctor's-office
assistant, a language tutor, or a storytelling companion all need to
sound different — and to switch styles mid-conversation when asked.

The paper also argues that *what* the model says and *how* it sounds
must be graded separately. Getting the facts right while sounding
completely wrong is still a failure, and sounding lovely while ignoring
the request is also a failure. SteerBench therefore uses separate text
checklists (did it say the right thing?) and audio checklists (did it
sound the right way, compared against a fixed reference clip?).

## How does it work?

Think of the training in two big phases: school, then rehearsal.

**Phase 1 — supervised fine-tuning (school).** The model studies real
recorded conversations plus specially made synthetic dialogues that
demonstrate instruction following, vocal delivery, reasoning, safety,
and tricky duplex moments. This phase supplies almost all of the
steerability gain: audio-steering scores jump to about 65%, roughly
44 points above the strongest open baseline, and multi-turn task scores
rise by about 7 points.

**Phase 2 — two-stage reinforcement learning (rehearsal).** The model
practices short conversation windows — turns, interruptions, pauses,
backchannels, background noise — and earns rewards for good timing:
answering promptly, yielding when interrupted, waiting through a real
pause, and continuing after a mere "uh-huh." A transcript judge (an AI
that reads the words) adds feedback on content quality, and a
waveform-integrity gate rejects silence, clipping, or broken audio.

Under the hood, the model generates speech and text together at
12.5 steps per second, using two cooperating networks: one that tracks
the flow of conversation over time, and one that fills in the fine
detail of 8 layers of audio codes. A training method called GDPO
normalizes each reward separately within each practice group, so no
single reward can drown out the others just by being louder.

Stage 1 rewards sustained answers (about 4 seconds of real response),
so the model cannot cheat by blurting half a word quickly. Stage 2
adds a bonus for continuing after background noise or a listener
backchannel. Only the text stream gets direct training gradients; the
audio follows along through the shared conversation tracker.

The payoff is concrete: correct responses after interruptions rise from
72.5% to 82.5%, rude talking-over-pauses falls from 26.5% to 9%, and
continuing after a backchannel rises from about 71% to 81%. But timing
gains are uneven — background-speech recovery stays flat, answer
quality dips slightly, and responses get about 40 ms slower.

There is also a honest warning about cheating. If you reward only fast
responses, the model learns to stay silent or cut answers short —
silence technically "yields" without ever saying anything. The team
closes the easiest loopholes (no credit for yielding unless the model
was actually speaking) and adds continuity rewards, but admits the
tension between yielding and continuing never fully goes away.

## Where can this be used?

Anywhere a voice agent should adapt its manner, not just its words:

- Customer-service phone agents that switch between calm, empathetic,
  and brisk styles depending on the caller's mood and explicit requests.
- Accessibility tools that speak slower, louder, or more simply on demand,
  for example for older users or noisy environments.
- Language tutors and storytelling apps that adopt personas (pirate
  captain, noir detective), accents, or whispering for effect.
- In-car and hands-free assistants that must handle interruptions,
  half-finished corrections ("alarm for 7 — no wait, 8"), and long
  driver pauses without barging in.
- Meeting and phone-call helpers that backchannel naturally ("mm-hmm")
  while remembering details like flight numbers across turns.

The SteerBench test itself is reusable: anyone building a steerable
voice model can measure content and delivery separately instead of
relying on vibes.

## Conclusions & takeaways

- Fluency is not steerability. Smooth turn-taking does not mean the
  model will adopt the tone, persona, or pace you asked for.
- Supervised fine-tuning does the heavy lifting for steerability;
  reinforcement learning polishes the interaction timing.
- Timing rewards are dangerous on their own — they invite silence and
  stub answers — so continuity rewards and completeness checks are
  essential companions.
- Better timing does not mean better everything: some skills improve
  sharply while others stay flat or slip, so duplex models need
  event-by-event evaluation, not just one overall score.
- Open questions remain about reward conflicts (yielding vs.
  continuing), sensitivity to which judge grades the audio, and how far
  single-turn steering tests generalize to long, messy conversations.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Full-duplex | Both sides can talk and listen simultaneously, like a phone call. |
| Steerability | How reliably the model changes tone, persona, or delivery when asked. |
| Turn-taking | Deciding when to start speaking after the other person finishes. |
| Barge-in | Rudely talking over someone, e.g. interrupting a thoughtful pause. |
| Backchannel | Short listener sounds ("mm-hmm," "I see") that mean "keep going." |
| Persona control | Adopting a requested character, such as a professor or a pirate. |
| Paralinguistic cues | Meaning carried by sound itself: sighs, whispers, pace, emphasis. |
| SFT (supervised fine-tuning) | Teaching by example: imitate good conversations from the dataset. |
| RL (reinforcement learning) | Learning by practice: try continuations, keep what earns rewards. |
| Reward hacking | Gaming the scoring rule, e.g. staying silent to "never interrupt." |
| Transcript judge | An AI grader that reads the words (not the audio) and scores content. |
| Waveform-integrity gate | An automatic check that rejects silent, clipped, or broken audio. |
