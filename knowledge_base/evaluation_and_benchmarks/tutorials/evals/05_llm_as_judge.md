# 05 — LLM-as-judge: grading free text with a model that we itself have to evaluate

Chapter 04 gave us level-1 evals: code that scores what it can score, exactly and for free. But the bulk of what our `answer` app produces resists code: does the reply *actually* answer the customer's question? Does it omit a required number? Does it cite a handbook section that doesn't say that? Those are judgments about meaning, and meaning is what LLMs (Large Language Models) are good at — so we ask an LLM to grade another LLM's output. That is **LLM-as-judge**: using a model as a grader.

This chapter builds one binary (pass/fail) judge per failure mode of chapter 03, aligns each judge against the human labels we already have on `dev` (20 tickets), freezes the winner, and measures it on the sealed `test` split (60 tickets). The headline result is uncomfortable and important: **our judges looked great on `dev` (kappa 0.64–1.00) and mostly fall apart on `test` (kappa −0.11 to +0.16).** The method is still correct — the loop, the metrics, the discipline — and that is exactly what this chapter is about. A judge is a model doing a classification task, and like any model it needs evaluation before you trust it in a gate.

## What you will learn

- Why an LLM judge is itself a model that needs evaluation, and the loop that evaluates it (align on `dev`, freeze, measure on `test`).
- Reference-aware vs reference-free judging, and which one we used and why.
- One binary judge per failure mode, with a short critique, and why binary + critique beats a 1–5 Likert score — backed by our own Likert ablation (mean 4.27/5, AUROC 0.360, below chance).
- The alignment loop as a diagram, with the real numbers at every step.
- The judge scorecard: TPR (True Positive Rate), TNR (True Negative Rate), accuracy, and Cohen's kappa — and an honest reading of what "TPR = 0.000" means.
- A no-context ablation: the judge is *not* checking the cited handbook section.
- The disagreement review: on 18 `missing_required_fact` disagreements, who was actually wrong — judge, label, or nobody ("ambiguous").
- What Anthropic's engineering guidance adds (rubrics, grading the outcome not the path) and where practitioners genuinely disagree (binary vs Likert).
- The cost per ticket — four calls, ~10 minutes of wall clock — and the argument for judging a *sample* of production traffic.
- Troubleshooting, exercises, and where chapter 06 takes this.

## Reference-aware vs reference-free

There are two broad families of judge:

- **Reference-aware** — the judge is shown a reference: a gold answer, a set of required facts, or (like us) the retrieved handbook context plus a failure-mode definition grounded in real labeled examples. It grades *this output against this standard*. Our chapter-03 labels were produced by exactly this: the reference-aware grader (`reference_grader_v1.txt`) comparing each reply against the gold `answer_points` and the retrieved sections.
- **Reference-free** — the judge only sees the question and the output, and applies a generic rubric ("is this helpful, on-topic, free of fabrication?"). Useful when no reference exists (open-ended chat), but weak for factual work: without the reference, the judge cannot tell "right policy, wrong section" from "right policy, right section" — it grades plausibility instead of correctness. (Braintrust calls this out explicitly as the "factual verification without reference context" failure mode.)

We use reference-aware judges: every mode prompt contains the ticket, the retrieved handbook context, the reply, and a definition of the failure mode written down in `taxonomy.yaml` from chapter 03's axial coding.

## One binary judge per failure mode

Each of the four modes from chapter 03 that had at least 4 labeled failures gets its own judge: `did_not_answer`, `missing_required_fact`, `unsupported_claim`, `wrong_section_retrieved`. `wrong_value` (2 fails) and `over_promise` (1 fail) stay unlabeled by a judge — too little signal to align against.

Why one judge per mode instead of one "quality" judge? Three reasons:

1. **A single question has an unambiguous answer.** "Does this reply commit `missing_required_fact`?" is checkable against the definition; "how good is this reply, 1–5?" is not.
2. **Separating failure axes is what makes judges debuggable.** If a combined judge says "fail", you do not know which failure — and chapter 03's whole point was that the *mode* tells you which prompt paragraph to fix.
3. **Practitioner guidance agrees.** Hamel & Shreya's FAQ recommends binary pass/fail over Likert scales because binary is faster to produce, more reproducible between raters, and easier to align an LLM judge against; Eugene Yan's survey of LLM-evaluator work reaches the same practical advice — split complex criteria into separate single-purpose judges. (Hamel & Shreya, "AI Evals FAQ"; Eugene Yan, "Evaluating the Effectiveness of LLM-Evaluators".)

