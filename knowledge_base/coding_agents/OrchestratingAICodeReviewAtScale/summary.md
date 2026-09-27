# Orchestrating AI Code Review at Scale

**Article:** [Orchestrating AI Code Review at Scale (Ryan Skidmore, 2026)](https://blog.cloudflare.com/ai-code-review/)

## Human Readable TL;DR

Imagine having seven specialized inspectors instead of one generalist check your work -- one looks for security holes, one checks the writing, one looks for performance issues, and so on. Cloudflare built exactly this for software code changes: when a developer submits changes, seven AI "reviewers" check different things simultaneously. The whole review takes under 4 minutes on average and costs about a dollar, replacing waits that used to stretch hours. Importantly, a human can always override the system with a "break glass" command if the AI is wrong.

## TL;DR

Cloudflare built a CI-native AI code review system that orchestrates seven specialized agents via a coordinator, deployed over 48,095 merge requests in its first 30 days. The system uses risk-based tiering to allocate 2-7 agents per review, tiered model selection (Opus for coordination, Sonnet for sub-reviewers, lightweight models for docs), an 85.7% cache hit rate to reduce costs, and circuit-breaker/failback patterns for production resilience. Median review completion is 3m 39s at $0.98 median cost, producing 1.2 actionable findings per review.

---

## Problem & Motivation

Code review is a bottleneck in software development -- reviewers are busy, reviews queue up, and developers lose flow waiting for feedback. Automated static analysis tools are shallow and miss semantic issues. A single AI reviewer with generic prompts produces too much noise (hallucinations, false positives) to be trusted at scale. Cloudflare needed a system that could deliver meaningful, low-noise reviews across 5,169 repositories with diverse codebases, at CI speed and sub-$2 cost per review.

---

## Main Original Ideas

1. **Specialized multi-agent review** -- Rather than one powerful model with broad instructions, seven domain-specific agents each own a narrow concern (security, code quality, performance, documentation, release management, compliance, AGENTS.md freshness). Specialization reduces hallucinations by narrowing the task space.

2. **Explicit negative prompting** -- Each agent is given explicit lists of what NOT to flag. This proved to be the primary lever for reducing review noise -- telling agents what to ignore was more impactful than refining what to find.

3. **Risk-based resource allocation** -- MRs are classified as Trivial (≤10 lines), Lite (≤100 lines), or Full (>100 lines or security-sensitive), and receive 2, 4, or 7+ agents respectively. Security-sensitive files always trigger Full regardless of diff size.

4. **Coordinator intelligence layer** -- A top-tier model (Opus 4.7) handles deduplication, recategorization, and reasonableness filtering after sub-reviewers complete. Sub-reviewers use Sonnet 4.6 / GPT-5.3; text-heavy tasks use lightweight models (Kimi K2.5). This tiered model strategy balances cost against task complexity.

5. **Re-review awareness** -- When developers push updates, the system runs incremental reviews with knowledge of prior findings. Fixed issues are auto-resolved, unfixed ones stay flagged, and developer-marked resolutions are respected unless substantially worsened.

6. **AGENTS.md freshness monitoring** -- A dedicated reviewer classifies architectural changes by materiality (High/Medium/Low) and flags when AI instruction files need updating -- closing the feedback loop between evolving codebases and AI configuration.

7. **Observable control plane via Cloudflare Workers** -- Model routing is changed at runtime without code deployment, enabling rapid failback and A/B testing of models in production.

---

## Key Findings

### Performance Metrics (First 30 Days: March 10 -- April 9, 2026)

| Metric | Value |
|--------|-------|
| Total review runs | 131,246 |
| Unique merge requests | 48,095 |
| Repositories covered | 5,169 |
| Avg reviews per MR | 2.7 |
| Median completion time | 3m 39s |
| P90 completion time | 6m 27s |
| P99 completion time | 10m 21s |
| Median cost per review | $0.98 |
| Average cost per review | $1.19 |
| P99 cost per review | $4.45 |
| Total findings | 159,103 (1.2/review avg) |
| Cache hit rate | 85.7% |
| Total tokens processed | 120 billion |
| "Break glass" overrides | 288 (0.6% of MRs) |

### Cost by Review Tier

| Tier | Trigger | Agents | Avg Cost |
|------|---------|--------|----------|
| Trivial | ≤10 lines, ≤2 files | 2 | $0.20 |
| Lite | ≤100 lines, ≤20 files | 4 | $0.67 |
| Full | >100 lines OR >50 files OR security-sensitive | 7+ | $1.68 |

### Findings Breakdown

- Code quality: 74,898 findings (47% of total)
- Documentation: 26,432 findings
- Security: 11,985 findings (4% critical rate)

### Qualitative findings

- Explicit "do not flag" instructions were the most effective noise-reduction mechanism
- JSONL streaming was critical for crash-resilience; per-line parsing avoids buffering entire documents
- 30-second heartbeat messages prevented user confusion when frontier models spend extended time reasoning
- Diff filtering (stripping lock files, minified assets, source maps) materially reduces prompt size and cost

---

## Suggestions & Future Directions

1. **Architectural context injection** -- Current reviewers lack full system design context; integrating architecture diagrams or dependency graphs could improve cross-system impact analysis.

2. **Concurrency bug detection** -- Static analysis misses timing-dependent race conditions; dynamic analysis integration or specialized concurrency agents are potential extensions.

3. **Large diff handling** -- 500-file refactors hit context window limits (warning triggers at 50%+ usage); chunked or hierarchical review strategies are needed for massive changes.

4. **Reduced cross-system blindspots** -- Agents cannot verify downstream consumer updates; integration with service dependency graphs could close this gap.

5. **Approval bias calibration** -- The current rubric biases toward acceptance (single warnings → "approved_with_comments"); teams may want per-repository tuning of approval strictness.

---

## Authors & Institutions

Ryan Skidmore -- Cloudflare
