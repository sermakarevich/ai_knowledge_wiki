> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Enforcing Architecture and Taste

**In one sentence:** Coherence in a fully agent-generated codebase comes from mechanically enforced invariants, a rigid layered domain architecture with a single Providers interface, and a deliberately permissive merge philosophy justified by agent-scale throughput.

## Key points

- The governing rule is enforcing invariants rather than micromanaging implementations: the team requires Codex to parse data shapes at the boundary but does not prescribe how (the model tends toward Zod, which was never mandated).
- Each business domain is divided into a fixed layer stack with strictly forward-only dependencies: Types to Config to Repo to Service to Runtime to UI, and cross-cutting concerns (auth, connectors, telemetry, feature flags) may enter only through a single explicit Providers interface; anything else is disallowed.
- Constraints are enforced mechanically by Codex-generated custom linters and structural tests, which the post calls an early prerequisite rather than a late-stage luxury: constraints are what permit speed without decay or drift.
- A small set of taste invariants is statically enforced: structured logging, naming conventions for schemas and types, file size limits, and platform-specific reliability requirements, among others.
- Because the lints are custom, error messages are written to inject remediation instructions into agent context, so every violation teaches the agent the fix at the moment of failure.
- The leadership model is explicit: enforce boundaries centrally and allow autonomy locally, mirroring a large platform organization; generated code need not match human stylistic preferences as long as it is correct, maintainable, and legible to future agent runs.
- Human taste feeds back continuously through review comments, refactoring PRs, and bug reports captured as documentation updates or tooling, with a promotion rule: when documentation falls short, the rule gets promoted into code.
- The merge philosophy is minimal blocking gates with short-lived PRs and test flakes handled by follow-up runs rather than indefinite blocking, on the grounds that with agent throughput far above human attention, corrections are cheap and waiting is expensive; the post is explicit this would be irresponsible at low throughput.

---

## Invariants over implementations

Documentation alone cannot keep a fully agent-generated codebase coherent. The team therefore constrains the solution space (strict boundaries, predictable structure, validated dependency directions, a limited set of permissible edges) while leaving agents free inside those boundaries. The boundary-parsing example is representative: what matters (validate shapes at the edge) is enforced; the library choice is the agent's.

## The layered domain model

Within each business domain (the post uses App Settings as the example), code may only depend forward through Types, Config, Repo, Service, Runtime, UI. Cross-cutting concerns enter through exactly one door: Providers. The dependency graph is validated by custom linters and structural tests, all themselves Codex-generated. The post's comment that this is architecture usually postponed until hundreds of engineers is pointed: with coding agents it must come early, because constraints substitute for the social coordination that normally prevents drift.

## Taste as executable rules

Taste invariants convert style into checkable properties. Structured logging, schema and type naming conventions, file size limits, and platform reliability requirements are statically enforced, and the custom error messages double as agent instructions: each lint failure carries its own remediation. In a human-first workflow these rules would feel pedantic; encoded once, they apply everywhere at once and become multipliers.

The team is explicit about where constraints stop. Boundaries, correctness, and reproducibility are centrally enforced; expression within boundaries is free. Output that looks unidiomatic to humans passes if it is correct, maintainable, and agent-legible. Taste corrections from reviews, refactors, and user-facing bugs flow back into docs or tooling, and persistent failures get promoted from prose guidance into enforced code.

## Throughput changes merging

Conventional norms (heavy blocking gates, long-lived PRs, blocking indefinitely on flakes) became counterproductive once Codex throughput exceeded human attention. The repository runs minimal blocking merge gates, short-lived PRs, and follow-up runs for flakes. The economic argument is that corrections are cheap and waiting is expensive at this throughput; the safety caveat is that the same policy at low throughput would be irresponsible. Agent-to-agent review (page 1) is what makes the permissive gates defensible: verification effort did not disappear, it moved from humans to agents.

**Covers:** article sections "Enforcing architecture and taste" (boundary parsing, layered domains, Providers, linters, taste invariants, remediation errors, boundaries-vs-autonomy, taste feedback, promote-into-code rule) and "Throughput changes the merge philosophy".
