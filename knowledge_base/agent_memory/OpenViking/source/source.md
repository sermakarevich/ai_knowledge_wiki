> PDF location: https://github.com/volcengine/OpenViking (no source.pdf fetched; see Source field below)
# volcengine/OpenViking
Source: https://github.com/volcengine/OpenViking
Kind: repo
Fetched: 2026-09-26T13:41:08.514625+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# volcengine/OpenViking

Commit: a09a9d20a8e07d08973aee177802d00e08df29e6

## README

### OpenViking: The Context Database for AI Agents

English / [中文](README_CN.md) / [日本語](README_JA.md)

<a href="https://www.openviking.ai">Website</a> · <a href="https://openviking.ai/studio">Live Demo</a> · <a href="https://github.com/volcengine/OpenViking">GitHub</a> · <a href="https://github.com/volcengine/OpenViking/issues">Issues</a> · <a href="https://docs.openviking.ai/">Docs</a>

<p>
  <a href="https://github.com/volcengine/OpenViking/releases"><img src="https://img.shields.io/github/v/release/volcengine/OpenViking?color=369eff&labelColor=black&logo=github&style=flat-square" alt="release"></a>
  <a href="https://github.com/volcengine/OpenViking"><img src="https://img.shields.io/github/stars/volcengine/OpenViking?labelColor&style=flat-square&color=ffcb47" alt="stars"></a>
  <a href="https://github.com/volcengine/OpenViking/issues"><img src="https://img.shields.io/github/issues/volcengine/OpenViking?labelColor=black&style=flat-square&color=ff80eb" alt="issues"></a>
  <a href="https://github.com/volcengine/OpenViking/graphs/contributors"><img src="https://img.shields.io/github/contributors/volcengine/OpenViking?color=c4f042&labelColor=black&style=flat-square" alt="contributors"></a>
  <a href="https://github.com/volcengine/OpenViking/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-AGPLv3-white?labelColor=black&style=flat-square" alt="license"></a>
  <a href="https://github.com/volcengine/OpenViking/commits/main"><img src="https://img.shields.io/github/last-commit/volcengine/OpenViking?color=c4f042&labelColor=black&style=flat-square" alt="last commit"></a>
</p>

<p>
  <a href="https://railway.com/deploy/openviking"><img src="https://railway.com/button.svg" alt="Deploy on Railway" height="30"></a>
</p>

<p>
  <a href="https://docs.openviking.ai/en/about/01-about-us#lark-group"><img src="docs/images/community/lark.svg" width="18" height="18" alt="Lark">&nbsp;Lark</a> ·
  <a href="https://docs.openviking.ai/en/about/01-about-us#wechat-group"><img src="docs/images/community/wechat.svg" width="18" height="18" alt="WeChat">&nbsp;WeChat</a> ·
  <a href="https://discord.com/invite/eHvx8E9XF3"><img src="docs/images/community/discord.svg" width="18" height="18" alt="Discord">&nbsp;Discord</a> ·
  <a href="https://x.com/openvikingai"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/images/community/x-dark.svg"><img src="docs/images/community/x.svg" width="16" height="16" alt="X"></picture>&nbsp;X</a>
</p>

<a href="https://trendshift.io/repositories/19668" target="_blank"><img src="https://trendshift.io/api/badge/repositories/19668" alt="volcengine%2FOpenViking | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

</div>

***



## What is OpenViking

OpenViking is an open-source context database for AI agents — one filesystem for everything an agent knows: knowledge, memory, and skills.

Most agent memory is a black box: text goes in, embeddings come out, and nobody can see what was actually stored. OpenViking organizes context as a virtual filesystem under `viking://` instead. Agents navigate it like files — `ls`, `tree`, `read`, `write`, `grep` — and you can open any directory to inspect and edit what your agent knows. Every directory carries a generated summary, so agents can scan summaries first and decide what to read.

