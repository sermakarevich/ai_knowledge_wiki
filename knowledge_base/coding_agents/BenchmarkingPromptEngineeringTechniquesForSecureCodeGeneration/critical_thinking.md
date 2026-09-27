> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: Benchmarking Prompt Engineering Techniques for
## Claims vs. evidence
- Central question: "Can we enhance GPT's secure code generation via prompt engineering?"
- The answer given is yes for the GPT-4o family, no for GPT-3.5-turbo proactive prompts.
- Prefix claim: pe-03-a ("very security-aware developer") cuts SAFVS by 47% on 4o-mini and 56% on 4o (3.27% vs. 7.43% baseline on 4o).
- Supporting detail: pe-03-a beats sibling prefixes/suffixes (pe-01-a/b/c, pe-02-a/b) in Table IV, so it is not just any security wording.
- RCI claim: one iteration fixes 24.5% (3.5-turbo), 49.5% (4o-mini), 64.7% (4o) of flawed snippets.
- Combination claim: RCI on pe-03-a snippets reaches 68.7% below baseline (2.33%) on 4o, the best cell reported.
- Iteration claim: further RCI rounds help (3.5-turbo iter-2 +32.8%, iter-3 +41.9%) but with diminishing returns by iter-3 on 4o-mini.
- Sensitivity claim: prompt leverage grows with capability — no proactive win on 3.5-turbo (worst +31.1% worse), broad wins on 4o-mini/4o.
- Adversarial mirror: pe-negative raises SAFVS 69.3% (3.5), 127.7% (4o-mini), 152.7% (4o to 18.76%), consistent with the steerability gradient.
- Metric basis: SAFVS requires Semgrep AND CodeQL to agree on the suspected CWE family per sample, averaged into OFVP over k runs.
- Scale basis: n=202 Python prompts after dropping unscannable cases; 10 samples per attempt at temperature 1; 100-sample baselines for 3.5 and 4o-mini.
- Functionality basis: HumanEval spot-check (4 attempts, 10 samples, 4o-mini) shows pass@10 flat (~94-95%) but pass@1 down ~10pts under RCI (86.7% -> ~76.7%).
- Extraction hygiene is solid: regex code-block pull plus ast.parse validation with bounded retries avoids rewarding syntax failures as secure.
- Cost transparency helps: tiktoken estimates plus Batch-API note and the $28-vs-$3080 anecdote make replication budgeting concrete.
- Statistical basis: descriptive only — box plots and relative diffs, explicitly no inferential tests, so rank order is suggestive not proven.
## Genuinely new vs. repackaged
- New: an automated, reusable benchmark harness (augment -> generate -> extract -> scan -> score) with pinned snapshots and open data/code.
- New: dual-scanner agreement metric (SAFVS) plus repeated-run distribution (OFVP) as a pragmatic answer to scanner noise and temperature-1 variance.
- New: direct comparison of prevention (prefix) vs. cure (RCI) vs. stacked prevention+cure on identical prompts and models.
- New: documentation of the capability gradient, including the uncomfortable 3.5-turbo inversion where dumber looks safer.
- Repackaged: security-persona prompting itself — Firouzi/Ghafari already showed "secure solution" wording lifting clean answers 3/100 to 42/100.
- Repackaged: RCI and CoT mechanics are imported from prior prompting literature, applied here rather than invented.
- Repackaged: the Prompt Agent (prefix preprocessing + RCI postprocessing in BetterChatGPT) restates CodeShield/LLMSecGuard scan-then-fix, minus the external analyzer in the repair loop.
- Net: method and measurement are the contribution; no novel prompting primitive is claimed or shown.
## Weaknesses and blind spots
- Scanner dependence: two static tools define truth; false negatives survive agreement filtering, and "fix the scanner finding" can masquerade as "fix the flaw."
- CWE-mapping fuzz: counting MITRE "Recommended Mapping" and "Can Also Be" CWEs widens the net but adds mapping judgment calls.
- Leakage risk: public LLMSecEval/SecurityEval predate 4o/4o-mini training cutoffs, so part of the win may be memorized secure completions.
- Baseline confound: 3.5-turbo's best baseline (5.97%) coincides with lower AST height — possibly shorter, incomplete, unscannable-as-vulnerable code.
- Narrow scope: Python single-snippet tasks only; no repo context, no multi-file taint flow, no JavaScript/other languages despite related-work coverage.
- Vendor lock: OpenAI-only, three snapshots; generalization to Claude/Llama/coding-specialist models is asserted nowhere and tested nowhere.
- Partial execution: only "most interesting" subset run on GPT-4o for cost reasons, inviting selection bias toward techniques already winning on 4o-mini.
- Variance handling: 10-sample adequacy rests on two 100-sample baselines and eyeballed central tendency, not power analysis.
- Prompt brittleness: persona vs. pe-03-a paraphrases differ markedly; some attempts (pe-02-d/e) need oracle CWE lists unavailable in production.
- Functionality gap: HumanEval tasks trigger zero scanner hits, so the security-functionality tradeoff is measured where security signal is absent.
- Over-caution signal: authors note RCI verbosity suited to beginners but alienating to experts — a UX tax on always-on hardening.
- Cost/latency realism: RCI doubles large-context calls per snippet and adds >10s even on short outputs; repo cost anecdote ($28 vs. ~$3080 at 4o scale) warns against naive always-on use.
## Applicability
- Directly usable: prepend a one-sentence security persona to codegen system prompts; near-zero cost, no reported chatbot impairment.
- Conditionally usable: expose RCI as an explicit "review and harden" action on diffs touching auth, crypto, SQL, subprocess, deserialization, or secrets.
- Operational pairing: keep static scans in CI — RCI output should re-enter Semgrep/CodeQL rather than being trusted on LLM self-critique alone.
- Measurement pairing: track scanners-agree rate per template/model version, plus pass@1/pass@10 on a held-out functional set, before and after prompt changes.
- Do not copy: CWE-list prefixes and deliberately-vulnerable probes are benchmark instruments, not production prompts.
- **Relevance to my work**
  - AI/ML engineering: trial the pe-03-a prefix in codegen templates; A/B scanner-agree rates per model bump; quarantine RCI to high-risk paths with latency budgets.
  - Agentic systems: implement the agent middleware pattern — preprocess (prefix) then optional postprocess (critique + rewrite code blocks only, preserving prose); cap at one RCI pass by default.
  - Elisity data platform: prioritize connector/pipeline codegen (ingest parsers, SQL builders, credential plumbing) where the benchmarked CWE classes overlap real blast radius; log prefix/RCI provenance per generated artifact for audit.
## What this changes
- Default posture flips: secure-prefix-on unless measured harm, instead of neutral prompt plus post-hoc scan.
- Stacking beats choosing: prevention plus one repair pass outperforms either alone (56% -> 68.7% on 4o), so pipeline design should compose them.
- Model upgrades now require prompt re-validation: steerability rises with capability in both directions, including adversarial misuse.
- Evaluation norm gets lighter: 10-sample dual-scanner screening plus a small HumanEval gate is enough to trial a template before committing.
## Verdict
- Useful, bounded, and honest about limits: strong enough harness and consistent-enough direction to act on the cheap intervention, too scanner-bound and vendor-narrow to redesign around RCI.
- Risk of over-reading is rank-order certainty and cross-model portability, neither of which the statistics or model coverage support.
- Practical path is prefix now, instrumented RCI next, re-benchmark on each model or language shift.
- **trial**
