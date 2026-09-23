> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
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
---
## C++ style: `.clang-format`
Verbatim excerpt (`.clang-format:25-32`):
```
Language:        Cpp
BasedOnStyle:  Google
IndentWidth:     4
TabWidth:        4
ContinuationIndentWidth: 4
MaxEmptyLinesToKeep: 2
AccessModifierOffset: -2  # The private/protected/public has no indent in class
Standard:  Cpp11
```
Additional exact flags (`.clang-format:33-35`): `AllowAllParametersOfDeclarationOnNextLine: true`, `BinPackParameters: false`, `BinPackArguments: false`. Usage documented in-file is `clang-format -i -style=file PATH/TO/SOURCE/CODE` (`.clang-format:14-19`).

## Python style and lint: `.flake8`, `.style.yapf`
`.flake8` options table:

| Setting | Value |
|---|---|
| `max-line-length` | `120` (`.flake8:46`) |
| `exclude` | `.git`, `__pycache__`, `utils/compute-wer.py`, `third_party/` (`.flake8:51-58`) |
| `filename` | `*.py` (`.flake8:60-61`) |
| `ignore` | `W503`, `E252,E262,E127,E265,E126,E266,E241,E261,E128,E125,E129`, `W291,W293,W605`, `E203,E305,E402,E501,E721,E741,F403,F405,F821,F841,F999,W503,W504,C408,E302,W291,E303`, `EXE001`, `B007,B008`, `C400,C401,C402,C403,C404,C405,C407,C411,C413,C414,C415` (`.flake8:75-86`) |
| `per-file-ignores` | `*/__init__.py: F401` (`.flake8:89-90`) |
| `select` | `E, W, F, C` (`.flake8:93-97`) |

`.style.yapf` is 4 lines total (`.style.yapf:460-463`):
```
[style]
based_on_style = pep8
column_limit = 80
```

## Git ergonomics and ignores: `.gitconfig`, `.gitignore`
`.gitconfig` defines short aliases `st`, `ci`, `br`, `co`, `df`, `l`, `ll` (`.gitconfig:103-110`), sets `merge.tool = vimdiff` (`.gitconfig:112-113`), `core.editor = vim` (`.gitconfig:115-117`), colorizes `branch`/`diff`/`status` output (`.gitconfig:119-138`), and sets `push.default = matching` with `credential.helper = store` (`.gitconfig:140-144`); the `[user]` `name`/`email` fields are empty (`.gitconfig:146-148`).
`.gitignore` covers editor/OS caches (`.DS_Store`, `.vscode`, `.idea`), Python artifacts (`*.pyc`, `*.whl`, `*.egg-info`, `build`), media/model outputs (`*.wav`, `*.pdmodel`, `*.pdiparams*`, `*.npz`), plus vendored trees `tools/kenlm`, `tools/kaldi`, `tools/srilm`, `tools/openfst-1.8.1/`, `tools/onnx`, `tools/onnxruntime`, `tools/Paddle2ONNX`, `docs/build/`, `speechx/fc_patch/`, and `third_party/ctc_decoders/paddlespeech_ctcdecoders.py` (`.gitignore:154-209`).

## Automation: `.mergify.yml`, `.pre-commit-config.yaml`, `.travis.yml`
Mergify rules table (selected, `.mergify.yml:215-352`):

| Rule | Condition | Action |
|---|---|---|
| auto-merge develop | `approved-reviews-by>=1`, `check-success=Travis CI - Pull Request`, `base=develop` | `merge: method: merge` |
| conflict warning | `conflict` | comment + add label `conflicts` |
| unlabel | `-conflict` | remove label `conflicts` |
| label Dataset | `files~=^dataset/` | add `Dataset` |
| label S2T / T2S / Audio / Vector / Text | `files~=^paddlespeech/s2t/` etc. | add matching label |
| label CLI / Server / Demo / Example | `files~=^paddlespeech/cli`, `^paddlespeech/server`, `^demos/`, `^examples/` | add matching label |
| label CI / Installation / Test / Docker / Deployment | `files~=` on `.circleci/`, `ci/`, `.github/`, `.travis.yml`, `tools/`, `setup.py`, `tests/`, `docker/`, `runtime/` | add matching label |

