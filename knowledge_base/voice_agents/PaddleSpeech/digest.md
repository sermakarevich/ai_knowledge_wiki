> [[index|Wiki]] | [[summary|Summary]]
# PaddlePaddle/PaddleSpeech — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** PaddleSpeech is an open-source PaddlePaddle-based toolkit for speech and audio tasks (ASR, TTS, translation, speaker verification, and more) with training, inference, and deployment support.
## Key points
- PaddleSpeech is an open-source toolkit on the PaddlePaddle platform for speech and audio tasks using state-of-the-art models (README.md:38).
- The project won the NAACL2022 Best Demo Award with paper at `https://arxiv.org/abs/2205.12007` (README.md:40).
- Demonstrated tasks include Speech Recognition (EN/ZH examples, README.md:58, README.md:65), English-to-Chinese Speech Translation (README.md:88), Text-to-Speech in multiple languages/dialects (README.md:106, README.md:113, README.md:134, README.md:141), and Punctuation Restoration (README.md:165-README.md:166).
- Stated vision is easy-to-use, efficient, flexible, scalable implementation empowering industrial application and academic research across training, inference/testing, and deployment (README.md:176).
- Entry points for quick start are CLI, Server, and Streaming Server, plus production-ready streaming ASR and streaming TTS systems (README.md:177, README.md:179).
- The Chinese frontend is rule-based with Text Normalization and G2P including polyphone and tone sandhi plus self-defined linguistic rules (README.md:180).
- Task coverage spans ASR, TTS synthesis, Speaker Verification, Keyword Spotting, Audio Classification, and Speech Translation, integrated with mainstream datasets such as LibriSpeech, LJSpeech, AIShell, and CSMSC (README.md:182-README.md:183).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The repository root files define code style, linting, git/CI automation, documentation builds, packaging includes, and the project's Chinese README landing page.
## Key points
- `.clang-format` pins C++ formatting to Google style with 4-space indent and C++11 standard (`.clang-format:25-32`).
- `.flake8` caps Python lines at 120 chars, checks only `*.py`, and selects `E, W, F, C` rule sets while ignoring a long list including `E501` (`.flake8:46-97`).
- `.gitignore` excludes build artifacts, media/model outputs (`*.wav`, `*.pdmodel`, `*.pdiparams*`), and vendored tool directories under `tools/` (`.gitignore:154-203`).
- `.mergify.yml` auto-merges `develop` PRs with ≥1 approval plus passing Travis CI, and auto-labels PRs by changed path such as `S2T`, `T2S`, `CLI`, `Server` (`.mergify.yml:216-296`).
- `.pre-commit-config.yaml` wires yapf, clang-format, cpplint, and import reordering with broad excludes for vendored/kaldi/third-party paths (`.pre-commit-config.yaml:358-424`).
- `.travis.yml` runs a single `JOB=PRE_COMMIT` Docker job on `paddlepaddle/paddle:latest` invoking `.travis/precommit.sh` and `.travis/unittest.sh` (`.travis.yml:469-498`).
- `MANIFEST.in` adds only two include patterns so TTS experiment text and frontend YAML files ship in the sdist (`MANIFEST.in:509-510`).
- `README_cn.md` (truncated in source) presents PaddleSpeech as a PaddlePaddle-based speech/audio model library with demos for ASR, translation, TTS, and punctuation restoration (`README_cn.md:550-685`).

## The system in five moves
1. PaddleSpeech presents itself as an open-source, state-of-the-art speech/audio toolkit on PaddlePaddle spanning research training through production deployment.
2. It demonstrates that breadth concretely with ASR, speech translation, multi-language TTS, and punctuation-restoration examples.
3. It makes the toolkit approachable via CLI, Server, and Streaming Server entry points plus production-ready streaming ASR/TTS systems.
4. It grounds quality in a rule-based Chinese frontend and mainstream-dataset coverage across ASR, TTS, verification, spotting, classification, and translation.
5. It enforces that scale with root-level style, lint, ignore, merge, pre-commit, and CI automation plus docs-build and packaging includes.
