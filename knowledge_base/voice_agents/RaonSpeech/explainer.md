> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# krafton-ai/Raon-Speech — In Plain Language

Think of Raon-Speech as a voice assistant brain that can listen, talk,
answer questions, and hold a phone-like conversation — in both English
and Korean.

## What is this about?

Raon-Speech is a family of open speech-and-language models (9 billion
parameters) released by KRAFTON AI with checkpoints, code, demos, and
benchmarks.

It has two tracks that share one core model and processor stack:

- **Offline track (Raon-Speech):** four jobs — turn text into speech
  (TTS), turn speech into text (STT), chat about spoken input
  (SpeechChat), and answer questions grounded in audio (TextQA).
- **Real-time track (Raon-SpeechChat):** a full-duplex conversationalist
  that listens and talks at the same time, like a phone call, instead of
  waiting politely for its turn.

The base model was trained on over 1 million hours of curated
speech-plus-text data and tested on 42 speech and text benchmarks. The
chatty real-time version got extra training on 116 thousand hours of
time-aligned dialogue.

Everything ships Hub-native: you can load `KRAFTON/Raon-Speech-9B` or
`KRAFTON/Raon-SpeechChat-9B` from Hugging Face, run scripts or a simple
`RaonPipeline` API, and try an interactive demo.

## Why does it matter?

Most voice systems are stitched together from separate parts: one model
transcribes, another answers, a third speaks. That works, but it is slow,
fragile, and bad at natural conversation.

Raon-Speech matters because it puts all of that into one shared model:

- One model handles listening, understanding, answering, and speaking,
  so there are fewer moving pieces to break.
- It is bilingual (English and Korean) from the ground up, with new
  Korean benchmarks (KVoiceBench, KOpenAudioBench, KMMAU) to prove it.
- The full-duplex track tackles the hard human parts of conversation:
  pauses, interruptions, talking over each other, and knowing when to
  respond versus just say "uh-huh."
- It is openly released — checkpoints, training and inference code,
  and demos — so others can reproduce, test, and build on it.

In short: fewer Frankenstein pipelines, more natural voice interaction.

## How does it work?

Picture one shared backbone with two personalities.

At the center is a single model design, `RaonModel`: a large language
model plus an audio encoder plus a sound-codec path (the Mimi codec).
Two flavors exist — `raon` for the offline jobs and `raon_duplex` for
real-time conversation — with small trainable connector blocks that glue
sound and text together.

For everyday jobs you describe each example as a chat-style JSON record
with a `channel` label (`tts`, `stt`, `speech-chat`, `textqa`), a list of
conversation turns, and pointers to audio files. Then you run it either
with a shell script or a few lines of Python:

- `pipe.stt("meeting.wav")` writes down what was said.
- `pipe.tts("Hello!", speaker_audio="voice.wav")` speaks in a cloned voice.
- `pipe.speech_chat("question.wav")` answers a spoken question.
- `pipe.textqa("What did the speaker say?", audio="clip.wav")` answers
  with audio as context.

For live conversation, the duplex version adds four tricks:

1. **Causal streaming** — it processes sound as it arrives instead of
   waiting for the whole sentence.
2. **Interleaved speech-text modeling** — it reads and writes words and
   sound tokens side by side, so talking and listening stay in sync.
3. **Interaction-state modeling** — it explicitly tracks "who is talking,
   who should talk next, was that an interruption?"
4. **Text lookahead** — it drafts what to say slightly ahead of speaking,
   so speech stays fluent under time pressure.

It also runs fast: streaming speech generation is reported at 2–4x faster
than real time on a single GPU, with under a second to the first sound.

## Where can this be used?

- **Voice assistants and smart speakers** that take orders, answer
  questions, and speak back naturally in English or Korean.
- **Live call agents** — customer support, game NPCs, tutoring bots —
  where interruptions and quick turn-taking matter.
- **Transcription and dubbing tools** — meeting notes, subtitles, and
  voice cloning from a short speaker sample.
- **Spoken question-answering** — ask about a lecture, podcast, or
  recording and get an answer grounded in the audio.
- **Research and evaluation** — the open checkpoints plus Korean speech
  benchmarks give teams something concrete to compare against.

You need Python 3.11+, a CUDA GPU for comfortable use, and either the
installed `raon` package (full scripts and real-time runtime) or just the
Hugging Face remote-code path (demos and basic use only).

## Conclusions & takeaways

- Raon-Speech is one bilingual voice-brain with two modes: careful
  offline work and lively real-time chat.
- Sharing one backbone across TTS, STT, chat, and QA is simpler and more
  consistent than chaining four separate models.
- The real novelty is the duplex track: it treats conversation itself —
  pauses, overlaps, backchannels — as something to model, not noise.
- Open weights, code, demos, and benchmarks make this a practical
  starting point for Korean/English voice products and research.
- The repo root is deliberately boring — just ignore-rules, licenses,
  and dependencies. All the action lives under `src/raon/`.

## Jargon decoder

| Term | Plain definition |
|---|---|
| SpeechLM | A language model that understands and produces speech, not just text. |
| TTS (text-to-speech) | Turning written words into spoken audio. |
| STT (speech-to-text) | Writing down what someone said; transcription. |
| Full-duplex | Both sides can talk and listen at once, like a phone call. |
| Turn-taking | Figuring out when one speaker finishes and the other should start. |
| Backchanneling | Short listener sounds ("uh-huh", "yeah") that mean "I'm following." |
| Audio encoder | The part that converts raw sound waves into numbers the model can use. |
| Audio codec (Mimi) | A compressor that turns sound into small tokens and back again. |
| Streaming / causal | Processing sound as it arrives, without peeking into the future. |
| Checkpoint / repo_id | A saved trained model, loaded by name like `KRAFTON/Raon-Speech-9B`. |
| RTF / TTFT / TBT | Speed scores: how fast vs. real time, time to first sound, time between sounds. |
| Speaker embedding | A voice fingerprint used to make TTS sound like a specific person. |
