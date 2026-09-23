> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Endpoint Anticipation for Low-Latency Spoken Dialogue — In Plain Language

## What is this about?

Talking to a voice assistant often feels sluggish: you finish speaking, and then there is an awkward pause — often a second or more — before it answers.

This paper asks: what if the assistant did not wait until you were completely done? Instead, it tries to *guess* you are about to finish — up to about 2.5 seconds early — and starts preparing its answer while you are still talking.

The authors call this idea **Endpoint Anticipation**. Think of a chef who starts plating dessert when they see you taking your last few bites, rather than waiting until your fork is down.

If the guess is right, the answer is ready almost instantly. If the guess is wrong, the half-made answer is thrown away and the system tries again.

The paper builds a small listening model that makes these guesses from raw sound alone, plus new ways to measure how much time is saved versus how much work is wasted.

## Why does it matter?

Humans in conversation respond fast: the gap between one person stopping and the other starting is roughly a quarter of a second (about 250 milliseconds). Today's voice pipelines are much slower — often 1 to 2 seconds.

The reason is their assembly line: first transcribe your speech, then think of a reply, then synthesize a voice — each step waiting for the last. Older "endpoint detectors" make this worse because they are reactive: they only confirm you finished *after* silence arrives, and only then does the whole pipeline start.

This matters for anything spoken and interactive: customer-service bots, in-car assistants, translation earpieces. Long pauses feel broken, and people start repeating themselves or talking over the system.

The paper shows a working demo inside a system called Unmute where this guessing trick cut the average wait from about 1195 ms to about 690 ms — a saving of roughly half a second — at the cost of about 28% extra throwaway computation. That is the difference between "laggy robot" and "almost human."

## How does it work?

The core idea is simple: forecast the end of the turn, don't just detect it after the fact. Here is the pipeline in plain steps:

1. **Listen to sound, not words.** The guesser works directly on the audio signal, without waiting for a transcript. That skips a slow step (speech recognition) entirely.
2. **Watch both sides.** It listens to two streams at once — you and the system — so it can tell a real ending apart from a short pause, a backchannel ("uh-huh"), or an interruption.
3. **Ask many small questions.** For each moment, it asks: "Will this person finish within 320 ms? Within 640 ms? ... Within 2560 ms?" Each time window gets a yes/no score.
4. **Set a trigger threshold.** When a score crosses a cutoff, the system fires: "go ahead and start answering early." A low cutoff means eager guesses (faster but more mistakes); a high cutoff means cautious guesses (slower but safer).
5. **Two model flavors.** EPA-S trains one separate model per time window; EPA-M trains one shared model with a separate output per window. Accuracy is similar, but EPA-M is cheaper because it needs no retraining for each new window.
6. **Speculate, then verify.** In the Unmute demo this means: fork the conversation state, draft roughly 10 reply tokens from the partial sentence, and pre-synthesize voice audio into a hidden cache. If the user really stops on time, the cached audio plays immediately. If not, it is discarded and the system keeps listening.

To keep score honestly, the paper defines four measures: how much time was actually saved on good guesses, how often guesses fired too early, how much extra compute was thrown away, and how accurately the system hit the exact start of the window.

Training used two datasets: SpokenWOZ (structured travel tasks) and Switchboard (freeform phone chats), with short filler turns under 2 seconds filtered out so the model does not learn to "anticipate" every "mm-hm."

## Where can this be used?

Anywhere a spoken system must feel snappy:

- **Task bots** — booking, banking, tech support, food ordering. Structured requests ("I need a hotel for Friday...") are the easiest to anticipate, and this is where the paper's scores are best.
- **Voice assistants and smart speakers** — cutting the dead air before an answer without rebuilding the whole pipeline.
- **Call centers and in-car systems** — masking slow language models and cloud round-trips by doing the work during the caller's speech.
- **Full-duplex chat systems** — assistants designed for interruptions and overlapping talk, where both sides listen and speak at once.

It is less reliable today for freeform, spontaneous chit-chat, where people hesitate, restart sentences, or trail off — the paper finds clearly worse scores on Switchboard than SpokenWOZ. It also fits best in modular pipelines (transcriber + language model + voice synthesizer chained together), which is still how most production voice products are built. Another natural fit is live translation earpieces,
where each saved half-second keeps the conversation flowing
instead of stalling on every turn.

## Conclusions & takeaways

- Waiting for silence is the bottleneck; guessing the ending early is a practical way around it.
- A small sound-only model can forecast turn endings seconds ahead and beat the adapted baseline (VAP) by a wide margin — e.g. ~640 ms of real savings versus ~160 ms at one setting.
- There is no free lunch: every millisecond saved costs some wasted, thrown-away computation. The threshold knob lets builders pick their speed-versus-waste tradeoff.
- One shared multi-window model (EPA-M) matches separate per-window models, so deployment is simpler.
- The code and Unmute integration are being open-sourced, so other teams can plug the guesser into their own pipelines.
- Structured conversations benefit first; spontaneous conversation remains harder and is the main open challenge, along with tricky cases like mid-sentence U-turns ("...actually, never mind") or late key facts.
- Bottom line: speculate during speech, verify at the endpoint, and spoken dialogue gets ~500 ms closer to human timing.

## Jargon decoder

| Term | What it really means |
|---|---|
| Endpoint / end-of-turn | The moment you finish speaking and hand over the floor. |
| Endpoint detection | Noticing *after the fact* that someone stopped talking. |
| Endpoint anticipation | Guessing *in advance* that someone will stop talking soon. |
| Speculative execution | Starting the answer early on a guess; discard it if wrong. |
| Horizon | How far ahead the guess looks (e.g. 640 ms before the end). |
| EPA-S / EPA-M | Single-window vs. shared multi-window guesser models. |
| VAP (baseline) | An older turn-taking model the paper compares against. |
| ASR / LLM / TTS | Transcriber (speech-to-text), thinker (reply writer), speaker (voice maker). |
| MRA | Median time actually saved by good early guesses. |
| PAR / ERC | Share of guesses fired too early / share of compute wasted. |
| HEA | How often the guess fires at exactly the right moment. |
| SpokenWOZ / Switchboard | Structured task dialogues vs. casual phone chats used for testing. |
