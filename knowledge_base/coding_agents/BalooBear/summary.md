# Technical Analysis: baloo-bear

**Repository:** https://github.com/bluebear-io/baloo-bear
**Version analyzed:** 0.1.0
**Date:** 2026-06-16

---

## 1. Overview / What Problem It Solves

AI-assisted PR review exists as a SaaS category (CodeRabbit, Korbit, PullRequest.com), but those services require sending your code to a hosted backend you do not control. Teams in regulated industries, or teams that simply want full control over model selection and deployment scope, cannot use them. Baloo fills this gap: it is an open-source GitHub App you self-host, configured with your own Anthropic or Gemini API keys, that installs on your repositories and reviews every PR automatically.

The problem Baloo solves is not just "run an LLM on a diff." Diffs omit the broader codebase context that separates a real bug from a false positive. Baloo provisions a full git checkout of the PR head at review time and places an agentic subprocess (the PI coding agent) inside that worktree. The agent reads files, greps for patterns, and explores call chains before forming findings, then a structured processor pipeline normalizes severity, routes findings to the correct GitHub mechanism, and optionally runs a cheap second LLM pass to discard false positives.

The primary user is a software team running its own GitHub App installation. The service integrates into the GitHub pull request workflow via webhooks, posts inline review comments and Checks API annotations, and optionally exposes a PostgreSQL-backed review history dashboard.

---

## 2. High-Level Architecture

```
┌──────────────┐   webhook POST /webhook   ┌─────────────────────────┐
│   GitHub     │ ────────────────────────► │  FastAPI                │
│   (PR event) │                           │  webhook_handler.py     │
└──────────────┘                           └──────────┬──────────────┘
                                                      │ asyncio.create_task
                                          ┌───────────▼──────────────┐
                                          │  review/orchestrator.py  │
                                          │  process_pr_review()     │
                                          └──────────┬───────────────┘
                                                     │
                               ┌─────────────────────┼────────────────────┐
                               ▼                     ▼                    ▼
                     ┌─────────────────┐  ┌────────────────┐  ┌──────────────────┐
                     │ repo_provision  │  │ agent/pi_runtime│  │ fidelity/        │
                     │ bare clone +    │  │ PI subprocess  │  │ documentation/   │
                     │ worktree        │  │ RPC over stdio │  │ optional passes  │
                     └────────┬────────┘  └────────┬───────┘  └──────────────────┘
                              │ cwd=worktree        │ structured JSON
                              └──────────────────── ┘
                                                     │
                                          ┌──────────▼──────────────┐
                                          │  processor/             │
                                          │  filter → FP-verify     │
                                          │  → severity-route       │
                                          │  → decision             │
                                          └──────────┬──────────────┘
                                                     │
                              ┌──────────────────────┼──────────────────┐
                              ▼                      ▼                  ▼
                     ┌──────────────┐      ┌────────────────┐  ┌───────────────┐
                     │ PR Review    │      │ Checks API     │  │ Dashboard DB  │
                     │ comments     │      │ MEDIUM annots  │  │ (optional)    │
                     └──────────────┘      └────────────────┘  └───────────────┘
```

**Data flow from webhook to posted review:**

1. GitHub sends a `pull_request` webhook to `POST /webhook`. Signature is verified with HMAC-SHA256 (`baloo/github/auth.py`), and the payload is validated against `PullRequestWebhookPayload`.
2. The handler spawns an `asyncio.Task` via `process_pr_review()` in the background, immediately returning `{"status": "queued"}`. A semaphore limits concurrent reviews (default 3).
3. `orchestrator.py` fetches PR metadata (diff, changed files, discussion threads) from the GitHub API, then calls `repo_provision.provision_repo()` to clone the head commit into `/tmp/baloo-repo-cache/<install_id>/<repo>.git` and produce a per-review worktree.
4. A `PIAgentBase` subprocess is launched with `cwd` pointing at the worktree. The PI binary communicates via JSON-RPC over stdio; the agent reads files, greps for patterns, and returns structured JSON findings.
5. Findings pass through `FindingsFilter` (severity threshold + hedging language detection), optional `FPVerifier` (concurrent cheap-model calls), `enforce_severity()` (category-driven floor/cap rules), and `route_findings()` (split by severity into review vs. Checks channels).
6. `GitHubAPIClient` posts inline PR review comments (CRITICAL/HIGH) and Checks API annotations (MEDIUM). `DecisionEngine` determines approve vs. request-changes based on finding counts and optional fidelity score.

