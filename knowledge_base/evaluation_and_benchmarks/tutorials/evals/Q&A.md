# Q&A

Short answers to the questions that came up while building this tutorial. Pointers
(`ch NN`) lead to the chapter where the detail lives.

## Core methods

**Q: How do I know which metric to use?**
Ask which question the metric answers, before asking which number it reports. "Is this
answer *structurally* broken" is a rule-based question. "Is it *supported* by the context"
is an NLI question. "How would a human read it" is an LLM-judge question. The same answer
gets very different scores from each because each of them is answering a different
question. The decision guide in ch 14 maps the question to the method, the cost, and the
known blind spot.

**Q: Rule-based checks are free. Why not just use those?**
They are cheap but brittle. In this tutorial the rule-based triage hit 11.7% of the bad
answers — plausible, well-formed, wrong-content answers slipped right through. Free is a
great adjective for a *first* filter; it doesn't make it a *complete* one. Layer on top:
NLI, then LLM-judge, then your own scorecard. (ch 04, ch 05)

**Q: Why does the embedding similarity score look so uninteresting (0.4–0.5 band)?**
`nomic-embed-text` normalizes to the unit sphere, so distances are compressed; the gap
between "good" and "wrong" answers is small in that space. Use AUC instead — 0.827 in this
run — because AUC is order-based and doesn't care about the absolute distance values. (ch 04)

**Q: What is kappa, and why is 0.54 bad?**
Kappa measures agreement beyond chance. 1.0 is perfect, 0.0 is chance. The common bar for
a "trustworthy judge" is ~0.6. This run's judge agreed with the dev-set reference
judgements at 0.54 — below the bar. That doesn't mean the judge is useless; it means that
for the *unsupported-claim* criterion, it's about as consistent as a coin flip that's
slightly biased. (ch 05)

**Q: Is LLM-as-judge just "asking an LLM to grade an LLM"?**
Yes, and that's the whole point — it's *your* scorecard, run by a model. The judge
(`qwen3.8:27b`) reads the same prompt as your dev-set reference judgements, and you verify
its agreement (kappa). It's not a magic number; it's a model you've measured. (ch 05, ch 06)

## Version comparison

**Q: The A/B difference is 0.0. Which version is better?**
You can't say the answer quality is different — the interval [-0.117, +0.117] contains 0.
What you *can* say: v2 is better at retrieval (recall/nDCG in ch 08) and about the same
on the answer itself; it pulled in more context, which helped recall but also introduced
off-section text that the judge flagged as unsupported. (ch 07)

**Q: What's the detection floor, and why does it matter?**
With this many answers (23 in the dev set, 100 in the A/B), the bootstrap power table in
ch 07 says you can only guarantee detecting a difference larger than ~24 percentage
points. If your real regression is 3 points, you're below the floor — you need more data,
not a fancier test. (ch 07)

**Q: Why use three different tests (bootstrap, Wilson, McNemar)?**
They answer three different questions: bootstrap → "how much would this score wobble on a
different sample"; Wilson → "what's the honest interval around this point estimate";
McNemar → "does each version win its own cases, or does v2 win where v1 is weak and lose
where v1 is strong?" One is a stability check, one is a calibration check, one is
per-case. You need all three. (ch 07)

## Benchmarks and frameworks

**Q: Why does the same model get different benchmark scores depending on the prompt?**
GSM8K: 0-shot 0.686, 5-shot 0.746 on `qwen3.8:27b` — same weights, 6 points moved.
Prompt format is a hyperparameter, not a formatting choice. Log the prompt with the data;
your "model score" is a (model, prompt, harness) tuple, not a model property. (ch 11)

**Q: Why do off-the-shelf benchmarks disagree with my own evaluations?**
They measure different things. IFEval tests instruction-following; your helpdesk judge
tests *grounded answer quality*. Both are real, both are valid, and both are answering
different questions. A model that scores high on IFEval can still give you wrong answers
in your domain. (ch 11, ch 04)

**Q: What did RAGAS / DeepEval actually add?**
They gave you a second opinion: RAGAS context relevance 0.855 vs faithfulness 0.737
— it split the "retrieval good, answer worse" story the hand-rolled judge told. That
agreement is evidence; the *blend* (one number hiding two) is the trade-off. (ch 08)

**Q: Is the CI gate (ch 13) a magic "no regressions" signal?**
No. It passes on `delta < 0.03` against the baseline (0.70). It does not pass on
"higher." It's a tripwire for *large* regressions — with the 24-point detection floor
from ch 07, a 3-point regression slips through. It's a floor, not a ceiling. (ch 13)

## Practical

**Q: How much does this cost per run?**
Rule-based: free (cached). LLM-as-judge: 121 calls × ~0.0003 USD ≈ 0.036 USD for the full
A/B. Benchmarks: whatever the LLM API costs for the benchmark corpus. The 14a quickstart
re-ran everything from the local cache with zero LLM calls — the cache is your cost
control. (ch 07, ch 12)

**Q: What if the judge's JSON parse fails?**
`qwen3.8:27b` emitted a trailing comma or a code fence around the JSON once. The fix is a
retry that strips code fences and re-asks; with the cache in place, retries are free. (ch 05)

**Q: How do I know a recipe is actually reproducible?**
Run it twice and diff the outputs. 14a did exactly this: every recipe rebuilt from cache,
zero LLM calls, byte-identical `just results`. If the cache key includes the recipe path,
the prompt string, and the data version, reproducibility is a property of the harness, not
a hope. (ch 12)
