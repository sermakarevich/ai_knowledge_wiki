> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# renan-martini/saybench — In Plain Language

## What is this about?

Saybench is a command-line tool that tests how well voice-AI services
handle *your* audio — your callers, accents, jargon, and phone-line quality.

Instead of trusting a vendor's demo numbers, you point saybench at your own
clips plus the written transcripts of what was actually said, and it scores
each provider on the same material.

It covers the whole voice pipeline in five modes: batch transcription
(send a file, get text back), streaming transcription (words as you speak),
the AI's reply step, full speech-to-speech voice bots, and text-to-speech
voice output.

Every mode ships with an offline "fake" provider, so you can try the full
workflow with zero API keys before spending a cent.

A bundled golden set of 14 clips (September 2026) gives a ready-made example:
one vendor scored 3.8% word error rate, the offline fake scored 16.5%,
and another vendor scored 19.0%.

## Why does it matter?

A single headline accuracy number hides the truth. In the published runs,
the vendor with 19% overall errors actually *beat* the 3.8% vendor on
acronyms, names, and casual conversation — and a third of its "errors"
were just digit formatting (like "429" vs "four two nine"), not mishearing.

Speed headlines mislead too. Two vendors only ~400ms apart on batch files
were 5x apart on how fast the first live word appeared — and that first-word
delay is what callers actually feel.

Connection setup matters as well: a cold connection took ~1109ms to the
first AI token versus ~595ms on a warm one, roughly a 3x effect hiding
inside "average latency."

And degradations are silent without automation, so saybench wires scoring
into CI: if a provider gets worse than your baseline, the build fails
before your customers notice.

## How does it work?

You start with a zero-key smoke test using the fake provider and bundled
clips: `saybench stt -providers fake`.

Then you add real vendors via environment keys only (never flags or config
files) and save a baseline report: `saybench stt -providers deepgram,openai
-report baseline.json`.

To test your own audio, you write a small manifest file listing each clip,
its correct transcript, and a category like "numbers" or "names" — then run
saybench against it.

Each mode measures what matters for that step: batch mode reports error
rate with a breakdown plus how many key terms (like customer names) survived;
streaming reports time-to-first-word and how stable early guesses were; the
AI step reports time-to-first-token; speech-to-speech reports voice-to-voice
delay and whether the bot understood an echo test; speech output reports
time-to-first-audio.

Later runs are compared against the baseline with a command like
`saybench compare baseline.json today.json -max-wer-regression 2.0`,
which fails if any provider got more than 2 points worse.

Results render as JSON, a terminal table, or a single-file HTML dashboard,
and a built-in MCP server lets coding agents drive the whole tool.

## Where can this be used?

Any team picking a transcription vendor for support calls, voicemail,
or meeting notes can rank providers on their own recordings first.

Builders of live voice agents can find who shows the first word fastest
and whether a warm connection or a different transport actually helps.

Teams wiring an AI reply step into a phone call can separate model speed
from network setup cost before promising a latency budget.

Anyone choosing between a do-it-all voice bot and a pipeline of separate
speech, AI, and voice steps can compare directly: the speech-native model's
first audio averaged 601ms versus ~808ms before the composed pipeline even
started speaking — but it talked 12.4 seconds per reply and sometimes
*performed* an echo instruction instead of repeating it.

Platform teams can add the compare gate to CI so a vendor API change or a
prompt regression fails the build, with condition-aware warnings (warm vs
cold, echo vs conversational) explaining the numbers.

## Conclusions & takeaways

Test on your own audio, because average error rates hide cases where the
"worse" vendor is better at exactly the words you care about.

Measure live-call delays, not just batch speed — first-word and first-audio
times decide whether a call feels snappy or broken.

Score honestly: break errors into types, check key terms separately, and
never print a flattering 0% when there is simply no data.

Automate the comparison so regressions fail the build instead of reaching
callers, and keep the design boring — keys from the environment, deadlines
on every network call, deterministic reports.

Saybench's plain lesson: the best voice stack is the one that hears *your*
callers, answers fast enough to feel live, and proves it every commit.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| STT (speech-to-text) | Turning recorded or live speech into written words. |
| Batch STT | Sending a whole audio file at once and getting the full transcript back. |
| Streaming STT | Transcribing live as someone speaks, with early guesses that update. |
| WER (word error rate) | Share of words the system got wrong; lower is better. |
| Keyterm recall | Share of important words (names, order numbers) that survived correctly. |
| TTFT / time-to-first-token | How long until the AI's reply starts arriving. |
| Time-to-first-partial | How long until streaming transcription shows its first guess. |
| Speech-to-speech | A voice bot that listens to speech and talks back directly. |
| TTS (text-to-speech) | Turning written text into spoken audio. |
| Time-to-first-audio | How long until the generated voice starts playing. |
| CI regression gate | An automatic check that fails the build if scores got worse. |
| MCP server | A hook that lets an AI coding assistant operate the tool. |
