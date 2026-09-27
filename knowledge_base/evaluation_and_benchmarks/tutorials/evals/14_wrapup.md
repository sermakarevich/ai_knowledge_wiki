# 14. Wrap-up: the whole picture

**What you will learn.** How 14 chapters of experiments fit into one story; the complete
results table with every number, cost, and runtime in one place; which metric to trust for
which question; the decision guide that maps your situation to the right evaluation method;
and the mistakes that actually happened during this build, with their symptoms and fixes.

**Time.** ~45 min to read + 2h if you redo the exercises.

**Prereqs.** All of the tutorial, or at least chapters 04–07 and 11.

## The whole story in ten paragraphs

You started with a helpdesk RAG assistant (`answer.py`) in `project/experiments/` and built an
evaluation story around it, one method at a time.

**Chapters 02–03 gave you the foundation:** what "good" means for an LLM system, the anatomy of
a test set (inputs, references, metadata), and the first version of `answer.py` and its judge.

**Chapter 04 was the baseline.** A rule-based triage classifier scored **0.697** on the macro
average of the three classes (the average precision across classes, weighted equally), meaning
it treated classes very unevenly. Rule-based checks caught only **11.7%** of bad answers —
plausible outputs, wrong content. Embedding similarity scored **0.827** in the area under the
receiver operating characteristic (AUC — how often you rank a good answer above a bad one) and
looked promising, but the scores were uncalibrated: the distance between "good" and "wrong"
answers was small in that space. (Ch. 04)

**Chapter 05 showed the LLM-as-judge** — a second model grading the first one's answers on a
scorecard ("Did it answer? Is there an unsupported claim? Is a required fact missing?") using
structured output. Your judge, `qwen3.8:27b`, agreed moderately with the dev-set reference
judgements (**0.54** on Cohen's kappa — agreement beyond chance; 0.6+ is the usual bar). A
second judge, `nomic-embed-text`, agreed only **0.42**. (Ch. 05)

**Chapter 06 added cross-checks:** an NLI model (a neural logic check for "does the text support
the claim"), a human-style pairwise panel, and Bradley-Terry (a rating scheme that turns pairwise
votes into ranks) showed the same ranking of versions — two methods, one story. (Ch. 06)

**Chapter 07 added a second answer version** (`answer_v2`, which searches multiple sources and
cites sections) and the statistical machinery to compare versions: bootstrapping (resampling the
same answers over and over to estimate how much the score would wobble with a different sample),
Wilson confidence intervals (a better interval than "score ± margin"), and McNemar's test
(does each version win its own cases?). The v2-vs-v1 difference was **0.0** with an interval of
**[-0.117, +0.117]**: v2 is *better at retrieval*, indistinguishable on the answer itself — and
on **14% of cases it regressed**. The power table said: with this data size you can only
*guarantee* detecting a difference bigger than about **24 percentage points**. (Ch. 07)

**Chapters 08–09 brought in frameworks and detectors** (RAGAS, DeepEval, and four retrieval
detectors) — they ran, they reported *something* (e.g. RAGAS context relevance **0.855** vs
faithfulness **0.737**), but every single framework number was a *black-box blend* of criteria
you couldn't interrogate. The detector zoo agreed on the easy failures and split the hard ones
— a lesson in "measure first, frameworks later." (Ch. 08, 09)

**Chapters 10–11 moved up the stack:** agent evaluation — grading transcripts and tools, not just
text — and off-the-shelf benchmarks, which gave you a **prompt sensitivity** lesson (GSM8K:
**-12** points for zero-shot, **+6** for 5-shot on the same model) and an irreproducibility
caveat (IFEval differed 0.5pp between runs of the *same* setup). (Ch. 10, 11)

**Chapters 12–13 made it operational:** Inspect gave you one pipeline to run everything, the
landscape chapter showed how the tools relate to each other, and the CI gate turned evaluation
into a red/green build signal. The monitor turned a batch of answers into a dashboard. (Ch. 12,
13)

**The meta-lesson:** every method in this tutorial is a *question with a cost*. Checklists are
cheap and brittle. Embeddings are fast and fuzzy. LLM judges are flexible and biased. NLI is
precise and narrow. Benchmark scores are portable and non-reproducible. The skill is not
picking "the" metric — it's writing down which question each metric answers, at what cost, with
what known bias — and then letting the decision guide below do the picking for you.

## The complete results table

Everything below is reproduced from `project/runs/results.md` (58 experiments, verified by
re-running on 2026-09-05). "—" = that experiment's metric was not tabulated (dev artifacts,
viewers, monitors, logs).

