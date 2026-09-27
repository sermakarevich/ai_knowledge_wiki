> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The four top-level files define DocMason's agent routing contract, workspace configuration, privacy boundary, and what stays out of git.
## Key points
- `AGENTS.md` declares the repository itself is the canonical operating surface and source of truth, with files, directories, scripts, and skill contracts as the workflow boundaries and no hidden services assumed (AGENTS.md:7).
- `ask` at `skills/canonical/ask/SKILL.md` is the only default top-level workflow for ordinary natural-language requests, while bootstrap, doctor, status, knowledge-base sync, log review, adapter sync, and `docmason update-core` are explicit operator routes (AGENTS.md:20-38).
- The runtime trust boundary requires a repo-local `.venv` whose resolved base interpreter sits inside `.docmason/toolchain/python/`, treats only `self-contained` toolchain state as ask-ready, and prefers `./scripts/bootstrap-workspace.sh --yes` for first-run setup (AGENTS.md:71-80).
- `docmason.yaml` commits the workspace surface: `source_dir: original_doc`, `knowledge_base_dir: knowledge_base`, `runtime_dir: runtime`, `native_agent: codex`, `platform: macos`, `python_requires: ">=3.11"`, packaging primary `uv` with `pip` fallback (docmason.yaml:6-18).
- Ingestion supports `pdf`, `pptx`, `docx`, `xlsx`, `md`, `txt`, `eml`-adjacent text tiers plus lightweight `mdx`/`yaml`/`tex`/`csv`/`tsv`, with `multimodal_first: true`, deterministic preprocessing, and partial-failure tolerance (docmason.yaml:62-88).
- `.gitignore` keeps private and generated state out of git: `/original_doc/*`, `/knowledge_base/*`, `/runtime/*`, `/adapters/*` (each with a kept `.gitkeep`), plus `/.docmason/`, `/.agents/`, `/.venv/`, and env/editor/log noise (.gitignore:1-14, .gitignore:24-34, .gitignore:50-69).
- `SECURITY.md` states DocMason is built for private local documents and the tracked repo must not become a public store of corpus data, compiled KB artifacts, or runtime history, with no dedicated security mailbox, no SLA, and no bounty program (SECURITY.md:5-7, SECURITY.md:11-14, SECURITY.md:48-50).
---
## .gitignore — what stays untracked
Private/generated roots are ignored but keep their directory placeholders (`.gitignore:1-14`):
> `/original_doc/*`, `!/original_doc/.gitkeep`, `/knowledge_base/*`, `!/knowledge_base/.gitkeep`, `/runtime/*`, `!/runtime/.gitkeep`, `/adapters/*`, `!/adapters/.gitkeep`
Also ignored (`.gitignore:10-24`):
> `/planning/`, `/evals/*`, `/scripts/private/`, `/skills/private/`, `/IMPLEMENTATION_PLAN.md`, `/.agents/`, `/.github/skills/`, `/.claude/skills`, `/.docmason/`
Toolchain, Python, local, and noise entries:
| Group | Entries |
|---|---|
| Python envs/build | `/.venv/`, `/venv/`, `/env/`, `/build/`, `/dist/`, `/*.egg-info/`, `/.pytest_cache/`, `/.ruff_cache/`, `/.mypy_cache/`, `/.coverage*`, `/coverage.xml`, `/htmlcov/`, `/.hypothesis/`, `/.tox/`, `/.nox/`, `/.cache/` (.gitignore:26-43) |
| Bytecode | `__pycache__/`, `*.py[cod]` (.gitignore:45-47) |
| Local/machine | `.env`, `.env.*`, `.python-version`, `.direnv/`, `.envrc` (.gitignore:49-54) |
| macOS/editor | `.DS_Store`, `.idea/`, `.vscode/` (.gitignore:56-59) |
| Logs/scratch | `*.log`, `*.tmp`, `*.swp`, `*.download`, `*.part`, `*.orig`, `*.rej`, `*.bak` (.gitignore:61-69) |
## AGENTS.md — agent routing contract
Verbatim thesis (AGENTS.md:3-5):
> `DocMason is a repo-native application workspace. The agent is the runtime.`
> `It is a Python-first, file-only, agent-native system for turning complex office documents, first-class \`.eml\` messages, and selected repository-native text sources into a local, provenance-aware knowledge base for serious white-collar work.`
Identity (AGENTS.md:12-18): canonical workspace-agent identity is `DocMason`; the exact default self-reference wording is:
> `I am DocMason, a repo-native multimodal AI agent for serious private document work. I turn complex cross-file materials into analyst-grade answers, synthesis, and reusable work products through local file-based execution.`
Front-door routing table (AGENTS.md:20-38):
| Request | Route |
|---|---|
| Ordinary natural-language request (default) | `skills/canonical/ask/SKILL.md` (only ordinary front door) |
| Prepare/initialize workspace | `skills/canonical/workspace-bootstrap/SKILL.md` |
| Diagnose readiness | `skills/canonical/workspace-doctor/SKILL.md` |
| Current stage / pending actions | `skills/canonical/workspace-status/SKILL.md` |
| Refresh knowledge base | `skills/canonical/knowledge-base-sync/SKILL.md` |
| Runtime failures / logs | `skills/canonical/runtime-log-review/SKILL.md` |
| Refresh generated adapters | `skills/canonical/adapter-sync/SKILL.md` |
| In-place release bundle update | `docmason update-core` |
First-contact signs (AGENTS.md:52-58): canonical `ask` really opened when the request leaves linked runtime artifacts, typically under `runtime/answers/`, `runtime/runs/`, `runtime/logs/`; `published KB` means `knowledge_base/current/`; `control-plane` means `runtime/control_plane/`.
Discovery boundaries (AGENTS.md:60-69): tracked search covers committed files; live corpus discovery is repo-side enumeration of `original_doc/` regardless of git tracking; KB discovery inspects `knowledge_base/`; runtime discovery inspects `runtime/`; non-negotiable rule:
> `ignore-aware repo search such as \`rg --files\` is not valid live-corpus discovery for \`original_doc/\`` (AGENTS.md:67-69)
Stable surface (AGENTS.md:81-88): reuse the stable `docmason` CLI, prefer `--json`, do not invent public commands; `ask` is exposed through the canonical skill, not as a public CLI command; stable output/docs/code stay English.
Evidence and placement (AGENTS.md:92-110): smallest sufficient evidence scope; KB-first; do not treat `original_doc/` or `knowledge_base/staging/` as published truth; never commit/expose private inputs, KB artifacts, runtime state, or adapters; `original_doc/` only for explicit future corpus input; `runtime/answers/` for canonical answers via helpers; `runtime/agent-work/` for drafts/scratch; never drop scratch in repo root or temp files under `knowledge_base/` or `adapters/`.
Capability floor (AGENTS.md:112-119): must read local files, run shell commands, inspect structured JSON, and inspect rendered images for multimodal work — else stop and explain rather than produce degraded pretend output.
## docmason.yaml — committed configuration
Top-level keys: `workspace`, `reference_environment`, `project`, `knowledge_base`, `trust_model`, `agents`, `ingestion`, `quality`, `roadmap` (docmason.yaml:6-110).
| Section | Exact values |
|---|---|
| `workspace` | `source_dir: original_doc`, `sample_corpus_dir: sample_corpus`, `knowledge_base_dir: knowledge_base`, `runtime_dir: runtime` (docmason.yaml:6-10) |
| `reference_environment` | `native_agent: codex`, `platform: macos`, `python_requires: ">=3.11"`, package `primary: uv`, `fallback: pip` (docmason.yaml:12-18) |
| `project` | `language_policy: english-only`, `implementation_bias: python-first`, `persistence_model: file-only` (docmason.yaml:20-23) |
| `knowledge_base` | `multimodal: true`, `primary_artifact_shape: json-plus-markdown`, `bilingual_outputs: false`, `publish_model: single-current-plus-logical-publish-ledger`, `preserve_unknown_boundaries: true` (docmason.yaml:25-32) |
| Evidence retention | `strategy: adaptive`, `render_during_analysis: almost-everything`, `prefer_joint_text_plus_image_reading: true`; PDF renderers `pypdfium2`, `pypdf`; office renderers `libreoffice-pdf`, `png-renders` (docmason.yaml:33-42) |
| `trust_model` | `strategy: heuristic-only`, `path_scope: local-branch-relative`, inputs: `local_branch_depth`, `first_level_subtree_context`, `shared_ancestor_proximity`, `source_stability`, `corroboration`, `extraction_confidence`, `recency`, `graph_centrality`, `inferred_document_role` (docmason.yaml:44-58) |
| `agents` | `canonical_contract: AGENTS.md`, `canonical_skills_dir: skills/canonical`, `generated_adapters_dir: adapters`, `native_reference_workflow: codex-macos`, targets `claude-code`, `github-copilot` (docmason.yaml:60-67) |
| `quality` | `validation_gate_required: true`, `publish_on_validation_success: true`, `prefer_explicit_failure_over_weak_fallback: true` (docmason.yaml:89-92) |
| `roadmap` | completed `phase-3-spreadsheet-and-multimodal-evidence-compiler-deepening`, follow-on `hybrid-pdf-parity-and-multimodal-kb-deepening`, next `phase-4-governed-interaction-memory-and-operator-control-plane` (docmason.yaml:94-97) |
Ingestion tiers (docmason.yaml:68-88): `office_pdf: pdf, pptx, docx, xlsx`; `first_class_text: md, markdown, txt`; `lightweight_text: mdx, yaml, yml, tex, csv, tsv`; policy `multimodal_first: true`, `deterministic_preprocessing: true`, `partial_failure_tolerant: true`.
## SECURITY.md — private-local posture
Posture (SECURITY.md:5-7):
> `DocMason is built for private local documents. Security and privacy are core product boundaries, not optional extras.`
Reporting (SECURITY.md:11-18): no dedicated private security mailbox yet; do not post exploits publicly or attach private documents, KB artifacts, or runtime logs; open a minimal public issue only to request a private disclosure channel.
Include `affected version, commit, or bundle channel`, `host environment and platform`, `concise reproduction steps using synthetic or redacted data`, `impact summary and any obvious mitigation` (SECURITY.md:22-27); never include confidential source documents, pasted KB outputs, runtime artifacts with business data, secrets, tokens, or sensitive screenshots (SECURITY.md:31-36).
Scope (SECURITY.md:40-43): repo runs locally; generated bundles may perform the bounded release-entry network call documented in `docs/policies/release-entry-and-networking.md`; host agents (Codex, Claude Code, GitHub Copilot) have their own privacy/retention behavior outside repo control. Disclosure prefers synthetic/redacted reproductions and private discussion for data or update-integrity risk (SECURITY.md:45-50). Limitations: no formal response SLA, no bounty, non-native/Windows paths may carry different risk (SECURITY.md:52-53).
**Covers:** `.gitignore` (ignore rules for private, generated, toolchain, and scratch paths); `AGENTS.md` (identity, front-door routing, discovery, trust, evidence, and placement rules); `docmason.yaml` (workspace, environment, KB, trust, agents, ingestion, quality, roadmap config); `SECURITY.md` (private-local posture, reporting, and scope notes)
