# AstraTTS

**Article:** [AstraTTS](https://github.com/Blackwood416/AstraTTS) — GitHub

## Human Readable TL;DR

AstraTTS is like a pocket recording studio that turns text into spoken voice on your own computer, with no cloud needed. Think of it as swapping a slow, general-purpose kitchen blender (plain Python inference) for a tuned espresso machine (ONNX Runtime with CPU optimizations) that can brew many cups at once through an inference pool. It starts playing audio almost instantly, like a video that streams while it downloads, and comes with a simple web dashboard for managing voices and models, much like a music library app. It runs on Windows, Linux, macOS, and Docker, speaking Chinese mixed with English or Japanese.

## TL;DR

AstraTTS is an ONNX Runtime-based, cross-platform text-to-speech engine with CPU-optimized inference, an inference pool for multi-channel concurrent synthesis, and millisecond-level streaming output with play-while-synthesizing. It ships a WebUI for voice management, model conversion, and parameter tuning with hot-reloadable YAML configuration, plus a CLI with platform-native low-latency playback. The default V1 engine (based on Genie-TTS) is stable and recommended, supporting Chinese/English and Chinese/Japanese bilingual mixed reading and V2ProPlus model cloning with deterministic generation, while the V2 engine (based on GPT-SoVITS-Minimal) is experimental, Chinese/English only, but adds TopK, temperature, and noise-scale sampling. Deployment covers native Windows bundles, Linux tarballs, macOS DMG/tarballs (V1 engine only), and Docker, with core resources distributed via GitHub Releases rather than Git LFS and a .NET 10 build environment.

---

## Problem & Motivation

Running high-quality neural text-to-speech locally is often slow, hard to deploy across platforms, and awkward to manage when multiple synthesis requests arrive at once. Traditional Python inference stacks leave multi-core CPU performance on the table, introduce noticeable first-audio latency, and typically lack an approachable way to organize voices, convert models, and tune parameters without restarting the service. AstraTTS is motivated by the desire for a fast, concurrent, cross-platform TTS server that starts speaking almost immediately, keeps configuration live, and gives non-expert users a visual control panel while still offering headless and CLI operation for servers and automation.

## Main Original Ideas

1. **ONNX Runtime CPU-optimized inference core:** the engine is built around ONNX Runtime with deep CPU instruction-set tuning, presented as far faster than conventional Python inference, and organized into the AstraTTS.Core SDK with a hybrid G2P engine plus RoBERTa and HuBERT feature extractors feeding per-version inference engines.

2. **Inference pool for concurrent synthesis:** a built-in inference pool spreads multi-channel synthesis across multi-core CPUs, so parallel requests and the V2ProPlus parallel model loading path can be served concurrently rather than queueing behind a single session.

3. **Millisecond-level streaming with hot-reloadable service:** streaming output delivers very low first-packet latency so playback begins while synthesis continues, while the YAML-based configuration takes effect at runtime without restarts, and the WebUI bundles synthesis lab, voice library, control center, and model converter views with light and dark themes.

4. **Dual-engine strategy with pragmatic platform matrix:** V1 is kept as the stable default with bilingual mixed reading and deterministic generation, V2 is carried as an experimental sampling-capable alternative, and platform support is mapped honestly to engine maturity, with macOS restricted to V1, Linux audio falling back across PipeWire, PulseAudio, and ALSA backends, and Docker offered as the recommended server deployment with regional mirrors.

## Key Findings

The project reports that the combination of ONNX Runtime optimization and the inference pool yields high-throughput concurrent synthesis on ordinary multi-core CPUs without GPU dependence. Streaming plus hot-reload makes the service feel interactive: audio starts in milliseconds and tuning does not interrupt serving. The V1 engine covers the stable production path including Chinese/English and Chinese/Japanese mixed reading and V2ProPlus voice cloning, while V2 remains a work-in-progress that trades language coverage for sampling controls. Recent releases consolidated real deployment lessons, adding macOS support via a community contribution, native Docker images, one-click WebUI config reset, Linux audio backend fallback, and a move of large core resources off Git LFS onto GitHub Releases with a flattened, versioned resource layout.

## Suggestions & Future Directions

The wiki itself flags trilingual mixed reading as still in development and V2 as experimental with Chinese/English only, so completing three-language mixing and hardening V2 toward parity are natural next steps. Enabling V2 and V2ProPlus on macOS, widening sampling and prosody controls on the stable engine, and adding quantitative latency, throughput, and quality benchmarks would make engine choice and capacity planning more evidence-based. On the operations side, prebuilt resource verification, slimmer default bundles, and richer headless observability for the inference pool would further help server and Docker adopters.

## Authors & Institutions

AstraTTS is an open-source project hosted at Blackwood416/AstraTTS under the MIT License. It builds on Genie-TTS for the V1 core architecture, GPT-SoVITS and GPT-SoVITS-minimal-inference for the V2 algorithm lineage, ONNX Runtime for inference, NAudio and wasapi_relink for .NET audio and low-latency playback, and a built-in default model sourced from BreakingBad (AI-Hobbyist). macOS support arrived via contributor Domination888 in PR #3.