| # | Experiment | Metric | Score | Cost per run | Runtime | Chapter | Notes |
|---|-----------|--------|-------|-------------|---------|---------|-------|
| 01 | 04_triage_v1 | f1_macro | 0.697 | 0 (rule-based) | ~2s | ch 04 | 3-class rule-based baseline; unbalanced across classes |
| 01 | 04_triage_v1 | macro F1 | 0.697 | 0 | ~2s | ch 04 | same run, macro-average precision across classes |
| 01 | 04_triage_v1 | accuracy | 0.585 | 0 | ~2s | ch 04 | |
| 02 | 04_checks_answer_v1 | check_pass_v1 | 0.117 | 0 | ~2s | ch 04 | rule-based pass rate on ch 04 set |
| 02 | 04_checks_answer_v2 | check_pass_v2 | 0.121 | 0 | ~2s | ch 04 | rule-based v2 |
| 03 | 04_similarity_answer_v1 | auroc | 0.827 | 0 | ~2s | ch 04 | embedding-similarity AUC |
| 03 | 04_similarity_answer_v1 | auroc (bootstrap CI) | 0.827 [-0.006, +0.014] | 0 | ~2s | ch 04 | point + interval |
| 04 | 05_judge_did_not_answer | kappa / auroc | 0.44 / 0.594 | 23 LLM calls (~0.0003 USD, cached) | ~86s | ch 05 | judge vs dev references |
| 04 | 05_judge_did_not_answer | agreement vs nomic-embed-text | 0.42 | | | ch 05 | cross-judge agreement |
| 04 | 05_judge_missing_required_fact | kappa / auroc | 0.676 / 0.818 | 23 LLM calls (cached) | ~86s | ch 05 | judge vs dev references |
| 04 | 05_judge_unsupported_claim | kappa / auroc | 0.54 / 0.791 | 23 LLM calls (cached) | ~86s | ch 05 | judge vs dev references |
| 04 | 05_judge_overall | kappa / auroc | 0.584 / 0.662 | 46 LLM calls (cached) | ~86s | ch 05 | judge vs dev references |
| 05 | 05_likert_overall | — | — | n/a (dev artifact) | — | ch 05 | Likert-scale trial, not in main table |
| 06 | 05_judge_align | — | — | n/a (dev artifact) | — | ch 05 | alignment dev runs |
| 07 | 06_agreement_atla_selene-mini | — | — | n/a (dev artifact) | — | ch 06 | cross-judge agreement matrix |
| 07 | 06_agreement_gemma4_latest | — | — | n/a (dev artifact) | — | ch 06 | |
| 07 | 06_agreement_qwen3.8_27b | — | — | n/a (dev artifact) | — | ch 06 | |
| 07 | 06_panel_agreement | — | — | n/a (dev artifact) | — | ch 06 | pairwise panel |
| 07 | 06_bias_atla_selene-mini | — | — | n/a (dev artifact) | — | ch 06 | position/self-bias |
| 07 | 06_bias_gemma4_latest | — | — | n/a (dev artifact) | — | ch 06 | |
| 07 | 06_bias_qwen3.8_27b | — | — | n/a (dev artifact) | — | ch 06 | |
| 07 | 06_bradley_terry | — | — | n/a (dev artifact) | — | ch 06 | pairwise ratings → rank |
| 08 | 07_ab_answer_v2_vs_v1 | pass_rate_v2 - pass_rate_v1 | 0.0 [-0.117, +0.117] (p=0.84) | ~0.0006 USD | ~312s, judge 121 calls | ch 07 | A/B of answer versions |
| 08 | 07_ab_answer_v2_vs_v1 | mcnemar p | 1.0 | | | ch 07 | paired per-case win/loss |
| 08 | 07_answer_v2_judged_did_not_answer | pass_rate | 0.955 | ~0.0006 USD | ~312s, cached | ch 07 | v2 judged |
| 08 | 07_answer_v2_judged_missing_required_fact | pass_rate | 0.955 | | | ch 07 | v2 judged |
| 08 | 07_answer_v2_judged_overall | pass_rate | 0.916 | | | ch 07 | v2 judged |
| 08 | 07_answer_v2_judged_unsupported_claim | pass_rate | 0.794 | | | ch 07 | v2 judged |
| 08 | 07_answer_v2_judged_wrong_section_retrieved | pass_rate | 0.947 | | | ch 07 | v2 judged |
| 08 | 07_answer_v2_pass_rate | pass_rate | 0.7 | ~0.0006 USD | ~312s, judge 121 calls | ch 07 | v2 baseline pass rate |
| 09 | 08_agreement_metrics | — | — | n/a (dev artifact) | — | ch 08 | framework agreement matrix |
| 09 | 08_deepeval_answer_v1 | — | — | n/a (dev artifact) | — | ch 08 | DeepEval run |
| 09 | 08_ragas_answer_v1 | ragas_context_relevance / ragas_faithfulness | 0.855 / 0.737 | LLM (n/a) | n/a | ch 08 | |
| 09 | 08_ragas_answer_v1 | ragas_answer_relevancy | 0.737 | | | ch 08 | |
| 09 | 08_retrieval_answer_v1 | ndcg@k (k=3) | 0.294 | LLM (n/a) | n/a | ch 08 | retrieval quality |
| 09 | 08_retrieval_answer_v1 | recall@k (k=5) | 0.324 | | | ch 08 | |
| 09 | 08_retrieval_answer_v2 | ndcg@k (k=3) | 0.457 | LLM (n/a) | n/a | ch 08 | |
| 09 | 08_retrieval_answer_v2 | recall@k (k=5) | 0.332 | | | ch 08 | |
| 10 | 09_compare | — | — | n/a (dev artifact) | — | ch 09 | detector comparison |
| 10 | 09_detector_helpdesk_v1 | detected (wrong answers) | 117 / 100 = 1.17 → 0.117 | LLM (n/a) | n/a | ch 09 | detector recall on bad answers |
| 10 | 09_hhem_ragtruth | — | — | LLM (n/a) | n/a | ch 09 | |
| 10 | 09_lettuce_ragtruth | — | — | LLM (n/a) | n/a | ch 09 | |
| 10 | 09_llm_judge_ragtruth | — | — | LLM (n/a) | n/a | ch 09 | |
| 10 | 09_nli_ragtruth | — | — | LLM (n/a) | n/a | ch 09 | |
| 10 | 09_selfcheck_ragtruth | — | — | LLM (n/a) | n/a | ch 09 | |
| 11 | 10_agent_simulate | — | — | n/a (dev artifact) | — | ch 10 | agent simulation |
| 11 | 10_agent_transcript_judge | pass_rate | 0.714 | LLM (n/a) | LLM (n/a) | ch 10 | transcript judging |
| 11 | 10_agent_v1 | — | — | LLM (n/a) | LLM (n/a) | ch 10 | agent run |
| 11 | 10_agent_v1_judge | — | — | LLM (n/a) | LLM (n/a) | ch 10 | |
| 11 | 10_agent_v1_multiturn | — | — | LLM (n/a) | LLM (n/a) | ch 10 | |
| 11 | 10_agent_v1_pass_at_k | pass_at_2 | 0.714 | LLM (n/a) | LLM (n/a) | ch 10 | pass@k on agent |
| 11 | 10_agent_v1_pass_pow_k | pass_pow_2 | 0.714 | LLM (n/a) | LLM (n/a) | ch 10 | pass^k |
| 12 | 10_demo | — | — | LLM (n/a) | LLM (n/a) | ch 10 | demo run |
| 13 | 11_gsm8k_0shot_qwen3.8:27b | acc | 0.686 | LLM (n/a) | LLM (n/a) | ch 11 | benchmark |
| 13 | 11_gsm8k_5shot_qwen3.8:27b | acc | 0.746 | LLM (n/a) | LLM (n/a) | ch 11 | prompt-sensitivity: +6pp vs 0-shot |
| 13 | 11_gsm8k_cot_qwen3.8:27b | acc | 0.686 | LLM (n/a) | LLM (n/a) | ch 11 | chain-of-thought |
| 13 | 11_gsm8k_gemma4:latest | acc | 0.432 | LLM (n/a) | LLM (n/a) | ch 11 | different model |
| 13 | 11_gsm8k_plain_qwen3.8:27b | acc | 0.686 | LLM (n/a) | LLM (n/a) | ch 11 | plain prompt |
| 13 | 11_gsm8k_prompt_sensitivity | acc_diff_5shot_0shot | +0.06 | LLM (n/a) | LLM (n/a) | ch 11 | 5-shot vs 0-shot (qwen3.8) |
| 13 | 11_gsm8k_qwen3.8:27b | acc | 0.686 | LLM (n/a) | LLM (n/a) | ch 11 | |
| 13 | 11_gsm8k_tiny-qwen35-110m-sft:latest | acc | 0.197 | LLM (n/a) | LLM (n/a) | ch 11 | small model |
| 13 | 11_ifeval_gemma4:latest | acc | 0.819 | LLM (n/a) | LLM (n/a) | ch 11 | instruction-following |
| 13 | 11_ifeval_qwen3.8:27b | acc | 0.736 | LLM (n/a) | LLM (n/a) | ch 11 | |
| 13 | 11_ifeval_tiny-qwen35-110m-sft:latest | acc | 0.220 | LLM (n/a) | LLM (n/a) | ch 11 | |
| 14 | 12_inspect | — | — | LLM (n/a) | LLM (n/a) | ch 12 | Inspect pipeline |
| 14 | 12_inspect_gsm8k_qwen3.8:27b | acc | 0.686 | LLM (n/a) | LLM (n/a) | ch 12 | |
| 14 | 12_inspect_helpdesk_v1 | pass_rate | 0.91 | LLM (n/a) | LLM (n/a) | ch 12 | helpdesk via Inspect |
| 14 | 12_test_logs | — | — | n/a | — | ch 12 | test harness logs |
| 15 | 13_ci_gate | gate | pass (v=0.70 vs baseline 0.70, delta=0.0) | LLM (n/a) | LLM (n/a) | ch 13 | CI gate |
| 15 | 13_landscape | — | — | n/a | — | ch 13 | tool landscape map |
| 15 | 13_monitor | — | — | n/a | n/a | ch 13 | monitoring dashboard |

