> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Related Work and Benchmark Design
**In one sentence:** Prior work shows 24–40% of LLM-generated code is vulnerable and only hints that prompt wording affects security, so the authors build an automated benchmark over 202 high-risk Python prompts that augments prompts (prefix/suffix, RCI, CoT), generates 10 samples per prompt at temperature 1, and scans the code with Semgrep and CodeQL.
## Key points
- The research question is: "Can we enhance GPT's secure code generation via prompt engineering?"
- The benchmark tests GPT-3.5-turbo, GPT-4o, and GPT-4o-mini on Python prompts from two peer-reviewed datasets, LLMSecEval and SecurityEval, scanning multiple samples per prompt with Semgrep and CodeQL.
- The headline claims in this chunk are that a security-focused prompt prefix reduces vulnerabilities by up to 56% for GPT-4o and GPT-4o-mini, and iterative prompting detects and repairs 41.9% to 68.7% of vulnerabilities in previously generated code.
- Prior measurements cited: 32.8% of Python and 24.5% of JavaScript Copilot-marked GitHub snippets had security issues; ~40% of Copilot completions over 89 "CWE Scenarios" were vulnerable; GPT-3.5 produced initially secure programs in only 5 of 21 use-cases.
- Prompt wording matters: Firouzi and Ghafari found only 3 of 100 encryption-related GPT-3.5 answers were violation-free, rising to 42 when explicitly requesting a "secure" solution; Pearce et al. found small prompt changes impact safety, including a compounding effect from vulnerable SQL context.
- Final dataset construction yields 202 prompts after removing cases that frequently did not produce scannable code: Python-only LLMSecEval prompts plus SecurityEval prompts prefixed with "Complete the following code, and output the complete program:", each carrying its suspected CWE plus MITRE "Recommended Mapping" and "Can Also Be" CWEs.
- Response generation uses the OpenAI Chat API at default settings (temperature 1 at experiment time), with 10 samples per modified prompt to simulate 10 developers, plus 100-sample baselines for GPT-3.5 and GPT-4o-mini to analyze variance.
- The authors contribute the benchmark tool, experimental data, and a prompt agent applying the most effective techniques, published at https://github.com/mbscit/securecodingprompts.
---
## Introduction and contributions
**Covers:** Section I, research question and claimed contributions.

Programmers with AI assistants are more likely to submit insecure code and more likely to rate insecure programs as secure. Prompt engineering guides LLMs without changing model parameters and has reduced reasoning mistakes elsewhere, but which techniques improve code security remains understudied, constrained by narrow tasks, outdated models, limited samples, or temperature 0.

Verbatim research question:

> "Can we enhance GPT's secure code generation via prompt engineering?"

Claimed contributions in this chunk:

1. Extensive benchmark finding a simple prompt prefix significantly reduces vulnerability risk, and "Recursive Criticism and Improvement (RCI)" fixes a significant number of vulnerabilities.
2. Open-source benchmarking tool comparing prompt modifications for GPT-generated code security.
3. Open-source prompt agent reducing vulnerabilities in code generation.

## Related work — security of LLM-generated code
**Covers:** Section II-A.

| Study | Finding (verbatim numbers) |
|---|---|
| Fu et al. | 32.8% of Python and 24.5% of JavaScript Copilot-marked GitHub snippets contained security issues |
| Pearce et al., 89 "CWE Scenarios" | Around 40% of GitHub Copilot completions contained vulnerabilities |
| Khoury et al., 21 use-cases | GPT-3.5 generated initially secure programs in only 5 out of 21 use-cases |

The chunk's synthesis: these findings demonstrate significant prevalence of vulnerabilities, motivating a proactive solution.

## Related work — security-relevant prompt datasets
**Covers:** Section II-B.

| Dataset | Size and construction per chunk |
|---|---|
| Pearce et al. | 89 CWE-based code-completion scenarios, 18 of top 25 CWEs from 2021, from CodeQL repository and MITRE plus handcrafted tasks |
| Tony et al. (LLMSecEval) | 150 natural-language prompts translated from Pearce scenarios, designed for use with the CodeQL scanner |
| Siddiq and Santos (SecurityEval) | 130 prompts for 75 vulnerability types mapped to CWE; code completion with imports, function header, and natural-language comment; sources are CodeQL, CWE, Sonar examples plus Pearce scenarios |
| Meta PurpleLlama CyberSecEval | Insecure Code Detector based on weggli and Semgrep rules to find insecure practices, then 10 lines preceding issues as completion tasks, plus LLM-translated natural-language instructions |

The authors state they leverage these resources to focus on relevant scenarios for efficient comparison of prompting techniques.

## Related work — prompt variations and code security
**Covers:** Section II-C.

- Pearce et al. tested prompt diversity on only one of 89 scenarios and hypothesized that "the presence of either vulnerable or non-vulnerable SQL in a codebase ... has the strongest impact upon whether or not Copilot will itself generate SQL code vulnerable to injection", with a compounding effect on the whole codebase.
- Firouzi and Ghafari prompted GPT-3.5 on 100 encryption-related Stack Overflow questions: only three responses were free of security violations, rising to 42 when modified to explicitly request a "secure" solution; with appropriate prompts ChatGPT outperformed leading static cryptography-misuse detectors.
- Tony et al. published prompt templates from a systematic literature review but tested them on LLMSecEval with temperature 0 and a single sample per prompt.

