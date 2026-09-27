---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation

### Q1. How does the survey scope its 27 papers, and what are its four stated aims?

> [!tip]- Answer
> > The survey splits 27 recent papers into Automated Program Repair with LLM integration and LLM-based code generation, covering bug detection and repair alongside general-purpose and task-specific code models. Its four aims are to summarize achieved goals, map repair scenarios and languages, explain LLM workflow integration with its challenges, and surface remaining limitations. See [[wiki/01-survey-overview-and-goals|Survey Overview and Goals]].

### Q2. What three methods make up the survey methodology, and how are papers selected?

> [!tip]- Answer
> > The survey uses systematic literature review with inclusion/exclusion criteria, taxonomy development comparing objectives, techniques, and outcomes, and comparative analysis with tabular and graphical visualization. Papers are kept only if they help answer one of the four research questions, then categorized under Code Generation or Automated Program Repair. See [[wiki/01-survey-overview-and-goals|Survey Overview and Goals]].

### Q3. What six APR approaches does the survey list for security bugs?

> [!tip]- Answer
> > For security bugs such as buffer overflows, injection flaws, race conditions, and access-control faults, the survey lists template-based patching, dynamic analysis with fuzzing and symbolic execution, search-based mutation APR, specification-guided repair for protocols, input sanitization and validation patches, and memory-safety repair with bounds checking or smart pointers. These span fast template reuse, co-evolving patches and inputs, and targeted C/C++ memory fixes. See [[wiki/02-survey-methodology|Survey Methodology and Research Questions: AI for Debugging and Bug Fixing]].

### Q4. How does the survey distinguish APR techniques for semantic versus syntactic bugs?

> [!tip]- Answer
> > Semantic bugs (logical deviations from expected behavior) are addressed with pattern-based patching, greybox fuzzing using execution feedback, evolutionary search-based APR, and specification-guided repair against formal models. Syntactic bugs (grammar violations and malformed structure) use pattern matching such as FixMiner mined from prior commits, grammar-based fuzzing mutating ASTs while staying valid, and search over syntactic mutations. See [[wiki/02-survey-methodology|Survey Methodology and Research Questions: AI for Debugging and Bug Fixing]].

### Q5. Which transfer-learning and LLM trends are advancing APR, and how do fault localization and test generation fit in?

> [!tip]- Answer
> > Transfer learning by fine-tuning pre-trained models such as GPT-4, Codex, and CodeT5 on bug datasets is rising, joined by self-supervised learning on unlabeled repositories, XAI for interpretable fixes, interactive debugging with active learning, and multi-modal context from comments, docs, and logs. Neural fault localization reasons over temporal properties and AST control flow, while AI-generated tests plus coverage analysis validate candidates and curb overfitting. See [[wiki/03-ai-trends-in-apr|Transfer Learning for Code: LLMs]].

### Q6. What persistent accuracy, context, resource, and LLM-specific challenges does the survey name?

> [!tip]- Answer
> > APR tools still mislabel correct code as faulty and vice versa, struggle with large dependency-heavy codebases, and impose high memory and compute overhead that disrupts workflows. LLM-specific limits include poor generalization to unseen or domain-specific bugs, weak grasp of business logic, introduced or missed security flaws, training-data bias toward common patterns, benchmark overfitting, and copyright concerns over proprietary code. See [[wiki/03-ai-trends-in-apr|Transfer Learning for Code: LLMs]].

### Q7. What does each benchmark family measure: HumanEval, MBPP, DebugBench, VulnLoc, Defects4J, TransCoder, ProFuzzBench, SCTBench?

> [!tip]- Answer
> > HumanEval and MBPP test code generation and bug-fixing efficiency on programming problems; DebugBench assesses LLM debugging performance and VulnLoc measures automatic vulnerability localization with minimal error margin. Defects4J provides real Java bugs for practical evaluation, TransCoder tests cross-language translation correctness, ProFuzzBench tests network-protocol vulnerability resistance, and SCTBench tests concurrency and synchronization handling. See [[wiki/04-benchmarks-and-debugging-tools|Modern Benchmark Tools for Evaluating Bug-Fixing Techniques]].

### Q8. What task-fit trade-off does the survey report among Codex, GPT-4, CodeT5, and GraphCodeBERT?

> [!tip]- Answer
> > Codex leads on speed and fluency for real-time completion and quick fixes but misses rare or subtle logic errors, while GPT-4 leads on complex-task precision and depth at the cost of speed and resources. CodeT5 is exact on localized, focused tasks and long coherent summaries but weak at real-time debugging, and GraphCodeBERT excels on structural dependencies and context-aware summarization but is too slow and resource-heavy for rapid completion or refactoring. See [[wiki/05-code-generation-models-compared|Code Generation Models Compared: Speed, Fluency, and Task Fit]].

### Q9. How does the survey group models by training strategy, and what mechanism-to-limitation pair defines each group?

> [!tip]- Answer
> > General pre-training covers Codex (12B GPT fine-tune, repeated sampling, weak on dependencies), CodeT5 (identifier-aware encoder-decoder, weak on structure), GraphCodeBERT (data-flow graphs on CodeSearchNet, weak on broad control flow), and Phind (CodeLlama-34B fine-tune, 73.8% HumanEval). Specialized code pre-training (OpenCodeInterpreter multi-turn dialogues, StarCoder2, SPT Code, Magicoder OSS-INSTRUCT with seed bias), bootstrapped methods (DeepSeek-Coder FIM plus 128K context, WizardCoder Evol-Instruct, Mixtral sparse experts, Smaug DPO-Positive), and Zephyr direct-distillation alignment complete the taxonomy. See [[wiki/06-model-strengths-and-weaknesses|Model Strengths and Weaknesses: Codex, CodeT5, GraphCodeBERT and Peers]].

### Q10. What does the survey bibliography contain, and which entries anchor code models, APR, and evaluation?

> [!tip]- Answer
> > The bibliography lists 27 entries from Phind-CodeLlama [1] through Zhong et al. "Debug like a Human" [27], spanning code LLMs, pre-training, debugging, fuzzing, and alignment. Anchors include Phind, StarCoder 2, Mixtral, DeepSeek-Coder, and Magicoder for code models; GraphCodeBERT, SPT-Code, and CodeT5 for representations; DEAR, ProveNFix, multi-agent synergy, and fuzzing-over-patch-space for APR; plus OpenAI evaluation, DebugBench, Zephyr, WizardLM, Smaug, and protocol, evolutionary, and greybox fuzzing papers. See [[wiki/07-references|References]].

### Q11. For a team choosing one model for real-time completion, complex multi-file repair, and dependency-heavy auditing, what should it pick and why?

> [!tip]- Answer
> > Recommend Codex or Copilot-style completion for real-time speed, GPT-4 for complex multi-file repair needing deep context despite higher cost and latency, and GraphCodeBERT for dependency-heavy auditing and summarization despite its unsuitability for rapid refactoring. This follows the survey's task-fit synthesis while hedging its persistent caveats on niche languages, security, and benchmark overfitting with pilot evaluation on the team's own codebase. See [[wiki/05-code-generation-models-compared|Code Generation Models Compared: Speed, Fluency, and Task Fit]].
