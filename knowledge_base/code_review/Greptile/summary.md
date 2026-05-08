# Technical Analysis: Greptile (examples showcase)

**Source:** https://www.greptile.com/examples (cross-referenced with /docs/introduction and /benchmarks)
**Version analyzed:** product as of 2026-05-08 (page advertises TREX in "Early Access"; benchmark dataset dated July 2025)
**Date:** 2026-05-08

> Caveat: Greptile is a closed-source commercial product. This summary analyzes the **public surface** (examples page, docs introduction, benchmarks page) — not source code. Architectural claims marked "(per docs; not verified in source)" cannot be checked against an internal implementation. The "11-section codebase summary" template is adapted accordingly: Sections 6 (Key Files) and 7 (Dependencies) are replaced with Examples Inventory and Integration Surface, since file/line citations into a private repo are not possible.

---

## 1. Overview / What Problem It Solves

Modern pull request review consumes senior-engineer attention disproportionate to its yield: reviewers eyeball diffs in isolation while the actual defects depend on call sites, invariants, and concurrency edges scattered across the rest of the codebase. The well-studied result (see e.g. `knowledge_base/.../code-reviews-do-not-find-bugs`, `defects-discovered-in-code-reviews` in this same vault) is that human MCR catches relatively few real bugs — most accepted comments are nitpicks about style and readability.

Greptile is an automated GitHub/GitLab PR review bot that posts line-level findings on every pull request, positioned as a replacement for "diff-only" linters and LLM-on-diff tools. Its public pitch is **whole-repository context**: per the docs, "[Greptile] builds a complete graph of your codebase — every function, class, and dependency" rather than reviewing files in isolation. The primary user is the **PR author and reviewers** on a real engineering team — not a CTF/security-research user, not an end-user developer running a CLI locally. The competitive frame on the benchmarks page is explicitly Bugbot, Copilot, CodeRabbit, Graphite.

The `/examples` page is a curated showcase of 18 specific findings posted on real public open-source PRs (NVIDIA, Meta PyTorch, Solana, Netflix Metaflow, OpenClaw, PostHog) — used both as marketing proof-of-life and as an implicit taxonomy of what kinds of defects the system claims to catch.

---

## 2. High-Level Architecture (per public docs)

```
   PR opened on GitHub / GitLab
              │
              ▼
  ┌──────────────────────────┐
  │  Webhook → Greptile      │
  │  (cloud or self-hosted)  │
  └──────────────────────────┘
              │
              ▼
  ┌──────────────────────────┐         ┌──────────────────────┐
  │  Repo graph builder      │ ◄────── │  Repository indexer   │
  │  (functions, classes,    │         │  (full-codebase scan) │
  │   dependency edges)      │         └──────────────────────┘
  └──────────────────────────┘
              │
              ▼
  ┌──────────────────────────┐
  │  Diff + graph context →  │
  │  LLM review pass         │
  │  (~3 min per PR)         │
  └──────────────────────────┘
              │
              ▼
  ┌──────────────────────────┐
  │  Line-level PR comments  │
  │  with severity + tag +   │
  │  "Send to Cursor / Claude │
  │   Code / Codex / Devin"  │
  │  buttons                 │
  └──────────────────────────┘
              │
              ▼
  ┌──────────────────────────┐
  │  👍 / 👎 / replies feed   │
  │  back into per-team      │
  │  learning (~2-3 weeks)   │
  └──────────────────────────┘
```

Data flow from PR open to PR comment:

1. A PR is opened/updated on GitHub or GitLab; a webhook hits Greptile.
2. The system loads (or refreshes) a **repository graph** — functions, classes, dependencies — built from the whole codebase, not just the diff. (per docs; not verified in source)
3. The diff is paired with relevant graph context and sent to an LLM review pass.
4. Findings are posted back as line-level PR comments with a category tag (Security / Logic / Validation / Runtime / Performance / Alignment / Error Handling / Refactoring / Concurrency) and a "send to coding agent" button.
5. Reviewers thumbs-up / thumbs-down or reply; "After 2-3 weeks, it stops commenting on things you don't care about" (verbatim, docs).

