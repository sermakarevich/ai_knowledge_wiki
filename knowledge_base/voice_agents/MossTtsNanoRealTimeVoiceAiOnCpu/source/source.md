# MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini - Firethering
Source: https://firethering.com/moss-tts-nano-open-source-tts/
Kind: article
Fetched: 2026-09-22T08:37:05.369710+00:00
Tool: urllib
PDF: https://firethering.com/moss-tts-nano-open-source-tts/ (no source.pdf in run work dir; original article URL pinned here)

MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini - Firethering

back to top

Home

Softwares

AI Tools

DevTools

3D Tools

Design Tools

Image Editors

Video Editors

Productivity

Utilities

Apps

Android Apps

iOS Apps

Games

Windows Games

macOS Games

Android Games

iOS Games

Tech

Picks

AI Picks

AI Models

Trends

Newsletter

Search

Monday, September 21, 2026

Home

Softwares

AI Tools

DevTools

3D Tools

Design Tools

Image Editors

Video Editors

Productivity

Utilities

Apps

Android Apps

iOS Apps

Games

Windows Games

macOS Games

Android Games

iOS Games

Tech

Picks

AI Picks

AI Models

Trends

Newsletter

Facebook

Instagram

Twitter

Vimeo

Youtube

Home

Softwares

AI Tools

DevTools

3D Tools

Design Tools

Image Editors

Video Editors

Productivity

Utilities

Apps

Android Apps

iOS Apps

Games

Windows Games

macOS Games

Android Games

iOS Games

Tech

Picks

AI Picks

AI Models

Trends

Newsletter

Search

HomeTechMOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling...

# MOSS-TTS-Nano: Real-Time Voice AI on CPU, Part of an Open-Source Stack Rivaling Gemini

ByMohit Geryani

April 15, 2026

0

Last updated:April 15, 2026

Share

Facebook

Twitter

Pinterest

WhatsApp

- Advertisement -

Most text-to-speech AI fall into two camps. The ones that sound good need serious hardware. The ones that run on anything sound robotic. MOSS-TTS-Nano is trying to be neither.

It’s a 100 million parameter model that runs on a regular CPU and it actually sounds good. Good enough that the team behind it built an entire family of speech models around the same core technology, one of which has gone head to head with Gemini 2.5 Pro and ElevenLabs and come out ahead on speaker similarity.

It just dropped on April 13th and it’s the newest addition to the MOSS-TTS family, a collection of five open source speech models from MOSI.AI and the OpenMOSS team. The family doesn’t just cover lightweight local deployment. One of its models MOSS-TTSD outperforms Gemini 2.5 Pro and ElevenLabs on speaker similarity in benchmarks. Another generates voices purely from text descriptions with no reference audio needed. And one is built specifically for real-time voice agents with a 180ms first-byte latency.

Nano is the entry point. The family is the story.

## Table of Contents

## Meet the Family

The MOSS-TTS family isn’t five versions of the same thing. Each model was built for a different problem and they’re genuinely distinct from each other.

MOSS-TTS is the flagship. It’s the one you reach for when you need the best voice quality zero-shot voice cloning, long-form speech that stays stable across minutes, fine-grained control over pronunciation. It comes in two sizes, 8B and 1.7B, and it’s what most benchmarks in this family are measured against.

MOSS-TTSD is the dialogue model. Two speakers, back and forth, with natural pacing and expressiveness that makes it sound like an actual conversation. This is the one that beat Gemini 2.5 Pro and ElevenLabs. More on that later.

MOSS-VoiceGenerator does something none of the others do. You describe a voice in plain text like age, tone, accent, character and it creates one from scratch. No reference audio needed. You’re designing a voice the way you’d describe a character.

MOSS-TTS-Realtime is built for voice agents. The kind that need to respond in under half a second and stay coherent across a full conversation. It hits 180ms time-to-first-byte after warmup which in voice agent terms is genuinely fast.

MOSS-SoundEffect is the odd one out in the best way. It generates environmental audio like rain, traffic, crowd noise, mechanical sounds from text descriptions with controllable duration. Useful for anyone building games, videos, or interactive experiences who doesn’t want to dig through royalty-free sound libraries.

Five models, one shared audio backbone, all Apache 2.0. You can use any of them independently or chain them together depending on what you’re building.

MOSS-TTS Family

## MOSS-TTS-Nano: The One That Changes the Access Problem

MOSS-TTS-Nano Demo

The access problem in local TTS has always been the same, the models worth using require hardware most people don’t have. An 8B model sounds great but it needs a GPU with enough VRAM to load it. That immediately rules out a huge chunk of people who’d otherwise use it.

Nano sidesteps this completely. At 100M parameters it’s small enough to run on 4 CPU cores and still stream audio in real time. That means a developer building a local app doesn’t need to spec their users’ machines around a GPU requirement. A researcher testing something doesn’t need to spin up cloud compute. Someone who just wants local voice AI on a modest laptop can actually have it.

The audio quality is 48kHz stereo,  higher than most TTS models output by default. It supports 20 languages including Chinese, English, Arabic, Japanese, Korean and more. Voice cloning works with a reference audio file and handles long text automatically by chunking it without you having to manage that yourself.

Setup is straightforward. Clone the repo, install requirements, point it at a reference audio file and give it text. There’s a CLI, a local web demo via FastAPI, and a Python API if you want to integrate it into something.

MOSS-TTS-Nano

## Running Light, Building Fast

