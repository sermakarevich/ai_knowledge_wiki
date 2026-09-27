# Chapter 10a — order-management agent: scaffolding + a 3-task temperature-0 demo

This is **half 1** of chapter 10 (`specs/10_agent_evals_impl.md`): the deterministic
mock shop DB, the 8 policy-bound tools, the tool-calling agent loop, the 20
hand-written tasks, the code graders (state / forbidden / step-budget / required
tools / reply keywords) and `pass@k` / `pass^k`, offline tests, and a small
temperature-0 demo. The full 20-task run, the transcript LLM-judge and the
multi-turn `simulate` (half 2) are deliberately **out of scope here**.

Why grade state, not text: an agent can reach the right outcome by many paths —
or reach a *wrong* outcome the "good" way. The grade is therefore the **final DB
state** after the episode, plus **path constraints** (forbidden tools, step
budget, required tools) and a light check on the reply. Text grading (a
transcript judge) is added in half 2 and cross-checked against this state grade.

## What was built

- **Mock shop DB** (`agent.py`): 15 orders / 12 customers seeded deterministically
  across the five statuses (`placed, shipped, delivered, returned, cancelled`),
  items (incl. custom-configured, non-returnable), addresses, fees and prior
  refunds. `fresh_db()` returns an isolated copy per episode; `snapshot()` /
  `diff()` give before/after state for the grader and the findings.
  Clock is frozen at `2026-09-01T12:00:00Z` so the policy windows (24 h address
  lock, 30-day returns, 200-refund escalation) grade deterministically.
- **8 tools**, each a plain Python function that mutates the episode DB and
  returns a JSON dict, with matching OpenAI-style JSON schemas for tool calling:
  `lookup_order`, `list_orders`, `cancel_order`, `update_address`, `start_return`,
  `issue_refund`, `escalate`, `reply` (ends the episode). Policy rules from the
  handbook are enforced **inside the tools** (e.g. `issue_refund` refuses ≥ 200
  without a started return or a recorded `escalate`; `start_return` refuses
  custom items and out-of-window returns) so a policy violation can never be made
  — the episode is then graded off the *attempt* plus the resulting state.
- **Agent loop** `run_episode(task, llm, ...)`: system prompt
  `prompts/agent_v1.txt` + the two handbook sections, tool-calling loop with
  `qwen3.8:27b`, max 12 steps, records the full trajectory (messages, tool calls
  with args + results, final DB diff, steps, per-task grade).
- **20 tasks** (`data/agent_tasks.jsonl`): **11 straightforward, 7
  policy-refusal** (correct outcome = no state change + a polite explanation),
  **2 needing `escalate`**, plus a couple of ambiguous orders that must be
  resolved from the email. Each carries `expected_state`, `required_actions`,
  `forbidden_actions`, `max_steps`, `expected_reply_keywords`, and a `category`
  of `straightforward` / `policy` / `escalation`.
- **Grading** (`grade_episode`): `state`, `required_tools`, `no_forbidden_tools`,
  `within_step_budget`, `final_reply` → `pass` = all five. `pass@k` (any trial —
  *capability*) and `pass^k` (all trials — *reliability*, Yao et al. 2024 / τ-bench)
  aggregate per task.
- **CLI** (`just agent-*`): `demo`, `run`, `grade`, `simulate` (stub), `all`.
- **Tests** `tests/test_10_agent.py` — 32 offline cases (no network): DB
  determinism, each tool's happy path + policy refusal, refund caps & escalation,
  `call_tool` error handling, graders (pass + each failure kind), `pass@k`/`pass^k`
  on synthetic trial matrices, and `run_episode` integration via a scripted `StubLLM`.
  All green: `uv run pytest tests/ -q -m "not slow"` → **165 passed**.

## The temperature-0 demo (`runs/10_demo/`, `just agent-demo`)

