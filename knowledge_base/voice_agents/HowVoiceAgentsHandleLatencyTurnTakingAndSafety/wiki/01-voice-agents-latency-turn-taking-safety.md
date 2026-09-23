> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# When We Turn Text Into Speech: Voice-Agent Pipeline, Latency, Turn-Taking, and Safety
**In one sentence:** A voice agent turns speech into text, reasons with a text LLM, and speaks the answer back with expressive TTS, while perceived latency is managed with audio cues, intelligent turn-taking, tunable speed/expressiveness tradeoffs, streaming-or-blocking safety guardrails, and fast-router-to-sub-agent delegation.
## Key points
- The pipeline is speech → text via speech-to-text, reasoning and output text via a text-based LLM, then text → speech on the other side.
- Expressive TTS lets the LLM laugh, whisper, and add expressiveness so the voice sounds human-like rather than robotic — sometimes indistinguishable from a real person when just listening.
- The LLM accounts for about 40 to 70% of pipeline latency, and pushing expressiveness can add latency artifacts that make speech sound more hesitant than intended.
- Latency is treated as perceived: background presence (office noise, music) signals the connection has not dropped, and tool-calling is narrated ("I'm gonna look you up in the system") plus audio cues such as keyboard clicking while work happens.
- Turn-taking is currently either-you-talk-or-I-talk, but the speech-to-text layer distinguishes affirmations ("yeah, yeah, okay") from real intent to interrupt so backchannels do not cut the agent off.
- The general tuning rule is that the faster the stack is made, the less expressive or less correct it becomes.
- Safety uses a second LLM standing on the side that cuts the conversation off if it goes off the rails (e.g. a banking agent must not give financial advice), in either streaming mode (audio passes through, cut on violation) or blocking mode (everything verified before audio), where blocking is safer but adds more latency.
- Routing and SDKs are layered for fit: a fast low-intelligence model (e.g. a secretary router) can delegate to a higher-capacity sub-agent with the same or a different voice, and the SDKs cascade from a universal platform-agnostic JavaScript library to a React package (hooks, provider) to a React Native package (audio input), with headless or prebuilt UI/chat-bubble options.
---
## What a voice agent is
**Covers:** definition of the voice-agent experience and pipeline

You open up a conversation using your voice to have a conversation with a machine. On a slightly more technical level, you take speech, turn it into text using speech-to-text, then a text-based large language model reasons over what was said and generates output text that gets turned into speech again on the other side.

## Expressive text-to-speech
**Covers:** LLM expressiveness, human-likeness, uncanny valley, identity disclosure

Something special about the platform is that when text is turned into speech, the text model is allowed to express itself: it can laugh, whisper, or add more expressiveness, so it does not sound as robotic and is very expressive and human-like — described as "pretty uncanny." The speaker notes sometimes receiving support tickets where, just from listening, they cannot tell who is the real person and who is the agent.

| Claim | Detail from chunk |
|---|---|
| Expressive controls | laugh, whisper, "more expressiveness" |
| Effect | does not sound robotic; very expressive and human-like |
| Uncanny-valley note | so almost-human it can feel creepy; latency artifacts remain depending on expressiveness |
| Hesitation artifact | more expressive settings can make speech sound more hesitant than wanted, which itself "starts bearing meaning" |

On disclosure, the chunk states there are security/safety guidelines around prompting: if somebody asks "are you a robot? Are you an agent, or are you human?", it should declare itself as non-human, and the product has safety guidelines and verification against trying to impose as a human. A longer latency can even be preferable so the agent is not pretending to be human.

Verbatim quotes:
- "when we turn text into speech, we also allow the text model, the LLM, to express itself."
- "if somebody asks, are you a robot? Are you an agent, or are you human? It should declare itself as non-human"

## Latency: perceived latency and audio cues
**Covers:** latency as the major pain point; perceived-latency mitigations

Latency is called the major pain point of voice agents/models, and the framing given is "latency is perceived." Mitigations named:

- Keep presence audible (e.g. office background noise or music on a call) so the user hears the connection has not dropped.
- Narrate slow work: when the agent does a task that takes time such as tool calling, it can say "oh, I'm gonna look you up in the system" plus play cues like keyboard clicking to convey that something is happening, so the user does not repeat themselves and gets feedback along the way.

Exact number: the LLM takes about 40 to 70% of the pipeline in terms of latency.

Verbatim quotes:
- "latency is perceived, right?"
- "you wanna make sure for the user that the connection is not dropped"

## Turn-taking and interruption handling
**Covers:** turn-taking algorithm; affirmation vs interruption intent

The described model is a turn-taking algorithm where either the user talks or the agent talks; users can speak while the agent talks without necessarily interrupting it. The speech-to-text layer is expected to know the difference between affirming what the agent is saying ("yeah, yeah, okay") and actually taking the turn, so a naive cutoff ("too stupid in that sense") does not interrupt the agent when the user only meant to affirm. The chunk frames this as being more intelligent about what the user's intent actually is when they speak.

## Tunability: speed vs expressiveness, guardrails, and routing
**Covers:** tunable parameters; streaming vs blocking safety; router plus sub-agent delegation

General rule stated: across speech-to-text, LLM, and text-to-speech, the faster you make it, the less expressive or the less correct you make it.

| Mechanism | How it works in the chunk | Latency/safety note |
|---|---|---|
| Sidecar guardrail LLM | A second LLM stands on the side and cuts the conversation off if it goes off the rails (example: banking service must not give financial advice) | Architectural choice: streaming vs blocking |
| Streaming mode | Lets audio through and cuts if it hears something it should not | Lower added latency |
| Blocking mode | Everything is verified before it goes into audio | Safer; adds more latency |
| Router + sub-agent | A low-intelligence fast model (e.g. a secretary that routes callers) delegates into another sub-agent with more brain capacity; voice can stay the same or change (e.g. a tonality/authority break when moving to loan advice) | Fit model cost and latency to the use case |

Verbatim quotes:
- "In general, the faster you make it, the less expressive or the less correct you make it, right?"
- "One adds more latency than the other. So all of these are tunable, right?"

## SDKs and platform surface
**Covers:** open API spec and code generation; layered JS/React/React Native SDKs; headless vs UI components; speech engine tiers

- The team is heavy on code generation with an open API spec covering the entire API surface, used to generate the server-side SDK surface — offered as a pattern to copy.
- Layered SDK architecture: a universal call JavaScript library that is platform- and framework-agnostic, then a React package on top implementing React paradigms (hooks, provider), then a React Native package that injects React-Native-specific audio input capabilities — a cascading core → framework-specific → platform-plus-framework-specific pattern also previously used at MongoDB/Realm.
- UI options: a headless option where you bring your own UI, plus UI components including an agent view and an embeddable chat bubble.
- Platform tiers: the fully integrated ElevenLabs Agents platform; standalone services where you bring your own text-to-speech, speech-to-text, and LLM; and a middle "speech engine" tier where you only bring the brain and the rest is handled by the platform — described as exceptionally good when you already have a text chat and just want to give it a voice.
- Scale/next goal stated in the chunk: ElevenLabs has 400 people with internal research shipping features and verticals; the speaker's goal is to be more agentic in keeping many SDKs aligned with feature parity, including generating the specification from the implementations and comparing across SDKs to converge the experience ("vibe alignment").
