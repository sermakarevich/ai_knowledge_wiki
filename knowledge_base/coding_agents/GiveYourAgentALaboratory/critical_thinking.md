> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: Give your agent a laboratory

## Claims vs. evidence
- Core claim: agents are only as good as their feedback loop, so prompts matter
  less than giving the agent tools to view and verify its own work.
- Evidence offered is two worked examples (performance harness, Figma visual
  loop), not controlled comparison — persuasive as demonstration, weak as proof.
- The "vague prompts fail" diagnosis rings true (short effort, repeated check-backs,
  fix-one-break-another), but the digest gives no baseline: no A/B of terse vs.
  scaffolded prompts, no success rates, no cost/latency numbers.
- Strongest evidential move: each pattern names a falsifiable loop (benchmark delta,
  enumerated visual diffs). Weakest: both assume the harness itself is correct.
- Verdict on evidence: sufficient to justify trying the pattern, insufficient to
  support the universal framing ("only as good as", "must", "really really hard").

## Genuinely new vs. repackaged
- Genuinely sharp: the inversion "build the laboratory before touching code" and
  the rule "if the agent asks you to do something manually, tool it instead."
- The expected-wrong first pass is a useful norm: it legitimizes iteration and
  reframes pass one as scaffolding, not failure.
- Repackaged: instrument → diagnose → iterate → report is classical performance
  engineering; screenshot-compare-fix is classical visual QA. The novelty is
  pointing these loops at an agent rather than a human.
- Skills-encoding advice ("get reps first, formalize later") restates known
  abstraction discipline: premature generalization produces brittle libraries.
- Net: old engineering discipline, new target. The contribution is packaging and
  timing (MCP-era tooling makes the loop cheap), not theory.

## Weaknesses and blind spots
- No discussion of harness validity: a benchmark that measures the wrong path, or
  a screenshot comparison blind to accessibility/state, optimizes the wrong thing.
- Cost blindness: benchmark + screenshot loops burn tokens, time, and MCP calls;
  no guidance on when the laboratory costs more than the task is worth.
- Flaky-loop risk: performance noise, nondeterministic rendering, and responsive
  breakpoints can trap the agent in fix-one-break-another cycling with no stop rule.
- Boundary rule ("flag big architectural changes and move on") is hand-waved; the
  hardest judgment — what not to automate — gets one sentence.
- Security/provenance gaps: pulling Figma via MCP and granting browser/devtools
  access widens the agent's action surface; no mention of sandboxing or review gates.
- Single-author, single-era evidence: January 2026 frontier-model behavior; the
  "models are lazy" claim may decay as models and harnesses improve.

## Applicability
- Applies where verification is automatable: benchmarks, tests, screenshots,
  schemas, reproducible pipelines. Weakens where ground truth is judgment-laden
  (taste, API design, novel architecture).
- Performance lab transfers directly to backend/data work; visual lab transfers to
  any pixel-spec task (marketing pages, dashboards, admin UI).
- Precondition checklist: can the agent run the harness itself? Is the oracle
  trustworthy? Is there a stop rule (diff count, benchmark threshold, max loops)?
- **Relevance to my work**
  - AI/ML engineering: eval harnesses are the laboratory — baseline metrics, error
    slices, and regression gates before letting an agent touch training or eval code.
  - Agentic systems: the "tool it instead of asking" rule is a design principle —
    every manual check-back is a missing tool (retriever, sandbox, diff viewer).
  - The Elisity data platform: perf-lab pattern fits ingestion/query hot paths
    (baseline traces, top bottlenecks, one-change-per-commit); visual lab fits
    console dashboards where Figma specs meet real data states.

## What this changes
- Prompting practice: stop polishing adjectives; start specifying oracles — what
  the agent will run, measure, and compare, and what "done" looks like numerically.
- Workflow order: instrumentation first, code second. A task without a harness is
  a task you are not ready to delegate.
- Skill strategy: treat long prompts as prototypes; only promote repeated,
  validated loops into `./claude/skills` with clear rerun descriptions.
- Calibration habit: vary scaffolding by job size — full four-phase lab for audits,
  lightweight check-back for small edits — and build feel through reps.

## Verdict
- The essay overclaims (universal laws from two anecdotes) but the prescription
  survives contact with skepticism: verifiable loops beat verbose wishes, and the
  two patterns are concrete enough to steal today.
- Main risk is misapplication — expensive loops, untrusted oracles, missing stop
  rules — so adopt the principle but gate the heavyweight form behind task value.
- For evaluatable engineering work with a runnable oracle, this is immediately useful;
  for open-ended design judgment, treat it as scaffolding, not salvation.
- Call: **trial**