The 8B flagship model fits on an 8GB GPU and if you don’t have one, there’s a fully torch-free path using llama.cpp for the backbone and ONNX Runtime for the audio tokenizer. No PyTorch installation required at all.

The llama.cpp path has four ready-made configs depending on your setup. Default ONNX, TensorRT for maximum throughput, a low-memory mode specifically tuned for 8GB GPUs, and a fully CPU-only option with no GPU involved whatsoever. You pick the one that matches your machine and go from there.

The community hasn’t been waiting around either. There’s already a ComfyUI extension for anyone who lives in that workflow. An OpenAI-compatible TTS API wrapper so you can drop MOSS-TTS into anything that already speaks to OpenAI’s audio endpoints. AnyPod, a podcast generation tool that uses MOSS-TTS and MOSS-TTSD as its backend. And a Norwegian LoRA adapter fine-tuned on the NST Norwegian speech dataset, contributed by a developer at Tosee, which tells you something about how quickly people are taking this and running with it.

A model that ships with this many entry points and already has community tooling two months in is worth paying attention to.

MOSS-TTS Github

## The Number Worth Knowing

Benchmarks in AI are easy to dismiss. Every model release comes with numbers that somehow make it look better than everything else. So when I say MOSS-TTSD-v1.0 beat Gemini 2.5 Pro on speaker similarity, I want to be specific about what that actually means.

On English speaker similarity, MOSS-TTSD scored 0.7893. Gemini 2.5 Pro scored 0.6786. That’s a open source dialogue model outperforming one of Google’s best on the metric that matters most for multi-speaker audio – does it actually sound like the right person is talking.

ElevenLabs V3 came in at 0.6730 on the same test. MOSS-TTSD beat that too.

For Chinese, it scored 0.7949 on speaker similarity against Doubao Podcast’s 0.8034, close enough that the gap is essentially a coin flip in practice.

These are the team’s own evaluations so treat them as self-reported. But the methodology is documented, the benchmark is public, and the numbers are specific enough to be meaningful.

ModelEN SIMZH SIM

MOSS-TTSD-v1.00.78930.7949

Gemini 2.5 Pro0.6786—

ElevenLabs V30.67300.6970

Doubao Podcast—0.8034

Related: Open-Source TTS Models That Can Clone Voices and Actually Sound Human

## Which One Is Right for You

That depends on what you’re actually trying to do. Just want to try local voice AI today without worrying about your hardware? Start with Nano. It runs on whatever you have, setup takes minutes, and the demo is live on Hugging Face right now if you want to hear it before installing anything.

Building something that needs the best voice quality and you have a GPU to work with? The 8B MOSS-TTS flagship is the one. GGUF weights are ready, llama.cpp path works, and an 8GB GPU is enough with the low memory config.

If you need two voices having a natural conversation. MOSS-TTSD is what you want and the benchmark numbers suggest it’s the strongest open source option in that specific space right now.

Want to create a completely new voice from a text description without any reference audio at all? MOSS-VoiceGenerator does exactly that and nothing else in this family does it.

For a live voice agent that needs to respond fast and stay consistent across a full conversation? MOSS-TTS-Realtime was designed for that problem specifically.

All five models are on Hugging Face and ModelScope. The main repo is on GitHub under OpenMOSS. The whole family is Apache 2.0,  build, fine-tune & use commercially. A family this complete, this accessible, and this honest about what each model is for doesn’t come around often. Worth bookmarking even if you don’t need it today.

Want more stories worth your time?

Add us to your Google favorites. We cover the tech stories, AI developments, and open-source projects that are easy to miss in the noise.

Please leave this field empty

## Don’t miss any Tech Story

### Subscribe To Firethering NewsLetter

Email Address *

You Can Unsubscribe Anytime! Read more in our privacy policy

Check your inbox or spam folder to confirm your subscription.

Tags

AI

AI Models

TTS

### LEAVE A REPLY Cancel reply

Comment:

Please enter your comment!

Name:*

Please enter your name here

Email:*

You have entered an incorrect email address!

Please enter your email address here

Website:

YOU MAY ALSO LIKE

### Everyone Agrees the AI Race Needs to Slow Down. But Can Anyone Do It?

Mohit Geryani-September 13, 20260

Anthropic CEO Dario Amodei says frontier AI needs to be paced, and Sam Altman agrees. But can companies and countries actually slow the AI race?

### Anthropic Researchers Fear the AI Race Could Cause Human Extinction

Mohit Geryani-September 9, 20260

An Anthropic researcher just resigned because he believes the AI race could end in human extinction.
Jacob Coxon spent three years working on pretraining research at OpenAI and Anthropic. In his resignation post, he accused both companies of racing toward self-improving superintelligence while gambling with consequences that could affect everyone.
That alone would make for a remarkable resignation.
Then Evan Hubinger joined the conversation.
Hubinger leads Alignment Science at Anthropic. He publicly agreed with Coxon's warning and said researchers at the company genuinely believe AI could kill all humans.
He also made a much more uncomfortable admission: Anthropic is trying to solve the problem, but he doesn't believe they yet have a plan for aligning superintelligence, or that they're clearly on track to do it.
So why keep building?
The answer has less to do with whether these researchers understand the risks and more to do with what happens when every major lab knows the others are still moving forward.
To see why that can become a trap, we first need to understand what they're actually worried about.

### Tired of Being a Tenant in Your Own PC? These 7 Open Source Tools...

Mohit Geryani-September 9, 20260

Tired of feeling like a tenant on your own PC? These 7 open source tools add missing features of your OS, fix everyday annoyances and give you more control.
