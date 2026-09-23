> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# MIRA: Real-Time Full-Duplex Human-Robot Interaction for Embodied Companions — In Plain Language

Imagine a robot companion that talks the way a friend does: it speaks,
gestures while it speaks, notices when you cut in, stops mid-sentence,
and picks up the thread again — without freezing or swinging an arm
through its own body. MIRA is a complete system that lets a humanoid
robot hold such a natural, interruptible spoken conversation while
moving safely in real time.

## What is this about?

Most talking robots work in two disconnected steps. One part decides
what to say; a separate part figures out how to move, often only after
the full sentence of audio is ready — so words and gestures fall out
of sync, and the robot cannot be interrupted gracefully mid-motion.
MIRA ties those jobs into one continuous loop on an Astribot S1
humanoid. Every reply decides two things at once: the words to speak,
and a small label saying how the body should express them (speak with
gestures, wave hello, listen attentively, apologize, or stay idle).
Fixed social moments play a pre-checked movement from a library; open
talking generates fresh gestures live from unfolding speech, following
its rhythm, pauses, and emphasis.

## Why does it matter?

Human conversation is full-duplex: both sides can overlap and interrupt
at any moment. A call where you must say "over" before the other person
replies feels stiff — yet many robots still behave that way. With a
physical robot the problem is harder than with a voice assistant. Words
on a screen can be deleted; a moving arm cannot. A late gesture or a
wrongly cancelled reply stays visible and feels awkward or unsafe. The
paper calls this the physical commitment problem: motion sent to the
motors cannot be taken back as easily as text. MIRA treats stopping
safely as a first-class skill. The robot starts speaking and gesturing
early (before the whole sentence exists), keeps motion smooth across
short chunks, and halts speech and movement within about half a second
on barge-in — while remembering the conversation so it can continue or
replace its answer. Concretely: 0.5 s of motion is generated in about
0.195 s (faster than real time), interruption takes ~0.466 s, and the
motion matches real gesture patterns with fewer self-collisions than
the reference data.

## How does it work?

Three pieces work as a team.
**1. CORTEX — the conversation manager.** It listens to streaming
speech (words plus tone), chat history, and whether the robot is
speaking, on two timescales. A fast gate stops speech and motion when
you keep talking for ~450 ms during robot speech — no understanding
needed first, stopping is urgent. A slower arbiter then decides what
you meant: simple rules first ("um" is filler; "stop" is a command),
then a language model for hard cases. Verdict: IGNORE (not for me),
REPLY (answer it), or INTERRUPT_AND_REPLY (replace the old answer).
A generator writes the reply, picks the body label, can call tools
(e.g. weather lookup), and streams text to speech so talking starts early.
**2. The embodiment cue — a routing slip for the body.** A sticky note
like `<motion: speak>` plus the sentence; peeled off before the voice
speaks, so you never hear it. It routes the body: stored movements for
greet, listen, confused, apologize, idle — or the live gesture engine
for `speak`. Missing notes fall back to `speak` (real sentences) or
`idle` (empty ones). Tone is used cautiously: frustration alone never
drives the arm; it joins words, intent, and history to pick a cue.
**3. ROSCO + RHPC + safety bridge — the movement engine.** ROSCO, a
diffusion model, turns streaming audio plus recent motion into the next
motion, listening only to present and past audio so gestures stay live.
RHPC sketches wide but commits narrow: predict 50 frames each step, hand
over only the first 15 (~0.5 s), reusing the last 10 as overlap — smooth
yet cheap to cancel. Every frame then passes a simulator check (joint
limits, collisions) and a 250 Hz control loop; on interruption the
movement session ends while conversation memory is kept.

## Where can this be used?

- Home and elder-care companions that chat, explain, and yield politely
  when interrupted mid-sentence.
- Receptionist, museum-guide, and retail robots that greet, listen,
  apologize on misunderstanding, and gesture while presenting.
- Tutoring and storytelling robots where speech-timed gestures aid focus.
- Assistive robots in clinics or care homes where a calm, safe stop —
  holding a safe pose instead of freezing mid-gesture — matters.
- Multi-person settings (living room, classroom, demo booth) where the
  robot must separate speech addressed to it from side chatter, pause,
  and resume without losing the thread.

## Conclusions & takeaways

- Robot chat is a body problem as much as a language problem: when to
  speak, how to move, and how to stop belong in one loop, not stages.
- Splitting fixed moves (library) from free talking (live generation)
  gives safety plus expressiveness: predictable where it counts, fluid
  where it matters.
- Fast stop plus slow thought is the key trade: halt the body in
  milliseconds on sound alone, then decide what the interruption meant.
- Smoothness is a system property, not just a smarter network:
  overlapping chunks, short cancellable commits, and robot-side checks
  matter as much as the gesture model.
- Limits remain: small gesture vocabulary, per-robot safety retuning,
  ~2 s startup (mostly speech recognition plus language model), and no
  long-term studies of living with such a companion yet.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Full-duplex | Both sides can speak and listen at once, including interrupting. |
| Embodiment cue | Short label (e.g. `speak`, `greet`, `listen`) for how the body acts out a reply. |
| CORTEX | Conversation manager: decides answer / interrupt / ignore, writes replies. |
| ROSCO | Gesture generator: turns streaming speech audio into body motion. |
| RHPC | "Sketch a lot, commit a little": predict 50 frames, hand over only 15. |
| Barge-in | User talking over the robot; it must stop and respond sensibly. |
| VAD gate | Sound detector triggering a quick stop on sustained human speech. |
| Diffusion model | Generator that sculpts noise step by step into realistic motion. |
| FID-G | Score for resemblance to real human movement (lower is better). |
| Self-collision rate | How often a planned pose would make body parts intersect. |
