> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiment Setup and Metrics

**In one sentence:** The experiments run 202 single-task prompts across three pinned GPT snapshots, extract code with a bounded retry loop, scan each sample with both Semgrep and CodeQL, and score attempts with the Scanners-Agree Filtered Vulnerable Samples (SAFVS) percentage repeated k times (OFVP) to capture randomness.

## Key points
- Three LLMs under test with pinned snapshots: `gpt-3.5-turbo-0125`, `gpt-4o-mini-2024-07-18`, and `gpt-4o-2024-08-06`.
- Benchmark scale is n = 202 prompts, each formulating one specific task, where each prompt execution yields one code sample.
- Code extraction retries are bounded: a problematic prompt causes at most 6 automatic LLM requests per sample size (3 generations from the original prompt with 2 code-extraction re-tries each).
- If code extraction fails for three consecutive samples, it is treated as a prompt-related issue requiring manual resolution, not further automatic Response Generation repeats.
- Every sample is scanned with two static scanners, Semgrep and CodeQL; a sample counts as vulnerable only if both agree (binary indicator `vuln_by_both(sample_i)`).
- The headline metric SAFVS is the percentage of the n samples where both scanners agree on the suspected CWE: `SAFVS = (1/n) Σ vuln_by_both(sample_i) × 100`.
- Each prompt is executed k times (each an independent API call), producing an Observed Filtered Vulnerability Percentages set `OFVP = {SAFVS_1, ..., SAFVS_k}` used to assess randomness effects on baselines and technique effectiveness.
- Scanner-reported syntax issues (even after successful `ast.parse`) trigger extraction re-tries, then a fresh Response Generation sample, then manual attention after three re-tries; invalid syntax is discarded rather than rewarded as secure.

---

## Models under test

| Model | Snapshot |
|---|---|
| GPT-3.5-turbo | `gpt-3.5-turbo-0125` |
| GPT-4o-mini | `gpt-4o-mini-2024-07-18` |
| GPT-4o | `gpt-4o-2024-08-06` |

**Covers:** Experimental setup across three LLMs and vulnerability metrics definitions.

## Code extraction retry policy

- Extraction failures feed back into the Response Generation step with a new sample.
- "If code extraction fails for three consecutive samples, this indicates a prompt-related issue," which "needs to be resolved manually instead" of being cleared by repeating Response Generation.
- Bound per problematic prompt per sample size: "at most 6 automatic requests to the LLM: 3 generations from the original prompt with 2 code extraction re-tries each."
- Stated rationale: "This strategy provides a balance of allowing for self-correction while enforcing manual intervention where necessary."

**Covers:** Experimental setup across three LLMs and vulnerability metrics definitions.

## E. Code Security Scan

- "To assess the security of each response, we write the extracted code into a file and scan it with two static scanners, Semgrep and CodeQL."
- "In some cases, the scanners report syntax issues, even though ast.parse was successful. If this occurs, the code extraction with the follow-up prompt is re-tried."
- Escalation: if the issue persists, "a new sample is generated using the Response Generation step"; "if the issue persists after three re-tries, the error is reported and needs manual attention."
- "Instead of rewarding invalid syntax by regarding it as secure code, it is discarded."
- Caveat: "Using static scanners to evaluate code security means inheriting their limitations."

**Covers:** Experimental setup across three LLMs and vulnerability metrics definitions.

## Metrics: SAFVS and OFVP

- "We have n = 202 prompts, each formulating one specific task. Each prompt execution results in one code sample."
- "We define a binary indicator vuln_by_both(sample_i) which equals 1 if both scanners agree that sample_i contains the suspected CWE vulnerability, and 0 otherwise."
- "The Scanners Agree Filtered Vulnerable Samples metric indicates the percentage of samples across all n tasks that contain the suspected CWE:" `SAFVS = (1/n) Σ vuln_by_both(sample_i) × 100`.
- "We execute each prompt k times. Hence, we get a set of Observed Filtered Vulnerability Percentages OFVP with size k for each prompt engineering attempt:" `OFVP = {SAFVS_1, ..., SAFVS_k}`.
- "We examine OFVP to understand the variability for identical prompts and assess the impact of randomness on both the model's baseline performance and the effectiveness of the prompting technique."
- Footnote in chunk: "Every prompt execution is an API call that is completely independent of" (truncated in chunk).

**Covers:** Experimental setup across three LLMs and vulnerability metrics definitions.
