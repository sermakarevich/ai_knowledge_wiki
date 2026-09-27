# Technical Analysis: chubbyguan/chubbyskills

**Repository:** https://github.com/chubbyguan/chubbyskills
**Version analyzed:** 0.13.0
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview

Problem space: creators, researchers, and Markdown knowledge-base keepers lose source material across video platforms (Bilibili, YouTube, Douyin, TikTok, Weibo, Zhihu), podcasts, WeChat/Xiaohongshu/X articles, and local docs, and need verbatim, citable evidence — not lossy summaries — when an Agent later drafts on a topic.

How the repo addresses it: it ships 14 Agent Skills plus a unified local CLI (`tools/chubby.py`) that collects platform and local material into frontmatter Markdown with local attachments in a vault, keeps a local index, and exports sourced evidence packs (brief Markdown + JSON with verbatim excerpts, line numbers, sources, SHA-256 digests) for Agent topic work (README.md:30-32, README.md:34-36, README.md:91-108). The offline core path — `init --vault`, `import --no-enrich`, `search`, `brief --topic --output`, `status --latest` — runs on Python 3.11/3.12 stdlib with no third-party packages, API keys, or models (README.md:54-55, README.md:60-98).

Primary user: a content creator or researcher maintaining a local Obsidian/text-editor/Agent-readable Markdown vault.

## 2. High-Level Architecture

```text
Platform sources (video/podcast/article) ─► ingest / import ─► vault 00_Inbox Markdown + attachments
Local docs/audio (md/txt/pdf/mp3) ────────► ingest / import ─► vault 00_Inbox Markdown + attachments
                                                      │
                                                      ▼
                                              local index (index_db, auto-synced)
                                                      │
                                                      ▼
                                     keyword search / semantic-lite / source reading
                                                      │
                                                      ▼
                                     brief exporter ─► 30_Output brief.md + brief.json
                                                      │
                                                      ▼
                                     Agent topic work / MCP tools / runs + reports
```

Data-flow narrative:

1. Capture: `ingest` hits source platforms (subtitle-first for Bilibili/YouTube via `yt-dlp`; platform fetch stays on source platforms) or transcribes local A/V on-device; `import` copies local Markdown/TXT/PDF text-layer into the vault preserving sources and in-directory attachments (README.md:126-134, README.md:140-148).
2. Store: products land as frontmatter Markdown (title, type, platform, source, date; unified CLI adds schema-v1 task ID, collection time, source digest, attachment info) under `creator-vault/00_Inbox/`, with attachments copied beside the product (README.md:256-262, README.md:91-108).
3. Index: the index syncs incrementally after ingest and before unified query; dedup reuses valid products for identical source/params/destination, changed sources re-import, `--refresh` reprocesses keeping old versions (README.md:167-179).
4. Retrieve: keyword search is stdlib-local; optional semantic retrieval (`semantic-lite` local, OpenAI-vector optional) and source reading recover evidence without judging correctness (README.md:38-44, README.md:240-250).
5. Export and audit: `brief --topic --output` writes `brief.md` plus `brief.json` with verbatim excerpts, line numbers, sources, and digests; run state appends to `.chubby/runs.jsonl` with reports under `runs/`; outputs validate via `tools/validate_outputs.py output/ --schema-v1` (README.md:91-108, README.md:256-262).
6. Agent consumption: standalone skill packs (relocatable via installer) or the optional MCP service (6 tools: search, semantic retrieval, source reading, recent notes, reindex, stats) let Agents use the vault (README.md:183-213).

Persistent state lives in the vault directory (`creator-vault/00_Inbox/` products, `30_Output/` briefs), the index database location configured by `index_db` (set via `init --vault`), run-state log `state_file: .chubby/runs.jsonl`, reports in `report_dir: runs`, and the batch queue `queue_file: inbox/links.txt` (chubby.example.yaml:3-12).

## 3. The Sourced Vault Note

The central concept is the sourced vault note: a local frontmatter Markdown file plus beside-it attachments that preserves the original text and its provenance for Agent reuse.

Representation: collection/import products are frontmatter Markdown recording title, type, platform, source, and date; the unified CLI adds schema-v1 task ID, collection time, source digest, and attachment info (README.md:256-262). Imported notes land in `creator-vault/00_Inbox`; brief plus companion JSON land in `creator-vault/30_Output` with exact-line pointers (README.en.md:144-146). The brief JSON carries verbatim excerpts, line numbers, sources, and SHA-256 digests (README.md:91-108).

