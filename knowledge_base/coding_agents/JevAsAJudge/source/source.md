# JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | alphaXiv
> PDF: https://www.alphaxiv.org/abs/2609.26550
Source: https://www.alphaxiv.org/abs/2609.26550
Kind: article
Fetched: 2026-09-25T09:16:49.685314+00:00
Tool: urllib
Topic: coding_agents

JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | alphaXiv

AbstractPaper

## Abstract

LLM-as-a-judge enables evaluation across diverse tasks, but inference cost and confidence reliability become critical at scale. We study whether a decision-only judge can provide an economical first pass and identify when stronger evaluation is needed. Comparing jev-as-a-judge with sixteen generative and reward-model judges, with blinded human adjudication, we find it within three percentage points of a state-of-the-art LLM judge, our strongest comparator, on ordinary preference and evidence-grounded factuality[p4] at 0.36% of the comparator's fee. Larger gaps arise when judgments require checking a derivation or resisting an elaborately written wrong answer.[p5]On several benchmarks, JEV's gap to this comparator is concentrated in low-confidence decisions.[p8] A frozen cascade that accepts confident verdicts and escalates uncertain ones retains 99% of the comparator's accuracy at lower cost.

View more

View Paper

36

Save

Cite

## AI Overview

Copy

Evaluating model answers is repeated work. People can assess open-ended answers in context, but human review is difficult to scale across many tasks, answers, and model revisions. The paper asks whether a cheaper judge can handle routine decisions and reserve a stronger model for the uncertain ones.

The authors' approach has two steps. A first judge returns a verdict along with probabilities over the allowed labels. When its confidence is high, its verdict is used. When it is uncertain, the case goes to a stronger LLM. In a frozen, offline test, this policy kept roughly 99% of the stronger judge's accuracy at a fraction of its fee. That result is specific to the tested workload and is not a guarantee.

## A cheap first pass, with limits

The first judge is TypeSafe JEV. It takes structured inputs and a rubric, then returns a typed verdict and probabilities over the allowed labels. The comparison is between complete configurations. JEV is proprietary, and this is not a compute-matched architectural comparison. The authors frame the work as an empirical test of accuracy, confidence, and operating cost together. A typed probability output by itself does not establish calibration.[p2]

Ordinary preference. On the 400-pair RewardBench sample, JEV scores 92.2% and GPT-6 Astra scores 93.5%. The paired difference is −1.25 percentage points, with a 95% cluster interval of [−3.8, 1.5].[p4]

Harder cases. Here a cheap first pass is not enough. On JudgeBench, JEV scores 78.6% against GPT-6's 93.1%. RM-Bench's hard pairs are ones where the rejected answer is more elaborately written. On these, JEV scores 74.8% against GPT-6's 94.6%. These comparisons support escalation for derivation-checking and misleading style. They do not support a claim that all difficult tasks fail in the same way.[p5][p5]

## Confidence as a routing signal

The confidence value, qqq, is the largest probability JEV assigns to any allowed label. The routing rule works as follows:

If qqq is above a threshold, the system accepts JEV's verdict.

Otherwise, it asks a stronger LLM and uses that verdict instead.

In pairwise comparisons, the frozen policy judges both candidate orders. It aligns the probabilities to the same semantic response and averages them before applying the gate.

The threshold is selected on pilot data and is not assumed to transfer universally.[p9]

Rubric and candidate responses enter JEV, which produces a decision and a confidence signal. The gate either accepts the decision or escalates to a stronger LLM, and both paths yield a final verdict. For pairwise tasks, the gate uses order-aligned, averaged probabilities and a workload-validated threshold. This is a mechanism schematic, not a result plot.

The case for escalation comes from how JEV's accuracy varies with its confidence. On the 990 base-order judgments, JEV accuracy generally rises across confidence bins. The paper reports that GPT-6's advantage is concentrated in JEV's less-confident cases.[p8] In these workloads, confidence is a useful ranking signal, but it is not a certificate of correctness. On style-adversarial RM-Bench pairs, JEV's confidence is less effective at identifying errors.[p9]

## What the frozen test shows

The main cascade evidence comes from a frozen, offline test.

How the threshold was chosen. For each fallback model, the threshold was selected on 96 pilot selection pairs (64 RewardBench and 32 JudgeBench). The selection rule sought maximum coverage while keeping selection accuracy within two points of that fallback. Invalid JEV outputs defer to the fallback.

How it was evaluated. The two-order policy was then evaluated on 510 extension preference pairs not used for fitting.[p9]

Result. At τ=0.9\tau=0.9τ=0.9, the JEV→GPT-6 cascade accepts 53.7% of pairs. It reaches 92.5% accuracy versus 93.1% for GPT-6 alone. Its fee is 56.8% of GPT-6's reported fee, or 62.2% under the conservative bound. This is roughly 99% of GPT-6 accuracy, not a guarantee.

Limits. The thresholds are workload-specific, and one policy does not transfer as intended. The frozen GPT-5.6 policy, for example, accepts 81.0% at τ=0.7\tau=0.7τ=0.7 but loses 2.35 points. Live sequential latency was not measured, and the measurements do not establish a reduction in generated tokens or live cascade latency.[p9]

The established contribution is an empirical operating profile of a cheap, decision-only judge paired with confidence-based escalation. JEV is close to GPT-6 on ordinary preference and clearly weaker on demanding judgments. On a specified held-out preference test, routing its uncertain cases upward preserved most of the stronger judge's accuracy at lower fee. The main boundary is that the threshold must be validated locally for each workload and fallback.

## Audio

JEV-as-a-Judge: Accept When Confident, Escalate When Unsure

0:00 /--:--

JEV-as-a-Judge: Accept When Confident, Escalate When Unsure

1x

Transcript

## Similar papers

A Survey on LLM-as-a-Judge19 Oct 2025Improving LLM-as-a-Judge Inference with the Judgment Distribution26 Sept 2025Leveraging LLMs as Meta-Judges: A Multi-Agent Framework for Evaluating  LLM Judgments23 Apr 2025Evaluating Judges as Evaluators: The JETTS Benchmark of LLM-as-Judges as  Test-Time Scaling Evaluators21 May 2025Does Context Matter? ContextualJudgeBench for Evaluating LLM-based  Judges in Contextual Settings19 Mar 2025

Show moreShow less

When AIs Judge AIs: The Rise of Agent-as-a-Judge Evaluation for LLMs05 Aug 2025Jagged Judges: Epistemic Stability Under Perturbation, Pressure, and Persistence21 Aug 2026Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges18 Aug 2025Replacing Judges with Juries: Evaluating LLM Generations with a Panel of
  Diverse Models01 May 2024Do Before You Judge: Self-Reference as a Pathway to Better LLM Evaluation24 Sept 2025

## Discussion

Comment

Sign in to save
