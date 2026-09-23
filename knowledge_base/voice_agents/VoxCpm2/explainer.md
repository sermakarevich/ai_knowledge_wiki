> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# OpenBMB/VoxCPM — In Plain Language

## What is this about?
VoxCPM2 is a computer program that turns written text into spoken audio —
in other words, a text-to-speech (TTS) voice generator.

Think of it like a highly skilled voice actor living inside your computer:
you hand it a script, and it reads the script out loud in a natural-sounding
human voice. It can speak 30 languages (plus several Chinese dialects),
and it produces studio-quality sound at 48kHz, which is the same quality
standard used for professional audio.

The project is open source under the Apache-2.0 license, so anyone can use
it, modify it, and even use it in commercial products for free. You can try
it through a simple point-and-click web page (a Gradio demo), a Python
programming interface, or a command-line tool.

## Why does it matter?
Most voice generators sound robotic, speak only one or two languages, or
require you to tag the language by hand ("this text is French"). VoxCPM2
removes those annoyances: it figures out the language on its own, reads with
natural rhythm and emotion picked up from the meaning of the text, and
outputs high-quality audio directly.

Three things make it stand out for everyday users:

1. **No recording needed.** You can invent a brand-new voice just by
   describing it in words ("a warm young woman's voice, gentle, with a
   slight smile") — no microphone required.
2. **Clone a voice from seconds of audio.** Give it a short clip of someone
   speaking, and it can read new text in that same voice.
3. **Cheap to run, ready to ship.** It streams speech in real time on a
   single gaming-grade GPU, and a faster server setup exists for production
   use — so it works for both hobby projects and real products.

Because it is free for commercial use and speaks 30 languages out of the box,
it lowers the cost of audiobooks, video dubbing, game voices, and voice
assistants dramatically.

## How does it work?
In plain terms, the process has four steps:

1. **You give it text (and optionally a voice sample).** There are three
   ways to use it. *Voice Design* takes only a voice description plus the
   text to read. *Controllable Cloning* takes a short voice clip plus the
   text, with an optional style note. *Ultimate Cloning* takes a voice clip
   *and* a written transcript of that clip, which anchors the new speech
   most precisely.
2. **A large neural network plans the speech.** A 2-billion-parameter model
   (built on a MiniCPM-4 language-model backbone, trained on over 2 million
   hours of speech) reads your text and decides how it should sound — pacing,
   emphasis, emotion — then sketches the sound directly as smooth,
   continuous audio patterns rather than chopping speech into rigid tokens.
3. **A sound builder turns the sketch into audio.** A component called
   AudioVAE V2 converts those patterns into an actual sound wave. It only
   needs a modest-quality 16kHz reference clip but produces a crisp 48kHz
   result, sharpening the sound itself with no separate upscaler needed.
4. **You get audio back, live if you want.** A Python call, a `voxcpm`
   command (`design`, `clone`, `batch`), or the web demo returns a `.wav`
   file. A streaming mode speaks long texts chunk by chunk, and a fast
   server mode (Nano-vLLM / vLLM-Omni) serves many users at once through a
   standard audio API.

Two small helpers clean up the result: text normalization (expanding "Dr."
into "doctor") and denoising (removing background hiss from your reference
clip). A speech-recognition helper can also transcribe a reference clip
automatically so you don't have to type it out.

## Where can this be used?
- **Audiobooks and podcasts:** narrate a whole book in 30 languages from one
  script, or invent a distinct narrator voice from a text description.
- **Video dubbing and localization:** re-speak the same video script in
  another language while keeping the original speaker's voice character.
- **Games and animated characters:** designers can audition voices by typing
  descriptions instead of hiring actors for every draft.
- **Voice assistants and accessibility:** apps that read articles, messages,
  or screen content aloud for visually impaired users or hands-free use.
- **Personal projects and fine-tuning:** hobbyists can adapt the model to a
  specific voice with the LoRA training web page, then swap voice packs in
  and out without reinstalling the model.

## Conclusions & takeaways
- VoxCPM2 is a free, commercial-friendly voice generator that reads text
  aloud naturally in 30 languages with no manual language settings.
- Its headline trick is flexibility: invent a voice from words alone, clone
  one from seconds of audio, or lock in maximum fidelity with audio plus a
  transcript.
- Under the hood, a big multilingual model sketches speech directly as
  smooth sound patterns, and a built-in audio builder delivers crisp 48kHz
  output from modest inputs.
- For builders, it is practical: install with `pip install voxcpm`, try the
  web demo, script it in Python, or serve it fast with a vLLM-compatible
  server — all on a single GPU.
- Bottom line: if you need believable machine speech in many languages
  without recording studios or licensing fees, this is one of the most
  complete open options available.

## Jargon decoder
| Term | What it really means |
|---|---|
| Text-to-speech (TTS) | Software that reads written text out loud as spoken audio. |
| Tokenizer-free / continuous representations | Instead of chopping speech into fixed puzzle pieces first, the model draws the sound as one smooth curve — which tends to sound more natural. |
| Diffusion autoregressive architecture | A technique that builds the sound step by step, refining noise into clear speech, each step guided by the previous ones. |
| Voice Design | Making up a brand-new voice purely from a written description, with no audio sample. |
| Controllable / Ultimate Cloning | Copying a real voice: "controllable" needs only a short clip; "ultimate" also needs the clip's transcript for the closest match. |
| AudioVAE V2 / super-resolution | The part that converts the model's sketch into a real sound wave, sharpening modest input into crisp 48kHz output by itself. |
| CFG value / inference timesteps | Two quality dials: how strongly the model follows your instructions, and how many refinement passes it makes (more passes = better but slower). |
| LoRA fine-tuning | A lightweight way to teach the model a specific new voice without retraining the whole giant model. |
| Gradio demo | A simple web page with text boxes and buttons for trying the model without writing code. |
| RTF (real-time factor) | A speed score: below 1.0 means it generates speech faster than a human could speak it. |
