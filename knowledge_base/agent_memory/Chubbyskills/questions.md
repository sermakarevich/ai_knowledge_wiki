---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: chubbyguan/chubbyskills

### Q1. What is Chubby Skills in one sentence, and what is its end-to-end pipeline?
> [!tip]- Answer
> Chubby Skills is a set of 14 Agent Skills plus a unified CLI that collects video/podcast/article/local-doc material into local Markdown with search and sourced evidence-pack export for Agents. The pipeline runs link/local-doc → Markdown source with attachments → local search → sourced brief → Agent topic work. Products stay in local frontmatter Markdown files usable by Obsidian, text editors, or Agents. See [[wiki/01-overview|Overview]].

### Q2. What is the offline quickstart sequence, and what does each step produce?
> [!tip]- Answer
> The offline demo needs only Python 3.11/3.12 with no third-party packages, API keys, or models: `init --vault`, `import --no-enrich`, `search`, `brief --topic --output`, and `status --latest`. Import lands Markdown with attachments in `creator-vault/00_Inbox`, while `brief` exports `30_Output/brief.md` plus `brief.json` with verbatim excerpts, line numbers, sources, and SHA-256 digests. The `brief` step runs locally without cloud models and never judges correctness. See [[wiki/01-overview|Overview]].

### Q3. How is the 14-skill catalog organized, and how are skills installed?
> [!tip]- Answer
> The catalog spans 6 video skills (bilibili/youtube/douyin/tiktok/weibo/zhihu), 1 podcast skill, 3 graphic-article skills (wechat/xiaohongshu/x), 1 enrichment skill, 1 knowledge-base skill, and 2 workflow skills (intel radar, learning notes). Skills install per-skill via `tools/install_skill.py <name> --dest <agent-skills-dir>`, which bundles in-repo dependencies and refuses to overwrite same-named skills. The knowledge-base skill can also expose 6 MCP tools (search, semantic retrieval, source reading, recent notes, reindex, stats). See [[wiki/01-overview|Overview]].

### Q4. What stays local in Chubby Skills, and what sends content off-device?
> [!tip]- Answer
> Doc import, keyword search, `semantic-lite` retrieval, and brief export are local, and local A/V transcription runs on-device (first run may download models). Platform collection hits the source platforms, with Xiaohongshu optionally using the user's own `XHS_COOKIE`. Setting `DEEPSEEK_API_KEY`/`OPENAI_API_KEY`/`ATLAS_API_KEY`/`MUAPI_API_KEY` opts into cloud enrichment, vector retrieval, or Atlas/MuAPI transcription, which sends content or audio to those vendors. See [[wiki/01-overview|Overview]].

### Q5. What does `chubby.example.yaml` define, and how is it used?
> [!tip]- Answer
> It is the copy-to-`chubby.yaml` pipeline defaults file created by `init --vault`, covering `output_dir`, `vault_dir`/`vault_root`, `index_db`, `state_file` (`.chubby/runs.jsonl`), `report_dir` (`runs`), `queue_file` (`inbox/links.txt`), `enrich: false`, and `timeout_seconds: 1800`. The vault root sets the `00_Inbox` capture destination and index location, while the queue file holds one batch-capture source per line. Repeating the same import reuses valid products, and re-exporting a brief needs a new filename or `--force`. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What do the `setup.sh` profiles install, and how do the requirements files split?
> [!tip]- Answer
> `setup.sh` offers `light` (env check only), `video` (ffmpeg, yt-dlp, funasr/modelscope/torch/torchaudio), `podcast` (ffmpeg, faster-whisper), `wechat` (beautifulsoup4, markitdown, pymupdf), `all`, and `doctor`, plus skill-name aliases that normalize to these profiles. Markdown/TXT import, keyword search, and brief need only the Python stdlib, while Bilibili/YouTube subtitles need `yt-dlp` and generic PDF import needs `pymupdf`. `requirements.txt` pins those heavy runtime stacks and `requirements-dev.txt` holds only test/lint deps (`PyYAML`, `ruff`). See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. Should a content creator or researcher adopt Chubby Skills for a local source library, and why?
> [!tip]- Answer
> Recommend it when the priority is a local, source-traceable Markdown library with verbatim, line-numbered evidence packs and a stdlib-only offline path for Markdown/TXT work. Recommend against it when the workload needs heavy platform coverage without setup friction, OCR for scanned PDFs, or judged-correct briefs, since capture is dependency-gated, PDF import is text-layer only, and briefs deliberately do not judge correctness. Pilot with the offline quickstart plus one platform path before committing a full vault to it. See [[wiki/01-overview|Overview]].
