# LangSmith Engine

**Docs:** [LangSmith Engine (LangChain, 2025)](https://docs.langchain.com/langsmith/engine)

## Human Readable TL;DR

Imagine you have a robot assistant that watches your software and automatically notices when something keeps going wrong. LangSmith Engine is like that: it watches AI agent logs, spots patterns of failure, figures out why they happen, and hands you suggested fixes -- sometimes even opening a code change for you. It's an autopilot for maintaining and improving AI systems.

## TL;DR

LangSmith Engine is a beta observability and continuous-improvement feature within LangSmith that automatically detects recurring failures in LLM agent traces, diagnoses root causes, proposes fixes, generates evaluation datasets from production traces, and deploys custom evaluators to prevent regressions. It runs on a configurable scan schedule (default every 6 hours) and integrates with GitHub to open PRs for proposed code or prompt changes.

---

## Problem & Motivation

As LLM agents move into production, they generate large volumes of traces containing recurring failures that are difficult to manually review at scale. Teams need automated tooling to surface patterns, diagnose root causes, and close the feedback loop from production failures to code/prompt improvements without constant manual effort.

---

## Main Original Ideas

1. **Automated Issue Detection** -- Engine continuously scans production traces on a configurable schedule (default 6 hours), clustering similar failures into actionable issues categorized by priority area (Tool Call Failures, Latency, or custom concerns).

2. **Root Cause Diagnosis** -- Each detected issue includes an AI-generated diagnosis with impact assessment and supporting trace links, so engineers can understand the failure pattern without manually sifting traces.

3. **Fix Proposal + GitHub Integration** -- Engine proposes concrete fixes (code or prompt changes) and can open a GitHub pull request directly in the connected repository, closing the loop from detection to remediation.

4. **Ground Truth Dataset Generation** -- From production traces, Engine generates offline evaluation dataset examples with assertion-based quality control, enabling systematic regression testing.

5. **Custom Evaluator Deployment** -- Engine can deploy custom evaluators into LangSmith's monitoring pipeline to catch newly introduced regressions in future traces.

---

## Key Findings

| Capability | Details |
|---|---|
| Scan interval | Every 6 hours (configurable) |
| Issue priorities | Low / Medium / High |
| Priority categories | Tool Call Failures, Latency, custom |
| GitHub integration | Opens PRs with proposed fixes |
| Inference model | LangChain-managed only (no BYOK) |
| Setup time | Up to 20 minutes for initial analysis |

- Issues are browsable with filters by Priority, Status, and Tags, sortable by Severity, Last Updated, or Created.
- Each issue surface area: diagnosis, supporting traces, proposed fix, evaluator config, and offline dataset examples.
- Cost tracking is available in the Engine settings panel.

---

## Suggestions & Future Directions

1. **BYOK support** -- Currently explicitly unsupported; a natural future extension would be allowing teams to use their own API keys for inference.
2. **Broader issue categories** -- Custom priority areas are supported but require manual specification; automated category discovery could lower setup friction.
3. **Tighter CI/CD integration** -- GitHub PR creation is available, but deeper integration (auto-merging on test pass, CI-triggered evaluator updates) would complete the loop.
4. **Webhook-driven workflows** -- Webhook configuration for issue notifications is available, suggesting future integration with incident management pipelines (PagerDuty, Slack, etc.).

---

## Status & Access

- **Status:** Beta
- **Access:** Organization Admin must enable Engine in Settings → Engine enablement
- **Cost:** Monthly usage tracked in Engine settings panel