Persistent state lives in Greptile's own service (cloud SOC2 Type II, or self-hosted via Docker Compose / Kubernetes Helm / air-gapped — per docs). The host repository sees only PR comments; no state is added to the repo itself.

---

## 3. The Core Abstraction: a Whole-Repo Code Graph

The single architectural claim Greptile leans on — and the one that distinguishes it from "LLM reads the diff" tools — is the **codebase graph**.

- **Representation (per docs, not verified):** "every function, class, and dependency" as nodes and edges, built once per repo and refreshed on changes.
- **Why it matters in the examples:** several of the 18 showcased findings are inherently cross-file and would be invisible to a diff-only review. Concrete instances:
  - `OpenClaw/ui/src/ui/app-chat.ts` — *"Rename leaves 3 callers undefined"* — only catchable if the reviewer knows about the 3 call sites elsewhere.
  - `OpenClaw/src/agents/model-suppression.ts` — *"Aliased providers escape suppression"* — requires knowing how providers get aliased upstream.
  - `PostHog/ee/hogai/django_checkpoint/checkpointer.py` — *"Security PR ships without the fix"* — requires comparing what a PR claims to do against what its diff actually changes.
- **Knobs controlling the representation:** none surfaced on the public pages. Custom rules, severity scoring, confidence levels, and similar config (which competitors expose) are **not documented** on `/docs/introduction` — the marketing line is that the system **learns** per-team preferences from reactions instead of being configured.

The 👍/👎 + replies feedback loop is effectively a per-team weighting on top of the static graph: the graph stays the same, but which findings get surfaced changes.

---

## 4. LLM / External Service Integration

Greptile **calls LLMs itself** — it is the server, the user's PR is the client. The public pages do not name a specific provider or model, but:

- Reviews are generated by an LLM pass over (diff + graph context); the docs commit to "**~3 minutes**" per PR as the SLA.
- TREX (test generation) is a separate product surface in Early Access on the same page.
- "Greptile Agent" is mentioned as a feature label but not architecturally explained on these pages.
- Outbound integration: review comments contain buttons to dispatch a finding into **Claude Code, Codex, Conductor, Cursor, or Devin**, passing file/line/suggested code. This is a one-way handoff — those agents are not Greptile dependencies, just supported destinations.

Cost-per-call points are not disclosed. Pricing lives at `/pricing`, which was not fetched for this analysis.

---

## 5. The Review Pipeline (as evidenced by the 18 examples)

The `/examples` page is the most concrete artifact of how the pipeline behaves. Each card is shaped:

```
<repo> | <file path> | "<one-line finding title>" | <category tag> | <language>
```

Steps inferable from the examples:

1. **Trigger:** PR opened/updated on a public repo Greptile is watching.
2. **Locate hotspot:** the system pins a specific file and line range — every example cites a file path inside the repo, not a generic "this PR".
3. **Classify:** assigns one of ~10 category tags (see Examples Inventory below). Categories are coarse — there is no visible numeric severity on the public examples cards, though the benchmarks page uses a Critical / High / Medium+Low scoring rubric.
4. **Phrase as a hazard, not a nitpick:** every showcased title names a *consequence*, e.g. *"Unbalanced CUDA release wipes context"*, *"Null block_id bypasses staleness guard"*, *"O(1) optimization is a silent no-op"*. None of the 18 examples are style/formatting nits — this is consistent with the marketing positioning against "noisy" reviewers.
5. **Attach handoff:** the comment includes a button to dispatch the issue to a coding agent (Cursor, Claude Code, Codex, Conductor, Devin) with file/line/suggestion preloaded.
6. **Learn from response:** reviewer 👍/👎/reply is fed back into per-team weighting; "after 2-3 weeks" the system suppresses categories the team consistently rejects.

Input shape: `(repo_graph, PR_diff, history_of_team_reactions) → list[FindingComment]` where each comment has `(file, line_range, title, category, suggested_code)`.

---

## 6. Examples Inventory (replaces "Key Files" — this is not a code repo)

