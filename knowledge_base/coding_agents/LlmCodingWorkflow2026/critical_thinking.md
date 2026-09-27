> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: My LLM coding workflow going into 2026 | AddyOsmani.com

## Claims vs. evidence

- Claim: spec-first planning ("waterfall in 15 minutes") makes downstream coding much smoother. Evidence: plausible and consistent with practitioner quotes (Les Orchard), but anecdotal — no controlled comparison, no failure-rate or velocity numbers.
- Claim: small chunks beat monolithic generation ("jumbled mess", "10 devs without talking"). Evidence: strong mechanistic basis (context limits, error compounding) plus repeated practitioner reports; one of the best-supported claims in the piece.
- Claim: CLI and async agents (Claude Code, Codex CLI, Gemini CLI, Jules, Copilot Agent) accelerate mechanical work. Evidence: concrete mechanism descriptions and examples (payment-module refactor → PR), but tool-specific and time-sensitive; Anthropic's "~90% of Claude Code written by Claude Code" is self-reported marketing-adjacent, not independently verified.
- Claim: agents "fly" with a good test suite but hallucinate confidence without one ("sure, all good!" while breaking things). Evidence: rings true and matches broad industry experience, but presented via vignette rather than measurement.
- Claim: rules files (CLAUDE.md/GEMINI.md), custom instructions, and mimicry priming materially improve output style. Evidence: weak-to-moderate — attributed quotes (Jesse Vincent, Ben Congdon), no A/B examples; likely true but magnitude unquantified.
- Claim: AI-on-AI review (second session or different model) catches what one model misses. Evidence: asserted as goal/aspiration ("more AI-on-AI reviews, which have caught things") with a single generic example; promising but under-evidenced.
- Overall: the piece argues from curated practitioner testimony, not data. Direction of each claim is credible; strength of each claim is overstated by omission of counter-cases.
- Claim: "waterfall in 15 minutes" alignment prevents wasted cycles. Evidence: no baseline — no account of spec-iteration time itself becoming the bottleneck on ambiguous or exploratory work.
- Claim: verbatim failure feedback ("tests failed with XYZ, let's debug") reliably steers models. Evidence: consistent with tool behavior (models correct well given concrete errors), but no discussion of loops that never converge or of flaky-test confusion.

## Genuinely new vs. repackaged

- Genuinely new (2025–2026 specific): CLI agents operating in-repo (read files, run tests, multi-step fixes); async cloud agents that clone, work, and open PRs; orchestration of parallel agents (Conductor, 3–4 threads); git-worktree-per-feature sandboxing for agent isolation; Chrome DevTools MCP giving agents runtime eyes (DOM, traces, console, network).
- Repackaged fundamentals: spec-before-code, bite-sized tasks, TDD per chunk, "prompt plan" files (= phased delivery plans), line-by-line review, save-point commits, tidy history for bisect, lint/CI/staging gates, style guides and onboarding analogues. The conclusion admits this: classic discipline matters more, human as "director of the show."
- The real novelty is density and integration — old practices composed into a tight loop (spec → plan → chunk → test → commit → CI → feed failures back verbatim) executed at higher velocity — not any single technique.
- Framing novelty: "AI-augmented, not AI-automated engineering" and the junior-dev / over-confident-pair-programmer mental models are useful repackagings, but they are management metaphors, not technical inventions.

## Weaknesses and blind spots