3 hand-picked tasks × 1 trial (temp 0): `pass@1 = 1.0`, `pass^1 = 1.0`.
Each pass is below the 12-step budget; the model used ≤ 3 tool calls each.
Wall time for the episode LLM turns: **8 calls, ~23 s total** (one turn per
step + the final reply; per-turn 1.1–4.0 s on the local Ollama, qwen3.8:27b).

| Task | Type | Outcome | Tools (order) | Why it passed |
|---|---|---|---|---|
| **t01** | straightforward cancel | ✅ | `lookup_order → cancel_order → reply` | Order was `placed`; cancel succeeded, refund 120 recorded, no fee. Reply confirmed the cancellation. |
| **t05** | policy refusal | ✅ | `lookup_order → reply` | Custom (personalized) jersey already in `returned` status — non-returnable. Correct behaviour: **no state change** + an apologetic explanation. |
| **t19** | ambiguous order | ✅ | `list_orders → lookup_order → reply` | "the framed bag" was ambiguous between two maya.chen orders; agent disambiguated to **O121**, noted it was delivered, and explained the 24 h address window had closed (polite refusal, no state change). |

Two of the three are *refusal* tasks — the agent declined to act and changed
nothing, which is the harder case: a naive model would "helpfully" mutate state
and lose the state/forbidden checks.

Per-task detail (from `trajectories.jsonl`):

| Task | Steps (LLM turns) | Tools in order |
|---|---|---|
| t01 | 3 | lookup_order, cancel_order, reply |
| t05 | 2 | lookup_order, reply |
| t19 | 3 | list_orders, lookup_order, reply |

Tool-calling quirks observed in the demo:
- The model always ends with a `reply(...)` tool call (not a bare text turn),
  even though the prompt allows both — the loop treats either as the final
  reply, so this costs no extra step.
- No tool arguments were malformed: every `arguments` field was valid JSON on
  the first try; no retries needed.
- Multi-call turns: the model issued exactly one tool call per turn; it never
  batched two tools in one turn (the loop supports both).
- On the ambiguous order (t19) the model disambiguated via `list_orders`
  before acting — no wasted `lookup_order` on a guessed id.

### Bugs found and fixed while wiring this up

- **`def all()` shadowed the builtin `all`.** The Typer `all` command name made
  every `all(iter)` call inside the module resolve to the Typer command — so the
  *grader* would fire the whole CLI. Renamed the function to `run_all` with
  `@app.command(name="all")` so the CLI name is unchanged but the builtin is
  unshaded.
- **`issue_refund` ignored a recorded escalation.** Previously a ≥ 200 refund with
  no started return was refused even after `escalate()`; now a recorded escalation
  is honoured (still refuses if neither a started return nor an escalation exists).
- **Asset paths resolved one level too high.** Prompt / `data/` / handbook live at
  different depths across layouts; `load_system_prompt` / `load_tasks` now search
  candidate bases rather than assuming a single root.
- **Missing `if __name__ == "__main__": app()` guard**, so `python -m ...agent`
  exited silently without doing anything.

## Not done here (half 2)

- The full **20 × 3 = 60-episode** run (`just agent-run`, ~240 LLM calls) and its
  `pass@3` / `pass^3` with bootstrap CIs in `runs/results.md`.
- **Transcript LLM-judge** (`agent_transcript_judge_v1.txt`) and its agreement
  (κappa) with the state grade.
- **`simulate`** multi-turn episodes with a simulated user answering the agent's
  clarifying questions.
- Note: two seed facts are under the spec's target — the DB seeds **15 orders / 12
  customers** vs the 30 the spec names, to keep the demo and the deterministic
  grading tractable within the ≤ 50 LLM-call budget for this half.

## Reproduce

```
just agent-demo        # 3 tasks, temp 0 → runs/10_demo/{metrics,trajectories,config}
just agent-grade       # re-derive pass@k / pass^k from a saved trajectories.jsonl (no LLM)
```
