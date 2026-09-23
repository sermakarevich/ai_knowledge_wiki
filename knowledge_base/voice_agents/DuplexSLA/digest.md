> [[index|Wiki]] | [[summary|Summary]]
# hyzhang24/DuplexSLA — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** DuplexSLA is a native full-duplex Speech–Language–Action foundation model that jointly decodes assistant audio and a structured action stream on a shared 160 ms chunk timeline (README.md:36).
## Key points
- DuplexSLA unifies listening, speaking, in-conversation planning, and tool calling on a single conversational clock, decoding assistant audio with a structured action stream on a shared 160 ms chunk timeline (README.md:36).
- It uses a dual-stream three-channel formulation to close the gap where duplex backbones lacked a native channel for in-conversation planning and tool calling (README.md:38).
- The user audio channel carries continuous user audio features at an 80 ms stride (README.md:40).
- The assistant audio channel carries discrete assistant speech tokens in a TA4 layout — 1 text anchor + 4 audio tokens at 40 ms stride per chunk (README.md:41).
- The action channel is a rate-limited textual stream carrying delayed transcripts, planning text, interaction-control labels, and structured tool calls at ≤10 tokens per chunk (README.md:42).
- All three channels are decoded jointly by a single backbone initialised from Step-Audio-2-mini (~7B parameters) and adapted via continued pretraining and post-training on duplex dialogue, turn-taking, and tool-call data (README.md:44).
- Turn-taking (`pause`, `interrupt`, `backchannel`) is emitted internally from semantic state rather than an external semantic VAD, and planning/tool calls are emitted on the action channel without halting assistant audio (README.md:48, README.md:50).

## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The top-level-files component captured in this chunk is the repository's `.gitignore`, which excludes OS, Python, environment, IDE, log, weight, and cache artefacts from version control.
## Key points
- The component covers exactly one source file, `.gitignore` (58 lines), defining what the repo checkout leaves untracked.
- It excludes macOS artefacts `.DS_Store`, `.AppleDouble`, and `.LSOverride` (`.gitignore:9`, `.gitignore:10`, `.gitignore:11`).
- It excludes Python build artefacts including `__pycache__/`, `*.py[cod]`, `*$py.class`, `*.so`, `build/`, `dist/`, `*.egg-info/`, and `*.egg` (`.gitignore:15`, `.gitignore:16`, `.gitignore:17`, `.gitignore:18`, `.gitignore:20`, `.gitignore:22`, `.gitignore:32`, `.gitignore:34`).
- It excludes virtual environments `.venv/`, `venv/`, `ENV/`, and `env/` (`.gitignore:37`, `.gitignore:38`, `.gitignore:39`, `.gitignore:40`).
- It excludes IDE/editor artefacts `.idea/`, `.vscode/`, `*.swp`, and `*.swo` (`.gitignore:43`, `.gitignore:44`, `.gitignore:45`, `.gitignore:46`).
- It excludes Jupyter checkpoints (`.ipynb_checkpoints/`), logs (`*.log`), and caches (`.cache/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`) (`.gitignore:49`, `.gitignore:52`, `.gitignore:62`, `.gitignore:63`, `.gitignore:64`, `.gitignore:65`).
- It excludes model weights and large artefacts `*.pt`, `*.pth`, `*.bin`, `*.safetensors`, and `*.ckpt`, noted as hosted on Hugging Face (`.gitignore:54`, `.gitignore:55`, `.gitignore:56`, `.gitignore:57`, `.gitignore:58`).

## The system in five moves
1. DuplexSLA frames full-duplex voice interaction as a single conversational clock where listening, speaking, planning, and tool calling happen together.
2. It puts user audio (80 ms stride), assistant audio (TA4 layout), and a rate-limited action stream (≤10 tokens/chunk) on a shared 160 ms chunk timeline decoded jointly by one Step-Audio-2-mini-based backbone.
3. The action channel carries transcripts, planning text, interaction-control labels, and structured tool calls so agency flows alongside speech without halting assistant audio.
4. Turn-taking (pause, interrupt, backchannel) is driven by the model's own semantic state rather than an external VAD.
5. The repo checkout itself keeps only source and docs tracked, leaving OS, Python, environment, IDE, log, cache, and Hugging Face-hosted weight artefacts untracked via `.gitignore`.
