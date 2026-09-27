# Plan — DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging

Source: https://arxiv.org/abs/2604.19305v1 (pdf via pdftotext; source.pdf not copied, 3.8 MB > 2 MB limit)
Chunks: 15 (bodies in `/Users/sergii/.fleet/workflows/summarise/wfr-b6791toc/chunks/*.md`, for later workers)

| Chunk slug | Planned wiki page | Covers |
|---|---|---|
| 01-debugrepair-enhancing-llm-based-automated-progra | 01-framework-overview.md | Covers paper abstract and DebugRepair framework introduction (problem, three components, claimed results). |
| 02-is-imperative-to-augment-llm-based-apr | 02-background-and-limitations.md | Covers background on LLM-based APR paradigms and the limitation of outcome-level failure symptoms. |
| 03-2-motivation-in-this-section-we | 03-motivation-example.md | Covers motivating Chart-24 bug example: symptom-only repair failure vs runtime-state debugging. |
| 04-timeseries-s1-new-timeseries-s1-insert | 04-framework-workflow.md | Covers framework workflow overview (Fig. 2) and test purification illustration with TimeSeries example. |
| 05-dependencies-lines-15-and-17-besides | 05-test-semantic-purification.md | Covers test semantic purification algorithm: backward slicing, alias handling, dependency resolution. |
| 06-please-add-appropriate-debugging-print-statement | 06-simulated-instrumentation.md | Covers simulated instrumentation: LLM-inserted debugging print statements with rule-based fallback. |
| 07-test-context-test-fix-may-involve | 07-conversational-repair.md | Covers debugging-driven conversational repair: hierarchical iterative loops, prompts, validation. |
| 08-4-3-baselines-to-make-a-comprehensive | 08-evaluation-setup.md | Covers evaluation setup: benchmarks (Defects4J, QuixBugs, HumanEval-Java) and 15 baselines. |
| 09-datasets-this-exceptional-performance-matches-th | 09-main-results.md | Covers main repair results across benchmarks and backbone LLMs vs SOTA baselines. |
| 10-j-acm-vol-37-no-4 | 10-results-analysis.md | Covers continued results analysis and per-benchmark/model breakdown discussion. |
| 11-to-tsapr-and-can-be-integrated | 11-comparison-and-generality.md | Covers comparison with TSAPR, integration discussion, and model-agnostic generality. |
| 12-effectiveness-of-test-purification-removing-test | 12-ablation-test-purification.md | Covers ablation on test purification component effectiveness. |
| 13-140-repair-rounds-kround-1 | 13-ablation-repair-rounds.md | Covers ablation on repair rounds/budget hyperparameters and debugging mechanism contribution. |
| 14-references-1-n-d-models | 14-conclusion-and-references-a.md | Covers conclusion, open-science note, and first half of references. |
| 15-33-yunkun-wang-yue-zhang-guochang | 15-references-b.md | Covers second half of references. |