The 18 findings on the `/examples` page, as a single ranked table. This is the de facto taxonomy of what Greptile is showcasing as its sweet spot.

| # | Repo | File | Title (verbatim) | Category | Lang |
|---|------|------|------------------|----------|------|
| 1 | NVIDIA DALI | `dali/core/device_guard.cc` | Unbalanced CUDA release wipes context | GPU | C++ |
| 2 | NVIDIA DataDesigner | `packages/data-designer/src/data_designer/cli/repositories/provider_repository.py` | Deprecation warnings never reach users | Logic | Python |
| 3 | NVIDIA Emerging-Optimizers | `emerging_optimizers/orthogonalized_optimizers/sinkhorn_muon.py` | Sinkhorn check rejects valid output | Validation | Python |
| 4 | Meta PyTorch OpenEnv | `envs/repl_env/server/repl_environment.py` | Undefined method breaks every step() | Runtime | Python |
| 5 | Meta PyTorch OpenEnv | `envs/pathway_analysis_env/models.py` | Ground truth leaks via state endpoint | Alignment | Python |
| 6 | Meta PyTorch OpenEnv | `src/openenv/cli/commands/push.py` | HF push leaks raw tracebacks | Error Handling | Python |
| 7 | Solana Kora | `crates/lib/src/transaction/instruction_util.rs` | Mid-loop overflow leaves orphaned keys | Logic | Rust |
| 8 | Solana Kora | `crates/lib/src/transaction/instruction_util.rs` | Empty data parsed as valid ATA Create | Validation | Rust |
| 9 | Solana Kora | `crates/lib/src/token/token.rs` | Null block_id bypasses staleness guard | Security | Rust |
| 10 | Netflix Metaflow | `metaflow/plugins/devcontainer/devcontainer_decorator.py` | Home mount defeats container sandbox | Security | Python |
| 11 | Netflix Metaflow | `metaflow/plugins/catch_decorator.py` | parallel_foreach silently truncates | Logic | Python |
| 12 | Netflix Metaflow | `metaflow/plugins/metadata_providers/service.py` | O(1) optimization is a silent no-op | Performance | Python |
| 13 | OpenClaw | `src/plugins/loader.ts` | Closes undefined fd in error path | Logic | TypeScript |
| 14 | OpenClaw | `ui/src/ui/app-chat.ts` | Rename leaves 3 callers undefined | Refactoring | TypeScript |
| 15 | OpenClaw | `src/agents/model-suppression.ts` | Aliased providers escape suppression | Logic | TypeScript |
| 16 | PostHog | `ee/api/agentic_provisioning/views.py` | No auth on provisioning endpoint | Security | Python |
| 17 | PostHog | `products/llm_analytics/frontend/tags/llmTagger.ts` | HogQL injection via URL parameter | Security | TypeScript |
| 18 | PostHog | `ee/hogai/django_checkpoint/checkpointer.py` | Security PR ships without the fix | Security | Python |

Category distribution: Security 5, Logic 5, Validation 2, Refactoring 1, Runtime 1, Performance 1, Alignment 1, Error Handling 1, GPU 1. Notably absent on this curated page: style, formatting, naming, "consider extracting a function", "add a docstring" — i.e. the comment categories that the academic literature in this same vault (`automatic-classification-review-comments-pull`, `defects-discovered-in-code-reviews`) finds dominate human MCR.

---

## 7. Integration Surface (replaces "Dependencies")

| Surface | Detail |
|---------|--------|
| **VCS — supported** | GitHub Cloud, GitHub Enterprise Server, GitLab Cloud, GitLab Self-Managed |
| **VCS — not mentioned** | Bitbucket, Gitea, Azure DevOps |
| **Coding-agent handoff** | Buttons to send a finding into Claude Code, Codex, Conductor, Cursor, Devin |
| **Other tooling** | Zapier (mentioned but not detailed) |
| **Languages** | "any programming language in your codebase" (verbatim, docs); examples cover C++, Python, Rust, TypeScript |
| **Deployment** | SOC2 Type II cloud; Docker Compose; Kubernetes via Helm; air-gapped |
| **Auth into customer code** | Not described on these public pages |
| **Notifications** | Not detailed (Slack/Linear/Jira are not mentioned in `/docs/introduction`) |

