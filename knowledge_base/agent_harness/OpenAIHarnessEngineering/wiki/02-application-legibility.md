> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Making the Application Legible to Agents

**In one sentence:** Because human QA became the bottleneck, the team made the running application itself directly operable by Codex: per-worktree bootable instances, browser control via the Chrome DevTools Protocol, and an ephemeral per-worktree observability stack queryable with LogQL and PromQL.

## Key points

- As code throughput rose, the bottleneck shifted to human QA capacity, so the team invested in making the UI, logs, and metrics directly legible to Codex rather than adding human testers.
- The application is bootable per git worktree, so Codex can launch and drive one isolated instance per change it works on.
- The Chrome DevTools Protocol is wired into the agent runtime with skills for DOM snapshots, screenshots, and navigation, letting Codex reproduce bugs, validate fixes, and reason about UI behavior directly.
- Single Codex runs are regularly observed working on one task for upwards of six hours, often overnight while humans sleep, using these live-application capabilities.
- Observability tooling got the same treatment: logs, metrics, and traces are exposed through a local stack that is ephemeral per worktree and torn down when the task completes.
- Agents query logs with LogQL and metrics with PromQL against their isolated copy of the app, which makes quantitative prompts tractable, e.g. service startup under 800ms or no span over two seconds in four critical user journeys.
- The fixed constraint throughout is human time and attention: every legibility investment buys back human QA hours by letting the agent verify its own work against the running system.

---

## The bottleneck shift

High agent throughput created a verification problem. Codex could generate changes far faster than humans could manually test them, so human QA became the binding constraint. The response was not more process gates but more agent capability: give Codex direct access to the same runtime signals a human QA engineer would use (the rendered UI, the logs, the metrics) so the agent can close its own verification loop.

## Browser control

### Per-worktree instances

Each git worktree gets its own bootable copy of the application. Codex launches an instance for the change under test and drives it independently, with full isolation from other concurrent agent runs. This turns "does it work" from a human manual check into an agent-executable procedure.

### Chrome DevTools Protocol skills

The agent runtime speaks the Chrome DevTools Protocol (CDP), and the repository contains skills for the three core operations: capturing DOM snapshots, taking screenshots, and navigating. With these, Codex can reproduce a reported bug in the live UI, apply a fix, and validate the fix by driving the same UI path again. The post emphasizes that this lets the agent reason about UI behavior directly instead of guessing from static code.

## Observability per worktree

Logs, metrics, and traces are served from a local observability stack that is spun up per worktree and destroyed when the task finishes, so every agent run gets a fully isolated copy of the application's telemetry. Codex queries logs with LogQL and metrics with PromQL. Concrete service-level prompts become executable acceptance criteria: "ensure service startup completes in under 800ms" or "no span in these four critical user journeys exceeds two seconds" can be checked by the agent against real telemetry rather than argued about in review.

## Long autonomous runs

With thelegibility loop in place, single Codex runs are regularly seen working a single task for upwards of six hours, frequently overnight. The agent launches its instance, reproduces, fixes, re-validates, and iterates without human intervention because every signal it needs (UI state, logs, metrics) is reachable from inside its own runtime.

**Covers:** article section "Increasing application legibility" (per-worktree boot, CDP/DOM/screenshots/navigation, ephemeral observability stack, LogQL/PromQL quantitative prompts, multi-hour runs).
