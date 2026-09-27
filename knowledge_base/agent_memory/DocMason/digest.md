> [[index|Wiki]] | [[summary|Summary]]
# JetXu-LLM/DocMason — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** DocMason is a local, repo-native agent app that compiles private Office/PDF/text work files into a file-based knowledge base with strict provenance so every answer is traceable to its source.
## Key points
- DocMason is a repo-native work system where the repo holds the truth and the agent (ChatGPT Work, Codex mode, or Claude Code) does the reasoning, with no hidden backends or cloud ingestion (README.md:39, README.md:106-109).
- Answers must be strictly traceable: the system compiles decks, spreadsheets, PDFs, and emails into structured, multimodal evidence bundles instead of flat text blobs (README.md:39, README.md:60).
- The runtime enforces strict data contracts and provenance boundaries, producing deterministic file-based evidence with offline retrieval/trace algorithms validated by code rules (README.md:45, README.md:60).
- Users start by dropping files into `DocMason/original_doc/` and either asking naturally (small corpora, background build) or explicitly staging folders then running environment prep plus knowledge-base build (README.md:71-80).
- On macOS the five-step path is download/unzip, open folder in ChatGPT Desktop, prepare environment, build knowledge base for medium-to-large corpora, then ask questions with exact source identity and provenance trace (README.md:102-136).
- Supported inputs are first-class Office/PDF (`pdf`, `pptx`, `ppt`, `docx`, `doc`, `xlsx`, `xls`), deep text (`md`, `markdown`, `txt`, `eml`), and lightweight text (`mdx`, `yaml`, `yml`, `tex`, `csv`, `tsv`), with LibreOffice required for Office fidelity and an embedded stack (`PyMuPDF`, `pypdfium2`, `pypdf`, `pillow`) for PDFs (README.md:170-174).
- DocMason itself makes zero model API calls and sends no document content, queries, or knowledge-base artifacts over the network; the only stated exception is a bounded update check by release bundles, whose description is truncated in the chunk (README.md:192-200).
## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The four top-level files define DocMason's agent routing contract, workspace configuration, privacy boundary, and what stays out of git.
## Key points
- `AGENTS.md` declares the repository itself is the canonical operating surface and source of truth, with files, directories, scripts, and skill contracts as the workflow boundaries and no hidden services assumed (AGENTS.md:7).
- `ask` at `skills/canonical/ask/SKILL.md` is the only default top-level workflow for ordinary natural-language requests, while bootstrap, doctor, status, knowledge-base sync, log review, adapter sync, and `docmason update-core` are explicit operator routes (AGENTS.md:20-38).
- The runtime trust boundary requires a repo-local `.venv` whose resolved base interpreter sits inside `.docmason/toolchain/python/`, treats only `self-contained` toolchain state as ask-ready, and prefers `./scripts/bootstrap-workspace.sh --yes` for first-run setup (AGENTS.md:71-80).
- `docmason.yaml` commits the workspace surface: `source_dir: original_doc`, `knowledge_base_dir: knowledge_base`, `runtime_dir: runtime`, `native_agent: codex`, `platform: macos`, `python_requires: ">=3.11"`, packaging primary `uv` with `pip` fallback (docmason.yaml:6-18).
- Ingestion supports `pdf`, `pptx`, `docx`, `xlsx`, `md`, `txt`, `eml`-adjacent text tiers plus lightweight `mdx`/`yaml`/`tex`/`csv`/`tsv`, with `multimodal_first: true`, deterministic preprocessing, and partial-failure tolerance (docmason.yaml:62-88).
- `.gitignore` keeps private and generated state out of git: `/original_doc/*`, `/knowledge_base/*`, `/runtime/*`, `/adapters/*` (each with a kept `.gitkeep`), plus `/.docmason/`, `/.agents/`, `/.venv/`, and env/editor/log noise (.gitignore:1-14, .gitignore:24-34, .gitignore:50-69).
- `SECURITY.md` states DocMason is built for private local documents and the tracked repo must not become a public store of corpus data, compiled KB artifacts, or runtime history, with no dedicated security mailbox, no SLA, and no bounty program (SECURITY.md:5-7, SECURITY.md:11-14, SECURITY.md:48-50).
## The system in five moves
1. Start from the thesis that answers over private work files must be strictly traceable, so the repo holds the truth and the agent does the reasoning with no hidden backend.
2. Drop Office/PDF/text files into `original_doc/` and enter through the small-corpus natural-ask path or the staged folder plus environment-prep and knowledge-base-build path.
3. Route every request through the `AGENTS.md` front door where `ask` is the only default workflow and bootstrap, doctor, status, sync, log-review, and adapter-sync are explicit operator routes.
4. Compile the corpus into a local file-based knowledge base of structured multimodal evidence bundles under committed `docmason.yaml` contracts (deterministic, multimodal-first, validation-gated) rather than flat text blobs.
5. Answer with exact source identity and provenance trace while keeping private corpus, KB artifacts, and runtime state local and out of git per `.gitignore`/`SECURITY.md`.
