---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Do Influence Tactics Matter? Investigating Prompt Framing Effects in LLM Code Generation

### Q1. What research question, scale, and headline finding define this study?

> [!tip]- Answer
> The study asks to what extent prompt framings inspired by Yukl & Falbe influence tactics produce measurable differences in LLM-generated code, testing operationalized tactic templates across five open-weight LLMs on LiveCodeBench and SWE-bench Verified at ~123,000 and ~57,000 generations respectively. Its headline finding is that urgency-emphasizing framings, notably Pressure, were associated with reduced correctness and security, alongside qualitative shifts in tone, structure, and hallucination rates. See [[wiki/01-overview-influence-tactics-prompt-framing|Overview]].

### Q2. How did the influence-tactics taxonomy evolve from Kipnis et al. to Yukl et al.?

> [!tip]- Answer
> Kipnis et al. factor-analyzed manager reports into eight tactics (Assertiveness through Coalitions), Yukl & Falbe's IBQ work updated this to nine (adding Consultation, Inspirational appeals, and reframing others), and Yukl et al. extended it to eleven by adding Apprising and Collaboration, with confirmatory factor analysis supporting the expanded structure. The study builds its prompt templates on the refined IBQ-G instrument from this lineage. See [[wiki/02-influence-tactics-background-taxonomy|Taxonomy]].

### Q3. What meta-analytic evidence and LLM-code gaps motivate testing influence framings on code generation?

> [!tip]- Answer
> Lee et al.'s meta-analysis of 49 samples found rational persuasion, inspirational appeal, apprising, collaboration, ingratiation, and consultation helped human task outcomes while pressure was reliably counter-productive, and since LLMs train on human communication it is reasonable to ask whether these framings shape model outputs. The gap is concrete: LLM code shows documented defects (367 defects, 62% GPT-4 API misuse, vulnerable-training-data risks) while prompt engineering focused on logical structure (CoT, decomposition, PICARD, Reflexion, APE) left tone, politeness, and persuasive framing under-explored. See [[wiki/02-influence-tactics-background-taxonomy|Taxonomy]].

### Q4. What does the distributional-cue interpretation claim, and what does it explicitly deny?

> [!tip]- Answer
> It claims influence framings act as surface-level lexical/pragmatic cues whose training-data co-occurrence with response styles can steer outputs, with non-uniform effects expected mainly where models have interpretive flexibility (verbosity, commenting, reasoning depth) rather than where test suites constrain correctness. It explicitly denies that LLMs experience pressure, ingratiation, or urgency or understand persuasion in any psychologically meaningful sense, grounding hypotheses only in IBQ-G linguistic form. See [[wiki/03-pragmatic-prompting-theory|Pragmatic Prompting Theory]].

### Q5. What are RQ1–RQ3, the four quality dimensions, and the four study phases?

> [!tip]- Answer
> RQ1 asks how tactic framings affect correctness, quality, maintainability, and security on structured LiveCodeBench tasks (easy/medium/hard); RQ2 asks the same for open-ended SWE-bench maintenance/debugging; RQ3 asks which qualitative patterns (tone, structure, commentary, verbosity, error handling) emerge, coded only on LiveCodeBench. The design runs four phases — benchmark selection, tactic selection/prompt design, quantitative analysis, qualitative codebook analysis — over the two complementary benchmarks. See [[wiki/03-pragmatic-prompting-theory|Pragmatic Prompting Theory]].

### Q6. What datasets, tactic exclusions, and models make up the study design?

> [!tip]- Answer
> The study uses LiveCodeBench release_v6 (1,055 Python problems from May 2023–April 2025, plus Self-Repair, Code Execution, and Test Output Prediction variants) and human-validated SWE-bench Verified issue-fix pairs requiring multi-file diffs. Four of eleven IBQ-G tactics were excluded — Apprising, Collaboration, Consultation, Coalition — leaving seven tactics plus a Pressure Alternative and Neutral baseline (nine scenarios), tested on five open-weight models via Groq (Llama 3.1 8B, Llama 3.3 70B, Llama 4 Maverick 17B 128e, DeepSeek R1 Distill Llama 70B, Qwen 3 32B non-reasoning) with three runs per condition. See [[wiki/04-study-design-datasets|Study Design]].

### Q7. How does Table 2 operationalize each tactic, and how do Pressure framings differ from Neutral?

> [!tip]- Answer
> Each tactic is paraphrased from its definition and instantiated as dual dataset-specific templates whose clauses carry IBQ-G item indices (1–44), e.g. rational persuasion cites stability/regressions (items 1–4), exchange offers credit and canonical-reference status (5–8), and legitimating invokes policy and group practice (13–16). Pressure demands compliance with monitoring and warns of negative consequences (items 21–24), with the Alternative swapping "watching you as you work" for "reviewing your work after you are done," while Neutral is a bare request with no framing. See [[wiki/05-prompt-templates-tactics|Prompt Templates]].

### Q8. Which metrics and tools are used, how are SWE-bench patches aggregated, and how must results be read?

> [!tip]- Answer
> Non-functional quality uses Cyclomatic Complexity (CCavg/CCmax via Radon), Maintainability Index (higher is easier), PyLint (with import checks disabled for SWE-bench), SLOC and comment percentage, plus Bandit low/medium/high severity counts. SWE-bench Verified metrics are post-minus-pre-patch deltas pooled across modified files (following Chen & Jiang 2025), restricted to successful compiling patches, and all metrics are strictly relative comparison signals across prompt conditions, never absolute quality judgments. See [[wiki/06-evaluation-metrics-models|Evaluation Metrics]].

### Q9. What was the execution scale, decoding/extraction setup, and statistical model?

