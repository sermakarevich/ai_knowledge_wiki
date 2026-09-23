> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# livekit/eot-bench — In Plain Language

## What is this about?

Voice assistants have one job they repeat hundreds of times per call:
decide, at every little silence, whether you are finished speaking.

eot-bench is an open scorecard for that decision. It asks models a
simple question at each pause — "is the person done talking?" — and
grades how well they answer.

The project ships two things together: a test harness (the grading
machine) and a public dataset of real human-to-agent conversations in
14 languages. Anyone can run the same test and compare results
apples-to-apples.

In short: it turns "our voice bot feels snappy" into something you
can measure.

## Why does it matter?

Before this benchmark, every team tested on its own private recordings
with its own grading rules. Results could not be reproduced or compared.

That matters because getting this decision wrong is very visible:

- Fire too early and the bot talks over you mid-thought.
- Wait too long and every reply starts with awkward dead air.

Both mistakes make people distrust voice agents, even when the
underlying language model is smart. eot-bench gives the whole field
common ground: the same conversations, the same pauses, the same
budgets for speed versus politeness.

It also matters for languages beyond English. The dataset covers
Arabic, Chinese, Dutch, English, French, German, Hindi, Indonesian,
Italian, Japanese, Korean, Portuguese, Spanish, and Turkish — so a
model that only works well in English cannot hide.

## How does it work?

Think of a single user turn as a sentence with a few breaths in it.

1. **Collect real turns.** Each test item is one complete user turn
   from a task-oriented conversation, with audio plus the words said
   so far.

2. **Mark every pause.** Every silence of at least 100 milliseconds
   is marked. The last pause is the true ending; all earlier pauses
   are hesitations the bot should listen through.

3. **Ask the model at each pause.** Given only what was available up
   to that moment — no peeking ahead — the model outputs a score:
   how confident is it that the turn is over?

4. **Apply a simple policy.** Three knobs turn scores into behavior:
   a confidence threshold for cutting in, a minimum wait before
   acting on the score, and a maximum wait before giving up and
   taking the floor anyway.

5. **Grade the tradeoff, not one number.** Sweeping those knobs
   traces a curve between two opposing goals: fewer false cutoffs
   (interruptions) versus lower latency (dead air). Models are ranked
   at fixed budgets — e.g. "how snappy at most 5% interruptions?" —
   plus the full tradeoff curve.

6. **Compare against a dumb baseline.** A silence-only detector that
   ignores words and meaning runs the same test, so every smart
   model must prove it beats plain timing.

7. **Publish everything.** Predictions, scores, curves, and
   per-language tables are committed as reproducible artifacts, with
   an interactive leaderboard on top.

The headline result so far: LiveKit Turn Detector v1 leads overall in
English and across all 14 languages, but the value is the shared
ruler, not any single winner.

## Where can this be used?

- **Picking a turn detector.** If you ship a voice agent, run your
  candidate models through the benchmark and pick the operating point
  that fits your product: a phone assistant may tolerate zero
  interruptions, a casual chatbot may prefer speed.
- **Tuning politeness versus snappiness.** The policy knobs map
  directly to product settings, so the benchmark curve becomes your
  config guide.
- **Testing multilingual readiness.** Run the same harness across all
  14 languages to find where your detector degrades before your users
  do.
- **Regression testing releases.** Re-run the harness on each new
  model version; if false cutoffs rise at your latency budget, block
  the release.
- **Research on conversational timing.** Use the open pause-level
  labels to prototype new detectors without collecting private
  voice data first.
- **Demos and bake-offs.** Vendors and teams can argue from one
  public leaderboard instead of competing slide decks.

## Conclusions & takeaways

- End-of-turn detection is a timing judgment under uncertainty, not
  a speech-recognition problem. The user pauses; you guess.
- You cannot be both perfectly fast and perfectly polite. Every
  system lives somewhere on the false-cutoff versus latency curve.
- Single accuracy numbers mislead here. Budgets ("at 300 ms delay,
  how often do we interrupt?") match how products actually feel.
- Latency means conversational dead air — how long the bot holds
  back — not how fast the neural network runs.
- Real pauses in real conversations, in many languages, are what
  make this benchmark trustworthy. Synthetic clips would miss the
  hesitations that cause real talk-overs.
- Open data plus a shared grading harness is the real contribution:
  anyone can reproduce, challenge, or beat the leaderboard.

## Jargon decoder

| Term | What it really means |
| --- | --- |
| End of turn (EoT) | The moment the speaker is truly finished and it is your turn to reply. |
| False cutoff | Interrupting too early — cutting someone off mid-thought. |
| Latency (here) | Dead air after the user finishes before the bot replies; not computer speed. |
| Pause / silence span | A quiet gap of at least 100 ms inside a turn that forces a hold-or-speak decision. |
| Hold | The correct call on a mid-turn hesitation: keep listening, do not reply yet. |
| Threshold | How confident the model must be before it dares to take the floor. |
| Action delay | Minimum waiting time before acting on the model's score; patience knob. |
| Timeout | Maximum wait before the bot speaks up even if still unsure. |
| Pareto frontier | The curve of best achievable tradeoffs — faster always costs more interruptions. |
| VAD baseline | A deliberately simple timer-based detector used as the "beat this" reference. |
| Operating point | One chosen setting on the curve, e.g. "at most 5% interruptions." |
| Adapter | A plug-in that lets a new model or vendor API take the same test. |
