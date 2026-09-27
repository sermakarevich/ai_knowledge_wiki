> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** DocMason is a local, repo-native agent app that compiles private Office/PDF/text work files into a file-based knowledge base with strict provenance so every answer is traceable to its source.
## Key points
- DocMason is a repo-native work system where the repo holds the truth and the agent (ChatGPT Work, Codex mode, or Claude Code) does the reasoning, with no hidden backends or cloud ingestion (README.md:39, README.md:106-109).
- Answers must be strictly traceable: the system compiles decks, spreadsheets, PDFs, and emails into structured, multimodal evidence bundles instead of flat text blobs (README.md:39, README.md:60).
- The runtime enforces strict data contracts and provenance boundaries, producing deterministic file-based evidence with offline retrieval/trace algorithms validated by code rules (README.md:45, README.md:60).
- Users start by dropping files into `DocMason/original_doc/` and either asking naturally (small corpora, background build) or explicitly staging folders then running environment prep plus knowledge-base build (README.md:71-80).
- On macOS the five-step path is download/unzip, open folder in ChatGPT Desktop, prepare environment, build knowledge base for medium-to-large corpora, then ask questions with exact source identity and provenance trace (README.md:102-136).
- Supported inputs are first-class Office/PDF (`pdf`, `pptx`, `ppt`, `docx`, `doc`, `xlsx`, `xls`), deep text (`md`, `markdown`, `txt`, `eml`), and lightweight text (`mdx`, `yaml`, `yml`, `tex`, `csv`, `tsv`), with LibreOffice required for Office fidelity and an embedded stack (`PyMuPDF`, `pypdfium2`, `pypdf`, `pillow`) for PDFs (README.md:170-174).
- DocMason itself makes zero model API calls and sends no document content, queries, or knowledge-base artifacts over the network; the only stated exception is a bounded update check by release bundles, whose description is truncated in the chunk (README.md:192-200).
---
## Thesis and architecture
DocMason is positioned as "A repo-native agent app for deep research over private work files" where "The repo is the app. Codex is the runtime" and the goal is to "Build a local, evidence-first knowledge base with provenance" (README.md:9-11).
Verbatim thesis (README.md:39):
> **DocMason** is built on a different thesis: **answers must be strictly traceable.**
The runtime contract is (README.md:45):
> DocMason is designed to enforce strict data contracts and provenance boundaries. The repo holds the truth; the agent does the reasoning.
Architecture diagram reference (README.md:47):
> ![DocMason Architecture](./docs/architecture/architecture.svg)
## Problem it solves
Flat-text pipelines strip structural and visual semantics that DocMason preserves (README.md:53-58):
- **Slide Decks**: Visual layout, presenter notes, and chart-text relationships are discarded (README.md:55).
- **Spreadsheets**: Multi-sheet references and nested tables break existing parsers (README.md:56).
- **Format-as-Semantics**: Critical signals (like red text for "Risk" or indentation for hierarchies) are erased (README.md:57).
- **Cross-Document Reasoning**: Multi-part proposals are disconnected, making global synthesis impossible (README.md:58).
Counter-claim (README.md:60):
> DocMason addresses this by forcing AI to respect original document structure and visual semantics.
## Entry paths
Flow diagram reference (README.md:68):
> ![Two ways to reach your first answer](./docs/product/readme-first-minute-flow.svg)
| Path | Procedure (verbatim) |
|---|---|
| A: Start Small | Drop files into `DocMason/original_doc/`, open the folder in ChatGPT Desktop Work, ask naturally; DocMason guides environment setup, builds the knowledge base in the background, and can incrementally sync later additions instead of a full restart (README.md:71) |
| B: Stage Entire Folders | Drop department-level folders into `DocMason/original_doc/`, open in ChatGPT Desktop Work, then run `> "Please prepare the DocMason environment."` followed by `> "Please build the knowledge base."`, then ask complex questions against the published corpus (README.md:74-80) |
Note (README.md:82):
> *Inside a valid workspace, you do not need to memorize internal commands. Just speak naturally to your AI agent.*
## macOS setup (five steps)
1. Download, unzip, drop files into `DocMason/original_doc/` — supports `.pptx`, `.docx`, `.xlsx`, `.pdf`, and other work files (README.md:103).
2. Open the folder in ChatGPT Desktop using [Work](https://learn.chatgpt.com/docs/get-started-with-work); Codex mode stays for coding/operator/implementation-heavy tasks and Claude Code stays a supported host adapter (README.md:106-109).
3. Host hooks and trust: optional prompt-continuity/one-shot Hooks never own the workflow and `AGENTS.md` plus canonical skills complete the same work if Hooks are disabled; ChatGPT Work/Codex trusts the project `.codex` layer with per-definition review in `/hooks`, Claude Code uses folder trust plus `/hooks` inspection with `disableAllHooks` or `allowManagedHooksOnly` able to suppress them; `docmason doctor` verifies committed config and scripts but cannot grant host trust (README.md:111-121).
4. Prepare the environment with the exact prompt `> "Please prepare the DocMason environment."` — sets up a managed local Python environment, installs dependencies, guides LibreOffice installation, requires granting full access to Codex when prompted (README.md:124-126).
5. Build (medium-to-large corpora) with `> "Please build the knowledge base."` — stages, compiles, validates, and publishes documents into a searchable evidence layer; small corpora may build automatically on first question — then ask e.g. `> "What are the main rollout risks across these documents, and which sources support them?"` with exact source identity and provenance trace (README.md:129-136).
## Demo proof case
Public corpus: ICO + GCS demo bundle compiled from official UK public-sector releases (README.md:142). Test prompt (README.md:147):
> "Across the ICO and GCS materials, what are the main rollout risks, and which sources support them?"
Good-answer criteria (README.md:150-152):
- **Cross-Document Reasoning:** synthesizes overlapping governance risks instead of echoing documents one by one (README.md:150).
- **Strict Provenance:** explicitly points to the exact document origin (README.md:151).
- **Inherently Traceable:** provides the real evidence bundles for root-context verification (README.md:152).
## Safety, formats, and current features
Why it feels safer (README.md:160-164):
- **Strict Source Identity** prevents hallucinating cross-source facts (README.md:160).
- **Answers Are Traceable** with verifiable lineage to the exact file and page (README.md:161).
- **100% Local and Auditable** inside the local folder boundary (README.md:162).
- Install footprint: **[LibreOffice](https://www.libreoffice.org/)** for Office fidelity plus an automatic local Python environment (README.md:164).
What you get today (README.md:180-184):
- **Incremental Sync** rebuilds/republishes `knowledge_base/current/` on `original_doc/` changes without a full reset (README.md:180).
- **Validation-Gated Commits**: bad data fails the build (README.md:181).
- **Rich Source Parsing** for `.pdf`, `.pptx`, `.xlsx`, `.md`, `.eml`, and more (README.md:182).
- **Deterministic Retrieval** with exact provenance trace (README.md:183).
- **Review Surface** via conversation-native logging and extraction (README.md:184).
## Truncation note
The chunk truncates the Privacy section at line 200 mid-sentence — `Generated \`clean\` and \`demo-ico-gcs\` release bundles may perform a bounded update check only when you explici` (README.md:199-200) — so the full update-check conditions and anything after that line are not covered here; no file after `top-level-files/` (README.md:204) is in scope for this page.
**Covers:** `README.md` (repo purpose, architecture, setup, formats, privacy boundary as excerpted in chunk 01-overview); `top-level-files/` listed only as a macro-component pointer (README.md:202-204)
