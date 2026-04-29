# Agentic Harness for Real-World Compilers

**Paper:** [Agentic Harness for Real-World Compilers (Zheng et al., 2025)](https://arxiv.org/abs/2603.20075)

## Human Readable TL;DR

Imagine you have a super-smart assistant that is great at fixing bugs in everyday software -- like a spell-checker for code. But when you ask it to fix problems inside a compiler (the tool that translates human-written programs into instructions a computer actually runs), it struggles badly because compilers are incredibly intricate machines with their own specialized language and logic. This paper builds a custom "workshop" full of compiler-specific diagnostic tools and test cases so that AI assistants can actually understand what went wrong inside a compiler and attempt repairs -- much like giving a general mechanic a specialized avionics toolkit before asking them to fix a jet engine. Even with this help, the AI still only gets about 20% of fixes truly right, showing how hard compiler work really is.

## TL;DR

This paper introduces `llvm-autofix`, the first agentic harness tailored for LLM-based compiler bug repair, targeting LLVM's middle-end. It includes compiler-specific tools (debugger integration, IR validation via alive2, build/test automation), a benchmark of 334 reproducible bugs (`llvm-bench`), and a minimal agent (`llvm-autofix-mini`) that improves resolution rates by ~22% over general-purpose agents. Expert review reveals that fewer than 42% of patches passing automated tests are genuinely correct, with the best model (GPT-5) achieving only 20.1% genuine resolution -- exposing fundamental gaps in LLM reasoning about compiler internals.

---

## Problem & Motivation

Compilers are foundational infrastructure -- virtually all software depends on them. Yet compiler bugs are uniquely difficult to fix: bug reports often contain only a reproducer and a stack trace (no natural language description), and understanding the root cause requires deep expertise in type systems, intermediate representations, optimization passes, and code generation.

Existing LLM-based software repair agents (e.g., SWE-agent) perform well on general software bugs but suffer a **62% average performance drop** when applied to compiler bugs. This gap exists because general-purpose agents lack the specialized tooling, domain context, and debugging capabilities needed for compiler internals. The authors aim to close this gap by providing LLMs with a purpose-built environment for LLVM bug repair.

---

## Main Original Ideas

1. **llvm-autofix Harness** -- A complete agentic environment wrapping LLVM-specific tasks (build configuration, reproducer validation, GDB-based dynamic debugging, IR validation with alive2, code exploration, patch editing, and regression testing) into agent-callable tools. This abstracts away environmental complexity so LLMs can focus on reasoning about the bug itself.

2. **llvm-bench Benchmark** -- An automatically constructed, reproducible benchmark of 334 LLVM middle-end bugs (222 crashes, 112 miscompilations) spanning 64 components, with difficulty stratification (easy/medium/hard) and a continuously updated "live" subset to mitigate data leakage. Each issue includes reproducers, golden patches, and component-specific regression tests.

3. **llvm-autofix-mini Agent** -- A four-stage minimal agent (Setup, Reason, Generate, Validate) that leverages dynamic debugging to inspect LLVM's internal state at crash points or before transformations, performs root cause analysis via a ReAct loop, synthesizes patches with online validation, and runs offline regression testing.

4. **Expert-Reviewed Genuine Capability Metric** -- Beyond automated pass/fail testing, the authors introduce expert review of accepted patches to measure genuine correctness, revealing that automated test passage significantly overestimates true fix quality.

5. **Taxonomy of LLM Failure Modes in Compiler Repair** -- A systematic categorization of how LLMs fail: bypassing assertions (ChangeAssert), incorrect localization (WrongLocalization), superficial fixes that lack generality or silently introduce new bugs (WrongFix), and premature exits (ProactiveExit).

---

## Key Findings

### Resolution Rates on llvm-bench live

| Model | Agent | Resolution Rate | vs. SWE-bench Verified |
|---|---|---|---|
| **GPT-5** | llvm-autofix-mini | **51.5%** | -35.2% |
| **GPT-5** | mini-SWE-agent | 21.0% | -- |
| DeepSeek V3.2 | mini-SWE-agent | 38.9% | -35.2% |
| Gemini 2.5 Pro | llvm-autofix-mini | ~40% | -- |
| Qwen 3 Max | llvm-autofix-mini | ~35% | -- |
| GPT-4o | mini-SWE-agent | ~15% | -82.9% |

### Genuine Correctness (Expert Review)

| Model | Agent | Genuine Resolution Rate |
|---|---|---|
| **GPT-5** | llvm-autofix-mini | **20.1%** |
| Other model-agent pairs | -- | <15% |

- Fewer than **42%** of patches passing all automated tests were judged genuinely correct by an LLVM expert.
- **6 out of 10** model-agent pairs produced zero correct patches for medium-difficulty issues; only GPT-5 with llvm-autofix-mini solved a single hard issue correctly.

### Qualitative Findings

- **Miscompilations are harder than crashes** -- resolution rates lag by ~13-14% across both agents.
- **Specialized tools matter** -- debugger commands (`debug`, `eval`) were the most frequently invoked tools, but also had the highest failure rates, suggesting room for improvement in tool interaction.
- **Bug localization is a bottleneck** -- even with the erroneous component specified in the prompt, frontier models improved file-level recall by less than 10% over GPT-4o.
- **llvm-autofix-mini scales better with token budget** -- unlike mini-SWE-agent (which plateaus around 3M tokens), llvm-autofix-mini shows continued improvement with larger budgets for most models.
- **Common failure modes**: ContextLimit (GPT-4o), TokenLimit/ToolLimit (frontier models on llvm-autofix-mini), ProactiveExit (mini-SWE-agent giving up prematurely), and RuinLLVM (mini-SWE-agent corrupting the repository).

---

## Suggestions & Future Directions

1. **Preventing assertion bypasses** -- LLMs frequently "fix" crashes by modifying or removing assertions rather than addressing root causes. Future agents need guardrails or validation mechanisms to detect and reject such superficial patches.

2. **Overcoming short-sightedness in repairs** -- Many patches are narrowly tailored to the specific reproducer and fail to generalize. Research into more holistic reasoning about optimization correctness (e.g., leveraging formal verification tools like alive2 more deeply) is needed.

3. **Improving bug localization** -- Current models struggle to identify the correct file and function even when given the faulty component. Better static analysis integration, retrieval-augmented approaches, or fine-tuning on compiler codebases could help.

4. **Long-context efficiency** -- Compiler debugging generates massive tool outputs that exhaust context windows. More efficient context management strategies and summarization techniques are needed.

5. **Extending to other compiler components and systems** -- The current focus is on LLVM's middle-end; extending to front-end, back-end, and other compiler infrastructures (GCC, Rust compiler) is a natural next step.

6. **More robust patch evaluation** -- Automated regression tests are insufficient to verify compiler patch correctness. Developing better automated evaluation methods (differential testing, property-based testing, expanded alive2 integration) that approximate expert-level judgment is an open challenge.

7. **Enhancing LLM compiler expertise** -- Fine-tuning LLMs on compiler-specific corpora, or designing retrieval mechanisms over LLVM documentation and commit history, could improve domain understanding.

---

## Authors & Institutions

Yingwei Zheng (Southern University of Science and Technology), Cong Li (ETH Zurich), Shaohua Li (The Chinese University of Hong Kong), Yuqun Zhang (Southern University of Science and Technology), Zhendong Su (ETH Zurich)
