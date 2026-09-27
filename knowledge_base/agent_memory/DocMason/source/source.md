# JetXu-LLM/DocMason
PDF: https://github.com/JetXu-LLM/DocMason (no source.pdf bundled with this run; use the source URL above)
Source: https://github.com/JetXu-LLM/DocMason
Kind: repo
Fetched: 2026-09-26T13:45:13.454232+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# JetXu-LLM/DocMason

Commit: cd5b129c7134d6bd9be191f681fbef8dfd20d716

## README

<div align="center">
  <h1>DocMason</h1>
  <p><strong>A repo-native agent app for deep research over private work files.</strong></p>
  <p>The repo is the app. Codex is the runtime.</p>
  <p>Build a local, evidence-first knowledge base with provenance.</p>
  
  <br>
  
  <p>
    <a href="https://github.com/JetXu-LLM/DocMason/releases/latest/download/DocMason-clean.zip">
      <img alt="Download DocMason" src="https://img.shields.io/badge/⬇️_Download_DocMason-0DAFC6?style=for-the-badge">
    </a>
  </p>
  
  <p>
    <img alt="Platform" src="https://img.shields.io/badge/platform-macOS-7959A2?style=flat-square&logo=apple&logoColor=white">
    <img alt="Supported formats" src="https://img.shields.io/badge/supported%20formats-Office%20%2F%20PDF%20%2F%20Text-0A8447?style=flat-square">
    <img alt="License" src="https://img.shields.io/badge/license-Apache%202.0-0F64B5?style=flat-square">
    <a href="https://github.com/JetXu-LLM/DocMason/releases">
      <img alt="Total downloads" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FJetXu-LLM%2FDocMason%2Fmain%2Fdocs%2Fbadges%2Fdownloads-endpoint.json&style=flat-square&v=3">
    </a>
  </p>
  
  <p><sub>
    Already paying for ChatGPT? Open <a href="https://learn.chatgpt.com/docs/get-started-with-work"><strong>ChatGPT Desktop Work</strong></a> and turn that capacity into a local Second Brain.<br>
    Watch the <a href="https://youtu.be/Sq3a5qxsLwM"><b>▶️ video demo</b></a> to see how DocMason performs deep research on local complex office files.<br>
    Get zero-to-working in minutes with this <a href="https://www.youtube.com/watch?v=jWRtr70Rvug"><b>▶️ 3-min setup tutorial video</b></a>.
  </sub></p>
</div>
<br>
Most workspace AI tools flatten your complex office documents into a single, unstructured text blob. They might summarize a file or retrieve a stray quote, but once your research gets complex, the illusion breaks. You lose the tables, the slide layouts, the hidden notes—and it becomes impossible to verify where the AI's answer actually came from.

**DocMason** is built on a different thesis: **answers must be strictly traceable.** It compiles your private decks, spreadsheets, PDFs, and emails into a local, file-based knowledge base. Instead of chatting with anonymous text chunks, your AI agent reasons over structured, multimodal evidence bundles. It’s not a cloud service or a lightweight wrapper. It is a local repo-native work system operated through ChatGPT Work, Codex mode, or Claude Code. No hidden backends, no cloud ingestion. Just your files, and answers you can actually trust.



## How It Works: A Production-Grade Runtime

DocMason is designed to enforce strict data contracts and provenance boundaries. The repo holds the truth; the agent does the reasoning.

![DocMason Architecture](./docs/architecture/architecture.svg)



## Why This Exists

Most document AI tools map complex corporate files into flat, unreadable text strings. They strip out critical structural and formatting semantics:

- **Slide Decks**: Visual layout, presenter notes, and chart-text relationships are discarded.
- **Spreadsheets**: Multi-sheet references and nested tables break existing parsers.
- **Format-as-Semantics**: Critical signals (like red text for "Risk" or indentation for hierarchies) are erased.
- **Cross-Document Reasoning**: Multi-part proposals are disconnected, making global synthesis impossible.

DocMason addresses this by forcing AI to respect original document structure and visual semantics. It produces deterministic file-based evidence, runs strong offline retrieval and trace algorithms, and validates the resulting knowledge base through strict code rules — all locally, with nothing leaving your machine. The repo holds the truth. The agent does the reasoning.



## Two Easy Ways to Start

Getting started requires zero developer experience. Just drop your files and let your AI agent handle the rest.

![Two ways to reach your first answer](./docs/product/readme-first-minute-flow.svg)

- **Path A: Start Small**
  Drop a handful of work files (`.pptx`, `.docx`, `.xlsx`, PDFs) into the `DocMason/original_doc/` folder. Open the DocMason folder in ChatGPT Desktop Work, and ask your question naturally. DocMason intelligently guides you through environment setup and quietly builds the knowledge base in the background — just approve when prompted. After that, you can keep adding or revising files inside `original_doc/`; on the native path, DocMason can quietly and incrementally sync the published knowledge base instead of forcing a full restart.

