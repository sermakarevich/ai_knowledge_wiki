> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evidence Discipline and Acceptance Iron Rules

**In one sentence:** Every acceptance claim carries one of four evidence labels — direct, proxy, local, blocked — upgrading a label is lying, and no branch merges until the orchestrator independently re-verifies commits, diffs, gates, and claims.

## Key points

- Four evidence levels: `direct` (real target environment), `proxy` (substitute or intermediary), `local` (dev/test only), `blocked` (needs human, credentials, hardware, or a product decision) (playbook `README.md:29-38`).
- House rule: "Upgrading an evidence label is lying" — never upgrade `local→proxy` or `proxy→direct` (`SKILL.md:519`); the founding incident was a local unit test labeled proxy, later cited as direct (playbook `README.md:38`).
- `direct` requires device readback, callback-backed ACKED, processor/DB artifact, or physical evidence; `SENT`/TCP/screenshot/oral confirmation are proxy at best (`SKILL.md:520-521`).
- Iron rule 1: a worker's "committed" is not evidence — acceptance opens by proving `git log <branch> --not main` is non-empty (founding incident: uncommitted work lost with a force-removed worktree).
- Iron rule 2: never trust self-reported gates — re-run key gates on the acceptance side; iron rule 3: review ≠ authorization to merge/push/deploy/cleanup; iron rule 4: remove worktrees only after the merge is verified (playbook `README.md:55-60`).
- The adapter adds a live-proof gate: anything touching runtime, production, device, payment, hardware, provider, or external service needs `direct` proof or an explicit item-specific waiver; `local` gates are insufficient (`SKILL.md:258`).
- A mandatory post-merge integration test runs after every batch because per-branch gates passing does not prove the layers work together (`SKILL.md:302-309`).

---

## The four levels

| Label | Meaning | Examples |
|---|---|---|
| `direct` | Real target environment | device readback, production log, payment confirmation, callback-backed ACKED, DB/API artifact |
| `proxy` | Substitute or intermediary | staging, screenshot, TCP liveness, SENT status, oral confirmation, mock |
| `local` | Dev/test only | unit test, local build, `diff --check`, static analysis |
| `blocked` | Unobservable | needs human, credentials, hardware, production access, product decision |

Project-specific evidence rules take precedence over the defaults (`SKILL.md:524`). Reviewers must actively catch exaggeration — local claimed as proxy, TCP reachability as payment proof (`SKILL.md:252-253`; ORC-02).

## The acceptance checklist

Per-branch acceptance (`SKILL.md:227-258`):

1. **Phantom-commit check** — `git -C <worktree> status --short --branch; git log --oneline -3`; commit on the agent's behalf if needed (`SKILL.md:227-238`).
2. **Diff boundary check** — `git -C <worktree> diff --name-status main..HEAD` + `diff --check main..HEAD`; allowed-paths-only, no forbidden contracts (`SKILL.md:242-249`).
3. **Checklist** — boundaries, self-review, gate re-run, evidence honesty, claim verification, idempotency, authorization separation, live-proof gate (`SKILL.md:247-258`).

## Merge hygiene and rescue

- Be on main before merging; merge with `--no-ff`; push to `origin/main` after serial batches so the next worktrees see prior work (`SKILL.md:264-283,314`).
- Out-of-bounds or stale-base rescue: `checkout main` + `cherry-pick <commit> --no-commit`, inspect staged, `reset`/`checkout --` forbidden files, commit in-scope only, remove worktree, delete branch (`SKILL.md:272-284`; `full-guide.md:80`).
- Simple doc conflicts: keep both entries; conflicts in shared contracts, migrations, aggregates, or protocols → stop for manual review (`SKILL.md:288`).
- P1 hotfix carve-out: the orchestrator may directly edit ≤5 lines in one file (`SKILL.md:777`) — a deliberate ORC-07-adjacent exception relying on labeling discipline alone.

**Covers:** orchestration-playbook `README.md:29-38,55-60`; claude-orchestrator `SKILL.md:227-309,508-524,777`, `docs/full-guide.md:80`.
