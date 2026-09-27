> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation — In Plain Language

## What is this about?

This paper is a guided tour of 27 recent studies on using AI — mostly large language models (LLMs) — for two programming jobs: fixing bugs automatically and writing new code.

It splits the field in two. The first half is Automated Program Repair (APR): tools that find bugs and propose fixes with less manual debugging. The second half is code generation: models that turn prompts, half-written code, or one language into working code, summaries, or translations.

For each study the authors note which model was used, which programming languages it handles, how the AI fits into the repair or writing workflow, and where it still falls short. The goal is to save other researchers months of reading by mapping what works, what does not, and what is missing.

In short: if you have heard "AI can fix and write code," this survey asks — which tools, for which bugs and languages, how well, and at what cost?

A useful mental picture: APR is like an apprentice mechanic who can spot a fault and suggest a part replacement, while code generation is like an apprentice who can draft a new part from your description. Both need a senior mechanic to inspect the work.

## Why does it matter?

Fixing bugs and writing routine code eat up a huge share of developer time. Even small gains in automation mean faster releases, fewer late-night debugging sessions, and fewer security holes slipping into production.

LLMs changed the game because they arrive pre-trained on enormous piles of public code. Instead of building a bug-fixer from scratch, teams can take a model like GPT-4, Codex, or CodeT5 and fine-tune it for their task. That lowers the barrier to entry and has sparked rapid progress.

But the stakes are high when the AI gets it wrong. A plausible-looking but incorrect fix can break working features, introduce a security vulnerability, or pass tests while missing the real problem. This survey matters because it compares claims head-to-head, using shared benchmarks, so teams can pick the right tool instead of trusting marketing.

It also highlights gaps that still need human judgment: complex multi-file bugs, niche languages, security-critical code, and code with deep business logic.

Put simply: the survey helps managers decide where AI assistance saves money today, and helps researchers see which problems are still unsolved.

## How does it work?

Think of the workflow in three stages: find the bug, propose a fix, and check the fix.

To find bugs, tools use different tricks for different bug types. Security bugs (like buffer overflows or bad access checks) are hunted with templates, runtime monitoring, and search-based methods. Logic bugs (the code runs but does the wrong thing) are hunted with mined fix patterns, fuzzing with random inputs, and evolutionary search. Typo-level syntax errors are caught with mined patterns, grammar-aware fuzzing, and mutation of the code structure.

Modern LLM approaches add four upgrades. Transfer learning takes a general code model and fine-tunes it on bug-fix examples. Neural fault localization reads the program's structure — its syntax tree and control flow — to pinpoint suspicious lines. Automated test generation writes new test cases to check each candidate fix does not break existing behavior. Coverage analysis then makes sure those tests actually exercise the changed code, reducing overfitting to one example.

Around that core loop, three helpers make results more trustworthy. Explainable AI tries to show why the model suggested a fix. Interactive debugging asks a human for help when the AI is unsure. Multi-modal models feed in not just code but comments, docs, and logs for extra context.

For writing code from scratch, the recipe is similar: pre-train on lots of code, then specialize. CodeT5 learns from developer-chosen variable names to grasp meaning. GraphCodeBERT adds data-flow graphs showing how values move between variables. DeepSeek-Coder practices filling in the middle of unfinished snippets. Magicoder invents realistic coding instructions from open-source snippets. Each trick trades speed, accuracy, and resource cost differently.

Checking is just as important as suggesting. Candidate patches are run against old and new tests, compared with templates from past human fixes, and sometimes ranked by probabilistic models that predict which patch is most likely correct before it ever reaches production.

## Where can this be used?

The survey's benchmarks show where these tools already help in practice.

Day-to-day coding assistants are the most mature use: fast autocompletion and quick fixes for common bugs, where Codex-style models inside tools like Copilot shine. Code summarization is another win — turning a tangled function into a readable paragraph for reviews and onboarding.

Bug triage and localization benefit too: models that flag the likely faulty lines and suggest a patch, leaving a human to approve. Security teams use protocol fuzzing and vulnerability-localization suites to probe network code and multithreaded programs for crashes and race conditions.

Cross-language work is growing: translating code between Python, Java, JavaScript, C, C++, and others, or refactoring legacy code more concisely. Evaluation suites like HumanEval, Defects4J, DebugBench, and TransCoder let teams test these uses in a controlled way before trusting them on real repositories.

The limits define where caution is needed: large dependency-heavy codebases, rare domain-specific bugs, niche languages like Bash, and high-assurance or security-critical systems still need expert review.

Two concrete examples from the survey: protocol-fuzzing setups probe C network code for hidden crash paths, while real-bug suites built from Java projects test whether a fix holds up outside toy examples. Both show the same lesson — lab scores only matter if the tool survives contact with real repositories.

## Conclusions & takeaways

There is no single best model — there is a best fit for each task.

If you remember one sentence from this explainer, let it be that one: match the model to the task, test every suggestion, and treat the AI as a capable junior partner.

For speed and fluency in everyday completion and quick fixes, Codex-style models lead. For precision on hard, context-heavy problems, GPT-4 leads but costs more time and compute. For focused or structure-heavy niches, CodeT5 and GraphCodeBERT do well but are less suited to real-time use. Newer models — Phind/CodeLlama, DeepSeek-Coder, StarCoder2, Mixtral, Zephyr, Smaug — push accuracy, language coverage, and efficiency further, yet each keeps a weakness around niche languages, complex logic, security, or multilingual support.

The survey's closing message is practical: use its training-strategy groupings and benchmark tables to match a model to your use case, prefer open-source options where you can inspect and adapt them, and keep humans in the loop. Persistent challenges — accuracy, context sensitivity, scaling to large systems, bias, benchmark overfitting, heavy resource use, and copyright concerns — mean AI repair and generation work best as assistants, not autopilots.

For a non-expert reader, the one-line moral is: AI coding tools are fast and often right, but still need testing, review, and the right tool for the job.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Automated Program Repair (APR) | Software that finds bugs and proposes fixes on its own, to cut manual debugging. |
| Large language model (LLM) | An AI trained on huge amounts of text and code that predicts likely next words or code tokens. |
| Fine-tuning | Taking a general pre-trained model and giving it extra training on a specific task, like bug fixing. |
| Transfer learning | Reusing knowledge from one task (general coding) to get a head start on a related task (fixing bugs). |
| Fault localization | Figuring out which lines of code actually cause the failure. |
| Abstract Syntax Tree (AST) | A tree-shaped map of code structure that tools use to reason about what the program does. |
| Fuzzing | Throwing many random or mutated inputs at a program to uncover crashes and hidden bugs. |
| Benchmark | A standard set of tasks, like HumanEval or Defects4J, used to compare tools fairly. |
| Overfitting | When a fix or model works on the test examples but fails on new, real-world cases. |
| Hallucination / plausible patch | A fix that looks correct and may pass tests but is actually wrong or insecure. |
