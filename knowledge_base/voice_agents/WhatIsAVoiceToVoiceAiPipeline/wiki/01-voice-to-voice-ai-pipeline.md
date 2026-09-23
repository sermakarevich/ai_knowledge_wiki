> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Voice-to-Voice AI Pipeline — Emotion and Low Latency

**In one sentence:** The classic voice-input → speech-to-text → LLM → text-to-speech → speaker pipeline strips out the caller's emotion when voice is flattened to text, so the chunk argues for a voice-to-voice pipeline (encoder → adapters → LLM → vocoder operating on voice vectors) that preserves emotion and lowers latency, built on models like Llama Omni rather than GPT, at the cost of lower tool-calling accuracy and less prompt control.

## Key points
- The old pipeline has four stages: voice input goes to speech-to-text, then to an LLM, then to text-to-speech, then out of the speaker for the user to hear.
- Converting voice to text loses emotion: if a user speaks with sadness or anger, the transcription carries the words but the LLM never sees the tone, so it cannot respond with the right feeling.
- A bolt-on emotion-detection library does not fix this because it works on the transcription, while the actual tone lives in the user's voice, not in the text.
- The proposed voice-to-voice pipeline feeds voice in as voice and returns voice out, carrying both meaning and emotion plus a narrative of what the LLM should respond and in which emotion.
- The pipeline has four modules — encoder, modality adapters, LLM, vocoder — where the encoder turns raw audio into voice/data vectors (meaning + emotion + tone + speed) instead of text, adapters shrink the long encoder vectors to an LLM-compatible length, the LLM takes voice vectors plus prompt and outputs voice vectors, and the vocoder turns those vectors back into speech.
- It requires a voice-vector-capable LLM: OpenAI GPT models cannot be used because their weights are closed and the input type cannot be changed, so the chunk uses Llama Omni models, which accept voice vectors as input (GPT models might accept them in the future).
- The two stated benefits are low latency and emotions passed through the pipeline, making the exchange feel natural like human-to-human instead of robotic.
- The stated limitations are less accuracy in tool calling and less control of the prompt, which is why the chunk says almost all real-world use cases seen so far still deploy STT → LLM → TTS.

---

## The old pipeline: STT → LLM → TTS

The chunk recaps the pipeline from the previous video: voice input → speech-to-text → LLM → text-to-speech → speaker output the user hears. In that flow the voice is converted into text and then text back into voice.

| Stage | Function in chunk |
|---|---|
| Speech-to-text | Turns voice input into text |
| LLM | Reasons over the text |
| Text-to-speech | Turns the LLM text back into voice output |

Speaker self-introduction (verbatim, as transcribed): "Hi myself Nishant. I'm CTO and co-founder at cudist. In this video I will walk you through the voice pipeline which is a voiceto voice pipeline."

## The problem: text strips emotion

Human-to-human connection is emotionally carried: the listener understands tone, emotions, and what the speaker wants to say. The chunk's claim is that every voice AI agent it has seen converts voice into text and text back into voice, and that flattening drops what the user felt in the sentence.

Concrete example given: a user says "Hi, I want to talk to Mark" spoken in anger (transcribed variants: "Hey, I want to talk to Mark"). Previously converted into text, the LLM does not understand the emotion behind it.

Verbatim problem statement: "whenever a voice that comes in and that it converts into text we lose the emotions."

## The solution: voice in, voice out

Instead of voice → text → voice, feed voice as input into the LLM as voice and produce voice as output. The chunk calls this a "voicetooice pipeline" and says it solves latency and emotion understanding, including which emotion the output should carry, so the exchange is more natural — "how one user speaks to another."

## How it works: encoder → adapters → LLM → vocoder

The chunk says there are four modules total: encoder, modality adapters, LLM, and vocoder (transcribed as "walkoder"/"walker"). The encoder is presented as the speech-to-text analogue and the vocoder as the text-to-speech analogue, except nothing is converted into text anymore.

Flow for the example utterance:

1. **Encoder:** raw audio comes in and is converted into vectors — "voice vectors" / "data vectors" — that carry emotions, meaning (what the user is trying to say), tone, and speed.
2. **Modality adapters:** the encoder vectors are normally long/high in length, so adapters convert them into a smaller, LLM-compatible length before feeding them to the model (they can also go directly into the LLM).
3. **LLM:** input is voice vectors plus prompt; output is voice vectors (described as "text or I would say voice vectors").
4. **Vocoder:** converts the output voice vectors into speech the user hears.

Recap given in the chunk: voice comes into the encoder, its length is converted to what the LLM accepts, the LLM takes voice vectors plus prompt and returns voice vectors, and the vocoder turns those into speech.

## Llama Omni vs GPT

The chunk asks whether the same LLM used in the voice-to-text/text-to-voice pipeline can be reused, and answers no — a different kind of LLM is needed, one that accepts voice vectors as input. Because OpenAI GPT models are closed-weight with no modification options for the input type, they cannot take voice vectors; Llama Omni models are presented as specifically voice-to-voice models that can. The chunk notes GPT models might accept voice vectors in the future.

## Benefits and limitations

Benefits stated: (1) low latency, (2) emotions being passed through the pipeline. The LLM input being voice vectors plus prompt is explicitly confirmed ("does this LLM can accept our prompt? Yes").

Limitations stated: less accurate in tool calling, and less control of the prompt. The chunk says that in the real world almost all use cases seen so far still run text-to-STT/LLM/text-to-speech (i.e. STT → LLM → TTS), which can be replaced by voice-to-voice except where tool calling and prompt control matter. It closes with the pros/cons framing of when to use and when not to use a voice-to-voice pipeline, plus an offer to help build voice AI pipeline/infrastructure via a consultation call link.

**Covers:** Voice-to-voice vs STT-LLM-TTS pipeline, encoder→adapters→LLM→vocoder flow, voice vectors preserving emotion, latency benefits, Llama Omni vs GPT limits, tool-calling accuracy trade-offs.
