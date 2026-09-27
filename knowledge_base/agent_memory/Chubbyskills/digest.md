> [[index|Wiki]] | [[summary|Summary]]
# chubbyguan/chubbyskills — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Chubby Skills is a set of 14 Agent Skills plus a unified CLI that collects video/podcast/article/local-doc material into local Markdown and supports search and sourced evidence-pack export for Agents.
## Key points
- Chubby Skills provides 14 Agent Skills and CLI tools for creators to save platform and local material as searchable, source-traceable local Markdown for Agent use (README.md:13-15, README.md:30-32).
- The pipeline runs link/local-doc → Markdown source with attachments → local search → sourced brief → Agent topic work (README.md:34-36).
- The offline quickstart runs `init --vault`, `import --no-enrich`, `search`, `brief --topic --output`, and `status --latest` with no third-party packages, API keys, or models (README.md:54-55, README.md:60-98).
- Platform ingest is dependency-gated per path: stdlib-only for Markdown/TXT/keyword/brief, `yt-dlp` for Bilibili/YouTube subtitles, `setup.sh video|podcast|wechat` plus `ffmpeg`/`faster-whisper`/`pymupdf` for local transcription and PDF text-layer import (README.md:126-134).
- The skill catalog spans 6 video, 1 podcast, 3 graphic-article, 1 enrichment, 1 knowledge-base, and 2 workflow skills (README.md:219-234).
- Data boundaries keep import/search/`semantic-lite`/brief local, platform fetch on source platforms, local A/V inference on-device, and optional `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` / `ATLAS_API_KEY` / `MUAPI_API_KEY` paths that send content or audio off-device (README.md:240-250).
- Outputs are frontmatter Markdown plus schema-v1 task metadata validated by `tools/validate_outputs.py output/ --schema-v1`, and v0.13.0 claims 220 tests with Linux/macOS CI (README.md:258-262, README.md:268).
## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The repository root defines project identity, default pipeline configuration, dependency profiles, environment setup, and ignored artifacts for the local Markdown-first source-library workflow.
## Key points
- The project is version `0.13.0` with 14 agent skills plus a local CLI workflow for importing, capturing, indexing, searching, and exporting evidence briefs from ordinary Markdown files (README.en.md:89-99).
- `chubby.example.yaml` provides the copy-to-`chubby.yaml` pipeline defaults: `output_dir`, `vault_dir`/`vault_root`, `index_db`, `state_file`, `report_dir`, `queue_file`, `enrich`, and `timeout_seconds` (chubby.example.yaml:3-12).
- `setup.sh` installs runtime dependencies by profile (`light`/`video`/`podcast`/`wechat`/`all`/`doctor`) plus skill-name aliases, without registering agent skills (setup.sh:311-321).
- `requirements.txt` pins the heavy runtime stacks for video transcription, podcast transcription, and WeChat/PDF processing, while `requirements-dev.txt` holds only test/lint dependencies (requirements.txt:291-304, requirements-dev.txt:279-281).
- `.gitignore` excludes Python/virtualenv/build outputs, media files, generated `output/`/`runs/`/`inbox/`/`.chubby/` artifacts, IDE files, and model caches (`.gitignore:9-53`).
- `README.en.md` documents the no-dependency Markdown/TXT quickstart (`init` → `import --no-enrich` → `search` → `brief`) and the per-content-type setup matrix for platform capture (README.en.md:119-142, README.en.md:167-174).
- The chunk notes `README.en.md` was truncated (5141 more characters not included); claims above cover only the visible portion and no contents beyond the truncation point are asserted.
## The system in five moves
1. Declare identity and defaults at the root: v0.13.0, 14 skills plus local CLI, and `chubby.example.yaml` pipeline paths and toggles.
2. Install only what each capture path needs via `setup.sh` profiles and the pinned heavy stacks, keeping Markdown/TXT/search/brief on stdlib.
3. Collect platform and local material — subtitles-first video, local podcast transcription, articles, PDFs, docs — into frontmatter Markdown with attachments in the vault inbox.
4. Recover evidence locally with keyword search, optional semantic retrieval, and auto-updated indexes without judging correctness.
5. Export sourced briefs with verbatim excerpts, line numbers, sources, and digests for Agent topic work, validated against schema-v1.
6. Keep boundaries explicit: local import/search/brief, on-device A/V inference, platform fetch on source platforms, and opt-in cloud keys that send content off-device.