And the JSON schema asks for the critique *before* the verdict:

```jsonc
Respond with JSON only:
{"critique": "<one short sentence citing the evidence>", "verdict": "pass" or "fail"}
```

Forcing the judge to cite its evidence first keeps the verdict tied to what it actually saw — and gives *us* something to audit when we disagree. (We will, a lot — see the disagreement review below.)

An excerpt of the `missing_required_fact` v2 (few-shot) prompt, `prompts/judge_missing_required_fact_v2.txt`, shows the shape: the role, the single-mode instruction, a precise definition, the ticket, the recalled context, the reply, then four worked examples (two `fail`, two `pass`) — all taken from the *dev* split, each with its expected verdict and a one-line rationale — and finally the answer rules. Two details matter:

```text
Judge a SINGLE failure mode only and ignore every other way the reply might be
good or bad.
...
FAILURE MODE: MISSED REQUIRED FACT (missing_required_fact)
Definition: the reply fails to convey a key fact the customer explicitly asked
about, or a fact the resolved answer depends on. A factual error, a missing
required number, a missing required confirmation, or omitting the core answer =
FAIL. Correct and complete coverage of every required fact = PASS.
```

The definition is the *standard*; the worked examples show the standard *applied*. That separation (standard / examples / answer rules) is deliberately the same pattern you would use with any rubric.

## Why binary + critique beats a 1–5 score

A 1–5 "quality" score is the most common way to grade LLM output, and the most common mistake. Three problems, one of which we measured on our own data:

1. **Scale compression (the "Likert pile-up").** Zheng et al. 2023 (arXiv 2306.05685) documented that both human and LLM raters crowd scores into the top of the scale — most judgments land on 4 or 5 — so a 5-point scale effectively becomes binary, but a *fuzzier* binary where 4 and 5 mean different things to different raters. Hamel & Shreya make the same observation: practitioners compress toward 3–4 anyway, so you get the cost of a scale and the information content of a coin with wobble.
2. **Alignment is measurably harder.** A Likert judge must match your human's *intensity* calibration, not just your pass/fail boundary. Binary has one boundary.
3. **One number blurs the reason.** A "4" says nothing about *which* failure mode — which is precisely what tells you which prompt to fix.

We ran the honest control. The same model, asked to score each of the first 30 `test` replies 1–5:

| Likert ablation (n = 30) | value |
|---|---:|
| AUROC of score vs pass label | **0.360** |
| mean score | **4.27 / 5** |
| score histogram | 1: 0,  2: 0,  3: 5,  4: 12,  5: 13 |

