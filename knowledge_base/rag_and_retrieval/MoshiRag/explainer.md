> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# kyutai-labs/moshi-rag — In Plain Language

## What is this about?
MoshiRAG is a voice chatbot you can talk to and interrupt, like a phone call.
It is built on top of an existing speech model called Moshi.
The new trick is that it can quietly look things up while it keeps talking.
So it stays fast and natural, but gives answers that are more factual.
Think of a friend who keeps chatting while quickly glancing at notes.
The project lives in one repo with three parts.
There is a Python version for research and experiments.
There is a Rust version for faster, production-style use.
And there is a web page you talk through in the browser.

## Why does it matter?
Most voice assistants face an awkward trade-off.
Either they answer instantly but make things up,
or they look things up and leave you waiting in silence.
Nobody wants a long pause in the middle of a spoken conversation.
Even a three-second delay can make a voice bot feel broken.
MoshiRAG tries to remove that trade-off.
It keeps listening and speaking the whole time,
even while a lookup is running in the background.
That makes grounded, knowledgeable voice conversation feel normal instead of robotic.
It shows that factuality does not have to kill real-time flow.

## How does it work?
Think of it as two workers cooperating: a talker and a researcher.
The talker is the front end.
It is a full-duplex Moshi speech model that listens and speaks continuously.
The researcher is the back end.
It is a text-based lookup system that runs in parallel.
Here is the sequence in everyday terms:
1. You speak. The system transcribes your words with a streaming speech-to-text helper.
2. The talker also keeps an "inner monologue."
That is its own running text notes about the conversation.
3. When the talker realizes it needs facts, it raises a silent flag.
That flag is called a retrieval trigger token.
4. The combined notes plus your transcription are sent to the researcher.
The audio never pauses for this handoff.
5. While waiting, the talker fills the gap with light chatter.
That can be "let me check that" or a rough first answer.
6. The researcher returns a short reference text.
That text is encoded and streamed back into the talker.
7. The rest of the spoken answer is then shaped by that reference.
So the reply sounds continuous but is better informed.
Under the hood there are two cooperating programs.
One is the main speech server.
The other is a reference-text encoder service.
Released voices include a female synthetic voice called Moshika.
It ships in both PyTorch and Rust formats.
Running it yourself needs a strong GPU, around 24 GB.
A local lookup model is recommended so slow networks do not hurt quality.

## Where can this be used?
- Hands-free assistants that must answer factual questions out loud without long silences.
- Customer support phone lines.
There the agent can chat politely while order or account details load.
- Live tutoring or coaching tools.
They can acknowledge the student first, then explain with checked material.
- In-car or on-device voice helpers.
Interruptions and overlapping speech are normal there.
- Research labs experimenting with real-time speech.
The PyTorch side is set up for tinkering.
- Production voice products that need efficiency.
Those are served by the Rust side plus a web client.
- Demo and deployment setups.
The included web UI and container stack cover frontend, backend, and encoder.

## Conclusions & takeaways
- The core idea is simple: never stop the conversation just to do a lookup.
- Splitting "talking" from "researching" lets each side do what it is good at.
- A tiny trigger signal plus filler speech hides the delay that usually ruins voice search.
- Grounding comes from injected reference text.
There is no need to retrain the whole voice model for every new fact.
- The cost is complexity.
Multiple services, GPUs, transcription, and a fast lookup model must all run together.
- Delays still matter: slow lookups can hurt answer quality.
- If you remember one sentence, make it this:
MoshiRAG is Moshi that keeps chatting while a helper fetches the facts.

## Jargon decoder
| Term | Plain definition |
| --- | --- |
| Full-duplex | Both sides can talk and listen at the same time, like a phone call, not walkie-talkie turns. |
| Moshi / Mimi | The underlying real-time speech model and its audio codec; MoshiRAG adds lookup on top of them. |
| RAG (retrieval-augmented generation) | Looking up outside information first, then letting the model answer using it. |
| Front end | The speech model you directly talk to; it handles listening, speaking, and timing. |
| Back end | The helper running in parallel that receives conversation text and returns reference text. |
| Retrieval trigger token | A hidden signal the model emits when it decides "I need to look this up now." |
| Inner monologue | The model's running text notes about what is happening, used as context for lookup. |
| Streaming ASR | Software that turns your speech into text word-by-word as you speak. |
| Reference text encoder | A service that converts the looked-up text into a form the speech model can absorb mid-sentence. |
| Pre-RAG content | Small talk or partial answers spoken while waiting, so the pause feels natural. |
| bf16 weights | A compact number format for the model files that saves memory with little quality loss. |
| vLLM / OpenAI-compatible API | A standard way to run and query a text model locally or over the network for lookups. |
