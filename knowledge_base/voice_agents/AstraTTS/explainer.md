> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# AstraTTS — In Plain Language

## What is this about?

AstraTTS is a free, open-source program that turns written text into spoken
audio — a text-to-speech (TTS) engine you can run on your own computer.

Think of it like a personal voice reader: you type (or send) a sentence, and
it speaks the sentence out loud in a chosen voice. It runs as a small local
service — by default at `http://localhost:5000` — with a point-and-click
web page for managing voices and models, plus a command-line tool for quick
one-off playback.

Two things define the project. First, it is built for speed on ordinary
CPUs: it uses ONNX Runtime with deep CPU optimization instead of slow
plain-Python inference, so it can start speaking within milliseconds and
keep generating audio while it plays. Second, it is built for real use
across machines: native apps for Windows 10/11, Linux, and macOS (Apple
Silicon and Intel), plus a Docker image for servers, with settings that
reload live without restarting.

It ships with two engines. V1 is the stable default and the recommended
choice; V2 is experimental and still being developed.

## Why does it matter?

Most capable voice-cloning and speech tools are either cloud services (you
upload text or audio to someone else's server) or slow Python research
demos that need a powerful graphics card.

AstraTTS matters because it removes both barriers:

- **Private and local.** Everything runs on your machine or your server.
  No audio or text has to leave your network.
- **Fast without a GPU.** CPU instruction-set tuning plus a pool of
  inference workers lets one machine serve several simultaneous requests
  using its multiple CPU cores.
- **Feels instant.** Millisecond-level first-packet streaming means
  playback starts almost immediately instead of waiting for the whole
  sentence to finish rendering.
- **Usable by non-experts.** Voice libraries, model conversion, and tuning
  knobs live in a web UI with light and dark themes — not just config
  files and scripts.
- **Bilingual out of the box.** It handles Chinese/English and
  Chinese/Japanese mixed text, which is hard for simpler engines that
  assume one language per sentence.

## How does it work?

In plain terms, the pipeline has four stages:

1. **You ask for speech.** Either through the web page, an app call to the
   local server, or the command-line tool (for example, asking it to say
   a short test phrase). You pick a voice ("avatar") and optionally a
   speed.
2. **The text is analyzed.** A front-end figures out pronunciation for each
   language in the text (a "hybrid G2P engine" with dictionaries and
   models), while helper models read context and vocal character — roughly
   "how should this sound?" This is where the RoBERTa/BERT-style text
   features and HuBERT-style voice features come in.
3. **The voice model generates audio.** The V1 or V2 neural network turns
   those features into sound waves, running inside ONNX Runtime. An
   "inference pool" keeps several workers ready, so multiple requests can
   synthesize at the same time instead of queuing up.
4. **Audio streams back.** In streaming mode, the first chunk of sound is
   sent within milliseconds and playback begins while the rest is still
   being generated. On Windows this uses low-latency WASAPI playback; on
   Linux it falls back through `pw-play` to `paplay` to `aplay`; on macOS
   streaming playback uses `ffplay` (from ffmpeg).

Under the hood the project is split into three parts: a core library with
the pronunciation and inference engines, a command-line tool, and the web
server with the management UI. All settings live in one YAML file
(`config.yaml`) — threads, engine choice, speed, streaming on/off, and the
voice list — and most changes apply instantly with no restart.

The engine choice is the main fork in the road. V1 (derived from
Genie-TTS) is deterministic: same input, same output, no randomness
knobs. V2 (derived from GPT-SoVITS-Minimal) supports randomness-style
sampling controls (TopK, temperature, noise scale) for more varied output,
but it is unfinished, Chinese/English only, and not enabled on macOS.

## Where can this be used?

- **Personal narration.** Reading articles, documents, or chat replies aloud
  on a Windows, Linux, or Mac laptop with no cloud account.
- **Voice libraries and cloning experiments.** Uploading a short reference
  recording, registering it as a named voice, and converting or cloning
  SoVITS-family models (including V2ProPlus models via the V1 engine).
- **Small servers and home labs.** Running the Docker image on a Linux box
  and sharing speech synthesis over the local network to other devices.
- **Apps and bots that need speech.** Any program that can call a local web
  service can request audio — announcements, notifications, game dialogue,
  accessibility readers, or prototyping a voice assistant.
- **Bilingual content.** Videos, language-learning material, or mixed
  Chinese/English and Chinese/Japanese scripts that single-language tools
  mispronounce. (Three-language mixing in one sentence is still in
  development.)

Practical notes from the digest: setup downloads a `resources-minimal`
pack from GitHub Releases (no longer via Git LFS); building from source
needs the .NET 10.0 SDK; and LAN sharing is a one-flag change to listen
on all interfaces instead of just localhost.

## Conclusions & takeaways

- AstraTTS is best understood as a **productized local TTS server**: fast
  CPU inference, streaming playback, and a management UI, not just a model.
- **Default to the V1 engine.** It is stable, supports bilingual mixing
  and model cloning, and is the only engine on macOS. Treat V2 as an
  experiment unless you specifically need its sampling knobs.
- The headline engineering ideas are the **ONNX Runtime CPU path**, the
  **inference pool for concurrency**, and **millisecond streaming with
  hot-reload config** — together they make local speech feel interactive.
- The cost of that footprint is operational: manual resource-pack
  downloads, per-OS audio backends, and a .NET build toolchain.
- If you need private, low-latency, multi-user speech on commodity
  hardware with bilingual text, this is a strong fit; if you need
  three-language mixing or a finished V2 engine, it is not there yet.

## Jargon decoder

| Term | What it means in plain language |
| :--- | :--- |
| TTS (text-to-speech) | Technology that reads written text out loud as audio. |
| ONNX Runtime | A fast, cross-platform runner for trained AI models; here it replaces slow Python inference. |
| Inference | The act of running a trained model to produce a result — here, generating speech. |
| Inference pool | A set of ready-to-work model copies that handle several requests at once. |
| Streaming output / first-packet latency | Sending the first bit of audio immediately so playback starts while the rest renders. |
| Hot reload | Settings take effect without stopping and restarting the program. |
| Avatar / voice library | A named voice built from a reference recording, selectable at synthesis time. |
| G2P (grapheme-to-phoneme) | The step that converts written words into pronunciation sounds. |
| Deterministic generation | Same input always gives the same output; no randomness knobs. |
| TopK / temperature / NoiseScale | Randomness controls in V2 that vary how expressive or unpredictable the voice sounds. |
| WebUI | The browser-based control panel for voices, models, and settings. |
| Docker image | A pre-packed container that runs the server identically on any machine with Docker. |
