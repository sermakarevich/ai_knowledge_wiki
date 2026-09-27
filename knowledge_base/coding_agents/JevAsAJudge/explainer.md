> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | alphaXiv — In Plain Language
Imagine you have to grade thousands of AI answers every day.
Hiring the smartest (and most expensive) judge for every single grade gets costly fast.
This paper asks a practical question: can a cheap, no-frills judge handle the easy
grades on its own, and call in the expensive expert only when it feels unsure?

## What is this about?
Grading AI outputs with another AI — called "LLM-as-a-judge" — works well but is
expensive at scale, and the big judge's own sense of confidence is unreliable.
The paper tests a cheaper alternative as a first pass: TypeSafe JEV, a
decision-only judge that takes structured inputs plus a grading rubric and returns
a typed verdict with probabilities over the allowed labels.
It was tested against sixteen other judges, including the strongest comparator,
GPT-6 Astra, with blinded human adjudication to settle the right answers.
The headline result: on ordinary preference and evidence-grounded factuality, the
cheap judge lands within about three points of the top model at 0.36% of its fee.
On a 400-pair RewardBench sample of routine preference, JEV scores 92.2% versus
93.5% for GPT-6 Astra (a paired difference of −1.25 points).
But the gaps widen sharply on harder judgments: on JudgeBench, which requires
checking a step-by-step derivation, JEV scores 78.6% versus 93.1%.
On RM-Bench hard pairs, where the wrong answer is written elaborately and
persuasively, JEV scores 74.8% versus 94.6%.
The paper's fix is a cascade: accept the cheap judge's verdict when it is
confident, and escalate the uncertain cases to the stronger model.
A frozen cascade of this kind keeps about 99% of the strong judge's accuracy
at a lower fee.

## Why does it matter?
Anyone grading AI systems at scale faces the same trade-off: quality versus cost.
If every comparison needs the flagship model, evaluation bills explode.
This result sketches a middle path for routine work.
The cheap judge is nearly as good as the best model on everyday preference picks —
the kind of "which answer is better?" choice that fills most evaluation queues —
while costing a tiny fraction of the fee.
That makes large evaluation runs, frequent model comparisons, and continuous
quality checks far more affordable.
At the same time, the paper draws a clear boundary: derivation-checking and
smoothly written but wrong answers still need the strong judge.
Knowing where the cheap judge holds up and where it breaks down lets teams spend
their evaluation budget where it actually changes the verdict.
The cascade turns that boundary into a working rule instead of a vague worry.

## How does it work?
Think of the system as a junior grader with a honesty meter plus a senior grader
on call.
First, the junior grader (JEV) reads the two candidate answers and the rubric,
then outputs a verdict plus a probability for each allowed label.
Second, the system computes a confidence score, q: simply the largest probability
JEV assigned to any allowed label.
Third, it applies a threshold rule: if q is above the threshold, accept JEV's
verdict; if below, escalate to the stronger LLM and use its verdict instead.
For pairwise comparisons, JEV judges both presentation orders, the probabilities
are aligned to the same meaning, and averaged before the gate is applied.
Thresholds are not guessed — they are fitted on small pilot data and then frozen.
Per fallback model, the threshold is chosen on 96 pilot selection pairs
(64 from RewardBench plus 32 from JudgeBench), aiming for maximum coverage while
staying within two points of that fallback's own accuracy.
Invalid JEV outputs automatically defer to the fallback model.
The main evidence is a frozen offline test on 510 held-out extension preference
pairs that were not used for fitting.
At a threshold of 0.9, the JEV-to-GPT-6 cascade accepts 53.7% of pairs itself and
reaches 92.5% accuracy versus 93.1% for GPT-6 alone — about 99% — at 56.8% of
GPT-6's reported fee (62.2% under a conservative bound).
Supporting evidence comes from 990 base-order judgments: JEV's accuracy generally
rises across confidence bins, and GPT-6's advantage is concentrated in JEV's
low-confidence cases.
One caveat: on style-adversarial RM-Bench pairs, confidence is less effective at
flagging JEV's errors.

## Where can this be used?
Anywhere teams currently pay a flagship model to grade large volumes of outputs.
Routine preference ranking — picking the better of two responses during model
development or regression testing — is the natural first deployment.
Evidence-grounded factuality checks, where the answer is judged against provided
sources, are the other workload the paper supports.
Harder lanes work best as escalation targets: math or code derivations that must
be verified step by step, and comparisons where one answer is polished but wrong.
In an evaluation pipeline, the cascade becomes a triage layer: the cheap judge
clears the confident majority, and the expensive judge spends its budget on the
doubtful minority.
The same pattern fits continuous monitoring of a deployed assistant, where most
daily traffic is routine but a slice deserves expert review.
The key condition from the paper: each new workload and each new fallback model
needs its own locally validated threshold — a setting that worked elsewhere
cannot simply be copied over.

## Conclusions & takeaways
- A cheap decision-only judge can match a top-tier judge within about three
  points on routine preference and factuality at a fraction of the fee — but it
  trails badly on derivation-checking and style-adversarial judgments.
- Confidence (the top-label probability) is a useful ranking signal for routing:
  accept confident verdicts, escalate the rest.
- The frozen cascade is the proof point: roughly 99% of GPT-6's accuracy at a
  little over half its fee on held-out preference pairs.
- Confidence is not a certificate of correctness — it ranks cases well on average
  but can miss errors, especially polished-but-wrong answers.
- Thresholds are workload-specific and must be validated locally; a transferred
  policy (for example the frozen GPT-5.6 setting) can accept many cases yet lose
  several points of accuracy.
- Treat this as an empirical operating profile — a tested cost-accuracy trade-off
  for one setup — not a universal rule, since live latency and token savings were
  not measured.

## Jargon decoder
| Term | What it means in plain language |
|---|---|
| LLM-as-a-judge | Using one AI model to grade or compare the outputs of other models. |
| TypeSafe JEV | The cheap judge tested here: strict inputs and rubric in, a fixed-format verdict plus probabilities out. |
| Typed verdict | A decision restricted to a preset list of allowed labels, not free-form text. |
| Confidence score (q) | The highest probability JEV gives to any allowed label; higher means JEV claims more certainty. |
| Threshold (τ) | The cut-off line: above it the cheap verdict stands, below it the case goes to the expert. |
| Cascade / escalation | The two-stage setup: the cheap judge handles easy cases, the strong model handles the doubtful ones. |
| Fallback model | The stronger LLM (e.g. GPT-6 Astra) whose verdict is used whenever a case is escalated. |
| RewardBench / JudgeBench / RM-Bench | Standard test suites: everyday preference picks, derivation-checking, and tricky style-adversarial pairs. |
| Frozen offline test | The threshold is fixed on pilot data first, then scored untouched on fresh held-out pairs. |
| Paired difference | The head-to-head accuracy gap on the same items, here −1.25 points for JEV versus GPT-6. |
