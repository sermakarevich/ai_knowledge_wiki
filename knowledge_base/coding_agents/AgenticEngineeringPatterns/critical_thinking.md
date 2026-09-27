> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: Agentic Engineering Patterns - Simon Willison's Weblog

## Claims vs. evidence
- Verifiable claim (sole): the guide offers "patterns for getting the best results out of coding agents like Claude Code and OpenAI Codex."
- Evidence available in digest: none — no prompts, transcripts, metrics, code diffs, or before/after examples captured.
- The TOC implies positions (TDD discipline, git hygiene, subagent use, browser-automated QA), but headings are not evidence; they are a scope promise.
- Sponsor teaser ("pressure washing" a codebase; "quality > quantity for security findings") is unattributed and unfalsifiable as captured.
- No counterfactual is offered: no "without this pattern" baseline, no failure log, no cost or latency figure.
- Reasoning-mode and chat-template headings promise internals, but without text they cannot adjudicate when reasoning effort pays off.
- The digest records no dates, versions, or model snapshots — agent behavior drifts, so undated advice decays fast.
- Even authorship-level claims (what "compound engineering loop" means, what the "hoard" contains) cannot be quoted — definitions sit behind the missing introduction.
- Net: claim-to-evidence ratio is unmeasurable from this material — treat every pattern as alleged until the full guide is ingested.

## Genuinely new vs. repackaged
- Framing ("agentic engineering" vs. "vibe coding") is positioned as new discipline, but digest gives no definition to test novelty.
- Most TOC items read as repackaged craft: red/green TDD, git essentials, linear walkthroughs, proofreader/alt-text artifacts.
- Candidate-novel items (inferred from headings only): "compound engineering loop," "hoard + recombine" habits, Explore/parallel/specialist subagent patterns, Showboat note-taking.
- Without body text, impossible to say whether these are genuinely new mechanisms or new names for delegation, caching, and templating.
- Token caching, system prompts, tool-calling loops are listed as background — standard agent-architecture exposition, not a contribution by itself.
- Annotated prompts, word clouds, and interactive explanations hint at a "comprehension" thread distinct from generation — potentially the most transferable idea.
- Appendix artifacts (proofreader, alt text, podcast highlights) suggest a habit of banking reusable prompts — consistent with the "hoard" thesis.
- Prior: Willison's strength is operationalizing obvious-in-hindsight practice — expect synthesis over invention.
- Credit where due: even a well-curated checklist of "which old disciplines matter more under agents" would be useful, if the guide delivers it.

## Weaknesses and blind spots
- Empty-capture problem: this analysis rates the digest, not the guide; any verdict on the guide itself is provisional.
- No cost/latency/token-caching numbers, no failure cases, no evals — headings promise "how agents work" but show no mechanism.
- Missing from TOC as captured: permissions/sandboxing, secret handling, multi-agent coordination hazards, eval harnesses, cost control.
- "Avoiding technical debt" and "AI should produce better code" are aspirations without a review gate described.
- "Inflicting unreviewed code on collaborators" is named as an anti-pattern, but no enforcement (hooks, CI gates, CODEOWNERS) is visible.
- Risk of survivorship framing: patterns from a high-skill solo practitioner may not transfer to teams with weak tests or no review culture.
- Single-vendor skew risk: framing names Claude Code and Codex — portability to other harnesses is unaddressed in the capture.
- Disclosure/colophon sections exist but are empty here — conflicts, sponsorship influence, and tooling versions remain unknown.

## Applicability
- Directly applicable only as a reading list: the TOC is a useful checklist (git + TDD + subagents + browser QA + walkthroughs).
- Not actionable as procedure: no prompt, hook, or workflow in the digest can be copied into practice.
- Best use now: cross-check against existing agent runbooks — anything on the TOC missing locally is a gap to investigate.
- Transferability caveat: solo-blog toolchain (Showboat, Present, GIF/WebAssembly demos) may not map to service-owned data platforms without adaptation.
- **Relevance to my work**
  - AI/ML engineering: TDD-first and "run tests first" headings reinforce gated agent loops; adopt as policy even before reading the guide.
  - Agentic systems: Explore/parallel/specialist subagent headings map to current subagent designs — worth comparing once body text lands.
  - Elisity data platform: browser-automation QA and Showboat-style note-taking could transfer to pipeline/UI verification; hold until concrete mechanism is captured.

## What this changes
- Changes nothing in practice today: no technique in the digest is specified enough to alter a workflow.
- Changes the backlog: prioritizes full-guide ingestion (introduction, principles, subagent, TDD, Showboat sections) as the next step.
- Sharpens the null hypothesis: if the full guide is only "write tests, use git, review diffs," it confirms discipline beats prompting.
- If the "compound loop" and "hoard" sections deliver reusable artifacts, that would upgrade this from checklist to method.
- Until then, default to existing controls: tests-gated loops, git-scoped agent branches, mandatory human review.
- A fair retest after full ingestion: can a junior engineer run one listed pattern end-to-end from the guide alone?

## Verdict
- On current evidence the guide is a promising TOC, not a proven method — rating the capture, not the author.
- Do not cite any pattern from this digest as Willison's recommendation; the body text is missing.
- The TOC's breadth (principles through appendix artifacts) suggests real substance exists upstream — this digest simply did not capture it.
- Cost of being wrong is low if the verdict is watch: revisit cost is one re-ingest; cost of premature adopt is cargo-culted workflow.
- Next action: re-ingest the introduction plus at least the subagent, TDD, and Showboat sections, then re-rate.
- **watch**
