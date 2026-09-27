> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: swarmclawai/swarmvault

## Claims vs. evidence
- Claim: one-command local-first wiki+graph from any source (`quickstart`/`scan`, no API keys via heuristic provider). Evidence in-slice: README flows and disk layout (`raw/`, `wiki/`, `state/graph.json`) are documented; heuristic output quality is not measured anywhere in this slice.
- Claim: trust via typed edges (`extracted`/`inferred`/`ambiguous`), contradiction detection, approval bundles, `lint --conflicts`. Evidence: command names and staging dirs exist in docs; no precision/recall numbers, no adversarial examples, no test results cited.
- Claim: scales past 100 pages via hybrid SQLite FTS + embeddings, bounded compile, graph traversal (`query`/`path`/`explain`/`callers`). Evidence: dependency footprint (graphology, SQLite FTS, embeddings) and `SCALE.md` tier table are consistent with the claim; the numbers read as budgets, not measured runs.
- Claim: 30+ input formats, tree-sitter code awareness, graph viewer, MCP server, Obsidian plugin, Neo4j export, watch mode. Evidence: package deps (parsers, cytoscape, MCP SDK, neo4j-driver, obsidian) make these plausible; none are exercised or demoed in this slice.
- Claim: team-ready (git `--commit`, hooks, scheduling, `STABILITY.md` semver contract). Evidence: contracts and config knobs exist on paper; no multi-user conflict, merge, or redaction behavior is evidenced.
- Claim: healthy repo hygiene (Biome 2.4.10 + lefthook pre-commit, strict `ES2022` TS baseline, locked pnpm workspace). Evidence: this one is actually verifiable in-slice — configs are quoted verbatim and consistent, which raises the prior on engineering discipline without proving runtime quality.
- Claim: multilingual reach (Japanese and Simplified Chinese READMEs). Evidence: both localizations exist but were truncated in the chunk, and both defer to English README as authoritative — reach is real, parity is unconfirmed.
- Claim: bounded, reviewable evolution (`compile --approve`, `compile --max-tokens`, candidates-first). Evidence: the mechanism names and staging locations are documented; whether reviewers can actually keep up at Medium/Large tier volumes is untested.
- Net: the strongest evidence is structural (monorepo, pinned deps, scale/stability docs); the weakest is empirical (quality, accuracy, and performance claims rest on README/SCALE assertions).

## Genuinely new vs. repackaged
- Genuinely useful packaging: the Karpathy three-layer gist (immutable `raw/`, compounding `wiki/`, co-evolved schema) turned into an actual CLI loop (`init`/`ingest`/`compile`/`query`/`next`/`doctor`) with approval staging and agent context packs. That workflow glue is the real contribution.
- Repackaged commodity stack: SQLite FTS + embeddings hybrid search, Louvain clustering, Cytoscape viewer, MCP server, Obsidian plugin, Neo4j sink, tree-sitter parsing — each is a standard component, and the gist-to-production table mostly compares "described" vs "shipped" rather than showing a novel algorithm.
- Positioning vs. peers: closest to Obsidian + Dendron + code-graph indexers + RAG-over-repo tools, with the differentiator being graph-typed, approval-gated, agent-consumable output rather than any retrieval breakthrough.
- What would count as genuinely new: published contradiction-detection evals, graph-guided-vs-naive token/accuracy deltas from `benchmark.json` on public corpora, or a demonstrated cold-compile story at Medium tier — all absent in this slice.
- Credit where due: edge typing, candidates-first landing, bounded context-pack budgets, and the `benchmark.json` naive-vs-graph-guided token comparison are sensible, uncommon-together choices — integration novelty, not research novelty.

