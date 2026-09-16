**Figure 4 — Long‑horizon control mechanisms.** This is not a quantitative plot (no axes or data trends); it is a set of three schematic flow diagrams, each illustrating one control primitive exposed by the Prime Agent harness for sustained, multi‑turn operation.

- **Autonomous mode (left panel).** A dashed "EXPLICIT BUDGET" header sits above a loop: a `TURN` block feeds a `TEST` decision diamond, which either passes through to `END` ("pass") or routes back via a "continue" edge to another `TURN`. The takeaway is that execution keeps taking turns until a task‑specified end‑condition test passes, with the budget (turn/token/wall‑clock limits) bounding the loop.

- **Goal (middle panel).** A dashed "PERSISTENT GOAL" header sits above a loop: `TURN` → `DONE?` diamond → `END` ("yes") or a "continue" edge back to `TURN`. The takeaway is that the objective persists across continuations and the loop ends only when the agent itself marks the goal complete (agentic completion), rather than by an external test.

- **Heartbeats (right panel).** A chain of clock icons linked by a dashed line, each pointing down to a `TURN` block. The takeaway is that turns are initiated externally on a cron/timed schedule rather than by an internal pass/fail condition.

**Overall takeaway:** the figure conveys the three complementary ways the harness drives long‑horizon work — budget‑bounded test‑gated loops, agent‑judged goal completion, and time‑triggered heartbeats — i.e., the control semantics that let a single runtime sustain extended, self‑directed execution.