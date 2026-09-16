> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Workflow Abstraction
**In one sentence:** The workflow layer is a verb surface (`enqueue`/`dispatch`/`watch`/`talk`/`delegate`/`discuss`) over a SQLite-backed task state machine with per-workflow dispatch gates, orchestrator routing, three fanout executors, quorum-gated discussions, classifier-driven auto-dispatch, and YAML module hooks.

## Key points
- Verbs map 1:1 to commands: `enqueue` writes an inbox row (`src/superharness/commands/inbox_enqueue.py:206`), `dispatch` claims and launches one item (`src/superharness/commands/inbox_dispatch.py:777`), `watch` loops dispatch across agents (`src/superharness/commands/inbox_watch.py:524`), `talk`/`delegate`/`discuss` are conversation, launch, and consensus entry points (`src/superharness/commands/talk.py:222`, `src/superharness/commands/delegate.py:793`, `src/superharness/commands/discuss.py:844`).
- There is no `shux queue` command; "queue" is only the `auto-dispatch` log verb for a task selected for enqueue (`src/superharness/commands/auto_dispatch.py:346`).
- Dispatch is workflow-gated, not status-global: `infer_workflow` defaults to `implementation` (`src/superharness/engine/next_action.py:217`), `allowed_statuses_for_workflow` returns a different dispatchable set per workflow (`src/superharness/engine/next_action.py:233`), and `plan_only_allowed_statuses` additionally admits `todo`/`plan_proposed` for implementation planning (`src/superharness/engine/next_action.py:271`).
- Three fanouts differ by trigger and aggregation: `parallel_dispatch` runs N isolated worktrees with no judge (`src/superharness/engine/parallel_dispatch.py:173`), `swarm` adds a reviewer vote with cheapest-slot fallback (`src/superharness/engine/swarm.py:106`), `ReviewFanout` runs read-only per-task reviewers and AND-merges verdicts (`src/superharness/engine/review_fanout.py:43`).
- Discussions are round-based with a quorum consensus gate (`agree`/`consensus`/`abstain` pass; `disagree`/`partial` block) (`src/superharness/engine/discussion.py:252`), advanced or closed by `cmd_advance` (`src/superharness/engine/discussion.py:559`), re-enqueued by `discussion_dispatch.dispatch` (`src/superharness/commands/discussion_dispatch.py:384`).
- Auto-dispatch scores adapters by keyword overlap and falls back to owner/`claude-code` (`src/superharness/engine/smart_dispatch.py:90`), splits roles into worktree/payload profiles (`src/superharness/engine/dispatch_profile.py:56`), and ships dry-run/print-only as its headless modes (`src/superharness/commands/auto_dispatch.py:386`, `src/superharness/commands/delegate.py:701`).
- Modules are YAML hook packs: templates live in `module_templates/` (`src/superharness/modules/registry.py:14`), `load_modules` reads `.superharness/modules/*.yaml` and skips disabled entries (`src/superharness/modules/loader.py:63`), `run_hooks(event, context, project_dir)` fires matching hooks (`src/superharness/modules/runner.py:57`).

---
## Workflow verbs
`enqueue` (`src/superharness/commands/inbox_enqueue.py:206`) validates the token, owner, and status gates (`src/superharness/commands/inbox_enqueue.py:88`) — `done` and `plan_proposed` are hard-blocked (`src/superharness/commands/inbox_enqueue.py:144`), other statuses are checked against `allowed_statuses_for_workflow`/`plan_only_allowed_statuses` (`src/superharness/commands/inbox_enqueue.py:159`) — then writes the row plus a ledger record in one SQLite transaction (`src/superharness/commands/inbox_enqueue.py:30`). `dispatch` (`src/superharness/commands/inbox_dispatch.py:777`) takes a mkdir lock (`src/superharness/commands/inbox_dispatch.py:814`), atomically claims the next pending row per agent (`src/superharness/commands/inbox_dispatch.py:740`), resolves execution context, transitions to `launched`, launches the agent, and reconciles to `done`/`failed`/`paused` (`src/superharness/commands/inbox_dispatch.py:837`). `watch` is the loop around dispatch: `_run_dispatch_cmd` spawns one detached `inbox_dispatch --to <target>` per agent (`src/superharness/commands/inbox_watch.py:524`), plus peer-review auto-approval for `plan_proposed` tasks (`src/superharness/commands/inbox_watch.py:793`), auto-review triggering (`src/superharness/commands/inbox_watch.py:1007`), and auto-close of `report_ready`/`review_requested` on LGTM (`src/superharness/commands/inbox_watch.py:1071`). `talk` (`src/superharness/commands/talk.py:222`) sends session-addressed messages as discussion rounds with `verdict="partial"` so auto-consensus never fires (`src/superharness/commands/talk.py:235`), keeping threads open up to `MAX_ROUNDS = 99` (`src/superharness/commands/talk.py:50`). `delegate` (`src/superharness/commands/delegate.py:793`) enforces scheduling/dependency gates (`src/superharness/commands/delegate.py:278`), content and lifecycle gates with permanent-block exit 2 (`src/superharness/commands/delegate.py:861`), optional preflight (`src/superharness/commands/delegate.py:952`), model/effort resolution, orchestrator routing, and prompt build before harness launch (`src/superharness/commands/delegate.py:643`). `discuss start` requires at least n-1 of available AI agents, minimum 2 (`src/superharness/commands/discuss.py:303`), seeds a `discussion`-workflow round-1 task (`src/superharness/commands/discuss.py:399`), and enqueues one inbox item per participant (`src/superharness/commands/discuss.py:469`).

