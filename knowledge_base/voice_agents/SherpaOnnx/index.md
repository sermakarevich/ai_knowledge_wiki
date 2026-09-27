---
type: index
title: k2-fsa/sherpa-onnx
description: Folder index for the sherpa-onnx offline speech toolkit: 12 local speech functions on ONNX Runtime across chips, OSes, and 12 programming languages, built by one CMake core with per-target scripts.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-22T17:38:17Z'
sources:
  - id: original
    resource: https://github.com/k2-fsa/sherpa-onnx
  - id: local-copy
    resource: source/source.md
tags: [offline-speech, onnx-runtime, text-to-speech, edge-inference]
---
# k2-fsa/sherpa-onnx

sherpa-onnx is a C/C++ core plus per-target build scripts that run twelve speech functions fully offline on ONNX Runtime across desktop, mobile, embedded, and WebAssembly targets. This folder captures that snapshot at version 1.13.8, from function and platform scope to the CMake options and cross-compilation matrix that ship it. Start with the summary for the big picture, then use the digest and wiki pages for verbatim, citable detail.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, architecture, build pipeline, and key files.
2. Read `digest.md` (~10 min) for the verbatim per-chunk key points plus the system in five moves.
3. Go deep in the `wiki/` pages for full tables and excerpts, then use `explainer.md` for plain-language background, `critical_thinking.md` for scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — overview, architecture, build pipeline, key files, dependencies, and limitations.
- [Digest](digest.md) — verbatim key points per chunk plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the offline speech toolkit.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, new vs. repackaged, gaps, and verdict.
- [Questions](questions.md) — 7 retrieval-practice questions covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md (repo root: supported functions, platforms, languages, Flutter/Tauri frameworks, NPUs, introduction, Huggingface Spaces links, truncated Android APK links) |
| [02-top-level-files](wiki/02-top-level-files.md) | `.clang-format`, `.clang-tidy`, `.flake8`, `.gitignore`, `CPPLINT.cfg`, `CMakeLists.txt` (visible part only; truncated at chunk line 4759), `build-aarch64-linux-gnu.sh`, `build-android-{arm64-v8a,armv7-eabi,x86-64,x86}.sh`, `build-arm-linux-gnueabihf.sh`, `build-axcl-linux-aarch64.sh`, `build-axera-linux-aarch64.sh`, `build-flutter-web-wasm.sh`, `build-ios{,-no-tts,-shared,-shared-sherpa-with-static-onnxruntime}.sh`, `build-macos{,-shared,-shared-sherpa-with-static-onnxruntime}.sh`, `build-ohos-{arm64-v8a,armeabi-v7a,x86-64}.sh`, `build-riscv64-linux-gnu{,-spacemit}.sh`, `build-rknn-linux-aarch64.sh`, `build-wasm-simd-{asr,kws,nodejs,speaker-diarization,speech-enhancement,tts,vad,vad-asr,web}.sh`, `jitpack.yml`, `MANIFEST.in`, `new-release.sh`, `OPENVINO.md`, `Package.swift`, `release.sh` |

## Original Source

- Upstream: <https://github.com/k2-fsa/sherpa-onnx>
- Local copy: [source/source.md](source/source.md)
