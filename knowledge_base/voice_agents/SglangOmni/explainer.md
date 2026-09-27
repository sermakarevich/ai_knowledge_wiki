> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# sgl-project/sglang-omni — In Plain Language

## What is this about?
Think of a voice assistant that can listen, think, and speak back.

Most AI servers handle only one of those jobs well: either
understanding words, or generating speech. This project is the
"conductor" that runs the whole chain end to end.

You give it speech, text, or images. It hands the request through
a series of specialist steps — cleaning up the input, understanding
it, thinking of a reply, turning that reply into voice sounds, and
finally producing playable audio. Then it sends the answer back
through a familiar, standard interface.

It does not replace the fast text-thinking engine (called SGLang).
Instead, it sits around that engine and manages everything before
and after the thinking happens.

## Why does it matter?
Turning text into speech — or speech into text — is not one big step.

It is many small steps, and each step needs different tools.
Some steps are heavy number-crunching. Some are light cleanup work.
Some must stream results piece by piece so the user does not wait.

Without a coordinator, developers have to glue all of that together
by hand: start each step, move data between them, handle users
talking over each other, and keep delays low.

This project provides that coordinator out of the box.
Each step gets the right kind of manager for its workload, data
moves efficiently between steps, and developers get one simple
front door instead of five different systems to wire up.

The practical payoff is lower delay, smoother live voice chat,
and less custom plumbing for every new voice model.

## How does it work?
Imagine an assembly line with a smart foreman and fast conveyor belts.

1. **The assembly line.** A request flows through stations:
   tidy up the input, convert sound or images into a form the
   computer understands, think up the reply, shape the voice,
   turn it into sound waves, and package the final answer.

2. **The right manager per station.** The thinking station reuses
   the high-speed SGLang engine. Lighter stations use simpler,
   faster loops. Busy streaming stations keep flowing without
   waiting for the whole answer to finish.

3. **Foreman plus conveyor belts.** One control layer tracks who
   asked for what and where each request is. A separate data layer
   carries the heavy sound-and-number payloads between stations
   using fast transfer methods, depending on the hardware.

4. **One familiar front door.** From the outside it looks like a
   standard chat-and-audio service: ask a question, request speech,
   upload a voice sample, or send audio for transcription.
   A router spreads incoming work across multiple workers and
   reports health and capabilities.

5. **Runs where you have hardware.** The main supported setup is
   NVIDIA graphics cards. There are early, experimental paths for
   Apple Silicon Macs and Intel graphics cards for selected models.

## Where can this be used?
- **Talking assistants:** a user speaks, the system replies in text,
  in voice, or both — like customer support bots or in-car helpers.
- **Reading text aloud:** turn articles, messages, or book chapters
  into natural-sounding audio, one clip at a time or in batches.
- **Live voice with low waiting:** stream the spoken reply while it
  is still being built, so conversations feel immediate.
- **Custom voices:** upload a short voice sample and have new
  sentences spoken in a similar voice.
- **Writing down meetings and calls:** convert recordings into text,
  including experimental setups that label who spoke and when.
- **Making songs from words:** supply lyrics plus a style description
  and get back a stereo music track.
- **Research and production teams:** groups adding new voice models,
  speeding up delivery between steps, or running many workers
  behind one endpoint.

## Conclusions & takeaways
The core idea is simple: voice AI is a team effort, not a solo act.

This project organizes the team. It owns the lineup of steps, starts
and stops them, moves data between them quickly, and presents one
clean interface to the outside world. It leaves the pure text-thinking
part to the engine that already does it best.

If you remember three things: it splits voice work into specialist
stages, it matches each stage with the right scheduler, and it keeps
the whole pipeline talking over fast transport behind a standard API.

That combination is what lets one system cover chat, speech creation,
music, transcription, and live streaming without rebuilding the
plumbing each time.

## Jargon decoder
| Term | What it means in plain language |
|------|----------------------------------|
| Serving runtime | The program that stays on, takes requests, and returns answers |
| Pipeline / stages | The step-by-step assembly line a request travels through |
| Encoder | The step that turns raw sound or images into computer-friendly notes |
| Autoregressive engine | The thinker that writes the reply one piece at a time |
| Talker / decoder / vocoder | The steps that turn a reply into voice sounds, then into playable audio |
| Scheduler | The manager deciding whose work runs next at each station |
| Control plane | The foreman tracking requests and telling stations what to do |
| Data plane / relay | The conveyor belts carrying heavy audio and number payloads |
| OpenAI-compatible endpoint | A front door shaped like a widely used standard, so existing tools plug in |
| Router | The receptionist spreading visitors across many workers |
| CUDA / XPU / MPS | Names for running the math on NVIDIA cards, Intel cards, or Mac chips |
