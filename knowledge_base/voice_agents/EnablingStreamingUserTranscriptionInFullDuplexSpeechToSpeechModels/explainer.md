> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Enabling Streaming User Transcription in Full-Duplex Speech-to-Speech Models — In Plain Language

## What is this about?

Imagine talking to a voice assistant that can listen and speak at the same time, just like a real person.

- Most voice assistants today are "walkie-talkie" style: you finish talking, then they answer.
- "Full-duplex" systems are more like phone calls: both sides can talk or interrupt at any moment.
- The catch: these natural-talking systems had no live written record of what the user was saying.
- Without that transcript, you cannot show captions, search the conversation, or check what was heard.
- This paper, from NVIDIA's Hu et al., fixes that missing piece.
- It adds a dedicated "transcription channel" that writes down the user's words in real time.
- Crucially, it does this while the assistant is still listening, thinking, and speaking.
- The result is a talkative AI that also takes notes on what you say, live.
- The headline numbers: about 10% word error rate inside the live conversation system.
- And about 7.7% error when the same design is trained purely as a transcriber.

## Why does it matter?

A voice assistant that cannot write down what it heard is hard to trust and hard to use.

- No transcript means no conversation log: you cannot scroll back or audit what happened.
- No transcript means weaker accessibility: deaf and hard-of-hearing users get no live captions.
- Earlier full-duplex systems (like Moshi) could chat naturally but offered no streaming user transcript.
- One workaround mixed transcription and reasoning into a single text stream, blurring two different jobs.
- This paper treats transcription as its own dedicated output, separate from the assistant's reply.
- That separation keeps the assistant's thinking clean while still capturing the user's words.
- Better still, the extra transcription barely disturbs the conversation flow.
- Turn-taking and interruption handling stay competitive: 90% precision, 95% recall, 100% barge-in accuracy.
- It even slightly helps question answering: OpenbookQA rises from 66.59% to 69.01%.
- In short: you get captions and logs almost for free, without breaking natural conversation.

## How does it work?

Think of it as giving the AI a second pen so it can write two things at once.

- The base system is called SALM-Duplex, built from two parts.
- Part one is a streaming speech encoder (Parakeet, 600M parameters) that turns audio into embeddings every 80ms.
- Part two is a large language model (Nemotron-Nano-9B-v2-Base, 9B parameters) that reasons and drafts replies.
- User speech, user transcript, and agent text are processed as three aligned streams.
- The new piece is a small extra "ASR head" sitting next to the assistant's reply head.
- Both heads share the same language model, so one decoding pass produces both outputs together.
- That means minimal extra parameters and no second expensive model run.
- To teach it timing, training aligns each written word with the exact audio moment it was spoken.
- This uses on-the-fly CTC forced alignment (torchaudio plus the MMS-FA acoustic model) during training.
- Words are anchored at their start ("left alignment"), which worked better than anchoring at the end.
- Silent gaps between words are filled with placeholder tokens so every audio frame has a target.
- Two delay knobs trade speed against accuracy: user-text delay `du` (set to 1.2s) and agent-text delay `da` (0.16s).
- A longer `du` gives the transcriber more context; a short `da` keeps replies snappy.
- Training mixes live conversation data, plain text chats, quizzes, speech instructions, and 16k hours of transcription data.
- Noisy backgrounds are added half the time so the model learns bars, streets, and cheap headsets too.

## Where can this be used?

Anywhere a voice AI talks naturally and someone needs a reliable live record.

- Live captions for voice calls, meetings, and customer-service bots.
- Conversation logging for support desks, clinics, and sales calls that need audit trails.
- Accessibility features for users who read along while they listen.
- Smarter interruption handling: the assistant sees the live transcript and responds better when cut off.
- In-car or hands-free assistants where glancing at a transcript confirms "did it hear me right?".
- Voice agents that hand off to humans: the transcript is the briefing note.
- Evaluation and debugging: developers can compare what was said versus what the agent did.
- Research systems that study turn-taking, pauses, and overlaps in real conversations.
- Standalone transcription: the same design, minus the chat heads, works as a competitive streaming transcriber.
- Any product that wants lower-latency transcription (1.2–1.6s) without running a separate speech recognizer.

## Conclusions & takeaways

A tiny extra output head solves a big practical gap in conversational AI.

- A lightweight parallel transcription head adds live user captions to full-duplex speech models.
- It needs minimal extra parameters and no major surgery on the base system.
- Inside the live chat system it reaches 10.21% average word error rate, beating dedicated FastConformer baselines.
- Conversation quality is preserved: turn-taking, barge-in, and interruption responses stay strong.
- It even handles pauses better than Moshi (far fewer false takeovers) at the cost of slightly slower smooth turn-taking.
- As a pure transcriber it reaches 7.73% average error, close to state-of-the-art streaming systems.
- The remaining gap is attributed to training on only part of the Granary dataset.
- Bottom line: natural-talking voice AI no longer has to choose between "conversational" and "accountable".

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Full-duplex | Both sides can listen and speak at the same time, like a phone call |
| Speech-to-speech (S2S) model | An AI that takes in voice and answers back in voice |
| Streaming transcription (ASR) | Writing down speech as it happens, word by word, not after the fact |
| ASR head | A small extra output layer whose only job is writing down the user's words |
| Turn-taking | Knowing when it is your turn to speak versus when to stay quiet |
| Barge-in | When the user interrupts the assistant mid-sentence and it must stop and listen |
| Word error rate (WER) | Share of words transcribed wrong; lower is better |
| Forced alignment | Matching each written word to the exact audio moment it was spoken |
| Latency | The delay between you finishing a sentence and the system reacting |
| Backbone LLM | The big language model doing the reasoning that both outputs share |