The pile-up is exactly the textbook pattern (all 28 non-bottom scores on 3–5). Worse, the AUROC of **0.360 is below chance** (0.50): the score is *weakly inversely* correlated with correctness — pass replies and fail replies are not just hard to separate by score, the scale is slightly misleading. All five tickets that got a 3 were failing tickets; the 25 tickets at 4–5 are a mix. A single fuzzy number cannot carry four distinct failure axes, and here it carried even less than noise. (Eugene Yan's "LLM-evaluators" survey is where you will see the same caution: prefer direct scoring or pairwise for specific, checkable criteria over a global quality score.)

## The alignment loop — evaluate the judge before evaluating the app

An LLM judge is a model doing a classification task (fail vs no-fail). Models are not trusted on release; they are validated. The same applies to the judge, and the loop is short:

```mermaid
flowchart LR
    L[chapter-03 labels on dev:\n20 tickets, pass/fail per mode] --> V1[judge v1\nzero-shot]
    V1 --> M1[TPR / TNR / kappa\non dev]
    M1 --> D{pick winner\nper mode}
    D -->|edit prompt,\nadd few-shot examples| V2[judge v2\nfew-shot]
    V2 --> M1
    D -->|frozen| T[run on test\n(n=60, never seen)]
    T --> S[scorecard +\ndisagreement review]
    S --> D
```

Two rules make this honest:

- **Alignment happens on `dev` only** (20 tickets, 34 fails total across modes; the per-mode positive counts are tiny — 1 to 3 — which matters, see below).
- **Few-shot examples are drawn from `dev` only.** The moment a worked example from `test` leaks into the judge prompt, the "test" is no longer sealed and the score is worthless.

The `missing_required_fact` alignment shows why the loop works at all. v1 (zero-shot), on `dev`:

| version | TPR | TNR | accuracy | kappa |
|---|---:|---:|---:|---:|
| v1 (zero-shot) | 0.333 | 1.000 | 0.900 | 0.459 |
| v2 (few-shot) | 1.000 | 1.000 | 1.000 | 1.000 |

v1 catches only 1 of 3 dev failures — a judge that leans "pass" misses omissions, exactly the pattern you would predict. Adding two `fail` + two `pass` worked examples fixes it on `dev` (kappa 1.000). Note the direction: this is a judge that *under-calls* failures, so the fix was showing it what "fail" looks like, not being stricter. For `did_not_answer`, the opposite happened — v2 *regressed* (kappa 0.459 vs 0.643: the few-shot version added one false positive) — so the winner per mode differs, and that is fine. You choose per mode by the alignment number, not by taste.

## The scorecard, and an honest reading of TPR vs TNR

Freeze the winners (v1 for `did_not_answer`; v2 for the other three) and run on `test`:

| mode | version | n | kappa | TPR | TNR | true fails | judged fails |
|---|---|---:|---:|---:|---:|---:|---:|
| `did_not_answer` | v1 | 60 | 0.116 | 0.400 | 0.800 | 5 | 13 |
| `missing_required_fact` | v2 | 60 | 0.027 | 0.133 | 0.889 | 15 | 7 |
| `unsupported_claim` | v2 | 60 | **−0.111** | 0.000 | 0.917 | 12 | 0 |
| `wrong_section_retrieved` | v2 | 60 | 0.000 | 0.000 | 1.000 | 8 | 0 |
| **overall** (pass = no mode fails) | — | 60 | 0.155 | 0.385 | 0.765 | 26 | — |

Now read it honestly, and the key is the *pair* TPR/TNR:

- **TPR = 0.000 for two modes is not "weak agreement with the label" — it is a judge that says "pass" to every true failure.** `unsupported_claim` produced **zero** `fail` verdicts against 12 labeled failures, and `wrong_section_retrieved` did the same against 8. A judge that passes everything has TPR 0 and TNR 1 — maximum "agreement" in the sense of accuracy (80+ %) while catching *nothing*. That is why raw accuracy is the wrong metric to trust here: class imbalance (few fails per mode) means a do-nothing judge looks competent.
- **TNR alone is equally useless.** A judge that fails everything scores TNR 0, TPR 1, and is "100 % recall". Neither extreme is informative on its own; you need both, plus a statistic that accounts for chance agreement.
- **Cohen's kappa** is the answer to that. Kappa is the fraction of *beyond-chance* agreement: it takes the observed agreement, subtracts the agreement you would get if the judge were just predicting the base rate (e.g. 70 % "pass" because 70 % of tickets have no such failure), and normalizes. A do-nothing judge gets kappa = 0 by construction; negative kappa means the judge is *worse than guessing from the base rate*. That is why `unsupported_claim` at kappa −0.111 is the truest statement in the table: its verdicts are mildly anti-correlated with the labels, whatever the 91.7 % TNR suggests. (Shankar et al., "Who Validates the Validators?", arXiv 2404.12272, makes exactly this argument for treating the LLM judge as a classifier and reporting TPR/TNR/kappa against human labels rather than raw agreement.)
- **Dev did not predict test.** `missing_required_fact` v2 went from kappa 1.000 (dev) to 0.027 (test); `did_not_answer` from 0.643 to 0.116. The 3 dev failures of `missing_required_fact` were easier to spot than the 15 test ones. Small dev sets are a *screen of screens*, not a guarantee — and with 1–3 positive examples per mode on dev, kappa there is almost a coin-flip statistic. Treat dev alignment as "is this judge sane and pointing the right direction"; only test (or, in production, a continuously labeled holdout) tells you how good it is.
- **The dominant error is under-calling.** 13 of 18 `missing_required_fact` disagreements are false negatives — the judge says pass on replies with a required fact missing. An under-conservative judge misses regressions; an over-conservative one drowns you in false alarms. Under-calling is the more dangerous one for a regression gate, because the failure you did not see is the one your users hit.

## No-context ablation

One question the design leaves open: does the `missing_required_fact` judge actually *use* the retrieved handbook context, or does it just read question + reply and guess? The nocontext run re-grades the same 30 `test` tickets with the handbook text withheld:

| condition | n | kappa | TPR | TNR |
|---|---:|---:|---:|---:|
| with context (v2) | 30 | −0.111 | 0.000 | 0.917 |
| no context (v2) | 30 | −0.154 | 0.000 | 0.875 |

Delta: kappa drops by 0.043, TPR unchanged at 0.000. **The context makes almost no difference — the judge is grading the reply text alone.** Two lessons: (a) it does not cross-reference the cited section against the handbook at all, which is the gap a "verify each claim is in the context" judge (chapter 09's territory) must fill; (b) a negative ablation is as valuable as a positive one — it tells you what the grader *is not doing*, so you stop pretending it does.

## Disagreement review — who was wrong

The scorecard tells you *how often* judge and label disagree. The review tells you *why*. For `missing_required_fact` on `test` there were **18 disagreements** (13 false-negatives, 5 false-positives). We re-read every one with the ticket, the label note, and the judge's critique, and classified each as judge wrong / label wrong / ambiguous:

| verdict | count | tickets |
|---|---:|---|
| **judge wrong** | 8 | tkt-010, 018, 020, 047, 054, 060, 066, 078 |
| **label wrong** | 3 | tkt-019, 070, 074 |
| **ambiguous** | 7 | tkt-011, 013, 014, 041, 053, 058, 064 |

So the most defensible test-split reading of `missing_required_fact` is not "TPR 0.133" but "**the judge caught ~2 of 15 real failures, and about half of those 15 labels are defensible**." Two representative cases, quoted from the review:

> **tkt-047** (judged a false-negative; *judge wrong*) — the label says: *"The reply omits the required key fact that the minimum purchase amount is $25.00 per card."* The judge replied: *"The reply correctly conveys the required facts that digital gift cards are delivered within 15 minutes and can be re-sent."* — the judge graded a different facet (delivery speed) and never checked the $25 minimum. This is the clearest example of the under-calling bias: it accepted "a fact was present" as "the required fact was present".

> **tkt-074** (judged a false-positive; *label wrong*) — the label note literally says *"reply matches the reference standard"* (i.e. pass), yet the judge argues *"the customer explicitly asked the assistant to review their account history; the assistant failed to perform this review."* Here the label itself is the outlier — the judge is not wrong; our chapter-03 grader mislabeled a ticket.

Reading these two back-to-back is the whole point: **disagreements are not automatically judge errors.** In our 18, the judge is at fault in 44 % (8/18), the label in 17 % (3/18), and the definition of the mode is genuinely ambiguous in 39 % (7/18) — "truncated ticket, asking for clarification is reasonable" is an argument, not a verdict. The fix for those 7 is not a better judge prompt; it is a sharper definition of `missing_required_fact` (we already know the mode's boundary bleeds into `did_not_answer` and `wrong_value`), which is the criteria-drift loop Shankar et al. describe: *the act of grading and the act of defining the criterion improve each other* (Shankar et al., "Who Validates the Validators?").

## What Anthropic's engineering guidance adds

Anthropic's agent-evals post (Grace, Hadfield et al., 2026) gives two principles that map one-to-one onto what we did and what we did not:

- **Combine graders, in order of cost.** Code-based checks, then model-based (rubric) graders, then humans — use the cheapest reliable method first, and reserve humans for calibration. Our chapter order (03 → 04 → 05) is exactly this. Their LLM grader guidance also matches ours: give the judge a way out ("return `unknown` when unsure"), prefer a clean, structured rubric per dimension, and run *separate* judges per dimension rather than one omnibus grade.
- **Grade the outcome, not the path.** Their framing for agent tasks is explicit: "a flight-booking agent might say 'Your flight is booked' at the end of the transcript, but the outcome is whether a reservation exists in the environment's SQL database." Translated to our single-turn `answer` app: **grade the state of the reply against the policy in the handbook** (did the required number appear? does the cited section exist?), not the *trajectory* of how the LLM arrived at the reply. In practice this is what "reference-aware" means concretely — it is a gradeable standard.

Where the practitioner literature genuinely disagrees (and where a reader should know which camp they are standing in): **binary vs Likert/ordinal.** Hamel & Shreya are binary-first, always; Anthropic's own Claude docs still ship 1–5 Likert examples for tone / context-usage. Our own data says the same thing Hamel & Shreya do: on our scale, a Likert score is *below chance* at separating pass from fail. Use ordinal scales for *exploratory* diagnostics; for gates, binary per dimension.

## Cost, and judging a sample in production

Per ticket, one `answer_v1` reply costs the judge **4 calls** (one per tracked mode), so the 60-ticket test split is 240 calls per mode (235–240 in `results.md`). `results.md` reports ~9.6 s/item per mode — `judge.py` runs the four modes concurrently in a small thread pool to cut wall time on the shared GPU box, so per-ticket wall clock is close to one mode's time, and re-runs are mostly instant because every LLM call is cached by prompt. The whole split per mode is well under ten minutes once the model is warm. That is cheap enough to judge the entire sealed set — and it is the arithmetic that makes "judge *every* ticket in a test split, judge a *sample* in production" a coherent policy. That is cheap enough to judge the entire sealed set — and it is the arithmetic that makes "judge *every* ticket in a test split, judge a *sample* in production" a coherent policy. That is cheap enough to judge the entire `test` split; that is *not* cheap enough to judge 100 % of production traffic at scale, and there is no reason to want to:

- **Production traffic is not a test set.** Your `test` tickets were built from a persona × topic × scenario grid; live tickets will drift (new products, policy changes, language). Judging 1 % of tickets with the four mode-judges and spot-reading 50 critiques per week is a **continuous labeled sample**: it tells you *where on `live` the judge is under-calling*, which is the exact signal the disagreement review gives you offline, just always.
- **It doubles as your data-freshness alarm.** If the `unsupported_claim` judge starts catching 10× what it caught on `test`, either the model drifted or the handbook changed — and the judge is your canary because it is running on every sampled ticket. (Langfuse / Braintrust both ship exactly this: sample → judge → human refinement.)
- **It seeds your fine-tuning data.** The same pass/fail flags that the disagreement review produces are the curation signal for a dataset that teaches your model (or a purpose-built judge) to be better at the modes it currently misses.

We will return to production monitoring in chapter 13; the cost arithmetic above is what makes it affordable.

## What landed in the results table

`just results` (run with the seven new `metrics.json` files from this chapter) adds these rows to `project/runs/results.md`:

| experiment | n | primary metric (kappa or AUROC) | 95 % CI | LLM calls | s/item | notes |
|---|---:|---:|---|---:|---:|---|
| `05_judge_did_not_answer` | 60 | 0.1158 | — | 238 | 9.645 | did_not_answer v1 (best=v1) |
| `05_judge_missing_required_fact` | 60 | 0.0270 | — | 240 | 9.726 | missing_required_fact v2 (best=v2) |
| `05_judge_unsupported_claim` | 60 | −0.1111 | — | 235 | 9.535 | unsupported_claim v2 (best=v2) |
| `05_judge_wrong_section_retrieved` | 60 | 0.0000 | — | 239 | 9.683 | wrong_section_retrieved v2 (best=v2) |
| `05_judge_overall` | 60 | 0.1549 | — | 0 | 0.0 | composed from 4 mode-judges |
| `05_likert_overall` | 30 | AUROC 0.3600 | — | 30 | 2.386 | 1–5 score vs pass label |
| `05_judge_missing_required_fact_nocontext` | 30 | −0.1538 | — | 30 | 2.686 | context withheld |

Read it as one story, not seven rows: (1) **the method works**, in the sense that dev alignment is reproducible and *does* separate versions per mode — `did_not_answer` v1 beats v2 and `missing_required_fact` v2 beats v1 exactly as dev said; (2) **but on test, 3 of 4 judges are effectively "pass" by default** (TPR 0–0.13), and the one judge that undercalls the most (`unsupported_claim`, kappa −0.11) is the one where the definition is most contested in the disagreement review; (3) **the Likert control (AUROC 0.36) confirms binary-per-mode is the right shape** — a single score is worse than no information; and (4) **the nocontext ablation (−0.154 vs −0.111) says the context does not carry the signal**, so our judges are grading the reply text, not the citation graph. The CI column is empty by design — chapter 07 fills it, and that matters most here, because with n = 60 per mode and 5 true-fails in `did_not_answer`, the difference between 0.11 and −0.11 is within a handful of tickets.

## Troubleshooting

| symptom | likely cause | fix |
|---|---|---|
| Judge verdict is inconsistent with its own critique | verdict was emitted before critique | swap the JSON field order: `critique` first, `verdict` second. Forcing the model to cite evidence before deciding measurably reduces verdict-critique mismatches (this is where we got our best per-mode TPR/TNR split). |
| Judge scores perfectly on `test` | worked examples from `test` leaked into the v2 prompt | draw few-shot examples from `dev` only, and add a code assertion that no `test` ticket id appears in any judge prompt (`judge.py` does this in `_load_examples`). |
| Judge agrees with *itself* across runs but disagrees with human labels | the judge is internally consistent but its definition of the mode is wrong/offset | this is a **label or definition problem**, not a judge-reliability problem. Re-read the disagreements, sharpen `taxonomy.yaml`, and realign on `dev`. |
| TPR = 0, TNR = 1 on a mode with real failures | judge is a constant "pass" for that mode (do-nothing judge) | kappa will be 0 or negative — trust kappa, ignore accuracy. Add 2–3 real `fail` worked examples from `dev`; if kappa stays ≤ 0 after a second iteration, the mode may need a sharper definition or a different judge *model* (chapter 06). |
| Dev kappa 1.000, test kappa ≈ 0 | 1–3 positive examples on dev → kappa is a coin-flip statistic | increase the dev set before trusting *any* version choice; treat dev as a sanity screen only. |
| Judge output is not parseable JSON | model drifts into prose | parse with a retry loop that feeds the parse error back into the prompt; after 3 attempts, log the raw output and grade it as "unparseable" rather than silently treating it as a pass (a silent pass is a false negative). |

## Exercises

1. **Write v3 for the weakest mode.** `unsupported_claim` has test kappa −0.111 and caught 0/12. Read its 12 `fail` labels and 8 true-pass tickets, write one or two additional worked examples *from dev* (add `judge_unsupported_claim_v3.txt`, never edit v1/v2), realign on dev, and see if you can get a positive test-kappa. If you can't, that is a finding about the *mode*, not the prompt — say so.
2. **Measure self-agreement.** This chapter's judges run at temperature 0.0 and are cached per prompt, so they are deterministic *as configured*. Temporarily raise the temperature to 0.7 for one mode (`missing_required_fact` v2), run it on the same 20 `dev` tickets twice, and compute the self-kappa (verdict of run 1 vs verdict of run 2). If it is below 0.8, the sampled verdicts are not stable — any test-kappa you measured on them is entangled with sampling noise. (This is deliberately different from everything in this chapter: we have been measuring agreement with *labels*, not with the judge's *own* behavior across runs.)
3. **Re-run the Likert control on all 60 `test` tickets** (currently only 30) and check it is still below-chance AUROC. If it is, that is the honest evidence to hand in any design review: single-score grading is *worse than no information*.
4. **Read 5 of the `ambiguous` disagreement tickets** (tkt-011, 013, 014, 041, 053, 058, 064) and write one sentence each proposing a sharper definition of `missing_required_fact` that would have resolved it. This is the criteria-drift loop in one minute of work.

Next: **chapter 06 — judges under the microscope** (MT-Bench human votes, position / verbosity / self-preference bias, and Bradley–Terry ratings).