- No numbers: no velocity, defect, review-time, or cost data; impossible to weigh supervision overhead against generation savings.
- Survivorship bias: sources are enthusiastic practitioners with strong testing cultures; the rush-project "inconsistent mess" anecdote is the lone failure case and is blamed on user indiscipline rather than tool limits.
- Single-thread assumption is under-examined: author prefers one main agent plus reviewer because parallel threads are "mentally taxing," yet offers worktrees plus Conductor for parallelism without resolving the attention bottleneck.
- Security, privacy, and compliance are absent: repo contents fed to cloud agents, agentic file/test execution, and auto-opened PRs carry exfiltration and supply-chain risk, unmentioned.
- Cost and latency ignored: repeated generation, test loops, dual-model review, and background VMs cost tokens, compute, and CI minutes; no guidance on when the loop is uneconomical.
- Large-codebase realities glossed over: context packing, model choice, and stale specs are named in passing but receive no treatment — no retrieval strategy, no spec-drift handling, no monorepo guidance.
- Evaluation gap: "only merge code you understand" is the entire correctness bar; no mutation testing, property tests, flaky-test discipline, or review checklists for AI-specific failure modes (confident hallucinations, duplicated logic, mismatched names).
- Tool churn: recommendations are pinned to a fast-moving roster (Jules, Conductor, CodeRabbit); half-life is months, and no abstraction survives tool death.
- Prompt-injection and untrusted-content risk unaddressed: agents that read diffs, logs, browser DOM, and reviewer comments inherit whatever malicious or misleading text those channels contain.
- No treatment of when *not* to use AI: exploratory spikes, novel architecture, and performance-critical paths where hand-written design outperforms generated boilerplate get no decision rule.

## Applicability

- Transfers best to: greenfield features with clear interfaces, boilerplate-heavy migrations, well-tested services, and teams already running CI/lint/staging with tidy git habits.
- Transfers poorly to: untested legacy code, latency- or cost-sensitive loops, regulated or secret-bearing repos, and teams without review bandwidth — exactly where "Dunning-Kruger on steroids" bites.
- Preconditions before copying: enforced test gate per chunk, small-commit discipline, branch/worktree isolation, and a maintained rules file; without these the workflow degrades into fast mess production.
- **Relevance to my work**
  - AI/ML engineering: adopt the spec → bite-sized plan → per-chunk test gate for pipeline and feature work; require repro/eval scripts as the "test suite" before accepting generated training or data-processing code.
  - Agentic systems: reuse the supervision pattern directly — one main agent plus a different-model reviewer, worktree isolation per experiment, verbatim tool-output feedback loops; cap parallel agents at what one engineer can actually review.
  - Elisity data platform: highest value in mechanical slices (schema migrations, connector boilerplate, test scaffolding) grounded in spec.md/plan.md; gate every agent PR with CI, lint, staging deploy, and a reviewer prompt; never let agents touch credentials, PII paths, or prod configs unattended.

## What this changes

- Process: make spec.md + plan.md mandatory context for agent sessions; implement strictly one plan step at a time with tests run and committed before proceeding.
- Version control: commit per chunk with descriptive messages ("save points"); use worktrees/branches per agent thread; paste diffs and logs into prompts and use bisect-friendly history.
- Configuration: maintain a live CLAUDE.md/GEMINI.md (style, banned patterns, functional-over-OOP, truthfulness rule: ask rather than invent; explanation rule: comment the fix rationale) plus Copilot/Cursor custom instructions.
- Verification: instruct agents to run tests per task and refuse "done" until green; add AI-on-AI review as a second pass on risky diffs; feed CI/linter/reviewer output back verbatim as refactor prompts.
- Craft: schedule unassisted coding and deliberate review-of-AI-output as skill maintenance; operate at design/interface level while the agent does boilerplate.
- What it does not change: accountability stays human ("I remain the accountable engineer"); architecture judgment, scope-splitting, and merge decisions are not delegable.

## Verdict

- The piece is a solid field manual for supervised agent use, honest about human accountability but thin on evidence, costs, security, and legacy-code realities. Its durable core — plan small, verify everything, contain with git, tune with rules, automate the gates — is sound and immediately actionable; its tool-specific layer will age fast.
- For a disciplined team with tests and CI, this is low-risk to pilot and likely net positive on boilerplate and mid-size features. For an undisciplined or untested codebase, adopting the generation half without the verification half is actively harmful.
- **trial**: pilot the full loop (spec → chunk → test → commit → review) on one bounded service with measured review time and defect rate before wider rollout.