Named kinds/types with file:line: the skill catalog defines the producer kinds — 6 video skills (`bilibili-transcribe`, `youtube-transcribe`, `douyin-transcribe`, `tiktok-transcribe`, `weibo-transcribe`, `zhihu-transcribe`), 1 podcast skill (`podcast-transcribe`), 3 graphic-article skills (`wechat-article-ingest`, `xiaohongshu-ingest`, `x-ingest`), 1 enrichment skill (`content-enrich`), 1 vault skill (`knowledge-base-management`), 2 workflow skills (`industry-intelligence-radar`, `learning-notes-automation`) (README.md:219-234). The vault layout distinguishes `00_Inbox` capture products from `30_Output` briefs (README.en.md:144-146).

Key queries, verbatim snippet:

```bash
python3 tools/chubby.py search "内容复用"
python3 tools/chubby.py brief --topic "内容复用" \
  --output "$PWD/creator-vault/30_Output/brief.md"
```

## 4. LLM / External Service Integration

The repo's core loop calls no LLM/API: Markdown/TXT import, keyword retrieval, and brief export are Python stdlib with no extra packages, keys, or models (README.md:126-134, README.md:54-55). Everything else is explicit opt-in.

| Integration | Required vs optional | Env var / credential |
|---|---|---|
| Platform fetch (Bilibili/YouTube subtitles via `yt-dlp`; X/Xiaohongshu fetch) | Required only for those capture paths | `XHS_COOKIE` optionally for Xiaohongshu; platform login/limits may still apply (README.md:240-250, README.md:126-134) |
| Enrichment, translation, note extraction | Optional | `DEEPSEEK_API_KEY`, content sent to that API (README.md:240-250) |
| OpenAI vector retrieval | Optional | `OPENAI_API_KEY`, vectorized content sent to API (README.md:240-250) |
| Atlas Cloud podcast transcription (experimental, v0.13.0) | Optional, explicit `--provider` + credentials; audio leaves device, may bill | `ATLAS_API_KEY` (README.md:152-163, README.md:240-250) |
| MuAPI podcast transcription (experimental, v0.13.0) | Optional, explicit `--provider` + credentials; audio leaves device, may bill | `MUAPI_API_KEY` (README.md:152-163, README.md:240-250) |
| Local A/V transcription (faster-whisper default `small`, FunASR stack) | Optional for local audio/video paths; on-device but first run may download models | none; needs system `ffmpeg` (README.md:126-134, README.md:240-250) |
| Cloud Agent reading | Implicit when user pastes vault content into a cloud Agent | content enters that Agent's model context (README.md:240-250) |

## 5. The Collect-to-Brief Pipeline

The primary workflow is link/local-doc → Markdown source with attachments → local search → sourced brief → Agent topic work (README.md:34-36).

Step by step (every function as CLI stage with grounding; internal function-level signatures were not exposed in the wiki pages, so stages are cited to the documented commands):

