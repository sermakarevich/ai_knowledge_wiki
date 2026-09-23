> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# remsky/Kokoro-FastAPI — In Plain Language

## What is this about?

Imagine you have written text — a story, an article, a script — and you want
a computer to read it out loud in a natural-sounding voice. That is what this
project does. It takes a compact speech model called Kokoro-82M and wraps it
in a ready-to-run web service, so any program can send text and get back audio.

You do not need to be a speech researcher to use it. You start one program
(a "container" or a direct launch script), and it opens a small website and
an address other software can call. Send a sentence, get back an MP3 or WAV
file. It can even read for hours of audio in minutes.

Out of the box it speaks several languages: English (American and British),
Spanish, French, Hindi, Italian, Japanese, Brazilian Portuguese, and Mandarin
Chinese. It also ships with a simple web page where you can paste long text,
press play, and follow along as it reads.

## Why does it matter?

Good computer voices used to be locked inside big paid services. You sent
your text to someone else's cloud, paid per character, and waited. This
project flips that: you run the voice engine on your own machine or server,
with no per-request bill and no data leaving your computer.

Three things make that practical. First, the underlying model is small (82
million parameters — tiny by today's standards), so it runs on an ordinary
laptop CPU or much faster on a graphics card. Second, it copies the way
popular paid services receive requests, so existing tools and code written
for those services work with almost no changes. Third, everything is
packaged with one-command startup, so setup is minutes rather than days.

The result is private, cheap, offline-capable narration: audiobooks,
video voiceovers, accessibility readers, and voice features inside apps,
without depending on an outside provider.

## How does it work?

Think of it as a kitchen with a standard ordering counter.

1. **You place an order.** Your program sends text plus choices — which
   voice, which language, how fast, which audio format — to a standard
   address on your machine (port 8880). It uses the same order format as a
   well-known commercial speech service, so most existing code just works.

2. **The kitchen prepares the text.** The service cleans up the text, turns
   words into pronunciation units (sounds, not letters), and picks the
   requested voice. You can use one voice, blend two voices together (for
   example, part one speaker and part another), or assign different voices
   to different parts for dialogue.

3. **The model speaks.** The Kokoro model converts those sound units into
   raw audio waves. A graphics card does this fastest (first sound in about
   a third of a second); a regular processor takes longer but still works.

4. **Audio is packed and streamed.** The raw sound is encoded into your
   chosen format — MP3, WAV, and others — and sent back. For long texts it
   streams: you start hearing the beginning while the rest is still being
   made, like watching a video while it buffers.

5. **Extras ride along.** Optionally you get captions timed to each word or
   chunk (for subtitles or read-along highlighting), fine control over
   pronunciation and pauses, and a web page for listening and testing.

Behind the scenes there are three ways to start it (a ready-made container,
a build-it-yourself container setup, or a direct launch), plus separate
ready-made versions for plain CPUs, NVIDIA graphics cards, experimental AMD
cards, and Apple Silicon — but they all end up serving the same address.

## Where can this be used?

- **Audiobooks and podcasts:** turn a manuscript or blog archive into
  listenable audio, including long sessions the web page can read aloud.
- **Video and course narration:** generate voiceovers in several languages
  from one script, with subtitles produced from the timed captions.
- **Dialogue and stories:** give different characters different voices, or
  blend voices to invent a new one for a narrator.
- **Accessibility:** read articles, documents, or app screens aloud for
  people who prefer listening, fully offline for privacy.
- **Apps and prototypes:** add a "read this to me" button or a voice for a
  chatbot using the standard request format, without signing up for a
  speech vendor.
- **Language learning and pronunciation study:** hear the same sentence in
  different languages or voices, and inspect the sound-unit output.
- **Local and private deployments:** run narration inside a company or
  school network where text must not be sent to outside services.

## Conclusions & takeaways

- This is speech synthesis made ordinary: type text in, get natural audio
  out, on hardware you already have.
- Copying a popular request format was a smart shortcut — it makes adoption
  nearly free for anyone already using that style of speech service.
- Small models plus careful packaging beat giant models for everyday jobs:
  fast enough, cheap enough, and private enough to run yourself.
- Voice blending, multi-speaker text, timed captions, and pronunciation
  controls are the features that lift it above a bare demo.
- The main trade-off is the usual one: a graphics card gives smooth live
  playback, while a plain processor is slower to start each request.
- If you remember one thing: it is a self-hosted, multi-language
  text-to-speech server that behaves like the commercial service your code
  may already know.

## Jargon decoder

| Term | What it really means |
|---|---|
| Text-to-speech (TTS) | Technology that turns written text into spoken audio. |
| Model | A trained recipe file the computer follows to convert text into voice; here a small, fast one. |
| API | A standard address where programs send requests and get answers, without a human clicking anything. |
| OpenAI-compatible endpoint | A request format copied from a popular speech service, so existing code works unchanged. |
| Container / Docker image | A sealed box with the program and everything it needs, so it runs the same anywhere. |
| GPU / CUDA / ROCm / MPS | Graphics-card helpers (NVIDIA, AMD, Apple) that do the math much faster than a plain processor. |
| Streaming | Hearing the start of the audio while the rest is still being generated. |
| Voice mixing / blending | Combining two voices in chosen proportions to create a new sound. |
| SSML | Simple markup tags inside text that control pauses, emphasis, or pronunciation. |
| Phonemes | The individual sound units of speech (sounds, not spelling) used to guide pronunciation. |
| Captions / timestamps | Notes saying which word is spoken at which moment, used for subtitles or highlighting. |
| Chunk size | How much text is processed at once; bigger chunks can sound smoother but start slower. |