Persistent state lives in PostgreSQL (optional, controlled by `DATABASE_ENABLED`). The bare clone cache lives on local disk under `REPO_CACHE_ROOT` (default `/tmp/baloo-repo-cache`).

---

## 3. The Review Finding

The central domain abstraction is the `ReviewFinding` / `ReviewComment` pair. The PI agent produces raw JSON that `schemas.py` coerces into `ReviewFinding` (Pydantic), which is then transformed into `ReviewComment` for all downstream processing.

**Finding shape** (`baloo/agent/schemas.py:60-80`):
- `file: str` — repo-relative path
- `line: Any` — coerced to int via `get_line()`, defaults to 1
- `severity: str` — `CRITICAL | HIGH | MEDIUM | LOW`; normalized via `_normalize_severity()`
- `category: str` — `Security | Bugs | Silent Failures | Guidelines | Performance | Quality`; normalized via `_normalize_category()`
- `title, description, impact, recommendation, code_example` — free-text fields formatted into the posted comment body

**Severity enforcement** (`baloo/agent/schemas.py:172-197`): category floors override agent severity deterministically. Security/Bugs/Silent Failures/Guidelines have a floor of HIGH (agent LOW/MEDIUM escalated; CRITICAL passes through). Performance is always MEDIUM. Quality is capped at MEDIUM. This prevents a cheap haiku-class model from assigning CRITICAL to a style issue.

**Category enum** (`baloo/github/models.py:23-30`):
```python
class FindingCategory(str, Enum):
    SECURITY = "Security"
    BUGS = "Bugs"
    SILENT_FAILURES = "Silent Failures"
    GUIDELINES = "Guidelines"
    PERFORMANCE = "Performance"
    QUALITY = "Quality"
```

The agent returns findings in the `ReviewOutput` schema; `findings_to_comments()` (`baloo/agent/schemas.py:216-259`) converts them to `ReviewComment` objects, formatting the body from structured fields.

**Key query**: severity routing splits `ReviewComment` lists via `route_findings()` (`baloo/processor/severity_router.py:27-56`) into `review` (blocking, PR inline) and `checks` (non-blocking, Checks API) buckets. LOW findings are currently dropped.

---

## 4. LLM / External Service Integration

