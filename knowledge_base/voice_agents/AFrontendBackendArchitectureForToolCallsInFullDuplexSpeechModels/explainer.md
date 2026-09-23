> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# A frontend-backend architecture for tool calls in full-duplex speech models — In Plain Language

## What is this about?
This paper is about giving a talking voice assistant the ability to look things up and do things.

Think of a normal phone conversation: both people can speak, pause, and interrupt at any time. That is what "full-duplex" means here — talking and listening happen at the same time, with no push-to-talk button.

The problem: voice assistants are great at chatting, but bad at tasks like "check the weather in New York" or "rebook my flight." Text assistants (chatbots) are much better at those tasks because they can call tools — meaning they can query a database, check an API (a service that provides data), or run a multi-step plan.

The paper's idea is simple: split the job in two.

- A "frontend" handles the conversation: listening, speaking, interrupting politely, saying "one moment please."
- A "backend" handles the thinking and doing: calling tools, reading results, and writing the answer.

The frontend just needs to learn one skill: recognizing when help is needed and handing the question to the backend.

## Why does it matter?
Today you must choose between natural talk and smart actions.

Voice models that speak directly sound natural and fast. They keep the tone of voice, handle pauses, and let you interrupt. But on grounded customer-service tasks (tasks where the answer must come from real data, not guessing), leading voice models complete only about 31–51% of tasks, while a text agent completes about 85%. Noise and accents make the gap even bigger.

Teaching the voice model itself to do all the tool calls is costly. Sound takes up a lot of the model's memory and capacity (the paper calls this a capacity tradeoff: audio tokens consume modeling power that text-only models can spend on facts and reasoning).

Delegation fixes this. The voice model stays small and focused on talking, while the text backend — which already knows how to follow instructions, call tools, and plan over many steps — does the hard work. The design is modular (parts can be swapped): you can upgrade the backend to a bigger model without retraining the voice part.

## How does it work?
Imagine you ask: "What is the weather in New York?"

1. **The frontend listens.** It has three inputs: your speech sounds, a live written transcript of what you said (streaming ASR — Automatic Speech Recognition, turning speech into text as you talk), and its own planned reply text.

2. **It fires a handoff signal.** Instead of starting a normal reply, it writes a special marker called `<tc bos>` (tool-call begin). This replaces the normal "start talking" marker. About 320 milliseconds (a third of a second) after you finish, it says a short filler like "Give me a moment," then writes `<tc eos>` (tool-call end).

3. **It goes quiet and sends the text to the backend.** Your transcript, cut at the end-of-turn marker, goes to the backend. The frontend stays silent, filling its reply channel with placeholder tokens (pad tokens — "say nothing for now").

4. **The backend does the work.** The backend is built with LangGraph, a framework for tool-using agents, running a ReAct loop (Reason + Act: the model thinks, calls a tool, reads the result, and repeats until done). It keeps memory across turns, so follow-up questions still make sense. It can run many rounds of tool calls.

5. **The answer is pasted back in.** The backend's plain-language answer (for example, "The weather in New York is 72 degrees") is wrapped in markers `<pf bos>` / `<pf eos>` and "prefilled" (pasted) into the frontend's reply channel about one second after the handoff. The frontend is trained to simply repeat that text aloud, starting from its normal "start talking" marker.

6. **Safe fallback.** If the frontend raised the flag by mistake, or the backend returns plain text instead of a tool call, that text is still passed through as the answer. So the bigger backend covers for small frontend mistakes.

7. **Speech comes out.** The frontend connects to a streaming TTS (Text-To-Speech) voice that turns the repeated text into spoken audio, with support for starting and interrupting.

Training this took a lot of data: about 530k hours of pretraining, 111k hours of fine-tuning, plus 8.5k hours of tool-call conversations. Most tool-call dialogues were first written by text models, filtered by judge models, cleaned (math- and code-heavy chats removed), turned into speech with several voices, and quality-checked with speech recognition.

Results reported in the paper:

- The frontend correctly raises the handoff flag 92–97% of the time (97.2% on simple requests, 93.5% on the hardest mixed ones).
- It correctly says "no tool needed" about 81.2% of the time.
- On a speech version of BFCL (Berkeley Function-Calling Leaderboard, a standard test of calling the right tool with the right details), the system scores about 73–75% on average — close to GPT-realtime on some parts.
- On 100 recorded real-human conversations (Full-Duplex-Bench v3), it fulfills the request about 54–67% of the time, with 100% turn-taking (it never breaks the flow of who speaks when). A bigger backend helps.
- Adding tool-call skill barely hurts normal chat, recognition accuracy, or interruption handling.

## Where can this be used?
Anywhere you want to talk naturally and still get real things done:

- **Customer support by voice:** airline rebooking, retail returns, IT help — cases that need 6–8 database lookups in a row.
- **In-car or hands-free assistants:** you interrupt, hesitate, or correct yourself ("no, I meant Tuesday"), and it keeps listening while it talks.
- **Medical or HR front desks:** multi-turn forms where the assistant must ask follow-up questions, decide when a tool is allowed, and when to say "I cannot do that."
- **Upgradable products:** a company can ship one voice frontend and plug in a stronger backend later, or swap backends per domain (small fast one for simple queries, large one for travel planning).

## Conclusions & takeaways
- Do not force one model to do everything. Let the voice model own talking and the text model own doing.
- A tiny signal — two special markers — is enough to connect them. No big rebuild of the voice model is needed.
- Pasting the backend answer back and repeating it ("prefill-and-repeat") is a robust trick: even wrong handoffs degrade into a normal spoken answer.
- The approach scales: a bigger backend (for example Qwen3-235B, a large text model) gives better answers with no frontend retraining.
- Cost is small: turn-taking, speech recognition, and chat quality drop only slightly after adding tool-call training.
- The filler ("Let me pull that up") and backchannels ("Okay, I am here") are deliberate: they hold the turn while tools run and keep the user from hanging up.

## Jargon decoder
| Term | Plain meaning |
|---|---|
| Full-duplex | Both sides can talk and listen at once, like a phone call — no button to press |
| Frontend | The voice part: hears you, talks back, decides when to ask for help |
| Backend | The text part: calls tools, reads databases, writes the final answer |
| Tool call | Asking an outside service to do something, e.g. check weather or book a flight |
| ASR (Automatic Speech Recognition) | Turning spoken audio into written text, live as you speak |
| TTS (Text-To-Speech) | Turning written text into spoken audio |
| Delegation token (`<tc bos>` / `<tc eos>`) | Special begin/end markers meaning "this needs a tool — hand it over" |
| Prefill-and-repeat | Pasting the backend answer into the frontend so it reads it aloud word for word |
| ReAct agent | A loop of thinking then acting: reason, call a tool, read result, repeat |
| BFCL | A standard test that checks whether a model calls the right tool with the right details |
| Turn-taking | Managing who speaks when: pauses, interruptions, and smooth handoffs |
| Backchannel | Short listener sounds like "okay" or "I am here" that show attention without taking over |
