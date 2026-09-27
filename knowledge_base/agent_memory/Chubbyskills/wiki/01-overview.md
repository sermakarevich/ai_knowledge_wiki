[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Chubby Skills is a set of 14 Agent Skills plus a unified CLI that collects video/podcast/article/local-doc material into local Markdown and supports search and sourced evidence-pack export for Agents.
## Key points
- Chubby Skills provides 14 Agent Skills and CLI tools for creators to save platform and local material as searchable, source-traceable local Markdown for Agent use (README.md:13-15, README.md:30-32).
- The pipeline runs link/local-doc → Markdown source with attachments → local search → sourced brief → Agent topic work (README.md:34-36).
- The offline quickstart runs `init --vault`, `import --no-enrich`, `search`, `brief --topic --output`, and `status --latest` with no third-party packages, API keys, or models (README.md:54-55, README.md:60-98).
- Platform ingest is dependency-gated per path: stdlib-only for Markdown/TXT/keyword/brief, `yt-dlp` for Bilibili/YouTube subtitles, `setup.sh video|podcast|wechat` plus `ffmpeg`/`faster-whisper`/`pymupdf` for local transcription and PDF text-layer import (README.md:126-134).
- The skill catalog spans 6 video, 1 podcast, 3 graphic-article, 1 enrichment, 1 knowledge-base, and 2 workflow skills (README.md:219-234).
- Data boundaries keep import/search/`semantic-lite`/brief local, platform fetch on source platforms, local A/V inference on-device, and optional `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` / `ATLAS_API_KEY` / `MUAPI_API_KEY` paths that send content or audio off-device (README.md:240-250).
- Outputs are frontmatter Markdown plus schema-v1 task metadata validated by `tools/validate_outputs.py output/ --schema-v1`, and v0.13.0 claims 220 tests with Linux/macOS CI (README.md:258-262, README.md:268).
---
## Purpose and pipeline
What it is (README.md:30-32):
> Chubby Skills is a set of 14 Agent Skills and CLI tools for content creators and personal knowledge bases. Products stay in local Markdown files processable by Obsidian, text editors, or Agents.

Pipeline (verbatim, README.md:34-36):
```text
链接 / 本地文档 → Markdown 原文与附件 → 本地搜索 → 带出处的资料包 → Agent 整理选题
```

| You want to do | Project provides (README.md:38-44) |
|---|---|
| Save platform material | Video subtitles/transcription, podcast transcription, article and image-text collection |
| Import existing material | Markdown, TXT, PDF text-layer import preserving sources and local attachments |
| Recover evidence while writing | Keyword search, optional semantic retrieval, source reading; auto index update after ingest |
| Assemble a topic pack | Markdown/JSON brief with verbatim excerpts, line numbers, sources, file digests |
| Let Agents use the vault | Standalone skill packs plus optional MCP service with search and source-reading tools |

## Quickstart (offline demo)
Requires Python 3.11 or 3.12 on macOS/Linux shell; no third-party packages, API keys, or models for the demo (README.md:54-55).

```bash
git clone https://github.com/chubbyguan/chubbyskills.git
cd chubbyskills
python3 -m venv .venv
source .venv/bin/activate
python3 tools/chubby.py init --vault "$PWD/creator-vault"
```
`init` creates `chubby.yaml` and vault directories; run later commands from the repo root reusing that config (README.md:60-68).

```bash
mkdir -p demo-input
cat > demo-input/notes.md <<'NOTE'
# 内容复用笔记
内容复用从保留原文和来源开始。同一份材料可以用于选题、文章和播客，但引用前要重新核对上下文。
NOTE
python3 tools/chubby.py import demo-input/notes.md --no-enrich
```
Swap in own `.md`/`.markdown`/`.txt`; add `--source-url "原始网页地址"` when the original page is known (README.md:72-87).

```bash
python3 tools/chubby.py search "内容复用"
python3 tools/chubby.py brief --topic "内容复用" \
  --output "$PWD/creator-vault/30_Output/brief.md"
python3 tools/chubby.py status --latest
```
Produces `creator-vault/00_Inbox/` Markdown with attachments, `30_Output/brief.md` plus `brief.json` with verbatim excerpts/line numbers/sources/SHA-256, and `.chubby/runs.jsonl` with `runs/` reports; `brief` exports locally without cloud models and does not judge correctness; re-export under a new filename or add `--force` to overwrite (README.md:91-108).

## Platform, local-doc, and audio paths
Subtitle-first YouTube example (README.md:114-122):
```bash
bash setup.sh light
python3 -m pip install yt-dlp
python3 tools/chubby.py doctor --platform youtube
python3 tools/chubby.py ingest "替换为你的真实链接" --no-enrich
python3 tools/chubby.py search "原文中的关键词"
```

| Processing path | Install / config (README.md:126-134) |
|---|---|
| Markdown/TXT import, keyword retrieval, brief | Python stdlib, no extra packages |
| X / Xiaohongshu graphics | Python stdlib; `bash setup.sh light` checks env, login/platform limits may still apply |
| Bilibili / YouTube subtitles | `python3 -m pip install yt-dlp` |
| Local video transcription | `bash setup.sh video`; needs system `ffmpeg`, first run downloads model |
| Local podcast transcription | `bash setup.sh podcast`; uses `faster-whisper`, default model `small` |
| WeChat article and its PDF path | `bash setup.sh wechat` |
| Generic PDF text-layer import | `python3 -m pip install 'pymupdf>=1.24'` |

Local docs (README.md:140-148):
```bash
python3 tools/chubby.py import "/你的资料目录/report.md" --no-enrich
python3 tools/chubby.py import "/你的资料目录/report.pdf" \
  --source-url "https://example.org/original-report" --no-enrich
```
Importer keeps the original, copies in-directory attachments beside the product, errors on missing/out-of-scope attachments; PDF extracts text layer only, no OCR.

Podcast default is local (README.md:152-163):
```bash
python3 tools/chubby.py ingest "/你的音频目录/episode.mp3" \
  --skill podcast --provider local --no-enrich
```
v0.13.0 adds experimental Atlas Cloud / MuAPI backends requiring explicit `--provider` plus credentials; audio goes to the provider and may bill; task IDs persist for resume, `--resubmit` creates a new (possibly billed) task; podcast auto-download accepts only public HTTP(S) direct URLs, no redirects or proxies.

Dedup, batch, retry (README.md:167-179):
```bash
python3 tools/chubby.py run --queue inbox/links.txt --no-enrich
python3 tools/chubby.py status --failed
python3 tools/chubby.py retry --all-failed
```
Same source/params/destination reuses valid products; changed sources re-import; `--refresh` reprocesses keeping old versions; index syncs incrementally after ingest and before unified query.

## Skill install and MCP
Install per-skill from the full repo root; Codex example installs the knowledge-base skill (README.md:183-200):
```bash
python3 tools/install_skill.py knowledge-base-management --dest ~/.codex/skills
python3 tools/install_skill.py --list
python3 tools/install_skill.py --all --dest /path/to/agent/skills
```
Installer bundles in-repo dependencies into a relocatable skill dir and refuses to overwrite same-named skills; use the installer or Release skill packs, not single-directory copies. Homepage `tools/chubby.py` needs the full repo; the standalone knowledge-base skill uses its own `tools/import_document.py`, `tools/vault_index.py`, `tools/evidence_brief.py`.

```bash
python3 -m pip install -r knowledge-base-management/requirements-mcp.txt
python3 tools/mcp_smoke.py --json
```
MCP exposes 6 tools: search, semantic retrieval, source reading, recent notes, reindex, stats; smoke test uses an ephemeral vault, real wiring needs server command plus `VAULT_DIR` (README.md:206-213).

## Skill catalog
| Direction | Skill | Main use (README.md:219-234) |
|---|---|---|
| Video | `bilibili-transcribe` | Bilibili subtitles-first, transcription, batch |
| Video | `youtube-transcribe` | YouTube subtitles, transcription, optional translation/bilingual |
| Video | `douyin-transcribe` | Douyin video to transcript |
| Video | `tiktok-transcribe` | TikTok video transcription |
| Video | `weibo-transcribe` | Weibo video transcription |
| Video | `zhihu-transcribe` | Zhihu video transcription |
| Podcast | `podcast-transcribe` | Single episode, RSS, local audio; optional experimental cloud backend |
| Graphic | `wechat-article-ingest` | WeChat articles and PDFs to Markdown |
| Graphic | `xiaohongshu-ingest` | Xiaohongshu graphics, video, optional analysis |
| Graphic | `x-ingest` | X/Twitter body, images, video |
| Enrich | `content-enrich` | Optional summaries, key points, tags |
| Vault | `knowledge-base-management` | Doc import, index, briefs, archive, MCP |
| Workflow | `industry-intelligence-radar` | Multi-source intel scan and trend briefs |
| Workflow | `learning-notes-automation` | Study notes, flashcards, knowledge links |

## Data boundaries, output protocol, verification
| Function | Location and config (README.md:240-250) |
|---|---|
| Doc import, keyword search, `semantic-lite`, brief | Local; local import does not fetch remote attachments |
| Platform collection | Hits source platforms; Xiaohongshu optionally uses own `XHS_COOKIE` |
| Local A/V transcription | On-device; first run may download models |
| Enrichment, translation, note extraction | Optional `DEEPSEEK_API_KEY`, content sent to that API |
| OpenAI vector retrieval | Optional `OPENAI_API_KEY`, vectorized content sent to API |
| Atlas / MuAPI transcription | Optional `ATLAS_API_KEY` / `MUAPI_API_KEY`, audio sent to vendors |
| Cloud Agent reading | Read content enters that Agent's model context |

Output protocol (README.md:256-262): collection/import products are frontmatter Markdown recording title, type, platform, source, date; unified CLI adds schema v1 task ID, collection time, source digest, attachment info.
```bash
python3 tools/validate_outputs.py output/ --schema-v1
```

Verification (README.md:266-280): v0.13.0 notes 220 tests, Linux/macOS CI, 24-script isolated imports across 14 skill packs, real PDF import and MCP interaction checks; release assets carry checksums; results do not imply all platforms/cloud services passed live acceptance. Offline self-check:
```bash
python3 tools/chubby.py quickstart --ephemeral --no-state
```
Docs entry, scope, license (README.md:284-304): docs cover `installation.md`, `creator-workflow.md`, `document-import.md`, `cloud-transcription.md`, `knowledge-automation.md`, `mcp-workflow.md`, `platform-fallbacks.md`, `integrations.md`, plus `CHANGELOG.md` (current 0.13.0); collection skills are for personal study/research under platform terms and law; code is MIT as-is, which grants no third-party content rights. No truncated files were noted in the chunk.

**Covers:** README.md (overview, quickstart, skill catalog, boundaries, output protocol, verification, docs entry, license); referenced `tools/chubby.py`, `tools/install_skill.py`, `tools/validate_outputs.py`, `tools/mcp_smoke.py`, `setup.sh`, `knowledge-base-management/` MCP and standalone tools, `docs/` workflow/platform guides, `examples/README.md`, `CHANGELOG.md`