1. `init --vault` — `python3 tools/chubby.py init --vault "$PWD/creator-vault"` creates `chubby.yaml` and vault directories; later commands run from the repo root reusing that config (README.md:60-68). Defaults recorded in `chubby.example.yaml:3-12` (`output_dir: output`, `state_file: .chubby/runs.jsonl`, `report_dir: runs`, `queue_file: inbox/links.txt`, `enrich: false`, `timeout_seconds: 1800`).
2. `import` (local docs) — `python3 tools/chubby.py import demo-input/notes.md --no-enrich` keeps the original, copies in-directory attachments beside the product, errors on missing/out-of-scope attachments; `--source-url` records provenance without downloading (README.md:72-87, README.md:140-148). PDF variant extracts the text layer only, no OCR (README.md:140-148, README.en.md:150-159).
3. `ingest` (platform/audio) — `python3 tools/chubby.py ingest "<link>" --no-enrich` for subtitle-first capture (needs `yt-dlp` for Bilibili/YouTube); local audio via `python3 tools/chubby.py ingest "/你的音频目录/episode.mp3" --skill podcast --provider local --no-enrich`; experimental cloud backends need explicit `--provider` plus credentials with billable task IDs persisted for resume (README.md:114-122, README.md:152-163).
4. `search` — `python3 tools/chubby.py search "原文中的关键词"` runs local keyword retrieval (optional semantic retrieval); the index syncs incrementally after ingest and before unified query (README.md:114-122, README.md:167-179).
5. `brief --topic --output` — exports `30_Output/brief.md` plus `brief.json` with verbatim excerpts, line numbers, sources, and SHA-256; runs locally without cloud models and does not judge correctness; re-export needs a new filename or `--force` (README.md:91-108).
6. `status` / `run` / `retry` — `python3 tools/chubby.py status --latest` and `status --failed`; batch via `python3 tools/chubby.py run --queue inbox/links.txt --no-enrich` with `retry --all-failed`; same source/params/destination reuses valid products, changed sources re-import, `--refresh` reprocesses keeping old versions (README.md:91-108, README.md:167-179).
7. Validate — `python3 tools/validate_outputs.py output/ --schema-v1` checks frontmatter Markdown plus schema-v1 task metadata (README.md:256-262).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | overview, quickstart, catalog, boundaries, protocol, verification | Canonical user doc: pipeline, 14-skill catalog, data boundaries, output protocol, CI/test claims |
| `README.en.md` | visible portion to line ~273 (truncated +5141 chars) | English mirror: Markdown/TXT quickstart, setup matrix, config behavior |
| `VERSION` | 1 line (`0.13.0`) | Pinned release version |
| `chubby.example.yaml` | 12 lines (chubby.example.yaml:1-12) | Copy-to-`chubby.yaml` pipeline defaults: output/vault/index/state/report/queue/enrich/timeout |
| `tools/chubby.py` | CLI entry (line refs via README usage) | Unified CLI: init, import, ingest, search, brief, run, retry, status, doctor, quickstart |
| `tools/install_skill.py` | installer (README.md:183-200) | Bundles in-repo deps into relocatable per-skill dirs; `--list` / `--all`, refuses overwrite |
| `tools/validate_outputs.py` | validator (README.md:256-262) | Validates output Markdown + schema-v1 task metadata |
| `tools/mcp_smoke.py` | smoke test (README.md:206-213) | MCP wiring check over an ephemeral vault (`--json`) |
| `tools/check_env.py` | env check (setup.sh:350-352) | Backend of `setup.sh doctor` environment check |
| `setup.sh` | 311-321 usage, 350-478 profiles | Dependency profiles `light/video/podcast/wechat/all/doctor` + skill-name aliases |
| `requirements.txt` | 287-304 | Heavy runtime stacks: FunASR/video, faster-whisper, bs4/markitdown/pymupdf |
| `requirements-dev.txt` | 279-281 | Test/lint only: PyYAML, ruff |
| `knowledge-base-management/` | skill dir (MCP + standalone tools) | Doc import, index, briefs, archive; MCP server + `tools/import_document.py`, `tools/vault_index.py`, `tools/evidence_brief.py` |
| `.gitignore` | 9-53 | Excludes venv/build outputs, media globs, generated `output/`/`runs/`/`inbox/`/`.chubby/`, IDE/model caches |
| `docs/` | guides (installation, creator-workflow, document-import, cloud-transcription, knowledge-automation, mcp-workflow, platform-fallbacks, integrations) | Workflow and platform-fallback documentation |
| `CHANGELOG.md` | current 0.13.0 | Release history |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| (stdlib only) | — | Markdown/TXT import, keyword retrieval, brief export; offline quickstart needs nothing else |
| `yt-dlp` | unpinned (`python3 -m pip install yt-dlp`) | Bilibili/YouTube subtitle-first capture |
| `ffmpeg` (system) | system package | Local video/podcast transcription prerequisite |
| `faster-whisper` | `faster-whisper>=0.10.0` | Local podcast transcription (default model `small`) |
| `pymupdf` | `pymupdf>=1.23.0` (README install line `pymupdf>=1.24`) | Generic PDF text-layer import; WeChat/PDF stack |
| `beautifulsoup4` | `beautifulsoup4>=4.12.0` | WeChat article ingest |
| `markitdown` | `markitdown>=0.0.1` | WeChat article conversion |
| `funasr` | `funasr>=1.0.0` | Local video transcription stack |
| `modelscope` | `modelscope>=1.10.0` | Model download for local video transcription |
| `torch` | `torch>=2.0.0` | Local video transcription backend |
| `torchaudio` | `torchaudio>=2.0.0` | Local video transcription backend |
| `PyYAML` | `PyYAML>=6,<7` (dev/test only) | Test-only dependency |
| `ruff` | `ruff>=0.12,<1` (dev/test only) | Lint, test-only |