## Weaknesses and blind spots
- Evidence gap dominates: this slice covers only the overview and repo-root files; engine, CLI, viewer, and test internals are unverified, and `pnpm-lock` plus localized READMEs were truncated in the chunk.
- Quality claims are uncalibrated: heuristic-provider extraction, contradiction detection, and rerank behavior have no reported metrics; offline-first may mean mediocre-first on hard corpora.
- Scale table tension: Large tier promises 400k nodes / 1.5M edges with <15 min warm compile, yet notes admit 3x-6x cold slowdowns, god-node memory pressure (`--max-old-space-size=8192`), FTS shard limits, and a ~10k-node Cytoscape viewer ceiling — the graph outgrows its own viewer by 40x.
- Operability costs: Node `>=24`, embedding/audio provider setup, Neo4j sink, git-hook watch mode, and per-source audio cost add friction the "30 seconds" pitch understates.
- Team and safety gaps: no evidenced story for concurrent edits, secret/redaction enforcement (`redaction.*` keys are declared, not demonstrated), private-repo ingest scope, or license hygiene of ingested material.
- Lock-in shape: vault conventions (`swarmvault.schema.md`, frontmatter, `state/` files) are sticky; migration outward via exports (HTML/Obsidian/Cypher) is promised but untested here.
- Freshness model is declared, not demonstrated: `freshness.defaultHalfLifeDays` and decay scores suggest stale-page handling, but no decay behavior, re-ingest semantics, or source-reload conflict story is evidenced in this slice.
- Desktop-only Obsidian plugin (`isDesktopOnly`, app `>=1.5.0`) plus a Glama registry stub narrow the verified client surface — mobile/web and registry maturity remain open questions.
- No security posture in-slice: offline-first helps privacy, but secret handling (`.env` exclusion is a start, not a policy), ingested-credential scrubbing, and share-kit oversharing risk (`share-card`/`share-kit` are designed to be copyable) are unaddressed.

## Applicability
- Personal research vaults, book/paper companions, and meeting-transcript archives: fits well if heuristic quality suffices.
- Repo comprehension and onboarding maps (`graph callers`/`path`/`explain`, callflow exports): plausible second use, pending verification on a real codebase.
- Agent context supply (bounded `context build`, task ledger, MCP tools): the most interesting fit — treats the vault as durable agent memory rather than chat scratch.
- Suggested trial shape: `demo`, then `quickstart` on a small real repo, then compare `benchmark.json` naive vs graph-guided tokens on 3-5 fixed questions before judging.
- Non-fits: real-time collaborative editing, regulated data with strict redaction proofs, and corpora far above the Medium tier without a Neo4j-backed plan.
- Team knowledge base or production RAG: premature on this evidence; needs conflict handling, evals, and redaction proof first.
- **Relevance to my work**
  - AI/ML engineering: candidate pattern for experiment-note and paper-trail vaults with typed provenance edges; worth copying the `extracted`/`inferred`/`ambiguous` tagging and candidates-staging discipline.
  - Agentic systems: context packs + MCP `query`/`explore`/`page` tools + task ledger map directly onto agent memory needs; trial as a bounded context supplier before building custom.
  - Elisity data platform: treat as reference architecture for docs/runbook indexing and onboarding graphs, not as a dependency — data-source connectors, access control, and evals would all need Elisity-grade replacements.

## What this changes
- If the trust and budget mechanics hold, it changes the default from "re-ingest the repo into every agent session" to "compile once, serve bounded graph-guided context" — with `benchmark.json` token comparisons as the receipt.
- It reframes knowledge work as pipeline work: immutable sources, staged approvals, lintable contradictions, versioned schema — closer to CI for knowledge than to a notes app.
- It reframes knowledge work as pipeline work: immutable sources, staged approvals, lintable contradictions, versioned schema — closer to CI for knowledge than to a notes app.
- It does not change the underlying retrieval science; it changes who pays the integration tax (the tool, upfront) versus the agent (per-prompt, forever).
- The `SWARMVAULT_OUT` split (generated artifacts under one dir, config/schema at root) and the zero-install schema template lower the trial cost — the design visibly optimizes for "try before you commit."
- The `next`/`doctor` loop (read-only next-action suggestion plus health-and-repair guidance) is a small but real usability bet: vaults rot, and a tool that notices rot is more trustworthy than one that silently serves stale pages.
- Concretely: worth a local `demo`/`quickstart` spike and a token-cost comparison before any architectural commitment.

## Verdict
- Useful integration of proven parts, oversold on autonomy-relevant claims (accuracy, contradiction handling, large-tier smoothness) relative to the evidence in this slice.
- The honest shape is a well-specified personal/agent vault with team features declared but unproven — verify engine behavior and quality metrics before trusting it with shared or sensitive corpora.
- Next evidence to demand: engine/CLI internals, retrieval evals, cold-compile timings, and a real multi-thousand-page vault walkthrough.
- Cost of being wrong is low for a local trial (scratch folder, no API keys) and high for a team rollout (sticky conventions, git-hook coupling) — sequence accordingly.
- Trial exit criteria: abandon if heuristic extraction needs heavy cleanup on your own corpus, or if cold-compile on a Medium-size repo misses the documented budget by far.
- **trial** — spike it locally for agent context packs; **watch** for team-wide or production adoption.
