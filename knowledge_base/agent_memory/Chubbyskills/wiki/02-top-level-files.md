[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The repository root defines project identity, default pipeline configuration, dependency profiles, environment setup, and ignored artifacts for the local Markdown-first source-library workflow.
## Key points
- The project is version `0.13.0` with 14 agent skills plus a local CLI workflow for importing, capturing, indexing, searching, and exporting evidence briefs from ordinary Markdown files (README.en.md:89-99).
- `chubby.example.yaml` provides the copy-to-`chubby.yaml` pipeline defaults: `output_dir`, `vault_dir`/`vault_root`, `index_db`, `state_file`, `report_dir`, `queue_file`, `enrich`, and `timeout_seconds` (chubby.example.yaml:3-12).
- `setup.sh` installs runtime dependencies by profile (`light`/`video`/`podcast`/`wechat`/`all`/`doctor`) plus skill-name aliases, without registering agent skills (setup.sh:311-321).
- `requirements.txt` pins the heavy runtime stacks for video transcription, podcast transcription, and WeChat/PDF processing, while `requirements-dev.txt` holds only test/lint dependencies (requirements.txt:291-304, requirements-dev.txt:279-281).
- `.gitignore` excludes Python/virtualenv/build outputs, media files, generated `output/`/`runs/`/`inbox/`/`.chubby/` artifacts, IDE files, and model caches (`.gitignore:9-53`).
- `README.en.md` documents the no-dependency Markdown/TXT quickstart (`init` → `import --no-enrich` → `search` → `brief`) and the per-content-type setup matrix for platform capture (README.en.md:119-142, README.en.md:167-174).
- The chunk notes `README.en.md` was truncated (5141 more characters not included); claims above cover only the visible portion and no contents beyond the truncation point are asserted.
---
## Project identity (README.en.md, VERSION)
Verbatim header and version:

```
# 🧰 Chubby Skills
### Turn saved content into a searchable source library
```

```
0.13.0
```

Version badge and release link in the README pin `Version-0.13.0` (README.en.md:89) and `New in [v0.13.0](./docs/release-0.13.0.md)` lists unified local document import, experimental Atlas/MuAPI podcast transcription with saved task recovery, and portable installation bundles (README.en.md:111).

Repository purpose stated verbatim (README.en.md:97):

> Chubby Skills is a set of **14 agent skills and a local command-line workflow** for content creators, researchers, and people who keep a Markdown knowledge base.

## Default pipeline config (chubby.example.yaml)
Verbatim file (chubby.example.yaml:1-12):

```yaml
# Chubby Skills pipeline config
# Copy to chubby.yaml or run: python3 tools/chubby.py init --vault /path/to/vault
# Paths can be absolute or relative to this repository.
output_dir: output
vault_dir:
# init --vault sets the root, its 00_Inbox capture destination and index below.
vault_root:
index_db:
state_file: .chubby/runs.jsonl
report_dir: runs
queue_file: inbox/links.txt
enrich: false
timeout_seconds: 1800
```

| Parameter | Default in example | Meaning per comments |
|---|---|---|
| `output_dir` | `output` | Pipeline output directory |
| `vault_dir` / `vault_root` | empty | Set by `init --vault`; root plus `00_Inbox` destination and index |
| `index_db` | empty | Index database location |
| `state_file` | `.chubby/runs.jsonl` | Run-state log |
| `report_dir` | `runs` | Report directory |
| `queue_file` | `inbox/links.txt` | Batch-capture queue (one source per line) |
| `enrich` | `false` | Content enrichment toggle |
| `timeout_seconds` | `1800` | Per-operation timeout |

## Entry workflow (README.en.md)
Local Markdown/TXT quickstart requires Python 3.11 or 3.12, no pip packages/API keys/models, via verbatim sequence (README.en.md:119-142):

```bash
git clone https://github.com/chubbyguan/chubbyskills.git
cd chubbyskills
python3 -m venv .venv
source .venv/bin/activate

python3 tools/chubby.py init --vault "$PWD/creator-vault"
python3 tools/chubby.py import demo-input/sample.md --no-enrich
python3 tools/chubby.py search "source library"
python3 tools/chubby.py brief --topic "source library" \
  --output "$PWD/creator-vault/30_Output/source-library-brief.md"
```

Behavioral rules stated in the README (README.en.md:144-146):

- Imported note lands in `creator-vault/00_Inbox`; brief plus companion JSON land in `creator-vault/30_Output` with exact-line pointers.
- Repeating the same import can reuse a valid result; changed document/attachments create a new result while retaining the old one.
- Repeating brief export needs a different output filename or explicit `--force`.

Own-file import and PDF caveats (README.en.md:150-159):

```bash
python3 tools/chubby.py import "/path/to/notes.md" --no-enrich
python3 tools/chubby.py import "/path/to/notes.txt" --no-enrich
python3 -m pip install 'pymupdf>=1.24'
python3 tools/chubby.py import "/path/to/report.pdf" --no-enrich
```

PDF import has no OCR; scanned PDFs without extractable text fail with an explanation; `--source-url` records provenance without downloading/verifying.

## Setup profiles (setup.sh)
Usage line verbatim (setup.sh:313-321):

```
bash setup.sh                 # light mode: zero/low-dependency tools
bash setup.sh light           # same as default
bash setup.sh video           # video transcription stack
bash setup.sh podcast         # podcast transcription stack
bash setup.sh wechat          # WeChat/PDF extraction stack
bash setup.sh all             # everything
bash setup.sh doctor          # environment check only
bash setup.sh bilibili xhs    # aliases are accepted
```

| Profile | Action (function) | Dependencies installed/checked |
|---|---|---|
| `light` (`install_light`, setup.sh:371-378) | Zero/low-dependency check only | `python3`; guidance for `DEEPSEEK_API_KEY`, `XHS_COOKIE` |
| `video` (`install_video`, setup.sh:380-389) | Video transcription stack | `python3`, `ffmpeg`, `yt-dlp`, `funasr modelscope torch torchaudio` |
| `podcast` (`install_podcast`, setup.sh:391-398) | Podcast transcription stack | `python3`, `ffmpeg`, `faster-whisper` |
| `wechat` (`install_wechat`, setup.sh:400-406) | WeChat/PDF stack | `python3`, `beautifulsoup4 markitdown pymupdf` |
| `all` (setup.sh:474-478) | Runs light + video + podcast + wechat | All of the above |
| `doctor` (`run_doctor`, setup.sh:350-352) | Environment check only | `python3 tools/check_env.py` |

Alias normalization (`normalize_target`, setup.sh:408-425) maps full skill names (e.g. `douyin-transcribe`, `podcast-transcribe`, `wechat-article-ingest`, `x-ingest`, `knowledge-base-management`) to the four profiles; unknown targets exit 2. `video`/`podcast`/`wechat` media paths additionally require `curl` (setup.sh:460-472).

README setup matrix mirrors these profiles (README.en.md:167-174):

| Content or operation | Setup |
|---|---|
| Local Markdown/TXT import, search, briefs | Python standard library; no additional setup |
| X/Xiaohongshu text and image posts | `bash setup.sh light` |
| Bilibili/YouTube captions | `python3 -m pip install yt-dlp` |
| Local video transcription | `bash setup.sh video`; requires system `ffmpeg` |
| Local podcast transcription | `bash setup.sh podcast`; installs `faster-whisper` |
| WeChat article/PDF processing | `bash setup.sh wechat` |

## Dependencies (requirements.txt, requirements-dev.txt)
Verbatim `requirements-dev.txt` (requirements-dev.txt:279-281):

```
# Test-only dependencies. Runtime Markdown generation uses the standard library.
PyYAML>=6,<7
ruff>=0.12,<1
```

Verbatim `requirements.txt` (requirements.txt:287-304):

```
# Chubby Skills - Dependencies
funasr>=1.0.0
modelscope>=1.10.0
torch>=2.0.0
torchaudio>=2.0.0
faster-whisper>=0.10.0
beautifulsoup4>=4.12.0
markitdown>=0.0.1
pymupdf>=1.23.0
```

| File | Group | Packages |
|---|---|---|
| `requirements.txt:291-294` | Video transcription (douyin/bilibili/tiktok/weibo/zhihu/youtube) | `funasr`, `modelscope`, `torch`, `torchaudio` |
| `requirements.txt:298` | Podcast transcription | `faster-whisper` |
| `requirements.txt:302-304` | WeChat article ingest | `beautifulsoup4`, `markitdown`, `pymupdf` |
| `requirements-dev.txt:280-281` | Test-only | `PyYAML`, `ruff` |

## Ignored artifacts (.gitignore)
Python/virtualenv/build entries (`.gitignore:9-20`): `__pycache__/`, `*.py[cod]`, `*$py.class`, `*.so`, `.Python`, `.venv/`, `venv/`, `env/`, `*.egg-info/`, `dist/`, `build/`. Generated/pipeline outputs (`.gitignore:29-40`): `output/`, `runs/`, `inbox/`, `.chubby/`, `chubby.yaml`, `*.md.bak`, media globs (`*.mp3`, `*.mp4`, `*.wav`, `*.avi`, `*.mov`, `*.jpg`, `*.jpeg`, `*.png`, `*.webp`). IDE/OS/model-cache entries (`.gitignore:42-53`): `.vscode/`, `.idea/`, `*.swp`, `*.swo`, `.DS_Store`, `Thumbs.db`, `.cache/`, `modelscope/`.

## Truncation note
`README.en.md` in the chunk is marked `... (truncated, 5141 more characters)` after the skills table at line 273; the skills table, changelog/docs links, and any content past that point are not covered here.

**Covers:** `.gitignore`, `chubby.example.yaml`, `README.en.md` (visible portion only; truncated per chunk), `requirements-dev.txt`, `requirements.txt`, `setup.sh`, `VERSION`