<a href="https://openviking.ai/studio" target="_blank" rel="noopener noreferrer">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/images/studio-playground-dark.png">
    <img src="docs/images/studio-playground.png" alt="OpenViking Studio: browse context and try semantic search">
  </picture>
</a>

[Try OpenViking Studio](https://openviking.ai/studio) in your browser, no installation required. [Self-host Web Studio](web-studio/README.md).



## Why OpenViking

- **One filesystem for knowledge, memory, and skills.** Resources hold documents and code; memories retain user preferences and experience; skills define how to perform tasks — not just extracted facts, but the full context, each with a `viking://` URI for browsing and retrieval. → [Viking URI](https://docs.openviking.ai/en/concepts/04-viking-uri) · [Context types](https://docs.openviking.ai/en/concepts/02-context-types)
- **Search a directory, not the whole index.** Scope semantic search to a project or memory subtree instead of scanning a flat vector pool. `find` runs a query directly; `search` plans retrieval from session context. → [Retrieval](https://docs.openviking.ai/en/concepts/07-retrieval)
- **Read the summary before the source.** Generated directory abstracts (L0) and overviews (L1) let agents judge relevance before opening full content (L2). → [Context layers](https://docs.openviking.ai/en/concepts/03-context-layers)
- **Sessions become files you can read.** Committing a session archives the conversation and extracts memories as Markdown you can inspect, edit, and merge. With VikingBot enabled, `ov compile` organizes source material into a wiki, knowledge graph, or report. → [Sessions](https://docs.openviking.ai/en/concepts/08-session) · [Context compilation](https://docs.openviking.ai/en/context-compilation/01-overview)

[Architecture](https://docs.openviking.ai/en/concepts/01-architecture) · [Design rationale](https://blog.openviking.ai/post/openviking-context-database/)

```
viking://
├── resources/              # Resources: project docs, repos, web pages, etc.
│   └── my_project/
│       ├── docs/
│       │   ├── api/
│       │   └── tutorials/
│       └── src/
└── user/
    └── {user_id}/
        ├── memories/
        │   └── preferences/
        │       ├── writing_style
        │       └── coding_habits
        ├── resources/
        │   └── private_project/
        ├── skills/
        │   ├── search_code
        │   └── analyze_data
        └── peers/
            └── web-visitor-alice/
```

The three loading tiers:

- **L0 (Abstract)**: a one-sentence summary for quick relevance checks.
- **L1 (Overview)**: core information and usage scenarios for planning.
- **L2 (Details)**: the full original data, read only when needed.

Semantically processed directories carry L0/L1 summaries, so agents can judge relevance before reading full files:

```
viking://resources/my_project/
├── .abstract.md           # L0: quick relevance check
├── .overview.md           # L1: structure and key points
└── docs/
    ├── .abstract.md
    ├── .overview.md
    └── api/
        ├── auth.md         # L2: full content, loaded on demand
        └── endpoints.md
```



## Proof it works

OpenViking 0.3.22 has been evaluated on long-conversation user memory (LoCoMo) and multi-turn agent tasks (tau2-bench). Full results and setup details, including knowledge-base QA, are in the [benchmark report](https://blog.openviking.ai/post/openviking-benchmark-results/); reproduction scripts live in [./benchmark](./benchmark).

The memory evaluation used [Doubao 2.0 Pro](https://console.volcengine.com/ark/region:cn-beijing/model/detail?Id=doubao-seed-2-0-pro) as the VLM and [Doubao-embedding-vision-251215](https://console.volcengine.com/ark/region:cn-beijing/model/detail?Id=doubao-embedding-vision) as the embedding model.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/benchmark-dark.svg">
  <img alt="Benchmark results. LoCoMo accuracy: OpenClaw 24.20% native vs 82.08% with OpenViking; Hermes 33.38% vs 82.86%; Claude Code 57.21% vs 80.32%. tau2-bench task success: Retail 70.94% vs 77.81%; Airline 54.38% vs 66.25%." src="docs/images/benchmark-light.svg">
</picture>

- **User memory (LoCoMo)**: with OpenViking, all three agent integrations land at 80–83% accuracy — up from 24–57% on their native memory — while input tokens drop by 34.3–91.0% and query latency by 58.45–66.10%.
- **Agent experience (tau2-bench)**: experience memory lifts task success by +6.87pp (retail) and +11.87pp (airline) over the same LLM without memory.



## Quick start

Requires Python 3.10+ and access to an embedding model and a VLM (cloud or local).

```bash
pip install openviking --upgrade
openviking-server init      # configure providers and models
openviking-server doctor    # check configuration and connectivity
openviking-server           # start the server
```

`init` writes `~/.openviking/ov.conf`. Supported options include Volcengine, OpenAI, Codex OAuth, Kimi, GLM, and local Ollama. See the [configuration guide](https://docs.openviking.ai/en/guides/01-configuration) for provider setup and the [quick start docs](https://docs.openviking.ai/en/getting-started/02-quickstart) for platform instructions.

The package includes the `ov` CLI. In another terminal, import a repository and search it:

```bash
ov status
ov add-resource https://github.com/volcengine/OpenViking


# Replace TASK_ID with the returned task_id; repeat until status is completed
ov task status TASK_ID
ov ls viking://resources/
ov tree viking://resources/volcengine -L 2
ov find "what is openviking"
ov grep "openviking" --uri viking://resources/volcengine/OpenViking/docs/en
```

`ov find` returns matching context with URIs you can inspect. For client configuration (`ov config`), standalone CLI installs, and index maintenance, see [CLI setup](https://docs.openviking.ai/en/getting-started/05-cli-setup).

Build your own integration with the [Python](sdk/python/README.md), [Go](sdk/go/README.md), or [TypeScript](sdk/typescript/README.md) SDK, or the [HTTP API](https://docs.openviking.ai/en/api/01-overview).



## Use it with your agent

Connect your agent to OpenViking for cross-session memory. Choose a native integration for automatic recall and session capture, or use MCP to give your agent memory and context tools.

<table>
<tbody>
<tr>
<td align="center" valign="bottom" width="16%">
<a href="https://docs.openviking.ai/en/agent-integrations/02-claude-code"><img src="docs/images/integrations/logos/claude-code.png" width="32" height="32" alt=""><br><strong>Claude</strong></a><br>
<sub>Hooks&nbsp;+&nbsp;MCP</sub>
</td>
<td align="center" valign="bottom" width="16%">
<a href="https://docs.openviking.ai/en/agent-integrations/04-codex"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/images/integrations/logos/openai-dark.svg"><img src="docs/images/integrations/logos/openai.svg" width="32" height="32" alt=""></picture><br><strong>Codex</strong></a><br>
<sub>Hooks&nbsp;+&nbsp;MCP</sub>
</td>
<td align="center" valign="bottom" width="16%">
<a href="https://docs.openviking.ai/en/agent-integrations/12-cursor"><img src="docs/images/integrations/logos/cursor.png" width="32" height="32" alt=""><br><strong>Cursor</strong></a><br>
<sub>Hooks&nbsp;+&nbsp;MCP</sub>
</td>
<td align="center" valign="bottom" width="16%">
<a href="https://docs.openviking.ai/en/agent-integrations/13-trae"><img src="docs/images/integrations/logos/trae.png" width="32" height="32" alt=""><br><strong>TRAE</strong></a><br>
<sub>Hooks&nbsp;+&nbsp;MCP</sub>
</td>
<td align="center" valign="bottom" width="16%">
<a href="https://docs.openviking.ai/en/agent-integrations/03-openclaw"><img src="docs/images/integrations/logos/openclaw.png" width="32" height="32" alt=""><br><strong>OpenClaw</strong></a><br>
<sub>Context&nbsp;engine</sub>
</td>
<td align="center" valign="bottom" width="16%">
<a href="https://docs.openviking.ai/en/agent-integrations/05-hermes"><img src="docs/images/integrations/logos/hermes-agent.png" width="32" height="32" alt=""><br><strong>Hermes</strong></a><br>
<sub>Built-in</sub>
</td>
</tr>
</tbody>
<tbody>
<tr>
<td align="center" valign="bottom" width="16%">
<a href="https://docs.openviking.ai/en/agent-integrations/10-opencode"><img src="docs/images/integrations/logos/opencode.png" width="32" height="32" alt=""><br><strong>OpenCode</strong></a><br>
<sub>Plugin&nbsp;+&nbsp;MCP</sub>
</td>
<td align="cente

... (truncated, 9864 more characters)

## pyproject.toml

```
[build-system]
requires = [
    "setuptools>=61.0",
    "setuptools-scm>=8.0",
    "cmake>=3.15",
    "maturin>=1.0,<2.0",
    "wheel",
]
build-backend = "setuptools.build_meta"

[project]
name = "openviking"
dynamic = ["version"]
description = "An Agent-native context database"
readme = "README.md"
requires-python = ">=3.10"
authors = [
    {name = "ByteDance", email = "noreply@bytedance.com"}
]
license = "AGPL-3.0"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
]
dependencies = [
    "openviking-sdk>=0.1.9",
    "pydantic>=2.0.0",
    "typing-extensions>=4.5.0",
    "pyyaml>=6.0",
    "httpx>=0.25.0",
    "pdfplumber>=0.10.0",
    "scrapy>=2.11.0",
    "trafilatura>=1.12.0",
    "feedparser>=6.0.0",
    "defusedxml>=0.7.1",
    "openai>=1.0.0",
    "requests>=2.33.0",
    "charset-normalizer>=3.4,<4",
    "firecrawl-anydoc>=0.2.4,<0.3",
    "json-repair>=0.25.0",
    "apscheduler>=3.11.0",
    "volcengine>=1.0.216",
    "volcengine-python-sdk[ark]>=5.0.3",
    "fastapi>=0.128.0",
    "uvicorn>=0.39.0",
    "xxhash>=3.0.0",
    "rapidfuzz>=3.14,<4",
    "jinja2>=3.1.6",
    "tabulate>=0.9.0",
    "urllib3>=2.7.0",
    "protobuf>=6.33.5",
    "pdfminer-six>=20251230",
    "typer>=0.12.0",
    "litellm>=1.83.7,<1.91.2",
    "python-multipart>=0.0.31",
    # Pin the parsing stack to avoid unvalidated upstream API and grammar changes.
    "tree-sitter==0.25.2",
    "tree-sitter-python==0.25.0",
    "tree-sitter-javascript==0.25.0",
    "tree-sitter-typescript==0.23.2",
    "tree-sitter-java==0.23.5",
    "tree-sitter-cpp==0.23.4",
    "tree-sitter-rust==0.24.0",
    "tree-sitter-go==0.25.0",
    "tree-sitter-c-sharp==0.23.1",
    "tree-sitter-php==0.24.1",
    "tree-sitter-lua==0.5.0",
    # OpenTelemetry
    "opentelemetry-api>=1.14",
    "opentelemetry-sdk>=1.14",
    "opentelemetry-exporter-otlp-proto-grpc>=1.14",
    "opentelemetry-exporter-otlp-proto-http>=1.14",
    "opentelemetry-instrumentation-asyncio>=0.61b0",
    "loguru>=0.7.3",
    "cryptography>=48.0.1",
    "argon2-cffi>=23.0.0",
    "lark-oapi>=1.5.3",
    "mcp>=1.27,<2",
    "pathspec>=1.1.1",
    "grep-ast==0.9.0",
    "tree-sitter-language-pack==1.13.3",
]


[project.optional-dependencies]
test = [
  "pytest>=7.0.0",
  "pytest-asyncio>=0.21.0",
  "pytest-xdist>=3.5.0",
  "boto3>=1.42.44",
  "pytest-cov>=4.0.0",
  "ragas>=0.1.0",
  "datasets>=2.0.0",
  "pandas>=2.0.0",
  "diff-match-patch>=20200713",
  "hvac>=2.0.0",
]
auth = [
  "python-jose[cryptography]>=3.3.0",
  "httpx>=0.25.0",
  "python-ldap>=3.4.0",
]
dev = [
    "mypy>=1.0.0",
    "ruff>=0.1.0",
    "setuptools_scm>=10.0.0",
]
doc = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
    "myst-parser>=2.0.0",
]
eval = [
    "ragas>=0.1.0",
    "datasets>=2.0.0",
    "pandas>=2.0.0",
]
gemini = [
    "google-genai>=1.0.0",
]
gemini-async = [
    "google-genai>=1.0.0",
    "anyio>=4.0.0",
]
ocr = [
    "pytesseract>=0.3.10",
]
build = [
    "setuptools>=61.0",
    "setuptools-scm>=8.0",
    "cmake>=3.15",
    "wheel",
    "build",
]
# vikingbot - all features included
bot = [
  "pydantic-settings>=2.0.0",
  "websockets>=12.0",
  "websocket-client>=1.6.0",
  "httpx[socks]>=0.25.0",
  "readability-lxml>=0.8.0",
  "rich>=13.0.0",
  "croniter>=2.0.0",
  "socksio>=1.0.0",
  "python-socketio>=5.16.2",
  "python-engineio>=4.13.2",
  "msgpack>=1.0.8",
  "python-socks[asyncio]>=2.4.0",
  "prompt-toolkit>=3.0.0",
  "pygments>=2.16.0",
  "html2text>=2020.1.16",
  "beautifulsoup4>=4.12.0",
  "ddgs>=9.0.0",
  "tavily-python>=0.5.0",
  "py-machineid>=1.0.0",
  "mcp>=1,<2",
  # All optional features included by default
  "langfuse>=3.0.0",
  "python-telegram-bot[socks]>=21.0",
  "lark-oapi>=1.0.0",
  "dingtalk-stream>=0.4.0",
  "slack-sdk>=3.26.0",
  "qq-botpy>=1.0.0",
  "opensandbox>=0.1.5",
  "opensandbox-server>=0.1.6",
  "agent-sandbox>=0.0.23",
  "fusepy>=3.0.1",
  "opencode-ai>=0.1.0a0",
  # Auth dependencies
  "python-jose[cryptography]>=3.3.0",
]
benchmark = [
    "langchain>=1.0.0",
    "langchain-core>=1.0.0",
    "langchain-openai>=1.0.0",
    "tiktoken>=0.5.0",
    "datasets>=2.0.0",
    "pandas>=2.0.0",
    "python-docx>=1.0.0",
]
local-embed = [
    "llama-cpp-python>=0.3.0",
]

opengauss = [
  # PostgreSQL wire-compatible driver verified against openGauss DataVec 7.0.
  "psycopg2-binary>=2.9,<3",
]

[project.urls]
Homepage = "https://github.com/volcengine/openviking"
Documentation = "https://openviking.ai"
Repository = "https://github.com/volcengine/openviking"
Issues = "https://github.com/volcengine/openviking/issues"

[project.scripts]
ov = "openviking_cli.rust_cli:main"  # Rust CLI 入口（极简包装器）
openviking = "openviking_cli.rust_cli:main"  # Rust CLI 入口（放弃 python CLI）
openviking-server = "openviking_cli.server_bootstrap:main"  # also: `openviking-server ingest ...`
vikingbot = "vikingbot.cli.commands:app"

[tool.setuptools_scm]
write_to = "openviking/_version.py"
local_scheme = "no-local-version"
tag_regex = "^v(?P<version>[0-9]+(?:\\.[0-9]+)*)$"
git_describe_command = "git describe --dirty --tags --long --match v[0-9]*"

[tool.setuptools.packages.find]
where = [".", "bot"]
include = ["openviking*", "vikingbot*"]
exclude = ["tests*", "docs*", "examples*"]

[tool.setuptools.package-data]
"vikingbot.studio.providers.feishu" = ["icon.png"]
openviking = [
    "prompts/templates/**/*.yaml",
    "server/static/**/*",
    "web_studio/dist/**/*",
    "lib/ragfs_python*.so",
    "lib/ragfs_python*.pyd",
    "bin/ov",
    "bin/ov.exe",
    "storage/vectordb/engine/*.abi3.so",
    "storage/vectordb/engine/*.pyd",
]
vikingbot = [
    "**/*.mjs",
    "skills/**/*.md",
    "skills/**/*.sh",
    "workspace/**/*",
    "bridge/**/*",
]

[tool.mypy]
python_version = "3.10"
warn_return_any = false
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false
check_untyped_defs = true
no_implicit_optional = false
warn_redundant_casts = true
warn_unused_ignores = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
norecursedirs = ["api_test", "oc2ov_test"]
markers = [
    "integration: tests that require external services or real model configuration",
    "cli_remote: tests that require a remote OpenViking CLI binary and server connection",
]
addopts = "-v --cov=openviking --cov-report=term-missing"

[tool.ruff]
line-length = 100
exclude = ["third_party"]
target-version = "py310"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "C",  # flake8-comprehensions
    "B",  # flake8-bugbear
]
ignore = [
    "E501",  # line too long (handled by black)
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
    "B006",  # Do not use mutable data structures for argument defaults
    "B904",  # Within an `except` clause, raise exceptions with `raise ... from err`
    "E741",  # Ambiguous variable name
    "E722",  # Do not use bare `except`
    "B027",  # empty method in an abstract base class
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[dependency-groups]
dev = [
    "pytest>=9.0.2",
]

```

## Cargo.toml

```
[workspace]
members = [
    "crates/ov_cli",
    "crates/ragfs",
    "crates/ragfs-python",
]
resolver = "2"

[profile.release]
opt-level = 3
lto = true
strip = true

[profile.release.package.ragfs]
codegen-units = 1

```

## setup.py

```
import importlib
import json
import os
import platform
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path

from setuptools import Distribution, Extension, setup
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:  # pragma: no cover - local build_ext may not have wheel installed
    bdist_wheel = None

SETUP_DIR = Path(__file__).resolve().parent
if str(SETUP_DIR) not in sys.path:
    sys.path.insert(0, str(SETUP_DIR))

get_host_engine_build_config = importlib.import_module(
    "scripts.build_support.x86_profiles"
).get_host_engine_build_config
resolve_openviking_version = importlib.import_module(
    "scripts.build_support.versioning"
).resolve_openviking_version

CMAKE_PATH = shutil.which("cmake") or "cmake"
C_COMPILER_PATH = os.environ.get("CC") or shutil.which("gcc") or "gcc"
CXX_COMPILER_PATH = os.environ.get("CXX") or shutil.which("g++") or "g++"
ENGINE_SOURCE_DIR = "src/"
ENGINE_BUILD_CONFIG = get_host_engine_build_config(platform.machine())
SKIP_CPP_BUILD = os.environ.get("OV_SKIP_CPP_BUILD") == "1"


def _sanitize_native_build_env(env):
    """Keep Rust native builds from accidentally linking against Linuxbrew libs.

    On older glibc systems, Homebrew-provided native libraries can require a newer
    libc than the host linker/runtime supports. When pkg-config resolves xz/bzip2
    from Linuxbrew, Cargo inherits those library search paths and link fails.
    """

    sanitized_env = env.copy()

    pkg_config = sanitized_env.get("PKG_CONFIG") or shutil.which("pkg-config")
    if pkg_config and "linuxbrew" in os.path.realpath(pkg_config).lower():
        system_pkg_config = "/usr/bin/pkg-config"
        if Path(system_pkg_config).exists():
            sanitized_env["PKG_CONFIG"] = system_pkg_config

    for key in ("PKG_CONFIG_PATH", "LIBRARY_PATH", "LD_LIBRARY_PATH"):
        value = sanitized_env.get(key)
        if not value:
            continue
        kept_paths = [
            path
            for path in value.split(os.pathsep)
            if path and "linuxbrew" not in os.path.realpath(path).lower()
        ]
        if kept_paths:
            sanitized_env[key] = os.pathsep.join(kept_paths)
        else:
            sanitized_env.pop(key, None)

    return sanitized_env


def _get_windows_python_sabi_library() -> Path:
    """Return the stable-ABI Python library path for Windows abi3 extensions."""
    candidate_roots = []
    for raw_root in (
        sys.base_prefix,
        sys.base_exec_prefix,
        sysconfig.get_config_var("installed_base"),
        sysconfig.get_config_var("base"),
    ):
        if not raw_root:
            continue
        candidate_root = Path(raw_root).resolve()
        if candidate_root not in candidate_roots:
            candidate_roots.append(candidate_root)

    candidate_paths = []
    for root in candidate_roots:
        candidate_paths.extend(
            [
                root / "libs" / "python3.lib",
                root / "python3.dll",
            ]
        )

    for candidate_path in candidate_paths:
        if candidate_path.exists():
            return candidate_path

    searched = ", ".join(str(path) for path in candidate_paths) or "<none>"
    raise RuntimeError(
        "Could not locate the Windows stable-ABI Python library for abi3 engine modules. "
        f"Searched: {searched}"
    )


class OpenVikingBuildExt(build_ext):
    """Build OpenViking runtime artifacts and Python native extensions."""

    def run(self):
        self.build_ov_cli_artifact()
        self.build_ragfs_python_artifact()
        self.cmake_executable = CMAKE_PATH

        if SKIP_CPP_BUILD:
            print("[SKIP] C++ vector engine build disabled by OV_SKIP_CPP_BUILD=1")
        else:
            for ext in self.extensions:
                self.build_extension(ext)

    def _copy_artifact(self, src, dst):
        """Copy a build artifact into the package tree and preserve executability."""
        print(f"Copying artifact from {src} to {dst}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        if sys.platform != "win32":
            os.chmod(str(dst), 0o755)

    def _copy_artifacts_to_build_lib(self, target_binary=None, target_lib=None):
        """Copy built artifacts into build_lib so wheel packaging can include them."""
        if self.build_lib:
            build_pkg_dir = Path(self.build_lib) / "openviking"
            if target_binary and target_binary.exists():
                self._copy_artifact(target_binary, build_pkg_dir / "bin" / target_binary.name)
            if target_lib and target_lib.exists():
                self._copy_artifact(target_lib, build_pkg_dir / "lib" / target_lib.name)

    def _require_artifact(self, artifact_path, artifact_name, stage_name):
        """Abort the build immediately when a required artifact is missing."""
        if artifact_path.exists():
            return
        raise RuntimeError(
            f"{stage_name} did not produce required {artifact_name} at {artifact_path}"
        )

    def _run_stage_with_artifact_checks(
        self, stage_name, build_fn, required_artifacts, on_success=None
    ):
        """Run a build stage and always validate its required outputs on normal return."""
        build_fn()
        for artifact_path, artifact_name in required_artifacts:
            self._require_artifact(artifact_path, artifact_name, stage_name)
        if on_success:
            on_success()

    def _resolve_cargo_target_dir(self, cargo_project_dir, env):
        """Resolve the Cargo target directory for workspace and overridden builds."""
        configured_target_dir = env.get("CARGO_TARGET_DIR")
        if configured_target_dir:
            return Path(configured_target_dir).resolve()

        try:
            result = subprocess.run(
                ["cargo", "metadata", "--format-version", "1", "--no-deps"],
                cwd=str(cargo_project_dir),
                env=env,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            metadata = json.loads(result.stdout.decode("utf-8"))
            target_directory = metadata.get("target_directory")
            if target_directory:
                return Path(target_directory).resolve()
        except Exception as exc:
            print(f"[Warning] Failed to resolve Cargo target directory via metadata: {exc}")

        return cargo_project_dir.parents[1] / "target"

    def build_ov_cli_artifact(self):
        """Build or reuse the ov Rust CLI binary."""
        if os.environ.get("OV_SKIP_OV_BUILD") == "1":
            print("[SKIP] ov CLI build disabled by OV_SKIP_OV_BUILD=1")
            return

        binary_name = "ov.exe" if sys.platform == "win32" else "ov"
        ov_cli_dir = Path("crates/ov_cli").resolve()
        ov_target_binary = Path("openviking/bin").resolve() / binary_name

        self._run_stage_with_artifact_checks(
            "ov CLI build",
            lambda: self._build_ov_cli_artifact_impl(ov_cli_dir, binary_name, ov_target_binary),
            [(ov_target_binary, binary_name)],
            on_success=lambda: self._copy_artifacts_to_build_lib(ov_target_binary, None),
        )

    def _build_ov_cli_artifact_impl(self, ov_cli_dir, binary_name, ov_target_binary):
        """Implement ov CLI building without final artifact checks."""

        prebuilt_dir = os.environ.get("OV_PREBUILT_BIN_DIR")
        if prebuilt_dir:
            src_bin = Path(prebuilt_dir).resolve() / binary_name
            if src_bin.exists():
                self._copy_artifact(src_bin, ov_target_binary)
                return

        if ov_cli_dir.exists() and shutil.which("cargo"):
            print("Building ov CLI from source...")
            try:
                env = _sanitize_native_build_env(os.environ.copy())
        

... (truncated, 15556 more characters)
```

## Top-level layout

- .agents/ (dir, 1 files, ~21 lines)
- .clang-format (~33 lines)
- .claude-plugin/ (dir, 1 files, ~20 lines)
- .dockerignore (~20 lines)
- .gitattributes (~6 lines)
- .github/ (dir, 38 files, ~5756 lines)
- .gitignore (~250 lines)
- .pr_agent.toml (~354 lines)
- agent-plugins/ (dir, 15 files, ~2229 lines)
- benchmark/ (dir, 177 files, ~56096 lines)
- bot/ (dir, 257 files, ~75607 lines)
- Caddyfile (~25 lines)
- Cargo.lock (~6743 lines)
- Cargo.toml (~15 lines)
- CONTRIBUTING.md (~296 lines)
- CONTRIBUTING_CN.md (~266 lines)
- CONTRIBUTING_JA.md (~285 lines)
- crates/ (dir, 162 files, ~108521 lines)
- deploy/ (dir, 18 files, ~1158 lines)
- docker-compose.yml (~71 lines)
- Dockerfile (~139 lines)
- docs/ (dir, 421 files, ~94634 lines)
- examples/ (dir, 733 files, ~189317 lines)
- LICENSE (~662 lines)
- Makefile (~186 lines)
- MANIFEST.in (~24 lines)
- npm/ (dir, 4 files, ~269 lines)
- openviking/ (dir, 782 files, ~217875 lines)
- openviking_cli/ (dir, 55 files, ~13558 lines)
- pyproject.toml (~303 lines)
- README.md (~336 lines)
- README_CN.md (~336 lines)
- README_JA.md (~336 lines)
- RELEASE.md (~195 lines)
- RELEASE_CN.md (~183 lines)
- scripts/ (dir, 5 files, ~922 lines)
- sdk/ (dir, 62 files, ~19868 lines)
- SECURITY.md (~11 lines)
- setup.py (~592 lines)
- src/ (dir, 66 files, ~14442 lines)
- tests/ (dir, 815 files, ~245963 lines)
- third_party/ (dir, 372 files, ~110452 lines)
- uv.lock (~7448 lines)
- web-studio/ (dir, 449 files, ~92823 lines)