## Orchestrator
`Orchestrator.route` returns owner+tier+effort+decompose in one model call with a `standard`/`medium` fallback (`src/superharness/engine/orchestrator.py:451`); `decompose` returns subtasks plus cost estimates (`src/superharness/engine/orchestrator.py:422`). The model chain tries Claude/Codex/Gemini/opencode/Pi max-tier entries per call (`src/superharness/engine/orchestrator.py:39`), order-shuffled with quality-score weighting so high-success models are picked first (`src/superharness/engine/orchestrator.py:173`), and per-pair success/failure is recorded after every attempt (`src/superharness/engine/orchestrator.py:206`). The prompt encodes the split policy: AC<=3 and files<=3 means no split, larger or cross-cutting means 2-6 subtasks, discussions never split (`src/superharness/engine/orchestrator.py:307`). `pi` routing is ignored unless the task carries the exact `agent:pi` opt-in tag (`src/superharness/engine/orchestrator.py:479`). Total failure degrades to a single `standard`-tier subtask covering the whole parent (`src/superharness/engine/orchestrator.py:720`). Project policy behind all of this is `shux workflow`: autonomy enum plus `default_preset` (implementation/quick/discussion/review/approval/note) and `require_tdd`, persisted to `.superharness/profile.yaml` (`src/superharness/commands/workflow_cmd.py:27`, `src/superharness/commands/workflow_cmd.py:43`).

## Fanout modes
`fanout_dispatch(project_dir, prompt, n)` (`src/superharness/engine/parallel_dispatch.py:173`) creates one `parallel/<task>-slot-<i>` worktree per slot (`src/superharness/engine/parallel_dispatch.py:202`), copies harness state in, runs SDK agents on threads (`src/superharness/engine/parallel_dispatch.py:229`), aggregates cost as sum and duration as max (`src/superharness/engine/parallel_dispatch.py:242`), and always removes worktrees in a `finally` block (`src/superharness/engine/parallel_dispatch.py:247`) — there is no judge, the caller merges via `_try_merge` (`src/superharness/engine/parallel_dispatch.py:142`). `swarm_dispatch` (`src/superharness/engine/swarm.py:106`) reuses the same worktree+thread pattern on `swarm/<task>-slot-<i>` branches (`src/superharness/engine/swarm.py:140`), then collects diffs, builds a compare-and-pick review prompt (`src/superharness/engine/swarm.py:46`), parses `WINNER:`/`REASONING:` lines (`src/superharness/engine/swarm.py:90`), defaults an invalid pick to the cheapest completed slot (`src/superharness/engine/swarm.py:252`), and only merges on `auto_merge=True` (`src/superharness/engine/swarm.py:270`). `ReviewFanout(project_dir, task_ids)` (`src/superharness/engine/review_fanout.py:55`) instead fans out one read-only `code_reviewer` per task via `delegate --print-only --json` (`src/superharness/engine/review_fanout.py:68`), runs them on a `ThreadPoolExecutor` (`src/superharness/engine/review_fanout.py:110`), and merges with AND semantics (`src/superharness/engine/review_fanout.py:43`):

```python
# src/superharness/engine/review_fanout.py:43
def merge_review_results(results: list[ReviewResult]) -> FanoutVerdict:
    all_findings: list[str] = []
    for r in results:
        all_findings.extend(r.findings)
    passed = all(r.passed for r in results)
    return FanoutVerdict(passed=passed, findings=all_findings, per_task=results)
```

## Discussion workflow
`cmd_start` inserts the discussion row (owners = participants, default `max_rounds=3`) and creates the on-disk scratch dir for `round-N-<agent>.yaml` files (`src/superharness/engine/discussion.py:79`, `src/superharness/engine/discussions_dao.py:38`). `cmd_submit_round` rejects non-participants, closed discussions, duplicate submits, and prompt-copy/ambiguous verdicts; only `agree|disagree|partial|consensus|abstain` are accepted (`src/superharness/engine/discussion.py:127`). Consensus is quorum, not unanimity (`src/superharness/engine/discussion.py:252`):

```python
# src/superharness/engine/discussion.py:249,252
_CONSENSUS_VERDICTS = frozenset({"agree", "consensus", "abstain"})
def compute_consensus(verdicts: dict[str, str], participants: list[str]) -> bool:
    n = len(participants)
    required = n if n <= 2 else n - 1
    submitted = {a: v.lower() for a, v in verdicts.items() if a in participants}
    if len(submitted) < required:
        return False
    return all(v in _CONSENSUS_VERDICTS for v in submitted.values())
```