> [!tip]- Answer
> Totals reach ~123,435 LiveCodeBench and ~56,745 SWE-bench Verified generations (1,055 and 485 problems × 9 tactics × 4 models × 3 runs plus one single-run reasoning model), all at Temperature 0.2, Top-p 0.95, max 8,192 tokens, with scripted code-block/diff extraction and official harnesses (6 s vs 1,800 s timeouts, 12 workers). Analysis uses the first trial per condition with Linear Mixed Models (continuous) and negative-binomial GLMMs (binary), ProblemID as random intercept, Neutrality as baseline, and Bonferroni-corrected post-hoc contrasts. See [[wiki/07-prompt-structure-execution|Execution Setup]].

### Q10. Which tactic effects were significant on each benchmark, and what limits validity?

> [!tip]- Answer
> On LiveCodeBench only functional correctness (p=0.001, ηp²=0.015) and Bandit warnings (p<0.001, ηp²=0.02) showed tactic main effects — Neutral beating both Pressure framings on correctness, Pressure exceeding Neutral on warnings — while MI, complexity, SLOC, comments, and PyLint did not; on SWE-bench Verified no tactic main effect was significant (p=0.13–0.60) and LLM effects dominated. Limits include Python-only tasks, a Llama-heavy pool excluding GPT-4o/Claude, one run for the reasoning model, and metrics read only as relative signals. See [[wiki/08-quantitative-results-overview|Results Overview]].

### Q11. How did Neutral vs Pressure compare on correctness and security, and what is the SWE-bench exception?

> [!tip]- Answer
> On LiveCodeBench, Neutral prompts yielded higher correctness than Pressure (p=0.002) and Pressure-Alternative (p=0.03), while both Pressure framings produced more Bandit low-severity warnings than Neutral (p<0.001, p=0.0004); a Llama 3.1 example shows Neutral giving correct documented DP code where Pressure gave wrong boolean-reachability logic with poor comments. On SWE-bench Verified, tactic had no correctness effect and the sole pairwise exception was SLOC, where Pressure produced more verbose code than Neutral (p=0.0025) despite a non-significant overall tactic effect. See [[wiki/09-functional-correctness-results|Functional Correctness]].

### Q12. What are the 13 codebook topics and the main tactic-linked qualitative patterns?

> [!tip]- Answer
> The codebook codes Communication Style, Tone, Characteristic, Starts With, Explanation of Code, Test, Complexity, Subject, Emojis, Hallucination Type, Readability, Error Handling, and Comments, reaching k>0.90 agreement after four refinement rounds. Tactic-normalized patterns show Legitimating as more technical with better comments and error handling, Exchange/Personal Appeal giving more explanations, Ingratiation/Inspirational Appeal as more direct, and Pressure/Rational Persuasion with higher repeating-hallucination rates versus lowest rates under Neutral/Exchange. See [[wiki/10-qualitative-codebook|Qualitative Codebook]].

### Q13. What practical implications follow — model choice, pressure caution, and scope caveats?

> [!tip]- Answer
> Model choice dwarfed tactic effects on nearly every metric (Qwen 3 and Llama 4 leading correctness/security), so developers should prioritize model selection while treating framing as a subtle stylistic layer, usable cautiously for documentation-heavy outputs but unreliable as a control method. The one consistent caution is avoiding coercive or urgency-based wording, linked to lower correctness, more security warnings, or extra verbosity even on benign tasks — modest here likely because tasks are constrained, unlike adversarial settings where persuasion tactics exceed 92% jailbreak success. See [[wiki/11-discussion-implications|Discussion]].

### Q14. Which A–M references anchor the benchmarks, influence literature, tooling, and replication?

> [!tip]- Answer
> Benchmark foundations are Jain et al. LiveCodeBench, Jimenez et al. SWE-bench, and Chowdhury et al. SWE-bench Verified; influence foundations are Kipnis, Schmidt & Wilkinson (1980) and Lee et al. (2017); tooling entries are PyLint, Radon, and Groq docs, with framing-adjacent cites such as Li et al. on emotional stimuli and Gandhi & Gandhi on prompt sentiment. The chunk also carries the paper's own replication package (Deaconu et al. 2025, OSF) — the reproducibility artifact behind the templates and scripts. See [[wiki/12-references-a-m|References A–M]].

### Q15. What does the L–Z back matter contain, and who authored the paper?

> [!tip]- Answer
> It lists refs 37–82 from Liu et al. through Zhuo et al., covering prompt engineering, code generation, and metrics (McCabe 1976, Sommerville 2015), politeness/framing cites (Quan & Chen 2025; Yin et al. 2024; Wang & Zhang 2026), and tool/model cites (Bandit, Qwen3 report) — back matter with no findings of its own. Authorship is five UBC Kelowna researchers: Alex Deaconu, Anubhav Gupta, Manaal Basha, Nicholas Haydu, and Gema Rodríguez-Pérez. See [[wiki/13-references-l-z|References L–Z]].

### Q16 (evaluation). Your team ships an LLM coding assistant and developers routinely prompt it with urgency ("you must finish this, I am watching you"). What prompt policy should you adopt from this paper, and what should you refuse to claim?

> [!tip]- Answer
> Adopt a policy banning coercive/urgency phrasing in default templates and high-stakes flows, since Pressure framings were the one consistent cost (lower LiveCodeBench correctness, more Bandit warnings, extra SWE-bench verbosity), while prioritizing model selection over framing tweaks and treating legitimating/exchange styles only as weak stylistic nudges. Refuse to claim that neutral phrasing guarantees secure or correct code, that framing fixes maintainability, or that these benign-task results transfer to adversarial settings where persuasion effects are far stronger. See [[wiki/11-discussion-implications|Discussion]].
