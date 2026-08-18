# Extract wiki page 01: Graph engineering enterprise guide

## Context

This is a short article, not a book. Read ONLY the file below, nothing else. Do not read this
task's own fleet artifacts/log/event files, and do not read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. Context is tight on
this model.

## Input

Read this file in full (plain text, small):

`/Users/sergii/.kb/papers/TrueFoundryGraphEngineeringEnterprise/source/chunks/01.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/TrueFoundryGraphEngineeringEnterprise/wiki/01-graph-engineering-enterprise-guide.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graph Engineering Enterprise Guide

**In one sentence:** <one sentence capturing the article's whole argument>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>
- <complete-claim bullet 6>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Cover: the definition of graph engineering and how it differs from knowledge-graph
engineering; the three historical roots (dataflow computation, multi-agent systems
research, organizational practice) and the "naming event" framing; where graph
engineering sits in the prompt/context/loop/graph layered hierarchy and why the layers
compose rather than supersede; the enterprise governance requirements (identity, gateway
policy, tool-level restrictions, the four guardrail hooks, cross-agent prompt-injection
risk); cost control mechanics (fan-out/retries increasing calls, budget and rate-limit
rules by tenant/team, the graph_id/node_id correlation pattern with its illustrative
header example verbatim); observability (gateway metrics vs. orchestrator traces, who is
source of truth for what); structural/human approval checkpoints; optimization via
node-level attribution (cheaper models, caching, fallback chains); the seven-item
enterprise checklist verbatim; the future-outlook predictions; the closing TrueFoundry
perspective quote; the FAQ Q&A pairs; and the technical metrics (latency ~10ms under
load, ~3-4ms core gateway latency, 350+ RPS on 1 vCPU) plus the product boundary
statement about Agent Harness's current limits (no nested subagents, no independently
configured specialist subagents).>

**Covers:** Entire article — definition, history, layered hierarchy, enterprise
governance/cost/observability, checklist, future outlook, FAQ, metrics, product
boundaries (source chunk 01, full article)
```

Key points must be complete standalone claims (not topic labels like "discusses governance")
— someone reading only the key points should have the article's substance. Preserve the
seven-item checklist and the cost-correlation header example precisely, since those are the
article's most specific technical content.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 01 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
