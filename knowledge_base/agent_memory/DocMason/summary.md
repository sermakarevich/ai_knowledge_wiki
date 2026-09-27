# Technical Analysis: JetXu-LLM/DocMason

**Repository:** https://github.com/JetXu-LLM/DocMason
**Version analyzed:** unknown
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Flat-text ingestion pipelines discard the structural and visual semantics of office work files: slide decks lose layout, presenter notes, and chart-text relationships (README.md:55); spreadsheets lose multi-sheet references and nested-table structure (README.md:56); formatting-as-signal such as red text for risk or indentation for hierarchy is erased (README.md:57); multi-part proposals spanning files cannot be synthesised because cross-document links are dropped (README.md:58).

DocMason addresses this by compiling private Office/PDF/text work files into a local, file-based knowledge base of structured, multimodal evidence bundles with strict source identity and provenance, so each answer traces to an exact file and page (README.md:39, README.md:60, README.md:160-161). The repository itself is the application and operating surface; a host agent does the reasoning and there is no hidden backend or cloud ingestion (README.md:39, README.md:106-109, AGENTS.md:3-5). The primary user is an analyst or knowledge worker doing deep research over private, cross-file corporate materials on a local machine.

## 2. High-Level Architecture

```
original_doc/ (private corpus, git-ignored)
  │ drop .pdf/.pptx/.docx/.xlsx/.md/.eml/.csv/...
  ▼
Host agent runtime (ChatGPT Work / Codex mode / Claude Code) ──► canonical skills
  │ skills/canonical/ask, workspace-bootstrap, workspace-doctor,
  │ workspace-status, knowledge-base-sync, runtime-log-review, adapter-sync
  ▼
Toolchain + parsers (.docmason/toolchain/python/, .venv/, LibreOffice, PyMuPDF/pypdfium2/pypdf/pillow)
  │ stage → compile → validate → publish
  ▼
knowledge_base/current/ (published evidence layer + logical publish ledger)
  │
  ├─► runtime/answers/ + runtime/runs/ + runtime/logs/ (answers, runs, review surface)
  └─► runtime/control_plane/ (operator control plane)
```

Data flow: (1) user drops files or department folders into `original_doc/` (README.md:71, README.md:103); (2) the host agent, routed through canonical skills with `ask` as the only default front door (AGENTS.md:20-38), prepares a repo-local managed Python environment and checks LibreOffice and host trust (README.md:111-126, AGENTS.md:71-80); (3) the build stages, compiles (including PDF rendering and Office conversion), validates, and publishes documents into `knowledge_base/current/` as JSON-plus-markdown evidence bundles (README.md:129, docmason.yaml:25-32); (4) ordinary questions execute KB-first retrieval with deterministic offline trace algorithms validated by code rules, returning answers with exact source identity (README.md:45, README.md:60, README.md:183, AGENTS.md:92-110); (5) conversation-native logging and extraction write reviewable artifacts to `runtime/` while incremental sync rebuilds/republishes on `original_doc/` changes without a full reset (README.md:180, README.md:184, AGENTS.md:52-58); (6) validation gates commits so bad data fails the build instead of publishing (README.md:181, docmason.yaml:89-92).

Persistent state lives entirely in git-ignored file directories: `original_doc/`, `knowledge_base/`, `runtime/`, `adapters/`, plus `/.docmason/` and `/.venv/` (`.gitignore:1-14`, `.gitignore:24-34`, `.gitignore:50-69`, docmason.yaml:6-10). The tracked repo holds config, scripts, and skill contracts only (AGENTS.md:7, SECURITY.md:5-7).

## 3. The Evidence Bundle

The central concept is the evidence bundle: a deterministic, file-based compilation of a source document's text, structure, and rendered visual semantics into a JSON-plus-markdown artifact with preserved provenance boundaries, as opposed to a flat text chunk (README.md:45, README.md:60, docmason.yaml:25-32). Representation is committed in config: `multimodal: true`, `primary_artifact_shape: json-plus-markdown`, `publish_model: single-current-plus-logical-publish-ledger`, `preserve_unknown_boundaries: true` (docmason.yaml:25-32). Retention policy renders almost everything during analysis and prefers joint text-plus-image reading, with PDF renderers `pypdfium2`, `pypdf` and Office renderers `libreoffice-pdf`, `png-renders` (docmason.yaml:33-42).