Pre-commit repos (`.pre-commit-config.yaml:357-424`): `mirrors-yapf` rev `v0.16.0` with `id: yapf` on `\.py$`; `pre-commit-hooks` rev `a11d9314b22d8f8c7556443875b731ef05965464` with `check-merge-conflict`, `check-symlinks`, `detect-private-key`, `end-of-file-fixer` (md only), `requirements-txt-fixer`, `check-yaml`, `check-json`, `pretty-format-json --no-sort-keys --autofix`; `Lucas-C/pre-commit-hooks` rev `v1.0.1` forbidding/removing CRLF and tabs in md; local `clang-format` entry `bash .pre-commit-hooks/clang-format.hook -i` and `cpplint --filter=-build,-whitespace,+whitespace/comma,-whitespace/indent`, plus `reorder-python-imports` rev `v2.4.0` — each with `exclude:` patterns for `runtime/engine/kaldi`, `audio/paddleaudio/src`, `third_party`, and similar vendored paths.
Travis (`.travis.yml:469-498`): `language: cpp`, `cache: ccache`, `dist: Bionic`, `services: docker`, single env `JOB=PRE_COMMIT`; `before_install` installs `virtualenv pre-commit pip` and pulls `paddlepaddle/paddle:latest`; `script` runs that image mounting `$PWD:/py_unittest` and executing `bash .travis/precommit.sh && source env.sh && bash .travis/unittest.sh`.

## Docs build and packaging: `.readthedocs.yml`, `MANIFEST.in`
`.readthedocs.yml` uses config `version: 2` (`.readthedocs.yml:435`), Sphinx config `docs/source/conf.py` (`.readthedocs.yml:438-439`), empty extra `formats: []` (`.readthedocs.yml:446`), and Python 3.7 with `docs/requirements.txt` plus setuptools install of `.` with `system_packages: true` (`.readthedocs.yml:449-455`).
`MANIFEST.in` verbatim (`.MANIFEST.in:509-510`, chunk `MANIFEST.in:506-511`):
```
include paddlespeech/t2s/exps/*.txt
include paddlespeech/t2s/frontend/*.yaml
```

## Project landing page: `README_cn.md` (truncated)
`README_cn.md` opens with a Simplified-Chinese/English switch and the PaddleSpeech logo plus license/release/OS/Python/contributor badges (`.README_cn.md:516-534`), and defines PaddleSpeech as an open speech/audio model library on PaddlePaddle covering key speech and audio tasks (`.README_cn.md:550-551`). Demos shown in the visible portion include ASR result tables for `en.wav`/`zh.wav` (`.README_cn.md:556-584`), English-to-Chinese speech translation (`.README_cn.md:586-607`), multi-row TTS examples (English, date/temperature Chinese, tongue-twister, mixed-language poem, Cantonese) (`.README_cn.md:609-666`), and punctuation restoration mapping `今天的天气真不错啊你下午有空吗我想约你一起去吃饭` to punctuated output (`.README_cn.md:668-685`). The features section claims ease of use via CLI, SoTA lightweight models, streaming ASR/TTS, rule-based Chinese frontend with text normalization and G2P, and cascaded audio/NLP/vision applications (`.README_cn.md:688-698`); install prerequisites listed are `gcc >= 4.8.5`, `paddlepaddle`, `python >= 3.8` on Linux/mac/Windows with `pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple` (`.README_cn.md:756-770`). Truncation note: the chunk cuts `README_cn.md` after the install section (chunk line 777: "truncated, 29457 more characters"); contents beyond that point are not summarized here.

**Covers:** `.clang-format`, `.flake8`, `.gitconfig`, `.gitignore`, `.mergify.yml`, `.pre-commit-config.yaml`, `.readthedocs.yml`, `.style.yapf`, `.travis.yml`, `MANIFEST.in`, `README_cn.md` (truncated, visible portion only)
