> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repository root defines licensing, attribution, packaging, dependency, and code-quality configuration for the Voxtream project.
## Key points
- `.gitignore` excludes editor, Python cache, build, audio/benchmark artifacts, and local experiment state from version control (`.gitignore:1-11`).
- `.pre-commit-config.yaml` enforces formatting and linting with black, isort, ruff (`--fix --exit-non-zero-on-fix`), and mypy type checking (`.pre-commit-config.yaml:24-46`).
- `ATTRIBUTION.md` requires CC BY 4.0 attribution to the Emilia and HiFiTTS-2 datasets for released model weights (`ATTRIBUTION.md:51-64`).
- Dual licensing is present: full Apache License 2.0 text in `LICENSE-APACHE` and MIT License copyright 2025 Nikita Torgashov in `LICENSE-MIT` (`LICENSE-APACHE:70-71`, `LICENSE-MIT:276-278`).
- `NOTICE` attributes the Depth Transformer component to SesameAI under Apache 2.0 (`NOTICE:312-316`).
- `MANIFEST.in` packages `README.md`, `voxtream/VERSION`, `requirements.txt`, plus `assets/*.wav|*.csv` and `configs/*.json` (`MANIFEST.in:301-306`).
- `requirements.txt` pins the training/inference/demo stack including torch/torchaudio, torchtune, lightning, moshi, transformers, gradio, hydra-core, and audio/ASR deps (`requirements.txt:331-353`).
---
## Ignore rules
Excludes local and generated artifacts from git:
```
.vscode/
__pycache__/
*.pyc
assets/audio/*.npy
assets/benchmark/*.npy
experiments/
dist/
*.egg-info/
gradio_cached_examples/
wavlm-large/
.codex
```
**Covers:** `.gitignore`
## Code quality hooks
Four pre-commit repos, pinned revisions:
| Hook | rev | Args |
|---|---|---|
| `black` | `25.9.0` | — |
| `isort` | `6.0.1` | — |
| `ruff` | `v0.13.1` | `--fix --exit-non-zero-on-fix` |
| `mypy` | `v1.18.2` | — |
Exact config excerpt:
```
repos:
  - repo: https://github.com/psf/black
    rev: 25.9.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 6.0.1
    hooks:
      - id: isort
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.13.1
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.18.2
    hooks:
      - id: mypy
```
**Covers:** `.pre-commit-config.yaml`
## Attribution and licenses
- `ATTRIBUTION.md:55-61` lists Emilia Dataset (`amphion/Emilia-Dataset`) and HiFiTTS-2 (`nvidia/hifitts-2`), both CC BY 4.0, and states released weights are based on them (`ATTRIBUTION.md:63-64`).
- `LICENSE-APACHE` is the standard Apache 2.0 text: copyright and patent grants (`LICENSE-APACHE:135-156`), redistribution conditions (`LICENSE-APACHE:158-197`), warranty disclaimer and liability limits (`LICENSE-APACHE:212-232`).
- `LICENSE-MIT:278` names copyright holder `2025 Nikita Torgashov` with standard MIT grant and AS-IS disclaimer (`LICENSE-MIT:280-296`).
- `NOTICE:315-316` states the Depth Transformer component is by SesameAI under Apache 2.0.
**Covers:** `ATTRIBUTION.md`, `LICENSE-APACHE`, `LICENSE-MIT`, `NOTICE`
## Packaging and dependencies
`MANIFEST.in` includes:
```
include README.md
include voxtream/VERSION
include requirements.txt
recursive-include assets *.wav
recursive-include assets *.csv
recursive-include configs *.json
```
Key `requirements.txt` pins (`requirements.txt:331-353`):
| Package | Pin |
|---|---|
| `torch`, `torchaudio` | `>=2.4,<2.9` |
| `torchtune` | `==0.4.0` |
| `torchao` | `==0.9.0` |
| `lightning` | `==2.4.0` |
| `transformers` | `==4.50.0` |
| `gradio` / `gradio_client` | `==4.44.1` / `==1.3.0` |
| `hydra-core` | `==1.3.2` |
| `huggingface_hub` | `==0.28.1` |
| `moshi` | `>=0.2.13` |
| `openai-whisper` | `==20250625` |
| `silero-vad` | `==6.2.0` |
**Covers:** `MANIFEST.in`, `requirements.txt`
**Covers:** .gitignore, .pre-commit-config.yaml, ATTRIBUTION.md, LICENSE-APACHE, LICENSE-MIT, MANIFEST.in, NOTICE, requirements.txt
