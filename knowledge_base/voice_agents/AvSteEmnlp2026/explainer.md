> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# AV-STE: Audio-Visual Speech Token Enhancement — In Plain Language

## What is this about?

Imagine you are on a video call in a noisy cafe. Your voice is drowned out
by clattering dishes and the table next to you, so the computer hears
garbage instead of your words.

AV-STE is a fix for that problem, designed for voice-based AI assistants
like Moshi that "think" in small sound-pieces called tokens.

Instead of trying to clean up the sound wave itself, AV-STE tries to
recover the correct sound-pieces — the clean tokens — directly from the
noisy microphone feed plus a small video of your mouth.

In one concrete demo, a sentence about Paris was buried under another
person talking at −5 dB. The plain audio-only system got only 27.6% of the
tokens right. With lip video added, AV-STE recovered 79.3% of them, and
the assistant's reply stayed on topic.

## Why does it matter?

Modern talking AIs do not pass around sound waves internally. They pass
around tokens: short labels, produced about 12 times per second, that say
roughly "this slice of sound means this speech content."

When noise corrupts those tokens, everything downstream breaks. The AI
mishears you and gives a confused or off-topic answer. Cleaning the
waveform does not always fix the tokens.

AV-STE matters because it repairs the tokens themselves. The repaired
tokens can be dropped into any compatible system — a text-to-speech voice,
a speech codec, or a dialogue model like Moshi — without retraining that
system.

The practical effect: a voice assistant that keeps understanding you in
background chatter, street noise, or a competing speaker, as long as it
can also see your lips.

## How does it work?

Think of it in three everyday steps: look, listen, and decide whom to trust.

1. **Look at the lips.** The system crops a small 96×96 black-and-white
   box around your mouth from the video, 25 frames per second. Lips are
   hard for background noise to fake, so they carry reliable clues about
   what sounds you are making.

2. **Listen to the noisy audio.** The microphone feed is resampled to
   standard 16 kHz mono. From it, the system reads the noisy version of
   the speech tokens.

3. **Fuse the two, trusting each source by the moment.** This is the core
   trick: an entropy-gated cross-attention module built on a model called
   AV-HuBERT. In plain terms, at every instant the system asks itself,
   "how sure is the audio right now?" When the audio is clear, it leans
   on the audio. When the audio is uncertain or confused, it leans more
   on the lip movements.

The model starts from a public lip-reading backbone and is then trained on
a mix of clean speech, background noises, and competing voices at loudness
levels from −10 to +10 dB. There are two released versions: one for
general background noise, and one specialized for competing speakers.

Input: one noisy audio clip plus one lip video.
Output: the repaired sequence of meaning-carrying tokens, about 12 per
second, ready to feed into a voice AI.

## Where can this be used?

- **Voice assistants in noise.** Kitchen smart speakers, car assistants,
  or video-call bots that must understand you over TV sound or cafe noise.
- **Full-duplex dialogue systems.** Assistants like Moshi that listen and
  speak at the same time are easily derailed by their own echo or by
  interruptions. Cleaner tokens keep the conversation on track.
- **Hearing assistance and transcription.** Any app that turns speech into
  text or re-spoken audio in crowded rooms, as long as a face camera is
  available and looking at the speaker.
- **Video conferencing.** Laptop calls where the camera already sees your
  face: the lip stream is essentially free extra evidence.
- **Robotics and kiosks.** Airport or street-facing machines that must
  pick one speaker out of a crowd.

What it needs: a visible, front-facing face, a correct mouth crop, and
matching 16 kHz audio. Without usable video — a covered face, a profile
view, darkness — it falls back to roughly audio-only behavior.

## Conclusions & takeaways

- Noise breaks the tokens that voice AIs reason with, not just the sound
  humans hear. Fixing the tokens fixes the assistant.
- Lips are a noise-proof second channel. Fusing them with audio gives
  large gains: in the showcased example, token accuracy roughly tripled
  and transcription error fell from 61.5% to 38.5%.
- Smart fusion beats blind fusion. The system dynamically trusts video
  more exactly when audio is uncertain.
- Token accuracy is the real scoreboard here, because the tokens plug
  straight into other models. Listening-quality sound is a helpful but
  secondary check.
- Limits are honest: demo clips were chosen to show a clear before/after,
  not average performance, and the method needs a good lip video plus
  licensed datasets to fully reproduce the paper's tables.

In short: give a talking AI both ears and eyes, teach it when to trust
each, and it understands you in noise far better than with ears alone.

## Jargon decoder

| Term | What it really means |
|---|---|
| Semantic token (cb0) | A short label, produced ~12 times per second, capturing *what* was said rather than exact voice quality. |
| Mimi | The speech codec that turns audio into tokens and back; AV-STE repairs its meaning-carrying layer. |
| Token accuracy | The main score: what fraction of repaired tokens match the clean-recording tokens. Higher is better. |
| WER (word error rate) | A secondary check: how many words a transcriber gets wrong on the re-decoded audio. Lower is better. |
| Lip ROI | The small cropped video box around just the mouth that the model watches. |
| AV-HuBERT | A pre-trained model that already understands how lip movements line up with speech sounds. |
| Cross-attention | The mechanism that lets the audio stream "ask questions" of the video stream at each moment. |
| Entropy-gated | A confidence switch: when audio is uncertain, the system turns up reliance on video. |
| SNR (signal-to-noise ratio) | How loud your voice is compared to background noise, in dB. Negative means noise is louder. |
| Moshi | A full-duplex voice dialogue AI that consumes these tokens to hold spoken conversations. |
