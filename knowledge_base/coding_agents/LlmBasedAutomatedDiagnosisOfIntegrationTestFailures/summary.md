# LLM-Based Automated Diagnosis Of Integration Test Failures At Google

**Paper:** [LLM-Based Automated Diagnosis Of Integration Test Failures At Google (Ziftci et al., 2026)](https://arxiv.org/abs/2604.12108)

## Human Readable TL;DR

Imagine you're a mechanic, but instead of one car, you have to figure out why a whole convoy of trucks broke down -- and the only clue is thousands of pages of mixed-up driver logs from every truck. That's what engineers at Google face when their big software tests fail. This paper describes a tool called Auto-Diagnose that uses an AI assistant to read through all those messy logs, figure out what went wrong, and post a short explanation right where engineers are already working. It got the answer right about 90% of the time and is now used across all of Google.

## TL;DR

Auto-Diagnose is an LLM-based tool deployed at Google that automatically diagnoses integration test failures by analyzing multi-component, multi-datacenter log streams. It uses Gemini 2.5 Flash with structured step-by-step prompting and strict negative constraints to produce root cause summaries with relevant log line citations. A manual evaluation on 71 real-world failures showed 90.14% accuracy, and a Google-wide deployment across 52,635 distinct failing tests found only 5.8% of user feedback rated it "Not helpful", ranking it #14 in helpfulness among 370 tools in Google's code review system.

---

## Problem & Motivation

Integration test failures at Google produce massive, unstructured, heterogeneous log output -- the median failing test generates 16 log files and 2,801 log lines across multiple data centers, processes, and threads. A Google-wide developer survey (6,059 respondents) identified diagnosing these failures as a top-five complaint, with developers often spending over an hour (sometimes over a day) per failure. Existing automated debugging and LLM-based repair research has focused almost exclusively on unit tests or small-scale scenarios, leaving the unique challenges of integration testing -- multi-component interactions, distributed logs, complex environments -- largely unaddressed.

---

## Main Original Ideas

1. **Auto-Diagnose system** -- A fully automated, LLM-based diagnosis tool specifically designed for integration tests at scale. It joins logs from all components, data centers, and threads into a single chronological stream and produces concise root cause summaries with cited log lines.

2. **Structured multi-step prompt engineering with negative constraints** -- The prompt uses a guided step-by-step reasoning chain (8 steps) with strict rules: the model must not speculate when logs are missing, must not make infrastructure assumptions, and must only use logs from the failing component when identifiable.

3. **In-workflow integration via Critique** -- Diagnoses are posted as structured annotations directly inside Google's code review system, providing contextual, timely assistance without requiring developers to leave their workflow.

4. **Log pre-processing pipeline** -- Logs from all data centers, processes, threads, and log levels (INFO+) are collected, joined, and sorted by timestamp into a single tractable stream before LLM consumption.

5. **Production-scale empirical evaluation** -- Combines a controlled manual evaluation (71 failures, 3 expert evaluators) with large-scale deployment metrics (224,782 executions, 22,962 developers) and qualitative interviews -- unusually rigorous for an industrial LLM tooling paper.

---

## Key Findings

### Manual Evaluation (71 failures)

| Metric | Value |
|--------|-------|
| Failures evaluated | 71 (randomly sampled) |
| Accurate diagnoses | 64/71 (**90.14%**) |
| Failed due to missing test driver logs | 4 |
| Failed due to missing SUT component logs | 3 |

The 7 inaccurate cases were caused by infrastructure bugs (logs not saved on crashes), not LLM reasoning errors.

### Production Deployment (Google-wide, since May 2025)

| Metric | Value |
|--------|-------|
| Code changes processed | 91,130 |
| Distinct developers | 22,962 |
| Distinct failing tests | 52,635 |
| Total executions | 224,782 |
| Median time to post finding | **56 seconds** |
| p90 time to post finding | 346 seconds |
| Mean log lines per test | 11,058 (median: 2,801) |
| Mean input tokens per execution | 110,617 |
| Mean output tokens per execution | 5,962 |

### User Feedback (517 reports from 437 developers)

| Rating | Count | Percentage |
|--------|-------|------------|
| "Please fix" (actionable) | 436 | 84.3% |
| "Helpful" | 51 | 9.9% |
| "Not helpful" | 30 | **5.8%** |

- Helpfulness-rate rank: **#14 out of 370 tools** in Critique (top 3.78%)
- Well below the 10% not-helpful threshold required for continued posting

### Model Configuration

- **LLM:** Gemini 2.5 Flash (zero-shot, no fine-tuning)
- **Temperature:** 0.1, **top_p:** 0.8

---

## Suggestions & Future Directions

1. **Noise filtering via passing run comparison** -- Filter error-level log lines that also appear in passing executions of the same test, reducing false signals and improving diagnosis accuracy.

2. **Automated code fixes** -- Extend beyond diagnosis to suggest concrete code repairs, aligned with developer expectations surfaced in user interviews.

3. **Acknowledged limitations** -- Results are specific to Google's infrastructure and Gemini 2.5 Flash; user feedback came from a self-selected subset (437 of 22,962); prompt sensitivity means small wording changes could degrade performance; log quality varies across components.

---

## Authors & Institutions

Celal Ziftci (Google, New York), Ray Liu (Google, New York), Spencer Greene (Google, New York), Livio Dalloro (Google, New York)