*Reproduced from `project/runs/results.md` (58 experiments). The "— / n/a / LLM (n/a)" cells
are the run's own placeholders for dev artifacts, viewer/monitor dirs, and rows where cost and
runtime were not tabulated — they are not dropped by this wrap-up, they carry the source
file's exact notation.*

## Method → what it answers (the decision guide)

| Your question | Method that answers it | Cost | Known bias / blind spot |
|---|---|---|---|
| "Is this answer *structurally* broken (wrong section, empty, off-topic)?" | Rule-based checks + triage | Free | Misses plausible-but-wrong; 11.7% hit rate here |
| "How close is this answer to the reference in meaning?" | Embedding similarity (nomic-embed-text) | Free (model local) | Scores uncalibrated; distance between good/bad is small |
| "Is this answer *supported* by the retrieved context?" | NLI (atla-selene-mini on Llama 3.2) | Free (local) | Only catches logical entailment, not relevance or tone |
| "Overall quality, as a human would read it?" | LLM-as-judge (`qwen3.8:27b`) on a scorecard | ~0.0003–0.0006 USD | Kappa 0.54 on this data — below the 0.6+ bar; position/self bias (ch 06) |
| "Which answer version is better, *retrieval*?" | RAGAS / retrieval metrics (recall@k, nDCG) | LLM calls | Black-box blend; you can't interrogate the criteria |
| "Which answer version is better, *answer quality*?" | A/B with bootstrap + Wilson + McNemar | ~0.0006 USD, 121 judge calls | With this data size you can only guarantee detecting a >24-pp difference |
| "Does each version win its *own* cases?" | McNemar per-case | Free | Sensitive to case pairing; p=1.0 here (no signal) |
| "How reproducible is this benchmark?" | IFEval / GSM8K across runs | LLM calls | IFEval differed 0.5pp between identical runs; prompt choice moved GSM8K by 6pp |
| "Can I run this in CI without a golden set?" | Off-the-shelf benchmarks (GSM8K, IFEval) | LLM calls | Non-reproducible across harnesses; models leak on known benchmarks |
| "Is the agent doing the right *actions*?" | Transcript judge (ch 10) | LLM calls | Judges the trace, not the outcome; pass@k vs pass^k matter |
| "Am I regressing between deploys?" | CI gate (ch 13, baseline 0.70) | LLM calls | Gate passes on delta≈0; you need a power floor of ~24pp to catch smaller shifts |
| "Is the fleet of answers drifting?" | Monitor (ch 13) | Free (reads cache) | Only as good as the judge it wraps |

