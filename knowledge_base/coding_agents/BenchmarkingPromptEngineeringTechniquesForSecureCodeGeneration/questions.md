---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Benchmarking Prompt Engineering Techniques for

### Q1. What paper is this, who wrote it, and what gap motivates it?

> [!tip]- Answer
> > The paper is "Benchmarking Prompt Engineering Techniques for Secure Code Generation with GPT Models" by Marc Bruni, Fabio Gabrielli, Mohammad Ghafari, and Martin Kropp. Its abstract states prompt engineering reduces LLM reasoning mistakes but its effect on mitigating vulnerabilities in generated code remains underexplored, so the authors implemented a benchmark. See [[wiki/01-benchmarking-prompt-engineering-secure-code|Benchmarking Prompt Engineering Techniques for Secure Code Generation with GPT Models]].

### Q2. What is the research question, and what prior evidence shows LLM-generated code is often insecure?

> [!tip]- Answer
> > The research question is "Can we enhance GPT's secure code generation via prompt engineering?" Prior work cited finds 32.8% of Python and 24.5% of JavaScript Copilot-marked snippets had issues, ~40% of Copilot completions over 89 CWE scenarios were vulnerable, and GPT-3.5 produced initially secure programs in only 5 of 21 use-cases. Small prompt changes mattered: explicitly requesting a "secure" solution raised violation-free encryption answers from 3 to 42 of 100. See [[wiki/02-related-work-and-benchmark-design|Related Work and Benchmark Design]].

### Q3. How was the 202-prompt benchmark dataset built, and how were responses generated?

> [!tip]- Answer
> > The dataset combines Python-only LLMSecEval prompts with SecurityEval prompts prefixed by "Complete the following code, and output the complete program:", each carrying its suspected CWE plus MITRE mappings, reduced to 202 prompts after dropping cases that rarely produced scannable code. Generation used the OpenAI Chat API at temperature 1 with 10 samples per modified prompt (simulating 10 developers), plus 100-sample baselines for GPT-3.5 and GPT-4o-mini to study variance. Code and data are at https://github.com/mbscit/securecodingprompts. See [[wiki/02-related-work-and-benchmark-design|Related Work and Benchmark Design]].

### Q4. Which models were tested and what did the API runs cost?

> [!tip]- Answer
> > The study spans low-cost to state-of-the-art: GPT-3.5-turbo, GPT-4o-mini (lightweight successor to 3.5-turbo), and GPT-4o (state-of-the-art at the time), testing how prompt sensitivity scales with capability. Costs were estimated per prompt with tiktoken plus a margin and a 50% Batch-API discount: all attempts on GPT-4o-mini cost USD 28 versus an estimated USD 3080 on GPT-4, scaling linearly with sample size. See [[wiki/03-models-cost-and-code-extraction|Models, Cost, and Code Extraction]].

### Q5. How does the code-extraction loop produce syntactically valid code without biasing prompts?

