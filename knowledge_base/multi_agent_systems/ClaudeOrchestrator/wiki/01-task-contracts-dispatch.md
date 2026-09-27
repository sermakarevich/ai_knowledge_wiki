> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Task Contracts and Dispatch

**In one sentence:** Every agent dispatch carries a bounded ten-field contract — outcome, anti-shallow-slice class, change rationale, boundaries, gates, evidence, challenge duty, restart policy, rubric, handoff — and without a contract there is no dispatch.

## Key points

- The contract is the central domain object: ten required fields, "no contract, no dispatch" (playbook `README.md:40-53`).
- Every task declares an anti-shallow-slice classification — `vertical-completion | runtime-proof | blocked-removal | owner-gated` — plus why it is not repeating an already-completed first slice.
- Boundaries are explicit: allowed paths, forbidden paths, branch name (`build/<slug>`), base commit (`origin/main`); concrete gate commands replace the word "passed".
- Agents have a duty to challenge unclear, risky, or over-broad contracts and stop instead of guessing (`SKILL.md:385-389`).
- The restart policy is inside the contract: repeated same-gate failure, contract drift, or noisy patch-on-patch means stop and recommend a clean restart (`SKILL.md:414-416`).
- The Claude adapter expands the ten fields into a twelve-section prompt template adding MUST-COMMIT, Common P1 Patterns, the Minimalism Ladder, shared-resource append-only rules, and a ≤~30-line handoff cap (`SKILL.md:350-464`).
- Handoffs report branch, commit hashes, file list, actual gate output, and residual risks — never the bare word "passed".

---

## The ten fields

From the playbook core (`README.md:40-53`):

1. **Outcome definition** — what counts as correct vs a real blocker.
2. **Anti-shallow-slice classification** — one of `vertical-completion | runtime-proof | blocked-removal | owner-gated`, with the reason this task is not a repeat of a completed first slice.
3. **Minimum-change rationale** — why reuse, deletion, config, or docs-only cannot solve it.
4. **Boundaries** — allowed paths, forbidden paths, branch name, base commit.
5. **Acceptance gates** — concrete commands; "not green = not done".
6. **Evidence requirements** — labeled per the four-level discipline (see [[03-evidence-discipline-acceptance-rules|Evidence Discipline]]).
7. **Duty to challenge** — report back and ask for a narrower contract before editing; do not guess (playbook `README.md:50`).
8. **Restart policy** — repeated same-gate failure → clean restart from the contract (playbook `README.md:51`).
9. **Subjective rubric** — axes, weights, scale, and evidence source whenever taste, UI, workflow, or parity matters; "without rubric, looks good is unfalsifiable".
10. **Handoff format** — branch, commit hashes, file list, actual output of every gate, residual risks.

## Adapter template (twelve sections)

The Claude adapter implements the contract as a prompt template (`SKILL.md:350-464`) pinning `Base: origin/main`, `Branch: build/<task-slug>` (`SKILL.md:366-370`), with additions the core does not have:

| Addition | Location | Content |
|---|---|---|
| MUST-COMMIT rule | `SKILL.md:390-393` | Agent must commit; uncommitted work is the #1 subagent failure mode |
| Common P1 Patterns | `SKILL.md:418-425` | Five checks (DTO naming, all-states coverage, tenant scoping, integer cents, null handling) claimed to cover ~40% of P1s |
| Minimalism Ladder | `SKILL.md:427-436` | delete → stdlib → dependency → inline → keep-minimum; never simplify security/error-handling/a11y |
| Shared-resource rules | `SKILL.md:438-443` | Append-only for strings.xml, nav graphs, DI, route registries |
| Handoff cap | `SKILL.md:453-463` | ≤~30 lines; detail goes into repo files, not the handoff |

## Supporting gates

- **Design-First gate** for high-risk work: design doc → verify premises by opening cited code → implement (`SKILL.md:143-168`).
- **Model-tier-by-consequence:** tier by cost of a wrong answer, not task size; reviewer lanes must differ in family, not tier (`SKILL.md:170-198`).
- **Decision Brief discipline:** What / Why / evidence-gathered-vs-missing / Options / Recommendation / Branch (`SKILL.md:680-690`).
- **Contract-sync gate:** blocks dispatching a contract-only branch when consumers must change in lockstep — fold minimal consumer wiring into the same serial task or stop (`SKILL.md:103`; `full-guide.md:85`).

**Covers:** orchestration-playbook `README.md:40-53`; claude-orchestrator `SKILL.md:101-118,143-198,350-464,680-690`.
