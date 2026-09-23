> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# OpenMOSS/MOSS-TTSD — In Plain Language

## What is this about?

MOSS-TTSD is an open-source tool that turns a written dialogue script
into a full spoken conversation, not just one voice reading lines aloud.

Think of it as a small radio-drama studio in software: you hand it a script
with one to five speakers, plus a short voice sample for each person,
and it performs the whole exchange as audio.

The headline features are long sessions (up to about 60 minutes of coherent
audio in one run), flexible casting (1–5 speakers with distinct personas),
and wide language coverage (20 languages including Chinese, English,
Japanese, and European languages).

Under the hood it is Python 3.10+ / PyTorch 2.0+ code, released under
Apache 2.0, installed via conda plus `requirements.txt` and `flash-attn`.

## Why does it matter?

Most speech tools are good at one voice reading one passage well.
Real content is messier: it needs several voices interacting over time.

MOSS-TTSD targets exactly that gap. Its shift is from "text-to-speech"
to "script-to-conversation": the goal is the flow of a multi-party
exchange — turn-taking, overlapping speech patterns, emotional nuance —
rather than isolated single-speaker fidelity.

That matters because the most useful formats are conversational:
talk shows, podcasts, commentary, audiobooks, dubbing, and comedy acts
all depend on who speaks when, and staying in character.

Its zero-shot cloning also lowers the bar to start: a short reference
recording per speaker is enough, instead of hours of studio data per voice.

## How does it work?

The core idea is simple: the model reads the whole tagged script and
generates the conversation as a continuous performance.

In plain terms, the workflow has three steps:

1. Give a voice sample. For each speaker (S1 through S5), you supply
   a short audio clip plus a transcript of what that clip says.
   This teaches the model "this is what S1 sounds like."
2. Write the dialogue. You write the script with speaker tags such as
   `[S1] Hello everyone. [S2] Glad to be here.` The tags say who speaks
   each line and when turns change.
3. Generate the audio. The model continues in each speaker's identity
   and a companion audio tokenizer decodes its output codes back into
   playable sound files, written per segment as wav files.

Two practical paths ship with the project: a batch script (`inference.py`)
that reads many dialogues from a JSONL file and spreads the work across
all visible GPUs, and an interactive Gradio demo for 1–5 speakers with
preset reference voices.

Shared helpers (`generation_utils.py`) handle the chores: cleaning up
dialogue text, reading sharded JSONL lines, resolving sampling settings,
and encoding the per-speaker prompt audios.

Practical defaults from the docs: use the `continuation` family of modes
for cloning, with sampling falling back to roughly 8192 max tokens,
temperature 1.1, top_p 0.9, top_k 50, and repetition penalty 1.1.
There is also a fused-model server path with SGLang for faster serving.

## Where can this be used?

- AI podcasts: turn an article or long text into a multi-host discussion
  rather than a single narrator reading.
- Sports and esports commentary: generate energetic back-and-forth
  commentary tracks for highlights or replays.
- Audiobooks and radio drama: give each character a stable, distinct
  voice sustained across long chapters.
- Dubbing and localization: keep the same cloned voices while switching
  languages for a scene or episode.
- Comedy and crosstalk acts: prototype timing-sensitive two-person
  routines with persona control and turn-taking.
- Creator prototyping: experiment with multi-speaker dialogue and
  long-context speech generation in the open.

## Conclusions & takeaways

The main takeaway is a shift in framing: from reading text aloud to
staging a conversation, with casting, timing, and personality included.

Its strengths are multi-speaker control (1–5 voices), long sessions
(up to 60 minutes with consistent identity), and portable voices
(short-sample cloning across 20 languages).

Its shape is practical: a simple script-plus-samples input, a batch path
for offline jobs, shared text/audio helpers, and an interactive demo
plus a fused server path for faster output.

If you remember one sentence: write a tagged script, attach a short voice
sample per speaker, and MOSS-TTSD performs the conversation.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Script-to-conversation | Generating a whole multi-speaker dialogue, not one voice reading lines. |
| Zero-shot voice cloning | Copying a voice from a short sample with no extra training step. |
| Speaker tags ([S1]–[S5]) | Labels in the script marking which of up to five speakers says each line. |
| Turn-taking | How speakers alternate, interrupt, or overlap naturally in conversation. |
| Persona maintenance | Keeping each speaker's voice and style consistent over a long session. |
| Long-context modeling | Handling very long inputs and outputs (here, up to ~60 minutes) in one run. |
| Audio tokenizer / codec | The part that converts between sound waves and compact codes the model uses. |
| Continuation mode | Generation style that continues from the given voice samples and prefix text. |
| JSONL input | A text file with one dialogue description per line for batch jobs. |
| Text normalization | Cleaning up punctuation and dialogue tags before generation. |
