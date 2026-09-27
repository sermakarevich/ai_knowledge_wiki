> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# wavekat/wavekat-turn — In Plain Language

## What is this about?

Imagine you are talking to a voice assistant on the phone.
There is an awkward moment in every such call: you pause to think,
and the assistant jumps in too early — or you finish speaking,
and it just sits there in silence.

This project is about fixing that moment.

`wavekat-turn` answers one simple question: "are they done speaking?"
That is different from the simpler question "is someone speaking right now?"
which is handled by a related tool for voice detection.

Think of it like a conversation helper at a dinner table.
One helper notices when someone's mouth is moving.
This helper notices when someone has actually finished their thought,
so the next person knows it is their turn to talk.

It is a small building block for voice apps, written in Rust,
and designed to sit inside a bigger voice pipeline alongside tools
that hear speech, understand words, generate replies, and speak them back.

## Why does it matter?

Getting "your turn versus my turn" wrong ruins voice conversations.

If the assistant interrupts, users feel cut off and repeat themselves.
If it waits too long, every exchange feels slow and robotic.
Humans handle this naturally with pauses, tone of voice, and half-finished sentences.
Machines need an explicit model for it.

This project matters because it packages that judgment into a reusable part:

- App builders do not have to train their own model or guess with timers.
- They can swap different detection models behind one common interface.
- The audio option is tiny and fast, so it can run on an ordinary computer
  without a graphics card and keep up with live speech.
- There is also a text-based option that reads written-down speech
  when an app already converts voice to text.

In short: fewer interruptions, less dead air, more natural conversations.

## How does it work?

Picture the system as a listener with three possible verdicts
after each short stretch of speech:

- "Finished" — the person is done, pass it on to the assistant's brain.
- "Unfinished" — the person is just pausing, keep listening.
- "Wait" — the person asked the assistant to hold on a moment.

Here is the flow in everyday terms:

1. **Listen continuously.** The app feeds small slices of audio into the detector
   as the person talks, like topping up a bucket drop by drop.
2. **Pick a brain.** The app chooses one of three ready-made brains:
   a small fast audio model, a language-specialized version of the same model
   (Mandarin Chinese is shipped first), or a larger text model
   that judges written transcripts instead of sound.
3. **Keep state with a controller.** A wrapper called the turn controller
   remembers what happened so far. When speech starts again, it does a gentle
   reset that keeps the buffer if the last turn was unfinished. When the
   assistant finishes replying, it does a full reset for the next round.
4. **Predict at pause time.** When the voice detector says speech just ended,
   the turn detector looks at the buffered audio or text and returns
   one of the three verdicts above.
5. **Stay honest with input rules.** The audio models only understand
   clean 16 kHz sound. Phone-quality 8 kHz audio must be converted up first,
   or the results are quietly wrong. The text model is only as good
   as the speech-to-text feed it reads.
6. **Check against the original.** Accuracy is tested by comparing the Rust
   version against the original Python version on three sample recordings,
   allowing only a tiny difference in scores. A single command reruns the check.

Developers turn features on and off at build time, so an app only carries
the model it actually uses. Language variants reuse the exact same
data format, so adding a new language later does not rewire the app.

## Where can this be used?

Anywhere a machine needs to hold a spoken conversation:

- **Voice assistants and phone bots** — decide when to reply instead of
  interrupting or leaving long silences.
- **Call centers** — hand the call to the next step at the right moment.
- **In-car or smart-home controls** — handle slow, hesitant speech
  with lots of mid-sentence pauses.
- **Translation and meeting tools** — wait until a speaker truly finishes
  before translating or summarizing.
- **Multilingual apps** — start with the general audio model, then switch
  to a language-tuned version (such as Mandarin) for better accuracy,
  without changing the rest of the code.
- **Text-pipeline apps** — use the transcript-based model when the app
  already has good live captions and wants a judgment based on words
  rather than tone of voice.

It is not the whole voice app — it is the "is it my turn yet?" reflex
that makes the whole app feel polite.

## Conclusions & takeaways

- Turn detection is its own job, separate from noticing sound or writing
  down words. Naming it clearly keeps the pipeline clean.
- One shared interface with swappable models keeps apps flexible:
  small and fast for audio, bigger and word-aware for text.
- Small details decide quality: correct audio sample rate, good transcripts,
  and remembering pause-versus-finished state between turns.
- Testing against a trusted reference keeps the fast Rust version honest.
- The practical payoff is simple: assistants that interrupt less,
  respond faster, and feel more human.

## Jargon decoder

| Term | What it really means |
|------|----------------------|
| Turn detection | Deciding whether the speaker has finished their turn. |
| VAD (voice activity detection) | Noticing whether anyone is speaking right now. |
| ASR (speech-to-text) | Software that writes down what was said. |
| Audio backend | A model that judges turn-taking from raw sound. |
| Text backend | A model that judges turn-taking from written words. |
| ONNX model | A portable, shared file format for running trained models. |
| int8 model | A shrunken model that runs faster with slightly less precision. |
| Trait / interface | A shared plug shape so different models can be swapped in. |
| Turn controller | The wrapper that tracks state and resets between turns. |
| Soft reset vs hard reset | Gentle keep-your-place reset vs full start-over reset. |
