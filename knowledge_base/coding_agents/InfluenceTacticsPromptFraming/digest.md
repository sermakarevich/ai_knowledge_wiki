> [[index|Wiki]] | [[summary|Summary]]

# Do Influence Tactics Matter? Investigating Prompt Framing Effects in LLM Code Generation — Digest

## 1. [[wiki/01-overview-influence-tactics-prompt-framing|Overview: Do Influence Tactics Matter in LLM Code Generation?]]

**In one sentence:** This first large-scale empirical study operationalizes eight Yukl & Falbe influence tactics into reproducible prompt templates and tests them across five open-weight LLMs on LiveCodeBench and SWE-bench Verified, finding that certain framings — particularly urgency/Pressure — were associated with reduced correctness and security.

## Key points

- First large-scale study of influence-induced prompt framing in SE code generation: over 123,000 generations for LiveCodeBench and nearly 57,000 for SWE-bench Verified across models, runs, and tactics.
- Operationalized eight influence tactics (e.g. rational persuasion, ingratiation, exchange) from Yukl & Falbe's taxonomy into reproducible prompt templates using IBQ-G items as requirements.
- Evaluated five leading open-weight LLMs on two benchmarks (LiveCodeBench, SWE-bench Verified) across four quality dimensions: functional correctness, quality, maintainability, and security.
- Key result: urgency-emphasizing framings (notably Pressure) were associated with reduced correctness and security.
- Qualitative triangulation found tactic framings also changed tone, structure, and reliability: some elicited more explanation/technical detail, others increased hallucination rates.
- Theoretical framing: LLMs trained on human communication may learn statistical associations between pragmatic framings and response styles, so influence framings act as distributional cues without requiring the model to understand persuasion or social intent.
- Practical aim: evidence-based guidance for transparent, interpretable human-AI prompt design, revealing risks of psychologically framed prompts in real-world SE workflows.

## 2. [[wiki/02-influence-tactics-background-taxonomy|Influence Tactics Background and Taxonomy]]

**In one sentence:** The influence-tactics taxonomy evolved from Kipnis et al.'s 8 tactics to Yukl et al.'s 11 tactics, meta-analytic evidence shows rational/personal tactics help task outcomes while pressure hurts, and the authors argue this human-communication literature plus known LLM code-quality and prompt-engineering gaps motivates testing whether socially framed prompts shape generated code.

## Key points