---

## 8. CLI / Usage Surface

There is no CLI. Usage is entirely:

- **Sign up** at `https://app.greptile.com/signup`.
- **Install GitHub/GitLab app** on target repos (mechanics not on these public pages).
- **Open a PR** → review comments arrive in ~3 minutes.
- **React** with 👍/👎/reply to shape future reviews.
- **Click the agent-handoff button** on a comment to forward to Cursor/Claude Code/Codex/Conductor/Devin.

Configuration files, env vars, and per-repo rule files are **not documented** on `/docs/introduction`. The product's stated philosophy is that learning replaces configuration.

---

## 9. Extensibility Points

Public extensibility, as advertised:

- **Per-team learning loop.** The only first-class extension knob exposed on the public pages: react to comments, and the system reweights what it surfaces. There is no documented config file for this.
- **"Custom Context"** is named as a feature on `/examples` ("Learning & Custom Context") but the mechanics are not described on these public pages. (per page; not verified.)
- **Coding-agent destinations.** The list of supported handoff agents (Cursor, Claude Code, Codex, Conductor, Devin) is closed and curated by Greptile — there is no documented mechanism for a customer to add a sixth.
- **Self-hosting / air-gapped deploy.** Listed as a deployment option, but no description of customization beyond what cloud allows.

There is no plugin SDK, no custom-rule DSL, no language-grammar registration — all features that competitors (CodeRabbit, Sonar) document. If those exist they are not on the pages reviewed.

---

## 10. Limitations and Gotchas

- **Closed-source, single-vendor.** Every architectural claim ("graph of your codebase", "~3 minutes", "82% catch rate") is a marketing claim from the vendor's own pages. None of it is independently verifiable from public source.
- **Self-reported benchmark.** The `/benchmarks` page reports Greptile at 82% catch rate vs. Bugbot 58%, Copilot 54%, CodeRabbit 44%, Graphite 6%, on 50 PRs across 5 repos in July 2025 with "default tool settings." Methodology is summarized but the ground-truth labels and the prompt/config used per competitor are not published. Treat as vendor-run, not third-party.
- **Curated examples ≠ steady-state behavior.** The 18 findings on `/examples` are hand-picked from popular open-source repos to look impressive. They do not tell you the **false-positive rate** the median user sees in week 1, before the 2–3-week learning period kicks in.
- **"Any language" is a strong claim.** The examples cover four languages (C++, Python, Rust, TypeScript). Whether Greptile's repo-graph extraction actually parses Erlang, OCaml, Zig, etc. with comparable depth — vs. falling back to text-only review — is not addressed on these pages.
- **Learning loop is opaque.** "After 2-3 weeks, it stops commenting on things you don't care about" is presented as a feature, not a mechanism. There is no public way to audit, export, or reset what the system has learned about a team. For a regulated buyer this is a gap.
- **Custom rules absent from public docs.** Teams that want hard-coded "always block PR if X" rules need to look beyond `/docs/introduction`; the public-facing docs intro frames every behavior as learned, not declared.
- **No discussion of the low-severity tail.** The benchmark only breaks out Critical / High / Medium+Low. The published taxonomy of comment types in academic MCR work (which is sitting in the same `papers/` vault) is much richer; Greptile's public collateral does not engage with it.

---

## 11. How It Compares to Alternatives

