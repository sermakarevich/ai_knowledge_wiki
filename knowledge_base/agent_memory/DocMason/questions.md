---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: JetXu-LLM/DocMason

### Q1. What is DocMason in one sentence, and what is its core thesis about traceability?
> [!tip]- Answer
> DocMason is a local, repo-native agent app that compiles private Office/PDF/text work files into a file-based knowledge base with strict provenance. Its thesis is that answers must be strictly traceable: the repo holds the truth while the agent (ChatGPT Work, Codex mode, or Claude Code) does the reasoning, with no hidden backends or cloud ingestion. It produces deterministic file-based evidence with offline retrieval/trace algorithms validated by code rules. See [[wiki/01-overview|Overview]].

### Q2. What four flat-text pipeline failures does DocMason claim to fix, and what does it build instead?
> [!tip]- Answer
> Flat-text pipelines discard slide-deck layout, notes, and chart-text relationships; break multi-sheet spreadsheet references and nested tables; erase format-as-semantics such as red "Risk" text or indentation hierarchies; and disconnect multi-part proposals so global synthesis is impossible. DocMason instead compiles decks, spreadsheets, PDFs, and emails into structured, multimodal evidence bundles that preserve original structure and visual semantics. It forces the AI to respect that structure rather than reasoning over stripped text blobs. See [[wiki/01-overview|Overview]].

### Q3. What are the two entry paths to a first answer, and what is the five-step macOS path?
> [!tip]- Answer
> Path A (Start Small) drops files into `DocMason/original_doc/`, opens the folder in ChatGPT Desktop Work, and asks naturally while DocMason builds the knowledge base in the background. Path B (Stage Entire Folders) drops department-level folders in, then runs the exact prompts "Please prepare the DocMason environment." and "Please build the knowledge base." before asking complex questions. On macOS the full path is download/unzip, open in ChatGPT Desktop, handle host hooks and trust, prepare the environment, then build for medium-to-large corpora and ask with exact source identity and provenance trace. See [[wiki/01-overview|Overview]].

### Q4. What does the ICO + GCS demo prove, and what makes DocMason feel safer than cloud ingestion?
> [!tip]- Answer
> The demo compiles official UK public-sector ICO + GCS releases and answers "what are the main rollout risks, and which sources support them?" with cross-document synthesis, explicit exact-document provenance, and real evidence bundles for root-context verification. Safety comes from strict source identity preventing cross-source hallucination, verifiable lineage to the exact file and page, and a 100% local auditable folder boundary. DocMason itself makes zero model API calls and sends no content, queries, or KB artifacts over the network, apart from a bounded update check whose full conditions are truncated in the chunk. See [[wiki/01-overview|Overview]].

### Q5. What is the AGENTS.md front-door routing contract, and what are its discovery and placement rules?
> [!tip]- Answer
> `ask` at `skills/canonical/ask/SKILL.md` is the only default workflow for ordinary natural-language requests; bootstrap, doctor, status, knowledge-base sync, log review, adapter sync, and `docmason update-core` are explicit operator routes. Live corpus discovery means repo-side enumeration of `original_doc/` (ignore-aware search like `rg --files` is invalid there), KB discovery inspects `knowledge_base/`, and runtime discovery inspects `runtime/`. Canonical answers go to `runtime/answers/` via helpers with drafts in `runtime/agent-work/`, never committed private inputs or scratch in the repo root, and the agent must stop rather than fake output if it cannot read files, run shell, inspect JSON, or view rendered images. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. What does docmason.yaml commit, and what stays out of git per .gitignore and SECURITY.md?
> [!tip]- Answer
> `docmason.yaml` commits `source_dir: original_doc`, `knowledge_base_dir: knowledge_base`, `runtime_dir: runtime`, `native_agent: codex`, `platform: macos`, Python `>=3.11` with `uv` primary and `pip` fallback, plus multimodal-first deterministic ingestion, heuristic-only trust model, validation-gated commits, and the phase roadmap. `.gitignore` keeps `/original_doc/*`, `/knowledge_base/*`, `/runtime/*`, `/adapters/*` (each with `.gitkeep`), `/.docmason/`, `/.venv/`, and env/editor/log noise out of git. `SECURITY.md` states the tracked repo must never store corpus data, KB artifacts, or runtime history, with no security mailbox, SLA, or bounty, and reports must use synthetic or redacted reproductions only. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Should a team handling confidential Office/PDF work adopt DocMason today, and why or why not?
> [!tip]- Answer
> Recommend a cautious pilot, not a broad rollout: adopt it where local-only provenance-traced answers over messy decks, spreadsheets, and emails outweigh the setup cost of LibreOffice, a managed Python toolchain, and ChatGPT Work/Codex host trust. Hold back on production dependence because the privacy update-check description is truncated in the digest, non-native and Windows paths carry noted risk differences, and there is no security mailbox, SLA, or bounty behind the private-local posture. Revisit full adoption after validating incremental sync, validation-gated builds, and host-agent retention behavior on the team's own corpus. See [[wiki/02-top-level-files|Top-level-files]].
