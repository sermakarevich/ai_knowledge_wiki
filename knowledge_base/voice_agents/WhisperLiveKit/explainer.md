> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# QuentinFuxa/WhisperLiveKit — In Plain Language

## What is this about?

WhisperLiveKit is a free, open-source toolkit that turns spoken words into written text in real time.

Think of it like live captions for anything: a meeting, a lecture, a podcast, or a phone call. You talk, and words appear on screen almost instantly.

It can also translate speech live — for example, someone speaks French and you read English subtitles as they talk.

You interact with it in three simple ways: a one-line install and command (`pip install whisperlivekit`, then `wlk`), a web page that shows live captions, and programming interfaces (a standard web API and a live streaming connection) so other apps can use it.

Under the hood it is built on the well-known Whisper speech-recognition family, but adapted for streaming instead of processing whole files at once. It also plugs in newer speech models (Voxtral, Qwen3-ASR, SenseVoice) and add-ons for translation and telling speakers apart.

## Why does it matter?

Regular speech-to-text tools usually wait for a whole sentence or file before they respond. That creates delay and awkward pauses in live settings.

Chopping live audio into small pieces naively causes another problem: words get cut in half and context is lost, so accuracy drops.

WhisperLiveKit matters because it applies recent simultaneous-speech research to fix that trade-off. It decides moment by moment when it has heard enough to safely write a word down, instead of guessing too early or waiting too long.

It also matters for practical reasons:

- It serves many users at once from one server, and quiets down when nobody is speaking, which saves computing power.
- It speaks the same language as the popular OpenAI transcription API, so existing tools can switch over with little code change.
- It runs on many kinds of computers — laptops, Apple Silicon Macs, plain CPUs, or powerful NVIDIA GPUs — through optional install packs.
- Its speed claims are backed by repeatable public tests on audiobook recordings, not just marketing numbers.

In short: lower delay, fewer cut-off words, and a setup ordinary developers can actually deploy.

## How does it work?

Imagine a careful listener taking notes during a fast talk. That is roughly the pipeline:

1. **Listen continuously.** Your microphone or audio file streams small slices of sound to the server over a live connection.
2. **Check if anyone is speaking.** A voice detector filters out silence, typing, and background noise so the heavy AI only runs when needed.
3. **Decide when a word is ready.** Instead of transcribing every slice blindly, smart rules watch the AI's confidence:
   - One strategy watches where the model's attention points and only locks in words the audio has fully covered.
   - Another strategy waits until two consecutive guesses agree before showing text, which avoids flickering corrections.
   - Newer models use encoders that read each audio block exactly once and never rewrite old words, keeping cost constant over time.
4. **Write, fix, and translate.** Early guesses appear quickly and are refined as more audio arrives. If translation is on, a second model converts the confirmed words into the target language.
5. **Label who spoke (optional).** A speaker-tracking add-on tags segments as speaker one, speaker two, and so on.
6. **Send results to clients.** The web page shows full snapshots of the transcript; advanced developers can choose a compact "only send what changed" mode. Offline files skip the server entirely and go straight to text or subtitle files.

A shared engine holds the loaded AI models, while each caller gets a private session with its own language, translation target, vocabulary hints, and access token.

## Where can this be used?

- **Meetings and classrooms:** live captions, searchable notes, and subtitles for remote attendees.
- **Customer support and call centers:** real-time transcripts, agent assistance, and automatic call summaries.
- **Media and creators:** turning podcasts and videos into text, subtitles (SRT files), and searchable archives.
- **Multilingual events:** live translation when speaker and audience do not share a language.
- **Accessibility:** instant captions for people who are deaf or hard of hearing.
- **Voice apps and demos:** browser extensions that caption any web audio, a Mac desktop client, and custom apps built on the web API.
- **Research and testing:** comparing models and hardware with the built-in benchmark command, since all test audio and scripts are public.

It fits anywhere you would otherwise wait for a recording to finish before transcribing it.

## Conclusions & takeaways

- WhisperLiveKit is live-caption infrastructure, not just a demo: install, run one command, open the web page, and talk.
- Its core trick is patience with proof — commit words only when the audio evidence is stable, which keeps latency low without mangling sentences.
- One server can handle many sessions in different languages, ignore silence cheaply, and plug into existing OpenAI-style code.
- Hardware flexibility is a feature: pick a lightweight pack for a laptop or a heavy GPU pack for best accuracy, accepting that some packs cannot be mixed.
- If you remember one idea, remember this: good live transcription is less about hearing faster and more about knowing when to wait half a second.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Streaming transcription | Writing down speech while the person is still talking, not after they finish. |
| Simultaneous translation | Translating live, sentence by sentence, instead of waiting for the whole speech. |
| Voice Activity Detection (VAD) | An automatic "is anyone speaking?" switch that saves work during silence. |
| AlignAtt policy | A rule that publishes a word only once the AI has clearly heard the matching audio. |
| LocalAgreement policy | A rule that shows text only when two back-to-back guesses agree, reducing flicker. |
| Speaker diarization | Figuring out "who spoke when" and labeling speaker one, speaker two, etc. |
| Causal encoder | A listener that reads each sound chunk once and never goes back to redo old work. |
| WebSocket | A persistent live wire between app and server for sending audio and receiving words instantly. |
| REST API | A simple send-a-file, get-text-back web request, compatible here with OpenAI's format. |
| Backend / extras | Swappable AI engines and install packs for different chips, languages, and speed needs. |
| Benchmark | A timed accuracy test on public audiobooks so speed claims can be checked and repeated. |
| Subtitles (SRT) | A standard caption-file format with timestamps for video players. |
