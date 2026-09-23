> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# StepAudio 3 Realtime Technical Report — In Plain Language

## What is this about?

StepAudio 3 Realtime is a voice AI designed to talk with you live, like a phone call.

Most voice assistants work in turns: you speak, then they think, then they answer.

This one listens, talks, thinks, and takes actions all at the same time.

It is built around a loop with four jobs:

- **Deep Perception:** hear not just your words, but how you say them — tone, pauses, background sounds.
- **Seamless Duplex:** manage the flow of conversation — when to speak, when to wait, when to let you interrupt.
- **Think-While-Speaking:** start answering before it has finished thinking, so replies feel instant.
- **Voice Agent:** look things up and do tasks (bookings, account questions) while still chatting.

A sister model, called ASR Max, focuses only on writing down speech very accurately.

## Why does it matter?

Talking is harder than texting for an AI.

People pause mid-sentence, say "uh-huh" just to show they are listening, interrupt, or talk over the AI.

A good voice assistant must tell the difference between "I am just thinking…" and "I am done, your turn."

It also faces a trade-off: thinking carefully takes time, but waiting too long feels awkward.

This report matters because it shows one system handling both sides at once:

- Smart answers (73.0 score on the StepAudioChat reasoning test).
- Fast, natural conversation (98.9 overall on the full-duplex conversation test).
- Strong hearing (top scores on several audio-understanding tests, such as 90.6 on MMSU).
- Real tasks done by voice (56.0% success on the τ-Voice customer-service test).

In short: careful thinking without the awkward silence.

## How does it work?

Think of it like a skilled receptionist who can listen, talk, think, and type at once.

**1. It keeps a shared notepad.**

Everything goes on one notepad: what you said, how you sounded, what it already said, how far its thinking has got, and whether a tool task is still running.

New speech or a tool result can change the plan at any moment — for example, stop talking and listen because you interrupted.

**2. It hears more than words.**

The hearing part (an audio encoder plus an adapter) turns sound into a form the language brain can understand.

Training happened in three stages — first connect sound to words, then train on huge mixed audio-plus-text data (1.2 trillion tokens), then polish on the best data — plus extra training on long conversations up to 128K context.

The ASR Max version is fine-tuned purely for transcription, reaching very low error rates like 1.18 on clean English and 0.49 on Mandarin AISHELL-1.

**3. It manages the conversational floor.**

The model asks: was that a pause or the end of your turn? Was that "right" a friendly nod or the start of a correction? Is that background chatter meant for me?

It learned this from over 10,000 hours of made-up two-sided conversations, plus practice on pauses, interruptions, backchannels, and ignoring background talk.

Result: first place on the full-duplex test, with 100.0 on turn taking and 99.0 on interruption handling.

**4. It thinks while it speaks.**

Instead of thinking fully and then speaking, it splits the job: one "brain" keeps reasoning privately while the other speaks short pieces out loud.

Simple questions skip deep thinking; hard ones get full reasoning. A shortcut called multi-token prediction drafts several thought-words at once, making private thinking about 1.5–2× faster.

Spoken quality stays close to the slow careful mode: 70.4 live versus 73.0 with full reasoning.

**5. It does tasks in the background.**

Simple questions are answered directly. Fresh facts go to quick tools like weather or web search. Bigger jobs (account lookups, multi-step bookings) run in the background while you keep talking.

It is trained to ask for missing details, confirm before acting, give progress updates, and fold results back into the chat.

## Where can this be used?

- **Customer service by voice:** airline changes, telecom support, store help — including interruptions and revised requests mid-call.
- **Hands-free helpers:** driving, cooking, or accessibility settings where you cannot look at a screen.
- **Live translation and transcription:** meetings and calls where rare names and technical terms must be heard correctly.
- **Companions and tutors:** natural back-and-forth with memory of earlier turns, persona, and topic.
- **Noisy real rooms:** kitchens, call centers, and streets where background voices must be ignored.
- **Agents that work while talking:** "check my booking while I keep explaining" instead of "please hold."

Weak spots today: retail tasks (37.7% vs 49.7% for the best rival) and following many stacked instructions across long conversations.

## Conclusions & takeaways

- Real-time voice needs listening, speaking, thinking, and acting at the same time — not one after another.
- Good hearing plus smart floor control (pauses, interruptions, background talk) is what makes conversation feel natural.
- Thinking-while-speaking is the key trick: answer now, keep reasoning in the background, think deeply only when needed.
- Data quality beats quantity: about 100K carefully checked examples beat 2M random ones on audio tests.
- The system is strong on hearing, turn-taking, and telecom tasks, but still has room to grow on retail tasks and complex multi-turn rules.
- Bottom line: this is a recipe for a voice assistant that is both quick and thoughtful.

## Jargon decoder

| Term | What it really means |
|---|---|
| Full-duplex | Both sides can speak and hear at the same time, like a phone call, not walkie-talkie turns. |
| Backchannel | A short "mm-hm" or "right" that means "I am listening," not "it is my turn." |
| Turn taking | Deciding when one speaker finishes and the other should start. |
| ASR (speech recognition) | Turning spoken sound into written words; scored by error rate (lower is better). |
| Mixture-of-experts | A model with specialist sub-parts; only a few switch on per request to save effort. |
| Think-While-Speaking | Start talking before private reasoning is finished, then keep improving the answer. |
| Adaptive Thinking | A switch that skips deep reasoning for easy turns and uses it for hard ones. |
| Multi-token prediction (MTP) | Draft several future words at once to think faster instead of one word at a time. |
| Voice Agent | The part that calls tools and services (search, bookings, accounts) by voice request. |
| τ-Voice benchmark | A test of voice agents doing airline, retail, and telecom customer tasks. |