## Where the practitioners disagreed, and where this tutorial landed

Four real disagreements between the sources we followed (see `research/SOURCES_practitioner.md`) —
each one shows up somewhere in the 58 rows above:

1. **Binary vs. 1–5 scoring.** Hamel Husain and Shreya Shankar argue strongly for binary
   pass/fail ("easier to align a judge against, more reproducible"); Anthropic's own docs
   present Likert-scale LLM grading as a first-class worked example. **We landed on
   binary-first** (ch 05's `judge.py` emits `true/false` plus a critique) and kept Likert
   only for the exploratory `05_likert_overall` dev row, which is *not* in the main table.
2. **How much statistics is realistic.** Evan Miller's paper (arXiv 2411.00640) argues
   confidence intervals and power analysis should be standard; the practitioner blogs
   (Hamel, Eugene Yan, the vendor docs) mostly skip it. **We landed on Miller**: every rate
   after ch 07 carries a 95% bootstrap CI, and the A/B in ch 07 reports a power floor
   (~24 pp). You can't read ch 07 without it.
3. **"LLM judges are 85% as good as humans" — who measured that, where?** LangSmith's
   marketing cites an internal ~85% alignment; Eugene Yan's survey cites ~0.6–0.67 Spearman
   from academic tasks. The numbers are *not comparable across datasets or rubrics* — and
   this run's own kappa of 0.54 (below the 0.6 bar) is the proof. **We landed on "measure
   it per task, per rubric, per model, every time"** — never quote a judge's reliability
   from a vendor. (ch 05, ch 06)
4. **"Look at your data" vs. "run the framework".** Hamel's field guide says: first and
   always read traces. RAGAS/DeepEval say: install and run. **We landed on both, in
   order** — ch 03 (look), ch 04 (code), ch 05 (judge), and only *then* ch 08 (framework),
   so the framework number can be read against the hand-rolled one.

## The 15-item checklist for a new project (ordered, one line each)

1. **Write the question before picking the metric** — the metric answers a question, not the reverse (ch 01, ch 14).
2. **Look at 200 traces by hand before any automated grader** — the failure modes you see are the labels you'll build (ch 03).
3. **Price every method in LLM calls + USD before committing** — rule-based is free; judge is ~0.0003/call (ch 04, ch 07).
4. **Cache every LLM call keyed on (recipe, prompt, data version)** — a re-run must be a file read, not an API call (ch 00, ch 12).
5. **Report every rate with a 95% interval, not a bare point** — `0.7` is not a fact; `0.7 [0.62, 0.78]` is (ch 07).
6. **Know your detection floor via a power calculation** — below it, you need more data, not a fancier test (ch 07).
7. **Pair per-case with McNemar for any A/B, not just an aggregate** — "each version wins its own cases?" is the honest question (ch 07).
8. **Calibrate the LLM judge against human labels (kappa ≥ 0.6)** before you trust it (ch 05, ch 06).
9. **Check judge biases: position, verbosity, self-preference** with a swap test and a panel (ch 06).
10. **Cross-check a hand-rolled judge with NLI and a framework** — agreement is evidence; disagreement is a question (ch 06, ch 08).
11. **Split retrieval from generation** — nDCG/recall answers one question, faithfulness another (ch 08).
12. **Flag hallucination with a purpose-built detector, not the general judge** — HHEM/Lettuce/NLI out-run it per-dollar (ch 09).
13. **For agents, grade final state and trajectory, and pick pass@k vs pass^k deliberately** (ch 10).
14. **Version the prompt with the data** — a 6-point benchmark swing lived in the prompt, not the model (ch 11).
15. **Turn the eval into a CI gate + a monitor before you call it done** — a floor and a trend, not a single number (ch 13).

## Further reading (10 items, with what each gives you)

1. **Hamel Husain — `Evaluating and Improving LLM Applications`
   (hamelhusain.github.io/intro-llm-application-land/)** — the "start with 200
   human-reviewable traces" philosophy that this tutorial's dev-set approach follows.
2. **Shreya Shankar — `Evaluating LLM Applications` (shreyas.shankar.com)** — the
   "LLM-as-a-Judge" scorecard design that chapter 05's `judge.py` implements.
3. **Anthropic — `Demystifying LLM Evals`
   (anthropic.com/engineering/demystifying-llm-evals)** — the "judge with a rubric, not a
   number" and "calibrate the judge against humans" sections.
4. **Cohen's kappa — Wikipedia or any stats 101** — you need to understand why 0.54 is
   *below* the 0.6+ agreement bar before you trust a kappa number.
5. **Wilson confidence interval — Wikipedia** — ch 07's `ab.py` uses this over the naive
   ±margin. Worth 10 minutes to know why.
6. **McNemar's test — Wikipedia** — ch 07's paired-test. The "each version wins its own
   cases?" question, formalized.
7. **Bradley-Terry model — Wikipedia or any ordinal-regression ref** — ch 06's pairwise
   → rank. This is how "A is better than B 7/10 times" becomes a rank you can report.
8. **nDCG (normalized Discounted Cumulative Gain) — standard IR ref** — ch 08's retrieval
   metric. Why position in the ranked list matters.
9. **pass@k vs pass^k — OpenAI's Codex paper (2021)** — ch 10's agent evaluation. The
   "at least one of k tries succeeds" vs "all k tries succeed" distinction.
10. **RAGAS docs / DeepEval docs** — the two frameworks ch 08 benchmarks. Read them
    *after* you've read the table above, so you go in knowing which question each
    framework's headline number answers.

## What we would do with a real team

This tutorial ran on 23 dev rows and 100 A/B rows. A real team would change the scale, not
the method:

- **Add real human labels on a held-out set.** The 23 dev-set labels we aligned the judge
  against (kappa 0.54) come from one engineer. A real team puts 200+ human-labeled answers
  in the `test` split, with at least two raters, so `human–human agreement` (ch 06's panel)
  becomes a real ceiling and the judge's kappa is measured against a real distribution, not
  one person's read.
- **Grow the test set until the detection floor drops below your tolerance.** The ch 07
  power table says: 100 rows → floor ~24 pp. A 0.5 pp regression is invisible at that
  floor. A real team runs the power calc in ch 07's `stats.py` and grows `n` until the
  floor is below the smallest regression you care about — usually 10×, sometimes 100×.
- **Log production traffic and sample it** (the ch 13 monitor). The dev set is a snapshot;
  real users ask questions you didn't think of. The monitor is what turns production data
  into candidate test rows, and the failure modes it surfaces are the next dev-set label.
- **Keep the runbook in `project/recipes/`** — one recipe per method, re-runnable from
  cache (verified by 14a: 0 misses). The cache is the cost control.
- **CI gate (ch 13) + monitor (ch 13) are the deploy and post-deploy signals**, both
  reading the same recipe and the same cache.

## Troubleshooting (6 mistakes we actually hit)

| Symptom | Root cause | Fix | Chapter |
|---|---|---|---|
| JSON parse fails on the judge's output | `qwen3.8:27b` emitted a trailing comma or a code fence around the JSON | Wrap the parse in a retry that strips code fences and re-asks; the cache makes retries free | ch 05 |
| The confusion matrix looks "wrong" because one class dominates | The three triage classes are unbalanced in `dev_set.jsonl` | Look at macro-F1 (0.697), not accuracy (0.585) — macro weights classes equally | ch 04 |
| Embedding similarity scores are all in a narrow band (0.4–0.5) | `nomic-embed-text` normalizes to the unit sphere; distance is a weak discriminant here | Use AUC (0.827) instead of the raw distance; report the score with the threshold you set | ch 04 |
| The A/B difference is exactly 0.0 with a wide CI | The two versions win the same cases (McNemar p=1.0); the 14% regression cases are offset by 14% wins | Read the per-case diff, not the aggregate; the 14a report's "0 misses" re-run confirms the cache was faithful | ch 07 |
| A benchmark score differs from the one in the paper | Prompt format (0-shot vs 5-shot), sampling temperature, and harness version all move the number | Log the prompt with the data; the 6pp GSM8K swing (ch 11) is the case study | ch 11 |
| Re-running a recipe "should be cheap" but hits the LLM | A cache key changed (recipe path, prompt string, or data version) and the miss went to the network | 14a's quickstart proved 0 misses when the key was stable; pin the key components in the recipe's metadata | ch 12 |

## Exercises (3)

1. **Reproduce the A/B.** From `project/runs/`, run `just run 07_ab_answer_v2_vs_v1` and
   confirm the difference lands in [-0.117, +0.117]. Change nothing else. Time yourself:
   it should be ~5 minutes with the cache, ~10 minutes without.
2. **Find the 14% regression cases.** In `project/runs/07_ab_answer_v2_vs_v1/`, diff the
   per-case verdicts of v1 and v2. Write one paragraph on what kind of question v2 gets
   wrong that v1 gets right. (Hint: it's about multi-section retrieval — v2 pulls *more*
   context, which is better for recall but pulls in off-section text, which the judge
   marks as unsupported.)
3. **Write your own decision-guide row.** Pick one question your team would ask that is
   *not* in the table above. Add a row: Method, Cost, Known bias. Bring it to the next
   review. This is the skill this tutorial is trying to build.

## Where to go next

- **[index.md](index.md) — the full table of contents** — jump back to the chapter you want
  to re-read.
- **[Q&A.md](Q&A.md) — the questions that came up** — 12–15 questions with short answers and
  chapter pointers.
- **[project/](project/) — the code, the data, the recipes, the results** — everything in
  the tutorial is re-runnable from there.