Named kinds and inputs: ingestion tiers in `docmason.yaml:68-88` are `office_pdf: pdf, pptx, docx, xlsx`; `first_class_text: md, markdown, txt` (plus `.eml` as first-class message input per AGENTS.md:3-5); `lightweight_text: mdx, yaml, yml, tex, csv, tsv`; policy flags `multimodal_first: true`, `deterministic_preprocessing: true`, `partial_failure_tolerant: true`. Supported inputs enumerated for users are `pdf`, `pptx`, `ppt`, `docx`, `doc`, `xlsx`, `xls`, deep text `md`, `markdown`, `txt`, `eml`, and lightweight `mdx`, `yaml`, `yml`, `tex`, `csv`, `tsv` (README.md:170-174). Trust scoring over bundles is heuristic-only over `local_branch_depth`, `first_level_subtree_context`, `shared_ancestor_proximity`, `source_stability`, `corroboration`, `extraction_confidence`, `recency`, `graph_centrality`, `inferred_document_role` with `path_scope: local-branch-relative` (docmason.yaml:44-58).

Key query rule, verbatim (AGENTS.md:67-69):

> `ignore-aware repo search such as \`rg --files\` is not valid live-corpus discovery for \`original_doc/\``

Corpus discovery is repo-side enumeration of `original_doc/` regardless of git tracking; KB discovery inspects `knowledge_base/`; runtime discovery inspects `runtime/`; published truth means `knowledge_base/current/`, never `original_doc/` or `knowledge_base/staging/` (AGENTS.md:60-69, AGENTS.md:92-110).

## 4. LLM / External Service Integration

The repo itself calls no LLM or model API and sends no document content, queries, or knowledge-base artifacts over the network (README.md:192-200). All model reasoning is delegated to the host agent the user already runs: ChatGPT Desktop Work (default for document work), Codex mode (coding/operator/implementation-heavy tasks), or Claude Code as a supported host adapter (README.md:106-109). Generated `clean` and `demo-ico-gcs` release bundles may perform a bounded update check only under explicit conditions, but the chunk truncates that sentence mid-word so the full conditions are not covered here (README.md:199-200); generated bundles may also perform the bounded release-entry network call documented in `docs/policies/release-entry-and-networking.md` (SECURITY.md:40-43). Host agents have their own privacy and retention behaviour outside repo control (SECURITY.md:40-43).

No API keys or model-related env vars are named in the covered pages. The `.env` and `.env.*` ignore entries indicate local environment files exist, but no required/optional call matrix applies because the repo defines no provider calls of its own. The capability floor instead requires the host agent to read local files, run shell commands, inspect structured JSON, and inspect rendered images, else stop rather than produce degraded output (AGENTS.md:112-119).

## 5. The Knowledge-Base Build and Ask Workflow

Two entry paths converge on the same build-then-ask pipeline (README.md:68-80). Path A (small corpora): drop files into `original_doc/`, open the folder in ChatGPT Desktop Work, ask naturally; DocMason guides setup, builds in the background, and incrementally syncs later additions (README.md:71). Path B (department folders / medium-to-large corpora): stage folders, run environment prep, run the KB build, then ask complex questions (README.md:74-80). Inside a valid workspace no internal commands need memorising; natural language suffices (README.md:82).

Step by step: (1) Download, unzip, drop files into `DocMason/original_doc/` — `.pptx`, `.docx`, `.xlsx`, `.pdf`, other work files (README.md:103). (2) Open the folder in ChatGPT Desktop Work; Codex mode and Claude Code remain available for their respective roles (README.md:106-109). (3) Establish host trust and hooks: prompt-continuity/one-shot Hooks never own the workflow and `AGENTS.md` plus canonical skills complete the same work if Hooks are disabled; ChatGPT Work/Codex trusts the project `.codex` layer with per-definition review in `/hooks`; Claude Code uses folder trust plus `/hooks` inspection with `disableAllHooks` or `allowManagedHooksOnly` able to suppress them; `docmason doctor` verifies committed config and scripts but cannot grant host trust (README.md:111-121). (4) Prepare the environment with the exact prompt `> "Please prepare the DocMason environment."`, which sets up the managed local Python environment, installs dependencies, and guides LibreOffice installation (README.md:124-126, AGENTS.md:71-80). (5) Build with `> "Please build the knowledge base."`, which stages, compiles, validates, and publishes into a searchable evidence layer; small corpora may build automatically on first question (README.md:129-136). (6) Ask with provenance, e.g. `> "What are the main rollout risks across these documents, and which sources support them?"`, evaluated on cross-document synthesis, strict provenance, and traceable evidence bundles (README.md:129-152). (7) Sync and review: incremental sync rebuilds/republishes `knowledge_base/current/` on `original_doc/` changes (README.md:180); canonical answers land under `runtime/answers/` via helpers and drafts under `runtime/agent-work/` (AGENTS.md:92-110); runtime failures route to `skills/canonical/runtime-log-review/SKILL.md` and readiness to `skills/canonical/workspace-doctor/SKILL.md` (AGENTS.md:20-38).

