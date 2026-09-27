---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: NevaMind-AI/memU

### Q1. In one sentence, what is memU and what makes its core inspectable?

> [!tip]- Answer
> memU is a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices. Its core memory logic is only 500 lines, kept compact enough to inspect, understand, and adapt. See [[wiki/01-overview|Overview]].

### Q2. Recite the six steps of memU's automatic skill-extraction pipeline in order.

> [!tip]- Answer
> The host adapter captures new sessions including messages and tool calls, then `prepare` slices each session into a self-contained self-evolve job. The agent then reads related skills and chooses to do nothing, patch, or create, writes readable skill Markdown with name, description, and workflow, commits it via `commit_results` for embedding under the `skill` track, and a future similar task retrieves it. See [[wiki/01-overview|Overview]].

### Q3. Contrast memU's record seam with its inject seam: what triggers each and which service entry point does each end at?

> [!tip]- Answer
> The record seam is a scheduled bridging task that mines session logs and ends at `commit` via `commit_results`, while the inject seam is a standing instruction that makes the agent run `<binary> retrieve` before answering and ends at `progressive_retrieve`. One host binary per agent (e.g. `memu-codex`, `memu-claude-code`) binds both seams, with `memu-agent detect` covering anything else. See [[wiki/01-overview|Overview]].

### Q4. How is memU's configuration resolved and which storage backends can it use?

> [!tip]- Answer
> Values resolve in order process env → `~/.memu/config.env` → default, with Local and Cloud backends selected by `MEMU_MEMORY_MODE` so all hosts on one machine share one backend. Local stores use `inmemory` for throwaway sessions, `sqlite` for local single-writer default, and `postgres` with pgvector for concurrent or large stores. See [[wiki/01-overview|Overview]].

### Q5. What three invariants does AGENTS.md impose on contributors, and what does the backend-parity rule require?

> [!tip]- Answer
> `MemoryService` in `src/memu/app/service.py` is the composition root with exactly three `AgenticMixin` entry points (`list_all_recall_files`, `progressive_retrieve`, `commit_results`); the service is embedding-only with no LLM or chat calls ever; and storage is pluggable across `inmemory`, `sqlite`, and `postgres`. Any repository-contract change must be propagated to all three backends plus `tests/test_agentic.py` and SQL migrations or bootstrap. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. Contrast SKILL.md with INSTALL-LATEST.md: when is each used and what does each enforce?

> [!tip]- Answer
> `SKILL.md` (`install-memu`) is the normal router: install `memu-cli`, pick a host binary via `<your-binary> init`, then print and follow `<your-binary> docs install` with verify gates, one shared backend per machine, and a word-for-word ready report ending in a `retrieve` check. `INSTALL-LATEST.md` (`install-memu-latest`) installs the moving git `main` HEAD durably on `PATH` (never `uvx`/`npx`), clears shadow installs first, verifies from a fresh shell, and confirms SHA subject and date via the GitHub commits API before setup. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. Your team shares one machine across Codex, Claude Code, and Cursor and wants cross-agent memory without operating Postgres: should you adopt memU, and in which configuration?

> [!tip]- Answer
> Yes, adopt memU with a single shared Local SQLite backend in `~/.memu/config.env` so what one host's sessions teach another host retrieves, installing each host binary and wiring both record and inject seams. Skip Postgres since the workload is single-machine and single-writer, and use `<binary> doctor` plus the `retrieve` check to verify the loop before relying on it. See [[wiki/01-overview|Overview]].
