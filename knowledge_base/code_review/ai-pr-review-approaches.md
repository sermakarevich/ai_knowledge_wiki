# Building a State-of-the-Art AI PR Review System

A research synthesis on the most sophisticated approaches to AI-assisted pull request review, with a focus on what to build, what to steal, and where to push past the current frontier. Sources are inline; some arxiv IDs in 2601–2604 (Jan–Apr 2026) and a handful of pre-prints should be cross-checked before citing externally.

---

## TL;DR

1. **The state of the art is multi-agent with verification, not single-shot reviewing.** Anthropic's own Code Review (`/ultrareview`) runs **7 fixed agents + N validation subagents** — and every flagged issue is independently re-validated before posting. The full prompt is open-source at `github.com/anthropics/claude-code/blob/main/plugins/code-review/commands/code-review.md`.
2. **The hardest problem is precision, not recall — and within precision, the nitpick problem dominates.** Greptile's honest baseline: **79% of generated comments were "technically correct but not actionable"** before they shipped feedback filtering. SWRBench: **<10% precision** for top systems. The Microsoft empirical study found **75% of useful human review comments are about evolvability and maintainability**, not the surface-level issues current AI reviewers default to. Most "AI code reviewer" is operating as an advanced linter, not a reviewer.
3. **The strategic review gap is structural, not a prompt bug.** AI reviewers nitpick because (a) training data is dominated by style comments, (b) BLEU/exact-match metrics reward common short phrases over rare insightful ones, (c) LLMs are calibrated confidently on surface issues and uncertainly on architectural ones, (d) sycophancy suppresses pushback on design decisions, and (e) the visible diff is the only context the model has. Prompting alone cannot fix a training-distribution problem — see §1.
4. **The biggest cost lever is prompt caching.** A naive 5-agent fan-out costs ~$2; the same architecture with proper repo-context caching costs ~$0.15. The $15–25 ceiling on `/ultrareview` is for very large or ambiguous PRs with extended thinking and many validation subagents.
5. **The frontier worth pushing past:** persistent per-repo memory of past findings (AgenticSCR), behavior-change as the actual KPI, online RL from accept/reject signals (iCodeReviewer 23%→84% acceptance; BugBot 52%→80% resolution rate via learned rules), execution-grounded review, **constitutional self-critique loops applied to the reviewer's own output** (Cloudflare's coordinator pattern reaches ~1.2 findings/review with 0.6% override rate), and **mandatory orientation passes** before any line-level analysis.

---

## 0. The Anthropic Code Review Blueprint (Reverse-Engineered from Public Source)

This is the most concrete production multi-agent code review system that has been shipped at scale. The architecture is *not* leaked — Anthropic published the entire orchestrator prompt in their `claude-code` repo.

**Source files:**
- Command: `github.com/anthropics/claude-code/blob/main/plugins/code-review/commands/code-review.md`
- Plugin README: `github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md`
- Docs: `code.claude.com/docs/en/code-review`
- Author: Boris Cherny (`boris@anthropic.com`), v1.0.0

**Pipeline:**

```
Step 1 (Haiku):  Pre-flight — skip if PR is draft/closed/trivial/already reviewed
Step 2 (Haiku):  CLAUDE.md discovery — return file paths only, no content
Step 3 (Sonnet): PR summary — read PR, return change summary
Step 4 (parallel):
  ├─ Sonnet #1: CLAUDE.md compliance check (redundant copy A)
  ├─ Sonnet #2: CLAUDE.md compliance check (redundant copy B)
  ├─ Opus   #3: Bug scan (diff only, "no extra context")
  └─ Opus   #4: Bug + security + logic scan
Step 5 (per-issue parallel):
  └─ For each candidate from Step 4: spawn Opus (bugs) or Sonnet (style)
     subagent that re-validates the issue independently
Step 6:          Filter — drop issues that fail Step 5 validation
Step 7:          Terminal summary (always)
Step 8:          Plan inline GitHub comments (only if --comment)
Step 9:          Post via mcp__github_inline_comment__create_inline_comment
```

**What's distinctive:**
- **Two redundant Sonnet agents on the same task** for CLAUDE.md compliance (cheap insurance against single-agent miss).
- **Per-issue validation** instead of a single aggregate critic. Each candidate finding is re-examined in isolation — the agent only sees that one issue and must independently confirm it. Confidence threshold: 80/100.
- **No cross-finding aggregator critic.** No final pass that looks at all findings together — surprising, and a clear extension point.
- **`REVIEW.md` injection.** A repo-root `REVIEW.md` is injected into every agent's system prompt as the highest-priority instruction. This is how teams version-control their review policy without a UI config.
- **Confidence-gated output.** A 0–100 confidence score per finding; <80 is dropped. Severity tags: 🔴 Important, 🟡 Nit, 🟣 Pre-existing.
- **One comment per issue, deduplicated**, with optional collapsible "extended reasoning" section that explains *why it was flagged and how it was verified*.
- **Direct quote on signal-to-noise:** "We only want HIGH SIGNAL issues… If you are not certain an issue is real, do not flag it. False positives erode trust and waste reviewer time."

**Why $15–25:** roughly 3M tokens per run with Opus-heavy validation fan-out (~17–22 agent calls), partially offset by aggressive prompt caching across agents that share the diff and repo context.

---

## §1. The Nitpick Problem and the Strategic Review Gap

This is the dominant failure mode in production and the gap that distinguishes a senior reviewer from a junior one. Treat it as its own engineering problem — not a prompting tweak — or your system will reproduce what every commercial tool reproduces: a flood of type-annotation suggestions and missed architectural issues.

### Why AI reviewers nitpick (root causes, not symptoms)

The behavior is structural. Six causes compound:

1. **Training data distribution.** "Too Noisy To Learn" ([2502.02757](https://arxiv.org/abs/2502.02757)) found **36% of sampled training comments are noise** — vague, non-actionable, unclear — even after prior cleaning. Public PR comments skew heavily toward visible surface issues because those are what any contributor without domain knowledge can write. A model trained to reproduce "consider renaming this" learns *that distribution*, not the rare architectural insight a senior posts once a quarter.

2. **BLEU / exact-match metric bias.** Reference comments are most numerous for style issues, so any metric based on n-gram overlap with references rewards models that generate common short phrases ("consider extracting this") over rare insightful ones (a race condition in concurrent cache invalidation). "Out of the BLEU" ([2208.03133](https://arxiv.org/abs/2208.03133)) shows BLEU cannot reliably distinguish quality differences below 5 points on code — the gradient pushes models toward the mundane.

3. **Calibration asymmetry.** "Mind the Confidence Gap" ([2502.11028](https://arxiv.org/html/2502.11028v1)) and reward-calibration RLHF papers document the asymmetry: LLMs are confident on questions decidable from the diff (variable name quality) and underconfident on questions requiring outside-diff context (architectural fit). Lacking context, the model defaults to what it can see with certainty. SWRBench measures the gap directly: **F1 ~21% on functional logic issues, ~16% on evolutionary/maintainability issues** — categories that need context the diff doesn't supply.

4. **Sycophancy.** [2411.15287](https://arxiv.org/abs/2411.15287) and [2509.16533](https://arxiv.org/abs/2509.16533) document that LLMs reverse positions under user rebuttal even when correct. In review terms: the agent flags a security issue, the author replies "we handle this upstream," the agent retracts. Saying a name is bad is low-stakes; saying "this design will make the payment flow untestable" is high-stakes — and RLHF raters, themselves uncertain, rated confident style comments well and uncertain architectural challenges neutrally. The model learned the safer path.

5. **No architectural context = default to visible diff.** Greptile's published telemetry: before they shipped codebase-graph indexing and feedback filtering, **79% of generated comments were "technically correct but not actionable or valuable"** ([ZenML case study](https://www.zenml.io/llmops-database/improving-ai-code-review-bot-comment-quality-through-vector-embeddings)). The model wasn't broken — it was reasoning correctly from incomplete information.

6. **Reward hacking via comment volume.** When success is measured as "comments per PR" or "coverage," the model is rewarded for verbosity. CR-Bench ([2603.11078](https://arxiv.org/html/2603.11078)) measured this: **agentic reflexion (iterative re-examination) drops SNR from 5.11 to 1.95** because each loop generates more findings without proportional truth. Self-improving agents amplify noise unless paired with strong filters.

### What human reviewers actually do (the baseline AI tools miss)

This is the gap. From [Microsoft Research's empirical study](https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/) of 1.5M comments across five products: **up to 75% of useful human review comments are about evolvability and maintainability, not functionality**. Today's AI tools optimize the inverse.

[Google's eng-practices guide](https://google.github.io/eng-practices/review/reviewer/looking-for.html) puts **design first** in the reviewer checklist:
> *"Do the interactions of various pieces of code in the CL make sense? Does this change belong in your codebase, or in a library? Does it integrate well with the rest of your system?"*

And on over-engineering:
> *"Encourage developers to solve the problem they know needs to be solved now, not the problem that the developer speculates might need to be solved in the future."*

The [Software Engineering at Google](https://abseil.io/resources/swe-book/html/ch09.html) book makes a structural distinction: peer reviewers (correctness/comprehension) ≠ code owners (maintainability/tech debt) ≠ readability reviewers (consistency). The owner asks: *"Will this code be easy or difficult to maintain? Does it add to my technical debt?"*. Most AI tools collapse all three roles into one.

The CRDM cognitive model ([2507.09637](https://arxiv.org/html/2507.09637v1)) maps human review onto recognition-primed decision theory: senior reviewers spend a meaningful portion of effort in an **orientation phase** — establishing context, rationale, scope, author — *before* analytical comments. **27% of questions during review are orientational**; the rest are analytical, and senior reviewers spend more of their analytical budget on *assessing* implementation rather than *understanding* it.

Today's AI reviewers spend ~0% on orientation. They process the diff directly. This is the structural gap.

The benchmark survey ([2602.13377](https://arxiv.org/html/2602.13377v1)) documents the consequence: *"Change Understanding and Analysis has transitioned from a research cornerstone (14 datasets) to a nearly absent standalone topic (1 dataset), as tasks are increasingly consolidated into end-to-end generative processes."* The field has stopped measuring the part that matters.

### The honest production numbers

| System | Headline metric | Source |
|---|---|---|
| Greptile pre-filtering | **79% nits** (not actionable) | [ZenML case study](https://www.zenml.io/llmops-database/improving-ai-code-review-bot-comment-quality-through-vector-embeddings) |
| Greptile post-filtering | 19% → 55% address rate | as above |
| Cursor BugBot | **52% → 80%** resolution rate via learned rules | [BugBot Learning](https://cursor.com/blog/bugbot-learning) |
| Atlassian Comment Ranker | **40-45% Code Resolution Rate**, matching humans, 30% PR cycle reduction | [Atlassian Engineering](https://www.atlassian.com/blog/atlassian-engineering/ml-classifier-improving-quality) |
| Cloudflare AI Code Review | **~1.2 findings/review**, 0.6% override rate | [Cloudflare Eng](https://blog.cloudflare.com/ai-code-review/) |
| BitsAI-CR (ByteDance) | **77% precision** at 12K weekly users | [2501.15134](https://arxiv.org/abs/2501.15134) |
| CodeRabbit GPT-5.1 | **58.7% Important comments**, < half competitor volume | [CodeRabbit blog](https://www.coderabbit.ai/blog/gpt-51-for-code-related-tasks-higher-signal-at-lower-volume) |
| Automated review study | 21.3% "Won't Fix" rate; PR closure 5h52m → **8h20m** | [2412.18531](https://arxiv.org/html/2412.18531v2) |
| Addy Osmani survey | PRs **18% larger** under AI, **incidents/PR up 24%**, change failure +30% | [addyo.substack](https://addyo.substack.com/p/code-review-in-the-age-of-ai) |

These numbers are the lower bound any new system has to beat. The "PR closure took longer with AI" finding is especially important: if your tool wastes more developer attention than it saves, it has negative ROI even at 100% correct findings.

### Suppression techniques, ranked by evidence

#### Tier 1 — Strongest published evidence

**1. Behavioral feedback embedding filter (Greptile pattern).** Generate everything; embed each candidate comment; block any with cosine similarity ≥ threshold to ≥3 historically-downvoted examples; pass any similar to ≥3 upvoted examples. Greptile's 19% → 55% address rate within two weeks is the strongest single result in the literature. Empirical insight: *"most nit comments cluster into a relatively small number of semantic categories"* — embedding clustering is sufficient.

**2. Separately-trained classifier with behavioral ground truth (Atlassian pattern).** Train a smaller model (ModernBERT in their case) on real resolution outcomes (did the author make a code change after the comment?) as the binary label. **40-45% Code Resolution Rate matching the human reviewer baseline.** Crucial distinction: *self-evaluation* (the LLM judging its own comment severity) is near-random; *separately trained* with behavioral labels is effective. Cold-start problem: needs ~10K+ labeled examples.

**3. Severity gating with structured output + second-pass validator (Cloudflare pattern).** XML-tagged severity classification (critical / warning / suggestion); a coordinator agent applies a "reasonableness filter" dropping speculative findings before posting. ~1.2 findings/review across 131K runs is the production exemplar. Requires explicit schema *and* a second-pass agent — a single self-rating prompt isn't enough.

**4. Online learned-rules from feedback (BugBot pattern).** Convert downvotes, rebuttals, and human reviewer corrections into rules. Rules with consistent negative signal are deactivated. **52% → 80% resolution rate** with 44K+ learned rules across 110K repos. This is the strongest existence proof that closed-loop learning solves the nitpick problem at scale.

#### Tier 2 — Moderate evidence

**5. Linter overlap suppression.** Anything a deterministic linter already flags should be removed from the LLM's output before posting. GitHub Copilot's [October 2025 update](https://github.blog/changelog/2025-10-28-new-public-preview-features-in-copilot-code-review-ai-reviews-that-see-the-full-picture/) integrated CodeQL + ESLint specifically for this. Architecturally trivial to implement; high reliability; removes an entire class of redundant comments.

**6. Multi-agent specialization with explicit "do NOT flag" lists (Cloudflare pattern).** Each specialized agent receives a tight scope prompt with explicit anti-list:
> *"Do NOT flag: theoretical risks that require unlikely preconditions; defense-in-depth suggestions when primary defenses are adequate."*

Scope constraint is *architectural*, not prompt-level — a security-only agent cannot generate a naming nit because it doesn't see naming.

**7. Hierarchical review (architecture-first, line-level second).** Run an architecture/design pass first; only fall through to line-level if no blocking design issues. Anchors the second pass in the right frame. Naor's [three-pass methodology](https://posts.managementdeltas.com/p/how-to-review-code-in-three-focused) is the human-side analogue.

**8. Anthropic's HIGH SIGNAL prompt instruction.** From the open-source `/ultrareview` prompt:
> *"We only want HIGH SIGNAL issues. Flag issues where: the code will fail to compile or parse; the code will definitely produce wrong results regardless of inputs; clear, unambiguous CLAUDE.md violations where you can quote the exact rule being broken… If you are not certain an issue is real, do not flag it. False positives erode trust and waste reviewer time."*

This is prompt-level; necessary but not sufficient on its own. Greptile's team found prompting alone insufficient — *"the model finds adjacent nitpick categories to fill the void."*

#### Tier 3 — Promising but less validated

**9. Persona engineering** — but the empirical evidence is mixed. [PromptHub research](https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference) found generic "act as a staff engineer" personas have minimal effect. What works: personas that specify *tradeoffs* ("prefers backward compatibility over performance"). If swapping "staff" for "junior" doesn't change output, the persona added nothing.

**10. Two-temperature ensemble.** Generate at temperature 0.2 and 0.8; keep only comments appearing in both. Theory: random surface comments don't recur at different sampling temperatures; genuine issues do. Plausible, lacks published validation in code review.

**11. Author trust calibration.** Adjust depth based on author track record — fewer style comments for senior contributors, more for newcomers. Mentioned in human review literature ([1807.04485](https://arxiv.org/pdf/1807.04485)) as a property of human reviewers; not yet shipped with documented results in any AI tool.

**12. Few-shot priming with good-vs-noise example pairs.** 3–5 contrast examples in the prompt anchor the desired distribution. Sound theoretical basis (in-context learning); specific code-review evidence absent.

### Encoding human principles as checkable heuristics

The classical software engineering canon is *not* mostly fuzzy aesthetic judgment. Most of it translates directly into checkable heuristics an AI can enforce. The job is to *constrain* the reviewer to checking these specific things, not generating free-form commentary.

| Principle | Source | AI-checkable form |
|---|---|---|
| Sandi Metz Rules | [Ruby Rogues 2013](https://gist.github.com/henrik/4509394) | Methods > 5 lines flagged with question; signatures with > 4 params asked "should this be a config struct?" |
| Deep Modules | [Ousterhout, *A Philosophy of Software Design*](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf) | Public method count > 7 on class with < 200 LOC implementation = shallow module |
| Hyrum's Law | [hyrumslaw.com](https://www.hyrumslaw.com/) | Public APIs leaking undocumented order, error message strings, or implementation-specific constants |
| Make Illegal States Unrepresentable | [Yaron Minsky](https://blog.janestreet.com/effective-ml-revisited/) | `Optional[T]` always required, paired bool params, runtime `assert x is not None` on fields |
| YAGNI / Speculative Generality | [Fowler](https://martinfowler.com/bliki/Yagni.html) | Interfaces with one implementation; type params used in one concrete context |
| Rule of Three | [Refactoring (Fowler)](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)) | New abstraction with < 3 call sites |
| Chesterton's Fence | [Chesterton 1929](https://en.wikipedia.org/wiki/Wikipedia:Chesterton%27s_fence) | Deletions of error handling, retry logic, sleeps, `defensive` code without explicit replacement |
| Least Astonishment | [Wikipedia](https://en.wikipedia.org/wiki/Principle_of_least_astonishment) | `get_X()` with side effects; functions returning different types based on input |
| Tidy First | [Beck 2023](https://henrikwarne.com/2024/01/10/tidy-first/) | PRs mixing structural changes with behavioral changes — flag for decomposition |
| Boring Technology | [McKinley](https://mcfunley.com/choose-boring-technology) | New dependency / novel approach with no clear cost-benefit articulation |
| Postel's Law (modern) | [Wikipedia](https://en.wikipedia.org/wiki/Robustness_principle) | Permissive input handling on *internal* APIs; overly strict validation on *external* boundaries |
| Goodbye, Clean Code | [Abramov 2020](https://overreacted.io/goodbye-clean-code/) | Don't flag duplication where the duplicates are different *concepts* in different domains |

This is what "human-aligned" looks like in practice: not vibes, but a cookbook of pre-encoded principles that an LLM checks one by one.

### Constitutional code review (no published system has this yet)

Anthropic's [Constitutional AI](https://arxiv.org/abs/2212.08073) trains a model to self-critique against a written constitution and revise. No published system applies this directly to code review — but Cloudflare's coordinator-judge pattern is an unannounced production approximation, and it's a clean architectural slot.

A workable **Review Constitution** for an AI reviewer:

**Reviewer values (positive):**
- Post a comment only if the cost of fixing is ≤ the value of the finding (the "cost-of-comment" threshold)
- Prefer asking questions over making assertions when the finding is uncertain or context-dependent
- Respect the author's stated intent before suggesting alternatives
- Flag issues in proportion to their severity; do not treat style and correctness equally
- Acknowledge uncertainty when a finding may be wrong or context-dependent

**Reviewer anti-values (negative):**
- Do not flag *speculative* risks ("this could cause a problem if someone…") — only demonstrated risks
- Do not suggest removing code without first asking why it exists (Chesterton's Fence)
- Do not push for abstraction when there is only one current caller (Semantic Compression / YAGNI)
- Do not change your position when the author pushes back without new factual evidence (anti-sycophancy)
- Do not flag issues in unchanged code that the PR doesn't affect
- Do not produce comments whose resolution would have no observable effect on correctness, performance, or maintainability

The mechanism: Stage 1 generates candidate findings → Stage 2 critiques each against every constitution principle → discard or revise → post. This is the same critique-revise loop CAI uses, applied to the reviewer's own output instead of the model's response.

### Essential vs. accidental complexity — the deepest unsolved problem

Brooks (1986): *"Essential complexity is intrinsic difficulty of the problem domain. Accidental complexity is difficulty arising from implementation choices, tooling, or organizational decisions."* Essential cannot be abstracted away; accidental can.

The diff doesn't tell you which is which. A complex state machine might be essential (regulatory requirement) or accidental (premature abstraction of two cases). LLMs cannot reliably distinguish without context outside the diff, and the [code smell benchmark](https://arxiv.org/html/2504.16027v1) confirms it: GPT-4 and DeepSeek detect speculative generality at the structural level (unused parameters, never-called methods) but cannot detect it at the design level (an architecture supporting three deployment modes when only one will ever be used).

**Markers correlating with essential complexity (do NOT flag for simplification):**
- Code at a system boundary (network, database, external API) — environment introduces the problem
- Documented domain rule, regulatory citation, or RFC referenced in adjacent comments
- Performance constraints or SLAs documented in linked tickets
- Pattern is *consistent across the codebase* — same "strange" pattern in every service handling that domain
- Code has explicit ownership and the owner can articulate "what would we lose by simplifying this"

**Markers correlating with accidental complexity (candidates to flag):**
- Inconsistent patterns for the same conceptual problem (three caching strategies, four error handlers)
- Deep abstraction with a single call site (interface implemented once is indirection, not polymorphism)
- "Framework fighting" — elaborate workarounds to make a tool do what it wasn't designed for
- No clear ownership; no one can articulate why it is the way it is
- Generic / parametrized code where all instantiations are identical

Until a system can verify these signals (consistency check across codebase, pulling linked issues, parsing ownership signals), it should default to *not flagging complexity for removal* — the false-positive cost dwarfs the false-negative cost. This is the single highest-leverage anti-nitpick rule: **do not push for simplification you cannot prove is accidental.**

### What this means for your reference architecture

The standard fan-out + validator architecture is not enough. To do strategic review you need three additional passes:

- **Mandatory orientation pass** — before any diff analysis. Read PR description + linked issue + recent commit history; output a one-sentence statement of stated intent + stated approach + stated scope. Every subsequent comment must reference this. This is the 27% of human review effort that AI tools currently spend 0% on.
- **Spec-grounding pass** — does the implementation address the stated intent? Does it solve the *root* problem or a symptom?
- **Constitutional self-critique filter** — every candidate comment evaluated against the Review Constitution before posting. Any comment that can't survive "explain why this matters strategically" is dropped.

Plus a hard rule that limits the destruction of trust: **the reviewer must not capitulate when the author pushes back without new factual evidence**. Anti-sycophancy is the alignment property that lets the system retain value when the author would prefer it didn't.

---

## Approaches, Sorted from Most to Least Sophisticated

The ranking is on architectural sophistication, not benchmark score. The most sophisticated systems are not always the best — some are fragile, some are infrastructure-heavy, some have negative ROI on small repos. Tradeoffs are noted per tier.

### Tier S — Frontier (Push Past Current Limits)

These are the techniques where the literature stops and the engineering opportunity begins.

#### S1. Persistent per-repo memory of past findings (AgenticSCR pattern)

**Source:** [AgenticSCR (2025)](https://arxiv.org/abs/2601.19138) (verify ID — January 2026 submission)

A structured store of every finding the system has ever produced for a given repo, indexed by (file, function, pattern). On a new PR, the planner queries the store: "have we seen this pattern before? what was the verdict? did the developer accept?" This is qualitatively different from RAG over docs — it is an *org-specific epistemic memory*. AgenticSCR reports +153% over static LLM baselines on context-dependent vulnerabilities.

**To build:** a sqlite/postgres table keyed by (repo, file_path, ast_signature, finding_category) → (verdict, developer_action, severity_calibrated). Updated after every review. Injected into the planner's system prompt with 1-hour cache TTL.

#### S2. Behavior-change as the primary KPI

The Empirical Study of Deployed AI Code Review ([2604.03196](https://arxiv.org/abs/2604.03196)) found that **PRs reviewed only by AI have a 23pp lower merge rate** than human-reviewed PRs, and 60% of reviews have <30% signal-to-noise. BLEU and exact-match metrics measure word overlap; they do not measure whether developers do anything with your comments. Pushing past the field means treating *did this comment result in a code change in the next commit* as the only metric that matters, and training on that signal directly.

iCodeReviewer ([2510.12186](https://arxiv.org/abs/2510.12186)) demonstrated this: fine-tuning on 1.2M real GitHub PR comment pairs with developer-accept-or-not as the label drove production acceptance from **23% (generic LLM) → 84%**. The delta is almost entirely domain adaptation to "what this team cares about."

**To build:** instrument every comment with thumbs-up/down + did-the-author-modify-this-line-in-next-commit signals. Use these as preference pairs for DPO/KTO fine-tuning of the bulk reviewer model, or as reranker training data for filtering.

#### S3. Execution-grounded review

CodeAgent ([2402.01030](https://arxiv.org/abs/2402.01030)) gives the agent a sandbox: when it suspects a bug, it writes a minimal test case, runs it, and reports the failure as evidence. A comment backed by *"I ran this and it failed with X"* is several orders of magnitude more actionable than *"I think this might fail."*

For PR review specifically, the play is: when a bug-finder agent flags something high-severity, route to an **execution agent** with code-execution tools that *constructs the failing test*. Only post if the test fails. Otherwise drop the finding. This converts much of "high precision is hard" into "did the verifier write a passing exploit."

#### S4. Spec-grounded checklist + LLM residual (SGCR)

SGCR ([2512.17540](https://arxiv.org/abs/2512.17540)) encodes team coding standards as deterministic checks (think: linter rules + structured checklists). The LLM only handles judgment calls the rule layer cannot resolve. Production adoption at HiThink Research went **22% → 42%**, attributed to engineers trusting deterministic checks more than open-ended LLM commentary.

This is the right *socio-technical* approach: a system that says "Rule 14 triggered: identifier-naming.kebab-case-required" is auditable; "the model said so" is not. CodeRabbit's hybrid LLM + 40-linter fusion is the commercial expression of the same principle.

#### S5. Online RL from production signals

iCodeReviewer is one half of this. The other half is closing the loop in production: every developer reaction (accepted, modified, dismissed, comment thread) becomes a training datapoint. Run nightly DPO updates on a small adapter; gate on offline eval before promotion. This is what nobody has shipped publicly yet — and it is the path past 84% acceptance toward something developers genuinely prefer to humans for *low-stakes* feedback.

---

### Tier A — Most Sophisticated Productionised Patterns

Architecturally rich; non-trivial infrastructure investment; documented production wins.

#### A1. Planner → fan-out specialists → per-finding validator (Anthropic Code Review pattern)

This is what `/ultrareview` does (see §0). The principles, generalized:

- **Planner is Opus**, decomposes the diff into concerns and writes a plan to external memory before context truncation (mirrors the [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) which "saves its research plan to external memory before context window truncation").
- **Specialists are Sonnet**, scoped by *concern* not *file*. Concern-based decomposition (security / performance / correctness / API design / style) prevents context pollution between concerns. Run 3–5 in parallel.
- **Validators are per-issue and isolated**. Each candidate finding gets its own subagent that *only sees that issue* and must independently confirm it with confidence ≥ threshold.
- **Subagent isolation** is structural, not advisory: separate context windows, read-only tools, summary returns to orchestrator. From [Claude Code best practices](https://code.claude.com/docs/en/best-practices): "Subagents run in separate context windows and report back summaries."

**Token economics:** Anthropic's research-system data — *single agent: ~4× more tokens than chat; multi-agent: ~15× more tokens than chat* — sets the floor. Multi-agent only justifies its cost when the task is too big for a single agent's context budget. For PRs <200 changed lines, single-agent with a rich tool-set wins on cost.

#### A2. Concern-routed multi-agent + critic-in-loop

RevAgent ([2511.00517](https://arxiv.org/abs/2511.00517)) classifies each diff hunk by concern type and routes to a specialist with a domain-tuned prompt; a discriminator agent picks the best output when concerns overlap. **+12.9% BLEU over single-agent on CodeReviewer.**

Magis ([2403.17927](https://arxiv.org/abs/2403.17927)) layers a critic-in-loop on top: the reviewer drafts comments; the critic reviews drafts before they post and can trigger revision. **~3pp of Magis's SWE-bench improvement comes from the critic alone.** Tradeoff: 2–3× round-trip latency; needs a hard timeout to avoid infinite revision cycles.

**Combined pattern:** classifier → router → 3–5 concern specialists (parallel) → critic that reviews each draft comment → post. Anthropic's pipeline lacks the cross-finding critic — that's a clear improvement vector for a custom system.

#### A3. Neuro-symbolic static analysis + LLM fusion

Three pieces:

- **SAST-first triage**: Du et al. ([2601.18844](https://arxiv.org/abs/2601.18844)) eliminate **94–98% of SAST false positives** at $0.001–$0.12 per alarm by running CodeQL/Semgrep first and using GPT-4 only as a triage/explanation layer. The LLM never sees a clean diff — only flagged hunks. Massive token savings.
- **IRIS** ([2405.17238](https://arxiv.org/abs/2405.17238)): the LLM *infers taint specs* (source/sink labels) for novel APIs, then feeds them to CodeQL for whole-repo dataflow. **+35% over CodeQL alone** on CWE-Bench-Java (69 vs 27 vulnerabilities found).
- **MoCQ** ([2504.16057](https://arxiv.org/html/2504.16057v3)): LLM generates Joern DSL vulnerability patterns; symbolic execution validates them iteratively. Found 46 new patterns + 25 unknown CVEs.

**The architecture insight:** symbolic systems are precise but require expert rules; LLMs are flexible but imprecise on reachability. Divide labor — symbolic for paths and reachability, LLM for semantic classification (is this a sanitizer? is this user-controlled?).

#### A4. Code graph DB + LLM query interface

Build a typed property graph at index time (nodes: MODULE, CLASS, FUNCTION, METHOD, FIELD; edges: CONTAINS, INHERITS, CALLS, USES). Agents issue Cypher-like queries against it.

- **CodexGraph** ([2408.03910](https://arxiv.org/abs/2408.03910)): write-then-translate query construction. **27.90% exact match on CrossCodeEval** vs 21.20% for AutoCodeRover.
- **CGM** ([2505.16901](https://arxiv.org/abs/2505.16901)): injects graph structure directly into LLM attention via a specialized adapter. **43% on SWE-bench Lite with Qwen2.5-72B** — first among open weights.
- **Codebase-Memory** ([2603.27277](https://arxiv.org/html/2603.27277)): tree-sitter → SQLite property graph for 66 languages, exposed via 14 typed MCP tools. **10× fewer tokens, 2.1× fewer tool calls** than file-exploration agents at 83% vs 92% answer quality — a small accuracy hit for dramatic cost reduction.

**To apply:** build the graph once per repo push (incrementally on each commit). On PR open, query "which functions call any symbol in this diff?", "which tests reference these functions?". Feed the resulting subgraph (not raw files) to the review LLM. This is what Greptile v3 does behind the scenes.

#### A5. Agentic multi-hop graph traversal (Greptile v3 / SWE-agent ACI pattern)

When the diff's impact set isn't predictable, give the agent a code-search + graph-traversal tool budget and let it explore. [Greptile v3](https://www.greptile.com/blog/greptile-v3-agentic-code-review) reports **82% bug catch rate** on 50 real OSS PRs (vs 54% Copilot, 44% CodeRabbit), with **75% lower inference cost via aggressive caching**, despite using 3× more context tokens.

The discipline that makes this work is the **Agent-Computer Interface (ACI)** from SWE-agent ([2405.15793](https://arxiv.org/abs/2405.15793)): instead of free-form bash, design specific tools — `get_function_body`, `get_callers`, `run_linter`, `get_test_coverage` — with predictable outputs. SWE-agent: **12.5% on SWE-bench vs 1.7% for vanilla GPT-4** — the gap is almost entirely the ACI.

#### A6. Hierarchical repo summarization ("repo brain")

Code-Craft ([2504.08975](https://arxiv.org/html/2504.08975v1)) builds a multi-level semantic summary pyramid at index time: function summaries → module summaries → repo summary, with each level grounded in its children. **Up to 82% relative top-1 retrieval precision improvement** on large complex codebases (libsignal, ingress-nginx).

For PR review, retrieve summaries for changed symbols + 1-hop callers, send summaries (not source) to the reviewer. Drastic token compression with semantic preservation. Re-summarize only changed functions per commit.

---

### Tier B — Solid, Established Patterns

These are the should-have-by-default building blocks. Most sophisticated stacks compose Tier-A patterns on top of these.

#### B1. LSP + tree-sitter context fusion

LSPRAG ([2510.22210](https://arxiv.org/html/2510.22210v1)) queries four LSP providers per token: definitions, all references, file symbols, token sequences. Extracts the smallest enclosing function for each. **+174% line coverage in Golang, +213% in Java** for unit test generation — direct proxy for cross-file semantic understanding.

[Aider's repo-map](https://aider.chat/docs/repomap.html) uses tree-sitter + PageRank-style scoring to select the highest-value symbols within a token budget. [Continue.dev's LSP context](https://deepwiki.com/continuedev/continue/6.6-lsp-context-integration) recursively crawls type definitions.

For each hunk: extract changed identifiers via tree-sitter → query LSP for defs and refs → extract enclosing function for each ref → dedupe and rank by proximity. Surgical, deterministic context with zero hallucination noise.

#### B2. Diff-aware impact analysis with change dependency graphs

Springer ESE 2024 ([Enhanced Code Reviews via PR-Based CIA](https://link.springer.com/article/10.1007/s10664-024-10600-2)) combines call-graph dependency analysis with co-change history (files that change together), bug frequency, author merge rate, PR size into a per-PR risk score using PageRank-weighted impact. DraCo ([2405.19782](https://arxiv.org/abs/2405.19782)) builds repo-specific context graphs via dataflow. **+3.43% EM and +3.27% identifier F1** on repository-level completion.

[Graphite's pragmatic guide](https://graphite.com/guides/ai-code-review-context-full-repo-vs-diff) confirms the rule: a "diff + relevant slices" hybrid (diff plus ranked callers, relevant tests, import chains) covers 80–90% of needed context without full-repo cost.

#### B3. Hybrid retrieval (BM25 + dense) with reranking

Standard production pattern: BM25 for exact symbol matches + dense embeddings for semantic similarity → RRF merge → cross-encoder rerank → top-K to LLM.

- Best code embedding as of late 2025: [voyage-code-3](https://blog.voyageai.com/2024/12/04/voyage-code-3/) — **+13.80%** over OpenAI text-embedding-3-large across 32 datasets, 32K context, int8/binary quantization support.
- Sourcegraph Cody ([their blog](https://sourcegraph.com/blog/how-cody-understands-your-codebase)) actually moved *away* from embeddings to BM25 over their code search index at enterprise scale. The lesson: at scale, exact-match retrieval over symbols beats fuzzy semantic similarity.

#### B4. RAG over historical PR comments — k=1 wins

LAURA ([2512.01356](https://arxiv.org/abs/2512.01356)) and RARe ([2511.05302](https://arxiv.org/abs/2511.05302)) independently established that **k=1 retrieval beats k>1** for past-comments RAG. More examples introduce conflicting signals. Both report **~+18% over base GPT-4** on CodeReviewer.

RARe also showed **same-repo retrieval beats cross-repo** by a large margin. Build per-repo indexes, not a single org-wide one. Index *accepted* historical comments only.

#### B5. Map-reduce on hunks with shared cached context

For PRs too big for a single agent. Map: each git hunk → a Sonnet subagent. Reduce: aggregator combines structured findings. Anthropic's [C compiler post](https://www.anthropic.com/engineering/building-c-compiler) is the canonical published example (~2,000 parallel Claude Code sessions with lock-file synchronization).

The architecture *requires* shared global context as a cached prefix — pass-by-reference via the prompt cache, not pass-by-copy in each message.

#### B6. Voting / ensemble across multiple model runs

Cheapest sophisticated pattern. Run the same security-review prompt 3× on Haiku with `temperature > 0`, take majority vote on severity classification. Route only high-confidence flagged items to a Sonnet/Opus specialist. Exploits Haiku's 1/3 the price of Sonnet for triage.

Anthropic's extended thinking research achieved 84.8% GPQA via "sampling multiple independent thought processes simultaneously and selecting the best via consensus voting." For binary review decisions (is this a bug?) ensembling is more robust than chain-of-thought on a single model.

---

### Tier C — Foundational Building Blocks

You need these regardless of which higher tier you build on.

- **AST-aware chunking** at function boundaries (tree-sitter), not file or fixed-size. Store (function_name, file, signature, body, callers, callees, summary) as the schema.
- **CodeReviewer baseline** ([2203.09095](https://arxiv.org/abs/2203.09095)) — Microsoft's 2022 fine-tuned T5 on 130K real PRs. The standard benchmark anchor.
- **Subagent isolation** — separate context windows for each parallel agent; communicate via summaries only.
- **Long-context fallback** — for repos <5K LoC, just feed everything; skip retrieval. [Lost in the Middle](https://arxiv.org/abs/2307.03172) caveat: place the diff and most-relevant retrievals at the *beginning and end* of the prompt, not the middle.

---

## Cost / Quality Engineering — How to Hit (or Beat) the $15-25 Budget

The naive cost of a 5-agent fan-out on a 500-line PR is ~$2 uncached. The same architecture cached aggressively is ~$0.15. The $15–25 ceiling on `/ultrareview` is for very large PRs with extended thinking and many validators. The engineering opportunity is enormous.

### Caching is the single largest lever

Mechanics from [Anthropic's caching docs](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching):
- Two TTLs: **5-min (1.25× write, 0.1× read)** or **1-hr (2.0× write, 0.1× read)**. Cache reads cost **10% of standard input** — a 90% discount.
- Min thresholds: 4,096 tokens (Opus 4.x / Haiku 4.5), 2,048 (Sonnet 4.6).
- Up to **4 explicit cache breakpoints** per request. Hierarchy: Tools → System → Messages.

**Architecture for review:**
- Tools block: cached, static across all subagents.
- System block: repo architecture summary + coding conventions + prior review summaries — 10K–50K tokens, **1-hr TTL** if reviews batch nightly, 5-min if interactive. This is the prefix all subagents share.
- Messages block: PR diff — not cached; varies per review.

**Cross-agent cache sharing.** Cache is keyed by prefix hash, so 5 parallel Sonnet subagents reading identical Tools+System hit the same cache after the first writes. For a 20K-token repo context across 5 agents: **uncached $0.30, cached $0.024 (12× cheaper)**.

**Pre-warming.** `max_tokens: 0` requests during off-peak write cache entries before reviews begin.

### Model routing

| Layer            | Model       | Role                                    |
|------------------|-------------|-----------------------------------------|
| Triage           | Haiku 4.5   | PR classification, voting ensembles     |
| Specialists      | Sonnet 4.6  | Per-concern parallel review (5 agents)  |
| Planner + Critic | Opus 4.7    | Decomposition + per-finding validation  |

Anthropic's data: *Opus lead + Sonnet subagents outperformed single-agent Opus 4 by 90.2%*. Reserve extended thinking strictly for the planner and critic — for style/naming review, Haiku without thinking dominates Opus with thinking on per-dollar quality.

### Token economics (500-line PR, 5 specialists)

- Input per Sonnet specialist: ~27K (1.75K diff + 17.5K context + 7.5K system+repo summary)
- Output per specialist: ~1.2K (structured JSON findings)
- Aggregator input: ~15K (sum of specialist outputs); output ~3K
- Opus planner+critic: 10K in / 3K out

**Realistic costs:**
- Uncached, 5 Sonnet + Opus critic: **~$0.40**
- Cached after first review of this repo: **~$0.13**
- + extended thinking on Opus critic for ambiguous cases: +$0.20 → **~$0.33**
- Batch API (50% discount, 24-hr SLA): **~$0.17 cached + batched**

The $15–25 ceiling represents 5,000+ line PRs without aggressive caching, or 17–22 validation subagents firing on a high-finding-count PR. With this architecture, expect **$0.50–$3.00** per typical PR, **$5–$10** for very large ones.

### Output-aware decomposition

Output tokens cost 5× input on Sonnet ($15 vs $3 per MTok). A free-form Sonnet agent will produce 10K+ tokens of prose review. Constrain to a structured contract:

```json
{
  "findings": [
    {
      "file": "str",
      "line_range": [int, int],
      "severity": "critical|high|medium|low",
      "category": "security|perf|correctness|style",
      "description": "str (≤100 tokens)",
      "suggestion": "str (≤100 tokens)"
    }
  ],
  "summary": "str (≤50 tokens)"
}
```

Caps each agent at ~3K tokens output regardless of finding count. The C-compiler post said it directly: *"the test harness should not print thousands of useless bytes."*

### Reuse across runs

- **Repo architecture summary** updated weekly via batch job, 5–10K tokens, injected with 1-hr TTL. Cost amortizes across all reviews that week.
- **Prior findings index**: per-file lookup of historical issue density. Routes high-risk files to Opus specialist instead of Sonnet.
- **Last 3 review summaries** (compressed to ~1.5K tokens) injected into planner so it deprioritizes already-flagged patterns.

---

## Evaluation — What to Measure and How

The measurement problem is harder than the implementation problem. The literature has converged on a clear lesson: **BLEU is dead, behavior-change is everything**.

### Tier 1 — offline, rigorous

**SWRBench** ([2509.01494](https://arxiv.org/html/2509.01494v1)) is the most methodologically rigorous benchmark:
- 1,000 manually verified GitHub PRs, 12 popular Python projects.
- **Change-points** as ground truth: a code location where reviewer feedback led to a modification.
- LLM-as-judge as a *matching* task (binary precision/recall), validated at 89–95% human agreement.
- Top-performing system today: **F1 = 19.38%**. Most tools have **<10% precision**. This is the field's most important number.

**CodeReviewBench** ([codereviewbench.com](https://www.codereviewbench.com/)): synthetic-but-realistic regressions across 5 languages, deterministic scoring. Useful as a clean controlled benchmark to layer on top of SWRBench.

**SecVulEval** ([2505.19828](https://arxiv.org/abs/2505.19828)): 25K C/C++ samples, 5,867 unique CVEs, statement-level granularity. Claude 3.7 Sonnet hits 23.83% F1 — calibrate accordingly.

### Tier 2 — controlled bug-finding proxies

- **SWE-bench Pro** ([why OpenAI moved](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)): 1,865 tasks across 41 repos with private set to prevent contamination. Frontier scores still <45%.
- **CWE-Bench-Java**: 120 vetted CVEs, 4 CWE categories. Small, clean, security-focused.

### Tier 3 — production telemetry

- **Accepted-issue rate**: did a subsequent commit address the comment? CodeRabbit's [framework post](https://www.coderabbit.ai/blog/framework-for-evaluating-ai-code-review-tools).
- **Merge rate delta**: PRs reviewed by your system vs control. The headline finding from [2604.03196](https://arxiv.org/abs/2604.03196) — AI-only-reviewed PRs merge 23pp less. *Make sure your system doesn't reproduce this.*
- **Thumbs up/down on each comment** as the cheapest continuous signal — but correct for organizational context (deadline-pressured teams ignore correct comments).

### LLM-as-judge — beware self-preference

[Self-preference bias is real and documented](https://arxiv.org/abs/2410.21819): GPT-4 prefers GPT-4 outputs at statistically significant rates. **Never use your own model family to judge your own reviews.** If you build on Claude, judge with Gemini or GPT-4o. Apply swap-and-average for all pairwise comparisons. Use [Prometheus 2](https://github.com/prometheus-eval/prometheus-eval) (0.897 Pearson correlation with human raters) with a criterion-separated rubric:
1. Issue correctness (is the flagged code actually problematic?)
2. Actionability (does the comment tell the author what to do?)
3. Severity calibration (does the assigned severity match expert opinion?)
4. Scope (focused on the diff, not pre-existing code?)

### What nobody is measuring well

- **Cross-file architectural feedback** — no benchmark tests "this change breaks a contract 12 files away."
- **Long-horizon impact** — does the PR create technical debt? Requires longitudinal RCT design that doesn't exist publicly.
- **Behavior change on *future* PRs by the same author.** The actual outcome metric.

These are open problems and an opportunity if you're willing to instrument your own org.

---

## Reference Architecture (How to Actually Build It)

Synthesizing the above into a production blueprint. The architecture splits into three layers: **index time** (offline, per-repo), **PR open** (per-review), and **continuous learning** (online).

```
                     ┌─────────────────────────────────────┐
                     │ INDEX TIME (per push to main)       │
                     │ ┌──────────────────────────────────┐│
                     │ │ tree-sitter parse → property     ││
                     │ │ graph (CodexGraph schema)        ││
                     │ │   ↓                              ││
                     │ │ LLM hierarchical summarization   ││
                     │ │ (Code-Craft pattern)             ││
                     │ │   ↓                              ││
                     │ │ voyage-code-3 embeddings of      ││
                     │ │ function bodies + BM25 index     ││
                     │ │   ↓                              ││
                     │ │ Per-repo memory: past findings,  ││
                     │ │ accepted comments index, learned ││
                     │ │ rules from feedback (BugBot)     ││
                     │ │   ↓                              ││
                     │ │ Pattern catalog: which idioms    ││
                     │ │ are consistent across this repo  ││
                     │ │ (used for accidental-complexity  ││
                     │ │ detection)                       ││
                     │ └──────────────────────────────────┘│
                     └─────────────────────────────────────┘
                                       │
                                       ▼
       ┌──────────────────────────────────────────────────────────┐
       │ PR OPEN — ORIENTATION FIRST (the 27% humans spend; AI 0%)│
       │                                                          │
       │  0. Read PR description, linked issue, recent commits    │
       │  1. Output ONE-SENTENCE STATEMENT of intent + approach   │
       │     + scope. All subsequent passes must reference this.  │
       │  2. Classify PR: structural / behavioral / mixed (Beck)  │
       │     — flag mixed PRs for decomposition before review     │
       └──────────────────────────────────────────────────────────┘
                                       │
                                       ▼
              ┌────────────────────────────────────────────────┐
              │ CONTEXT GATHERING                              │
              │  3. Haiku triage → cheap/skip filter           │
              │  4. SAST first pass (CodeQL/Semgrep)           │
              │  5. Diff parse → changed symbols extracted     │
              │  6. Graph BFS 2 hops → impact set              │
              │  7. Hybrid retrieval (BM25+dense+rerank)       │
              │  8. k=1 retrieval over accepted comments       │
              │  9. Build cached prefix:                       │
              │     [tools][REVIEW.md][repo_summary][priors]   │
              └────────────────────────────────────────────────┘
                                       │
                                       ▼
       ┌──────────────────────────────────────────────────────────┐
       │ STRATEGIC PASS (Opus) — runs FIRST, can short-circuit    │
       │                                                          │
       │  • Spec-grounding: does implementation match stated      │
       │    intent? Does it solve root or symptom?                │
       │  • Complexity audit (Brooks + Ousterhout): essential     │
       │    or accidental? Check pattern consistency across       │
       │    repo — accidental ⇒ flag, essential ⇒ don't           │
       │  • Pattern conformance: does design fight existing       │
       │    repo idioms?                                          │
       │  • Single highest-value architectural concern (forced    │
       │    to commit to ONE, not a list)                         │
       │                                                          │
       │  If blocking issue: STOP — do not generate line-level    │
       │  findings on code that needs structural rethink.         │
       └──────────────────────────────────────────────────────────┘
                                       │ (no blocking strategic issue)
                                       ▼
              ┌────────────────────────────────────────────────┐
              │ ORCHESTRATION (Opus planner)                   │
              │  Decomposes by concern; plan to memory         │
              └────────────────────────────────────────────────┘
                                       │
              ┌────────────┬───────────┼─────────────┬──────────┐
              ▼            ▼           ▼             ▼          ▼
          Sonnet       Sonnet      Sonnet        Sonnet     Sonnet
        (security)   (correct)   (perf)        (style)    (api/arch)
                                                        with explicit
              ┌──────────────────────────────────────┐   "DO NOT FLAG"
              │ Each agent has scoped "DO NOT flag"  │   anti-list per
              │ list (Cloudflare pattern). Linter-   │   Cloudflare
              │ overlapping findings auto-suppressed │
              └──────────────────────────────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────┐
                       │ PER-FINDING VALIDATOR     │  ← Opus on bugs
                       │ Each candidate, isolated  │     Sonnet on style
                       │ Confidence threshold 80   │
                       └───────────────────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────┐
                       │ EXECUTION-GROUNDED        │  ← Tier S3
                       │ For high-severity bugs:   │     Synthesizes a
                       │ run repro test or drop    │     failing test
                       └───────────────────────────┘
                                       │
                                       ▼
       ┌──────────────────────────────────────────────────────────┐
       │ CONSTITUTIONAL CRITIC (the new mandatory layer)          │
       │                                                          │
       │  For each surviving finding, evaluate against the        │
       │  Review Constitution:                                    │
       │    • Cost-of-fix ≤ value-of-finding?                     │
       │    • References stated intent (orientation pass)?        │
       │    • If suggesting simplification: proven accidental,    │
       │      not essential? Pattern inconsistency check?         │
       │    • Speculative or demonstrated?                        │
       │    • Anti-sycophancy: would I retract this if author     │
       │      said "it's fine" without new evidence?              │
       │  Discard any finding that fails constitution check.      │
       │                                                          │
       │  Then: cross-finding aggregator critic — dedupe,         │
       │  calibrate severity, identify whether COMBINATIONS       │
       │  indicate a deeper issue.                                │
       └──────────────────────────────────────────────────────────┘
                                       │
                                       ▼
       ┌──────────────────────────────────────────────────────────┐
       │ BEHAVIORAL EMBEDDING FILTER (Greptile pattern)           │
       │                                                          │
       │  Embed each surviving comment. Block if cosine ≥ thresh  │
       │  to ≥3 historically-downvoted comments. Pass if similar  │
       │  to ≥3 upvoted ones.                                     │
       └──────────────────────────────────────────────────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────┐
                       │ POST inline GitHub        │
                       │ comments + structured     │
                       │ JSON to telemetry sink.   │
                       │ Severity tags (Anthropic):│
                       │ 🔴 Important / 🟡 Nit /   │
                       │ 🟣 Pre-existing           │
                       └───────────────────────────┘
                                       │
                                       ▼
       ┌──────────────────────────────────────────────────────────┐
       │ CONTINUOUS LEARNING LOOP                                 │
       │                                                          │
       │  • Thumbs ± + did-author-modify-this-line-in-next-commit │
       │  • Convert downvotes/rebuttals → learned rule            │
       │    deactivations (BugBot pattern)                        │
       │  • Update embedding-filter index of upvoted/downvoted    │
       │  • Add new findings to per-repo memory store             │
       │  • Build DPO preference pairs for nightly adapter update │
       └──────────────────────────────────────────────────────────┘
```

**Where this differs from `/ultrareview` and from common multi-agent designs:**

1. **Orientation pass is mandatory and runs first.** No diff analysis until the agent has stated what the PR is trying to accomplish in one sentence. This is the 27% of human review effort no AI tool currently spends.
2. **Strategic pass runs before line-level pass and can short-circuit.** If the design is wrong, don't post nits about how to clean up code that needs rewriting.
3. **SAST-first** — eliminates 90%+ of LLM noise on rule-checkable issues. Anthropic doesn't appear to do this in `/ultrareview`.
4. **Constitutional critic** — a per-finding self-critique loop against a written Review Constitution. No published system has this; Cloudflare's coordinator approximates it.
5. **Cross-finding aggregator critic** — Anthropic only validates per-finding; this catches inconsistency between specialists and combinations that indicate deeper issues.
6. **Behavioral embedding filter** — Greptile-style downvote/upvote similarity gate before posting.
7. **Execution-grounded validation** for high-severity bugs — synthesize a failing test, only post if it actually fails.
8. **Continuous learning loop** with DPO adapter updates — closes the loop on what your team actually accepts. iCodeReviewer's 23%→84% lift is the existence proof.
9. **Anti-sycophancy as a constitutional principle** — explicit instruction to retain position under pushback unless new factual evidence is provided.

---

## Brief Commercial Scan

Eight tools, in order of architectural relevance to a builder:

- **Claude Code `/ultrareview`** — multi-agent + per-finding validation, $15–25/run, full prompt OSS. The blueprint to start from.
- **Greptile** ($30/seat/mo) — agentic graph traversal, 82% bug catch rate. The codebase-graph-indexing exemplar.
- **Cursor BugBot** ($40/user/mo add-on) — 8 parallel passes + validator + voting. Tight editor handoff to Background Agent for fixes.
- **CodeRabbit** ($24/dev/mo) — single-pass LLM + 40 linters/SAST. The hybrid LLM+deterministic exemplar.
- **GitHub Copilot Code Review** (bundled in Copilot, $10–39/mo) — agentic since March 2026, lives in the GitHub UI. Lowest friction.
- **Graphite Agent** ($40/contributor/mo) — review unified with stacked-PR workflow.
- **Sourcegraph Amp** (enterprise) — Code Graph depth for monorepos. Self-hostable.
- **Qodo PR-Agent** (open source, [github.com/qodo-ai/pr-agent](https://github.com/qodo-ai/pr-agent)) — self-hostable, multi-provider via LiteLLM. The cleanest reference implementation to fork.

**Top 5 ideas to steal across them:**
1. **Per-agent self-verification** (Anthropic): each finding must be independently re-derivable.
2. **`REVIEW.md` injection** (Anthropic): version-controlled review policy as highest-priority system prompt.
3. **Codebase graph index built ahead of time** (Greptile): pre-built call+import graph queried at review time.
4. **Hybrid LLM + linter routing** (CodeRabbit): rule-checkable issues → SAST; judgment calls → LLM.
5. **Severity taxonomy with machine-readable check-run output** (Anthropic): downstream CI gates on counts without scraping comments.

---

## Push Past the Frontier — Concrete Bets

Where the literature stops and the engineering opportunity begins. Picking three to ship would put a team ahead of every commercial offering today.

### The strategic-review bets (most differentiating, least solved)

1. **Mandatory orientation pass with intent extraction.** Before any diff analysis, force the agent to read the PR description + linked issue + recent commits and emit a one-sentence statement: *"This change claims to address X by doing Y."* All subsequent comments must reference this. The 27% of human review effort spent on orientation (CRDM model) is the gap; closing it is the highest-leverage strategic move.
2. **Constitutional self-critique loop for the reviewer.** Write a Review Constitution (cost-of-comment threshold, anti-speculation, anti-sycophancy, Chesterton's Fence, YAGNI, "explain why this matters strategically"). Generate candidate findings → Stage-2 LLM critiques each against every principle → discard those that fail. This is Anthropic's CAI applied to the reviewer's *own output*. No published system does this directly.
3. **Anti-sycophancy as a hard constraint.** Explicit instruction: *"Do not change your assessment based on author pushback unless new factual evidence is provided."* Sycophancy ([2509.16533](https://arxiv.org/abs/2509.16533)) is the alignment failure that destroys reviewer value precisely when pushback matters most. Reduce capitulation via prompt + activation steering at inference (DiffMean) + adversarial-framing detection.
4. **Pattern-conformance check via repo idiom catalog.** Build at index time: catalog of which patterns appear consistently across the codebase. At review time, *suppress simplification suggestions that fight the established pattern*. This is the operational form of "is this complexity essential or accidental" — pattern consistency is the strongest signal that complexity is intentional.
5. **Single-finding adversarial mode for design.** Force the strategic agent to commit to *one* most important architectural concern, not a list. The "one concern" constraint forces prioritization. Pair with adversarial framing: one agent argues the design is wrong, another defends, the system posts the debate as the comment.
6. **Heuristic-based principle checks as the foundation, LLM as residual.** Encode the table in §1 (Sandi Metz rules, Hyrum's Law, Make Illegal States Unrepresentable, Chesterton's Fence deletions, etc.) as deterministic checks. LLM only handles judgment calls. SGCR's 22%→42% adoption lift confirms this is mostly about trust, not capability.

### The continuous-learning bets (compound over time)

7. **Closed-loop online learning from production signals.** Combine accept/reject + thumbs ± + did-the-author-modify-this-line in next commit into preference pairs; nightly DPO update on a Sonnet adapter; gate on offline eval before promotion. iCodeReviewer's 23%→84% acceptance lift is the existence proof; BugBot's 52%→80% via learned rules is the production confirmation.
8. **Persistent per-repo epistemic memory.** Every finding and its outcome in a structured store, queried at planner time. *"Claim X has been wrong 4/5 times in this repo — drop confidence below threshold."* AgenticSCR is the academic precedent; no commercial tool ships this end-to-end.
9. **Behavioral embedding filter (Greptile pattern, productized further).** Index every historical comment by embedding + accept/reject. At review time, gate every candidate comment by similarity to past downvotes. Greptile reports 19%→55% address rate from this single mechanism.

### The verification bets (precision wins)

10. **Execution-grounded validation for high-severity findings.** Severity ≥ high → route to an execution agent that synthesizes a failing test → only post if the test fails. Converts much of the precision problem into a verifier problem. CodeAgent ([2402.01030](https://arxiv.org/abs/2402.01030)) shows this works on HumanEval/MBPP; nobody has shipped it for PR review.
11. **Cross-finding aggregator critic.** Anthropic skips this. A single Opus pass over all surviving findings: dedupe, calibrate severity, identify whether *combinations* indicate a deeper issue. Catches inconsistency between specialists.

### The measurement bet (the only KPI that ultimately matters)

12. **Behavior-change as the primary KPI.** Instrument before-vs-after: do PRs from authors receiving your reviews show different patterns 30 days later than a control group? Track per-author code-quality drift over time. The Empirical Study finding that AI-only-reviewed PRs *merge 23pp less* than human-reviewed ones is the warning sign — your system must be measured against developer outcomes, not comment counts.

### The user-experience bet (review-left-shift)

13. **Real-time feedback during writing, not at PR open.** Hook into the IDE; surface findings on save, before push. Economic value is not the comment — it is collapsing the rework cycle. The author still has the design context loaded; the cost of the fix is 10× lower than after PR is open.

---

## Source Index

### Anthropic / production systems
- [Code Review official docs](https://code.claude.com/docs/en/code-review)
- [`code-review.md` orchestrator prompt (open source)](https://github.com/anthropics/claude-code/blob/main/plugins/code-review/commands/code-review.md)
- [Code Review blog post](https://claude.com/blog/code-review)
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Building a C Compiler with Parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Managed Agents Multiagent Sessions](https://platform.claude.com/docs/en/managed-agents/multi-agent)
- [Prompt Caching Docs](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching)
- [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Visible Extended Thinking](https://www.anthropic.com/news/visible-extended-thinking)
- [The "Think" Tool](https://www.anthropic.com/engineering/claude-think-tool)
- [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Claude Code Ultra: Three Explorers + Critic (MindStudio)](https://www.mindstudio.ai/blog/claude-code-ultra-plan-multi-agent-architecture)
- [DEV.to — Anthropic Code Review pricing](https://dev.to/umesh_malik/anthropic-code-review-for-claude-code-multi-agent-pr-reviews-pricing-setup-and-limits-3o35)

### Multi-agent code review papers
- [AgenticSCR](https://arxiv.org/abs/2601.19138) — verify
- [SAST + LLM Hybrid (Du et al.)](https://arxiv.org/abs/2601.18844) — verify
- [RevAgent](https://arxiv.org/abs/2511.00517)
- [iCodeReviewer](https://arxiv.org/abs/2510.12186)
- [SGCR](https://arxiv.org/abs/2512.17540)
- [LAURA](https://arxiv.org/abs/2512.01356)
- [RARe](https://arxiv.org/abs/2511.05302)
- [AutoCodeRover](https://arxiv.org/abs/2404.05427)
- [RepoAgent](https://arxiv.org/abs/2402.16667)
- [SWE-agent](https://arxiv.org/abs/2405.15793)
- [Magis](https://arxiv.org/abs/2403.17927)
- [CodeAgent](https://arxiv.org/abs/2402.01030)
- [Empirical Study of Deployed AI Code Review](https://arxiv.org/abs/2604.03196) — verify
- [CodeReviewer (Microsoft 2022)](https://arxiv.org/abs/2203.09095)

### Context / retrieval
- [RepoCoder](https://arxiv.org/abs/2303.12570)
- [CodePlan](https://arxiv.org/abs/2309.12499)
- [Aider Repo Map](https://aider.chat/docs/repomap.html)
- [Sourcegraph Cody architecture](https://sourcegraph.com/blog/how-cody-understands-your-codebase)
- [voyage-code-3](https://blog.voyageai.com/2024/12/04/voyage-code-3/)
- [Greptile v3 blog](https://www.greptile.com/blog/greptile-v3-agentic-code-review)
- [LSPRAG](https://arxiv.org/html/2510.22210v1)
- [Codebase-Memory](https://arxiv.org/html/2603.27277) — verify
- [Code-Craft](https://arxiv.org/html/2504.08975v1)
- [CodexGraph](https://arxiv.org/abs/2408.03910)
- [Code Graph Model](https://arxiv.org/abs/2505.16901)
- [DraCo](https://arxiv.org/abs/2405.19782)
- [IRIS](https://arxiv.org/abs/2405.17238)
- [MoCQ](https://arxiv.org/html/2504.16057v3)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Graphite full-repo vs diff context](https://graphite.com/guides/ai-code-review-context-full-repo-vs-diff)

### Evaluation
- [SWRBench](https://arxiv.org/html/2509.01494v1)
- [Code Review Benchmarks Survey (99 papers)](https://arxiv.org/html/2602.13377v1) — verify
- [Limits of Automated Eval for Code Review Bots](https://arxiv.org/html/2604.24525) — verify
- [CodeReviewQA](https://arxiv.org/abs/2503.16167)
- [CodeReviewBench](https://www.codereviewbench.com/)
- [SWE-bench Verified](https://www.swebench.com/verified.html)
- [Why OpenAI moved to SWE-bench Pro](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- [SecVulEval](https://arxiv.org/abs/2505.19828)
- [CWE-Bench-Java](https://github.com/iris-sast/cwe-bench-java)
- [PatchEval](https://arxiv.org/pdf/2511.11019)
- [CVE-Bench](https://arxiv.org/abs/2503.17332)
- [Self-Preference Bias in LLM-as-Judge](https://arxiv.org/abs/2410.21819)
- [Quantifying & Mitigating Self-Preference](https://arxiv.org/abs/2604.22891) — verify
- [Positional Bias in LLM-as-Judge](https://arxiv.org/abs/2406.07791)
- [Prometheus 2](https://arxiv.org/abs/2310.08491)
- [Does AI Code Review Lead to Code Changes?](https://arxiv.org/html/2508.18771v1)
- [CodeAnt 200K-PR Benchmark](https://www.codeant.ai/blogs/ai-code-review-benchmark-results-from-200-000-real-pull-requests)
- [Greptile 50-PR Benchmark](https://www.greptile.com/benchmarks)
- [CodeRabbit Martian Benchmark](https://www.coderabbit.ai/blog/coderabbit-tops-martian-code-review-benchmark)
- [CodeRabbit Eval Framework](https://www.coderabbit.ai/blog/framework-for-evaluating-ai-code-review-tools)

### Commercial tools
- [CodeRabbit](https://www.coderabbit.ai/) | [Pricing](https://www.coderabbit.ai/pricing) | [GPT-5.1: higher signal, lower volume](https://www.coderabbit.ai/blog/gpt-51-for-code-related-tasks-higher-signal-at-lower-volume)
- [Greptile](https://www.greptile.com/) | [Pricing](https://www.greptile.com/pricing) | [Graph-based codebase context](https://www.greptile.com/docs/how-greptile-works/graph-based-codebase-context) | [ZenML case study: nitpick reduction](https://www.zenml.io/llmops-database/improving-ai-code-review-bot-comment-quality-through-vector-embeddings)
- [Graphite Agent](https://graphite.com/blog/introducing-graphite-agent-and-pricing) | [Diamond](https://diamond.graphite.dev/) | [Features](https://graphite.com/features/ai-reviews/)
- [Cursor BugBot](https://cursor.com/bugbot) | [Building a Better BugBot](https://cursor.com/blog/building-bugbot) | [BugBot Learning](https://cursor.com/blog/bugbot-learning)
- [GitHub Copilot Code Review (agentic)](https://github.blog/changelog/2026-03-05-copilot-code-review-now-runs-on-an-agentic-architecture/) | [Oct 2025 quality update](https://github.blog/changelog/2025-10-28-new-public-preview-features-in-copilot-code-review-ai-reviews-that-see-the-full-picture/)
- [Sourcegraph Amp](https://sourcegraph.com/amp)
- [Qodo PR-Agent (OSS)](https://github.com/qodo-ai/pr-agent) | [Docs](https://qodo-merge-docs.qodo.ai/)
- [Cloudflare AI Code Review architecture](https://blog.cloudflare.com/ai-code-review/)
- [Atlassian Comment Ranker (ModernBERT classifier)](https://www.atlassian.com/blog/atlassian-engineering/ml-classifier-improving-quality)
- [BitsAI-CR (ByteDance, FSE 2025)](https://arxiv.org/abs/2501.15134)
- [JetBrains Qodana — Ethics of AI Code Review](https://blog.jetbrains.com/qodana/2026/03/ethics-of-ai-code-review/)

### The nitpick problem & strategic review (added in §1)

#### Why AI nitpicks
- [Too Noisy To Learn (arXiv:2502.02757)](https://arxiv.org/abs/2502.02757) — 36% of training comments are noise
- [Out of the BLEU (arXiv:2208.03133)](https://arxiv.org/abs/2208.03133) — BLEU is broken for code
- [Mind the Confidence Gap (arXiv:2502.11028)](https://arxiv.org/html/2502.11028v1) — calibration asymmetry
- [Sycophancy in LLMs (arXiv:2411.15287)](https://arxiv.org/abs/2411.15287)
- [Sycophancy Under User Rebuttal (arXiv:2509.16533)](https://arxiv.org/abs/2509.16533)
- [Causal Separation of Sycophancy (arXiv:2509.21305)](https://arxiv.org/html/2509.21305v1)
- [Taming Overconfidence in LLMs (OpenReview)](https://openreview.net/forum?id=l0tg0jzsdL)
- [CR-Bench (arXiv:2603.11078)](https://arxiv.org/html/2603.11078) — reflexion drops SNR from 5.11 to 1.95
- [Beyond Strict Rules: LLMs for Code Smell Detection (arXiv:2504.16027)](https://arxiv.org/html/2504.16027v1)
- [Drowning in AI Code Review Noise — Jet Xu](https://dev.to/jet_xu/drowning-in-ai-code-review-noise-a-framework-to-measure-signal-vs-noise-304e)
- [HN: AI code review bubble](https://news.ycombinator.com/item?id=46766961) | [HN: 70% of AI PR comments useless](https://news.ycombinator.com/item?id=45772215) | [HN: Greptile nitpick problem](https://news.ycombinator.com/item?id=42451968)

#### What human reviewers actually do
- [Google eng-practices: Looking For](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Software Engineering at Google — Code Review chapter](https://abseil.io/resources/swe-book/html/ch09.html)
- [Microsoft: Characteristics of Useful Code Reviews (Bosu et al.)](https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/) — 75% of useful comments are evolvability/maintainability
- [Code Review as Decision-Making (arXiv:2507.09637)](https://arxiv.org/html/2507.09637v1) — CRDM cognitive model, 27% orientation
- [Predicting Usefulness of Code Review Comments (arXiv:1807.04485)](https://arxiv.org/pdf/1807.04485)
- [What Types of Code Review Comments Get Resolved? (arXiv:2510.05450)](https://arxiv.org/abs/2510.05450)
- [Hold On! Is My Feedback Useful? (arXiv:2501.06738)](https://arxiv.org/abs/2501.06738)
- [Naor: Three focused review passes](https://posts.managementdeltas.com/p/how-to-review-code-in-three-focused)
- [Automated Code Review In Practice (arXiv:2412.18531)](https://arxiv.org/html/2412.18531v2) — PR closure 5h52m → 8h20m
- [Rethinking Code Review Workflows with LLM Assistance (arXiv:2505.16339)](https://arxiv.org/html/2505.16339v1)
- [Grounded AI for Code Review (arXiv:2510.10290)](https://arxiv.org/abs/2510.10290)
- [AI-powered Code Review: Early Results (arXiv:2404.18496)](https://arxiv.org/html/2404.18496v2)
- [Refute-or-Promote Adversarial Multi-Agent Review (arXiv:2604.19049)](https://arxiv.org/html/2604.19049)

#### Classical engineering principles
- [Brooks: No Silver Bullet (1986)](https://worrydream.com/refs/Brooks_1986_-_No_Silver_Bullet.pdf) — essential vs accidental
- [Ousterhout: A Philosophy of Software Design (extract)](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf)
- [Pragmatic Engineer review of A Philosophy of Software Design](https://blog.pragmaticengineer.com/a-philosophy-of-software-design-review/)
- [janmeppe summary of A Philosophy of Software Design](https://www.janmeppe.com/blog/a-philosophy-of-software-design-john-ousterhout/)
- [Beck: Tidy First? (Henrik Warne summary)](https://henrikwarne.com/2024/01/10/tidy-first/) | [SE-Radio interview](https://se-radio.net/2024/05/se-radio-615-kent-beck-on-tidy-first/)
- [Sandi Metz Rules (Ruby Rogues 2013)](https://gist.github.com/henrik/4509394) | [Thoughtbot post](https://thoughtbot.com/blog/sandi-metz-rules-for-developers)
- [Casey Muratori: Semantic Compression](https://caseymuratori.com/blog_0015)
- [Hyrum's Law](https://www.hyrumslaw.com/) | [DZone explanation](https://dzone.com/articles/hyrums-law-what-it-means-for-api-design-and-manage)
- [Postel's Law / Robustness Principle](https://en.wikipedia.org/wiki/Robustness_principle)
- [Chesterton's Fence (symflower)](https://symflower.com/en/company/blog/2022/programming-principle-chestertons-fence/)
- [Principle of Least Astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment)
- [Make Illegal States Unrepresentable (Yaron Minsky)](https://blog.janestreet.com/effective-ml-revisited/) | [functional-architecture.org](https://functional-architecture.org/make_illegal_states_unrepresentable/)
- [Fowler: YAGNI](https://martinfowler.com/bliki/Yagni.html)
- [Rule of Three](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming))
- [McKinley: Choose Boring Technology](https://mcfunley.com/choose-boring-technology)
- [Abramov: Goodbye, Clean Code](https://overreacted.io/goodbye-clean-code/) | [Deconstruct 2019: The WET Codebase](https://www.deconstructconf.com/2019/dan-abramov-the-wet-codebase)
- [Ian Duncan: When Is Complexity Accidental?](https://www.iankduncan.com/engineering/2025-05-26-when-is-complexity-accidental/)
- [Fowler: Conversation about LLM Abstractions](https://martinfowler.com/articles/convo-llm-abstractions.html)

#### Constitutional AI for review + practitioner perspectives
- [Constitutional AI (arXiv:2212.08073)](https://arxiv.org/abs/2212.08073)
- [Collective Constitutional AI — Anthropic](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input)
- [Addy Osmani: Code Review in the Age of AI](https://addyo.substack.com/p/code-review-in-the-age-of-ai) — 18% larger PRs, +24% incidents/PR
- [Charity Majors blog](https://charity.wtf/) | [2025 was for AI…](https://charitydotwtf.substack.com/p/2025-was-for-ai-what-2010-was-for)
- [PromptHub: Persona prompting empirical results](https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference)
- [Crashoverride: Prompting LLMs for security review](https://crashoverride.com/blog/prompting-llm-security-reviews)




Books — Top 12 for PR Review Encoding

Tier 1 — Highest yield (concrete, directly encodable rules)

1. Refactoring (Martin Fowler, 1999 / 2nd ed 2018) — https://refactoring.com/
The code-smell catalog. Use this first. Each smell has structural signals an LLM (or AST analyzer) can check. Long Method, Large Class, Long Parameter List, Feature Envy, Data Clumps, Primitive Obsession, Switch Statements, Shotgun Surgery, Divergent Change, Refused Bequest. Maps 1:1 to PR review heuristics.

2. A Philosophy of Software Design (John Ousterhout, 2018)
The single best modern book on complexity. Definition of complexity ("anything that makes the system hard to understand and modify"), three symptoms (change amplification, cognitive load, unknown unknowns), Deep Modules concept. Also: tactical vs. strategic programming, comments belong in design, define errors out of existence. Stanford CS190 lectures on YouTube reproduce most of it.

3. The Pragmatic Programmer (Hunt & Thomas, 1999 / 20th anniversary ed 2019)
~100 actionable tips. DRY, orthogonality, tracer bullets, broken windows theory, "good enough software," "don't program by coincidence." Many tips encode directly as review prompts: "Does this code know more than it needs to?", "Are these things changing for the same reason?"

4. Effective Java (Joshua Bloch, 3rd ed 2017)
90 items, each phrased as an actionable rule. Prefer composition over inheritance, Use enums instead of int constants, Favor immutability, Minimize mutability, Beware the performance of string concatenation. The structure makes this the most mechanically encodable book in the list — even for non-Java codebases the principles transfer 80% (immutability, defensive copies, accessor design).

5. Code Complete 2 (Steve McConnell, 2004)
900+ pages, encyclopedic. Variable naming, routine cohesion (functional vs. communicational vs. temporal), defensive programming, layout/style. Older but holds up. Use as a checklist source rather than read cover-to-cover.

6. Working Effectively with Legacy Code (Michael Feathers, 2004)
The "seam" concept (a place where you can alter behavior without editing in place) is the most useful single idea for reviewing legacy-touching PRs. Characterization tests pattern. Encodable rule: "if this PR modifies code without tests, did it add a characterization test before changing behavior?"

Tier 2 — Strategic/architectural (harder to fully automate, valuable as constitution principles)

7. Tidy First? (Kent Beck, 2023)
Short and crisp. The single rule worth shipping: PRs should be either structural changes (rename, extract, move — reversible, behavior-preserving) or behavioral changes — never both in the same commit. Mixed PRs are flagged for decomposition. The economic model in part 3 is also gold.

8. Designing Data-Intensive Applications (Martin Kleppmann, 2017)
The modern distributed-systems canon. Replication, partitioning, transactions, consistency, consensus. Hard to encode automatically but essential for reviewing any PR touching storage, queues, or distributed state. The principles section ("reliability, scalability, maintainability") generates good orientation-pass questions.

9. Domain-Driven Design (Eric Evans, 2003) — also: DDD Distilled (Vaughn Vernon, 2016) for the short version
Bounded contexts, ubiquitous language, aggregates, anti-corruption layers. The strategic-design half (bounded contexts, context maps) is more encodable than the tactical patterns. Constitution principle: "Does this PR cross a bounded context boundary without an explicit translation layer?"

10. Release It! (Michael Nygard, 2018, 2nd ed)
Stability patterns (circuit breaker, bulkhead, timeout, fail fast) and antipatterns (integration points, chain reactions, cascading failures, blocked threads, attacks of self-denial). Production-aware review checklist. Encodable: "Does this synchronous external call have a timeout? Circuit breaker? Bulkhead?"

Tier 3 — Influential but use with caveats

11. Clean Code (Robert Martin, 2008)
Hugely influential, equally controversial. Many of its rules are mechanically encodable (function size, naming, single responsibility) — but https://overreacted.io/goodbye-clean-code/ and others have correctly criticized the abstraction-everywhere bias. Use the local rules (function size, parameter count, naming clarity) and skip the abstraction prescriptions. Pair with Abramov's essay.

12. Patterns of Enterprise Application Architecture (Fowler, 2002)
The vocabulary every web/backend engineer uses: Repository, Unit of Work, Data Mapper, Active Record, Identity Map, Service Layer. Less about review checks, more about giving the agent the vocabulary to describe what it sees.

---
Articles & Essays — The Required Reading

These are short, free, and encode disproportionate value.

1. https://worrydream.com/refs/Brooks_1986_-_No_Silver_Bullet.pdf — Essential vs. accidental complexity. Already in your report.
2. http://curtclifton.net/papers/MoseleyMarks06a.pdf — Best essay on complexity ever written. Distinguishes essential complexity, essential state, and accidental complexity/state. Required reading.
3. http://www.laputan.org/mud/ — Why systems devolve into the same shape. The "default architecture" most code ends up in.
4. https://mcfunley.com/choose-boring-technology — Innovation tokens, complexity budgets. Encodable: "Does this PR introduce a new dependency? Justify the cost of carry."
5. https://www.dreamsongs.com/RiseOfWorseIsBetter.html — Simplicity-of-implementation vs. simplicity-of-interface tradeoff.
6. https://12factor.net/ — 12 specific, checkable rules for cloud-native apps. Most encodable essay in this list.
7. https://overreacted.io/goodbye-clean-code/ — Counter-balance to Clean Code's abstraction bias. "Don't flag duplication where the duplicates are different concepts in different domains."
8. https://www.cs.cmu.edu/~rdriley/487/papers/Thompson_1984_ReflectionsonTrustingTrust.pdf — Security culture. Required for any reviewer touching auth/build chains.
9. https://abseil.io/resources/swe-book — Free online. The Code Review chapter is exactly the human baseline I quoted in §1.
10. https://www.hyrumslaw.com/ — The observable-behavior-becomes-contract law. One paragraph; encodable directly.
11. https://pages.cs.wisc.edu/~remzi/Naur.pdf — Why code without context is dangerous. Foundation for the orientation-pass argument.
12. https://caseymuratori.com/blog_0015 — Best argument against premature abstraction. Already in your report.

---
How to actually use these in PR review

Three honest observations after extracting from these for the report:

1. Most books restate the same ~30 principles in different vocabulary. Your AI reviewer doesn't need 12 books worth of rules — it needs ~30 principles each instantiated as a checkable heuristic. Refactoring + Ousterhout + Effective Java + Tidy First + Twelve-Factor cover ~80% of the encodable surface.
2. Books are not rule files. They argue with stories. The work is extracting rules. For Refactoring, https://refactoring.guru/refactoring/smells and Fowler's online catalog already do this. For Effective Java, https://github.com/HugoMatilla/Effective-JAVA-Summary exist on GitHub. For others, you'll do it yourself or have an LLM extract on first read.
3. Pair every prescriptive book with its critique. Clean Code with Goodbye Clean Code. Design Patterns with "design patterns are missing language features." DDD with the YAGNI essay. Without the counterweight, your reviewer will become the dogmatic junior engineer who flags everything.

---

## §2. Encoded Principles Reference — Concrete Rules Extracted from the Canon

The §1 table covered ~12 marquee principles. This section is the comprehensive extraction: every checkable rule from the Tier-1 books and the required-reading essays, in the format the reviewer's constitution and per-finding validator can consume directly.

Format throughout: **Rule** = the principle. **Detection signal** = what the AI (or AST analyzer) actually checks. **Guardrail** = when *not* to fire — the false-positive condition that turns AI reviewers into nitpickers.

Use this as a starting rule library — every rule here is contested by at least one practitioner; calibrate to your codebase by deleting half of them rather than adding more.

### 2.1 Refactoring — Fowler's Code Smell Catalog

[refactoring.guru/refactoring/smells](https://refactoring.guru/refactoring/smells) is the canonical online reference; this is the AI-encoding form.

| Smell | Detection signal | Guardrail |
|---|---|---|
| Long Method | Function > 30 lines OR > 5 levels of nesting | Skip if the body is a flat sequence of named domain steps with no branches |
| Large Class | Class with > 7 public methods AND > 300 LOC | Skip aggregate roots, controllers, generated code |
| Long Parameter List | > 4 positional parameters | Skip if all parameters are primitives of the same conceptual type (6 floats forming a transform) |
| Feature Envy | Method on class A calls > 3 methods on class B and 0 on self | Skip Builders, Visitors, intentional inversion-of-control |
| Data Clumps | Same 3+ params/fields appear together in 3+ places | Skip if grouping has no natural conceptual name |
| Primitive Obsession | Domain concept (`UserId`, `Money`, `Email`) passed as `str` / `int` | Skip in test fixtures and at I/O serialization boundaries |
| Switch Statements | Type-discriminated switch repeated in > 1 location | Skip if cases are over a closed enum that won't grow (compiler-checked exhaustiveness wins over polymorphism) |
| Shotgun Surgery | Single conceptual change touches > 5 files | Skip schema migrations, renames, dependency bumps |
| Divergent Change | One class modified for > 2 unrelated reasons in last N PRs | Skip if class is a deliberate facade |
| Refused Bequest | Subclass overrides parent method to throw / no-op | Skip Adapter / NullObject patterns |
| Speculative Generality | Interface, abstract class, or generic type with one implementation | Skip if implementation is the test double |
| Lazy Class | Class with < 3 lines of behavior beyond field access | Skip value objects and tagged-union variants |
| Dead Code | Unreferenced symbol after the diff | Skip public exports of a library |
| Comments | Comment explains *what* the next line does | Keep comments explaining *why* (non-obvious constraint) or *what not to do* |
| Duplicate Code | Same expression / 5-line block in > 1 location | Skip when duplicates are different *concepts* in different bounded contexts (Goodbye Clean Code) |
| Temporary Field | Field set only in one method's branch | Skip caches with documented invalidation |
| Message Chains | `a.getB().getC().getD().method()` | Skip fluent builders |
| Middle Man | Class delegates > 50% of methods to one collaborator | Skip pass-through Repository / port adapter when the collaborator is replaceable |
| Inappropriate Intimacy | Class A reads private state of class B (reflection, friend, `_` access) | Skip co-evolved type pairs in same module |
| Alternative Classes with Different Interfaces | Two classes with similar methods but different names | Skip when classes belong to different bounded contexts |
| Incomplete Library Class | Wrapper class adds 1-2 methods to a third-party type | Skip if wrapper hides a security policy |
| Comments-as-Bandaid | Comment apologizes for unclear code (`hack`, `TODO`, `for now`) | Treat as backlog item, not a blocker |

### 2.2 A Philosophy of Software Design — Ousterhout

| Rule | Detection signal | Guardrail |
|---|---|---|
| Modules should be deep | Public surface (method count) ≤ 1/3 of implementation LOC | Skip facades over external libraries |
| Eliminate change amplification | Logical change requires edits in > 3 files | Skip when files form a single bounded context that travels together |
| Reduce cognitive load | New reader needs > 5 concepts to understand a function | Skip pure utilities at the bottom of the dependency stack |
| Eliminate unknown unknowns | Behavior depends on undocumented invariant of caller | Surface as a question, not a blocker |
| Strategic > tactical programming | Quick fix that adds a special case where a general fix exists nearby | Skip true emergencies (incident hotfix); flag for follow-up |
| Define errors out of existence | New `try/except` that catches and returns sentinel | Suggest making the precondition impossible instead |
| Comments belong to the design phase | Comment exists *only* because the code is unclear | Keep comments documenting non-obvious *why* |
| General-purpose modules are deeper | New module is parametrized for one caller's needs | Same as Speculative Generality |
| Different layer = different abstraction | Adjacent layers using identical vocabulary | Likely a leaky abstraction; ask if the layer earns its keep |
| Pull complexity downward | API forces every caller to handle the same edge case | Move the handling into the callee |
| Information leakage | Two unrelated modules know the same fact (file format, protocol detail) | Centralize the knowledge |

### 2.3 Effective Java — Bloch (top-encodable subset of the 90 items)

Full list: [github.com/HugoMatilla/Effective-JAVA-Summary](https://github.com/HugoMatilla/Effective-JAVA-Summary). Most rules transfer to other languages.

| Rule | Detection signal | Guardrail |
|---|---|---|
| Prefer composition over inheritance | New `class X extends Y` where Y is not abstract or designed for inheritance | Skip framework-mandated extension points |
| Favor immutability | New mutable field where final/readonly would suffice | Skip hot paths with measured allocation cost |
| Minimize mutability | Public setter on field with < 2 mutation sites | Skip framework-required JavaBean / ORM entities |
| Use builders for > 4 constructor params | Constructor with > 4 args | Skip when params are all required and same type makes builder noise |
| Make defensive copies | Constructor stores reference to mutable input without copying | Skip when ownership transfer is documented |
| Prefer interfaces to abstract classes | New abstract class where interface + default methods works | Skip when state must be shared |
| Use enums instead of int constants | New `int` constants (`STATUS_OPEN = 1`) used as discriminators | Skip protocol fields where the integer is the wire value |
| Eliminate obsolete object references | Field holding reference past its useful life (unbounded cache, listener without removal) | Skip when GC root behavior is intentional and documented |
| Avoid finalizers / cleaners | New `__del__` / `finalize` for resource cleanup | Use context managers / try-with-resources instead |
| Prefer try-with-resources | Manual `close()` in `finally` | Suggest the language's resource block |
| Always override `equals` and `hashCode` together | Override of one without the other | Hard rule |
| Always override `toString` / `__repr__` | Domain class without one | Skip dataclasses where the default is informative |
| Refer to objects by their interfaces | Variable typed as concrete class where interface exists | Skip when calling a method only the concrete class has |
| Use varargs judiciously | New variadic API where a list parameter is clearer | Skip when the 0/1-arg case is the dominant call pattern |
| Return empty collections, not null | Method returning `null` for "no results" | Skip when null carries information distinct from empty |
| Optionals only as return values | `Optional` / `Maybe` stored as a field | Suggest restructuring data |
| Document threading guarantees | Public method touches mutable state with no `@ThreadSafe` / docstring | Hard requirement at module API boundary |
| Prefer executors / structured concurrency | Raw thread creation | Skip in low-level infrastructure code |
| Beware string concatenation in loops | `+=` on string in a hot loop | Skip when N is bounded small |
| Strive for failure atomicity | Method that mutates partially on exception | Document the partial-failure contract if atomicity isn't possible |

### 2.4 The Pragmatic Programmer — Hunt & Thomas

| Tip | Detection signal | Guardrail |
|---|---|---|
| DRY | Same *knowledge* expressed in > 1 place (config, code, schema) | Skip when duplication is *coincidental* — different concepts that look alike |
| Orthogonality | New module reads/writes state of > 2 other modules | Skip orchestration / saga code by design |
| Reversibility | Decision baked into > 5 places without an abstraction layer | Cost-of-change vs. cost-of-abstraction tradeoff |
| Tracer bullets | New feature lacks an end-to-end smoke path | Skip pure refactor PRs |
| Don't program by coincidence | New code relies on undocumented behavior of dependency | Add the test that pins the behavior |
| Fix broken windows | PR adds TODO/FIXME without ticket reference | Tag, don't block |
| Good-enough software | PR over-engineers a known-throwaway path | Confirm "throwaway" status with author before flagging |
| Make it easy to reuse | New utility takes 4+ params from a single caller | Inline the utility (Semantic Compression) |
| Configure, don't integrate | Magic constants embedded in business logic | Pull to config / feature flag |
| Crash early | Code swallows error and returns sentinel | Promote to raise unless the caller documents handling |
| Use assertions to prevent the impossible | New `if x is None` for a case the type system says can't happen | Replace with assertion or remove |
| Don't outrun your headlights | PR makes assumption about a future requirement | Flag as YAGNI |
| Refactor early | PR adds duplicated structure rather than extracting | Same as Rule of Three |
| Test or your users will | New code path with no test | Pair with characterization-test rule for legacy code |

### 2.5 Code Complete 2 — McConnell

| Rule | Detection signal | Guardrail |
|---|---|---|
| Routine cohesion | Function does > 1 of: validate, transform, persist, format | Skip pipeline stages |
| Variables live as briefly as possible | Local declared > 10 lines before first use | Skip top-of-function declaration in languages without block scope |
| Names describe what, not how | `processData`, `handleStuff`, `manager` | Suggest a domain verb |
| Avoid magic numbers | Numeric literal > 1 in non-test code | Skip 0/1, common HTTP codes (200/404), well-known constants |
| Pseudocode programming | Function with deeply nested control flow without comments at branch points | Suggest extracting named functions per branch |
| Defensive programming at boundaries | New input from external source without validation | Skip internal-only helpers |
| Boolean parameters are usually a smell | Function takes `bool` flag changing behavior | Suggest two functions or a tagged enum |
| Consistent indentation/layout | PR uses different style from the file's existing code | Auto-format, don't comment |

### 2.6 Working Effectively with Legacy Code — Feathers

| Rule | Detection signal | Guardrail |
|---|---|---|
| Find a seam before changing behavior | PR modifies a function with no tests | Require characterization test in same PR or follow-up |
| Characterization tests | New behavior change to legacy code without locking existing behavior first | Skip if legacy code is being deleted |
| Sprout method | Adding new behavior inside an existing complex function | Suggest extracting to a new method called from the existing one |
| Sprout class | New responsibility added to a class with > 5 public methods | Suggest a new class |
| Wrap method | New cross-cutting concern (logging, retry) added inline in N call sites | Suggest decorator / wrapper |
| Extract interface for testability | Untestable code coupled to concrete external dependency | Suggest interface + injection |

### 2.7 Tidy First — Beck

| Rule | Detection signal | Guardrail |
|---|---|---|
| Separate structural and behavioral changes | PR contains both rename/extract/move AND new behavior | Block; ask for decomposition into two PRs |
| Tidy first when it makes the next change cheaper | Behavioral change made without first tidying obviously-related mess | Suggest, don't block |
| Don't over-tidy | PR-level reformat of files unrelated to the behavioral change | Block; ask to revert the unrelated tidy |
| Reversibility favors tidies | Tidy is irreversible (renames public API, deletes config) | Treat as behavioral change |

### 2.8 Designing Data-Intensive Applications — Kleppmann

These are orientation-pass questions more than line-level checks; the validator escalates to the author when uncertain.

| Concern | Detection signal | Guardrail |
|---|---|---|
| Replication safety | New write path to a replicated store | Ask: which consistency level? |
| Partitioning | New query that doesn't include partition key | Ask: hot partition risk? |
| Transaction boundaries | Multi-step state change without explicit transaction / saga | Flag, ask for rollback semantics |
| Idempotency | New API that mutates state and is retried by callers | Ask for idempotency key strategy |
| Backpressure | New unbounded queue / channel | Flag |
| Schema evolution | Migration without backwards-compatible step | Block; require expand-contract |
| Time / clocks | Code compares wall-clock timestamps from two services | Suggest logical clock or single source of truth |
| At-least-once vs. exactly-once | New consumer assumes at-most-once delivery from an at-least-once broker | Block |
| Read-your-writes | UI reads from a follower right after writing to leader | Flag, suggest read-from-primary or sticky session |

### 2.9 Domain-Driven Design — Evans

| Rule | Detection signal | Guardrail |
|---|---|---|
| Bounded context boundary | New direct call from module A to internals of module B in different domain | Suggest anti-corruption layer |
| Ubiquitous language | New name in code differs from the term used in linked spec / ticket | Comment; don't block |
| Aggregate consistency | Cross-aggregate write in single transaction | Use eventual consistency; flag |
| Anti-corruption layer | New translation logic mixed with business logic | Extract translation to named ACL module |
| Domain over data | New entity defined as bag-of-fields without behavior | Ask if invariants belong on the type |
| Repositories at aggregate boundary | Repository exposes child entities directly | Re-route through aggregate root |

### 2.10 Release It! — Nygard

| Pattern | Detection signal | Guardrail |
|---|---|---|
| Timeouts | New synchronous external call without explicit timeout | Hard rule for I/O |
| Circuit breakers | New synchronous external call in a hot path without breaker | Skip background jobs with bounded retry |
| Bulkheads | Single thread pool / connection pool serving > 1 dependency | Suggest pool-per-dependency |
| Fail fast | Long-running call that doesn't validate inputs upfront | Validate early |
| Steady state | New unbounded log file / metric cardinality | Bound it |
| Test harness for stability | No chaos / fault-injection test for a new external integration | Suggest, don't block |
| Decoupling middleware | New synchronous chain of > 3 services for a write | Suggest event / queue |

**Antipatterns to flag:**
- Integration points with no isolation
- Chain reactions (one failure cascades)
- Cascading failures (no circuit breaker between layers)
- Blocked threads (synchronous wait without timeout)
- Self-denial (cron storms, retry storms, thundering herd)
- Slow responses (no SLA enforcement)
- Unbounded result sets

### 2.11 Clean Code — Martin (with Goodbye-Clean-Code counterweight)

Use the local rules; skip the abstraction prescriptions.

| Rule | Detection signal | Guardrail (Abramov filter) |
|---|---|---|
| Small functions | Function > 30 lines | Skip if extracting hurts a sequential narrative |
| Single responsibility (function) | Function does setup + work + reporting | Skip when steps are < 3 lines each |
| Names reveal intent | Single-letter or abbreviated names outside short scopes | Skip mathematical / loop indices |
| Functions take < 4 args | > 3 args | Skip when args are a coherent group (use struct) |
| Comments explain why, not what | Comment paraphrases the next line | Keep "why" comments |
| **Anti-rule:** DRY everything | DO NOT flag duplication where the duplicates are different *concepts* | Entire Goodbye-Clean-Code corrective |
| **Anti-rule:** Always extract | DO NOT push for extracting a function used in one place | Single-call-site abstraction is indirection, not reuse |

### 2.12 Twelve-Factor App — [12factor.net](https://12factor.net/)

The most encodable essay in the canon. Each factor is a checkable rule.

| # | Factor | Detection signal |
|---|---|---|
| I | Codebase | Multiple repos for one app, or one repo serving > 1 app |
| II | Dependencies | Dependency installed implicitly (system-wide) rather than declared |
| III | Config | Config baked into code / committed `.env` / hardcoded URLs |
| IV | Backing services | Hard-coded backing-service URL; no swap-by-config |
| V | Build/release/run | Mutable releases; build steps mixed into runtime |
| VI | Processes | Process holds in-memory state across requests |
| VII | Port binding | App requires a webserver to be installed separately |
| VIII | Concurrency | Process model can't scale via process replication |
| IX | Disposability | Process leaks resources or can't shut down on SIGTERM |
| X | Dev/prod parity | Dev uses different backing service from prod (sqlite vs. postgres) |
| XI | Logs | App writes to log files instead of stdout/stderr |
| XII | Admin processes | One-off admin scripts not run with same release/config |

### 2.13 Required-Reading Essays — Distilled Rules

| Rule | Source | Detection signal | Guardrail |
|---|---|---|---|
| Essential vs. accidental complexity | [Brooks 1986](https://worrydream.com/refs/Brooks_1986_-_No_Silver_Bullet.pdf) | Don't simplify unless §1 markers say "accidental" | Default = don't flag |
| Essential / accidental, state / control | [Moseley & Marks](http://curtclifton.net/papers/MoseleyMarks06a.pdf) | New mutable state where derived value would suffice | Skip when persistence is the requirement |
| Big Ball of Mud | [Foote & Yoder](http://www.laputan.org/mud/) | New code added at the boundary of a defined module that erodes the boundary | Suggest extending the module's API instead |
| Innovation tokens | [McKinley](https://mcfunley.com/choose-boring-technology) | New language / framework / paradigm in PR | Require explicit cost-of-carry justification in PR description |
| Worse is better | [Gabriel](https://www.dreamsongs.com/RiseOfWorseIsBetter.html) | Implementation favors interface elegance at large implementation cost | Surface tradeoff; do not block |
| Goodbye, Clean Code | [Abramov](https://overreacted.io/goodbye-clean-code/) | DO NOT flag duplication when concepts differ across domains | Hard anti-rule |
| Trusting Trust | [Thompson 1984](https://www.cs.cmu.edu/~rdriley/487/papers/Thompson_1984_ReflectionsonTrustingTrust.pdf) | New build-toolchain dependency or auth-touching change | Require security-sub-reviewer signoff |
| Hyrum's Law | [hyrumslaw.com](https://www.hyrumslaw.com/) | Public API leaks: error message strings, ordering, timing, internal IDs | Either document as contract or hide |
| Programming as Theory Building | [Naur](https://pages.cs.wisc.edu/~remzi/Naur.pdf) | PR makes a non-trivial change without referencing the team's mental model (linked design doc, ADR, or comment thread) | Foundation for orientation-pass; ask, don't block |
| Semantic Compression | [Muratori](https://caseymuratori.com/blog_0015) | New abstraction with one call site | Inline; revisit at Rule-of-Three |
| Sandi Metz Rules | [henrik gist](https://gist.github.com/henrik/4509394) | Class > 100 lines; method > 5 lines; method args > 4; controller actions instantiate > 1 object | Treat as questions, not blockers |
| Postel's Law (modern, narrow form) | [Wikipedia](https://en.wikipedia.org/wiki/Robustness_principle) | Lenient input handling on internal-only API; strict validation on customer-facing API | Modern guidance inverts the original ("strict on input, generous on output") |
| Chesterton's Fence | [Chesterton](https://en.wikipedia.org/wiki/Wikipedia:Chesterton%27s_fence) | PR deletes error handling, retry, sleep, defensive code | Block until author explains the original purpose |
| Principle of Least Astonishment | [Wikipedia](https://en.wikipedia.org/wiki/Principle_of_least_astonishment) | `getX()` with side effects; functions returning different types based on input | Hard rule |
| Make Illegal States Unrepresentable | [Minsky](https://blog.janestreet.com/effective-ml-revisited/) | `Optional[T]` always required; paired bool params; runtime `assert x is not None` | Hard rule |
| YAGNI | [Fowler](https://martinfowler.com/bliki/Yagni.html) | Speculative parameterization, hooks, plugin points without current consumer | Inline; trust Rule of Three |
| Rule of Three | [Wikipedia](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)) | New abstraction with < 3 call sites | Inline |

### 2.14 Operationalizing the Rule Library

Three notes:

1. **Most rules are guardrails on each other.** DRY contradicts Goodbye-Clean-Code. Small Functions contradicts Sequential Narrative. Composition-over-Inheritance contradicts Domain-over-Data. Use the *guardrail column* — without it, your reviewer will become the dogmatic junior.

2. **Don't stack rules — gate them.** A reviewer that runs all ~200 rules on every PR will produce 50+ comments. Route by file type / change type: a config-only PR runs ~10 rules; a new public API runs ~40; a database migration runs the DDIA + Twelve-Factor subset; an auth-touching PR adds Trusting-Trust + the Release-It stability subset. The orientation pass picks the rule subset.

3. **Per-rule precision > rule count.** SWRBench top systems hit 19% F1 because they fire too many rules. Halve your rule list, keep only the rules with > 70% historical accept rate, and rate-limit per-PR comment count to 3-5. The §1 production data ([Greptile/CodeRabbit cleanup thread](https://news.ycombinator.com/item?id=42451968)) shows this is the dominant adoption barrier — not raw recall.

The intended consumer of this section is a `principles.yaml` (or equivalent) checked into the reviewer repo, with each rule tagged by `severity`, `applicable_languages`, `change_types`, and a `guardrail` predicate. Per-rule deletion is the calibration mechanism — don't add rules to production without a logged accept-rate.