- **Path B: Stage Entire Folders**
  Drop your massive, department-level folders into `DocMason/original_doc/`. Open the DocMason folder in ChatGPT Desktop Work. Ask your agent:
  > "Please prepare the DocMason environment."

  Then:
  > "Please build the knowledge base."

  Once it's done, start asking complex research questions against the entire published corpus.

*Inside a valid workspace, you do not need to memorize internal commands. Just speak naturally to your AI agent.*



## Getting Started on macOS

**📺 Prefer a visual guide? Watch the 3-minute full setup tutorial video👇**

<a href="https://youtu.be/jWRtr70Rvug">
  <img src="https://img.youtube.com/vi/jWRtr70Rvug/maxresdefault.jpg" alt="DocMason Setup Tutorial" width="700">
</a>
<br>
<a href="https://youtu.be/jWRtr70Rvug">
  <img alt="Watch on YouTube" src="https://img.shields.io/badge/▶️_Click_to_Watch_the_3--min_Tutorial-0D3A69?style=for-the-badge&logo=youtube&logoColor=white">
</a>

<br>

**Five steps from download to your first traceable answer — no developer experience required.**

**1. Download, unzip, and drop in your files**
**[Download DocMason](https://github.com/JetXu-LLM/DocMason/releases/latest/download/DocMason-clean.zip)**, unzip it to any folder on your Mac, then drag your `.pptx`, `.docx`, `.xlsx`, `.pdf`, and other work files into `DocMason/original_doc/`.

**2. Open the DocMason folder in ChatGPT Desktop**
For ordinary document and professional work, open the folder in ChatGPT Desktop and use
[Work](https://learn.chatgpt.com/docs/get-started-with-work). Codex mode remains available for
coding, operator maintenance, and implementation-heavy tasks; Claude Code remains a supported
host adapter. This is the operating model — the repo is your app, the agent is your runtime.

DocMason ships optional prompt-continuity and one-shot completion Hooks for both hosts. They make
continuations smoother, but never own the workflow: if Hooks are untrusted, disabled, unsupported,
or blocked by policy, `AGENTS.md` and the canonical skills still complete the same work normally.

- **ChatGPT Work/Codex:** trust the project `.codex` layer and review each current Hook definition
  in `/hooks`. A new or changed definition is skipped until it is reviewed again.
- **Claude Code:** accept folder trust, then use `/hooks` to inspect the loaded project Hooks.
  `disableAllHooks` or managed `allowManagedHooksOnly` policy can suppress them.

`docmason doctor` verifies the committed configuration and executable scripts; no local command can
grant or prove host trust, so runtime activation remains visible in the host.

**3. Ask your agent to prepare the environment**
> "Please prepare the DocMason environment."

DocMason will set up a managed local Python environment, install required dependencies, and guide you through LibreOffice installation if it's not already present. Just **grant full access to Codex** when prompted.

**4. Build the knowledge base** *(for medium-to-large corpora)*
> "Please build the knowledge base."

DocMason stages, compiles, validates, and publishes your documents into a searchable evidence layer. For a small handful of files, DocMason may handle this step automatically during your first question.

**5. Start asking questions**
> "What are the main rollout risks across these documents, and which sources support them?"

Your answers come with exact source identity and provenance trace — you can verify every claim against the original file and page.



## The Public Proof Case (Demo Bundle)

If you want to see a rigorously traceable answer before using your own files, the fastest public proof uses the ICO + GCS demo corpus compiled from official UK public-sector releases.

[Try the ICO + GCS Demo Bundle](https://github.com/JetXu-LLM/DocMason/releases/latest/download/DocMason-demo-ico-gcs.zip) to test a governed truth environment before transitioning to your own private folders.

**Ask this through your AI agent:**
> "Across the ICO and GCS materials, what are the main rollout risks, and which sources support them?"

**What good looks like:**
- **Cross-Document Reasoning:** The answer synthesizes overlapping governance risks instead of echoing documents one by one.
- **Strict Provenance:** The answer explicitly points to the exact document origin, instead of blurring the corpus into one anonymous narrative.
- **Inherently Traceable:** It provides the real evidence bundles so you can verify the root context.



## Why It Feels Safer

DocMason is built for **deep research** over your real work files — where every answer must be **traceable** to its actual source.

* **Strict Source Identity.** DocMason enforces strict document boundaries. It prevents agents from hallucinating cross-source facts that only vaguely fit together.
* **Answers Are Traceable.** You don't just get convincing text. You get a verifiable lineage pointing directly to the exact file and page you dropped in.
* **100% Local and Auditable.** Your files, staged data, and compiled knowledge base remain physically inside your local folder boundary. [See more →](#privacy-and-local-first-boundary)

**What gets installed:** DocMason needs **[LibreOffice](https://www.libreoffice.org/)** to parse Office files (`.pptx`, `.docx`, `.xlsx`) with full fidelity — this is the most important external dependency. It also sets up a local Python environment automatically. All setup is handled through your AI agent — just approve installations when prompted.



## Supported Work File Types

- **First-Class Office & PDF**: `pdf`, `pptx`, `ppt`, `docx`, `doc`, `xlsx`, `xls`
- **First-Class Deep Text**: `md`, `markdown`, `txt`, `eml` (email)
- **Lightweight Text**: `mdx`, `yaml`, `yml`, `tex`, `csv`, `tsv`

High-fidelity Office file parsing relies on a lightweight local LibreOffice shim. PDF parsing uses the embedded stack (`PyMuPDF`, `pypdfium2`, `pypdf`, `pillow`). Together they preserve multimodal structure, layout, and sheet/page context for deeper analysis, not just plain-text extraction. Markdown, plain text, `.eml`, and the lightweight-compatible family do not require LibreOffice.



## What You Get Today

- **Incremental Sync**: Add or revise files in `original_doc/`, and DocMason can quietly rebuild and republish your local `knowledge_base/current/` without forcing a full reset.
- **Validation-Gated Commits**: Bad data fails the build instead of quietly degrading answers.
- **Rich Source Parsing**: First-class handling for `.pdf`, `.pptx`, `.xlsx`, `.md`, `.eml`, and more.
- **Deterministic Retrieval**: Exact provenance trace over published corpora.
- **Review Surface**: Conversation-native logging and extraction for real analysis.



## Privacy and Local-First Boundary

DocMason is designed to run entirely over local files. Here's exactly what that means:

**DocMason does NOT send any of the following over the network:**
- Your document content, file names, or file paths
- Your queries or answer text
- Any corpus data, evidence bundles, or knowledge-base artifacts

**All AI inference traffic** is handled by your chosen host agent (Codex, Claude Code, etc.) — DocMason itself makes zero model API calls. The network behavior of your AI agent is governed by that agent's own privacy and telemetry policy.

**The only network request DocMason may make:**
Generated `clean` and `demo-ico-gcs` release bundles may perform a bounded update check only when you explici

... (truncated, 2854 more characters)

## pyproject.toml

```
[build-system]
requires = ["hatchling>=1.27"]
build-backend = "hatchling.build"

[project]
name = "docmason"
version = "0.1.8"
description = "A Python-first, file-only, agent-native workspace for building multimodal knowledge bases from complex office documents."
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.11"
keywords = [
  "agents",
  "document-processing",
  "knowledge-base",
  "multimodal",
  "rag",
]
classifiers = [
  "Development Status :: 3 - Alpha",
  "Intended Audience :: Developers",
  "Intended Audience :: End Users/Desktop",
  "License :: OSI Approved :: Apache Software License",
  "Operating System :: MacOS",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
  "Topic :: Office/Business",
  "Topic :: Scientific/Engineering :: Artificial Intelligence",
  "Topic :: Software Development :: Libraries :: Python Modules",
]
dependencies = [
  "openpyxl>=3.1",
  "pillow>=11.0",
  "PyMuPDF>=1.25",
  "pypdf>=5.0",
  "pypdfium2>=4.30",
  "python-docx>=1.1",
  "python-pptx>=1.0",
]

[project.optional-dependencies]
dev = [
  "mypy>=1.11",
  "pytest>=8.3",
  "pytest-cov>=5.0",
  "ruff>=0.6",
]

[project.scripts]
docmason = "docmason.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/docmason"]

[tool.pytest.ini_options]
addopts = "-ra"
testpaths = ["tests"]

[tool.ruff]
line-length = 100
src = ["src", "tests"]
target-version = "py311"

[tool.ruff.lint]
select = ["B", "E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true
packages = ["docmason"]
warn_unused_configs = true

```

## Top-level layout

- .claude/ (dir, 6 files, ~188 lines)
- .codex/ (dir, 3 files, ~58 lines)
- .githooks/ (dir, 3 files, ~35 lines)
- .github/ (dir, 4 files, ~208 lines)
- .gitignore (~69 lines)
- adapters/ (dir, 1 files, ~1 lines)
- AGENTS.md (~121 lines)
- CONTRIBUTING.md (~82 lines)
- docmason.yaml (~111 lines)
- docs/ (dir, 20 files, ~1186 lines)
- knowledge_base/ (dir, 1 files, ~1 lines)
- LICENSE (~201 lines)
- ops/ (dir, 5 files, ~264 lines)
- original_doc/ (dir, 1 files, ~1 lines)
- pyproject.toml (~73 lines)
- README.md (~226 lines)
- runtime/ (dir, 1 files, ~1 lines)
- sample_corpus/ (dir, 18 files, ~2448 lines)
- scripts/ (dir, 9 files, ~2062 lines)
- SECURITY.md (~52 lines)
- skills/ (dir, 35 files, ~2323 lines)
- src/ (dir, 48 files, ~57771 lines)
- tests/ (dir, 30 files, ~30092 lines)