- **CodeRabbit.** Same form factor (PR comment bot with config/rules), broader integration list (Bitbucket, Linear, Jira, Slack are public for CodeRabbit). Greptile's pitch vs. CodeRabbit on `/benchmarks` is a 2× catch-rate gap (82% vs 44%) attributed to the whole-repo graph; CodeRabbit's pitch vs. Greptile is configurability and platform breadth.
- **Cursor Bugbot.** Closer architecturally — diff plus repo-aware LLM, posted as PR comments. Greptile's benchmark places it at 58%, the second-best competitor on their dataset. Bugbot is bundled with Cursor; Greptile is standalone, which matters if your team is not on Cursor.
- **GitHub Copilot code review.** Native to GitHub, no install friction, but Greptile's benchmark places it at 54%. Tradeoff: zero procurement effort vs. lower catch rate (per Greptile's numbers).
- **Sonar / SonarQube + Semgrep.** Static-analysis tradition — deterministic rules, no LLM, no per-team learning. Massively cheaper at scale, no false-positive drift, but limited to bug classes encodable as static rules. Greptile's claim is that the LLM + repo-graph combination catches semantic/cross-file bugs (the OpenClaw "rename leaves 3 callers undefined" example) that pure-static tools miss.
- **Graphite reviewer.** Listed on the benchmark at 6%; positioned as a stack-aware PR tool first, AI review second. Greptile is review-first.

**Positioning statement:** Greptile is the "whole-repo graph + LLM + per-team learning loop" point in the AI-PR-review design space — opinionated against configuration, opinionated against diff-only context, and benchmarked against other LLM-bots rather than against static analyzers.

---

## Appendix: Selected Example Findings (verbatim from `/examples`)

These are the 18 finding **titles** as the customer would see them in the PR comment header. (Bodies are not on the marketing page.) Grouped to show what the system claims to catch.

### Cross-file consequences (graph-dependent)

> **Rename leaves 3 callers undefined** — `OpenClaw/ui/src/ui/app-chat.ts` (Refactoring, TypeScript)
> **Aliased providers escape suppression** — `OpenClaw/src/agents/model-suppression.ts` (Logic, TypeScript)
> **Closes undefined fd in error path** — `OpenClaw/src/plugins/loader.ts` (Logic, TypeScript)

### Spec / intent mismatches

> **Security PR ships without the fix** — `PostHog/ee/hogai/django_checkpoint/checkpointer.py` (Security, Python)
> **O(1) optimization is a silent no-op** — `Netflix Metaflow/metaflow/plugins/metadata_providers/service.py` (Performance, Python)
> **parallel_foreach silently truncates** — `Netflix Metaflow/metaflow/plugins/catch_decorator.py` (Logic, Python)

### Security / authorization gaps

> **No auth on provisioning endpoint** — `PostHog/ee/api/agentic_provisioning/views.py` (Security, Python)
> **HogQL injection via URL parameter** — `PostHog/products/llm_analytics/frontend/tags/llmTagger.ts` (Security, TypeScript)
> **Null block_id bypasses staleness guard** — `Solana Kora/crates/lib/src/token/token.rs` (Security, Rust)
> **Home mount defeats container sandbox** — `Netflix Metaflow/metaflow/plugins/devcontainer/devcontainer_decorator.py` (Security, Python)

### Validation / parsing

> **Empty data parsed as valid ATA Create** — `Solana Kora/crates/lib/src/transaction/instruction_util.rs` (Validation, Rust)
> **Sinkhorn check rejects valid output** — `NVIDIA Emerging-Optimizers/emerging_optimizers/orthogonalized_optimizers/sinkhorn_muon.py` (Validation, Python)

### Runtime / resource

> **Undefined method breaks every step()** — `Meta PyTorch OpenEnv/envs/repl_env/server/repl_environment.py` (Runtime, Python)
> **Unbalanced CUDA release wipes context** — `NVIDIA DALI/dali/core/device_guard.cc` (GPU, C++)
> **Mid-loop overflow leaves orphaned keys** — `Solana Kora/crates/lib/src/transaction/instruction_util.rs` (Logic, Rust)

### Observability / leakage

> **HF push leaks raw tracebacks** — `Meta PyTorch OpenEnv/src/openenv/cli/commands/push.py` (Error Handling, Python)
> **Ground truth leaks via state endpoint** — `Meta PyTorch OpenEnv/envs/pathway_analysis_env/models.py` (Alignment, Python)
> **Deprecation warnings never reach users** — `NVIDIA DataDesigner/.../provider_repository.py` (Logic, Python)