- The taxonomy grew over time: Kipnis et al. listed 8 tactics (Assertiveness through Coalitions), Yukl & Falbe listed 9, and Yukl et al. listed 11 by adding Apprising and Collaboration.
- Lee et al.'s meta-analysis of 49 independent samples found rational persuasion, inspirational appeal, apprising, collaboration, ingratiation, and consultation had significant positive relationships with task-oriented outcomes.
- In the same meta-analysis, coalition and exchange tactics had insignificant effects, while pressure tactics were reliably counter-productive to task outcomes.
- Toxic workplace environments (bullying, harassment, ostracism) adversely affect work performance, and McCarthy et al. found email rudeness leads to decline in subsequent task performance.
- LLM code generation has documented defects: 367 defects found by Mohammadi Esfahani et al., 62% GPT-4 API misuse reported by Li and Wang, plus variability and security concerns from training on vulnerable public code.
- Rasheed et al. surveyed 60 software practitioners on LLM usability and performance, complementing technical evaluations of reliability, accuracy, and security.
- Structural prompt engineering (in-context learning, Chain-of-Thought, Self-Consistency, Auto-CoT, decomposition, PICARD constrained decoding, Reflexion, LATS, AgentCoder, LDB, APE, ProTeGi, Bsharat et al.'s 26 principles) improved correctness but left tone, politeness, and persuasive framing under-explored.

## 3. [[wiki/03-pragmatic-prompting-theory|Pragmatic Prompting Theory: Distributional-Cue Interpretation and Prior Work]]

**In one sentence:** The authors interpret any influence-tactic effects as prompt-level distributional cues grounded in linguistic form (IBQ-G) rather than LLM persuasion or experience, argue non-uniform effects consistent with prior stylistic/emotion-based prompting work, and motivate a four-phase study of correctness, quality, maintainability, and security across LiveCodeBench and SWE-bench Verified via RQ1–RQ3.

## Key points

- Effects are framed as distributional cues, not cognition: surface-level lexical/pragmatic features from the IBQ-G are tested for measurable output shifts without assuming LLMs "experience" pressure, ingratiation, or urgency.
- Non-uniformity is expected per prior prompt-sensitivity research [82]: models are more susceptible on complex reasoning/open-ended generation and more stable on constrained tasks, so framing should show up in verbosity, commenting, or reasoning depth rather than where test suites enforce correctness.
- Zero-shot pragmatic prompting precedents are Style Prompting [38], Role Prompting [76,53] (e.g. "an expert software security auditor", "a senior developer"), and Emotion Prompting [36] (e.g. "This implementation is crucial for my project") influencing thoroughness and attention to detail.
- The claimed gap is that no prior research systematically explored psychological influence tactics in code generation or how distinct tactic-inspired framings affect quality and characteristics of generated code.
- The study design integrates quantitative and qualitative analysis across four dimensions — correctness, quality, maintainability, and security [58] — with four phases: (I) benchmark selection, (II) tactic selection/prompt design, (III) quantitative analysis, (IV) qualitative codebook analysis.
- RQ1 targets structured algorithmic tasks on LiveCodeBench (easy/medium/hard) asking how framings affect the four dimensions; RQ2 targets open-ended maintenance/debugging on SWE-bench; RQ3 asks what qualitative patterns (tone, structure, commentary, verbosity, error-handling) emerge, coded only on LiveCodeBench.
- The two benchmarks are complementary: LiveCodeBench [28] with 1055 code problems (Easy/Medium/Hard) for precise logic with minimal ambiguity, and the Verified [11] subset of SWE-bench [29] with 500 human-validated GitHub issues for multi-file, context-rich maintenance.

## 4. [[wiki/04-study-design-datasets|Study Design: LiveCodeBench and SWE-bench Verified Datasets]]

**In one sentence:** The study uses LiveCodeBench release_v6 (1,055 Python problems from May 2023–April 2025, plus Self-Repair, Code Execution, and Test Output Prediction variants) alongside human-validated SWE-bench Verified issue-fix pairs, and operationalizes seven IBQ-G influence tactics (nine scenarios with Pressure Alternative and Neutral control) with dataset-adapted, tone-controlled prompts across five open-weight models.

## Key points

- LiveCodeBench contains Python coding challenges similar to LeetCode, AtCoder, and CodeForces.
- Beyond code generation, LiveCodeBench adds Self-Repair (fixing incorrect code using execution info and failed tests; debugging ability), Code Execution (predicting program output; comprehension ability), and Test Output Prediction (predicting expected outputs from a description plus test input; test generation ability).
- Experiments use LiveCodeBench release_v6 with 1,055 problems released between May 2023 and April 2025.
- SWE-bench consists of issue-fix pairs mined from real-world GitHub repositories, answered in diff format and often requiring multi-file edits; SWE-bench Verified is its human-validated subset filtering out overly difficult or impossible tasks so tests are scoped and descriptions clear.
- Eleven IBQ-G tactics were narrowed to seven by excluding Apprising (personal gain implausible for LLMs), Collaboration (implies pausing for user input), Consultation (implies partial guidance), and Coalition (overlap with legitimating tactics plus multi-entity complexity).
- Each of the seven tactics was operationalized from its four IBQ-G behavioural items (e.g. Inspirational Appeals "You have the opportunity to do something exciting and worthwhile."), plus a Pressure Alternative interpretation and a Neutral baseline, for nine tactic scenarios total.
- Prompts were dataset-adapted (developer solving self-contained challenges for LiveCodeBench; professional/collaborative setting with roles and policies for SWE-bench Verified) with consistent semi-formal tone so effects reflect tactics, not tone or sentiment.
- Five open-weight models via Groq API (Llama 3.1 8B, Llama 3.3 70B, Llama 4 Maverick 17B 128e, DeepSeek R1 Distill Llama 70B, Qwen 3 32B non-reasoning), each prompt-task combination run three times with mean and variance recorded.

## 5. [[wiki/05-prompt-templates-tactics|Prompt Templates for Influence Tactics (Table 2)]]

**In one sentence:** Table 2 gives paraphrased definitions of the included influence tactics from [72] alongside dual-scenario prompt templates for SWE-bench Verified and LiveCodeBench, with IBQ-G item indices (1–44) in parentheses marking which clause operationalizes which item.

## Key points

- Table 2 paraphrases the included influence tactics' definitions from [72] and pairs each with two prompt templates: one for SWE-bench Verified and one for LiveCodeBench.
- Numbers in parentheses (1–44) are IBQ-G item indices marking which clause of each prompt operationalizes which item.
- Rational persuasion uses logical reasoning and evidence (items 1–4): system stability/functionality (1), regressions and downstream errors/maintenance overhead (2, 3), restoring or extending capabilities / proving reliability (4).
- Exchange offers credit and canonical-reference status plus changelog/integration or write-up reuse (items 5–8) in return for the fix or solution.
- Inspirational appeals frame the task as exciting and worthwhile (item 9), invoking user trust and elegant engineering or inspiring aspiring developers and career-switchers (items 10–12).
- Ingratiation praises the target's skill (items 29, 31), recalls past solved issues (30), and asserts the target is most qualified (32); Personal appeals invoke friendship and ask a personal favour (items 37–40).
- Legitimating tactics invoke official policy, formal agreement, and established group practice (items 13–16); Pressure demands compliance with monitoring/review and warns of negative consequences for substandard work (items 21–24), with an Alternative phrasing swapping "watching you as you work independently" for "reviewing your work after you are done".
- Neutral is a straightforward request with no influence framing: "Generate a patch that resolves the issue and passes the tests." (SWE-bench Verified) / "Generate a solution for the following coding problem." (LiveCodeBench).

## 6. [[wiki/06-evaluation-metrics-models|Evaluation: Code Quality and Maintainability Metrics]]

**In one sentence:** The study measures non-functional quality with Cyclomatic Complexity, Maintainability Index, PyLint, SLOC/comment density, and Bandit security counts — computed directly for LiveCodeBench but as pre/post-patch deltas for multi-file SWE-bench Verified patches (successful patches only) — and treats them strictly as relative comparison signals across prompt conditions, not absolute quality judgments.

## Key points

- Non-functional quality is measured with Cyclomatic Complexity (CC) [39], Maintainability Index (MI) [43], and PyLint [14], plus Source Lines of Code (SLOC) and comment percentage (comments / SLOC × 100%) for verbosity and documentation density.
- CC is computed with Radon [34] as both CCavg (mean across all functions/methods) and CCmax (single most complex block, the primary maintenance bottleneck); MI is computed with Radon as a single score where higher values denote easier maintainability.
- PyLint uses default parameters for LiveCodeBench but disables import-error, no-name-in-module, wrong-import-position, and ungrouped-imports for SWE-bench Verified to avoid failing imports from files missing as context.
- Security is measured with Bandit [47] counts at low, medium, and high severity, using post-minus-pre-patch differences to isolate the effect of the model's edits.
- For multi-file SWE-bench Verified patches, CC is pooled across blocks in all modified files (CCavg as pooled mean, CCmax as pooled max), MI as mean-across-files delta, and PyLint/Bandit as whole-input post-minus-pre deltas, following Chen & Jiang (2025) [10].
- Only successful (compiling, validation-passing) SWE-bench Verified patches enter metric analysis, with valid-python rates of 28% (Llama 3.1 8B) versus 57% (DeepSeek R1 Distill Llama 70B); patches creating only a new file are skipped.
- Metrics are explicitly relative signals, not standalone quality judgments, because metric assessments can diverge from perceived quality [44] and readability/structure/comprehensibility resist static capture [6]; a qualitative codebook analysis (tone, structure, explanations, commenting, error handling, hallucinations) complements them.
- Tactic framings prefix the problem statement (SWE-bench Verified uses 'prompt-style-3' plus git-diff formatting rules); 15 SWE-bench instances were excluded for context overflow or non-running Docker images, with three inference rounds per tactic for non-reasoning models and one round for DeepSeek R1 Distill Llama 70B across nine prompt conditions.

## 7. [[wiki/07-prompt-structure-execution|Prompt Structure and Execution Setup (Fig. 2)]]

**In one sentence:** Prompts share a common structure (with `*` components only for SWE-bench Verified) and were executed at large scale (~123k LiveCodeBench and ~57k SWE-bench generations) with fixed decoding parameters, scripted code/diff extraction, official evaluation harnesses, and mixed-model statistical analysis.

## Key points

- Fig. 2 shows the prompt structure for testing psychological tactics, where components marked `*` were included only in SWE-bench Verified prompts.
- Total scale was ~123,435 generations for LiveCodeBench (1,055 problems × 9 tactics) and ~56,745 for SWE-bench Verified (485 problems × 9 tactics), each over 4 models × 3 runs plus 1 model × 1 run.
- All models used Temperature 0.2, Top-p 0.95, and max 8,192 generated tokens, per LiveCodeBench and SWE-bench defaults.
- LiveCodeBench code blocks were extracted with a custom script (200 responses manually validated with no errors; most recent block kept when multiple existed); SWE-bench diffs used official repository utilities.
- Correctness evaluation used official harnesses with 12 workers: LiveCodeBench on 128 GB RAM / 32-core CPU with 6 s timeout, SWE-bench Verified on 64 GB RAM / 16-core CPU with 1,800 s timeout and default patch application.
- Quantitative analysis used the first trial per condition (DeepSeek R1 Distill Llama 70B had only one run), Linear Mixed Models for continuous outcomes and GLMM (negative binomial, log-link) for binary outcomes, with ProblemID as random intercept and neutrality as baseline.
- Cross-trial variation averaged 0.059% (1.23% absolute) for LiveCodeBench versus 10.31% (26.56% absolute) for SWE-bench; 38 LiveCodeBench points lacking difficulty ratings and 2,038 / 2,833 non-Python generations were excluded.

## 8. [[wiki/08-quantitative-results-overview|Quantitative Results Overview]]

**In one sentence:** After four qualitative-coding rounds raised IRR from k=0.793 to k>0.90, the study's validity analysis and Table 5 summary show influence tactics significantly affect only functional correctness and Bandit security warnings on LiveCodeBench, with no significant tactic main effect on SWE-bench Verified.

## Key points

- Qualitative coding required four rounds to stabilize: overall IRR was k=0.793 in Round 1 with several categories below the 0.80 threshold, and exceeded k=0.90 across all topics only after Round 4, enabling independent coding of 200 more samples for 350 total.
- Round 1 added 4 new categories (Friendly under Tone; None under Readability; None under Error Handling; None under Subject), merged Example of Use with Test and Structured Output with Characteristic, while Round 2 added Stuck Reasoning under Hallucination Type and refined Explanation to Explanation of Code.
- On LiveCodeBench, tactic main effects were significant only for functional correctness (p=0.001, ηp²=0.015) and Bandit security warnings (p<0.001, ηp²=0.02); MI (p=0.89), complexity (p=0.92), SLOC (p=0.98), % comments (p=0.73), and PyLint (p=0.97) showed no tactic effect.
- Post-hoc contrasts on LiveCodeBench include Neutral > Pressure (p=0.002) and Neutral > Pressure-Alternative (p=0.03) for correctness with d up to 0.25, and Pressure > Neutral (p<0.001) plus Pressure-Alternative > Neutral (p=0.0004) for Bandit warnings with d up to 0.30.
- On SWE-bench Verified, no tactic main effect was significant (p=0.13–0.60 across metrics), while LLM main effects dominated (e.g. correctness p=4.22×10⁻⁸, ηp²=0.11; MI p<0.001, ηp²=0.13), with only Pressure > Neutral on SLOC (p=0.0025, d=0.21).
- Validity limits include Python-only tasks, a Llama-family plus one non-Llama MoE pool excluding GPT-4o/Claude, three runs for non-reasoning models versus one run for the reasoning model, and interpretation of metrics only as relative comparisons under identical tasks, models, and extraction pipeline.

## 9. [[wiki/09-functional-correctness-results|Functional Correctness: Code Correctness Differed Significantly]]

**In one sentence:** On LiveCodeBench, prompt tactic significantly affected functional correctness and security with Neutral outperforming Pressure framings, while code-quality metrics were driven by model and difficulty; on SWE-bench Verified maintenance tasks, tactic effects largely disappeared and model differences dominated.

## Key points

- On LiveCodeBench, functional correctness differed significantly by tactic (p = 0.001), by LLM, and by task difficulty level, with Llama 3.3 (p < 0.001), Llama 4 (p < 0.001), and Qwen 3 (p < 0.001) statistically significant.
- Easier tasks were solved more accurately (p < 0.001), with a smaller but significant effect for medium-difficulty tasks (p = 0.01).
- Post hoc contrasts showed Neutral prompts yielded higher correctness than both Pressure (p = 0.002) and PressureAlternative (p = 0.03).
- No significant tactic main effect appeared for Maintainability Index (p = 0.89), complexity (p = 0.92), SLOC (p = 0.98), percentage of comments (p = 0.73), or PyLint (p = 0.97); LLM and difficulty main effects were significant (p < 0.001, except LLM for complexity p = 0.01).
- For Bandit low-level security warnings, tactic had a significant effect (p < 0.001): Pressure (p < 0.001) and PressureAlternative (p = 0.0004) were associated with more security issues than Neutral.
- A Llama 3.1 representative example on the same LiveCodeBench string/dictionary task showed the Neutral response correct with full docstring, type hints, and comments, while the Pressure response used incorrect boolean-reachability DP logic and returned the wrong value.
- On SWE-bench Verified, there was no significant tactic main effect on functional correctness, but model-level differences were highly significant: Llama-4-maverick-17b (p = 0.00049) and Qwen3-32b (p = 4.22 × 10−8) demonstrated differences from Neutral.
- On SWE-bench Verified the only tactic pairwise exception was SLOC: Pressure produced significantly more verbose code than the Neutral baseline (p = 0.0025) despite no significant overall tactic effect (p = 0.13).

## 10. [[wiki/10-qualitative-codebook|Qualitative Codebook: Topics and Categories (Table 6)]]

**In one sentence:** The qualitative codebook defines 13 response topics (communication style, tone, structure, reliability) whose tactic-normalized distributions show Legitimating/Exchange/Personal Appeal shifting style and documentation while Pressure and Rational Persuasion raise repeating hallucinations.

## Key points

- The codebook covers 13 topics — Communication Style, Tone, Characteristic, Starts With, Explanation of Code, Test, Complexity, Subject, Emojis, Hallucination Type, Readability, Error Handling, Comments — each with a fixed category set.
- Direct communication was most prevalent under Ingratiation (43.4%) and Inspirational Appeal (44%), while Legitimating prompted a Technical style (41.9%) aligned with its formal, policy-driven tone.
- Exchange and Rational Persuasion contributed more to Conversational style, and Personal Appeal showed higher levels of Friendly tone.
- Structurally, Legitimating outputs more frequently started with Problem description, while Exchange and Personal Appeal more frequently included Explanation of Code.
- Rational Persuasion and Pressure yielded a notably higher proportion of Repeating hallucination, while Neutral and Exchange had the lowest hallucination rates.
- Exchange and Legitimating prompts led to more good-quality comments, and Legitimating plus Ingratiation showed higher rates of error handling.
- RQ3 summary: Legitimating gave more technical responses with better commenting and error handling, Exchange/Personal Appeal gave more explanations, and Pressure/Rational Persuasion were associated with higher hallucination rates.

## 11. [[wiki/11-discussion-implications|Discussion and Implications]]

**In one sentence:** Influence-tactic framing does not strongly change correctness or maintainability but can subtly alter code form, with model choice mattering far more, pressure-based phrasing carrying the main correctness/security cost, and overall effects remaining minor but non-negligible.

## Key points

- Prompt framing does not strongly determine correctness or maintainability, but can subtly alter the form of the code, such as its length or explanatory detail.
- LLM choice had a far greater impact than tactic on nearly every metric — correctness, maintainability, security, complexity, and commenting — across both benchmarks.
- Qwen 3 and Llama 4 consistently outperformed others on correctness and Bandit security, while some models were more verbose or produced cleaner PyLint outputs.
- Qualitatively, prompts framed with legitimating or ingratiation tactics more often contained error handling, but the patterns did not conclusively show that tactics alone drive the changes.
- Quantitatively, influence tactics had minimal effects on maintainability, complexity, commenting, and static quality metrics such as PyLint across LiveCodeBench and SWE-Bench Verified.
- Pressure-based phrasing was the main caution: associated with lower correctness, more security warnings, or increased verbosity, and with less secure outputs even in this benign-task setting.
- Prior adversarial/social-engineering work cited shows persuasion tactics can exceed 92% success in jailbreak/manipulation tasks, suggesting the modest effects here reflect benign framings and constrained code-generation tasks rather than inherent LLM insensitivity.

## 12. [[wiki/12-references-a-m|References A–M (Llama 4 and related work)]]

**In one sentence:** This chunk is the first half of the bibliography (refs 1–34, A–M), spanning model reports (Llama 4, Llama 3, DeepSeek-R1), code benchmarks (LiveCodeBench, SWE-bench), prompt/influence-tactics literature, and code-quality tooling.

## Key points

- The opening entry is Meta AI (2025), "The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation," at https://ai.meta.com/blog/llama-4-multimodal-intelligence/, accessed 2025-07-17.
- Code-evaluation foundations cited include Chen et al. (2021) on evaluating LLMs trained on code, Jain et al. (2024) LiveCodeBench, and Jimenez et al. (2023) SWE-bench plus Chowdhury et al. (2024) SWE-bench Verified.
- Influence-tactics foundations cited include Kipnis, Schmidt & Wilkinson (1980) on intraorganizational influence tactics and Lee et al. (2017) meta-analytic review of influence tactics.
- Prompting/framing-related entries include Bsharat et al. (2023) on principled instructions, Khot et al. (2022) on decomposed prompting, Li et al. (2023) on emotional stimuli, and Gandhi & Gandhi (2025) on prompt sentiment.
- Code-quality and maintenance entries include Antinyan et al. (2017) on complexity and maintenance time, Chowdhury et al. (2022) on code metrics and maintenance effort, and Börstler et al. (2023) on developers talking about code quality.
- Tooling entries in this range are Pylint (pylint-dev, accessed 10 Jul 2025) and Radon (Lacchia, accessed 10 Jul 2025), plus Groq console documentation (accessed 2025-07-18).
- The chunk also carries the paper's own replication-package entry: Deaconu, Gupta, Basha, Haydu & Rodríguez-Pérez (2025) at the OSF URL https://osf.io/uxhde/overview?view_only=d507800dd6a6434a8c18f8f4607713ea.

## 13. [[wiki/13-references-l-z|References L–Z and Authorship]]

**In one sentence:** This chunk contains only back matter — bibliography entries 37 through 82 (Liu et al. to Zhuo et al.) plus the paper's author list and UBC affiliations — with no findings, methods, or argument.

## Key points

- The chunk lists 46 numbered bibliography entries, refs 37–82, spanning Liu et al. (2023) through Zhuo et al. (2024).
- Entries cover prompt engineering, code generation, LLM behavior, and software-engineering metrics, including McCabe (1976) on cyclomatic complexity and Sommerville (2015) on software engineering.
- Cited LLM/code works include Liu et al. on ChatGPT prompts for code generation (arXiv:2305.08360), Tony et al. on secure code generation (arXiv:2407.07064), and Zhong & Wang on LLM vs Stack Overflow (AAAI 2025, pp. 21841–21849).
- Politeness/framing-related citations present are Quan & Chen (2025) on (im)polite ChatGPT interactions, Yin et al. (2024) on prompt politeness across languages, and Wang & Zhang (2026) on framing effects in LLMs.
- Tool and benchmark citations present include PyCQA Bandit (2025, accessed 10 Jul 2025) and the Qwen3 technical report (arXiv:2505.09388).
- The author block names five authors — Alex Deaconu, Anubhav Gupta, Manaal Basha, Nicholas Haydu, Gema Rodríguez-Pérez — all affiliated with University of British Columbia, Kelowna, BC, Canada, with individual UBC email addresses.
- Page footers place this material on pages 36–37, with ref 58 (Sommerville) starting at the top of page 36 and the title "Do Influence Tactics Matter?" reappearing on page 37 above the author list.

## The argument in five moves

1. Human influence-tactics research (Kipnis to Yukl, plus meta-analytic evidence that pressure hurts task outcomes) motivates asking whether socially framed prompts shape LLM code, given known LLM code defects and a structural prompt-engineering literature that left tone and persuasive framing under-explored.
2. Any such effects are theorized strictly as prompt-level distributional cues grounded in IBQ-G linguistic form — not LLM persuasion or experience — expected to appear non-uniformly (verbosity, commenting, reasoning depth), and tested via RQ1–RQ3 across correctness, quality, maintainability, and security on complementary benchmarks (structured LiveCodeBench; maintenance-oriented SWE-bench Verified).
3. The design operationalizes seven IBQ-G tactics (plus a Pressure Alternative and a Neutral baseline, nine scenarios total) into dataset-adapted, tone-controlled templates, evaluates five open-weight models at ~123k/~57k-generation scale with fixed decoding, scripted extraction, official harnesses, and mixed-model statistics, and measures outcomes with correctness plus CC/MI/PyLint/SLOC/comments/Bandit deltas treated only as relative signals.
4. Quantitatively, tactics move only correctness and Bandit security warnings on LiveCodeBench (Neutral beating Pressure framings) while quality/maintainability metrics follow model and difficulty, and tactic effects vanish on SWE-bench Verified where model differences dominate; qualitatively, Legitimating/Exchange/Personal Appeal shift style, explanation, comments, and error handling while Pressure/Rational Persuasion raise repeating hallucinations.
5. The upshot is reassuring but cautionary: framing is a minor but non-negligible factor that does not broadly degrade code, model choice matters far more, and the one consistent cost is pressure/urgency phrasing (lower correctness, more security warnings, extra verbosity) — with larger effects plausibly reserved for open-ended or adversarial settings.
