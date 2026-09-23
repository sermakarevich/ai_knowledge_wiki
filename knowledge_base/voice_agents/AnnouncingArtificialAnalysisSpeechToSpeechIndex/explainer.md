> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Announcing the Artificial Analysis Speech to Speech Index | Artificial Analysis — In Plain Language

Think of this as a report card for AI voice assistants — the kind you talk
to out loud, and they talk straight back to you with no text in between.
Until now there was no single score for how good these "talking" models
are, so Artificial Analysis bundled three separate tests into one number:
the Speech to Speech Index.

## What is this about?

Artificial Analysis announced a new leaderboard called the Speech to Speech
Index. It gives every "native" voice-to-voice AI model a single quality
score, built by averaging three separate test suites with equal weight.

The three ingredients are:

- **Speech Reasoning** (a test called Big Bench Audio) — can the model
  think clearly when everything arrives and leaves as spoken audio?
- **Conversational Dynamics** (a slice of Full Duplex Bench) — does it
  handle the flow of a real conversation: pauses, turn-taking,
  interruptions, and little "uh-huh" reactions?
- **Agentic Performance** (a test called τ-Voice) — can it actually get
  things done, like completing customer-service tasks for an airline,
  a shop, or a phone company?

A model only appears on the leaderboard if it has valid results on all
three tests, so every score is a complete three-sided comparison.

The first leaderboard puts OpenAI's GPT-Realtime-2 (High) on top at
77.2%, followed by xAI's Grok Voice Think Fast 1.0 at 75.7%,
GPT-Realtime-1.5 at 72.0%, and Google's Gemini 3.1 Flash Live Preview
(High) at 69.5%. The team says it will keep refining the tests and add
more models over time.

## Why does it matter?

If you are picking a voice model, one test alone can mislead you. A model
can be brilliant at answering quiz questions out loud but terrible at
letting you interrupt, or charming in chit-chat but useless at booking
a flight. Combining all three sides into one number makes comparisons
honest and practical.

The breakdown also reveals where the frontier really is. Straightforward
spoken reasoning is now tightly bunched at the top — most leading models
do it well. What separates the best from the rest is natural conversation
flow and the ability to carry out multi-step tasks by voice, and the
task-completion side is still very hard: every model scores below 53%
there. In other words, talking smart is largely solved, but talking
naturally *and* getting work done is not.

Finally, quality is only half the buying decision. The announcement pairs
each quality score with speed and price, so builders can see what the
extra points actually cost in waiting time and dollars.

## How does it work?

Imagine grading a student on three subjects and averaging the marks.

1. **Test reasoning by voice.** Big Bench Audio asks 1,000 spoken
   reasoning questions drawn from four puzzle types (spotting bad logic,
   navigating, counting objects, and untangling lies). Grok Voice Think
   Fast 1.0 leads here at 97.1%, with the top models clustered close
   behind.
2. **Test conversation manners.** The Full Duplex Bench slice checks
   pause handling, turn-taking, interruptions, and backchanneling —
   the small signals that say "I'm listening." GPT-Realtime-2 leads this
   dimension (its Minimal setting tops the slice at 96.1%).
3. **Test real errands.** τ-Voice plays out end-to-end customer-service
   calls across airline, retail, and telecom scenarios. Grok Voice Think
   Fast 1.0 leads at just 52.1%, ahead of GPT-Realtime-2 (High) at 39.8%,
   which shows how demanding this dimension is.
4. **Blend into one score.** Each of the three percentages counts for
   one-third of the final index. No model can hide a weak side: missing
   any of the three means no index score at all.
5. **Add speed and cost context.** Speed is measured as time to first
   audio (TTFA) — how fast you hear the first reply. Cost is quoted per
   hour of input audio. These sit alongside the quality score rather
   than inside it.

## Where can this be used?

- **Choosing a voice assistant engine.** A startup building a hands-free
  helper can shortlist models from one table instead of reconciling three
  separate benchmarks.
- **Designing phone agents.** Airline, retail, and telecom support lines
  map directly onto the τ-Voice scenarios, so the Agentic Performance
  column predicts which model is likeliest to finish a caller's request.
- **Tuning for responsiveness.** If every half-second of delay matters —
  for example in a live interpretation or drive-through ordering demo —
  the TTFA column flags fast options such as Deepslate Opal at 0.44s.
- **Budgeting voice features.** Teams watching operating costs can trade
  a few quality points for a much cheaper hourly rate, for instance by
  comparing the Gemini preview settings against the GPT-Realtime tier.
- **Tracking progress over time.** Because the index is versioned and the
  team plans to add models, it works as a repeated yardstick: re-run the
  same blend and see whether the field is catching up on hard tasks.

## Conclusions & takeaways

- One blended number now summarizes native voice-to-voice quality across
  reasoning, conversation flow, and task completion, with equal weight.
- GPT-Realtime-2 (High) leads overall at 77.2%, with Grok Voice Think
  Fast 1.0 close behind at 75.7%.
- Conversation flow and task completion decide the ranking; plain spoken
  reasoning is crowded at the top.
- Doing errands by voice (τ-Voice) is the hardest test by far — nobody
  passes 53%, so expect rapid work here.
- Speed and price cut against quality: the fastest model (Deepslate Opal,
  0.44s) and the cheapest (Gemini Minimal, $1.50/hour) both score in the
  low 60s and mid 50s, well below the leaders.
- Shoppers should pick from all three columns — score, speed, cost —
  not the headline score alone, and watch for new models as coverage
  grows.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Speech to Speech (S2S) | A model that listens to your voice and answers back in voice, with no typing step in the middle. |
| Native Speech to Speech | A model built to handle audio end to end, rather than stitching a separate listener, thinker, and speaker together. |
| Speech to Speech Index | The single blended quality score from this announcement — the average of three voice tests. |
| Big Bench Audio | A quiz of 1,000 spoken logic puzzles used to measure clear thinking by voice. |
| Full Duplex Bench | A test of conversation flow: pauses, taking turns, handling interruptions, and listener feedback. |
| τ-Voice (tau-Voice) | A test of getting errands done by voice, such as solving airline, retail, or telecom requests. |
| Conversational Dynamics | How naturally a model chats: timing, turn-taking, and reacting while you speak. |
| Agentic Performance | How well a model completes multi-step tasks for you, not just answers questions. |
| Time to first audio (TTFA) | How many seconds you wait before hearing the start of the model's spoken reply. |
| Equal weighting | Each of the three tests counts for one-third of the final score — none dominates. |