All-agree in a round flips the discussion to `consensus` and may spawn `impl-*`/`action-*` follow-up tasks for non-agree points (`src/superharness/engine/discussion.py:270`, `src/superharness/engine/discussion.py:323`). `cmd_advance` reconciles YAML-only submissions into SQLite, then returns `advanced` (with an idempotent `_advance` marker), or `closed` with `consensus`/`max_rounds_reached` (`src/superharness/engine/discussion.py:559`). The dispatcher loop (`src/superharness/commands/discussion_dispatch.py:384`) recovers orphaned `launched`/`running` rows (`src/superharness/commands/discussion_dispatch.py:217`), auto-closes discussions past their effort deadline (low 10m / medium 20m / high 30m) (`src/superharness/commands/discussion_dispatch.py:426`), advances complete rounds with an inbox idempotency guard (`src/superharness/commands/discussion_dispatch.py:508`), and for incomplete rounds only re-enqueues pending agents with no active item, no YAML on disk, no DB submission, availability OK, and retry budget left (`src/superharness/commands/discussion_dispatch.py:546`). `cmd_close` sets the terminal status and cancels all matching `disc_id/round-%` inbox rows in one update, then terminates still-launched agent processes (`src/superharness/engine/discussion.py:930`).

## Auto-dispatch
`run_auto_dispatch` scans `todo` tasks only (`src/superharness/commands/auto_dispatch.py:45`), skips anything with an unresolved `blocked_by` (`src/superharness/commands/auto_dispatch.py:304`), classifies each task, and either enqueues directly or decomposes first when effort meets `--effort-gate` (default `high`) with `--orchestrate` (`src/superharness/commands/auto_dispatch.py:268`). Classification is two-stage: `model_router.classify_task` for the tier plus `smart_dispatch.choose_agent` for the agent, with fully-experimental adapters demoted to explicit-`--agent`-only (`src/superharness/commands/auto_dispatch.py:72`). Scoring itself is keyword overlap over manifest `tags`/`skills`/`strengths` (`src/superharness/engine/smart_dispatch.py:74`), resolved against project then bundled manifests (`src/superharness/engine/smart_dispatch.py:50`), falling back to owner then `claude-code` on empty keywords or zero score (`src/superharness/engine/smart_dispatch.py:111`, `src/superharness/engine/smart_dispatch.py:131`). Enqueue defaults to `plan_only=True` for the `implementation` workflow and direct execution otherwise, with discussion round tasks bypassing plan-only when the profile flag allows (`src/superharness/commands/auto_dispatch.py:130`). Role shaping comes from `DispatchProfile.for_role` (`src/superharness/engine/dispatch_profile.py:56`): orchestrator/worker get full payload with context inheritance, while `validator`/`code_reviewer` force a fresh worktree, no context inheritance, and a filtered payload of locked contract + diff + report (`src/superharness/engine/dispatch_profile.py:15`). Headless operation is `--dry-run` (count without writes, `src/superharness/commands/auto_dispatch.py:292`) and delegate/dispatch `--print-only` preview paths (`src/superharness/commands/delegate.py:701`).

## Module templates
Template files ship in `src/superharness/module_templates/` (`auto-schedule`, `ntfy`, `obsidian`, `openclaw`, `remember`, `security`, `ship`, `telegram`), resolved as the built-in dir in `TEMPLATE_DIR` (`src/superharness/modules/registry.py:14`); `available_modules` lists stems (`src/superharness/modules/registry.py:17`), `enabled_modules` reads `.superharness/modules/*.yaml` with `enabled: true` (`src/superharness/modules/registry.py:29`). `load_modules` loads that project dir, validates each manifest against the SDK v1 schema, and drops invalid or disabled entries (`src/superharness/modules/loader.py:63`); the `Module` record is name/enabled/hooks/settings/detect/file_path (`src/superharness/modules/loader.py:35`). `run_hooks` rejects unknown events, matches `module.hooks[event]`, honors `condition`, and dispatches the named registered action (`src/superharness/modules/runner.py:57`). Format is fixed: `schema_version`, `name`, `description`, `enabled`, `detect`, `hooks.<event>.action`, `settings`. Verbatim sample (`src/superharness/module_templates/ship.yaml:1`):

```yaml
# src/superharness/module_templates/ship.yaml:1
schema_version: '1'
name: ship
description: "Auto-commit and push on task close"
enabled: false
detect:
  bin: git
hooks:
  on_close:
    action: git_ship
settings:
  auto_push: false    # default: commit only, ask before push
```

Note: `tests/contract/test_workflow_policy.py` is a name collision — it freezes GitHub Actions SHA-pinning and step-level secret scope (`tests/contract/test_workflow_policy.py:30`), not task-workflow verbs, and is otherwise out of scope for this page.

**Covers:** workflow verbs, orchestrator sequencing, fanout vs swarm vs review_fanout, discussion rounds/consensus/auto-close, auto-dispatch scoring/profiles/headless, module template format/loader/registry/runner.