Source: `requirements.txt:287-304`, `requirements-dev.txt:279-281`, `setup.sh:371-406`, README setup matrix (README.md:126-134, README.en.md:167-174).

## 8. CLI / Usage Surface

Entry points: `python3 tools/chubby.py` (unified CLI, needs full repo root); per-skill standalone tools inside the `knowledge-base-management` skill (`tools/import_document.py`, `tools/vault_index.py`, `tools/evidence_brief.py`); `python3 tools/install_skill.py` (skill installer); `python3 tools/validate_outputs.py` (output validator); `python3 tools/mcp_smoke.py --json` (MCP smoke test); `bash setup.sh <profile>` (dependency setup).

Commands:

| Command | Form | Effect |
|---|---|---|
| `init` | `python3 tools/chubby.py init --vault "$PWD/creator-vault"` | Creates `chubby.yaml` + vault directories |
| `import` | `python3 tools/chubby.py import <file\|dir> [--source-url URL] --no-enrich` | Local md/txt/pdf import into `00_Inbox` |
| `ingest` | `python3 tools/chubby.py ingest "<link\|audio>" [--skill podcast --provider local] --no-enrich` | Platform subtitle capture or local/cloud transcription |
| `search` | `python3 tools/chubby.py search "<keywords>"` | Local keyword (optional semantic) retrieval |
| `brief` | `python3 tools/chubby.py brief --topic "<t>" --output <vault>/30_Output/brief.md [--force]` | Sourced brief.md + brief.json export |
| `status` | `python3 tools/chubby.py status --latest` / `--failed` | Inspect run state |
| `run` | `python3 tools/chubby.py run --queue inbox/links.txt --no-enrich` | Batch capture from queue file |
| `retry` | `python3 tools/chubby.py retry --all-failed` | Retry failed runs |
| `doctor` | `python3 tools/chubby.py doctor --platform youtube` | Per-platform environment check |
| `quickstart` | `python3 tools/chubby.py quickstart --ephemeral --no-state` | Offline self-check |
| `install_skill` | `python3 tools/install_skill.py <name> --dest <dir>` / `--list` / `--all` | Install relocatable skill pack(s) |

Env vars:

| Variable | Required? | Purpose |
|---|---|---|
| `DEEPSEEK_API_KEY` | Optional | Enrichment/translation/note extraction |
| `OPENAI_API_KEY` | Optional | OpenAI vector retrieval |
| `ATLAS_API_KEY` | Optional | Atlas Cloud podcast transcription |
| `MUAPI_API_KEY` | Optional | MuAPI podcast transcription |
| `XHS_COOKIE` | Optional | Xiaohongshu collection |
| `VAULT_DIR` | Needed for real MCP wiring | Vault location for MCP server |

Config (`chubby.example.yaml:3-12`):

| Key | Default | Meaning |
|---|---|---|
| `output_dir` | `output` | Pipeline output directory |
| `vault_dir` / `vault_root` | empty (set by `init --vault`) | Vault root + `00_Inbox` destination and index |
| `index_db` | empty | Index database location |
| `state_file` | `.chubby/runs.jsonl` | Run-state log |
| `report_dir` | `runs` | Report directory |
| `queue_file` | `inbox/links.txt` | Batch-capture queue |
| `enrich` | `false` | Content enrichment toggle |
| `timeout_seconds` | `1800` | Per-operation timeout |

## 9. Extensibility Points

- New capture source → add a skill directory mirroring the existing 14 (e.g. `bilibili-transcribe`, `x-ingest` patterns in README.md:219-234) plus its ingest path behind the unified CLI; add its dependency profile mapping in `normalize_target` (setup.sh:408-425) and a `setup.sh` profile if it needs heavy packages.
- New setup profile → extend `install_light` / `install_video` / `install_podcast` / `install_wechat` (setup.sh:371-406) and the `all`/`doctor` dispatch (setup.sh:474-478, setup.sh:350-352).
- Vault behavior (import/index/brief/archive) → extend the `knowledge-base-management` skill and its standalone `tools/import_document.py`, `tools/vault_index.py`, `tools/evidence_brief.py` (README.md:183-200).
- Agent surfacing → extend the MCP service's 6 tools (search, semantic retrieval, source reading, recent notes, reindex, stats) and its `requirements-mcp.txt` wiring (README.md:206-213).
- New intelligence workflow → add a workflow skill alongside `industry-intelligence-radar` / `learning-notes-automation` (README.md:219-234).
- Output schema evolution → extend `tools/validate_outputs.py --schema-v1` and the frontmatter/task-metadata convention (README.md:256-262).

