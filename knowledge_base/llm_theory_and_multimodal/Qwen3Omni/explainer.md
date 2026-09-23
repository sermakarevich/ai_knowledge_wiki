> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# QwenLM/Qwen3-Omni — In Plain Language

## What is this about?

Qwen3-Omni is an AI model that can see, hear, and talk back.

Most chatbots only read typed text. Qwen3-Omni accepts four kinds
of input — typed text, photos, spoken audio, and video — and answers
back in two ways: written text and natural-sounding speech.

It works in real time. You can speak to it, show it a video, and it
streams its reply as it thinks, the way a video call feels, instead
of making you wait for one big block of text at the end.

It is also multilingual. It reads text in 119 languages, understands
speech in 19 languages, and can speak its answers aloud in 10 languages.

There is a second, smaller specialist in the same family: a model
called Qwen3-Omni-30B-A3B-Captioner that does one job — listening to
an audio clip and writing a detailed description of what it hears.

## Why does it matter?

Three reasons make this notable.

First, breadth without trade-offs. Usually, teaching a model new
skills (like hearing) makes it worse at old ones (like writing).
Qwen3-Omni was trained text-first and then on mixed data, so it keeps
its reading and image skills while adding hearing and speaking.

Second, strong results. It scores at the top on 22 out of 36 tested
audio and video tasks, and is the best freely available model on 32
out of 36. Its speech recognition, sound understanding, and voice
conversation are described as comparable to a leading commercial
system, Gemini 2.5 Pro.

Third, it is practical and open. Anyone can download it, run it on
their own machine, and try it through ready-made demo apps and
step-by-step example notebooks — no paid API required.

## How does it work?

Think of it as a brain plus a voice, working as a team.

The "Thinker" is the brain. It takes in whatever you give it — words,
a picture, a sound clip, a video — and figures out what it means and
what to say next. It is built as a Mixture-of-Experts, which means it
has many small specialist sub-models inside and only wakes up the few
it needs for each question. That keeps it fast while staying smart.

The "Talker" is the voice. Once the Thinker decides what to say, the
Talker turns those words into spoken audio, streamed out piece by
piece so you hear it almost immediately. A special multi-part design
keeps the delay between thinking and speaking as short as possible.

Training happened in stages. The model first learned language from
text, then learned to connect sounds and images to that language
ability — including a stage called AuT pretraining that links audio
understanding to text understanding.

In everyday use the flow is simple: your message (text plus any
photos, clips, or recordings) is formatted into a chat, a processor
bundles the media together — including the sound inside videos — and
the model generates a reply. You can pick one of three voices
(Chelsie, Ethan, or Aiden), and the spoken reply comes back as
standard audio. A chat demo handles full conversations; the captioner
demo handles single audio clips only.

## Where can this be used?

The example notebooks show the range. For sound alone: transcribe
speech in many languages (even long recordings), translate speech to
other languages as text or speech, describe any sound, tell music
styles and rhythms apart, or untangle clips mixing speech, music, and
background noise.

For pictures and video: read text out of messy photos, find and point
to objects in an image, answer questions about any photo, solve a math
problem photographed on paper, describe a video in detail, give
navigation instructions from a first-person video, or spot when a
scene changes.

For live interaction: hold a spoken conversation with natural
back-and-forth turn-taking, control the model's personality and rules
with a system prompt (for example, "keep spoken answers under 50
words"), and run it locally for private or offline use, such as a
voice assistant, a meeting helper, or an accessibility tool that
describes what it sees and hears.

## Conclusions & takeaways

Qwen3-Omni is best understood as a single model that reads, looks,
listens, watches, writes, and speaks — live and in many languages.

Its headline promise is "everything in, speech out, in real time,"
without losing the text skills it started with, and its test scores
back up that promise on audio and video tasks.

If you remember one thing: the Thinker understands, the Talker
speaks, and the demos plus notebooks let you try both on your own
computer today — full conversation in one app, detailed audio
descriptions in the other.

## Jargon decoder

| Term | What it really means |
| --- | --- |
| Omni-modal | The model accepts many input types (text, image, audio, video), not just typed words. |
| Foundation model | A large general-purpose model others can reuse for many tasks instead of building from scratch. |
| Streaming response | The answer arrives piece by piece as it is made, so you see or hear it right away. |
| Mixture-of-Experts (MoE) | The model holds many small specialists and only uses a few per question, saving time and compute. |
| Thinker–Talker | Two-part design: one part decides what to say, the other turns it into spoken audio. |
| AuT pretraining | A training stage that teaches the model to connect what it hears with what it reads. |
| Multi-codebook design | A technique for turning speech into compact codes so audio can be generated with low delay. |
| Turn-taking | The natural rhythm of conversation — knowing when one speaker finishes and the other starts. |
| System prompt | Hidden instructions that set the model's behavior, style, or rules for the whole chat. |
| Captioner | A specialist model that listens to audio and writes a detailed description of it. |