Baloo does not call LLMs directly via an SDK. All LLM calls are proxied through the [PI](https://github.com/mariozechner/pi-coding-agent) binary, an external subprocess that handles provider routing, retry, and tool-use loop.

**Providers:**
- **Anthropic (Claude)** — primary provider. Configured via `ANTHROPIC_API_KEY`. Default model is `claude-sonnet-4-6`. Short names (`sonnet`, `haiku`, `opus`) are resolved to full model IDs in `baloo/agent/config.py`.
- **Google Gemini** — fallback provider. Configured via `GEMINI_API_KEY`. Default fallback: `google/gemini-2.5-flash`. Full model references use `provider/model` format.
- **OpenAI** — listed in `agent_provider` enum but not verified in source as fully implemented.

**PI subprocess protocol** (`baloo/agent/pi_runtime.py:1-10`): PI is launched via `asyncio.create_subprocess_exec` with `--rpc` flag. Communication is JSON-RPC over stdin/stdout. PI handles the tool-use loop internally; Baloo sends a prompt, PI calls `read`/`grep`/`find`/`ls` tools on the worktree, and returns the final assistant text plus usage metadata.

**Where LLM is required:** the main review agent call (every PR), FP verification calls (per finding, concurrent), and optional: fidelity analysis, documentation drift analysis, thread agent replies.

**Where LLM is NOT required:** webhook validation, GitHub API calls, severity routing, decision engine, dashboard UI.

**Cost tracking**: `baloo/agent/costs.py` normalizes usage across providers. `PIRunResult` carries `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `thinking_tokens`, `cost_usd`. Per-review cost is logged and optionally stored in the DB.

**Thinking level**: PI supports `off | minimal | low | medium | high`. Controlled by `PI_THINKING_LEVEL` (default `medium`). FP verifier explicitly sets `thinking_level="off"` to reduce cost.

---

## 5. The Review Orchestration Pipeline

Entry point: `process_pr_review()` in `baloo/review/orchestrator.py:~150-600`.

**Step 1 — PR context assembly** (`orchestrator.py`):
`GitHubAPIClient.get_pr_context()` fetches the diff, file list, commit messages, and discussion threads. If `REPO_CACHE_ENABLED`, `provision_repo()` (`agent/repo_provision.py`) clones or updates a bare repo and checks out a per-review worktree at `head_sha`. The agent `cwd` is set to the worktree path; without a checkout the agent sees only the diff in its prompt.

**Step 2 — Scope decision for `synchronize` events** (`orchestrator.py:_decide_sync_scope()`):
For pushes to existing PRs, a fast no-tools PI call decides `scoped` vs. `full_pr` based on how much the new commits change behavior. Scoped reviews only present the `before..head` diff to the agent.

**Step 3 — Main review agent** (`orchestrator.py → PIAgentBase.run_query()`):
The review prompt is assembled from `build_review_prompt()` (`agent/prompts.py`), injecting: PR metadata, diff, discussion context, guidelines from `AGENTS.md`/`CONTRIBUTING.md`, and optional fidelity context. The PI agent runs up to `max_turns=20` with file read/grep/find tools enabled. Output is parsed via `findings_to_comments()`.

**Step 4 — Parallel optional passes** (`orchestrator.py`):
Fidelity analysis (`fidelity/fidelity_analyzer.py`) and documentation drift analysis (`documentation/analyzer.py`) run concurrently with the main review via `asyncio.gather`.

**Step 5 — Processor pipeline**:
- `FindingsFilter.filter_findings()` drops findings below `REVIEW_MIN_SEVERITY` and hedged low-severity comments.
- `FPVerifier.verify()` (`processor/fp_verifier.py`) runs up to `FP_VERIFICATION_MAX_CONCURRENT` concurrent haiku-class calls, each returning `{"verdict": "real" | "fp", "reason": "..."}`. Fail-open: errors keep the finding.
- `route_findings()` splits into review (CRITICAL/HIGH) and checks (MEDIUM) buckets.
- `DecisionEngine.make_decision()` returns `(approve, request_changes)` based on severity counts and optional fidelity score.

**Step 6 — GitHub posting** (`github/api_client.py`):
`post_review()` creates a GitHub review with inline comments on diff lines. `post_checks()` creates Checks API annotations. The review body includes a summary line, finding counts, and optionally the fidelity and documentation drift reports.

**Step 7 — Discussion thread agent** (optional, `THREAD_AGENT_ENABLED`):
On `pull_request_review_comment` webhook events (replies to Baloo comments), `_process_thread_reply()` spawns a thread agent that reads discussion context and posts a reply. Capped at `THREAD_AGENT_MAX_REPLIES` per thread to avoid runaway conversations.

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|--------------|
| `baloo/review/orchestrator.py` | 1890 | Core review lifecycle: PR assembly, agent invocation, processor pipeline, GitHub posting, discussion tracking |
| `baloo/agent/pi_runtime.py` | 1004 | PI subprocess management: JSON-RPC protocol, JSON extraction/repair, retry logic, cost normalization |
| `baloo/github/api_client.py` | 887 | GitHub REST API client: PR diff, file contents, review posting, Checks API, installation token refresh |
| `baloo/agent/prompts.py` | 565 | Review system prompt, severity/category guidelines, Dependabot prompt, discussion context builder |
| `baloo/config/settings.py` | 259 | All env-var settings via pydantic-settings; 40+ configurable fields with defaults |
| `baloo/agent/schemas.py` | 259 | `ReviewFinding` / `ReviewOutput` Pydantic models; `enforce_severity()` category floor/cap logic |
| `baloo/github/webhook_handler.py` | 308 | FastAPI app + `/webhook` handler; webhook signature verification, HMAC validation, security checks |
| `baloo/processor/fp_verifier.py` | 367 | Concurrent LLM-based false-positive filter; audit log writer; fail-open design |
| `baloo/github/models.py` | 243 | Domain models: `ReviewSeverity`, `FindingCategory`, `PRContext`, `ReviewComment`, `DiscussionThread` |
| `baloo/agent/repo_provision.py` | 363 | Bare clone cache + per-review worktree; LRU eviction; bwrap sandbox; ephemeral token injection |
| `baloo/dashboard/router.py` | 290 | Optional Jinja2 dashboard: review history, cost totals, finding breakdowns |
| `baloo/agent/sandbox.py` | 196 | `bwrap` sandbox wrapper; falls back to off if unprivileged namespaces unavailable |
| `baloo/db/service.py` | 231 | PostgreSQL persistence: review records, FP signals, cancellation polling |
| `baloo/processor/decision_engine.py` | 70 | `approve / request_changes` logic from severity counts + fidelity score |
| `main.py` | 45 | Entry point: configures logging, starts uvicorn on configured host/port |

---

## 7. Dependencies

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `fastapi` | `>=0.100.0` | ASGI web framework for webhook endpoint and dashboard |
| `uvicorn[standard]` | `>=0.49.0` | ASGI server |
| `pydantic` | `>=2.13.4` | Domain models, structured output parsing, settings validation |
| `pydantic-settings` | `>=2.14.1` | Env-var settings loading |
| `cryptography` | `>=48.0.0` | GitHub App JWT signing |
| `httpx` | `>=0.24.0` | Async HTTP client for GitHub REST API |
| `pyjwt` | `>=2.13.0` | GitHub App installation token generation |
| `python-dotenv` | `>=1.0.0` | `.env` file loading |
| `sqlalchemy[asyncio]` | `>=2.0.50` | ORM for optional PostgreSQL persistence |
| `asyncpg` | `>=0.29.0` | Async PostgreSQL driver |
| `alembic` | `>=1.13.0` | Database migrations |
| `psycopg2-binary` | `>=2.9.12` | Sync PostgreSQL driver (Alembic migrations) |
| `jinja2` | `>=3.1.0` | Dashboard HTML templates |
| `python-multipart` | `>=0.0.32` | Form parsing (dashboard auth) |
| `mako` | `>=1.3.11` | Alembic migration templates |
| `requests` | `>=2.34.2` | Sync HTTP (used in auth token refresh path) |
| `pygments` | `>=2.20.0` | Syntax highlighting in dashboard |

**Dev only:** `pytest`, `pytest-asyncio`, `pytest-cov`, `black`, `ruff`, `mypy`, `aiosqlite`.

**External runtime dependency (not in pyproject.toml):** the `pi` binary must be on PATH or configured via `PI_BINARY_PATH`. This is the PI coding agent from `github.com/mariozechner/pi-coding-agent` and is a hard requirement — no PI binary means no review.

---

## 8. CLI / Usage Surface

**Entry points** (from `pyproject.toml`): none declared; the server is started via `python main.py` or Docker.

**Commands:**
```bash
# Development
uv sync && npm install          # install Python + Node deps
uv run python main.py           # start webhook server (port 8000)
uv run pytest                   # test suite
uv run ruff check baloo         # lint
uv run black --check baloo      # format check

# Local dry-run review (no GitHub posting)
uv run python scripts/local_review.py
uv run python scripts/local_review.py --base origin/main --head HEAD
uv run python scripts/local_review.py --json
uv run python scripts/local_review.py --fail-on-blocking  # exit 1 if CRITICAL/HIGH

# Docker
docker compose up --build
```

**Key environment variables:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `GITHUB_APP_ID` | — | GitHub App numeric ID (required) |
| `GITHUB_PRIVATE_KEY` | — | PEM file path or inline PEM (required) |
| `GITHUB_WEBHOOK_SECRET` | — | HMAC signature secret (required) |
| `ANTHROPIC_API_KEY` | — | Anthropic API key (required if using Claude) |
| `GEMINI_API_KEY` | — | Google Gemini API key (fallback model) |
| `AGENT_MODEL` | `claude-sonnet-4-6` | Primary review model |
| `AGENT_FALLBACK_MODEL` | `google/gemini-2.5-flash` | Fallback on primary failure |
| `PI_BINARY_PATH` | `pi` | Path to PI coding agent binary |
| `PI_THINKING_LEVEL` | `medium` | PI extended thinking budget |
| `REVIEW_MIN_SEVERITY` | `MEDIUM` | Drop findings below this level |
| `REVIEW_AUTO_APPROVE` | `true` | Auto-approve PRs with no HIGH/CRITICAL |
| `FP_VERIFICATION_ENABLED` | `true` | Enable false-positive verification pass |
| `FP_VERIFICATION_MODEL` | `haiku` | Model for FP verification (cheap) |
| `THREAD_AGENT_ENABLED` | `false` | Enable replies to PR review comment threads |
| `DATABASE_ENABLED` | `false` | Enable PostgreSQL review history |
| `DASHBOARD_ENABLED` | `true` | Enable review history UI (requires DATABASE) |
| `REPO_CACHE_ENABLED` | `true` | Clone repo for full-file agent access |
| `REPO_CACHE_ROOT` | `/tmp/baloo-repo-cache` | Disk path for bare clones and worktrees |
| `REPO_CACHE_MAX_DISK_GB` | `10` | LRU eviction threshold in GB |
| `REPO_SANDBOX_MODE` | `bwrap` | Agent subprocess sandbox (`bwrap` or `off`) |
| `FIDELITY_ENABLED` | `true` | Compare PR against design plan doc |
| `DOCUMENTATION_DRIFT_ENABLED` | `false` | Check for stale documentation |
| `MAX_CONCURRENT_REVIEWS` | `3` | Concurrent review tasks per process |
| `INSTALLATION_ID` | — | Scope this broker to one GitHub installation |

**Configuration files:**

| Path | Purpose |
|------|---------|
| `.env` | Primary config (path overridable via `BALOO_ENV_FILE`) |
| `.env.example` | Template with all required variables |
| `alembic.ini` | Alembic migration configuration |
| `docker-compose.yml` | Production deployment with optional PostgreSQL |

---

## 9. Extensibility Points

- **Adding a new LLM provider**: The PI binary handles provider routing; adding a new provider requires updating PI itself, not Baloo. Within Baloo, `baloo/agent/config.py` contains the model short-name resolution map -- add new short names there and update `AGENT_MODEL` documentation.

- **Adding a new finding category**: Add a member to `FindingCategory` in `baloo/github/models.py:23-30`, add severity floor/cap logic in `_CATEGORY_MIN_SEVERITY` in `baloo/agent/schemas.py:47-53`, and update the `REVIEW_SYSTEM_PROMPT` in `baloo/agent/prompts.py` to instruct the agent on the new category.

- **Custom review guidelines per repo**: Place an `AGENTS.md` or `CONTRIBUTING.md` at the repo root. The review prompt loads these via the PI agent (`read AGENTS.md`) and flags violations as HIGH findings. No Baloo code change needed.

- **Custom fidelity plan paths**: Set `FIDELITY_PLAN_PATH_PATTERN` to a path with `{ticket_id}` placeholder (default `docs/plans/{ticket_id}.md`). The ticket ID extractor (`baloo/fidelity/ticket_extractor.py`) parses the PR title/branch for a configurable prefix (`TICKET_ID_PREFIX`, default `PROJ`).

- **Optional modules (documentation drift, fidelity, dashboard)**: Each is a self-contained subdirectory (`baloo/fidelity/`, `baloo/documentation/`, `baloo/dashboard/`). Enable via env var; disable by setting the var to `false`. The orchestrator checks the flag before importing and calling these modules.

- **AST tools extension** (`extensions/baloo-ast-tools.ts`): A TypeScript/Node.js plugin that adds `ast_outline`, `ast_grep`, and `ast_symbols` tools to PI. Controlled by `AST_TOOLS_ENABLED`. To add a new AST tool, extend this file and the prompt section `AST_TOOLS_PROMPT_SECTION` in `baloo/agent/prompts.py:26-37`.

---

## 10. Limitations and Gotchas

- **External PI binary is a hard dependency**: The `pi` binary is not packaged with Baloo. The Docker image or host must have it installed and on PATH (or at `PI_BINARY_PATH`). The Dockerfile does not show installation of PI, meaning fresh deployments require manual setup not documented in `docker-compose.yml` (per README; not fully verified in Dockerfile source).

- **bwrap sandbox silently degrades**: `REPO_SANDBOX_MODE=bwrap` falls back to `off` when unprivileged user namespaces are unavailable (common in some container runtimes). The fallback is logged but not surfaced as a warning in the review output, so operators may believe sandboxing is active when it is not.

- **Diff-only fallback loses context**: If `REPO_CACHE_ENABLED=false` or provisioning fails, the agent sees only the diff in its prompt. The PI agent's file read/grep tools will fail on file paths not present in the diff. The orchestrator degrades gracefully, but finding quality drops substantially.

- **PI JSON output repair is fragile**: `_repair_json_string_literals()` in `pi_runtime.py:131-185` repairs common LLM JSON mistakes (unescaped quotes, raw newlines in strings). This is necessary because PI forwards the raw assistant text. Complex nested structures or very large responses can still fail to parse, falling back to `is_error=True`.

- **`active_reviews` dict is process-local**: Multi-replica deployments (e.g. two Docker containers behind a load balancer) cannot cancel each other's reviews via the `active_reviews` dict. The DB-backed cancellation poller (`_monitor_review_cancellation`) handles this, but only if `DATABASE_ENABLED=true`. Without a DB, duplicate reviews for the same PR may run concurrently across replicas.

- **PostgreSQL is optional but several features depend on it**: `DATABASE_ENABLED=false` disables the dashboard, cross-replica cancellation, FP feedback signals, and review history. The dashboard nav links appear in the webhook handler mount logic but the router is only registered when `database_enabled and database_url` both hold.

- **No built-in rate limiting for GitHub API calls**: `GitHubAPIClient` does not implement exponential backoff or secondary rate limit handling. Under high PR volume, the service may hit GitHub's per-installation rate limits without graceful degradation.

- **`TICKET_ID_PREFIX` is a single string**: The fidelity plan feature assumes all tickets share one prefix (e.g. `PROJ-123`). Teams with multiple project prefixes cannot configure multi-prefix matching without code changes.

---

## 11. How It Compares to Alternatives

**CodeRabbit** is the dominant hosted AI PR reviewer. It offers richer UI (chat with the bot, PR summaries, incremental review), handles more VCS providers (GitHub, GitLab, Bitbucket, Azure DevOps), and requires zero infrastructure. The tradeoff: your code leaves your network, you pay per PR, and you cannot control the review model or prompt. Baloo inverts this: self-hosted, bring-your-own-key, but you own ops.

**Reviewpad** (now part of Linearb) focuses on PR automation workflows -- labeling, routing, auto-merge rules -- with optional LLM review as one capability among many. Baloo focuses exclusively on deep agentic code review with no workflow automation layer.

**PullRequest.com** pairs human expert reviewers with automated checks. It is a managed service where human reviewers validate AI findings. Baloo has no human reviewer tier; everything is automated. The FP verifier is the closest equivalent to a human sanity check, but it is another LLM call, not a person.

**GitHub Copilot code review** (native) is a first-party option that runs inside GitHub's infrastructure without requiring a self-hosted service. It has lower setup friction and tighter IDE integration. Baloo's advantages are: configurable model choice, fidelity analysis against design docs, repo-level `AGENTS.md` enforcement, and full control over when and how reviews are posted.

**Positioning**: Baloo is the right choice for teams that treat the review pipeline as infrastructure they own -- willing to run a service, contribute Anthropic/Gemini API costs, and customize review behavior at the prompt/category/severity level without vendor lock-in.

---

## Appendix: Selected Code Snippets

**`enforce_severity()` -- category-driven severity normalization** (`baloo/agent/schemas.py:172-197`)

```python
def enforce_severity(finding: ReviewFinding) -> str:
    category = _normalize_category(finding.category).upper()
    agent_severity = _normalize_severity(finding.severity).upper()
    agent_rank = _SEVERITY_ORDER.get(agent_severity, 2)

    floor = _CATEGORY_MIN_SEVERITY.get(category)
    if floor is not None:
        floor_rank = _SEVERITY_ORDER[floor]
        return agent_severity if agent_rank >= floor_rank else floor

    if category == "PERFORMANCE":
        return "MEDIUM"

    if category == "QUALITY":
        cap_rank = _SEVERITY_ORDER["MEDIUM"]
        return agent_severity if agent_rank <= cap_rank else "MEDIUM"

    return "MEDIUM"
```

**`FPVerifier.verify()` -- fail-open concurrent false-positive filter** (`baloo/processor/fp_verifier.py:80-130`)

```python
async def verify(self, comments, pr_context):
    semaphore = asyncio.Semaphore(self.max_concurrent)

    async def _verify_one(comment):
        async with semaphore:
            return await self._verify_single(comment, pr_context)

    tasks = [_verify_one(c) for c in comments]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, res in enumerate(results):
        comment = comments[i]
        if isinstance(res, Exception):
            # Fail-open: keep the finding on error
            result.verified.append(comment)
            stats.kept += 1
            stats.errors += 1
            continue
        _, verdict_data = res
        if verdict_data.get("verdict") == "fp":
            result.rejected.append(FPRejection(comment=comment, ...))
        else:
            result.verified.append(comment)
```

**Webhook security: cross-tenant repo ownership check** (`baloo/github/webhook_handler.py:84-115`)

```python
async def _validate_webhook_security(installation_id, repo_full_name):
    if current_settings.installation_id and \
       str(installation_id) != current_settings.installation_id:
        return {"status": "skipped", "reason": "installation not configured"}

    try:
        GitHubAuth().get_installation_token(installation_id)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=403, detail="Invalid installation")

    if repo_full_name and not await verify_repo_belongs_to_installation(
        installation_id, repo_full_name
    ):
        raise HTTPException(
            status_code=403,
            detail="Repository not accessible for this installation",
        )
    return None
```
