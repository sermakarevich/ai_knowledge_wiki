> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science

## Claims vs. evidence
- Claim: a model-agnostic harness (works with any base model) for long-horizon
  math and TCS (Theoretical Computer Science) research.
  Evidence: partial — all runs use Gemini 3.1 Pro and Gemini 3.7 Flash only.
  No test with GPT, Claude, or open models, so "model-agnostic" is unproven.
- Claim: 71.0% on TCS-Bench (300 research-level theorem tasks from
  FOCS/STOC/SODA papers), beating GPT-5.6 Pro max at 68.0%.
  Evidence: moderate-strong for breadth, but the scorer is a reference-assisted
  automated grader (~90% expert agreement on 100 samples), not human judging.
  A few points of grader error would change the ranking.
- Claim: the harness itself is the lift (direct Gemini 3.1 Pro 30.3%,
  DeepThink 52.0%, Colosseum single runs 54–55%).
  Evidence: reasonable direction, but with no compute-matched baseline.
  Colosseum uses 32-leaf exploration trees plus 16-leaf downstream trees,
  i.e. far more model calls than any single-shot baseline.
- Claim: cross-model critique selection (Flash critiques the Pro proof 8 times;
  submit Pro if at least 5 judge it correct) drives 55% to 71.0%.
  Evidence: strongest internal result — the critique signal reaches AUC
  (Area Under Curve, a 0–1 ranking-quality score) 0.896, vs. 64.7% routing
  with Pro's own verifier. But the rule is asymmetric and the oracle
  best-of-two is 77.3%, so selection still leaves ~6 points on the table.
- Claim: five new results plus 46/75-page Knuth-cycle drafts and a 22-page
  independent rediscovery of the Erdos unit-distance breakthrough (15 rounds,
  internet disabled). Evidence: suggestive but attribution is thin —
  proofs live in companion papers, human roles are undisclosed, and none
  carries a machine-checked certificate (e.g. Lean, a formal proof checker).
- Claim: 218/222 Codeforces with execution feedback.
  Evidence: real, yet a different regime — runnable tests give ground truth
  that pure proof work lacks, so it does not transfer to proof correctness.

## Genuinely new vs. repackaged
- Genuinely new as a composition: (1) an explicit readiness gate that blocks
  decomposition until a strategy card is "concrete enough", with a formal
  minor-vs-major obligation rule; (2) DAG (Directed Acyclic Graph — a map of
  dependencies with no cycles) decomposition where document order and work
  order are separated and retries are local to failed sections.
- Also new in combination: (3) overlapping random-sample tree aggregation that
  carries falsifier critiques forward instead of voting them away; (4) dual
  cross-round memory — the full rejected draft plus a curated knowledge
  directory (theorems/lemmas, failed approaches, references, observations,
  each with source and caveats).
- Repackaged: the inner loop (generate → adversarial falsify → aggregate)
  restates Self-Refine, Tree-of-Thoughts, multi-agent debate, and REBASE-style
  inference scaling. Verifier-guided search, blueprint + dependency graphs
  (LeanMarathon), and generate–verify–revise loops (Aletheia, QED,
  ProofCouncil, RMA) are acknowledged relatives in the paper itself.
- Fair reading: the novelty is orchestration discipline plus scale and strict
  prompt contracts — not a new sampling or learning algorithm.
  The paper is honest about extending Woodruff et al. [56].

## Weaknesses and blind spots
- No cost accounting: no call counts, tokens, dollars, or latency.
  Trees with 100+ leaves × solvers × falsers × aggregators × retries ×
  15 rounds imply a very large bill; efficiency is unjudged.
- No ablations: readiness gate, DAG locality, critique-preserving aggregation,
  knowledge directory — without removing each piece, every mechanism claims
  credit for the whole gain.
- Fixed allocation, admitted by the authors: widths (32,16,8,5,1) and k=5 are
  set upfront. The proposed adaptive controller (expand uncertain branches,
  retry unstable sections, stop stable ones) is future work only.
- Verification gap: natural-language proofs reviewed by model verifiers, where
  one concrete fatal defect rejects. A persuasive-but-wrong long draft can
  still pass, unlike Lean-checked systems or OpenAI's Lean-certificate work.
- Limited reproducibility: Appendix A gives explicitly "shortened" prompts;
  harness code, full prompts, curator details, and grader prompt are missing.
- Reporting bias: five successes and two long case studies are shown; failed
  campaigns, dead-end rounds, and curator error accumulation are unquantified.
- Unverifiable product claim: integration into Google Antigravity's Teamwork
  framework as the "Long Proof pattern" is cited, not demonstrated.

## Applicability
- Direct reuse of the whole harness fits long-proof math/TCS work with big
  inference budgets. Most teams should borrow the patterns, not the system.
- Transferable patterns: gate a strategy before decomposing it; split work
  into a dependency graph with local retry; keep critiques attached to
  candidates through aggregation; keep two memories (last full attempt plus
  a curated reusable-findings store); use a cheap critic as a router.
- Limits: needs tasks that split into checkable sections plus some verifier
  signal (tests, execution, strong critique). Shallow Q&A gains little.
- **Relevance to my work**
  - AI/ML engineering: the falsifier + aggregator roles template an evaluation
    pipeline — generate candidates, attack with edge-case critics, aggregate
    with objections preserved instead of majority vote.
  - Agentic systems: the readiness gate ("is this plan concrete enough to
    split?") and the conservative revision rule ("no new sections, no new
    strategy in revision") are reusable guards against plan drift.
  - The Elisity data platform: the knowledge directory (lemmas, failed
    approaches, references, observations with source + caveats) maps to a
    curated findings store across runs — failed queries, data-quality
    pitfalls, reusable transforms — so later runs inherit evidence.

## What this changes
- It moves the bet from bigger single answers to better orchestration of many
  medium answers: stage control plus critique-preserving aggregation beats
  flat sampling and voting on proofs.
- It shows a cheap critic can be a strong router (+16 points over the best
  single run here), which can matter more than squeezing the generator.
- It makes research trajectories (strategies, critiques, DAGs, drafts,
  revision histories) first-class artifacts — for debugging agents and,
  prospectively, as post-training data, credit assignment aside.
- It normalizes 15-round, 50+ page agent-produced drafts as persistent
  revisable documents rather than one-shot generations.

## Verdict
- Strong systems paper with real breadth results, weakened by Google-only
  models, an automated grader, missing costs and ablations, and no formal
  checking. Borrow the architecture; do not buy it as a finished product.
- Practical call: pilot the readiness gate, DAG-local retry, and
  critique-attached aggregation in one existing workflow with
  compute-matched logging before anything larger.
- **trial**