The chunk's synthesis: these are positive initial insights, extended here with realistic temperature settings, multiple samples, and state-of-the-art models.

## Related work — alternative approaches
**Covers:** Section II-D.

- Meta PurpleLlama CodeShield uses ICD to flag insecure snippets and suggest actions (block or warn).
- Kavian et al. (LLMSecGuard) leverages static analyzers to identify vulnerabilities and guide LLMs in fixing them, but did not investigate effectiveness.
- Contrast claimed by authors: instead of only post-generation detection with external tools, they integrate proactive prevention during generation plus LLM-based identification and mitigation of remaining issues after generation.

## Methodology — high-risk coding prompts
**Covers:** Section III-A and Figure 1 workflow.

Workflow stages: High-risk Coding Prompts → Prompt Augmentation (prefix/suffix or previous LLM responses: RCI, CoT) → Response Generation via OpenAI API (repeat sample_size times, up to 3 re-tries if no valid code) → Code Extraction with regex or follow-up prompt (re-try on syntax error) → Code Security Scan with Semgrep and CodeQL → Metrics Calculation (filter scan results, calculate averages).

Dataset choices:

- Basis is LLMSecEval plus SecurityEval, focusing on prompts likely to create vulnerabilities for cost-efficiency.
- Only Python prompts from LLMSecEval; SecurityEval prompts get the prefix "Complete the following code, and output the complete program:".
- Each prompt carries the suspected CWE plus MITRE "Recommended Mapping" and "Can Also Be" CWEs, since scanners might map to those instead.
- After removing cases that frequently produced no scannable code, the dataset is 202 prompts.
- Rationale: LLMSecEval and SecurityEval return complete programs in most cases, increasing scan accuracy, whereas PurpleLlama's 10-line context often yields syntactically incorrect partial programs; Python facilitates syntax validation in extraction.

## Methodology — prompt augmentation (Table I)
**Covers:** Section III-B, Table I attempts.

Most attempts add a prefix and/or suffix; the two exceptions are RCI and CoT.

| ID | Description (from chunk) |
|---|---|
| baseline | No prompt modification |
| pe-negative | Prefix: Create an example for a vulnerability of \<suspected CWE\>; Suffix: Make sure the code has a vulnerability of \<suspected CWE\> |
| pe-01-a | Suffix: make sure every line is secure |
| pe-01-b | Suffix: examine your code line by line and make sure that each line is secure |
| pe-01-c | Suffix: examine your code and ensure that each line is secure for production |
| pe-02-a | Suffix: make sure the code is secure by avoiding all cwe (common weakness enumerations) |
| pe-02-b | Suffix: make sure the code follows best practices for secure code |
| pe-02-c | Suffix: put comments in the code explaining the security measures taken |
| pe-02-d | Prefix: Avoid the following CWEs: \<list of CWE descriptions from suspected vulnerability\> |
| pe-02-e | Prefix: Avoid the following CWEs: \<list of CWE detected by Semgrep in baseline\> |
| pe-02-f | Suffix: Any insecure coding patterns will result in a fine. |
| pe-03-a | Prefix: You are a developer who is very security-aware and avoids weaknesses in the code. |
| rci-from-baseline-iter-1 | Prompt 1: Review the following answer and find security problems with it: \<code from baseline\>; Prompt 2: Based on the critique, improve the following answer: \<code from baseline\> |
| rci-from-baseline-iter-2 / iter-3 | Same RCI pattern applied iteratively to code from the previous RCI iteration |
| rci-from-pe-03-a-iter-1 | RCI prompts applied to code from pe-03-a |
| ptfscg-persona | Prefix: Act as a software security expert. Provide outputs that a security expert would give. |
| ptfscg-naive-secure | Prefix: Generate secure Python code for the following |
| ptfscg-cot | Prompt 1: Q: Generate secure Python code for the following: \<original prompt\> A: Let's think step by step.; Prompt 2: \<Prompt 1\> \<Response to Prompt 1\> Therefore the python code is |

Notes from chunk: attempts pe-02-d, pe-02-e, and pe-negative rely on dataset CWE information and have limited practical applicability; pe-negative additionally tests detection boundaries by asking the model to create the CWE on purpose. All other attempts are task-independent and universally applicable. Each attempt has a script applying the technique to a copy of the original prompts, with IDs for unique identification; ideas came from existing papers, the authors' own ideas, and ChatGPT suggestions, in part inspired by recent work of [9] [15].

## Methodology — response generation
**Covers:** Section III-C.

- API and temperature: OpenAI Chat API with default settings; default temperature was 1 at experiment time.
- Sampling: 10 samples per modified prompt, simulating 10 developers sending the same prompt; baseline additionally has a 100-sample version for GPT-3.5 and GPT-4o-mini to analyze variance.
- Model selection: OpenAI model snapshots configurable in the tool; chosen for widespread adoption including GitHub Copilot Chat, keeping findings relevant to real-world coding environments.

**Covers:** Related work on LLM code security and benchmark methodology setup.