Every function-level reference available in the covered pages is a skill route or CLI entry rather than a Python function: `skills/canonical/ask/SKILL.md` (AGENTS.md:20-38), `skills/canonical/workspace-bootstrap/SKILL.md` (AGENTS.md:20-38), `skills/canonical/workspace-doctor/SKILL.md` (AGENTS.md:20-38), `skills/canonical/workspace-status/SKILL.md` (AGENTS.md:20-38), `skills/canonical/knowledge-base-sync/SKILL.md` (AGENTS.md:20-38), `skills/canonical/runtime-log-review/SKILL.md` (AGENTS.md:20-38), `skills/canonical/adapter-sync/SKILL.md` (AGENTS.md:20-38), `./scripts/bootstrap-workspace.sh --yes` (AGENTS.md:71-80), `docmason doctor` (README.md:111-121), `docmason update-core` (AGENTS.md:20-38).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | whole (cited 9-200) | Product thesis, architecture reference, entry paths, macOS setup, formats, privacy boundary |
| `AGENTS.md` | whole (cited 3-119) | Agent identity, front-door routing, discovery/trust/evidence/placement rules, capability floor |
| `docmason.yaml` | whole (cited 6-110) | Committed workspace, environment, KB, trust, agents, ingestion, quality, roadmap config |
| `SECURITY.md` | whole (cited 5-53) | Private-local posture, disclosure procedure, scope and limitations |
| `.gitignore` | whole (cited 1-69) | Keeps corpus, KB, runtime, adapters, toolchain, and scratch out of git |
| `skills/canonical/ask/SKILL.md` | n/a (routed at AGENTS.md:20-38) | Only default workflow for ordinary natural-language requests |
| `skills/canonical/workspace-bootstrap/SKILL.md` | n/a (routed at AGENTS.md:20-38) | Workspace prepare/initialise route |
| `skills/canonical/workspace-doctor/SKILL.md` | n/a (routed at AGENTS.md:20-38) | Readiness diagnostics route |
| `skills/canonical/workspace-status/SKILL.md` | n/a (routed at AGENTS.md:20-38) | Current stage / pending actions route |
| `skills/canonical/knowledge-base-sync/SKILL.md` | n/a (routed at AGENTS.md:20-38) | KB refresh / incremental sync route |
| `skills/canonical/runtime-log-review/SKILL.md` | n/a (routed at AGENTS.md:20-38) | Runtime failure and log review route |
| `skills/canonical/adapter-sync/SKILL.md` | n/a (routed at AGENTS.md:20-38) | Generated host-adapter refresh route |
| `scripts/bootstrap-workspace.sh` | n/a (invoked at AGENTS.md:71-80) | Preferred first-run toolchain setup (`--yes`) |
| `docs/architecture/architecture.svg` | n/a (referenced at README.md:47) | Architecture diagram |
| `docs/product/readme-first-minute-flow.svg` | n/a (referenced at README.md:68) | Entry-path flow diagram |
| `docs/policies/release-entry-and-networking.md` | n/a (referenced at SECURITY.md:40-43) | Bounded release-entry network call policy |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `python` | `>=3.11` (docmason.yaml:12-18) | Reference interpreter; repo-local resolved base must sit inside `.docmason/toolchain/python/` (AGENTS.md:71-80) |
| `uv` | primary packaging tool, no version string given (docmason.yaml:12-18) | Preferred installer for the managed local Python environment |
| `pip` | fallback packaging tool, no version string given (docmason.yaml:12-18) | Fallback installer when `uv` is unavailable |
| `PyMuPDF` | no version string given in covered pages (README.md:170-174) | Embedded PDF parsing/rendering |
| `pypdfium2` | no version string given (README.md:170-174; docmason.yaml:33-42) | PDF renderer |
| `pypdf` | no version string given (README.md:170-174; docmason.yaml:33-42) | PDF renderer/parser |
| `pillow` | no version string given (README.md:170-174) | Image handling for multimodal renders |
| `LibreOffice` | system install, no version string given (README.md:164, README.md:170-174) | Office-fidelity conversion (`libreoffice-pdf`, `png-renders` per docmason.yaml:33-42) |

