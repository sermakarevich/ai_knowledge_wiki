> [[index|Wiki]] | [[summary|Summary]]

# NevaMind-AI/memU — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** memU is a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices (README:23).

## Key points

- memU stores personal memory as a wiki shared across sessions, agents, and devices (README:7, README:23).
- Its core memory logic is only 500 lines, kept compact enough to inspect, understand, and adapt (README:23).
- It automatically distills reusable Markdown skills from agent history via a scheduled bridging task (README:93, README:104).
- `MemoryService` makes no LLM or chat calls; judgment and synthesis stay inside the agent while the service stores, embeds, and retrieves skill Markdown (README:104).
- Each host runs memU as a sidecar binary binding two seams: `record` (scheduled bridging task → `commit` via `commit_results`) and `inject` (standing instruction → `<binary> retrieve` → `progressive_retrieve`) (README:130-133).
- All hosts share one memory backend configured via `~/.memu/config.env` (local or MemU Cloud), so what one host's sessions teach, another host retrieves (README:149-150).
- Configuration resolves in order process env → `~/.memu/config.env` → default, with Local and Cloud backends selected by `MEMU_MEMORY_MODE` (README:195-197).
- `<binary> doctor` verifies the whole loop (config, selected mode, live retrieval) and displays the resolved mode (README:154-155, README:209-210).

## 2. [[wiki/02-top-level-files|Top-Level Files]]

**In one sentence:** The repo root holds contributor/operator contracts — agent rules, install skills, packaging includes, lint hooks, and ignore lists — not service code.

## Key points

- `AGENTS.md` declares `MemoryService` (`src/memu/app/service.py`) the composition root with exactly three `AgenticMixin` entry points — `list_all_recall_files`, `progressive_retrieve`, `commit_results` — and forbids adding any LLM/chat call (AGENTS.md:8-14).
- `AGENTS.md` mandates storage parity across `inmemory`, `sqlite`, and `postgres`, with protocol changes propagated to all backends plus `tests/test_agentic.py` and SQL migrations/bootstrap (AGENTS.md:12, AGENTS.md:42-46).
- `SKILL.md` (`name: install-memu`) routes any host agent through three steps — install `memu-cli`, pick a host binary via `<your-binary> init`, then print and follow `<your-binary> docs install` with verify gates (SKILL.md:1-3, SKILL.md:21-30, SKILL.md:81-90).
- `SKILL.md` enforces one shared backend per machine, a fixed word-for-word ready report template ending with a `retrieve "When did the user register for memU?"` check, and keep-store/remove-residue uninstall defaults (SKILL.md:100-107, SKILL.md:107-148, SKILL.md:154-168).
- `INSTALL-LATEST.md` (`name: install-memu-latest`) installs the moving git `main` HEAD durably on `PATH` (never `uvx`/`npx`), unInstaller-shadows first, verifies from a fresh shell, and confirms SHA subject/date via the GitHub commits API before setup (INSTALL-LATEST.md:1-3, INSTALL-LATEST.md:11-16, INSTALL-LATEST.md:30-46, INSTALL-LATEST.md:55-72).
- `.pre-commit-config.yaml` runs `pre-commit-hooks` (case-conflict, merge-conflict, toml/yaml/json checks, `pretty-format-json --autofix --no-sort-keys`, end-of-file, trailing-whitespace) plus `ruff` with `--exit-non-zero-on-fix` and `ruff-format` (`.pre-commit-config.yaml:1-21`).
- `.gitignore` (216 lines), `MANIFEST.in` (22 lines), and `.python-version` (`3.13`) scope the working tree and sdist: runtime/database artefacts (`data/`, `*.db`, `persona_memory.db`, `*.sqlite3`), secrets (`.env*`, `secrets.txt`, `api_keys.txt`), models (`models/`, `*.bin`, `*.pt`), IDE/OS noise, with sdist including `README.md`/`memu *.py`/`setup_postgres_env.sh` and pruning `example`, `server/`, `docs/`, `scripts/`, docker files (`.gitignore:1`, `.gitignore:171-184`, `.gitignore:209-221`, `.python-version:1`, `MANIFEST.in:1-22`).

## The system in five moves

1. memU frames personal memory as a shared LLM wiki across sessions, agents, and devices with a 500-line inspectable core.
2. Each host runs memU as a sidecar binary binding the record seam (scheduled bridging task mining session logs) and the inject seam (standing instruction retrieving before answering).
3. The scheduled pipeline captures sessions, prepares self-evolve jobs, lets the agent create or patch readable skill Markdown, then commits and indexes it for later retrieval.
4. `MemoryService` stays embedding-only with three `AgenticMixin` entry points and no LLM calls, backed by pluggable `inmemory`/`sqlite`/`postgres` stores under one shared backend per machine.
5. Operator contracts at the repo root — install skills, verify gates, `doctor` checks, lint hooks, and packaging scope — keep install, setup, and contribution reproducible.
