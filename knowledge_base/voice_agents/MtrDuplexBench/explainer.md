> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# ZhangHe0918/MTR-DuplexBench — In Plain Language

## What is this about?

MTR-DuplexBench is a test suite for a new kind of voice AI:
full-duplex speech models that can listen and talk at the same time.

Most voice assistants today work like walkie-talkies. You speak,
then wait, then the assistant answers. A full-duplex model works
more like a phone call. Both sides can speak, interrupt, pause,
or make background noise, all in real time.

This benchmark checks how well those models handle realistic,
multi-round spoken conversations — not just one clean question
and one clean answer, but back-and-forth dialogue with messy
timing, interruptions, and overlapping speech.

It was accepted by ACL 2026 Findings and ships as a package:
a paper, a dataset on HuggingFace, and a set of scoring scripts.

Think of it as a driving test for talking machines. The test
course is a set of scripted conversation scenarios. The car is
your model. The examiners are automatic scoring programs.

## Why does it matter?

Talking to a machine still feels awkward compared to talking
to a person. A big reason is turn-taking: knowing when to speak,
when to wait, when to jump in, and when to stay quiet.

If a voice assistant cuts you off, answers too slowly, ignores
a "stop" instruction, or says something unsafe, people stop
trusting it. These failures are hard to catch with text-only
tests because they only show up in real spoken interaction.

This project matters because it gives researchers a shared,
repeatable way to measure exactly those skills:

- Can the model hold a natural multi-round conversation?
- Does it handle interruptions, pauses, and background noise gracefully?
- Does it actually follow spoken instructions?
- Does it refuse harmful requests safely?

Without a common yardstick, every team reports its own numbers
and nobody can compare results. A shared benchmark makes
progress visible and honest.

## How does it work?

The workflow has three steps, like a recipe: prepare the script,
record the performance, then grade it.

**Step 1: Read the script.**

Each test starts from a scenario encoding — a JSON file that
describes the shape of a conversation. It says who speaks when,
where interruptions or pauses happen, and how rounds are timed.
There are different scripts for each skill being tested, such as
smooth turn-taking, pause handling, background noise, instruction
following, safety, and overall dialogue quality.

**Step 2: Run your model and record stereo audio.**

You play the user-side audio into your model and record what
comes out. The result must be a stereo sound file with a fixed
rule: the left channel holds the user's voice and the right
channel holds the model's voice. Keeping the two sides on
separate channels lets the graders tell who said what, even
when both talk at once.

**Step 3: Transcribe and score automatically.**

Scoring scripts take over from there. First, a shared helper
program uses Whisper, an automatic speech-to-text tool, to turn
both audio channels into written transcripts. Results are saved
step by step, so a crash does not lose everything, and repeated
runs reuse cached transcripts.

Then each skill gets its own grader:

- Dialogue Quality: GPT-4o reads the transcript and rates each
  model turn from 0 to 5 on whether it makes sense.
- Conversational Features: programs measure timing facts such
  as response delay, how often the model chimes in, and whether
  interruptions and pauses were handled correctly.
- Instruction Following: GPT-4o gives a yes-or-no score on
  whether the model obeyed the user's instruction.
- Safety: GPT-4o gives a safe-or-unsafe verdict on answers to
  risky requests.

Finally, per-turn and per-round scores are averaged into overall
rates, so models can be compared on multi-round conversations.

## Where can this be used?

Anyone building or studying real-time voice AI can use it:

- Voice-assistant teams testing whether a new model interrupts
  less and responds faster than the old one.
- Researchers comparing published speech models on equal terms
  instead of cherry-picked demos.
- Safety teams probing whether a talkative model can be tricked
  by spoken jailbreaks or harmful requests.
- Product teams checking instruction-following, such as "speak
  more slowly" or "stop and let me finish," in actual audio.
- Students learning how speech evaluation works, from audio
  recording to transcription to automatic judging.

The setup also generalizes. The same pattern — scripted scenario,
stereo recording, transcribe, then score — could be reused for
call centers, language tutoring, or accessibility tools where
natural turn-taking and safety both matter.

## Conclusions & takeaways

The core idea is simple: if you want human-like voice AI, test
it the way humans talk — with overlap, noise, and many rounds.

Three things to remember:

1. Realism comes from the scenario scripts plus stereo audio.
   Separating user and model voices makes messy, overlapping
   speech measurable instead of just confusing.
2. Grading mixes machine listening with machine judging.
   Whisper turns sound into words; GPT-4o or timing programs
   turn words and timestamps into scores.
3. Four skills, one pipeline. Dialogue quality, conversational
   timing, instruction following, and safety are scored
   separately but run through the same record-and-grade flow.

In short: write the conversation script, record both sides of
the call, then let the scripts do the grading.

## Jargon decoder

| Term | What it really means |
| :--- | :--- |
| Full-duplex | Listening and speaking at the same time, like a phone call rather than a walkie-talkie. |
| Turn-taking | The back-and-forth rhythm of conversation: knowing when to speak and when to wait. |
| Scenario encoding | A JSON script that defines who speaks when, including interruptions, pauses, and timing. |
| Stereo audio (left/right channels) | One sound file with two tracks: user voice on the left, model voice on the right. |
| ASR (automatic speech recognition) | Software, here Whisper, that turns spoken audio into written text. |
| LLM judge (GPT-4o) | Using a powerful language model as an automatic grader for dialogue quality, instructions, or safety. |
| Latency | How long the model waits before responding; lower usually feels more natural. |
| Backchannel | Short listener sounds like "uh-huh" or "yeah" that signal attention without taking over. |
| Instruction following rate | The share of tasks where the model actually did what the user asked. |
| Safety evaluation | Checking whether the model refuses or safely handles harmful spoken requests. |