## 8. CLI / Usage Surface

Entry points: natural-language prompts inside the host agent (default), the stable `docmason` CLI for operator commands, and canonical skill files for explicit routes (AGENTS.md:20-38, AGENTS.md:81-88).

| Command / prompt | Effect |
|---|---|
| `> "Please prepare the DocMason environment."` (README.md:124-126) | Sets up managed local Python env, installs deps, guides LibreOffice install |
| `> "Please build the knowledge base."` (README.md:129) | Stages, compiles, validates, publishes corpus into searchable evidence layer |
| Natural question, e.g. `> "What are the main rollout risks across these documents, and which sources support them?"` (README.md:129-136) | KB-first answer with exact source identity and provenance trace |
| `docmason doctor` (README.md:111-121) | Verifies committed config and scripts; cannot grant host trust |
| `docmason update-core` (AGENTS.md:20-38) | In-place release-bundle update |
| `docmason` with `--json` (AGENTS.md:81-88) | Machine-readable output; reuse stable CLI, do not invent public commands |
| `./scripts/bootstrap-workspace.sh --yes` (AGENTS.md:71-80) | Preferred first-run toolchain setup |

| Env var | Required? | Meaning (per covered pages) |
|---|---|---|
| (none named) | n/a | `.env` / `.env.*` are git-ignored local/machine entries (`.gitignore:49-54`), but no specific variable is named in the covered pages |

| Config key (docmason.yaml) | Value |
|---|---|
| `workspace.source_dir` / `knowledge_base_dir` / `runtime_dir` | `original_doc` / `knowledge_base` / `runtime` (docmason.yaml:6-10) |
| `reference_environment` | `native_agent: codex`, `platform: macos`, `python_requires: ">=3.11"`, `primary: uv`, `fallback: pip` (docmason.yaml:12-18) |
| `project` | `language_policy: english-only`, `implementation_bias: python-first`, `persistence_model: file-only` (docmason.yaml:20-23) |
| `knowledge_base` | `multimodal: true`, `json-plus-markdown`, `single-current-plus-logical-publish-ledger` (docmason.yaml:25-32) |
| `quality` | `validation_gate_required: true`, `publish_on_validation_success: true`, `prefer_explicit_failure_over_weak_fallback: true` (docmason.yaml:89-92) |

## 9. Extensibility Points

- New host agent support: add generated adapters under `adapters/` and refresh via `skills/canonical/adapter-sync/SKILL.md`; native reference workflow is `codex-macos` with targets `claude-code`, `github-copilot` (docmason.yaml:60-67, AGENTS.md:20-38). `adapters/` is git-ignored (`.gitignore:1-14`).
- New document type or parser: extend the ingestion tiers and flags in `docmason.yaml` (`office_pdf`, `first_class_text`, `lightweight_text`, `multimodal_first`, `deterministic_preprocessing`, `partial_failure_tolerant`, docmason.yaml:68-88) plus the corresponding compiler/render path behind the `libreoffice-pdf` / `png-renders` / `pypdfium2` / `pypdf` evidence-retention config (docmason.yaml:33-42).
- New operator workflow: add a canonical skill under `skills/canonical/` and register its route in `AGENTS.md` front-door table; `ask` remains the only ordinary front door (AGENTS.md:20-38). Private experiments go in `/skills/private/` and `/scripts/private/`, which are git-ignored (`.gitignore:10-24`).
- New trust signal or quality gate: extend `trust_model` inputs in `docmason.yaml:44-58` and the `quality` gate flags in `docmason.yaml:89-92`.
- New roadmap phase: follow the `roadmap` chain in `docmason.yaml:94-97` (completed spreadsheet/multimodal deepening, follow-on hybrid-PDF parity, next governed interaction memory and operator control plane).