> [!tip]- Answer
> > Because scanners need valid code but responses mix code with prose, the authors deliberately avoid code-only instructions in the original prompts and extract code separately. A regex finds ```-delimited blocks (zero blocks may mean pure code, one block is taken, multiple blocks trigger a follow-up), then `ast.parse` must succeed with AST height above two. Failures append "Only output the python code and nothing else…", retried up to twice before regenerating the sample from scratch (max 3 times). See [[wiki/03-models-cost-and-code-extraction|Models, Cost, and Code Extraction]].

### Q6. What are the SAFVS and OFVP metrics, and why require both scanners to agree?

> [!tip]- Answer
> > Every sample is scanned with Semgrep and CodeQL, and `vuln_by_both(sample_i)` is 1 only if both agree the suspected CWE is present. SAFVS is the percentage of the n = 202 samples flagged by both scanners, and each prompt is executed k times to yield the OFVP set {SAFVS_1, …, SAFVS_k} capturing randomness. Filtering to the suspected CWE reduces false positives, and scanner agreement supports relative comparison rather than an absolute security measure. See [[wiki/04-experiment-setup-and-metrics|Experiment Setup and Metrics]].

### Q7. What bounds the extraction/scan retry loop, and which pinned snapshots were tested?

> [!tip]- Answer
> > The pinned snapshots are `gpt-3.5-turbo-0125`, `gpt-4o-mini-2024-07-18`, and `gpt-4o-2024-08-06`, with n = 202 single-task prompts each yielding one sample per execution. A problematic prompt causes at most 6 automatic requests per sample size (3 generations × 2 extraction retries), and three consecutive failures are treated as a prompt issue needing manual resolution. Scanner syntax complaints after a passing `ast.parse` escalate the same way, since invalid syntax is discarded rather than counted as secure. See [[wiki/04-experiment-setup-and-metrics|Experiment Setup and Metrics]].

### Q8. Why did proactive prompts fail on GPT-3.5-turbo, and what did RCI achieve?

> [!tip]- Answer
> > On GPT-3.5-turbo every proactive single-prompt technique increased vulnerable samples versus the 5.97% baseline (worst pe-02-c at 7.82%, −31.1%), and only post-generation RCI helped. RCI iteration 1 cut baseline issues by 24.5% (4.50%), with iterations 2 and 3 removing another 8.9% and 14.1% of initial vulnerabilities (4.01%, then 3.47% / +41.9%). The adversarial pe-negative prompt raised vulnerable samples 69.3% to 10.10%. See [[wiki/05-results-gpt-3-5-turbo|Results — GPT-3.5-turbo]].

### Q9. Which techniques topped the GPT-4o-mini table, and by how much?

> [!tip]- Answer
> > The best row was `rci-from-pe-03-a-iter-1` at 2.97% filtered vulnerable samples (+61.2% vs baseline), followed by `rci-from-baseline-iter-3/iter-2` at 3.17% (+58.6%) and `rci-from-baseline-iter-1` at 3.86% (+49.5%). The single-prompt prefix pe-03-a reached 4.06% (+47.0%), near CoT at 3.96% (+48.3%), while the adversarial pe-negative raised vulnerable samples 127.7% above baseline. Gains flattened by the third RCI iteration, showing diminishing returns. See [[wiki/06-results-gpt-4o-mini|Results — GPT-4o-mini]].

### Q10. What were the GPT-4o headline numbers, and how did sensitivity differ across models?

> [!tip]- Answer
> > On GPT-4o (7.43% baseline) every tested technique helped: prefix pe-03-a was best single-prompt at 3.27% (−56%), RCI on baseline cut 64.7% (2.62%), and RCI on pe-03-a reached 2.33% (−68.7%), while pe-negative spiked to 18.76% (+152.7%). Cross-model comparison shows sensitivity growing with capability: generic prompts did nothing for GPT-3.5-turbo but helped GPT-4o-mini and most of all GPT-4o, while RCI helped all models but most on advanced ones. GPT-3.5-turbo's seemingly secure baseline may reflect incomplete code (lower AST height). See [[wiki/07-results-gpt-4o-and-comparison|GPT-4o Results and Cross-Model Comparison]].

### Q11. What can legitimately be claimed from the Fig. 6 chunk on this wiki page?

> [!tip]- Answer
> > Almost nothing numeric: the chunk is garbled figure-extraction text preserving only the axis title "Vulnerable Percentage", tick marks 15/10/5, and the caption "Fig. 6. Vulnerability Comparison". Technique labels and per-attempt values cannot be reliably reconstructed, so the page records the gap instead of inventing values — use Tables II–IV and the prose for numbers. See [[wiki/08-result-figures-and-distributions|Result Figures and Distributions]].

### Q12. What does the Prompt Agent do, and what are the key validity threats and conclusion numbers?

> [!tip]- Answer
> > The BetterChatGPT-based Prompt Agent prepends the pe-03-a prefix verbatim ("You are a developer who is very security-aware and avoids weaknesses in the code") and optionally applies RCI post-processing to markdown code blocks, cutting GPT-4o vulnerabilities ~64.7% without the prefix and ~68.7% with it; the prefix felt harmless but RCI added 10+ seconds delay and verbose caution. Key threats include training-data exposure, two-scanner dependence, isolated Python snippets, snapshot variability, phrasing sensitivity, no inferential tests, and OpenAI-only models. The conclusion: the prefix cut flaws 47% (4o-mini) and 56% (4o) but backfired on 3.5-turbo, while one RCI iteration fixed 24.5%/49.5%/64.7% across 3.5-turbo, 4o-mini, and 4o. See [[wiki/09-discussion-prompt-agent-conclusion|Discussion, Prompt Agent, Threats to Validity and Conclusion]].

### Q13. For a GPT-4o coding assistant, which combination would you recommend and what trade-offs justify it?

> [!tip]- Answer
> > Recommend the security-aware prefix (pe-03-a) always on plus optional RCI post-processing: the prefix alone gives a ~56% cut nearly free, and RCI on prefixed code reaches ~68.7% fewer vulnerabilities, combining proactive prevention with iterative repair. Justify it by cost and UX: RCI needs multiple large calls, adds 10+ second delays with diminishing returns, and HumanEval pass@1 dipped ~10% under RCI, so reserve RCI for security-critical code. This judgment holds only for the GPT-4o family and Python snippets under dual-scanner SAFVS, not for GPT-3.5-turbo or other languages. See [[wiki/09-discussion-prompt-agent-conclusion|Discussion, Prompt Agent, Threats to Validity and Conclusion]].