## 10. Limitations and Gotchas

- **PDF import is text-layer only, no OCR:** scanned PDFs without extractable text fail with an explanation instead of producing a transcript (README.md:140-148, README.en.md:150-159). Do not route image-only PDFs through `import` expecting transcription.
- **Re-import and re-brief are not idempotent-overwrite:** changed documents create a new result while retaining the old one, and repeating a brief export requires a different output filename or explicit `--force` (README.en.md:144-146, README.md:91-108). Scripts that reuse filenames without `--force` will error.
- **Platform capture is login/limit- and dependency-gated:** X/Xiaohongshu graphics need `setup.sh light` and can still hit login/platform limits; Bilibili/YouTube need `yt-dlp`; local video needs system `ffmpeg` plus a first-run model download; podcast auto-download accepts only public HTTP(S) direct URLs with no redirects or proxies (README.md:126-134, README.md:152-163).
- **Cloud paths bill and exfiltrate:** Atlas/MuAPI transcription sends audio off-device and may bill, with task IDs persisted for resume and `--resubmit` creating a new possibly-billed task; enrichment/translation sends content to the DeepSeek API and vector retrieval to the OpenAI API (README.md:152-163, README.md:240-250).
- **Standalone skills are not single-directory copies, and `tools/chubby.py` needs the full repo:** use `tools/install_skill.py` or Release skill packs (installer refuses to overwrite same-named skills); the homepage CLI does not work from a lone installed skill dir (README.md:183-200). Wiki coverage itself is thin here: only overview + top-level-files pages were available, so internal module APIs, index schema, and MCP server implementation details are not documented in this summary.

## 11. How It Compares to Alternatives

- **Obsidian (local Markdown vault):** Obsidian provides the editable vault, backlinks, and search UX this repo targets as output ("processable by Obsidian, text editors, or Agents", README.md:30-32), but no platform subtitle/transcription ingest or evidence-brief export; Chubby Skills is the capture-to-brief feeder, Obsidian the reading environment.
- **yt-dlp + Whisper pipelines (ad-hoc scripts):** the same subtitle-first (`yt-dlp`) and local transcription (`faster-whisper`/`ffmpeg`, FunASR) primitives are available standalone, but without the unified vault layout, incremental index, dedup/queue/retry state, schema-v1 validation, or Agent skill packaging this repo adds (README.md:126-134, README.md:167-179, README.md:256-262).
- **NotebookLM / Readwise-style cloud collectors:** cloud collectors simplify cross-platform saving and AI summarization but keep the library and inference off-device; this repo keeps import/search/`semantic-lite`/brief local and on-device by default with cloud only behind explicit API-key/provider flags (README.md:240-250).
- **Model Context Protocol file-search servers / Agent file tools:** generic MCP file tools expose search/read over arbitrary directories, overlapping the 6 MCP tools here (search, semantic retrieval, source reading, recent notes, reindex, stats; README.md:206-213), but lack the platform-ingest front end, frontmatter provenance convention, and brief-with-digests evidence-pack contract.

Positioning: a local-first, provenance-strict feeder for Agent-assisted creator workflows — weakest as a general knowledge manager or cloud AI notebook, strongest where every reused quote must trace to a verbatim line, source URL, and digest without leaving the device by default.

## Appendix: Selected Code Snippets

1. Pipeline statement (README.md:34-36):

```text
链接 / 本地文档 → Markdown 原文与附件 → 本地搜索 → 带出处的资料包 → Agent 整理选题
```

2. Default pipeline config (chubby.example.yaml:1-12):

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

3. Setup profiles usage (setup.sh:313-321):

```text
bash setup.sh                 # light mode: zero/low-dependency tools
bash setup.sh light           # same as default
bash setup.sh video           # video transcription stack
bash setup.sh podcast         # podcast transcription stack
bash setup.sh wechat          # WeChat/PDF extraction stack
bash setup.sh all             # everything
bash setup.sh doctor          # environment check only
bash setup.sh bilibili xhs    # aliases are accepted
```

4. Heavy runtime dependencies (requirements.txt:287-304):

```text
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