## 10. Limitations and Gotchas

- **Privacy section is truncated, so the update-check contract is incomplete.** The chunk cuts the Privacy section mid-sentence at `README.md:199-200`, leaving the bounded update-check conditions and everything after `top-level-files/` (`README.md:204`) uncovered; do not assume the network boundary beyond what is stated.
- **`rg --files` and other ignore-aware search miss the live corpus.** `original_doc/` contents are git-ignored by design, so the non-negotiable rule is that ignore-aware repo search is not valid live-corpus discovery; enumerate `original_doc/` repo-side instead (AGENTS.md:67-69, `.gitignore:1-14`).
- **macOS + Codex native bias; other paths carry different risk.** Reference environment is `native_agent: codex`, `platform: macos` (docmason.yaml:12-18); non-native and Windows paths may carry different risk and there is no formal SLA (SECURITY.md:52-53).
- **`docmason doctor` cannot fix host trust.** It verifies committed config and scripts but per-definition review in `/hooks` (Codex) or folder trust plus `/hooks` inspection (Claude Code) must still be granted by the operator (README.md:111-121).
- **Heavy local toolchain is mandatory, not optional.** Office fidelity requires a LibreOffice install plus an automatic local Python environment with PDF/image stack (`PyMuPDF`, `pypdfium2`, `pypdf`, `pillow`) (README.md:164, README.md:170-174); the host agent must also clear the capability floor (file reading, shell, JSON, rendered-image inspection) or stop rather than degrade (AGENTS.md:112-119).
- **Security process is minimal.** No dedicated private security mailbox, no response SLA, no bounty; reporters must open a minimal public issue to request a private channel and use only synthetic or redacted reproductions (SECURITY.md:11-27, SECURITY.md:48-53).

## 11. How It Compares to Alternatives

- **NotebookLM (Google):** hosted, cloud-ingestion notebook with cited answers over uploaded sources; DocMason inverts this with a repo-local, file-only KB and no document content leaving the machine (README.md:162, README.md:192-200).
- **AnythingLLM:** self-hostable RAG desktop/server with vector store and multi-provider LLM wiring; DocMason instead delegates all reasoning to an external host agent, keeps retrieval deterministic and file-based, and gates publishing on validation rather than embedding similarity (README.md:45, README.md:183, AGENTS.md:3-5).
- **PrivateGPT:** local RAG over private files with pluggable LLM/vector backends; DocMason differs by compiling structure-preserving multimodal evidence bundles (layout, notes, chart-text, sheet references) instead of flat text chunks, with heuristic trust signals rather than vector scores (README.md:53-60, docmason.yaml:44-58).
- **Dify / LangChain-based RAG stacks:** framework or platform for building API-driven retrieval pipelines with hosted orchestration; DocMason is a fixed repo-native workspace where the repo holds the truth, state is plain files under `original_doc/` / `knowledge_base/current/` / `runtime/`, and the only default workflow is the canonical `ask` skill (AGENTS.md:7, AGENTS.md:20-38, docmason.yaml:6-10).

Positioning: DocMason trades hosted convenience and vector-recall breadth for local auditability, structural fidelity, and strict provenance — suited to private multi-file office corpora where every claim must resolve to an exact source.

## Appendix: Selected Code Snippets

1. Runtime contract (README.md:45):

> DocMason is designed to enforce strict data contracts and provenance boundaries. The repo holds the truth; the agent does the reasoning.

2. Agent identity (AGENTS.md:3-5):

> `DocMason is a repo-native application workspace. The agent is the runtime.`
> `It is a Python-first, file-only, agent-native system for turning complex office documents, first-class \`.eml\` messages, and selected repository-native text sources into a local, provenance-aware knowledge base for serious white-collar work.`

3. Private-local posture (SECURITY.md:5-7):

> `DocMason is built for private local documents. Security and privacy are core product boundaries, not optional extras.`

4. Untracked private/generated roots (.gitignore:1-14):

> `/original_doc/*`, `!/original_doc/.gitkeep`, `/knowledge_base/*`, `!/knowledge_base/.gitkeep`, `/runtime/*`, `!/runtime/.gitkeep`, `/adapters/*`, `!/adapters/.gitkeep`
